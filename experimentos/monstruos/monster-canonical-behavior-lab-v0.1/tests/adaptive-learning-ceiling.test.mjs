import assert from 'node:assert/strict';
import {
  ADAPTIVE_LEARNING_CEILING_STATUS,
  pressureTierFromPressure,
  pressureCapForAdaptiveCeiling,
  clampPressureToAdaptiveCeiling,
  reconcileLearningWithCeiling
} from '../adaptive/adaptive-learning-ceiling-v0.2.mjs';
import {adaptiveCapabilityCeiling} from '../adaptive/stage-progression-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('status declares natural overreach semantics',()=>{
  assert.equal(ADAPTIVE_LEARNING_CEILING_STATUS,'EXPERIMENTAL_V03_NATURAL_OVERREACH');
});

T('pressure thresholds derive T0..T4 exactly',()=>{
  assert.equal(pressureTierFromPressure(0),0);
  assert.equal(pressureTierFromPressure(19),0);
  assert.equal(pressureTierFromPressure(20),1);
  assert.equal(pressureTierFromPressure(44),1);
  assert.equal(pressureTierFromPressure(45),2);
  assert.equal(pressureTierFromPressure(69),2);
  assert.equal(pressureTierFromPressure(70),3);
  assert.equal(pressureTierFromPressure(89),3);
  assert.equal(pressureTierFromPressure(90),4);
  assert.equal(pressureTierFromPressure(100),4);
});

T('historical ceiling API no longer caps pressure',()=>{
  assert.deepEqual(
    [0,1,2,3,4].map(pressureCapForAdaptiveCeiling),
    [100,100,100,100,100]
  );
  assert.equal(clampPressureToAdaptiveCeiling({pressure:100,ceilingTier:1}),100);
});

T('player can legitimately overreach expected T1 band into T4',()=>{
  const r=reconcileLearningWithCeiling({
    pressure:100,
    maxTierReached:0,
    ceilingTier:1
  });
  assert.equal(r.pressure,100);
  assert.equal(r.pressureWasCapped,false);
  assert.equal(r.pressureTier,4);
  assert.equal(r.maxTierReached,4);
  assert.equal(r.effectiveAdaptiveTier,4);
  assert.equal(r.expectedCapabilityTier,1);
  assert.equal(r.overreachedExpectedBand,true);
});

T('historical floor remains irreversible after decay',()=>{
  const peak=reconcileLearningWithCeiling({
    pressure:89,
    maxTierReached:2,
    ceilingTier:2
  });
  assert.equal(peak.maxTierReached,3);

  const decayed=reconcileLearningWithCeiling({
    pressure:0,
    maxTierReached:peak.maxTierReached,
    ceilingTier:2
  });
  assert.equal(decayed.floorTier,2);
  assert.equal(decayed.earnedTier,2);
  assert.equal(decayed.effectiveAdaptiveTier,2);
});

T('T4 still decays only to consolidated T3',()=>{
  const peak=reconcileLearningWithCeiling({
    pressure:100,
    maxTierReached:3,
    ceilingTier:1
  });
  assert.equal(peak.maxTierReached,4);

  const decayed=reconcileLearningWithCeiling({
    pressure:0,
    maxTierReached:peak.maxTierReached,
    ceilingTier:1
  });
  assert.equal(decayed.floorTier,3);
  assert.equal(decayed.effectiveAdaptiveTier,3);
});

T('stage capability remains guidance, not a limiter',()=>{
  const expected=adaptiveCapabilityCeiling('rata_qi',1);
  assert.equal(expected.tier,1);

  const forced=reconcileLearningWithCeiling({
    pressure:70,
    maxTierReached:0,
    ceilingTier:expected.tier
  });
  assert.equal(forced.pressureTier,3);
  assert.equal(forced.effectiveAdaptiveTier,3);
  assert.equal(forced.overreachedExpectedBand,true);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
