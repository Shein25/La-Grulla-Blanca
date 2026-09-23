import { applyEffects, factsMatch } from './goap.mjs';

function byId(actions,id) {
  return actions.find(a=>a.id===id) || null;
}

export function executeNext(planResult,world,goal,actions) {
  if (!planResult || planResult.status !== 'PLAN_FOUND') {
    return { status:'NO_ACTIVE_PLAN', world:{...world}, remainingPlan:null, executed:null };
  }
  const plan=[...planResult.plan];
  if (factsMatch(world,goal)) {
    return { status:'GOAL_REACHED', world:{...world}, remainingPlan:plan, executed:null };
  }
  if (!plan.length) {
    return { status:'REPLAN_REQUIRED', reason:'Plan vacío pero objetivo no satisfecho.', world:{...world}, remainingPlan:[], executed:null };
  }

  const id=plan[0], action=byId(actions,id);
  if (!action) {
    return { status:'REPLAN_REQUIRED', reason:'Acción inexistente: '+id, world:{...world}, remainingPlan:plan, executed:null };
  }
  if (!factsMatch(world,action.preconditions)) {
    return { status:'REPLAN_REQUIRED', reason:'Precondiciones cambiaron para '+id, world:{...world}, remainingPlan:plan, executed:null };
  }

  const next=applyEffects(world,action.effects);
  const remaining=plan.slice(1);
  return {
    status:factsMatch(next,goal)?'GOAL_REACHED':'STEP_APPLIED',
    world:next,
    remainingPlan:remaining,
    executed:id,
  };
}

export function executeWholePlan(planResult,world,goal,actions,maxSteps=50) {
  let current={...world}, remaining=planResult;
  const trace=[];
  for (let i=0;i<maxSteps;i++) {
    const step=executeNext(remaining,current,goal,actions);
    trace.push(step);
    current=step.world;
    if (step.status==='GOAL_REACHED') return {status:'GOAL_REACHED',world:current,trace};
    if (step.status!=='STEP_APPLIED') return {status:step.status,world:current,trace};
    remaining={...remaining,plan:step.remainingPlan};
  }
  return {status:'STEP_LIMIT',world:current,trace};
}
