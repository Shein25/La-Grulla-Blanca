import {
  initialGrullaBrainState,
  enterGrullaPhase,
  chooseGrullaIntent,
  observeResolvedPlayerAction,
  grullaCounterAnnouncement
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

import {
  grullaPhaseProfile,
  bindGrullaRuntimeIntent,
  resolvePhase1ResonantHit
} from './grulla-encounter-runtime-contract-v0.1.mjs';

import {
  playerActionFromResolvedCombat
} from './grulla-player-action-adapter-v0.1.mjs';

import {
  grullaTechniquePreResolutionGate
} from './grulla-technique-gate-v0.1.mjs';

export const GRULLA_SESSION_STATUS='EXPERIMENTAL_INTEGRATION_READY_GRULLA_SESSION_V01';

function freezeSession(s){
  return Object.freeze({
    phase:s.phase,
    phaseHp:s.phaseHp,
    brainState:s.brainState,
    phase1ResonancePrepared:!!s.phase1ResonancePrepared
  });
}
function sessionOk(session){
  if(!session||typeof session!=='object')throw new TypeError('session inválida');
  if(![1,2,3].includes(session.phase))throw new RangeError('session.phase inválida');
  if(!session.brainState||session.brainState.phase!==session.phase)throw new TypeError('brainState fuera de fase');
}
function damageOf(v){
  if(typeof v!=='number'||!Number.isFinite(v)||v<0)throw new TypeError('damage debe ser número finito >= 0');
  return v;
}

export function initialGrullaEncounterSession({phase=1}={}){
  const p=grullaPhaseProfile(phase);
  return freezeSession({
    phase,
    phaseHp:p.hpPool,
    brainState:initialGrullaBrainState({phase}),
    phase1ResonancePrepared:false
  });
}

export function grullaSessionProfile(session){
  sessionOk(session);
  return grullaPhaseProfile(session.phase);
}

export function gateGrullaSessionPlayerTechnique(session,signal){
  sessionOk(session);
  if(!signal||signal.kind!=='TECHNIQUE')throw new TypeError('signal TECHNIQUE requerido');
  return grullaTechniquePreResolutionGate({
    brainState:session.brainState,
    techniqueId:signal.techniqueId,
    techniqueType:signal.techniqueType,
    element:signal.element??null,
    elements:signal.elements??null,
    resolvedElement:signal.resolvedElement??null,
    qiSpent:signal.qiSpent
  });
}

export function observeGrullaSessionPlayerResolved(session,signal){
  sessionOk(session);
  const action=playerActionFromResolvedCombat(signal);
  const observed=observeResolvedPlayerAction(session.brainState,action);
  const next=freezeSession({
    ...session,
    brainState:observed.state
  });
  return Object.freeze({
    session:next,
    action,
    event:observed.event,
    counterAnnouncement:grullaCounterAnnouncement(observed.state)
  });
}

export function chooseGrullaSessionIntent(session,{context={},rng=()=>.5}={}){
  sessionOk(session);
  const chosen=chooseGrullaIntent({
    state:session.brainState,
    context,
    rng
  });
  const runtime=bindGrullaRuntimeIntent({
    phase:session.phase,
    intent:chosen.intent
  });
  const next=freezeSession({
    ...session,
    brainState:chosen.state
  });
  return Object.freeze({
    session:next,
    intent:chosen.intent,
    runtime
  });
}

export function markGrullaSessionIntentResolved(session,runtimeIntent){
  sessionOk(session);
  if(!runtimeIntent||runtimeIntent.kind!=='GRULLA_RUNTIME_INTENT')throw new TypeError('runtimeIntent inválido');
  if(runtimeIntent.phase!==session.phase)throw new RangeError('runtimeIntent fuera de fase');

  let prepared=session.phase1ResonancePrepared;
  if(session.phase===1&&runtimeIntent.execution.preparesPhase1Resonance===true){
    prepared=true;
  }

  return freezeSession({
    ...session,
    phase1ResonancePrepared:prepared
  });
}

export function resolveGrullaSessionPhase1Wing(session,{
  hit,
  rawDamage,
  guardActive,
  guardPerHit=0,
  guardCapacity=0
}){
  sessionOk(session);
  if(session.phase!==1)throw new RangeError('Resonancia de Pata sólo existe en Fase I');

  const resolution=resolvePhase1ResonantHit({
    prepared:session.phase1ResonancePrepared,
    hit,
    rawDamage,
    guardActive,
    guardPerHit,
    guardCapacity
  });

  const next=freezeSession({
    ...session,
    phase1ResonancePrepared:false
  });

  return Object.freeze({session:next,resolution});
}

export function applyGrullaSessionBossDamage(session,damage){
  sessionOk(session);
  damage=damageOf(damage);
  const phaseHp=Math.max(0,session.phaseHp-damage);
  return Object.freeze({
    session:freezeSession({...session,phaseHp}),
    phaseDefeated:phaseHp<=0,
    appliedDamage:Math.min(session.phaseHp,damage)
  });
}

export function enterNextGrullaSessionPhase(session){
  sessionOk(session);
  if(session.phase>=3)throw new RangeError('Fase III no tiene transición posterior en este contrato');
  if(session.phaseHp>0)throw new RangeError('PHASE_NOT_DEFEATED');

  const phase=session.phase+1;
  const profile=grullaPhaseProfile(phase);
  return freezeSession({
    phase,
    phaseHp:profile.hpPool,
    brainState:enterGrullaPhase(session.brainState,phase),
    phase1ResonancePrepared:false
  });
}
