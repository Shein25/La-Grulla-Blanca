import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {LAN_MEIHUA_UTILITY_PROFILE} from '../profiles/lan-meihua-utility-profile.mjs';
import {LAN_MEIHUA_SCENARIOS,lanContext} from '../scenarios/lan-meihua.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const CANON=data.npc_def.lan_meihua;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};
const one=r=>r.dispatchResults[0], runtime=s=>s.npcs[0];
function stateFor(){
  const world=structuredClone(LAN_MEIHUA_SCENARIOS.m16Medicine.world);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(LAN_MEIHUA_UTILITY_PROFILE),world,utilityContext:lanContext(world)}],
    schedulerConfigs:[{id:'lan_meihua_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon is Lan Meihua',()=>assert.equal(CANON.id,'lan_meihua'));
T('routes valid',()=>assert.equal(CANON.rutas.every(r=>r.every(x=>CANON.posicion_valida.includes(x))),true));
T('M16 canon makes her principal Medicina authority',()=>assert.ok(CANON.territorio_por_etapa.M16.includes('responsable principal')));
T('canonical R4 is SABE',()=>assert.equal(CANON.conocimiento_inicial.R4,'SABE'));
T('current R1-R3 projection validates',()=>assert.deepEqual(validateNpc(LAN_MEIHUA_UTILITY_PROFILE),[]));
T('adding canonical R4 is rejected by current schema',()=>{
  const npc=structuredClone(LAN_MEIHUA_UTILITY_PROFILE); npc.knowledge.R4='SABE';
  assert.ok(validateNpc(npc).some(x=>x.includes('sobran R4')));
});
T('M16 medical duty selects generic work',()=>{
  const first=tickAutonomousLoop(stateFor(),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});
T('generic medical duty reaches symbolic completion',()=>{
  const first=tickAutonomousLoop(stateFor(),1);
  const second=tickAutonomousLoop(first.state,2);
  assert.equal(one(second).status,'GOAL_REACHED');
  assert.equal(runtime(second.state).world.dutySatisfied,true);
});
T('GOAP has no patient/triage/treatment state',()=>{
  const serialized=JSON.stringify(GOAP_ACTIONS).toLowerCase();
  for(const term of ['patient','paciente','triage','tratamiento','herida','veneno','quemadura']) assert.equal(serialized.includes(term),false);
});
T('cumplir_deber remains only boolean completion',()=>{
  const a=GOAP_ACTIONS.find(x=>x.id==='cumplir_deber');
  assert.deepEqual(a.effects,{dutyPending:false,dutySatisfied:true});
});
T('canon and profile stay immutable',()=>{
  const c=JSON.stringify(CANON),p=JSON.stringify(LAN_MEIHUA_UTILITY_PROFILE);
  tickAutonomousLoop(stateFor(),1);
  assert.equal(JSON.stringify(CANON),c);
  assert.equal(JSON.stringify(LAN_MEIHUA_UTILITY_PROFILE),p);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
