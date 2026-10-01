import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {PROFILES,SOCIAL_PROFILES} from '../vendor/profiles.mjs';
import {CANDIDATE_ASSIGNMENTS,ASSIGNMENT_STATUS} from '../profiles/candidate-assignments.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';

const data=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8'));
const M=data.profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('assignment matrix is explicitly experimental',()=>assert.equal(ASSIGNMENT_STATUS,'EXPERIMENTAL_NON_CANONICAL'));

T('all 18 monsters have exactly one candidate assignment',()=>{
  assert.deepEqual(Object.keys(CANDIDATE_ASSIGNMENTS).sort(),Object.keys(M).sort());
});

T('all cognitive profile ids exist',()=>{
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)) assert.ok(PROFILES[a.profileId],id);
});

T('all social profile ids exist',()=>{
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)) assert.ok(SOCIAL_PROFILES[a.socialProfileId],id);
});

T('every assignment has finite OFENSIVA/CONTROL preferences',()=>{
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)){
    assert.ok(Number.isFinite(a.preferences.OFENSIVA),id);
    assert.ok(Number.isFinite(a.preferences.CONTROL),id);
  }
});

T('candidate cognitive distribution remains 4/5/5/3/1',()=>{
  const c={};
  for(const a of Object.values(CANDIDATE_ASSIGNMENTS))c[a.profileId]=(c[a.profileId]||0)+1;
  assert.deepEqual(c,{INSTINTIVO:4,REACTIVO_1:5,CAZADOR_2:5,TACTICO_3:3,MASTER_4:1});
});

T('pending T0 stats block combat input instead of using alternate values',()=>{
  for(const [id,def] of Object.entries(M)){
    assert.throws(
      ()=>buildCandidateMonsterInput({mobId:id,def,round:1,mode:'DECISION_EXPERIMENTAL'}),
      /not READY/
    );
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
