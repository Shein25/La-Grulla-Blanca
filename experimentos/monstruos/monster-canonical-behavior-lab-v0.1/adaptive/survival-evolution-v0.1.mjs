import {PROFILES} from '../vendor/profiles.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,techniqueDue} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay} from '../tactics/tactical-overlay-v0.1.mjs';

export const SURVIVAL_EVOLUTION_STATUS='EXPERIMENTAL_NON_CANONICAL_SURVIVAL_V01';

const nextProfile=Object.freeze({
  INSTINTIVO:'REACTIVO_1',
  REACTIVO_1:'CAZADOR_2',
  CAZADOR_2:'TACTICO_3',
  TACTICO_3:'MASTER_4',
  MASTER_4:'MASTER_4'
});

const p=(name,effect,extra={})=>Object.freeze({
  name,
  effect:Object.freeze(effect),
  ...extra
});

export const SURVIVAL_POLICIES=Object.freeze({
  rata_qi:p('Reflejo de Madriguera',{kind:'EVADE_NEXT',evasionBonus:25,durationActions:1,cooldownRounds:2}),
  serpiente_qi:p('Muda del Cauce',{kind:'EVADE_NEXT',evasionBonus:20,durationActions:1,cooldownRounds:2}),
  lobo_espiritual:p('Paso de la Cola Vigilante',{kind:'EVADE_NEXT',evasionBonus:20,durationActions:1,cooldownRounds:2},
    {socialWeights:Object.freeze({MANADA_WITH_ALLY:-4})}),
  eco_caido:p('Guardia del Último Ensayo',{kind:'MITIGATE_NEXT',damageReductionPct:35,durationHits:1,cooldownRounds:2}),
  pez_lunar:p('Giro de Corriente Ciega',{kind:'EVADE_NEXT',evasionBonus:20,durationActions:1,cooldownRounds:2}),
  sombra_ahogada:p('Disolverse en Marea',{kind:'MITIGATE_NEXT',damageReductionPct:30,durationHits:1,cooldownRounds:2}),
  centinela_pluma:p('Cierre de Plumas Pétreas',{kind:'MITIGATE_NEXT',damageReductionPct:35,durationHits:1,cooldownRounds:2},
    {socialWeights:Object.freeze({TERRITORIAL_SOLO:3})}),
  devorador_niebla:p('Cuerpo de Bruma Replegada',{kind:'MITIGATE_NEXT',damageReductionPct:30,durationHits:1,cooldownRounds:2}),
  avispa_jade:p('Quiebro de Jade',{kind:'EVADE_NEXT',evasionBonus:25,durationActions:1,cooldownRounds:2},
    {socialWeights:Object.freeze({COLONIA_WITH_ALLY:-4})}),
  mono_pildoras:p('Salto del Ladrón',{kind:'EVADE_NEXT',evasionBonus:20,durationActions:1,cooldownRounds:2},
    {socialWeights:Object.freeze({OPORTUNISTA_LOW_HP:-5})}),
  sapo_ceniza:p('Piel de Brasa Muerta',{kind:'MITIGATE_NEXT',damageReductionPct:30,durationHits:1,cooldownRounds:2},
    {socialWeights:Object.freeze({TERRITORIAL_SOLO:3})}),
  sapo_caldera:p('Cierre de las Tres Gargantas',{kind:'MITIGATE_NEXT',damageReductionPct:35,durationHits:1,cooldownRounds:2},
    {socialWeights:Object.freeze({TERRITORIAL_SOLO:3})}),
  escarabajo_hierro:p('Cierre de Caparazón',{kind:'MITIGATE_NEXT',damageReductionPct:40,durationHits:1,cooldownRounds:2},
    {socialWeights:Object.freeze({COLONIA_WITH_ALLY:-3})}),
  rey_escarabajo:p('Diagrama de Placas',{kind:'MITIGATE_NEXT',damageReductionPct:40,durationHits:1,cooldownRounds:2},
    {socialWeights:Object.freeze({COLONIA_WITH_ALLY:-3})}),
  anguila_estelar:p('Desliz de Meridiano',{kind:'EVADE_NEXT',evasionBonus:20,durationActions:1,cooldownRounds:2}),
  guardian_coral:p('Arrecife Replegado',{kind:'MITIGATE_NEXT',damageReductionPct:35,durationHits:1,cooldownRounds:2},
    {socialWeights:Object.freeze({TERRITORIAL_SOLO:3})}),
  halcon_tormenta:p('Ascenso Contraviento',{kind:'EVADE_NEXT',evasionBonus:25,durationActions:1,cooldownRounds:2}),
  mantis_nube:p('Velo de Nube Cortada',{kind:'EVADE_NEXT',evasionBonus:20,durationActions:1,cooldownRounds:2})
});

