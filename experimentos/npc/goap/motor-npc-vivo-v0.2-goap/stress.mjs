import assert from 'node:assert/strict';
import { GOAP_ACTIONS } from './actions.mjs';
import { decideAndPlan } from './controller.mjs';
import { executeWholePlan } from './executor.mjs';
import { cloneNpc } from '../../utility-ai/motor-npc-vivo-v0.1.1/npc-fixtures.mjs';

const N=Math.max(1,Number(process.argv[2]||10000));
let seed=Number(process.argv[3]||1337)>>>0;
const rnd=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/2**32};
const chance=p=>rnd()<p;
const r100=()=>Math.floor(rnd()*101);
const npcs=['disciplinado','leal','curioso'];
const counts=new Map();
let replans=0, noPlan=0;

for(let i=0;i<N;i++){
  const at=['puesto','jugador','superior'][Math.floor(rnd()*3)];
  const playerPresent=chance(.65);
  const playerNeedsHelp=playerPresent&&chance(.5);
  const anomalyPresent=chance(.45);
  const hasEvidence=chance(.3);
  const dutyPending=chance(.55);

  const world={
    at,
    playerPresent,
    playerReachable:chance(.85),
    playerNeedsHelp,
    playerHelped:false,
    anomalyPresent,
    anomalyInvestigated:false,
    hasEvidence,
    superiorAvailable:chance(.8),
    superiorInformed:false,
    passageOpen:chance(.8),
    messengerAvailable:chance(.7),
    dutyPending,
    dutySatisfied:false,
    waited:false,
    urgency:r100(),
    danger:r100(),
    dutyImportance:r100(),
  };

  const npc=cloneNpc(npcs[Math.floor(rnd()*npcs.length)]);
  const c=decideAndPlan(npc,world,GOAP_ACTIONS,{maxExpansions:500});
  if(c.status==='NO_PLANNABLE_GOAL'){
    noPlan++;
    continue;
  }

  assert.equal(c.status,'PLAN_READY');
  assert.ok(Number.isFinite(c.selectedGoal.score));
  assert.ok(Number.isFinite(c.plan.cost));
  assert.ok(Array.isArray(c.plan.plan));

  const run=executeWholePlan(c.plan,world,c.selectedGoal.goal,GOAP_ACTIONS,30,c.selectedGoal.relevance);
  if(run.status==='REPLAN_REQUIRED') replans++;
  else assert.equal(run.status,'GOAL_REACHED');

  counts.set(c.selectedGoal.id,(counts.get(c.selectedGoal.id)||0)+1);
}

console.log('Stress GOAP PASS: '+N+' casos · seed final '+seed);
console.log({goals:Object.fromEntries([...counts.entries()].sort((a,b)=>b[1]-a[1])),replans,noPlan});
