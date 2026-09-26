import {
  initialGrullaEncounterSession,
  grullaSessionProfile,
  gateGrullaSessionPlayerTechnique,
  observeGrullaSessionPlayerResolved,
  chooseGrullaSessionIntent,
  markGrullaSessionIntentResolved,
  resolveGrullaSessionPhase1Wing,
  applyGrullaSessionBossDamage,
  enterNextGrullaSessionPhase
} from './grulla-encounter-session-v0.1.mjs';

export const GRULLA_SPECIAL_COMBAT_ADAPTER_STATUS='EXPERIMENTAL_INTEGRATION_READY_SPECIAL_COMBAT_ADAPTER_V01';

// Discriminador interno de integración. NO es mob_id canónico ni añade criatura a MOBS.
export const GRULLA_SPECIAL_COMBAT_TAG='grulla_boss_v01';

function freezeDeep(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const v of Object.values(value))freezeDeep(v);
  return Object.freeze(value);
}

function assertSpecialTag(tag){
  if(typeof tag!=='string'||!tag)throw new TypeError('specialTag debe ser string no vacío');
  return tag;
}

export function isGrullaSpecialCombat(especial,{specialTag=GRULLA_SPECIAL_COMBAT_TAG}={}){
  assertSpecialTag(specialTag);
  return especial===specialTag;
}

export function createGrullaSpecialCombatState({
  especial=GRULLA_SPECIAL_COMBAT_TAG,
  specialTag=GRULLA_SPECIAL_COMBAT_TAG,
  phase=1
}={}){
  if(!isGrullaSpecialCombat(especial,{specialTag})){
    throw new RangeError('NOT_GRULLA_SPECIAL_COMBAT');
  }
  return freezeDeep({
    especial,
    session:initialGrullaEncounterSession({phase})
  });
}

export function grullaSpecialProfile(state){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  return grullaSessionProfile(state.session);
}

/**
 * Se llama DESPUÉS de resolver tid/conf/tipo/coste y ANTES de ejecutar
 * daño/control/guardia/esquiva/fortificación.
 *
 * El qi debe consumirse según ver74 aunque la técnica esté bloqueada.
 */
export function gateGrullaSpecialTechnique(state,techniqueSignal){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  return gateGrullaSessionPlayerTechnique(state.session,techniqueSignal);
}

/**
 * Se llama sólo después de que la acción del jugador ya quedó resuelta.
 * Debe ejecutarse antes de elegir/resolver la respuesta de la Grulla.
 */
export function observeGrullaSpecialPlayerResolved(state,resolvedSignal){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  const observed=observeGrullaSessionPlayerResolved(state.session,resolvedSignal);
  return freezeDeep({
    state:freezeDeep({...state,session:observed.session}),
    action:observed.action,
    event:observed.event,
    counterAnnouncement:observed.counterAnnouncement
  });
}

/**
 * Selección del turno enemigo. Sólo recibe contexto visible/resuelto:
 * ratios actuales de HP/Qi y RNG.
 */
export function chooseGrullaSpecialEnemyAction(state,{context={},rng=()=>.5}={}){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  const chosen=chooseGrullaSessionIntent(state.session,{context,rng});
  return freezeDeep({
    state:freezeDeep({...state,session:chosen.session}),
    intent:chosen.intent,
    runtime:chosen.runtime
  });
}

/**
 * Se llama después de resolver la intención enemiga. Pata Fase I arma Resonancia.
 */
export function markGrullaSpecialEnemyActionResolved(state,runtimeIntent){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  return freezeDeep({
    ...state,
    session:markGrullaSessionIntentResolved(state.session,runtimeIntent)
  });
}

/**
 * Resolver exclusivamente el Golpe de Ala de Fase I cuando puede existir
 * Resonancia. El motor productivo sigue siendo dueño del roll de impacto y del
 * daño base: este helper sólo aplica el orden cerrado Resonancia -> absorción.
 */
export function resolveGrullaSpecialPhase1Wing(state,resolutionInput){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  const r=resolveGrullaSessionPhase1Wing(state.session,resolutionInput);
  return freezeDeep({
    state:freezeDeep({...state,session:r.session}),
    resolution:r.resolution
  });
}

/**
 * Intercepta el daño al pool de fase ANTES del cleanup genérico de mob muerto.
 *
 * - Fase I/II derrotadas: crea la fase siguiente a HP completo.
 * - Fase III derrotada: encounterDefeated=true.
 * - Nunca transfiere overkill al pool siguiente.
 */
export function applyGrullaSpecialBossDamage(state,damage){
  if(!state?.session)throw new TypeError('state de Grulla requerido');

  const fromPhase=state.session.phase;
  const hit=applyGrullaSessionBossDamage(state.session,damage);
  let session=hit.session;

  if(!hit.phaseDefeated){
    return freezeDeep({
      state:freezeDeep({...state,session}),
      appliedDamage:hit.appliedDamage,
      phaseDefeated:false,
      encounterDefeated:false,
      phaseTransition:null
    });
  }

  if(fromPhase===3){
    return freezeDeep({
      state:freezeDeep({...state,session}),
      appliedDamage:hit.appliedDamage,
      phaseDefeated:true,
      encounterDefeated:true,
      phaseTransition:null
    });
  }

  session=enterNextGrullaSessionPhase(session);
  return freezeDeep({
    state:freezeDeep({...state,session}),
    appliedDamage:hit.appliedDamage,
    phaseDefeated:true,
    encounterDefeated:false,
    phaseTransition:freezeDeep({
      from:fromPhase,
      to:session.phase,
      nextHp:session.phaseHp
    })
  });
}

/**
 * Snapshot mínimo para sincronizar la representación visual/productiva del boss.
 * No expone historia interna, planes ocultos ni RNG futuro.
 */
export function grullaSpecialPublicSnapshot(state){
  if(!state?.session)throw new TypeError('state de Grulla requerido');
  const profile=grullaSessionProfile(state.session);
  return freezeDeep({
    phase:state.session.phase,
    phaseHp:state.session.phaseHp,
    phaseMaxHp:profile.hpPool,
    attack:profile.attack,
    defense:profile.defense,
    phaseId:profile.id,
    resonancePrepared:state.session.phase===1&&state.session.phase1ResonancePrepared===true
  });
}