export function survivalAbilityId(mobId){
  return `${mobId}__survival_1`;
}

export function adaptationXpGain({rounds,reachedLowHp=false,heavyHitObserved=false}={}){
  if(!Number.isInteger(rounds)||rounds<0)throw new TypeError('rounds debe ser entero >= 0');
  if(rounds===0)return 0;
  return 1 + ((reachedLowHp||heavyHitObserved)?1:0);
}

export function survivalUnlockXp(def){
  if(!def||typeof def!=='object')throw new TypeError('def inválida');
  return def.unico?4:6;
}

export function survivalEvolutionStage({mobId,def,survivalXp}){
  if(!SURVIVAL_POLICIES[mobId])throw new RangeError(`sin política de supervivencia para ${mobId}`);
  if(!Number.isSafeInteger(survivalXp)||survivalXp<0)throw new TypeError('survivalXp debe ser entero seguro >= 0');
  return survivalXp>=survivalUnlockXp(def)?1:0;
}

export function buildSurvivalAbilityCatalog({mobId,def,stage}){
  if(!SURVIVAL_POLICIES[mobId])throw new RangeError(`sin política de supervivencia para ${mobId}`);
  if(stage!==0&&stage!==1)throw new RangeError('stage de supervivencia inválido');

  const out=applyTacticalOverlay(mobId,buildCanonicalAbilityCatalog(mobId,def));
  if(stage===0)return out;

  const policy=SURVIVAL_POLICIES[mobId];
  const id=survivalAbilityId(mobId);
  out[id]={
    id,
    intentCategory:'DEFENSA',
    tags:['EXPERIMENTAL_NON_CANONICAL','SURVIVAL_EVOLUTION_1',policy.effect.kind],
    telegraph:`${policy.name}.`,
    cooldownKey:`${id}__cooldown`,
    requirements:{signalsAll:[]},
    utility:{
      base:18,
      signalWeights:{
        SELF_LOW_HP:22,
        TOOK_HEAVY_HIT:10,
        PLAYER_LOW_HP:3
      },
      memoryWeights:{},
      socialWeights:{...(policy.socialWeights||{})}
    }
  };
  return out;
}

export function buildSurvivalMonsterInput({
  mobId,def,round,survivalXp,mode='DECISION_EXPERIMENTAL',
  recentAbilityIds=[],survivalCooldown=false
}){
  const stage=survivalEvolutionStage({mobId,def,survivalXp});
  const base=buildCandidateMonsterInput({mobId,def,round,mode,recentAbilityIds});
  if(stage===0)return {...base,adaptiveStage:0};

  const assignmentProfile=base.profileId;
  const evolvedProfileId=nextProfile[assignmentProfile];
  if(!PROFILES[evolvedProfileId])throw new RangeError(`perfil evolucionado inválido: ${evolvedProfileId}`);

  const survivalId=survivalAbilityId(mobId);
  const due=techniqueDue(def,round);
  let effectiveKit;

  if(mode==='CADENCE_COMPAT'&&def.tecnica&&due){
    // La técnica canónica sigue siendo obligatoria en su ronda.
    effectiveKit=[canonicalAbilityIds(mobId).technique];
  }else{
    effectiveKit=[canonicalAbilityIds(mobId).basic,survivalId];
    if(mode==='DECISION_EXPERIMENTAL'&&def.tecnica&&due){
      effectiveKit.splice(1,0,canonicalAbilityIds(mobId).technique);
    }
  }

  return {
    ...base,
    profileId:evolvedProfileId,
    effectiveKit,
    preferences:{...base.preferences,DEFENSA:1},
    cooldowns:{...base.cooldowns,[`${survivalId}__cooldown`]:!!survivalCooldown},
    adaptiveStage:1
  };
}

export function survivalPolicyView(mobId){
  const x=SURVIVAL_POLICIES[mobId];
  if(!x)return null;
  return Object.freeze({
    mobId,
    abilityId:survivalAbilityId(mobId),
    name:x.name,
    effect:x.effect
  });
}
