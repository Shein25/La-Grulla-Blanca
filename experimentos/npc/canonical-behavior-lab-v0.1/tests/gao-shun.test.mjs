import assert from 'node:assert/strict';
import {createRuntime as createFSMRuntime,stepFSM,validateMachine} from '../vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree,validateTree} from '../vendor/bt-engine.mjs';
import {GAO_SHUN_CANON,GAO_SHUN_ALLOWED_INTENTS,GAO_SHUN_POLICY_STATUS} from '../canonical/gao-shun.mjs';
import {GAO_SHUN_FSM} from '../policies/gao-shun-fsm.mjs';
import {GAO_SHUN_BT} from '../policies/gao-shun-bt.mjs';
import {GAO_SHUN_SCENARIOS} from '../scenarios/gao-shun.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const allowed=new Set(GAO_SHUN_ALLOWED_INTENTS);

function runFSM(events){
  let rt=createFSMRuntime(GAO_SHUN_FSM),trace=[];
  for(const ev of events){
    const r=stepFSM(GAO_SHUN_FSM,rt,ev);
    trace.push({event:ev.type,state:r.to,intents:r.emitted});
    rt=r.nextRuntime;
  }
  return trace;
}
function runBT(ticks){
  let rt=createBTRuntime(GAO_SHUN_BT),trace=[];
  for(const t of ticks){
    const r=tickBehaviorTree(GAO_SHUN_BT,rt,t);
    trace.push({facts:t.facts,status:r.status,intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction});
    rt=r.nextRuntime;
  }
  return trace;
}

T('canon source is Gao Shun',()=>assert.equal(GAO_SHUN_CANON.id,'gao_shun'));
T('policy is explicitly non-canonical',()=>assert.equal(GAO_SHUN_POLICY_STATUS,'EXPERIMENTAL_NON_CANONICAL'));
T('canonical route stays inside posicion_valida',()=>assert.equal(GAO_SHUN_CANON.rutas[0].every(x=>GAO_SHUN_CANON.posicion_valida.includes(x)),true));
T('canonical initial room is valid',()=>assert.equal(GAO_SHUN_CANON.posicion_valida.includes(GAO_SHUN_CANON.sala_inicial),true));
T('FSM validates',()=>assert.doesNotThrow(()=>validateMachine(GAO_SHUN_FSM)));
T('Behavior Tree validates',()=>assert.doesNotThrow(()=>validateTree(GAO_SHUN_BT)));

for(const [name,scenario] of Object.entries(GAO_SHUN_SCENARIOS)){
  T(`${name}: FSM emits only allowed intents`,()=>{
    for(const row of runFSM(scenario.fsm)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
  T(`${name}: BT emits only allowed intents`,()=>{
    for(const row of runBT(scenario.bt)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
}

T('FSM escalation preserves observe-warn-block-return sequence',()=>{
  assert.deepEqual(runFSM(GAO_SHUN_SCENARIOS.escalation.fsm).flatMap(x=>x.intents),
    ['OBSERVE_TARGET','WARN_TARGET','BLOCK_PASSAGE','RETURN_POST','HOLD_POST']);
});
T('BT escalation reevaluates to observe-warn-block-hold',()=>{
  assert.deepEqual(runBT(GAO_SHUN_SCENARIOS.escalation.bt).flatMap(x=>x.intents),
    ['OBSERVE_TARGET','WARN_TARGET','BLOCK_PASSAGE','HOLD_POST']);
});
T('BT hostile interruption preempts patrol',()=>{
  const trace=runBT(GAO_SHUN_SCENARIOS.interruption.bt);
  assert.equal(trace[1].preempted,'patrol');
  assert.deepEqual(trace[1].intents,['BLOCK_PASSAGE']);
});
T('BT completed patrol is not falsely preempted',()=>{
  const trace=runBT(GAO_SHUN_SCENARIOS.routine.bt);
  assert.equal(trace[1].preempted,null);
});
T('FSM hostile interruption changes PATROL to BLOCK immediately',()=>{
  const trace=runFSM(GAO_SHUN_SCENARIOS.interruption.fsm);
  assert.equal(trace[0].state,'PATROL');
  assert.equal(trace[1].state,'BLOCK');
});
T('test harness does not mutate canonical profile',()=>{
  const before=JSON.stringify(GAO_SHUN_CANON);
  for(const s of Object.values(GAO_SHUN_SCENARIOS)){runFSM(s.fsm);runBT(s.bt);}
  assert.equal(JSON.stringify(GAO_SHUN_CANON),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
