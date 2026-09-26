import assert from 'node:assert/strict';
import {
  consolidatedFloorFromMaxReached,
  registerReachedTier,
  effectiveTierAfterDecay,
  reconcilePopulationAdaptation
} from '../adaptive/adaptive-ecology-milestone-floor-v0.2.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('milestone floor mapping is 0,1,1,2,3',()=>{
  assert.deepEqual(
    [0,1,2,3,4].map(consolidatedFloorFromMaxReached),
    [0,1,1,2,3]
  );
});

T('reaching T1 permanently prevents decay to T0',()=>{
  const r=reconcilePopulationAdaptation({pressureTier:0,maxTierReached:0,reachedTier:1});
  assert.equal(r.maxTierReached,1);
  assert.equal(r.floorTier,1);
  assert.equal(r.effectiveTier,1);
});

T('reaching T2 can still decay to consolidated T1',()=>{
  const r=reconcilePopulationAdaptation({pressureTier:0,maxTierReached:2,reachedTier:2});
  assert.equal(r.floorTier,1);
  assert.equal(r.effectiveTier,1);
});

T('reaching T3 permanently consolidates T2',()=>{
  const r=reconcilePopulationAdaptation({pressureTier:0,maxTierReached:3,reachedTier:3});
  assert.equal(r.floorTier,2);
  assert.equal(r.effectiveTier,2);
});

T('reaching T4 can decay one tier but never below T3',()=>{
  for(const pressureTier of [0,1,2,3]){
    const r=reconcilePopulationAdaptation({pressureTier,maxTierReached:4,reachedTier:4});
    assert.equal(r.floorTier,3);
    assert.equal(r.effectiveTier,3);
  }
});

T('pressure can raise effective tier above floor again',()=>{
  assert.equal(effectiveTierAfterDecay({pressureTier:4,maxTierReached:4}),4);
  assert.equal(effectiveTierAfterDecay({pressureTier:3,maxTierReached:4}),3);
  assert.equal(effectiveTierAfterDecay({pressureTier:2,maxTierReached:4}),3);
});

T('max historical tier never decreases',()=>{
  assert.equal(registerReachedTier({maxTierReached:3,reachedTier:1}),3);
  assert.equal(registerReachedTier({maxTierReached:3,reachedTier:4}),4);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
