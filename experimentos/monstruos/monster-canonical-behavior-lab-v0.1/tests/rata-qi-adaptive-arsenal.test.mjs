import assert from 'node:assert/strict';
import {
  RATA_QI_ADAPTIVE_ARSENAL_STATUS,
  RATA_QI_T4_PARAMS_STATUS,
  RATA_QI_T4_ABILITY,
  RATA_QI_ADAPTIVE_PROGRESSION,
  rataQiAdaptiveAbilityIds
} from '../adaptive/rata-qi-adaptive-arsenal-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('Rata T4 is new-engine identity with numeric calibration pending',()=>{
  assert.equal(RATA_QI_ADAPTIVE_ARSENAL_STATUS,'EXPERIMENTAL_NEW_ENGINE_PENDING_NUMERIC_CALIBRATION_V02');
  assert.equal(RATA_QI_T4_PARAMS_STATUS,'PENDING_T0_T4_REBALANCE');
});

T('Mordisco Frenético keeps identity but no pre-T0 combat numbers',()=>{
  assert.equal(RATA_QI_T4_ABILITY.unlockTier,4);
  assert.equal(RATA_QI_T4_ABILITY.name,'Mordisco Frenético');
  assert.deepEqual(
    RATA_QI_T4_ABILITY.effect,
    {kind:'MULTI_HIT_BASIC_SCALAR',paramsStatus:'PENDING_T0_T4_REBALANCE'}
  );
  for(const forbidden of [
    'hits','damageScalarPerHit','independentHitRolls','defenseAppliedPerHit',
    'absorptionAppliedPerHit','ignoresDefense','ignoresAbsorption','qiDrain','dot','control'
  ])assert.equal(Object.hasOwn(RATA_QI_T4_ABILITY.effect,forbidden),false,forbidden);
});

T('T4 ability is reversible with adaptive tier decay',()=>{
  assert.deepEqual(rataQiAdaptiveAbilityIds(0),[]);
  assert.deepEqual(rataQiAdaptiveAbilityIds(1),['rata_qi__survival_1']);
  assert.deepEqual(rataQiAdaptiveAbilityIds(2),['rata_qi__survival_1']);
  assert.deepEqual(rataQiAdaptiveAbilityIds(3),['rata_qi__survival_1']);
  assert.deepEqual(rataQiAdaptiveAbilityIds(4),['rata_qi__mordisco_frenetico_t4','rata_qi__survival_1']);
});

T('T1-T4 notes keep pending numeric work explicit',()=>{
  assert.ok(RATA_QI_ADAPTIVE_PROGRESSION.T1.note.includes('pendientes'));
  assert.ok(RATA_QI_ADAPTIVE_PROGRESSION.T2.note.includes('PENDIENTE'));
  assert.ok(RATA_QI_ADAPTIVE_PROGRESSION.T3.note.includes('PENDIENTE'));
  assert.ok(RATA_QI_ADAPTIVE_PROGRESSION.T4.note.includes('PENDIENTES'));
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
