import {PROFILES} from '../vendor/profiles.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,techniqueDue} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay} from '../tactics/tactical-overlay-v0.1.mjs';

export const SURVIVAL_EVOLUTION_STATUS='EXPERIMENTAL_NEW_ENGINE_PENDING_NUMERIC_CALIBRATION_V02';
export const ADAPTIVE_PARAMS_STATUS='PENDING_T0_T4_REBALANCE';

const nextProfile=Object.freeze({
  INSTINTIVO:'REACTIVO_1',
  REACTIVO_1:'CAZADOR_2',
  CAZADOR_2:'TACTICO_3',
  TACTICO_3:'MASTER_4',
  MASTER_4:'MASTER_4'
});

const p=(name,kind)=>Object.freeze({
  name,
  effect:Object.freeze({
    kind,
    paramsStatus:ADAPTIVE_PARAMS_STATUS
  })
});

// Sólo conserva identidad mecánica. Ninguna magnitud de combate adaptativa
// queda autorizada hasta que el T0 de la especie sea READY en el motor nuevo.
export const SURVIVAL_POLICIES=Object.freeze({
  rata_qi:p('Reflejo de Madriguera','EVADE_NEXT'),
  serpiente_qi:p('Muda del Cauce','EVADE_NEXT'),
  pez_lunar:p('Giro de Corriente Ciega','EVADE_NEXT'),
  avispa_jade:p('Quiebro de Jade','EVADE_NEXT'),
  mono_pildoras:p('Salto del Ladrón','EVADE_NEXT'),
  anguila_estelar:p('Desliz de Meridiano','EVADE_NEXT'),
  halcon_tormenta:p('Ascenso Contraviento','EVADE_NEXT'),

  lobo_espiritual:p('Paso de la Cola Vigilante','DEFENSE_UP'),
  centinela_pluma:p('Cierre de Plumas Pétreas','DEFENSE_UP'),
  mantis_nube:p('Guardia de las Dos Hojas','DEFENSE_UP'),

  eco_caido:p('Guardia del Último Ensayo','MITIGATE_NEXT'),
  sombra_ahogada:p('Disolverse en Marea','MITIGATE_NEXT'),
  sapo_ceniza:p('Piel de Brasa Muerta','MITIGATE_NEXT'),

  devorador_niebla:p('Cuerpo de Bruma Replegada','ABSORB_RESERVE'),
  sapo_caldera:p('Cierre de las Tres Gargantas','ABSORB_RESERVE'),
  escarabajo_hierro:p('Cierre de Caparazón','ABSORB_RESERVE'),
  rey_escarabajo:p('Diagrama de Placas','ABSORB_RESERVE'),
  guardian_coral:p('Arrecife Replegado','ABSORB_RESERVE')
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
  return def.unique?4:6;
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
  if(policy.effect.paramsStatus!==ADAPTIVE_PARAMS_STATUS){
    throw new Error(`${mobId}: adaptive survival params must remain pending until T0-T4 rebalance`);
  }

  const id=survivalAbilityId(mobId);
  const probe=buildCandidateMonsterInput({mobId,def,round:1,mode:'DECISION_EXPERIMENTAL'});
  const offensivePreference=Number.isFinite(probe.preferences?.OFENSIVA)?probe.preferences.OFENSIVA:1;
  const survivalBase=18 + (offensivePreference-1)*20;

  out[id]={
    id,
    intentCategory:'DEFENSA',
    tags:['EXPERIMENTAL_NEW_ENGINE','SURVIVAL_EVOLUTION_1',policy.effect.kind],
    telegraph:`${policy.name}.`,
    cooldownKey:`${id}__cooldown`,
    requirements:{signalsAll:[]},
    execution:{
      kind:policy.effect.kind,
      paramsStatus:ADAPTIVE_PARAMS_STATUS
    },
    utility:{
      base:survivalBase,
      signalWeights:{
        SELF_LOW_HP:22,
        TOOK_HEAVY_HIT:10,
        PLAYER_LOW_HP:3
      },
      memoryWeights:{},
      socialWeights:{}
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

  if(mode==='CADENCE_COMPAT'&&def.technique&&due){
    effectiveKit=[canonicalAbilityIds(mobId).technique];
  }else{
    effectiveKit=[canonicalAbilityIds(mobId).basic,survivalId];
    if(mode==='DECISION_EXPERIMENTAL'&&def.technique&&due){
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
