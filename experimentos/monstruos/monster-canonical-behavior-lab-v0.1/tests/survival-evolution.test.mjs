import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  SURVIVAL_EVOLUTION_STATUS,ADAPTIVE_PARAMS_STATUS,SURVIVAL_POLICIES,
  adaptationXpGain,survivalUnlockXp,survivalEvolutionStage,
  survivalAbilityId,buildSurvivalMonsterInput
} from '../adaptive/survival-evolution-v0.1.mjs';

const M=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8')).profiles;
const combatants=Object.keys(M).sort();

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('status requires new-engine numeric recalibration',()=>{
  assert.equal(SURVIVAL_EVOLUTION_STATUS,'EXPERIMENTAL_NEW_ENGINE_PENDING_NUMERIC_CALIBRATION_V02');
  assert.equal(ADAPTIVE_PARAMS_STATUS,'PENDING_T0_T4_REBALANCE');
});

T('all 18 monsters have exactly one survival identity',()=>{
  assert.deepEqual(Object.keys(SURVIVAL_POLICIES).sort(),combatants);
});

T('adaptation XP rewards encounters, not idle calls',()=>{
  assert.equal(adaptationXpGain({rounds:0}),0);
  assert.equal(adaptationXpGain({rounds:1}),1);
  assert.equal(adaptationXpGain({rounds:4,reachedLowHp:true}),2);
  assert.equal(adaptationXpGain({rounds:4,heavyHitObserved:true}),2);
});

T('survival stage calculation remains independent of combat numbers',()=>{
  for(const id of combatants){
    const def=M[id],threshold=survivalUnlockXp(def);
    assert.equal(survivalEvolutionStage({mobId:id,def,survivalXp:threshold-1}),0,id);
    assert.equal(survivalEvolutionStage({mobId:id,def,survivalXp:threshold}),1,id);
  }
});

T('all four defensive mechanic families remain represented',()=>{
  const counts={};
  for(const policy of Object.values(SURVIVAL_POLICIES)){
    counts[policy.effect.kind]=(counts[policy.effect.kind]||0)+1;
    assert.equal(policy.effect.paramsStatus,ADAPTIVE_PARAMS_STATUS);
    assert.deepEqual(Object.keys(policy.effect).sort(),['kind','paramsStatus']);
  }
  assert.deepEqual(counts,{EVADE_NEXT:7,DEFENSE_UP:3,MITIGATE_NEXT:3,ABSORB_RESERVE:5});
});

T('survival combat input is blocked until T0 stats are READY',()=>{
  for(const id of combatants){
    const def=M[id],xp=survivalUnlockXp(def);
    assert.throws(
      ()=>buildSurvivalMonsterInput({mobId:id,def,round:1,survivalXp:xp}),
      /not READY/
    );
  }
});

T('survival ability ids remain species-scoped',()=>{
  for(const id of combatants)assert.equal(survivalAbilityId(id),`${id}__survival_1`);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
