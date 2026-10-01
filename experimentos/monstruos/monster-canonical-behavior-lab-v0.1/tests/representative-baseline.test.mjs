import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {
  ADAPTER_STATUS,PROFILE_ASSIGNMENTS,HARNESS_DEFAULT_ASSIGNMENT,
  buildCanonicalAbilityCatalog,buildMonsterInput
} from '../adapter/canonical-combat-adapter.mjs';

const data=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8'));
const M=data.profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('adapter is new-engine-only',()=>assert.equal(ADAPTER_STATUS,'EXPERIMENTAL_NEW_ENGINE_ONLY'));

T('default assignment is only harness fallback',()=>{
  assert.equal(HARNESS_DEFAULT_ASSIGNMENT.profileId,'INSTINTIVO');
  assert.equal(HARNESS_DEFAULT_ASSIGNMENT.socialProfileId,'SOLITARIO');
});

T('five representative assignments are explicit',()=>{
  assert.deepEqual(Object.keys(PROFILE_ASSIGNMENTS).sort(),[
    'devorador_niebla','lobo_espiritual','mantis_nube','rata_qi','serpiente_qi'
  ]);
});

T('representative cognitive ladder is wired 0..4',()=>{
  assert.equal(PROFILE_ASSIGNMENTS.rata_qi.profileId,'INSTINTIVO');
  assert.equal(PROFILE_ASSIGNMENTS.serpiente_qi.profileId,'REACTIVO_1');
  assert.equal(PROFILE_ASSIGNMENTS.lobo_espiritual.profileId,'CAZADOR_2');
  assert.equal(PROFILE_ASSIGNMENTS.devorador_niebla.profileId,'TACTICO_3');
  assert.equal(PROFILE_ASSIGNMENTS.mantis_nube.profileId,'MASTER_4');
});

T('identity ability catalogs build without numeric fallback',()=>{
  for(const [id,def] of Object.entries(M)){
    const catalog=buildCanonicalAbilityCatalog(id,def);
    assert.ok(catalog[`${id}__basic`],id);
    if(def.technique)assert.ok(catalog[`${id}__technique`],id);
  }
});

T('combat input is blocked until T0 stats and technique params are READY',()=>{
  for(const [id,def] of Object.entries(M)){
    assert.throws(()=>buildMonsterInput({mobId:id,def,round:1,mode:'CADENCE_COMPAT'}),/not READY/);
  }
});

T('identity adapter does not inject memory/social weights',()=>{
  for(const [id,def] of Object.entries(M)){
    const catalog=buildCanonicalAbilityCatalog(id,def);
    for(const a of Object.values(catalog)){
      assert.deepEqual(a.utility.memoryWeights,{},id+':'+a.id);
      assert.deepEqual(a.utility.socialWeights,{},id+':'+a.id);
      assert.deepEqual(a.utility.signalWeights,{},id+':'+a.id);
    }
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
