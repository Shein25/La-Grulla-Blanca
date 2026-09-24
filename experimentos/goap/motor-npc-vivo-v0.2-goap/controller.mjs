import { rankGoals } from './goal-selector.mjs';
import { planGOAP } from './goap.mjs';

const INCONCLUSIVE = new Set(['SEARCH_LIMIT','FRONTIER_LIMIT','COST_OVERFLOW']);

export function decideAndPlan(npc,world,actions,options={}) {
  const ranking=rankGoals(npc,world);
  const attempts=[];

  for (const candidate of ranking) {
    if (!candidate.available) continue;

    const plan=planGOAP(world,candidate.goal,actions,options);
    attempts.push({
      goalId:candidate.id,
      utility:candidate.score,
      status:plan.status,
      cost:plan.cost,
      expansions:plan.expansions,
      maxFrontier:plan.maxFrontier,
    });

    if (plan.status==='PLAN_FOUND') {
      const executablePlan={
        ...plan,
        goal:{...candidate.goal},
        relevance:{...candidate.relevance},
        goalId:candidate.id,
      };
      return {
        status:'PLAN_READY',
        selectedGoal:candidate,
        goalRanking:ranking,
        plan:executablePlan,
        attempts,
      };
    }

    if (INCONCLUSIVE.has(plan.status)) {
      return {
        status:'PLANNING_DEFERRED',
        reason:plan.status,
        selectedGoal:candidate,
        goalRanking:ranking,
        plan,
        attempts,
      };
    }

    if (plan.status!=='NO_PLAN') {
      throw new Error('Estado de planner no manejado: '+plan.status);
    }
  }

  return {
    status:'NO_PLANNABLE_GOAL',
    selectedGoal:null,
    goalRanking:ranking,
    plan:null,
    attempts,
  };
}
