import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {evaluateDialogueTopic,validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {SONG_RUI_UTILITY_PROFILE} from '../profiles/song-rui-utility-profile.mjs';
import {SONG_RUI_SCENARIOS,songContext} from '../scenarios/song-rui.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const CANON=data.npc_def.song_rui;

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};
const one=r=>r.dispatchResults[0];
const runtime=s=>s.npcs.find(x=>x.id==='song_rui_lab');
function stateFor(){
  const world=structuredClone(SONG_RUI_SCENARIOS.m16ArchiveProtection.world);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(SONG_RUI_UTILITY_PROFILE),world,utilityContext:songContext(world)}],
    schedulerConfigs:[{id:'song_rui_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon is Song Rui',()=>assert.equal(CANON.id,'song_rui'));
T('canonical routes valid',()=>assert.equal(CANON.rutas.every(r=>r.every(x=>CANON.posicion_valida.includes(x))),true));
T('R3 is canonically SABE',()=>assert.equal(CANON.conocimiento_inicial.R3,'SABE'));
T('R4 R5 R6 R9 are canonically SOSPECHA',()=>{
  for(const k of ['R4','R5','R6','R9']) assert.equal(CANON.conocimiento_inicial[k],'SOSPECHA');
});
T('Utility profile validates current R1-R3 projection',()=>assert.deepEqual(validateNpc(SONG_RUI_UTILITY_PROFILE),[]));

T('R3 can be evaluated as known knowledge',()=>{
  const r=evaluateDialogueTopic(SONG_RUI_UTILITY_PROFILE,'R3',SONG_RUI_SCENARIOS.r3Dialogue.dialogueContext);
  assert.equal(r.state,'SABE');
  assert.notEqual(r.mode,'NO_SABE');
  assert.ok(r.disclosure>0);
});
T('adding canonical R4 breaks current knowledge schema',()=>{
  const npc=structuredClone(SONG_RUI_UTILITY_PROFILE);
  npc.knowledge.R4='SOSPECHA';
  assert.ok(validateNpc(npc).some(x=>x.includes('sobran R4')));
});
T('adding all extra known/suspected canonical topics is rejected',()=>{
  const npc=structuredClone(SONG_RUI_UTILITY_PROFILE);
  for(const k of ['R4','R5','R6','R9']) npc.knowledge[k]=CANON.conocimiento_inicial[k];
  const errors=validateNpc(npc);
  for(const k of ['R4','R5','R6','R9']) assert.ok(errors.some(x=>x.includes(k)));
});

T('M16 archive protection selects generic work goal',()=>{
  const first=tickAutonomousLoop(stateFor(),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});
T('generic archive duty reaches symbolic completion',()=>{
  const first=tickAutonomousLoop(stateFor(),1);
  const second=tickAutonomousLoop(first.state,2);
  assert.equal(one(second).executed,'cumplir_deber');
  assert.equal(one(second).status,'GOAL_REACHED');
  assert.equal(runtime(second.state).world.dutySatisfied,true);
});
T('cumplir_deber contains no archive/document semantics',()=>{
  const action=GOAP_ACTIONS.find(x=>x.id==='cumplir_deber');
  assert.ok(action);
  assert.deepEqual(action.effects,{dutyPending:false,dutySatisfied:true});
  const serialized=JSON.stringify(action).toLowerCase();
  for(const term of ['archivo','document','catalog','proteger']) assert.equal(serialized.includes(term),false);
});
T('canon remains immutable',()=>{
  const before=JSON.stringify(CANON);
  evaluateDialogueTopic(SONG_RUI_UTILITY_PROFILE,'R3',SONG_RUI_SCENARIOS.r3Dialogue.dialogueContext);
  assert.equal(JSON.stringify(CANON),before);
});
T('profile remains immutable',()=>{
  const before=JSON.stringify(SONG_RUI_UTILITY_PROFILE);
  tickAutonomousLoop(stateFor(),1);
  assert.equal(JSON.stringify(SONG_RUI_UTILITY_PROFILE),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
