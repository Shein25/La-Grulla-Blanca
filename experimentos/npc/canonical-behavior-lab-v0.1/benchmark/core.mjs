import crypto from 'node:crypto';
import {createRuntime as createFSMRuntime,stepFSM} from '../vendor/fsm-engine.mjs';
import {createRuntime as createBTRuntime,tickBehaviorTree} from '../vendor/bt-engine.mjs';
import {chooseAction,validateActionContext} from '../vendor/utility-engine-v0.1.1.mjs';

import {GAO_SHUN_ALLOWED_INTENTS} from '../canonical/gao-shun.mjs';
import {GAO_SHUN_FSM} from '../policies/gao-shun-fsm.mjs';
import {GAO_SHUN_BT} from '../policies/gao-shun-bt.mjs';
import {GAO_SHUN_SCENARIOS} from '../scenarios/gao-shun.scenarios.mjs';

import {PEI_LUO_ALLOWED_INTENTS} from '../canonical/pei-luo.mjs';
import {PEI_LUO_FSM} from '../policies/pei-luo-fsm.mjs';
import {PEI_LUO_BT} from '../policies/pei-luo-bt.mjs';
import {PEI_LUO_SCENARIOS} from '../scenarios/pei-luo.scenarios.mjs';

import {JIANG_RUI_ALLOWED_INTENTS} from '../canonical/jiang-rui.mjs';
import {JIANG_RUI_FSM} from '../policies/jiang-rui-fsm.mjs';
import {JIANG_RUI_BT} from '../policies/jiang-rui-bt.mjs';
import {JIANG_RUI_UTILITY_PROFILE,UTILITY_ACTION_TO_INTENT} from '../profiles/jiang-rui-utility-profile.mjs';

export const TIERS=Object.freeze({
  smoke:10_000,
  standard:100_000,
  deep:500_000,
  million:1_000_000
});

export const JIANG_THRESHOLDS=Object.freeze({
  highRiskDanger:60,
  highRiskUrgency:70
});

