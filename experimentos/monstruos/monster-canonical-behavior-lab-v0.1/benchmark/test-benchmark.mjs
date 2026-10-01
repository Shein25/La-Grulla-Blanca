import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {TIERS,resolveRuns,runMonsterBenchmark} from './core.mjs';

const M=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8')).profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('tiers remain available for future READY profiles',()=>{
  assert.deepEqual(TIERS,{smoke:1000,standard:10000,deep:100000,million:1000000});
});
T('custom runs override tier',()=>assert.equal(resolveRuns({tier:'smoke',runs:123}),123));
T('invalid runs rejected',()=>assert.throws(()=>resolveRuns({runs:0})));

T('behavior benchmark refuses pending T0 profiles',()=>{
  assert.throws(()=>runMonsterBenchmark(M,{runs:10,seed:3,mob:'all'}),/not READY/);
});

T('single pending monster is also rejected',()=>{
  assert.throws(()=>runMonsterBenchmark(M,{runs:10,seed:3,mob:'rata_qi'}),/not READY/);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
