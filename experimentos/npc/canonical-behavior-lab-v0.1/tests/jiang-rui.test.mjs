import assert from 'node:assert/strict';
import {createRuntime as createFSMRuntime,stepFSM,validateMachine} from '../vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree,validateTree} from '../vendor/bt-engine.mjs';
import {chooseAction,validateNpc,validateActionContext} from '../vendor/utility-engine-v0.1.1.mjs';
import {JIANG_RUI_CANON,JIANG_RUI_ALLOWED_INTENTS,JIANG_RUI_POLICY_STATUS} from '../canonical/jiang-rui.mjs';
import {JIANG_RUI_UTILITY_PROFILE,UTILITY_ACTION_TO_INTENT} from '../profiles/jiang-rui-utility-profile.mjs';
import {JIANG_RUI_FSM} from '../policies/jiang-rui-fsm.mjs';
import {JIANG_RUI_BT} from '../policies/jiang-rui-bt.mjs';
import {JIANG_RUI_SCENARIOS} from '../scenarios/jiang-rui.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const allowed=new Set(JIANG_RUI_ALLOWED_INTENTS);

function runFSM(events){
  let rt=createFSMRuntime(JIANG_RUI_FSM),trace=[];
  for(const ev of events){
    const r=stepFSM(JIANG_RUI_FSM,rt,ev);
    trace.push({event:ev.type,state:r.to,intents:r.emitted});
    rt=r.nextRuntime;
  }
  return trace;
}
function runBT(ticks){
  let rt=createBTRuntime(JIANG_RUI_BT),trace=[];
  for(const t of ticks){
    const r=tickBehaviorTree(JIANG_RUI_BT,rt,t);
    trace.push({facts:t.facts,status:r.status,intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction});
    rt=r.nextRuntime;
  }
  return trace;
}
function runUtility(context){
  const d=chooseAction(JIANG_RUI_UTILITY_PROFILE,context);
  return {
    action:d.action,
    intent:UTILITY_ACTION_TO_INTENT[d.action] ?? null,
    score:d.score,
    raw:d.raw,
    top3:d.ranking.filter(x=>x.available).slice(0,3).map(x=>({action:x.name,score:x.score,raw:x.raw}))
  };
}

