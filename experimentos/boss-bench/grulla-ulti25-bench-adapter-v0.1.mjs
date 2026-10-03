import {
  GRULLA_SPECIAL_COMBAT_ADAPTER_STATUS,
  GRULLA_SPECIAL_COMBAT_TAG,
  createGrullaSpecialCombatState,
  grullaSpecialProfile,
  gateGrullaSpecialTechnique,
  observeGrullaSpecialPlayerResolved,
  chooseGrullaSpecialEnemyAction,
  markGrullaSpecialEnemyActionResolved,
  resolveGrullaSpecialPhase1Wing,
  applyGrullaSpecialBossDamage,
  grullaSpecialPublicSnapshot
} from '../monstruos/monster-canonical-behavior-lab-v0.1/integration/grulla-ver74-special-combat-adapter-v0.1.mjs';

import {
  GRULLA_F3_PACT_STATUS,
  GRULLA_F3_PACT_STATE,
  initialGrullaF3Pact,
  activateGrullaF3Pact,
  applyGrullaF3PactToLifeDamage,
  releaseGrullaF3PactAfterRealAction,
  grullaF3PactTelemetry
} from './grulla-f3-pacto-ultimo-vuelo-v0.1.mjs';

export const GRULLA_ULTI25_BENCH_ADAPTER_STATUS='LAB_GRULLA_ULTI25_BENCH_ADAPTER_V01';
export const GRULLA_ULTI25_SOURCE_COMMIT='4237f126a66193607f7857e5a9883b3070cc7c78';
export const GRULLA_ULTI25_PACT_CONTRACT='GRULLA_F3_PACTO_ULTIMO_VUELO_2026-10-02';
export const GRULLA_ULTI25_NUMERIC_AUTHORITY_STATUS='AUTHORITY_SYNC_REQUIRED_BEFORE_MASS_BENCH';

function freezeDeep(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const v of Object.values(value))freezeDeep(v);
  return Object.freeze(value);
}
function requireState(state){
  if(!state||typeof state!=='object'||!state.special||!state.pact)throw new TypeError('Grulla bench state requerido');
}
function safeDamage(v){
  if(typeof v!=='number'||!Number.isFinite(v)||v<0)throw new TypeError('damage debe ser número finito >= 0');
  return v;
}
function safeSource(v){
  if(typeof v!=='string'||!v.trim())throw new TypeError('source debe ser string no vacío');
  return v;
}
function maybeActivateF3Pact(pact,phase){
  return phase===3?activateGrullaF3Pact(pact):pact;
}
function wrapSpecial(state,special,{pact=state.pact,enemyActionsResolved=state.enemyActionsResolved}={}){
  const phase=grullaSpecialPublicSnapshot(special).phase;
  return freezeDeep({
    ...state,
    special,
    pact:maybeActivateF3Pact(pact,phase),
    enemyActionsResolved
  });
}

export function createGrullaUlti25BenchState({phase=1}={}){
  const special=createGrullaSpecialCombatState({especial:GRULLA_SPECIAL_COMBAT_TAG,phase});
  const pact=initialGrullaF3Pact({active:phase===3});
  return freezeDeep({
    special,
    pact,
    enemyActionsResolved:0,
    sourceCommit:GRULLA_ULTI25_SOURCE_COMMIT,
    underlyingAdapterStatus:GRULLA_SPECIAL_COMBAT_ADAPTER_STATUS,
    pactStatus:GRULLA_F3_PACT_STATUS
  });
}

export function grullaUlti25BenchProfile(state){
  requireState(state);
  return grullaSpecialProfile(state.special);
}

export function gateGrullaUlti25BenchTechnique(state,techniqueSignal){
  requireState(state);
  return gateGrullaSpecialTechnique(state.special,techniqueSignal);
}

export function observeGrullaUlti25BenchPlayerResolved(state,resolvedSignal){
  requireState(state);
  const observed=observeGrullaSpecialPlayerResolved(state.special,resolvedSignal);
  return freezeDeep({
    state:wrapSpecial(state,observed.state),
    action:observed.action,
    event:observed.event,
    counterAnnouncement:observed.counterAnnouncement
  });
}

