import { rankGoals } from './goal-selector.mjs';
import { planGOAP } from './goap.mjs';

export function decideAndPlan(npc,world,actions,options={}) {
  const ranking=rankGoals(npc,world);
  const attempts=[];

  for (const candidate of ranking) {
    if (!candidate.available) continue;
    const plan=planGOAP(world,candidate.goal,actions,options);
    attempts.push({goalId:candidate.id,utility:candidate.score,status:plan.status,cost:plan.cost});
    if (plan.status==='PLAN_FOUND') {
      return {
        status:'PLAN_READY',
        selectedGoal:candidate,
        goalRanking:ranking,
        plan,
        attempts,
      };
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
