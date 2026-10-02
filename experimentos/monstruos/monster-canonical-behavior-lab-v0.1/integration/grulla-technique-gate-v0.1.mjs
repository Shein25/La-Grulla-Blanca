import {grullaTechniqueEffectiveness} from '../adaptive/grulla-boss-brain-v0.1.mjs';
import {techniqueActionFromResolved} from './grulla-player-action-adapter-v0.1.mjs';

export const GRULLA_TECHNIQUE_GATE_STATUS='EXPERIMENTAL_INTEGRATION_READY_TECHNIQUE_GATE_V01';

function freezeDeep(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const v of Object.values(value))freezeDeep(v);
  return Object.freeze(value);
}

export function grullaTechniquePreResolutionGate({
  brainState,
  techniqueId,
  techniqueType,
  element=null,
  elements=null,
  resolvedElement=null,
  qiSpent
}){
  const action=techniqueActionFromResolved({
    techniqueId,
    techniqueType,
    element,
    elements,
    resolvedElement,
    qiSpent,
    damage:0
  });

  const eff=grullaTechniqueEffectiveness(brainState,action);

  return freezeDeep({
    techniqueId:action.techniqueId,
    techniqueRole:action.techniqueRole,
    blocked:eff.blocked,
    consumeQi:eff.consumeQi,
    refundQi:eff.refundQi,
    suppressEffects:eff.suppressEffects,
    suppressDamage:eff.suppressDamage,
    suppressControl:eff.suppressControl,
    suppressAfflictions:eff.suppressAfflictions,
    suppressResourceEffects:eff.suppressResourceEffects,
    suppressGuard:eff.suppressGuard,
    suppressDefenseBuff:eff.suppressDefenseBuff,
    suppressEvasion:eff.suppressEvasion,
    counterMode:eff.counterMode,
    counterLabel:eff.counterLabel,
    telegraph:eff.telegraph,
    reason:eff.reason
  });
}
