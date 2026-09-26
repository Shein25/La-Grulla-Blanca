import assert from 'node:assert/strict';
import {createRuntime as createFSMRuntime,stepFSM,validateMachine} from '../vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree,validateTree} from '../vendor/bt-engine.mjs';
import {PEI_LUO_CANON,PEI_LUO_ALLOWED_INTENTS,PEI_LUO_POLICY_STATUS} from '../canonical/pei-luo.mjs';
import {PEI_LUO_FSM} from '../policies/pei-luo-fsm.mjs';
import {PEI_LUO_BT} from '../policies/pei-luo-bt.mjs';
import {PEI_LUO_SCENARIOS} from '../scenarios/pei-luo.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const allowed=new Set(PEI_LUO_ALLOWED_INTENTS);

function runFSM(events){
  let rt=createFSMRuntime(PEI_LUO_FSM),trace=[];
  for(const ev of events){
    const r=stepFSM(PEI_LUO_FSM,rt,ev);
    trace.push({event:ev.type,state:r.to,intents:r.emitted});
    rt=r.nextRuntime;
  }
  return trace;
}
function runBT(ticks){
  let rt=createBTRuntime(PEI_LUO_BT),trace=[];
  for(const t of ticks){
    const r=tickBehaviorTree(PEI_LUO_BT,rt,t);
    trace.push({facts:t.facts,status:r.status,intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction});
    rt=r.nextRuntime;
  }
  return trace;
}

T('canon source is Pei Luo',()=>assert.equal(PEI_LUO_CANON.id,'pei_luo'));
T('normal routine is explicitly experimental',()=>assert.equal(PEI_LUO_POLICY_STATUS.normalRoutine,'EXPERIMENTAL_NON_CANONICAL'));
T('crisis-rations hypothesis is tied to M16 canon',()=>assert.equal(PEI_LUO_POLICY_STATUS.crisisRations,'CANON_SUPPORTED_M16_POLICY_HYPOTHESIS'));
T('canonical route stays inside posicion_valida',()=>assert.equal(PEI_LUO_CANON.rutas[0].every(x=>PEI_LUO_CANON.posicion_valida.includes(x)),true));
T('canonical initial room is valid',()=>assert.equal(PEI_LUO_CANON.posicion_valida.includes(PEI_LUO_CANON.sala_inicial),true));
T('canonical transit is empty',()=>assert.deepEqual(PEI_LUO_CANON.transito_tecnico,[]));
T('FSM validates',()=>assert.doesNotThrow(()=>validateMachine(PEI_LUO_FSM)));
T('Behavior Tree validates',()=>assert.doesNotThrow(()=>validateTree(PEI_LUO_BT)));

for(const [name,scenario] of Object.entries(PEI_LUO_SCENARIOS)){
  T(`${name}: FSM emits only allowed intents`,()=>{
    for(const row of runFSM(scenario.fsm)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
  T(`${name}: BT emits only allowed intents`,()=>{
    for(const row of runBT(scenario.bt)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
}

T('FSM routine preserves explicit work cycle',()=>{
  assert.deepEqual(runFSM(PEI_LUO_SCENARIOS.routine.fsm).flatMap(x=>x.intents),
    ['MOVE_TO_DINING','SERVE_RATIONS','RETURN_KITCHEN','RESET_KITCHEN','PREPARE_RATIONS']);
});
T('BT routine produces same observable work intents',()=>{
  assert.deepEqual(runBT(PEI_LUO_SCENARIOS.routine.bt).flatMap(x=>x.intents),
    ['MOVE_TO_DINING','SERVE_RATIONS','RETURN_KITCHEN','RESET_KITCHEN','PREPARE_RATIONS']);
});
T('FSM crisis interrupts SERVE into CRISIS',()=>{
  const trace=runFSM(PEI_LUO_SCENARIOS.crisis_interrupts_service.fsm);
  assert.equal(trace[1].state,'SERVE');
  assert.equal(trace[2].state,'CRISIS');
  assert.deepEqual(trace[2].intents,['ORGANIZE_CRISIS_RATIONS']);
});
T('BT crisis preempts serve immediately',()=>{
  const trace=runBT(PEI_LUO_SCENARIOS.crisis_interrupts_service.bt);
  assert.equal(trace[2].preempted,'serve');
  assert.deepEqual(trace[2].intents,['ORGANIZE_CRISIS_RATIONS']);
});
T('BT crisis preempts prepare immediately',()=>{
  const trace=runBT(PEI_LUO_SCENARIOS.crisis_from_prep.bt);
  assert.equal(trace[1].preempted,'prepare');
  assert.deepEqual(trace[1].intents,['ORGANIZE_CRISIS_RATIONS']);
});
T('FSM exits crisis through explicit return state',()=>{
  const trace=runFSM(PEI_LUO_SCENARIOS.crisis_from_prep.fsm);
  assert.equal(trace[0].state,'CRISIS');
  assert.equal(trace[1].state,'RETURN');
  assert.deepEqual(trace[1].intents,['RETURN_KITCHEN']);
});
T('canonical profile is not mutated by harness',()=>{
  const before=JSON.stringify(PEI_LUO_CANON);
  for(const s of Object.values(PEI_LUO_SCENARIOS)){runFSM(s.fsm);runBT(s.bt);}
  assert.equal(JSON.stringify(PEI_LUO_CANON),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
