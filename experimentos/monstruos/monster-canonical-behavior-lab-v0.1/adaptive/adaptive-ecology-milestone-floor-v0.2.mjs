export const ADAPTIVE_ECOLOGY_MILESTONE_STATUS='EXPERIMENTAL_V02_MILESTONE_FLOOR';

function tier(v,label){
  if(!Number.isInteger(v)||v<0||v>4)throw new RangeError(label+' debe ser entero 0..4');
  return v;
}

/**
 * Trinquete evolutivo:
 * maxReached 0 -> floor 0
 * maxReached 1 -> floor 1
 * maxReached 2 -> floor 1
 * maxReached 3 -> floor 2
 * maxReached 4 -> floor 3
 */
export function consolidatedFloorFromMaxReached(maxTierReached){
  const max=tier(maxTierReached,'maxTierReached');
  if(max===0)return 0;
  if(max===1)return 1;
  return max-1;
}

export function registerReachedTier({maxTierReached,reachedTier}){
  const max=tier(maxTierReached,'maxTierReached');
  const reached=tier(reachedTier,'reachedTier');
  return Math.max(max,reached);
}

export function effectiveTierAfterDecay({pressureTier,maxTierReached}){
  const pressure=tier(pressureTier,'pressureTier');
  const max=tier(maxTierReached,'maxTierReached');
  const floor=consolidatedFloorFromMaxReached(max);
  return Math.max(pressure,floor);
}

export function reconcilePopulationAdaptation({pressureTier,maxTierReached,reachedTier=pressureTier}){
  const nextMax=registerReachedTier({maxTierReached,reachedTier});
  const floorTier=consolidatedFloorFromMaxReached(nextMax);
  const effectiveTier=effectiveTierAfterDecay({pressureTier,maxTierReached:nextMax});
  return Object.freeze({
    pressureTier:tier(pressureTier,'pressureTier'),
    maxTierReached:nextMax,
    floorTier,
    effectiveTier
  });
}
