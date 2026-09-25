import {createRuntime as createFSMRuntime,stepFSM} from './vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree} from './vendor/bt-engine.mjs';
import {GAO_SHUN_FSM} from './policies/gao-shun-fsm.mjs';
import {GAO_SHUN_BT} from './policies/gao-shun-bt.mjs';
import {GAO_SHUN_SCENARIOS} from './scenarios/gao-shun.scenarios.mjs';

function runFSM(events){
  let rt=createFSMRuntime(GAO_SHUN_FSM),trace=[];
  for(const ev of events){const r=stepFSM(GAO_SHUN_FSM,rt,ev);trace.push({event:ev.type,state:r.to,intents:r.emitted});rt=r.nextRuntime;}
  return trace;
}
function runBT(ticks){
  let rt=createBTRuntime(GAO_SHUN_BT),trace=[];
  for(const t of ticks){const r=tickBehaviorTree(GAO_SHUN_BT,rt,t);trace.push({facts:t.facts,status:r.status,intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction});rt=r.nextRuntime;}
  return trace;
}

const out={npc:'gao_shun',scenarios:{}};
for(const [name,s] of Object.entries(GAO_SHUN_SCENARIOS)){
  out.scenarios[name]={description:s.description,fsm:runFSM(s.fsm),behaviorTree:runBT(s.bt)};
}
console.log(JSON.stringify(out,null,2));
