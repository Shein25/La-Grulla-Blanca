import assert from 'node:assert/strict';
import {
  MONSTER_STAT_SOURCE_CONTRACT_STATUS,
  ARC1_MONSTER_IDS,
  NEW_ENGINE_MONSTER_STAT_POLICY,
  assertNewEngineMonsterBase
} from '../adaptive/monster-stat-source-contract-v0.1.mjs';

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('contract explicitly requires new engine',()=>{
  assert.equal(MONSTER_STAT_SOURCE_CONTRACT_STATUS,'EXPERIMENTAL_BRIDGE_NEW_ENGINE_REQUIRED_V01');
  assert.equal(NEW_ENGINE_MONSTER_STAT_POLICY.numericSource,'NEW_ENGINE_T0_ONLY');
  assert.equal(NEW_ENGINE_MONSTER_STAT_POLICY.legacyNumericImport,'FORBIDDEN');
  assert.equal(NEW_ENGINE_MONSTER_STAT_POLICY.legacyFormulaTranslation,'FORBIDDEN');
});

T('all 18 Arc 1 monsters are covered',()=>{
  assert.equal(ARC1_MONSTER_IDS.length,18);
  assert.equal(new Set(ARC1_MONSTER_IDS).size,18);
});

T('legacy ver74-shaped combat stats are rejected',()=>{
  assert.throws(()=>assertNewEngineMonsterBase({
    engine_contract:'NEW_COMBAT_STATS_V0_1',
    stats_status:'READY_NEW_ENGINE_T0',
    numeric_source:'NEW_ENGINE_ONLY',
    hp:9,qi_max:0,precision:65,evasion:40,defense:0,tenacity:20,control:0,
    crit_chance:5,crit_damage:1.5,basic_damage:'1d4',
    ataque:1,defensa:10,'daño':'1d4'
  }),/legacy numeric field forbidden/);
});

T('complete new-engine profile is accepted',()=>{
  assert.equal(assertNewEngineMonsterBase({
    engine_contract:'NEW_COMBAT_STATS_V0_1',
    stats_status:'READY_NEW_ENGINE_T0',
    numeric_source:'NEW_ENGINE_ONLY',
    hp:24,qi_max:0,precision:90,evasion:30,defense:1,tenacity:20,control:0,
    crit_chance:5,crit_damage:1.5,basic_damage:'1d4+2'
  }),true);
});

T('pending or incomplete profiles are rejected',()=>{
  assert.throws(()=>assertNewEngineMonsterBase({
    engine_contract:'NEW_COMBAT_STATS_V0_1',
    stats_status:'PENDING_INTEGRAL_REBALANCE_NEW_ENGINE',
    numeric_source:'NEW_ENGINE_ONLY'
  }),/not READY_NEW_ENGINE_T0/);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
