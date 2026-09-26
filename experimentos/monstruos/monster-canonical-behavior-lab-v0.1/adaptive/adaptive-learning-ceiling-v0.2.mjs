import {reconcilePopulationAdaptation} from './adaptive-ecology-milestone-floor-v0.2.mjs';

export const ADAPTIVE_LEARNING_CEILING_STATUS='EXPERIMENTAL_V02_LEARNING_CEILING';

export const ADAPTIVE_PRESSURE_THRESHOLDS=Object.freeze({
  T1:20,
  T2:45,
  T3:70,
  T4:90,
  MAX:100
});

const PRESSURE_CAP_BY_CEILING=Object.freeze({
  0:19,
  1:44,
  2:69,
  3:89,
  4:100
});

function tier(v,label){
  if(!Number.isInteger(v)||v<0||v>4)throw new RangeError(label+' debe ser entero 0..4');
  return v;
}

function pressure(v){
  if(!Number.isFinite(v)||v<0||v>100)throw new RangeError('pressure debe estar entre 0 y 100');
  return v;
}

export function pressureTierFromPressure(value){
  const p=pressure(value);
  if(p>=ADAPTIVE_PRESSURE_THRESHOLDS.T4)return 4;
  if(p>=ADAPTIVE_PRESSURE_THRESHOLDS.T3)return 3;
  if(p>=ADAPTIVE_PRESSURE_THRESHOLDS.T2)return 2;
  if(p>=ADAPTIVE_PRESSURE_THRESHOLDS.T1)return 1;
  return 0;
}

export function pressureCapForAdaptiveCeiling(ceilingTier){
  return PRESSURE_CAP_BY_CEILING[tier(ceilingTier,'ceilingTier')];
}

/**
 * El techo limita aprendizaje real, no sólo manifestación.
 *
 * Consecuencia deliberada:
 * - una población con ceiling T1 no puede almacenar presión de T2/T3/T4;
 * - al subir el jugador de etapa no aparecen tiers "precargados";
 * - hacen falta nuevos eventos válidos para seguir aprendiendo.
 */
export function clampPressureToAdaptiveCeiling({pressure:value,ceilingTier}){
  const p=pressure(value);
  const cap=pressureCapForAdaptiveCeiling(ceilingTier);
  return Math.min(p,cap);
}

export function reconcileLearningWithCeiling({
  pressure:value,
  maxTierReached,
  ceilingTier
}){
  const ceiling=tier(ceilingTier,'ceilingTier');
  const cappedPressure=clampPressureToAdaptiveCeiling({pressure:value,ceilingTier:ceiling});
  const pressureTier=pressureTierFromPressure(cappedPressure);
  const reconciled=reconcilePopulationAdaptation({
    pressureTier,
    maxTierReached,
    reachedTier:pressureTier
  });

  return Object.freeze({
    rawPressure:pressure(value),
    pressure:cappedPressure,
    pressureWasCapped:cappedPressure!==value,
    pressureTier,
    maxTierReached:reconciled.maxTierReached,
    floorTier:reconciled.floorTier,
    earnedTier:reconciled.effectiveTier,
    capabilityCeilingTier:ceiling,
    effectiveAdaptiveTier:Math.min(reconciled.effectiveTier,ceiling)
  });
}
