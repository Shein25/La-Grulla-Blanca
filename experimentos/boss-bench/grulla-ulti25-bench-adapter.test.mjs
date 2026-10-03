import assert from 'node:assert/strict';
import {
  createGrullaUlti25BenchState,
  chooseGrullaUlti25BenchEnemyAction,
  markGrullaUlti25BenchEnemyActionResolved,
  applyGrullaUlti25BenchBossLifeDamage,
  grullaUlti25BenchPublicSnapshot,
  validateGrullaUlti25BenchAdapterContract
} from './grulla-ulti25-bench-adapter-v0.1.mjs';

assert.equal(validateGrullaUlti25BenchAdapterContract().ok,true);

let s=createGrullaUlti25BenchState();
let r=applyGrullaUlti25BenchBossLifeDamage(s,999,{source:'SELFTEST_F1'});
assert.equal(r.phaseTransition.to,2); s=r.state;
r=applyGrullaUlti25BenchBossLifeDamage(s,999,{source:'SELFTEST_F2'});
assert.equal(r.phaseTransition.to,3); s=r.state;
let snap=grullaUlti25BenchPublicSnapshot(s);
assert.equal(snap.phase,3); assert.equal(snap.phaseHp,50); assert.equal(snap.f3_gate_active,true);

r=applyGrullaUlti25BenchBossLifeDamage(s,999,{source:'ULTI_PACKET_1'}); s=r.state;
snap=grullaUlti25BenchPublicSnapshot(s);
assert.equal(r.lethalPrevented,true); assert.equal(r.encounterDefeated,false); assert.equal(snap.phaseHp,1);
r=applyGrullaUlti25BenchBossLifeDamage(s,999,{source:'ULTI_PACKET_2'}); s=r.state;
snap=grullaUlti25BenchPublicSnapshot(s);
assert.equal(r.lethalPrevented,true); assert.equal(snap.phaseHp,1); assert.equal(snap.f3_lethal_preventions,2);

let chosen=chooseGrullaUlti25BenchEnemyAction(s,{context:{playerHpRatio:.7,playerQiRatio:.5,selfHpRatio:.02},rng:()=>.5});
s=chosen.state;
let marked=markGrullaUlti25BenchEnemyActionResolved(s,chosen.runtime,{resolved:false,prevented:true});
s=marked.state;
snap=grullaUlti25BenchPublicSnapshot(s);
assert.equal(marked.pactReleased,false); assert.equal(snap.f3_gate_active,true);

chosen=chooseGrullaUlti25BenchEnemyAction(s,{context:{playerHpRatio:.7,playerQiRatio:.5,selfHpRatio:.02},rng:()=>.5});
s=chosen.state;
marked=markGrullaUlti25BenchEnemyActionResolved(s,chosen.runtime,{resolved:true,prevented:false});
s=marked.state;
snap=grullaUlti25BenchPublicSnapshot(s);
assert.equal(marked.pactReleased,true); assert.equal(snap.f3_gate_active,false); assert.equal(snap.f3_first_real_action_resolved,true);
r=applyGrullaUlti25BenchBossLifeDamage(s,1,{source:'POST_RELEASE'});
assert.equal(r.encounterDefeated,true);

console.log(JSON.stringify({pass:true,tests:5,snapshot:grullaUlti25BenchPublicSnapshot(r.state)},null,2));
