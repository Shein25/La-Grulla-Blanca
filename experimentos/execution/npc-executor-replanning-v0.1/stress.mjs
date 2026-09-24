import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createExecutionSession, advanceExecutionSession } from './execution-session.mjs';
import { makeWorld, makeActions, makeInitialConfig } from './fixtures.mjs';

const seed = Number(process.argv[2] ?? 1337);
if (!Number.isSafeInteger(seed) || seed < 0) throw new TypeError('seed inválida');
let randomState = seed >>> 0;
function random() { randomState = (Math.imul(randomState, 1664525) + 1013904223) >>> 0; return randomState; }
const episodes = 10_000;
const digest = createHash('sha256');
const match = (state, conditions) => Object.entries(conditions).every(([key, value]) => Object.hasOwn(state, key) && Object.is(state[key], value));
const stateKey = state => JSON.stringify(Object.entries(state).sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0));

// Oracle separado para el catálogo pequeño: explora estados simbólicos sin importar GOAP.
function routeExists(initial, goal, catalog) {
  const queue = [initial];
  const visited = new Set([stateKey(initial)]);
  for (let head = 0; head < queue.length; head++) {
    const state = queue[head];
    if (match(state, goal)) return true;
    for (const action of catalog) {
      if (!match(state, action.preconditions)) continue;
      const next = { ...state, ...action.effects };
      const key = stateKey(next);
      if (!visited.has(key)) { visited.add(key); queue.push(next); }
    }
    assert.ok(queue.length < 100, 'oracle BFS debe permanecer pequeño');
  }
  return false;
}

function verifyPlan(initial, goal, catalog, plan) {
  let current = { ...initial };
  for (const id of plan) {
    const action = catalog.find(a => a.id === id);
    assert.ok(action, `acción ${id} existe`);
    assert.ok(match(current, action.preconditions), `preconditions de ${id}`);
    current = { ...current, ...action.effects };
  }
  assert.ok(match(current, goal), 'plan nuevo alcanza el mismo goal');
}

let advances = 0, stepsApplied = 0, goalsReached = 0, goalsReachedExternally = 0;
let replanRequests = 0, replansReady = 0, noPlanForGoal = 0, planningDeferred = 0;
let intentReevaluations = 0, externalWorldChanges = 0, maxStepsPerEpisode = 0;
let maxReplansPerEpisode = 0, staleActionsPrevented = 0, actionsExecutedDuringReplan = 0;
let obsoleteGoalActionsExecuted = 0;

