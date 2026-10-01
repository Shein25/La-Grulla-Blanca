import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {canonicalAbilityIds,techniqueDue,techniqueWarning} from '../adapter/canonical-combat-adapter.mjs';
import {bindMonsterIntent,canonicalTelegraph,BRIDGE_STATUS} from '../integration/canonical-intent-bridge-v0.1.mjs';

const catalog=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8'));
const M=catalog.profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function ready(id,{cadence=3}={}){
  const p=structuredClone(M[id]);
  p.stats_status='READY';
  p.stats={hp:30,qi_max:0,precision:80,evasion:40,defense:1,tenacity:20,control:0,crit_chance:5,crit_damage:1.5,basic_damage:'1d6+1'};
  if(p.technique){
    p.technique.params_status='READY';
    p.technique.params={cadence,direct_damage:'1d6+3'};
  }
  return p;
}

T('bridge targets only the new engine schema',()=>assert.equal(BRIDGE_STATUS,'EXPERIMENTAL_NEW_ENGINE_INTEGRATION_V1'));

T('pending catalog cannot bind combat intent',()=>{
  const id='lobo_espiritual',ids=canonicalAbilityIds(id);
  assert.throws(
    ()=>bindMonsterIntent({mobId:id,def:M[id],round:1,decision:{status:'INTENT_SELECTED',abilityId:ids.basic}}),
    /not READY/
  );
});

T('READY basic binding exposes new-engine combat fields',()=>{
  const id='lobo_espiritual',def=ready(id),ids=canonicalAbilityIds(id);
  const b=bindMonsterIntent({mobId:id,def,round:1,decision:{status:'INTENT_SELECTED',abilityId:ids.basic}});
  assert.equal(b.kind,'BASIC_ATTACK');
  assert.deepEqual(b.combat,{
    precision:80,damage:'1d6+1',critChance:5,critDamage:1.5,element:null
  });
});

T('READY technique respects explicit new cadence',()=>{
  const id='lobo_espiritual',def=ready(id,{cadence:3}),ids=canonicalAbilityIds(id);
  assert.equal(techniqueDue(def,3),true);
  assert.equal(techniqueDue(def,2),false);
  const b=bindMonsterIntent({mobId:id,def,round:3,decision:{status:'INTENT_SELECTED',abilityId:ids.technique}});
  assert.equal(b.kind,'TECHNIQUE');
  assert.deepEqual(b.combat,def.technique);
});

T('telegraph uses new technique params',()=>{
  const id='serpiente_qi',def=ready(id,{cadence:4});
  assert.equal(techniqueWarning(def,3),true);
  const t=canonicalTelegraph({mobId:id,def,round:3});
  assert.equal(t.executesOnRound,4);
  assert.equal(t.techniqueName,def.technique.name);
  assert.equal(t.cadence,4);
});

T('off-cadence technique is rejected',()=>{
  const id='serpiente_qi',def=ready(id,{cadence:4}),ids=canonicalAbilityIds(id);
  assert.throws(
    ()=>bindMonsterIntent({mobId:id,def,round:2,decision:{status:'INTENT_SELECTED',abilityId:ids.technique}}),
    /CADENCE_VIOLATION/
  );
});

T('bound orders are deep-frozen',()=>{
  const id='serpiente_qi',def=ready(id),ids=canonicalAbilityIds(id);
  const b=bindMonsterIntent({mobId:id,def,round:3,decision:{status:'INTENT_SELECTED',abilityId:ids.technique}});
  assert.equal(Object.isFrozen(b),true);
  assert.equal(Object.isFrozen(b.combat),true);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
