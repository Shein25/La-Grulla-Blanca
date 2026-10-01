import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,buildMonsterInput} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay,TACTICAL_OVERLAY_STATUS} from '../tactics/tactical-overlay-v0.1.mjs';

const M=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8')).profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('overlay status is explicit',()=>assert.equal(TACTICAL_OVERLAY_STATUS,'EXPERIMENTAL_NON_CANONICAL_REUSE_AUDITED_WEIGHTS'));

T('overlay does not mutate ability catalog',()=>{
  const base=buildCanonicalAbilityCatalog('guardian_coral',M.guardian_coral);
  const before=JSON.stringify(base);
  applyTacticalOverlay('guardian_coral',base);
  assert.equal(JSON.stringify(base),before);
});

T('basic offensive weight remains PLAYER_LOW_HP +5',()=>{
  const id='lobo_espiritual';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).basic];
  assert.deepEqual(a.utility.signalWeights,{PLAYER_LOW_HP:5});
});

T('offensive technique weight remains PLAYER_LOW_HP +6',()=>{
  const id='lobo_espiritual';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.signalWeights,{PLAYER_LOW_HP:6});
});

T('control technique keeps absorption memory weight',()=>{
  const id='guardian_coral';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.memoryWeights,{DEFENSA_ABSORCION:-8});
});

T('MANADA technique keeps social weight',()=>{
  const id='lobo_espiritual';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.socialWeights,{MANADA_WITH_ALLY:5});
});

T('OPORTUNISTA technique keeps low-player weight',()=>{
  const id='mono_pildoras';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.socialWeights,{OPORTUNISTA_LOW_HP:15});
});

T('tactical combat decisions are blocked while T0 stats are pending',()=>{
  for(const id of ['serpiente_qi','lobo_espiritual','guardian_coral','mono_pildoras','mantis_nube']){
    assert.throws(()=>buildMonsterInput({mobId:id,def:M[id],round:1,mode:'DECISION_EXPERIMENTAL'}),/not READY/);
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
