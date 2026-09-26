import assert from 'node:assert/strict';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {QIAO_REN_CANON,QIAO_REN_POLICY_STATUS,QIAO_REN_M17_REQUIRED_CAPABILITY} from '../canonical/qiao-ren.mjs';
import {QIAO_REN_UTILITY_PROFILE} from '../profiles/qiao-ren-utility-profile.mjs';
import {QIAO_REN_SCENARIOS,qiaoContext} from '../scenarios/qiao-ren.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const runtime=(state)=>state.npcs.find(x=>x.id==='qiao_ren_lab');
const one=(result)=>result.dispatchResults[0];

function stateFor(scenario){
  const world=structuredClone(scenario.world);
  const utilityContext=qiaoContext(world,scenario.contextOverrides);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(QIAO_REN_UTILITY_PROFILE),world,utilityContext}],
    schedulerConfigs:[{id:'qiao_ren_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon source is Qiao Ren',()=>assert.equal(QIAO_REN_CANON.id,'qiao_ren'));
T('canonical route stays inside posicion_valida',()=>assert.equal(QIAO_REN_CANON.rutas[0].every(x=>QIAO_REN_CANON.posicion_valida.includes(x)),true));
T('canonical route keeps SECTA_INTERIOR gate',()=>assert.deepEqual(QIAO_REN_CANON.gates_en_ruta,['SECTA_INTERIOR']));
T('utility traits explicitly non-canonical',()=>assert.equal(QIAO_REN_POLICY_STATUS.utilityTraits,'EXPERIMENTAL_NON_CANONICAL'));
T('M17 authorization is explicitly a capability gap',()=>assert.equal(QIAO_REN_POLICY_STATUS.m17Authorization,'CANONICAL_REQUIREMENT_CAPABILITY_GAP'));
T('Utility profile validates',()=>assert.deepEqual(validateNpc(QIAO_REN_UTILITY_PROFILE),[]));

T('routine duty creates a FULFILL_DUTY plan',()=>{
  const first=tickAutonomousLoop(stateFor(QIAO_REN_SCENARIOS.routineDuty),1);
  assert.equal(one(first).path,'DECISION');
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.equal(one(first).status,'PLAN_SESSION_CREATED');
  assert.ok(runtime(first.state).executionSession);
  assert.ok(runtime(first.state).executionSession.plan.length>=1);
});

T('routine duty reaches goal on later dispatch',()=>{
  const first=tickAutonomousLoop(stateFor(QIAO_REN_SCENARIOS.routineDuty),1);
  const second=tickAutonomousLoop(first.state,2);
  assert.equal(one(second).path,'EXECUTION');
  assert.equal(one(second).status,'GOAL_REACHED');
  assert.equal(one(second).executed,'cumplir_deber');
  assert.equal(runtime(second.state).world.dutySatisfied,true);
  assert.equal(runtime(second.state).executionSession,null);
});

T('M16 coordination with evidence selects reporting goal',()=>{
  const first=tickAutonomousLoop(stateFor(QIAO_REN_SCENARIOS.m16CoordinationWithEvidence),1);
  assert.equal(one(first).path,'DECISION');
  assert.equal(one(first).utilityAction,'informar_superior');
  assert.equal(one(first).goalId,'REPORT_SUPERIOR');
  assert.equal(one(first).status,'PLAN_SESSION_CREATED');
  assert.ok(runtime(first.state).executionSession.plan.length>=1);
});

T('return-to-post scenario selects RETURN_POST',()=>{
  const first=tickAutonomousLoop(stateFor(QIAO_REN_SCENARIOS.returnToPost),1);
  assert.equal(one(first).path,'DECISION');
  assert.equal(one(first).utilityAction,'regresar_puesto');
  assert.equal(one(first).goalId,'RETURN_POST');
  assert.equal(one(first).status,'PLAN_SESSION_CREATED');
});

T('current GOAP vocabulary does not implement canonical M17 authorization',()=>{
  const serialized=JSON.stringify(GOAP_ACTIONS).toLowerCase();
  assert.equal(serialized.includes('nucleo_profundo'),false);
  assert.equal(serialized.includes('authorize_exception'),false);
  assert.equal(serialized.includes('autorizar'),false);
  assert.equal(QIAO_REN_M17_REQUIRED_CAPABILITY,'AUTHORIZE_EXCEPTION_NUCLEO_PROFUNDO');
});

T('autonomous scenarios do not mutate canonical profile',()=>{
  const before=JSON.stringify(QIAO_REN_CANON);
  for(const s of Object.values(QIAO_REN_SCENARIOS)){
    let st=stateFor(s);
    const first=tickAutonomousLoop(st,1);
    if(runtime(first.state).executionSession) tickAutonomousLoop(first.state,2);
  }
  assert.equal(JSON.stringify(QIAO_REN_CANON),before);
});

T('autonomous scenarios do not mutate Utility calibration profile',()=>{
  const before=JSON.stringify(QIAO_REN_UTILITY_PROFILE);
  for(const s of Object.values(QIAO_REN_SCENARIOS)) tickAutonomousLoop(stateFor(s),1);
  assert.equal(JSON.stringify(QIAO_REN_UTILITY_PROFILE),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
