import assert from 'node:assert/strict';
import {
  RATA_QI_ADAPTIVE_ARSENAL_STATUS,
  RATA_QI_T4_ABILITY,
  RATA_QI_ADAPTIVE_PROGRESSION,
  rataQiAdaptiveAbilityIds
} from '../adaptive/rata-qi-adaptive-arsenal-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('status is explicitly experimental and non-canonical',()=>{
  assert.equal(RATA_QI_ADAPTIVE_ARSENAL_STATUS,'EXPERIMENTAL_NON_CANONICAL_RATA_QI_ADAPTIVE_ARSENAL_V01');
});

T('Mordisco Frenético is T4 only and keeps physical rat identity',()=>{
  assert.equal(RATA_QI_T4_ABILITY.unlockTier,4);
  assert.equal(RATA_QI_T4_ABILITY.name,'Mordisco Frenético');
  assert.equal(RATA_QI_T4_ABILITY.effect.kind,'MULTI_HIT_BASIC_SCALAR');
  assert.equal(RATA_QI_T4_ABILITY.effect.hits,2);
  assert.equal(RATA_QI_T4_ABILITY.effect.damageScalarPerHit,0.75);
  assert.equal(RATA_QI_T4_ABILITY.effect.ignoresDefense,false);
  assert.equal(RATA_QI_T4_ABILITY.effect.ignoresAbsorption,false);
  assert.equal(RATA_QI_T4_ABILITY.effect.qiDrain,0);
  assert.equal(RATA_QI_T4_ABILITY.effect.dot,null);
  assert.equal(RATA_QI_T4_ABILITY.effect.control,null);
});

T('T4 ability is reversible with adaptive tier decay',()=>{
  assert.deepEqual(rataQiAdaptiveAbilityIds(0),[]);
  assert.deepEqual(rataQiAdaptiveAbilityIds(1),['rata_qi__survival_1']);
  assert.deepEqual(rataQiAdaptiveAbilityIds(2),['rata_qi__survival_1']);
  assert.deepEqual(rataQiAdaptiveAbilityIds(3),['rata_qi__survival_1']);
  assert.deepEqual(rataQiAdaptiveAbilityIds(4),['rata_qi__mordisco_frenetico_t4','rata_qi__survival_1']);
});

T('T2 and T3 active abilities remain explicit pending work',()=>{
  assert.ok(RATA_QI_ADAPTIVE_PROGRESSION.T2.note.includes('PENDIENTE'));
  assert.ok(RATA_QI_ADAPTIVE_PROGRESSION.T3.note.includes('PENDIENTE'));
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