T('canon source is Jiang Rui',()=>assert.equal(JIANG_RUI_CANON.id,'jiang_rui'));
T('utility traits explicitly non-canonical',()=>assert.equal(JIANG_RUI_POLICY_STATUS.utilityTraits,'EXPERIMENTAL_NON_CANONICAL'));
T('investigation hypothesis tied to LIII canon',()=>assert.equal(JIANG_RUI_POLICY_STATUS.investigate,'CANON_SUPPORTED_LIII_POLICY_HYPOTHESIS'));
T('M16 route hypothesis tied to canon',()=>assert.equal(JIANG_RUI_POLICY_STATUS.routeCrisis,'CANON_SUPPORTED_M16_POLICY_HYPOTHESIS'));
T('all canonical routes stay inside posicion_valida',()=>assert.equal(JIANG_RUI_CANON.rutas.every(route=>route.every(x=>JIANG_RUI_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(JIANG_RUI_CANON.posicion_valida.includes(JIANG_RUI_CANON.sala_inicial),true));
T('canonical transit is empty',()=>assert.deepEqual(JIANG_RUI_CANON.transito_tecnico,[]));
T('FSM validates',()=>assert.doesNotThrow(()=>validateMachine(JIANG_RUI_FSM)));
T('Behavior Tree validates',()=>assert.doesNotThrow(()=>validateTree(JIANG_RUI_BT)));
T('Utility profile validates',()=>assert.deepEqual(validateNpc(JIANG_RUI_UTILITY_PROFILE),[]));

for(const [name,scenario] of Object.entries(JIANG_RUI_SCENARIOS)){
  T(`${name}: Utility context validates`,()=>assert.deepEqual(validateActionContext(scenario.utility),[]));
  T(`${name}: FSM emits only allowed intents`,()=>{
    for(const row of runFSM(scenario.fsm)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
  T(`${name}: BT emits only allowed intents`,()=>{
    for(const row of runBT(scenario.bt)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
  T(`${name}: Utility action maps inside whitelist`,()=>{
    const u=runUtility(scenario.utility);
    assert.notEqual(u.intent,null);
    assert.equal(allowed.has(u.intent),true);
  });
}

T('routine patrol agrees across all three motors',()=>{
  const s=JIANG_RUI_SCENARIOS.routine_patrol;
  assert.deepEqual(runFSM(s.fsm)[0].intents,['PATROL_ROUTE']);
  assert.deepEqual(runBT(s.bt)[0].intents,['PATROL_ROUTE']);
  assert.equal(runUtility(s.utility).intent,'PATROL_ROUTE');
});

T('low anomaly without superior exposes Utility weighting difference',()=>{
  const s=JIANG_RUI_SCENARIOS.low_anomaly_no_superior;
  assert.deepEqual(runFSM(s.fsm)[0].intents,['INVESTIGATE_ROUTE_ANOMALY']);
  assert.deepEqual(runBT(s.bt)[0].intents,['INVESTIGATE_ROUTE_ANOMALY']);
  assert.equal(runUtility(s.utility).intent,'PATROL_ROUTE');
});

T('high anomaly without superior converges on investigation',()=>{
  const s=JIANG_RUI_SCENARIOS.high_anomaly_no_superior;
  assert.deepEqual(runFSM(s.fsm)[0].intents,['INVESTIGATE_ROUTE_ANOMALY']);
  assert.deepEqual(runBT(s.bt)[0].intents,['INVESTIGATE_ROUTE_ANOMALY']);
  assert.equal(runUtility(s.utility).intent,'INVESTIGATE_ROUTE_ANOMALY');
});

T('low anomaly with reachable superior exposes reporting choice in Utility',()=>{
  const s=JIANG_RUI_SCENARIOS.low_anomaly_with_superior;
  assert.deepEqual(runFSM(s.fsm)[0].intents,['INVESTIGATE_ROUTE_ANOMALY']);
  assert.deepEqual(runBT(s.bt)[0].intents,['INVESTIGATE_ROUTE_ANOMALY']);
  assert.equal(runUtility(s.utility).intent,'REPORT_SUPERIOR');
});

T('away from post converges on return',()=>{
  const s=JIANG_RUI_SCENARIOS.away_from_post;
  assert.deepEqual(runFSM(s.fsm)[0].intents,['RETURN_POST']);
  assert.deepEqual(runBT(s.bt)[0].intents,['RETURN_POST']);
  assert.equal(runUtility(s.utility).intent,'RETURN_POST');
});

T('M16 route crisis converges on reporting escalation',()=>{
  const s=JIANG_RUI_SCENARIOS.m16_route_crisis;
  assert.deepEqual(runFSM(s.fsm)[0].intents,['REPORT_SUPERIOR']);
  assert.deepEqual(runBT(s.bt)[0].intents,['REPORT_SUPERIOR']);
  assert.equal(runUtility(s.utility).intent,'REPORT_SUPERIOR');
});

T('Utility low-anomaly ranking is reproducible and patrol beats investigate narrowly',()=>{
  const u=runUtility(JIANG_RUI_SCENARIOS.low_anomaly_no_superior.utility);
  assert.deepEqual(u.top3.map(x=>x.action),['patrullar','investigar','esperar']);
  assert.ok(u.top3[0].score>u.top3[1].score);
});

T('Utility high-anomaly ranking flips investigation over patrol',()=>{
  const u=runUtility(JIANG_RUI_SCENARIOS.high_anomaly_no_superior.utility);
  assert.deepEqual(u.top3.map(x=>x.action),['investigar','patrullar','esperar']);
});

T('canonical profile is not mutated by harness',()=>{
  const before=JSON.stringify(JIANG_RUI_CANON);
  for(const s of Object.values(JIANG_RUI_SCENARIOS)){runFSM(s.fsm);runBT(s.bt);runUtility(s.utility);}
  assert.equal(JSON.stringify(JIANG_RUI_CANON),before);
});
T('utility calibration profile is not mutated by chooseAction',()=>{
  const before=JSON.stringify(JIANG_RUI_UTILITY_PROFILE);
  for(const s of Object.values(JIANG_RUI_SCENARIOS))runUtility(s.utility);
  assert.equal(JSON.stringify(JIANG_RUI_UTILITY_PROFILE),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
