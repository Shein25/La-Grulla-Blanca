import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  MONSTER_STAT_CONTRACT_STATUS,ENGINE_CONTRACT,ARC1_MONSTER_IDS,
  PROFILE_FIELDS,REQUIRED_STATS,TECHNIQUE_FIELDS,AI_FIELDS,ADAPTIVE_FIELDS,
  assertMonsterProfile
} from '../adaptive/monster-stat-source-contract-v0.1.mjs';

const catalog=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8'));

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('new engine is the only monster stat contract',()=>{
  assert.equal(MONSTER_STAT_CONTRACT_STATUS,'NEW_ENGINE_ONLY_V1');
  assert.equal(ENGINE_CONTRACT,'NEW_COMBAT_STATS_V0_1');
  assert.equal(catalog.status,'NEW_ENGINE_ONLY');
});

T('all 18 Arc 1 monsters are covered exactly once',()=>{
  assert.equal(ARC1_MONSTER_IDS.length,18);
  assert.deepEqual(Object.keys(catalog.profiles).sort(),ARC1_MONSTER_IDS);
});

T('all profiles match the exact active schema',()=>{
  for(const [id,p] of Object.entries(catalog.profiles)){
    assert.equal(p.id,id);
    assert.equal(p.engine_contract,ENGINE_CONTRACT);
    assert.equal(assertMonsterProfile(p,{requireReady:false}),true);
    assert.deepEqual(Object.keys(p).sort(),PROFILE_FIELDS);
    assert.deepEqual(Object.keys(p.stats).sort(),REQUIRED_STATS);
    assert.deepEqual(Object.keys(p.ai).sort(),AI_FIELDS);
    assert.deepEqual(Object.keys(p.adaptive).sort(),ADAPTIVE_FIELDS);
    if(p.technique)assert.deepEqual(Object.keys(p.technique).sort(),TECHNIQUE_FIELDS);
  }
});

T('all unresolved combat magnitudes remain null',()=>{
  const unresolved=['hp','qi_max','precision','evasion','defense','tenacity','control','basic_damage'];
  for(const [id,p] of Object.entries(catalog.profiles)){
    assert.equal(p.stats_status,'PENDING_INTEGRAL_REBALANCE',id);
    for(const key of unresolved)assert.equal(p.stats[key],null,`${id}.${key}`);
    if(p.technique){
      assert.equal(p.technique.params_status,'PENDING_INTEGRAL_REBALANCE',id);
      assert.equal(p.technique.params,null,id);
    }
  }
});

T('unknown profile fields fail schema validation',()=>{
  const p=structuredClone(catalog.profiles.rata_qi);
  p.unexpected_field=true;
  assert.throws(()=>assertMonsterProfile(p,{requireReady:false}),/schema mismatch/);
});

T('unknown technique fields fail schema validation',()=>{
  const p=structuredClone(catalog.profiles.serpiente_qi);
  p.technique.unexpected_field=true;
  assert.throws(()=>assertMonsterProfile(p,{requireReady:false}),/schema mismatch/);
});

T('pending profiles are blocked from combat',()=>{
  for(const p of Object.values(catalog.profiles)){
    assert.throws(()=>assertMonsterProfile(p),/not READY/);
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