function rng(seed){
  let x=seed>>>0;
  return ()=>{
    x^=x<<13; x^=x>>>17; x^=x<<5;
    return (x>>>0)/4294967296;
  };
}
function inc(obj,key,n=1){obj[key]=(obj[key]||0)+n}
function traceFSM(machine,events){
  let rt=createFSMRuntime(machine), intents=[], states=[];
  for(const ev of events){
    const r=stepFSM(machine,rt,ev);
    intents.push(...r.emitted); states.push(r.to); rt=r.nextRuntime;
  }
  return {intents,states};
}
function traceBT(tree,ticks){
  let rt=createBTRuntime(tree), intents=[], preemptions=0, running=[];
  for(const t of ticks){
    const r=tickBehaviorTree(tree,rt,t);
    intents.push(...r.emitted);
    if(r.preemptedAction)preemptions++;
    running.push(r.runningAction);
    rt=r.nextRuntime;
  }
  return {intents,preemptions,running};
}
function validIntents(intents,allowed){return intents.every(x=>allowed.has(x))}
function replayNpc(name,machine,tree,scenarioMap,allowedIntents,runs,random,digest){
  const names=Object.keys(scenarioMap), allowed=new Set(allowedIntents);
  const metrics={
    runs,invalidIntents:0,
    fsmIntentCounts:{},btIntentCounts:{},
    sequenceAgreement:0,sequenceDisagreement:0,
    btPreemptions:0,scenarioCounts:{}
  };
  const examples=[];
  for(let i=0;i<runs;i++){
    const scenarioName=names[Math.floor(random()*names.length)];
    const s=scenarioMap[scenarioName];
    const f=traceFSM(machine,s.fsm), b=traceBT(tree,s.bt);
    inc(metrics.scenarioCounts,scenarioName);
    for(const x of f.intents)inc(metrics.fsmIntentCounts,x);
    for(const x of b.intents)inc(metrics.btIntentCounts,x);
    metrics.btPreemptions+=b.preemptions;
    if(!validIntents(f.intents,allowed)||!validIntents(b.intents,allowed))metrics.invalidIntents++;
    const same=JSON.stringify(f.intents)===JSON.stringify(b.intents);
    same?metrics.sequenceAgreement++:metrics.sequenceDisagreement++;
    if(!same && examples.length<12) examples.push({scenario:scenarioName,fsm:f.intents,behaviorTree:b.intents});
    digest.update(JSON.stringify([name,scenarioName,f.intents,b.intents,b.preemptions]));
  }
  return {mode:'replay',metrics,examples};
}
function jiangSample(random){
  const danger=Math.floor(random()*101);
  const missionUrgency=Math.floor(random()*101);
  const anomalyPresent=random()<0.55;
  const superiorReachable=random()<0.70;
  const awayFromPost=random()<0.12;
  const highRisk=danger>=JIANG_THRESHOLDS.highRiskDanger || missionUrgency>=JIANG_THRESHOLDS.highRiskUrgency;
  const patrolDue=!awayFromPost;
  const btFacts={patrolDue,anomaly:anomalyPresent,highRisk,superiorReachable,awayFromPost};
  let fsmEvent;
  if(highRisk && superiorReachable) fsmEvent='HIGH_RISK';
  else if(anomalyPresent) fsmEvent='ANOMALY';
  else if(awayFromPost) fsmEvent='AWAY_FROM_POST';
  else fsmEvent='PATROL_DUE';
  const utility={
    playerPresent:false,playerRequestsHelp:false,playerRank:0,
    dutyImportance:awayFromPost?85:75,
    danger,missionUrgency,anomalyPresent,awayFromPost,superiorReachable,
    relevantKnowledge:'SOSPECHA',
    dutyMode:awayFromPost?'ninguno':'patrullar'
  };
  return {danger,missionUrgency,anomalyPresent,superiorReachable,awayFromPost,highRisk,btFacts,fsmEvent,utility};
}
function jiangRun(runs,random,digest){
  const allowed=new Set(JIANG_RUI_ALLOWED_INTENTS);
  const metrics={
    runs,invalidIntents:0,invalidContexts:0,
    allThreeAgreement:0,
    pairAgreement:{fsm_bt:0,fsm_utility:0,bt_utility:0},
    distributions:{fsm:{},behaviorTree:{},utility:{}},
    utilityActions:{},
    buckets:{
      lowRiskNoSuperior:{runs:0,utility:{}},
      highRiskNoSuperior:{runs:0,utility:{}},
      anyRiskWithSuperior:{runs:0,utility:{}},
      awayFromPost:{runs:0,utility:{}}
    }
  };
  const disagreements=[];
  for(let i=0;i<runs;i++){
    const s=jiangSample(random);
    if(validateActionContext(s.utility).length)metrics.invalidContexts++;

    const f=traceFSM(JIANG_RUI_FSM,[{type:s.fsmEvent,facts:{}}]).intents[0]||null;
    const b=traceBT(JIANG_RUI_BT,[{facts:s.btFacts,actionResults:{}}]).intents[0]||null;
    const ud=chooseAction(JIANG_RUI_UTILITY_PROFILE,s.utility);
    const u=UTILITY_ACTION_TO_INTENT[ud.action]??null;

    if(!f||!b||!u||!allowed.has(f)||!allowed.has(b)||!allowed.has(u))metrics.invalidIntents++;
    inc(metrics.distributions.fsm,f||'NULL');
    inc(metrics.distributions.behaviorTree,b||'NULL');
    inc(metrics.distributions.utility,u||'NULL');
    inc(metrics.utilityActions,ud.action);

    if(f===b)metrics.pairAgreement.fsm_bt++;
    if(f===u)metrics.pairAgreement.fsm_utility++;
    if(b===u)metrics.pairAgreement.bt_utility++;
    if(f===b && b===u)metrics.allThreeAgreement++;

    let bucket;
    if(s.awayFromPost) bucket=metrics.buckets.awayFromPost;
    else if(s.superiorReachable && (s.anomalyPresent||s.highRisk)) bucket=metrics.buckets.anyRiskWithSuperior;
    else if(s.highRisk) bucket=metrics.buckets.highRiskNoSuperior;
    else bucket=metrics.buckets.lowRiskNoSuperior;
    bucket.runs++; inc(bucket.utility,u||'NULL');

    if(!(f===b&&b===u) && disagreements.length<30){
      disagreements.push({
        danger:s.danger,missionUrgency:s.missionUrgency,
        anomaly:s.anomalyPresent,superiorReachable:s.superiorReachable,
        awayFromPost:s.awayFromPost,highRisk:s.highRisk,
        fsm:f,behaviorTree:b,utility:u,
        utilityAction:ud.action,utilityScore:ud.score,
        utilityTop3:ud.ranking.filter(x=>x.available).slice(0,3).map(x=>[x.name,x.score])
      });
    }
    digest.update(JSON.stringify(['jiang_rui',s.danger,s.missionUrgency,s.anomalyPresent,s.superiorReachable,s.awayFromPost,f,b,u,ud.action,ud.score]));
  }
  const denom=Math.max(1,runs);
  metrics.agreementPct={
    allThree:metrics.allThreeAgreement/denom*100,
    fsm_bt:metrics.pairAgreement.fsm_bt/denom*100,
    fsm_utility:metrics.pairAgreement.fsm_utility/denom*100,
    bt_utility:metrics.pairAgreement.bt_utility/denom*100
  };
  return {mode:'decision_surface',thresholds:JIANG_THRESHOLDS,metrics,examples:disagreements};
}

export function resolveRuns({tier='smoke',runs=null}={}){
  if(runs!==null){
    const n=Number(runs);
    if(!Number.isSafeInteger(n)||n<1)throw new TypeError('runs debe ser entero seguro >= 1');
    return n;
  }
  if(!Object.hasOwn(TIERS,tier))throw new RangeError(`tier desconocido: ${tier}`);
  return TIERS[tier];
}

export function runBenchmark({tier='smoke',runs=null,seed=1337,npc='all'}={}){
  const runsPerNpc=resolveRuns({tier,runs});
  const random=rng(Number(seed)>>>0);
  const digest=crypto.createHash('sha256');
  const result={
    benchmark:'NPC_BEHAVIOR_BENCHMARK_V01',
    tier,runsPerNpc,seed:Number(seed)>>>0,npc,
    policyNotice:'CANON y perfiles/políticas experimentales permanecen separados.',
    results:{}
  };
  if(npc==='all'||npc==='gao_shun'){
    result.results.gao_shun=replayNpc('gao_shun',GAO_SHUN_FSM,GAO_SHUN_BT,GAO_SHUN_SCENARIOS,GAO_SHUN_ALLOWED_INTENTS,runsPerNpc,random,digest);
  }
  if(npc==='all'||npc==='pei_luo'){
    result.results.pei_luo=replayNpc('pei_luo',PEI_LUO_FSM,PEI_LUO_BT,PEI_LUO_SCENARIOS,PEI_LUO_ALLOWED_INTENTS,runsPerNpc,random,digest);
  }
  if(npc==='all'||npc==='jiang_rui'){
    result.results.jiang_rui=jiangRun(runsPerNpc,random,digest);
  }
  if(Object.keys(result.results).length===0)throw new RangeError(`npc desconocido: ${npc}`);
  result.digest=digest.digest('hex');
  return result;
}
