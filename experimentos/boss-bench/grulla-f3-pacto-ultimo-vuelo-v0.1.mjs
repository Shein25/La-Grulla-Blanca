export const GRULLA_F3_PACT_STATUS='LAB_CONTRACT_GRULLA_F3_PACT_V01';

export const GRULLA_F3_PACT_STATE=Object.freeze({
  INACTIVE:'INACTIVE',
  ACTIVE:'ACTIVE',
  CRACKED_WAITING_FOR_F3_ACTION:'CRACKED_WAITING_FOR_F3_ACTION',
  RELEASED:'RELEASED'
});

function freezeDeep(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const v of Object.values(value))freezeDeep(v);
  return Object.freeze(value);
}
function finiteNonNegative(v,label){
  if(typeof v!=='number'||!Number.isFinite(v)||v<0)throw new TypeError(label+' debe ser número finito >= 0');
  return v;
}
function safeSource(v){
  if(typeof v!=='string'||!v.trim())throw new TypeError('source debe ser string no vacío');
  return v;
}

export function initialGrullaF3Pact({active=false}={}){
  return freezeDeep({
    state:active?GRULLA_F3_PACT_STATE.ACTIVE:GRULLA_F3_PACT_STATE.INACTIVE,
    lethalPreventions:0,
    preventedLethalDamage:0,
    maxSingleOverkillPrevented:0,
    skipAttempted:false,
    firstRealF3ActionResolved:false,
    gateReleaseOrdinal:null,
    lastSkipSource:null
  });
}

export function activateGrullaF3Pact(pact=initialGrullaF3Pact()){
  if(pact.state===GRULLA_F3_PACT_STATE.RELEASED)return pact;
  if(pact.state===GRULLA_F3_PACT_STATE.ACTIVE||pact.state===GRULLA_F3_PACT_STATE.CRACKED_WAITING_FOR_F3_ACTION)return pact;
  return freezeDeep({...pact,state:GRULLA_F3_PACT_STATE.ACTIVE});
}

export function grullaF3PactProtects(pact){
  return !!pact&&[
    GRULLA_F3_PACT_STATE.ACTIVE,
    GRULLA_F3_PACT_STATE.CRACKED_WAITING_FOR_F3_ACTION
  ].includes(pact.state);
}

export function applyGrullaF3PactToLifeDamage({
  pact,
  phase,
  currentHp,
  requestedLifeDamage,
  source='UNKNOWN'
}){
  if(!pact||typeof pact!=='object')throw new TypeError('pact requerido');
  if(!Number.isInteger(phase)||phase<1||phase>3)throw new RangeError('phase debe ser 1..3');
  currentHp=finiteNonNegative(currentHp,'currentHp');
  requestedLifeDamage=finiteNonNegative(requestedLifeDamage,'requestedLifeDamage');
  source=safeSource(source);

  const ordinaryApplied=Math.min(currentHp,requestedLifeDamage);
  if(phase!==3||!grullaF3PactProtects(pact)||currentHp<=0||requestedLifeDamage<currentHp){
    return freezeDeep({
      pact,
      appliedLifeDamage:ordinaryApplied,
      lethalPrevented:false,
      preventedLethalDamage:0,
      source
    });
  }

  const maxAllowed=Math.max(0,currentHp-1);
  const appliedLifeDamage=Math.min(requestedLifeDamage,maxAllowed);
  const preventedLethalDamage=Math.max(0,requestedLifeDamage-appliedLifeDamage);

  const next=freezeDeep({
    ...pact,
    state:GRULLA_F3_PACT_STATE.CRACKED_WAITING_FOR_F3_ACTION,
    lethalPreventions:pact.lethalPreventions+1,
    preventedLethalDamage:pact.preventedLethalDamage+preventedLethalDamage,
    maxSingleOverkillPrevented:Math.max(pact.maxSingleOverkillPrevented,preventedLethalDamage),
    skipAttempted:true,
    lastSkipSource:source
  });

  return freezeDeep({
    pact:next,
    appliedLifeDamage,
    lethalPrevented:true,
    preventedLethalDamage,
    source
  });
}

export function releaseGrullaF3PactAfterRealAction(pact,{
  phase,
  consumesAction,
  resolved,
  prevented=false,
  actionOrdinal=null
}={}){
  if(!pact||typeof pact!=='object')throw new TypeError('pact requerido');
  if(phase!==3||consumesAction!==true||resolved!==true||prevented===true)return pact;
  if(!grullaF3PactProtects(pact))return pact;

  return freezeDeep({
    ...pact,
    state:GRULLA_F3_PACT_STATE.RELEASED,
    firstRealF3ActionResolved:true,
    gateReleaseOrdinal:actionOrdinal
  });
}

export function grullaF3PactTelemetry(pact){
  if(!pact||typeof pact!=='object')throw new TypeError('pact requerido');
  return freezeDeep({
    f3_gate_active:grullaF3PactProtects(pact),
    f3_gate_state:pact.state,
    f3_lethal_preventions:pact.lethalPreventions,
    f3_skip_attempted:pact.skipAttempted,
    f3_skip_source:pact.lastSkipSource,
    f3_prevented_lethal_damage:pact.preventedLethalDamage,
    f3_max_single_overkill_prevented:pact.maxSingleOverkillPrevented,
    f3_first_real_action_resolved:pact.firstRealF3ActionResolved,
    f3_gate_release_ordinal:pact.gateReleaseOrdinal
  });
}