for (let episode = 0; episode < episodes; episode++) {
  const kind = random() % 15;
  const config = makeInitialConfig(kind === 5 || kind === 9 || kind === 11 ? { plan: [] } :
    kind === 10 ? { plan: ['desconocida'] } : {});
  let session = createExecutionSession(config);
  let world = makeWorld({ unrelated: random() % 1000 });
  let catalog = makeActions();
  let steps = 0, replans = 0, terminal = false;

  function perturb(changes) {
    const next = { ...world, ...changes };
    if (JSON.stringify(next) !== JSON.stringify(world)) externalWorldChanges++;
    world = next;
  }

  for (let tick = 0; tick < 50; tick++) {
    if (tick === 0 && [4, 7, 8, 11].includes(kind)) perturb({ routeAOpen: false, routeBOpen: false });
    if (tick === 0 && kind === 12) perturb({ playerNeedsHelp: false });
    if (tick === 0 && kind === 13) perturb({ playerHelped: true });
    if (tick === 1 && [1, 14].includes(kind)) perturb({ routeAOpen: false, routeBOpen: kind === 1 });
    if (tick === 1 && [2, 7].includes(kind)) perturb({ playerNeedsHelp: false });
    if (tick === 1 && [3, 8].includes(kind)) perturb({ playerHelped: true });
    if (tick === 1 && kind === 6) catalog = catalog.filter(a => a.id !== 'usar_a');
    if (tick === 1 && kind === 4) perturb({ routeBOpen: true });
    if (tick === 2 && [11, 14].includes(kind)) perturb({ routeBOpen: true });
    const options = tick === 0 && kind === 5 ? { maxExpansions: 0 } :
      tick === 0 && kind === 9 ? { maxFrontier: 1 } : {};
    const previousSession = session;
    const beforeWorld = { ...world };
    const beforeSession = structuredClone(session);
    const beforeCatalog = structuredClone(catalog);
    const beforeOptions = structuredClone(options);
    const obsolete = !match(beforeWorld, previousSession.goal) && !match(beforeWorld, previousSession.relevance);
    const nextAction = previousSession.mode === 'ACTIVE' && previousSession.plan.length ?
      catalog.find(a => a.id === previousSession.plan[0]) : null;
    const stale = previousSession.mode === 'ACTIVE' && previousSession.plan.length > 0 &&
      !match(beforeWorld, previousSession.goal) && match(beforeWorld, previousSession.relevance) &&
      (!nextAction || !match(beforeWorld, nextAction.preconditions));
    const result = advanceExecutionSession(session, world, catalog, options);
    advances++;
    assert.deepEqual(session, beforeSession, 'session input intacta');
    assert.deepEqual(world, beforeWorld, 'world input intacto');
    assert.deepEqual(catalog, beforeCatalog, 'actions trusted no mutadas');
    assert.deepEqual(options, beforeOptions, 'plannerOptions intactos');
    assert.deepEqual(advanceExecutionSession(session, world, catalog, options), result, 'determinismo');
    if (result.executed !== null) { steps++; stepsApplied++; }
    if (result.replan?.attempted === true) replans++;
    assert.equal(result.counters.stepCount, steps, 'stepCount = acciones reales');
    assert.equal(result.counters.replanCount, replans, 'replanCount = intentos reales');
    if (result.session) {
      assert.equal(result.session.stepCount, steps);
      assert.equal(result.session.replanCount, replans);
    }
    if (result.replan?.attempted === true && result.executed !== null) actionsExecutedDuringReplan++;
    if (obsolete && result.executed !== null) obsoleteGoalActionsExecuted++;
    assert.equal(actionsExecutedDuringReplan, 0);
    assert.equal(obsoleteGoalActionsExecuted, 0);
    if (stale) {
      assert.equal(result.replan?.attempted, true, 'acción stale provoca replanning');
      assert.equal(result.executed, null);
      staleActionsPrevented++;
    }
    if (previousSession.mode === 'REPLAN_PENDING') {
      assert.equal(result.executed, null, 'pending nunca ejecuta');
    }
    if (obsolete) {
      assert.equal(result.status, 'INTENT_REEVALUATION_REQUIRED');
      assert.equal(result.replan, null);
    }
    if (result.replan?.attempted === true) {
      assert.deepEqual(result.world, beforeWorld, 'replan no cambia mundo');
      assert.deepEqual(result.session.goal, previousSession.goal, 'mismo goal');
      assert.equal(result.session.goalId, previousSession.goalId);
      if (previousSession.mode === 'ACTIVE') replanRequests++;
    }
    switch (result.status) {
      case 'STEP_APPLIED':
        assert.ok(result.executed !== null);
        assert.equal(result.session.mode, 'ACTIVE');
        break;
      case 'GOAL_REACHED':
        goalsReached++;
        if (result.executed === null) goalsReachedExternally++;
        assert.equal(result.session, null);
        assert.equal(result.replan, null);
        terminal = true;
        break;
      case 'REPLAN_READY':
        replansReady++;
        assert.equal(result.executed, null);
        assert.equal(result.session.mode, 'ACTIVE');
        assert.ok(routeExists(beforeWorld, previousSession.goal, catalog));
        verifyPlan(beforeWorld, previousSession.goal, catalog, result.session.plan);
        break;
      case 'NO_PLAN_FOR_GOAL':
        noPlanForGoal++;
        assert.equal(result.session.mode, 'REPLAN_PENDING');
        assert.equal(result.session.plan, null, 'plan stale descartado');
        assert.equal(routeExists(beforeWorld, previousSession.goal, catalog), false);
        break;
      case 'PLANNING_DEFERRED':
        planningDeferred++;
        assert.equal(result.session.mode, 'REPLAN_PENDING');
        assert.equal(result.session.plan, null, 'plan stale descartado');
        assert.ok(['SEARCH_LIMIT', 'FRONTIER_LIMIT', 'COST_OVERFLOW'].includes(result.replan.plannerStatus));
        break;
      case 'INTENT_REEVALUATION_REQUIRED':
        intentReevaluations++;
        assert.equal(result.session, null);
        assert.equal(result.executed, null);
        assert.equal(result.replan, null);
        terminal = true;
        break;
      default: assert.fail(`estado público inesperado: ${result.status}`);
    }
    if (episode % 1000 === 0 && tick === 0) {
      const another = advanceExecutionSession(session, world, catalog, options);
      another.world.at = 'mutated';
      if (another.session) another.session.goal.playerHelped = false;
      assert.deepEqual(result, advanceExecutionSession(session, world, catalog, options), 'outputs desacoplados');
    }
    digest.update(JSON.stringify({ episode, tick, kind, result }));
    digest.update('\n');
    world = result.world;
    session = result.session;
    if (terminal) break;
  }
  assert.ok(terminal, `episodio ${episode} debe terminar en <= 50 advances`);
  maxStepsPerEpisode = Math.max(maxStepsPerEpisode, steps);
  maxReplansPerEpisode = Math.max(maxReplansPerEpisode, replans);
}

console.log(JSON.stringify({ seed, episodes, advances, stepsApplied, goalsReached, goalsReachedExternally,
  replanRequests, replansReady, noPlanForGoal, planningDeferred, intentReevaluations,
  externalWorldChanges, maxStepsPerEpisode, maxReplansPerEpisode, staleActionsPrevented,
  actionsExecutedDuringReplan, obsoleteGoalActionsExecuted, digest: digest.digest('hex') }));
