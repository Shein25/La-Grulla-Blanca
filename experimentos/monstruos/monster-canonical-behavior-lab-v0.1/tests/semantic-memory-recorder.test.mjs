import assert from 'node:assert/strict';
import {semanticEventFromOutcome,recordSemanticOutcome} from '../integration/semantic-memory-recorder-v0.1.mjs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,baseCombat,neutralSocial,seededRng} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay} from '../tactics/tactical-overlay-v0.1.mjs';
import fs from 'node:fs';

const M=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8')).mobs;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('absorption effective maps exactly',()=>{
  assert.deepEqual(semanticEventFromOutcome({type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true}),
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:2});
});
T('absorption failure maps exactly',()=>{
  assert.deepEqual(semanticEventFromOutcome({type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:false}),
    {category:'DEFENSA_ABSORCION',result:'FALLIDA',round:2});
});
T('recovery maps exactly',()=>{
  assert.deepEqual(semanticEventFromOutcome({type:'PLAYER_RECOVERY_RESOLVED',round:3,effective:true}),
    {category:'RECUPERACION',result:'EFECTIVA',round:3});
});
T('unknown outcomes are ignored rather than invented',()=>{
  assert.equal(semanticEventFromOutcome({type:'PLAYER_DODGE_RESOLVED',round:3,effective:true}),null);
});
T('recorder preserves chronological order',()=>{
  let m=[];
  m=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true});
  m=recordSemanticOutcome(m,{type:'PLAYER_RECOVERY_RESOLVED',round:3,effective:false});
  assert.deepEqual(m.map(x=>x.round),[2,3]);
});
T('older future-incompatible outcome is rejected',()=>{
  const m=[{category:'RECUPERACION',result:'EFECTIVA',round:4}];
  assert.throws(()=>recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:3,effective:true}),/preceder/);
});
T('input memory is never mutated',()=>{
  const m=[{category:'RECUPERACION',result:'EFECTIVA',round:1}];
  const before=JSON.stringify(m);
  const next=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true});
  assert.equal(JSON.stringify(m),before);
  assert.notEqual(next,m);
});
T('returned memory/events are frozen',()=>{
  const m=recordSemanticOutcome([],{type:'PLAYER_RECOVERY_RESOLVED',round:1,effective:true});
  assert.equal(Object.isFrozen(m),true);
  assert.equal(Object.isFrozen(m[0]),true);
});
T('extra fields are rejected to prevent hidden inference',()=>{
  assert.throws(()=>semanticEventFromOutcome({type:'PLAYER_RECOVERY_RESOLVED',round:1,effective:true,hpAfter:99}),/campo no permitido/);
});
T('invalid effective is rejected',()=>{
  assert.throws(()=>semanticEventFromOutcome({type:'PLAYER_RECOVERY_RESOLVED',round:1,effective:1}),/boolean/);
});

function decision(id,memory,seed=6){
  const def=M[id],round=def.tecnica.cada;
  const monster=buildCandidateMonsterInput({mobId:id,def,round,mode:'DECISION_EXPERIMENTAL'});
  const abilities=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,def));
  return chooseMonsterIntent({
    monster,profiles:PROFILES,abilities,
    combat:baseCombat(round),memory,social:neutralSocial(),rng:seededRng(seed)
  });
}

T('recorded semantic memory is directly consumable by Monster AI',()=>{
  let m=[];
  m=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:1,effective:true});
  m=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true});
  m=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:3,effective:true});
  const r=decision('guardian_coral',m,6);
  assert.ok(r.debug.activeMemory.length>0);
  assert.deepEqual(r.debug.activeMemory,m.slice(-3));
});
T('INSTINTIVO still ignores recorder output',()=>{
  const m=recordSemanticOutcome([],{type:'PLAYER_ABSORPTION_RESOLVED',round:1,effective:true});
  const id='sapo_ceniza',def=M[id],round=def.tecnica.cada;
  const monster=buildCandidateMonsterInput({mobId:id,def,round,mode:'DECISION_EXPERIMENTAL'});
  const abilities=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,def));
  const r=chooseMonsterIntent({monster,profiles:PROFILES,abilities,combat:baseCombat(round),memory:m,social:neutralSocial(),rng:seededRng(5)});
  assert.equal(r.debug.activeMemory.length,0);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
