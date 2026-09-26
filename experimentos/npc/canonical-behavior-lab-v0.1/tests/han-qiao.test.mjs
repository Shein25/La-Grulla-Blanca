import assert from 'node:assert/strict';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {HAN_QIAO_CANON,HAN_QIAO_POLICY_STATUS,HAN_QIAO_REQUIRED_MATERIAL_CAPABILITY} from '../canonical/han-qiao.mjs';
import {HAN_QIAO_UTILITY_PROFILE} from '../profiles/han-qiao-utility-profile.mjs';
import {HAN_QIAO_SCENARIOS,hanContext} from '../scenarios/han-qiao.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const runtime=(state)=>state.npcs.find(x=>x.id==='han_qiao_lab');
const one=(result)=>result.dispatchResults[0];

function stateFor(scenario){
  const world=structuredClone(scenario.world);
  const utilityContext=hanContext(world,scenario.contextOverrides);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(HAN_QIAO_UTILITY_PROFILE),world,utilityContext}],
    schedulerConfigs:[{id:'han_qiao_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon source is Han Qiao',()=>assert.equal(HAN_QIAO_CANON.id,'han_qiao'));
T('canonical routes stay inside posicion_valida',()=>assert.equal(HAN_QIAO_CANON.rutas.every(route=>route.every(x=>HAN_QIAO_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(HAN_QIAO_CANON.posicion_valida.includes(HAN_QIAO_CANON.sala_inicial),true));
T('Utility traits explicitly non-canonical',()=>assert.equal(HAN_QIAO_POLICY_STATUS.utilityTraits,'EXPERIMENTAL_NON_CANONICAL'));
T('M16 logistics hypothesis is canon-supported',()=>assert.equal(HAN_QIAO_POLICY_STATUS.m16Logistics,'CANON_SUPPORTED_M16_POLICY_HYPOTHESIS'));
T('material logistics gap is explicit',()=>assert.equal(HAN_QIAO_POLICY_STATUS.materialLogistics,'CANONICAL_DOMAIN_CAPABILITY_GAP'));
T('Utility profile validates',()=>assert.deepEqual(validateNpc(HAN_QIAO_UTILITY_PROFILE),[]));

T('ordinary low-duty request chooses player help',()=>{
  const first=tickAutonomousLoop(stateFor(HAN_QIAO_SCENARIOS.ordinaryHelp),1);
  assert.equal(one(first).utilityAction,'ayudar_jugador');
  assert.equal(one(first).goalId,'HELP_PLAYER');
  assert.equal(one(first).status,'PLAN_SESSION_CREATED');
  assert.deepEqual(runtime(first.state).executionSession.plan,['ir_jugador','ayudar_jugador']);
});

T('ordinary help plan reaches playerHelped',()=>{
  const first=tickAutonomousLoop(stateFor(HAN_QIAO_SCENARIOS.ordinaryHelp),1);
  const second=tickAutonomousLoop(first.state,2);
  const third=tickAutonomousLoop(second.state,3);
  assert.equal(one(second).executed,'ir_jugador');
  assert.equal(one(third).executed,'ayudar_jugador');
  assert.equal(one(third).status,'GOAL_REACHED');
  assert.equal(runtime(third.state).world.playerHelped,true);
});

T('M16 high logistics duty overrides simultaneous player request',()=>{
  const first=tickAutonomousLoop(stateFor(HAN_QIAO_SCENARIOS.m16Resources),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.equal(one(first).status,'PLAN_SESSION_CREATED');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});

T('M16 symbolic duty reaches dutySatisfied',()=>{
  const first=tickAutonomousLoop(stateFor(HAN_QIAO_SCENARIOS.m16Resources),1);
  const second=tickAutonomousLoop(first.state,2);
  assert.equal(one(second).executed,'cumplir_deber');
  assert.equal(one(second).status,'GOAL_REACHED');
  assert.equal(runtime(second.state).world.dutySatisfied,true);
});

T('current fulfill-duty action does not model material allocation',()=>{
  const action=GOAP_ACTIONS.find(x=>x.id==='cumplir_deber');
  assert.ok(action);
  assert.deepEqual(action.effects,{dutyPending:false,dutySatisfied:true});
  assert.equal(Object.hasOwn(action.effects,'resourcesAllocated'),false);
  assert.equal(HAN_QIAO_REQUIRED_MATERIAL_CAPABILITY,'RESOURCE_ALLOCATION_AND_LOGISTICS');
});

T('tests do not mutate canonical profile',()=>{
  const before=JSON.stringify(HAN_QIAO_CANON);
  for(const s of Object.values(HAN_QIAO_SCENARIOS))tickAutonomousLoop(stateFor(s),1);
  assert.equal(JSON.stringify(HAN_QIAO_CANON),before);
});

T('tests do not mutate Utility calibration profile',()=>{
  const before=JSON.stringify(HAN_QIAO_UTILITY_PROFILE);
  for(const s of Object.values(HAN_QIAO_SCENARIOS))tickAutonomousLoop(stateFor(s),1);
  assert.equal(JSON.stringify(HAN_QIAO_UTILITY_PROFILE),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
