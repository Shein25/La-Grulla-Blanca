import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  MONSTER_STAT_CONTRACT_STATUS,ENGINE_CONTRACT,ARC1_MONSTER_IDS,REQUIRED_STATS,
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

T('all profiles use the new schema',()=>{
  for(const [id,p] of Object.entries(catalog.profiles)){
    assert.equal(p.id,id);
    assert.equal(p.engine_contract,ENGINE_CONTRACT);
    assert.equal(assertMonsterProfile(p,{requireReady:false}),true);
    assert.deepEqual(Object.keys(p.stats).sort(),[...REQUIRED_STATS].sort());
  }
});

T('pending profiles are blocked from combat',()=>{
  for(const p of Object.values(catalog.profiles)){
    assert.throws(()=>assertMonsterProfile(p),/not READY/);
  }
});

T('complete READY profile is accepted',()=>{
  const p=structuredClone(catalog.profiles.rata_qi);
  p.stats_status='READY';
  p.stats={hp:24,qi_max:0,precision:90,evasion:30,defense:1,tenacity:20,control:0,crit_chance:5,crit_damage:1.5,basic_damage:'1d4+2'};
  assert.equal(assertMonsterProfile(p),true);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
