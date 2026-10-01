import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const data=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8'));
const M=data.profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('catalog uses the new combat-stat contract',()=>{
  assert.equal(data.schema_version,'arc1-monsters-v1');
  assert.equal(data.status,'NEW_ENGINE_ONLY');
  assert.equal(data.engine_contract,'NEW_COMBAT_STATS_V0_1');
});

T('catalog has exactly 18 Arc 1 monsters',()=>assert.equal(Object.keys(M).length,18));

T('all monsters expose the new schema',()=>{
  for(const [id,m] of Object.entries(M)){
    assert.equal(m.id,id);
    assert.equal(typeof m.name,'string',id);
    assert.equal(m.engine_contract,'NEW_COMBAT_STATS_V0_1',id);
    assert.equal(typeof m.stats,'object',id);
    assert.ok(Object.hasOwn(m.stats,'precision'),id);
    assert.ok(Object.hasOwn(m.stats,'evasion'),id);
    assert.ok(Object.hasOwn(m.stats,'defense'),id);
    assert.ok(Object.hasOwn(m.stats,'tenacity'),id);
    assert.ok(Object.hasOwn(m.stats,'control'),id);
  }
});

T('all uncalibrated T0 profiles remain explicitly pending',()=>{
  for(const [id,m] of Object.entries(M)){
    assert.equal(m.stats_status,'PENDING_INTEGRAL_REBALANCE',id);
  }
});

T('technique identities use mechanic families, not combat numbers',()=>{
  for(const [id,m] of Object.entries(M)){
    if(!m.technique)continue;
    assert.equal(typeof m.technique.name,'string',id);
    assert.ok(Array.isArray(m.technique.mechanics),id);
    assert.equal(m.technique.params_status,'PENDING_INTEGRAL_REBALANCE',id);
    assert.equal(m.technique.params,null,id);
  }
});

T('native stage distribution is 5/5/4/4',()=>{
  const counts={1:0,2:0,3:0,4:0};
  for(const m of Object.values(M))counts[m.native_stage_index]++;
  assert.deepEqual(counts,{1:5,2:5,3:4,4:4});
});

T('element set stays limited to current content',()=>{
  const set=[...new Set(Object.values(M).map(x=>x.element).filter(Boolean))].sort();
  assert.deepEqual(set,['agua','fuego','metal','viento']);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
