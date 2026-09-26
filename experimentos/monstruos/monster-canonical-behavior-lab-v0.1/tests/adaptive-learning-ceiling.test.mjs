import assert from 'node:assert/strict';
import {
  pressureTierFromPressure,
  pressureCapForAdaptiveCeiling,
  clampPressureToAdaptiveCeiling,
  reconcileLearningWithCeiling
} from '../adaptive/adaptive-learning-ceiling-v0.2.mjs';
import {adaptiveCapabilityCeiling} from '../adaptive/stage-progression-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

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

T('pressure caps match the upper edge of each learnable tier',()=>{
  assert.deepEqual(
    [0,1,2,3,4].map(pressureCapForAdaptiveCeiling),
    [19,44,69,89,100]
  );
});

T('T1 ceiling cannot preload T2-T4 pressure',()=>{
  assert.equal(
    clampPressureToAdaptiveCeiling({pressure:100,ceilingTier:1}),
    44
  );
  const r=reconcileLearningWithCeiling({
    pressure:100,
    maxTierReached:0,
    ceilingTier:1
  });
  assert.equal(r.pressure,44);
  assert.equal(r.pressureTier,1);
  assert.equal(r.maxTierReached,1);
  assert.equal(r.effectiveAdaptiveTier,1);
});

T('raising the ceiling does not reveal a tier without new pressure',()=>{
  const atT1=reconcileLearningWithCeiling({
    pressure:100,
    maxTierReached:0,
    ceilingTier:1
  });
  const afterAdvance=reconcileLearningWithCeiling({
    pressure:atT1.pressure,
    maxTierReached:atT1.maxTierReached,
    ceilingTier:2
  });
  assert.equal(afterAdvance.pressure,44);
  assert.equal(afterAdvance.pressureTier,1);
  assert.equal(afterAdvance.maxTierReached,1);
  assert.equal(afterAdvance.effectiveAdaptiveTier,1);
});

T('new pressure after advancement can earn the newly available tier',()=>{
  const r=reconcileLearningWithCeiling({
    pressure:69,
    maxTierReached:1,
    ceilingTier:2
  });
  assert.equal(r.pressureTier,2);
  assert.equal(r.maxTierReached,2);
  assert.equal(r.effectiveAdaptiveTier,2);
});

T('historical floor remains irreversible after decay',()=>{
  const peak=reconcileLearningWithCeiling({
    pressure:89,
    maxTierReached:2,
    ceilingTier:3
  });
  assert.equal(peak.maxTierReached,3);

  const decayed=reconcileLearningWithCeiling({
    pressure:0,
    maxTierReached:peak.maxTierReached,
    ceilingTier:3
  });
  assert.equal(decayed.floorTier,2);
  assert.equal(decayed.earnedTier,2);
  assert.equal(decayed.effectiveAdaptiveTier,2);
});

T('T4 learning still decays only to consolidated T3',()=>{
  const peak=reconcileLearningWithCeiling({
    pressure:100,
    maxTierReached:3,
    ceilingTier:4
  });
  assert.equal(peak.maxTierReached,4);

  const decayed=reconcileLearningWithCeiling({
    pressure:0,
    maxTierReached:peak.maxTierReached,
    ceilingTier:4
  });
  assert.equal(decayed.floorTier,3);
  assert.equal(decayed.effectiveAdaptiveTier,3);
});


T('real stage capability ceiling and population ratchet work together',()=>{
  const c1=adaptiveCapabilityCeiling('rata_qi',1);
  assert.equal(c1.tier,1);

  const farmedAtStage1=reconcileLearningWithCeiling({
    pressure:100,
    maxTierReached:0,
    ceilingTier:c1.tier
  });
  assert.equal(farmedAtStage1.pressure,44);
  assert.equal(farmedAtStage1.maxTierReached,1);

  const c2=adaptiveCapabilityCeiling('rata_qi',2);
  assert.equal(c2.tier,2);

  const immediatelyAfterAdvance=reconcileLearningWithCeiling({
    pressure:farmedAtStage1.pressure,
    maxTierReached:farmedAtStage1.maxTierReached,
    ceilingTier:c2.tier
  });
  assert.equal(immediatelyAfterAdvance.effectiveAdaptiveTier,1);

  const afterNewHunting=reconcileLearningWithCeiling({
    pressure:69,
    maxTierReached:immediatelyAfterAdvance.maxTierReached,
    ceilingTier:c2.tier
  });
  assert.equal(afterNewHunting.effectiveAdaptiveTier,2);
  assert.equal(afterNewHunting.maxTierReached,2);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
