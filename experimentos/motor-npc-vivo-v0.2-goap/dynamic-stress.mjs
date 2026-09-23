import assert from 'node:assert/strict';
import { GOAP_ACTIONS } from './actions.mjs';
import { decideAndPlan } from './controller.mjs';
import { executeNext } from './executor.mjs';
import { factsMatch } from './goap.mjs';
import { cloneNpc } from '../motor-npc-vivo-v0.1.1/npc-fixtures.mjs';

const N=Math.max(1,Number(process.argv[2]||5000));
let seed=Number(process.argv[3]||1337)>>>0;
const rnd=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/2**32};
const chance=p=>rnd()<p;
const pick=a=>a[Math.floor(rnd()*a.length)];
const r100=()=>Math.floor(rnd()*101);
const npcIds=['disciplinado','leal','curioso'];

const metrics={
  goalReached:0,
  replanRequired:0,
  successfulReplans:0,
  goalChanged:0,
  planningDeferred:0,
  noPlannableGoal:0,
  repeatedStates:0,
  stepLimit:0,
  uselessMoveAfterObsoleteGoal:0,
};

function randomWorld(){
  const playerPresent=chance(.7);
  return {
    at:pick(['puesto','jugador','superior']),
    playerPresent,
    playerReachable:chance(.85),
    playerNeedsHelp:playerPresent&&chance(.5),
    playerHelped:false,
    anomalyPresent:chance(.45),
    anomalyInvestigated:false,
    hasEvidence:chance(.3),
    superiorAvailable:chance(.85),
    superiorInformed:false,
    passageOpen:chance(.8),
    messengerAvailable:chance(.75),
    dutyPending:chance(.55),
    dutySatisfied:false,
    waited:false,
    urgency:r100(),
    danger:r100(),
    dutyImportance:r100(),
  };
}

function event(world){
  const next={...world};
  const roll=Math.floor(rnd()*8);
  if(roll===0) next.passageOpen=false;
  else if(roll===1) next.superiorAvailable=false;
  else if(roll===2) next.messengerAvailable=false;
  else if(roll===3) { next.playerNeedsHelp=false; next.playerHelped=false; }
  else if(roll===4) next.playerReachable=false;
  else if(roll===5) next.dutyPending=false;
  else if(roll===6) next.anomalyPresent=false;
  else next.at=pick(['puesto','jugador','superior']);
  return next;
}

function signature(world,goalId,plan){
  const keys=Object.keys(world).sort();
  return JSON.stringify([keys.map(k=>[k,world[k]]),goalId,plan]);
}

for(let episode=0;episode<N;episode++){
  const npc=cloneNpc(pick(npcIds));
  let world=randomWorld();
  let decision=decideAndPlan(npc,world,GOAP_ACTIONS,{maxExpansions:200,maxFrontier:500});
  let priorGoal=decision.selectedGoal?.id ?? null;
  const seen=new Set();
  let finished=false;

  for(let attempt=0;attempt<12;attempt++){
    if(decision.status==='PLANNING_DEFERRED'){
      metrics.planningDeferred++; finished=true; break;
    }
    if(decision.status==='NO_PLANNABLE_GOAL'){
      metrics.noPlannableGoal++; finished=true; break;
    }
    assert.equal(decision.status,'PLAN_READY');

    const sig=signature(world,decision.selectedGoal.id,decision.plan.plan);
    if(seen.has(sig)){ metrics.repeatedStates++; finished=true; break; }
    seen.add(sig);

    if(chance(.28)) world=event(world);

    const obsoleteBefore=Object.keys(decision.selectedGoal.relevance).length>0 &&
      !factsMatch(world,decision.selectedGoal.relevance);
    const step=executeNext(
      decision.plan,
      world,
      decision.selectedGoal.goal,
      GOAP_ACTIONS,
      decision.selectedGoal.relevance
    );
    world=step.world;

    if(step.status==='GOAL_REACHED'){
      metrics.goalReached++; finished=true; break;
    }

    if(step.status==='STEP_APPLIED'){
      if(step.executed?.startsWith('ir_') && obsoleteBefore) metrics.uselessMoveAfterObsoleteGoal++;
      decision={...decision,plan:{...decision.plan,plan:step.remainingPlan}};
      continue;
    }

    assert.equal(step.status,'REPLAN_REQUIRED');
    metrics.replanRequired++;

    const replanned=decideAndPlan(npc,world,GOAP_ACTIONS,{maxExpansions:200,maxFrontier:500});
    if(replanned.status==='PLAN_READY'){
      metrics.successfulReplans++;
      if(priorGoal && replanned.selectedGoal.id!==priorGoal) metrics.goalChanged++;
      priorGoal=replanned.selectedGoal.id;
    }
    decision=replanned;
  }

  if(!finished) metrics.stepLimit++;
}

assert.equal(metrics.uselessMoveAfterObsoleteGoal,0);
console.log('Dynamic stress GOAP PASS: '+N+' episodios · seed final '+seed);
console.log(metrics);
