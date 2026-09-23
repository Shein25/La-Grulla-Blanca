import { applyEffects, factsMatch } from './goap.mjs';

function byId(actions,id) {
  return actions.find(a=>a.id===id) || null;
}

function relevanceStillHolds(world,relevance) {
  return !relevance || !Object.keys(relevance).length || factsMatch(world,relevance);
}

export function executeNext(planResult,world,goal,actions,relevance={}) {
  if (!planResult || planResult.status !== 'PLAN_FOUND') {
    return { status:'NO_ACTIVE_PLAN', world:{...world}, remainingPlan:null, executed:null };
  }

  const plan=[...planResult.plan];

  if (factsMatch(world,goal)) {
    return { status:'GOAL_REACHED', world:{...world}, remainingPlan:plan, executed:null };
  }

  if (!relevanceStillHolds(world,relevance)) {
    return {
      status:'REPLAN_REQUIRED',
      reason:'El objetivo dejó de ser relevante.',
      goalObsolete:true,
      world:{...world},
      remainingPlan:plan,
      executed:null,
    };
  }

  if (!plan.length) {
    return {
      status:'REPLAN_REQUIRED',
      reason:'Plan vacío pero objetivo no satisfecho.',
      goalObsolete:false,
      world:{...world},
      remainingPlan:[],
      executed:null,
    };
  }

  const id=plan[0], action=byId(actions,id);
  if (!action) {
    return {
      status:'REPLAN_REQUIRED',
      reason:'Acción inexistente: '+id,
      goalObsolete:false,
      world:{...world},
      remainingPlan:plan,
      executed:null,
    };
  }

  if (!factsMatch(world,action.preconditions)) {
    return {
      status:'REPLAN_REQUIRED',
      reason:'Precondiciones cambiaron para '+id,
      goalObsolete:false,
      world:{...world},
      remainingPlan:plan,
      executed:null,
    };
  }

  const next=applyEffects(world,action.effects);
  const remaining=plan.slice(1);

  return {
    status:factsMatch(next,goal)?'GOAL_REACHED':'STEP_APPLIED',
    goalObsolete:false,
    world:next,
    remainingPlan:remaining,
    executed:id,
  };
}

export function executeWholePlan(planResult,world,goal,actions,maxSteps=50,relevance={}) {
  if (!Number.isInteger(maxSteps) || maxSteps < 0) throw new TypeError('maxSteps debe ser entero >= 0');

  let current={...world}, remaining=planResult;
  const trace=[];

  for (let i=0;i<maxSteps;i++) {
    const step=executeNext(remaining,current,goal,actions,relevance);
    trace.push(step);
    current=step.world;

    if (step.status==='GOAL_REACHED') return {status:'GOAL_REACHED',world:current,trace};
    if (step.status!=='STEP_APPLIED') return {status:step.status,world:current,trace};

    remaining={...remaining,plan:step.remainingPlan};
  }

  if (factsMatch(current,goal)) return {status:'GOAL_REACHED',world:current,trace};
  return {status:'STEP_LIMIT',world:current,trace};
}
