import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,baseCombat,neutralSocial,seededRng,canonicalAbilityIds} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay} from '../tactics/tactical-overlay-v0.1.mjs';
import {bindMonsterIntent} from '../integration/canonical-intent-bridge-v0.1.mjs';
import {absorptionOutcomeFromResolvedHit} from '../integration/resolved-combat-signal-adapter-v0.1.mjs';
import {recordSemanticOutcome} from '../integration/semantic-memory-recorder-v0.1.mjs';

const M=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8')).mobs;
const id='guardian_coral';
const def=M[id];
const round=def.tecnica.cada;
const ids=canonicalAbilityIds(id);

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function decide(mode,memory){
  const monster=buildCandidateMonsterInput({mobId:id,def,round,mode});
  const abilities=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,def));
  return chooseMonsterIntent({
    monster,
    profiles:PROFILES,
    abilities,
    combat:baseCombat(round,{selfHp:0.2,playerHp:0.05}),
    memory,
    social:neutralSocial(),
    rng:seededRng(1)
  });
}
function absorptionMemory(){
  let memory=[];
  for(let r=1;r<=3;r++){
    const outcome=absorptionOutcomeFromResolvedHit({round:r,absorbido:4});
    memory=recordSemanticOutcome(memory,outcome);
  }
  return memory;
}

const neutral=decide('DECISION_EXPERIMENTAL',[]);
const memory=absorptionMemory();
const adaptive=decide('DECISION_EXPERIMENTAL',memory);
const cadence=decide('CADENCE_COMPAT',memory);

T('fixture round is canonical technique round',()=>assert.equal(round%def.tecnica.cada,0));
T('neutral experimental decision selects canonical technique',()=>assert.equal(neutral.abilityId,ids.technique));
T('neutral decision binds to canonical TECHNIQUE order',()=>{
  const order=bindMonsterIntent({mobId:id,def,round,decision:neutral});
  assert.equal(order.kind,'TECHNIQUE');
  assert.deepEqual(order.canonical,def.tecnica);
});
T('three resolved absorptions become three semantic memory events',()=>{
  assert.deepEqual(memory,[
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:1},
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:2},
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:3}
  ]);
});
T('memory is visible to tactical decision',()=>assert.deepEqual(adaptive.debug.activeMemory,memory));
T('memory contributes exactly -24 to Guardian technique',()=>{
  const row=adaptive.debug.considered.find(x=>x.abilityId===ids.technique);
  assert.equal(row.breakdown.memory,-24);
});
T('experimental decision changes technique to basic after effective absorption history',()=>{
  assert.equal(adaptive.abilityId,ids.basic);
  assert.notEqual(adaptive.abilityId,neutral.abilityId);
});
T('adaptive basic binds to canonical BASIC_ATTACK order',()=>{
  const order=bindMonsterIntent({mobId:id,def,round,decision:adaptive});
  assert.equal(order.kind,'BASIC_ATTACK');
  assert.equal(order.canonical.daño,def.daño);
});
T('CADENCE_COMPAT ignores tactical alternative and still selects technique',()=>assert.equal(cadence.abilityId,ids.technique));
T('CADENCE_COMPAT bound order preserves canonical technique payload after memory',()=>{
  const order=bindMonsterIntent({mobId:id,def,round,decision:cadence});
  assert.equal(order.kind,'TECHNIQUE');
  assert.deepEqual(order.canonical,def.tecnica);
});
T('feedback loop does not mutate canonical mob definition',()=>{
  const before=JSON.stringify(def);
  decide('DECISION_EXPERIMENTAL',absorptionMemory());
  assert.equal(JSON.stringify(def),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
