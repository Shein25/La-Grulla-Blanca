import {createRuntime as createFSMRuntime,stepFSM} from './vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree} from './vendor/bt-engine.mjs';
import {chooseAction} from './vendor/utility-engine-v0.1.1.mjs';
import {JIANG_RUI_UTILITY_PROFILE,UTILITY_ACTION_TO_INTENT} from './profiles/jiang-rui-utility-profile.mjs';
import {JIANG_RUI_FSM} from './policies/jiang-rui-fsm.mjs';
import {JIANG_RUI_BT} from './policies/jiang-rui-bt.mjs';
import {JIANG_RUI_SCENARIOS} from './scenarios/jiang-rui.scenarios.mjs';

function fsm(events){let rt=createFSMRuntime(JIANG_RUI_FSM),out=[];for(const e of events){const r=stepFSM(JIANG_RUI_FSM,rt,e);out.push({state:r.to,intents:r.emitted});rt=r.nextRuntime;}return out}
function bt(ticks){let rt=createBTRuntime(JIANG_RUI_BT),out=[];for(const t of ticks){const r=tickBehaviorTree(JIANG_RUI_BT,rt,t);out.push({intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction});rt=r.nextRuntime;}return out}
function utility(c){const d=chooseAction(JIANG_RUI_UTILITY_PROFILE,c);return {action:d.action,intent:UTILITY_ACTION_TO_INTENT[d.action]??null,score:d.score,top3:d.ranking.filter(x=>x.available).slice(0,3).map(x=>({action:x.name,score:x.score}))}}

const out={npc:'jiang_rui',scenarios:{}};
for(const [name,s] of Object.entries(JIANG_RUI_SCENARIOS)){
  out.scenarios[name]={description:s.description,fsm:fsm(s.fsm),behaviorTree:bt(s.bt),utility:utility(s.utility)};
}
console.log(JSON.stringify(out,null,2));