export function chooseGrullaUlti25BenchEnemyAction(state,{context={},rng=()=>.5}={}){
  requireState(state);
  const chosen=chooseGrullaSpecialEnemyAction(state.special,{context,rng});
  return freezeDeep({
    state:wrapSpecial(state,chosen.state),
    intent:chosen.intent,
    runtime:chosen.runtime
  });
}

export function markGrullaUlti25BenchEnemyActionResolved(state,runtimeIntent,{
  resolved=true,
  prevented=false
}={}){
  requireState(state);
  if(!runtimeIntent||typeof runtimeIntent!=='object')throw new TypeError('runtimeIntent requerido');

  if(resolved!==true||prevented===true){
    return freezeDeep({
      state,
      pactReleased:false,
      countedRealAction:false
    });
  }

  const special=markGrullaSpecialEnemyActionResolved(state.special,runtimeIntent);
  const nextOrdinal=state.enemyActionsResolved+1;
  const pact=releaseGrullaF3PactAfterRealAction(state.pact,{
    phase:runtimeIntent.phase,
    consumesAction:runtimeIntent.consumesAction,
    resolved:true,
    prevented:false,
    actionOrdinal:nextOrdinal
  });
  const pactReleased=state.pact.state!==GRULLA_F3_PACT_STATE.RELEASED&&pact.state===GRULLA_F3_PACT_STATE.RELEASED;

  return freezeDeep({
    state:wrapSpecial(state,special,{pact,enemyActionsResolved:nextOrdinal}),
    pactReleased,
    countedRealAction:true
  });
}

export function resolveGrullaUlti25BenchPhase1Wing(state,resolutionInput){
  requireState(state);
  const r=resolveGrullaSpecialPhase1Wing(state.special,resolutionInput);
  return freezeDeep({
    state:wrapSpecial(state,r.state),
    resolution:r.resolution
  });
}

export function applyGrullaUlti25BenchBossLifeDamage(state,damage,{
  source='UNKNOWN'
}={}){
  requireState(state);
  damage=safeDamage(damage);
  source=safeSource(source);

  const before=grullaSpecialPublicSnapshot(state.special);
  const gate=applyGrullaF3PactToLifeDamage({
    pact:state.pact,
    phase:before.phase,
    currentHp:before.phaseHp,
    requestedLifeDamage:damage,
    source
  });

  const hit=applyGrullaSpecialBossDamage(state.special,gate.appliedLifeDamage);
  let pact=gate.pact;
  if(hit.phaseTransition?.to===3)pact=activateGrullaF3Pact(pact);
  const wrapped=wrapSpecial(state,hit.state,{pact});

  return freezeDeep({
    state:wrapped,
    requestedLifeDamage:damage,
    appliedLifeDamage:hit.appliedDamage,
    lethalPrevented:gate.lethalPrevented,
    preventedLethalDamage:gate.preventedLethalDamage,
    source,
    phaseDefeated:hit.phaseDefeated,
    encounterDefeated:hit.encounterDefeated,
    phaseTransition:hit.phaseTransition
  });
}

export function grullaUlti25BenchPublicSnapshot(state){
  requireState(state);
  const base=grullaSpecialPublicSnapshot(state.special);
  return freezeDeep({
    ...base,
    ...grullaF3PactTelemetry(state.pact),
    enemy_actions_resolved:state.enemyActionsResolved,
    source_commit:state.sourceCommit,
    adapter_status:GRULLA_ULTI25_BENCH_ADAPTER_STATUS,
    numeric_authority_status:GRULLA_ULTI25_NUMERIC_AUTHORITY_STATUS
  });
}

export function validateGrullaUlti25BenchAdapterContract(){
  const errors=[];
  if(GRULLA_ULTI25_SOURCE_COMMIT!=='4237f126a66193607f7857e5a9883b3070cc7c78')errors.push('SOURCE_COMMIT');
  if(GRULLA_SPECIAL_COMBAT_ADAPTER_STATUS!=='EXPERIMENTAL_INTEGRATION_READY_SPECIAL_COMBAT_ADAPTER_V01')errors.push('UNDERLYING_ADAPTER_STATUS');
  if(GRULLA_F3_PACT_STATUS!=='LAB_CONTRACT_GRULLA_F3_PACT_V01')errors.push('PACT_STATUS');
  return freezeDeep({ok:errors.length===0,errors,numericAuthorityStatus:GRULLA_ULTI25_NUMERIC_AUTHORITY_STATUS});
}
