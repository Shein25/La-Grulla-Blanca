import {reconcilePopulationAdaptation} from './adaptive-ecology-milestone-floor-v0.2.mjs';

export const ADAPTIVE_LEARNING_CEILING_STATUS='EXPERIMENTAL_V03_NATURAL_OVERREACH';

export const ADAPTIVE_PRESSURE_THRESHOLDS=Object.freeze({
  T1:20,
  T2:45,
  T3:70,
  T4:90,
  MAX:100
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

/**
 * Compatibilidad de API.
 *
 * Desde la autoridad humana 2026-10-06 la etapa del jugador NO impone un
 * hard cap sobre la presión. El ceiling histórico se conserva únicamente como
 * banda esperada/orientativa. Por eso cualquier ceiling devuelve MAX=100.
 */
export function pressureCapForAdaptiveCeiling(ceilingTier){
  tier(ceilingTier,'ceilingTier');
  return ADAPTIVE_PRESSURE_THRESHOLDS.MAX;
}

/**
 * Compatibilidad de API: ya no recorta pressure.
 *
 * Si el jugador consigue producir presión válida más allá de su banda
 * esperada, la población puede seguir adaptándose. El muro natural es la
 * dificultad del combate + decay, no una prohibición de etapa.
 */
export function clampPressureToAdaptiveCeiling({pressure:value,ceilingTier}){
  tier(ceilingTier,'ceilingTier');
  return pressure(value);
}

export function reconcileLearningWithCeiling({
  pressure:value,
  maxTierReached,
  ceilingTier
}){
  const expectedTier=tier(ceilingTier,'ceilingTier');
  const currentPressure=pressure(value);
  const pressureTier=pressureTierFromPressure(currentPressure);
  const reconciled=reconcilePopulationAdaptation({
    pressureTier,
    maxTierReached,
    reachedTier:pressureTier
  });

  return Object.freeze({
    rawPressure:currentPressure,
    pressure:currentPressure,
    pressureWasCapped:false,
    pressureTier,
    maxTierReached:reconciled.maxTierReached,
    floorTier:reconciled.floorTier,
    earnedTier:reconciled.effectiveTier,
    // Campo histórico conservado por compatibilidad. Es ORIENTATIVO, no gate.
    capabilityCeilingTier:expectedTier,
    expectedCapabilityTier:expectedTier,
    effectiveAdaptiveTier:reconciled.effectiveTier,
    overreachedExpectedBand:reconciled.effectiveTier>expectedTier
  });
}
