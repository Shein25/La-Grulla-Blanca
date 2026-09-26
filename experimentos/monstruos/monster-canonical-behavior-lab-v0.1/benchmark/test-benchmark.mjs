import assert from 'node:assert/strict';
import fs from 'node:fs';
import {TIERS,resolveRuns,runMonsterBenchmark} from './core.mjs';

const M=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8')).mobs;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('tiers scale to one million per selected mob',()=>{
  assert.deepEqual(TIERS,{smoke:1000,standard:10000,deep:100000,million:1000000});
});
T('custom runs override tier',()=>assert.equal(resolveRuns({tier:'smoke',runs:123}),123));
T('invalid runs rejected',()=>assert.throws(()=>resolveRuns({runs:0})));
T('same seed yields same digest',()=>{
  const a=runMonsterBenchmark(M,{runs:100,seed:42,mob:'all'});
  const b=runMonsterBenchmark(M,{runs:100,seed:42,mob:'all'});
  assert.equal(a.digest,b.digest);
});
T('different seed changes digest',()=>{
  const a=runMonsterBenchmark(M,{runs:100,seed:1,mob:'all'});
  const b=runMonsterBenchmark(M,{runs:100,seed:2,mob:'all'});
  assert.notEqual(a.digest,b.digest);
});
T('all mode covers exactly 18 combatants',()=>{
  const r=runMonsterBenchmark(M,{runs:10,seed:3,mob:'all'});
  assert.equal(r.mobCount,18);
  assert.equal(Object.hasOwn(r.results,'muneco_practica'),false);
});
T('smoke sample has zero cadence violations and invalid selections',()=>{
  const r=runMonsterBenchmark(M,{runs:1000,seed:4,mob:'all'});
  for(const [id,x] of Object.entries(r.results)){
    assert.equal(x.metrics.cadenceViolations,0,id);
    assert.equal(x.metrics.invalidSelections,0,id);
  }
});
T('INSTINTIVO sapo has zero memory-driven changes',()=>{
  const r=runMonsterBenchmark(M,{runs:3000,seed:5,mob:'sapo_ceniza'}).results.sapo_ceniza.metrics;
  assert.equal(r.memoryChangedDecision,0);
});
T('TACTICO guardian shows memory-driven decision changes',()=>{
  const r=runMonsterBenchmark(M,{runs:5000,seed:6,mob:'guardian_coral'}).results.guardian_coral.metrics;
  assert.ok(r.memoryChangedDecision>0);
});
T('MANADA lobo shows social-driven decision changes',()=>{
  const r=runMonsterBenchmark(M,{runs:5000,seed:7,mob:'lobo_espiritual'}).results.lobo_espiritual.metrics;
  assert.ok(r.socialChangedDecision>0);
});
T('OPORTUNISTA mono shows social-driven decision changes',()=>{
  const r=runMonsterBenchmark(M,{runs:5000,seed:8,mob:'mono_pildoras'}).results.mono_pildoras.metrics;
  assert.ok(r.socialChangedDecision>0);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
