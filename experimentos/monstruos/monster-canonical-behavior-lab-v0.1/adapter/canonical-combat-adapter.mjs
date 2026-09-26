export const ADAPTER_STATUS='EXPERIMENTAL_NON_CANONICAL';

export const HARNESS_DEFAULT_ASSIGNMENT=Object.freeze({profileId:'INSTINTIVO',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})});

export const PROFILE_ASSIGNMENTS=Object.freeze({
  rata_qi:Object.freeze({profileId:'INSTINTIVO',socialProfileId:'COLONIA',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})}),
  serpiente_qi:Object.freeze({profileId:'REACTIVO_1',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:0.9,CONTROL:1.1})}),
  lobo_espiritual:Object.freeze({profileId:'CAZADOR_2',socialProfileId:'MANADA',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})}),
  devorador_niebla:Object.freeze({profileId:'TACTICO_3',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:1.0,CONTROL:1.0})}),
  mantis_nube:Object.freeze({profileId:'MASTER_4',socialProfileId:'SOLITARIO',preferences:Object.freeze({OFENSIVA:1.1,CONTROL:1.0})})
});

function assertMob(id,def){
  if(!id||!def||typeof def!=='object')throw new TypeError('mob canónico inválido');
  if(typeof def.daño!=='string')throw new TypeError(`${id}.daño inválido`);
  if(def.tecnica&&(!Number.isInteger(def.tecnica.cada)||def.tecnica.cada<1))throw new TypeError(`${id}.tecnica.cada inválido`);
}

export function techniqueDue(def,round){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round debe ser entero >= 0');
  return !!(def.tecnica && round % def.tecnica.cada===0);
}

export function techniqueWarning(def,round){
  if(!Number.isInteger(round)||round<0)throw new TypeError('round debe ser entero >= 0');
  return !!(def.tecnica && (round+1)%def.tecnica.cada===0);
}

export function canonicalAbilityIds(mobId){
  return {basic:`${mobId}__basic`,technique:`${mobId}__technique`};
}

function techniqueCategory(t){
  return t&&(t.veneno||t.quemadura||t.drenaQi)?'CONTROL':'OFENSIVA';
}

export function buildCanonicalAbilityCatalog(mobId,def){
  assertMob(mobId,def);
  const ids=canonicalAbilityIds(mobId);
  const out={
    [ids.basic]:{
      id:ids.basic,
      intentCategory:'OFENSIVA',
      tags:['CANON_BASE_ATTACK'],
      telegraph:`Ataque básico de ${def.name} (${def.daño}).`,
      requirements:{signalsAll:[]},
      utility:{base:40,signalWeights:{},memoryWeights:{},socialWeights:{}}
    }
  };
  if(def.tecnica){
    const effects=[];
    if(def.tecnica.veneno)effects.push('VENENO');
    if(def.tecnica.quemadura)effects.push('QUEMADURA');
    if(def.tecnica.drenaQi)effects.push('DRENA_QI');
    out[ids.technique]={
      id:ids.technique,
      intentCategory:techniqueCategory(def.tecnica),
      tags:['CANON_TECHNIQUE',...effects],
      telegraph:`${def.tecnica.name}.`,
      requirements:{signalsAll:[]},
      utility:{base:60,signalWeights:{},memoryWeights:{},socialWeights:{}}
    };
  }
  return out;
}

export function buildMonsterInput({mobId,def,round,mode='CADENCE_COMPAT',recentAbilityIds=[]}){
  assertMob(mobId,def);
  const assignment=PROFILE_ASSIGNMENTS[mobId] || (mode==='CADENCE_COMPAT' ? HARNESS_DEFAULT_ASSIGNMENT : null);
  if(!assignment)throw new RangeError(`sin perfil experimental para ${mobId}`);
  const ids=canonicalAbilityIds(mobId);
  const due=techniqueDue(def,round);
  let effectiveKit;
  if(!def.tecnica) effectiveKit=[ids.basic];
  else if(mode==='CADENCE_COMPAT') effectiveKit=due?[ids.technique]:[ids.basic];
  else if(mode==='DECISION_EXPERIMENTAL') effectiveKit=due?[ids.basic,ids.technique]:[ids.basic];
  else throw new RangeError(`mode desconocido: ${mode}`);

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
