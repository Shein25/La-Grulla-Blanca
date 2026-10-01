import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {canonicalAbilityIds,techniqueDue,techniqueWarning} from '../adapter/canonical-combat-adapter.mjs';
import {bindMonsterIntent,canonicalTelegraph,BRIDGE_STATUS} from '../integration/canonical-intent-bridge-v0.1.mjs';

const catalog=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8'));
const M=catalog.profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('bridge targets only the new engine schema',()=>assert.equal(BRIDGE_STATUS,'EXPERIMENTAL_NEW_ENGINE_INTEGRATION_V1'));

T('pending catalog cannot bind basic combat intent',()=>{
  const id='lobo_espiritual',ids=canonicalAbilityIds(id);
  assert.throws(
    ()=>bindMonsterIntent({mobId:id,def:M[id],round:1,decision:{status:'INTENT_SELECTED',abilityId:ids.basic}}),
    /not READY/
  );
});

T('pending catalog cannot bind technique combat intent',()=>{
  const id='serpiente_qi',ids=canonicalAbilityIds(id);
  assert.throws(
    ()=>bindMonsterIntent({mobId:id,def:M[id],round:1,decision:{status:'INTENT_SELECTED',abilityId:ids.technique}}),
    /not READY/
  );
});

T('pending technique cannot expose cadence or telegraph',()=>{
  const id='serpiente_qi';
  assert.throws(()=>techniqueDue(M[id],1),/not READY/);
  assert.throws(()=>techniqueWarning(M[id],1),/not READY/);
  assert.throws(()=>canonicalTelegraph({mobId:id,def:M[id],round:1}),/not READY/);
});

T('bridge tests contain no fabricated READY monster profile',()=>{
  for(const p of Object.values(M))assert.notEqual(p.stats_status,'READY');
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
