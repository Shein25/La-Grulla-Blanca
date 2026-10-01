export const ADAPTER_STATUS='EXPERIMENTAL_NEW_ENGINE_ONLY';
export const ENGINE_CONTRACT='NEW_COMBAT_STATS_V0_1';
export const READY='READY';

export const HARNESS_DEFAULT_ASSIGNMENT=Object.freeze({profileId:'INSTINTIVO',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})});

export const PROFILE_ASSIGNMENTS=Object.freeze({
  rata_qi:Object.freeze({profileId:'INSTINTIVO',socialProfileId:'COLONIA',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})}),
  serpiente_qi:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:0.9,CONTROL:1.1})}),
  lobo_espiritual:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'MANADA',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})}),
  devorador_niebla:Object.freeze({profileId:'TACTICO_3',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})}),
  mantis_nube:Object.freeze({profileId:'MASTER_4',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:1.1,CONTROL:1.0})})
});

export function assertMonsterDefinition(id,def){
  if(!id||!def||typeof def!=='object')throw new TypeError('monster definition invalid');
  if(def.id!==id)throw new TypeError(`${id}.id mismatch`);
  if(def.engine_contract!==ENGINE_CONTRACT)throw new TypeError(`${id}.engine_contract invalid`);
  if(typeof def.name!=='string'||!def.name)throw new TypeError(`${id}.name invalid`);
  return true;
}

export function assertMonsterCombatReady(id,def){
  assertMonsterDefinition(id,def);
  if(def.stats_status!==READY)throw new Error(`${id}: T0 stats are not READY`);
  const required=['hp','qi_max','precision','evasion','defense','tenacity','control','crit_chance','crit_damage','basic_damage'];
  for(const key of required){
    if(def.stats?.[key]===null||def.stats?.[key]===undefined)throw new Error(`${id}.stats.${key} unresolved`);
  }
  if(def.technique){
    if(def.technique.params_status!==READY)throw new Error(`${id}: technique params are not READY`);
    if(!Number.isInteger(def.technique.params?.cadence)||def.technique.params.cadence<1){
      throw new Error(`${id}: technique cadence unresolved`);
    }
  }
  return true;
}

export function techniqueDue(def,round){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round must be integer >= 0');
  assertMonsterCombatReady(def.id,def);
  return !!(def.technique && round % def.technique.params.cadence===0);
}

export function techniqueWarning(def,round){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round must be integer >= 0');
  assertMonsterCombatReady(def.id,def);
  return !!(def.technique && (round+1)%def.technique.params.cadence===0);
}

export function canonicalAbilityIds(mobId){
  return {basic:`${mobId}__basic`,technique:`${mobId}__technique`};
}

function techniqueCategory(t){
  const mechanics=new Set(t?.mechanics||[]);
  return mechanics.has('POISON_DOT')||mechanics.has('BURN_DOT')||mechanics.has('QI_DRAIN')?'CONTROL':'OFENSIVA';
}

export function buildCanonicalAbilityCatalog(mobId,def){
  assertMonsterDefinition(mobId,def);
  const ids=canonicalAbilityIds(mobId);
  const out={
    [ids.basic]:{
      id:ids.basic,
      intentCategory:'OFENSIVA',
      tags:['BASE_ATTACK'],
      telegraph:`Ataque básico de ${def.name}.`,
      requirements:{signalsAll:[]},
      utility:{base:40,signalWeights:{},memoryWeights:{},socialWeights:{}}
    }
  };
  if(def.technique){
    const effects=[];
    const mechanics=new Set(def.technique.mechanics||[]);
    if(mechanics.has('POISON_DOT'))effects.push('VENENO');
    if(mechanics.has('BURN_DOT'))effects.push('QUEMADURA');
    if(mechanics.has('QI_DRAIN'))effects.push('DRENA_QI');
    out[ids.technique]={
      id:ids.technique,
      intentCategory:techniqueCategory(def.technique),
      tags:['MONSTER_TECHNIQUE',...effects],
      telegraph:`${def.technique.name}.`,
      requirements:{signalsAll:[]},
      utility:{base:60,signalWeights:{},memoryWeights:{},socialWeights:{}}
    };
  }
  return out;
}

export function buildMonsterInput({mobId,def,round,mode='CADENCE_COMPAT',recentAbilityIds=[]}){
  assertMonsterCombatReady(mobId,def);
  const assignment=PROFILE_ASSIGNMENTS[mobId] || (mode==='CADENCE_COMPAT' ? HARNESS_DEFAULT_ASSIGNMENT : null);
  if(!assignment)throw new RangeError(`no experimental profile for ${mobId}`);
  const ids=canonicalAbilityIds(mobId);
  const due=techniqueDue(def,round);
  let effectiveKit;
  if(!def.technique) effectiveKit=[ids.basic];
  else if(mode==='CADENCE_COMPAT') effectiveKit=due?[ids.technique]:[ids.basic];
  else if(mode==='DECISION_EXPERIMENTAL') effectiveKit=due?[ids.basic,ids.technique]:[ids.basic];
  else throw new RangeError(`unknown mode: ${mode}`);

  return {
    id:mobId,
    profileId:assignment.profileId,
    socialProfileId:assignment.socialProfileId,
    effectiveKit,
    preferences:{...assignment.preferences},
    recentAbilityIds:[...recentAbilityIds],
    cooldowns:{}
  };
}

export function baseCombat(round,{selfHp=1,playerHp=1,signals={}}={}){
  return {
    round,
    self:{hpRatio:selfHp,statuses:[]},
    player:{hpRatio:playerHp,visibleStates:[]},
    signals:{...signals}
  };
}

export function neutralSocial(){
  return {alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false};
}

export function seededRng(seed){
  let a=seed>>>0;
  return {random(){
    a|=0;a=(a+0x6d2b79f5)|0;
    let t=Math.imul(a^(a>>>15),1|a);
    t=(t+Math.imul(t^(t>>>7),61|t))^t;
    return ((t^(t>>>14))>>>0)/4294967296;
  }};
}
