import assert from 'node:assert/strict';
import {TIERS,JIANG_THRESHOLDS,resolveRuns,runBenchmark} from './core.mjs';

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('tiers monotonic',()=>assert.ok(TIERS.smoke<TIERS.standard&&TIERS.standard<TIERS.deep&&TIERS.deep<TIERS.million));
T('million tier is one million per NPC',()=>assert.equal(TIERS.million,1_000_000));
T('custom runs override tier',()=>assert.equal(resolveRuns({tier:'smoke',runs:1234}),1234));
T('invalid runs rejected',()=>assert.throws(()=>resolveRuns({runs:0})));
T('Jiang thresholds explicit',()=>assert.deepEqual(JIANG_THRESHOLDS,{highRiskDanger:60,highRiskUrgency:70}));
T('same seed same digest',()=>{
  const a=runBenchmark({runs:200,seed:42,npc:'all'});
  const b=runBenchmark({runs:200,seed:42,npc:'all'});
  assert.equal(a.digest,b.digest);
});
T('different seed changes digest',()=>{
  const a=runBenchmark({runs:200,seed:1,npc:'all'});
  const b=runBenchmark({runs:200,seed:2,npc:'all'});
  assert.notEqual(a.digest,b.digest);
});
T('Gao has no invalid intents',()=>assert.equal(runBenchmark({runs:500,seed:3,npc:'gao_shun'}).results.gao_shun.metrics.invalidIntents,0));
T('Pei has no invalid intents',()=>assert.equal(runBenchmark({runs:500,seed:4,npc:'pei_luo'}).results.pei_luo.metrics.invalidIntents,0));
T('Jiang has no invalid contexts or intents',()=>{
  const r=runBenchmark({runs:2000,seed:5,npc:'jiang_rui'}).results.jiang_rui.metrics;
  assert.equal(r.invalidContexts,0); assert.equal(r.invalidIntents,0);
});
T('Jiang FSM and BT are mostly categorical peers',()=>{
  const r=runBenchmark({runs:5000,seed:6,npc:'jiang_rui'}).results.jiang_rui.metrics;
  assert.ok(r.agreementPct.fsm_bt>90);
});
T('Jiang Utility creates measurable disagreement surface',()=>{
  const r=runBenchmark({runs:5000,seed:7,npc:'jiang_rui'}).results.jiang_rui.metrics;
  assert.ok(r.agreementPct.fsm_utility<99);
  assert.ok(Object.keys(r.utilityActions).length>=3);
});
T('all mode returns three NPC',()=>{
  const r=runBenchmark({runs:10,seed:8,npc:'all'});
  assert.deepEqual(Object.keys(r.results).sort(),['gao_shun','jiang_rui','pei_luo']);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
