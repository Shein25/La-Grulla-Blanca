import {createRuntime as createFSMRuntime,stepFSM} from './vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree} from './vendor/bt-engine.mjs';
import {PEI_LUO_FSM} from './policies/pei-luo-fsm.mjs';
import {PEI_LUO_BT} from './policies/pei-luo-bt.mjs';
import {PEI_LUO_SCENARIOS} from './scenarios/pei-luo.scenarios.mjs';

function runFSM(events){
  let rt=createFSMRuntime(PEI_LUO_FSM),trace=[];
  for(const ev of events){const r=stepFSM(PEI_LUO_FSM,rt,ev);trace.push({event:ev.type,state:r.to,intents:r.emitted});rt=r.nextRuntime;}
  return trace;
}
function runBT(ticks){
  let rt=createBTRuntime(PEI_LUO_BT),trace=[];
  for(const t of ticks){const r=tickBehaviorTree(PEI_LUO_BT,rt,t);trace.push({facts:t.facts,status:r.status,intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction});rt=r.nextRuntime;}
  return trace;
}

const out={npc:'pei_luo',scenarios:{}};
for(const [name,s] of Object.entries(PEI_LUO_SCENARIOS)){
  out.scenarios[name]={description:s.description,fsm:runFSM(s.fsm),behaviorTree:runBT(s.bt)};
}
console.log(JSON.stringify(out,null,2));
