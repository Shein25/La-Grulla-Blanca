import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';

import {
  MONSTER_STAGE_PROGRESSION_STATUS,STAGE_ROLES,STAGE_BANDS,
  NATIVE_STAGE_BY_MOB,nativeStageOf,stageRelation,adaptiveCapabilityCeiling
} from '../adaptive/stage-progression-v0.1.mjs';

const here=dirname(fileURLToPath(import.meta.url));
const snapshot=JSON.parse(readFileSync(resolve(here,'../canonical/MOBS_ver74.snapshot.json'),'utf8'));
const combatants=Object.keys(snapshot.mobs).filter(id=>id!=='muneco_practica').sort();

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(err){fail++;console.error('FAIL',name);console.error(err.stack||err)}};

T('stage progression is explicitly experimental',()=>{
  assert.equal(MONSTER_STAGE_PROGRESSION_STATUS,'EXPERIMENTAL_NON_CANONICAL_STAGE_PROGRESSION_V01');
});

T('all 18 combatants receive exactly one native stage assignment',()=>{
  assert.deepEqual(Object.keys(NATIVE_STAGE_BY_MOB).sort(),combatants);
});

T('every assignment uses stage 1..4 and a declared role',()=>{
  for(const [id,x] of Object.entries(NATIVE_STAGE_BY_MOB)){
    assert.ok(STAGE_BANDS[x.stage],id);
    assert.ok(STAGE_ROLES.includes(x.role),id);
  }
});

T('stage distribution is 5/5/4/4',()=>{
  const counts={1:0,2:0,3:0,4:0};
  for(const x of Object.values(NATIVE_STAGE_BY_MOB))counts[x.stage]++;
  assert.deepEqual(counts,{1:5,2:5,3:4,4:4});
});

T('nativeStageOf returns declared stage',()=>{
  for(const [id,x] of Object.entries(NATIVE_STAGE_BY_MOB))assert.equal(nativeStageOf(id),x.stage,id);
});

T('player below native stage never grants extra adaptive tier',()=>{
  for(const [id,x] of Object.entries(NATIVE_STAGE_BY_MOB)){
    if(x.stage===1)continue;
    const c=adaptiveCapabilityCeiling(id,x.stage-1);
    assert.equal(c.tier,1,id);
    assert.equal(c.relation,'AHEAD_OF_PLAYER',id);
  }
});

T('outgrowing native stage raises capability ceiling without stats',()=>{
  const c1=adaptiveCapabilityCeiling('rata_qi',1);
  const c4=adaptiveCapabilityCeiling('rata_qi',4);
  assert.equal(c1.tier,1);
  assert.equal(c4.tier,4);
  assert.ok(c4.capabilities.includes('SECONDARY_ADAPTATION_ELIGIBLE'));
  assert.equal('hp' in c4,false);
  assert.equal('attack' in c4,false);
  assert.equal('defense' in c4,false);
});

T('stageRelation distinguishes native match and outgrown band',()=>{
  assert.equal(stageRelation('pez_lunar',3).relation,'NATIVE_MATCH');
  assert.equal(stageRelation('pez_lunar',4).relation,'PLAYER_OUTGREW_NATIVE_STAGE');
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
