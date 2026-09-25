import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { tickAutonomousLoop } from './autonomous-loop.mjs';
import { initialFixture, memoryEventFixture, observationFixture, stateFixture } from './fixtures.mjs';
import { GOAP_ACTIONS } from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import { factsMatch } from '../../goap/motor-npc-vivo-v0.2-goap/goap.mjs';

const SEEDS = [1337, 1, 42, 999, 20260924];
const GLOBAL_TURNS = 3000;
const NPC_COUNT = 16;

function generator(seed) {
  let state = seed >>> 0;
  return () => {
    state ^= state << 13; state ^= state >>> 17; state ^= state << 5;
    return state >>> 0;
  };
}

function equalFacts(a, b) {
  const ak = Object.keys(a).sort(), bk = Object.keys(b).sort();
  return ak.length === bk.length && ak.every((key, index) => key === bk[index] && Object.is(a[key], b[key]));
}

function initialState() {
  const items = [], configs = [];
  for (let index = 0; index < NPC_COUNT; index++) {
    const id = `npc_${String(index).padStart(2, '0')}`;
    if (index === NPC_COUNT - 1) {
      items.push(initialFixture(id, { playerPresent: false, playerNeedsHelp: false,
        waited: true, dutyImportance: 0, urgency: 0, danger: 0 },
      { traits: { disciplina: 0, sociabilidad: 0, curiosidad: 0, prudencia: 0,
        lealtad_institucional: 0, empatia: 0 } }, { superiorReachable: false }));
      configs.push({ id, interval: 43, minGap: 0, firstPeriodicTurn: 43 });
      continue;
    }
    const lane = index % 4;
    const traits = lane === 0
      ? { empatia: 100, sociabilidad: 0, curiosidad: 0, disciplina: 0,
        prudencia: 0, lealtad_institucional: 0 }
      : lane === 1
        ? { empatia: 0, sociabilidad: 0, curiosidad: 100, disciplina: 0,
          prudencia: 0, lealtad_institucional: 0 }
        : lane === 2
          ? { empatia: 0, sociabilidad: 0, curiosidad: 0, disciplina: 100,
            prudencia: 0, lealtad_institucional: 90 }
          : { empatia: 0, sociabilidad: 0, curiosidad: 0, disciplina: 0,
            prudencia: 80, lealtad_institucional: 100 };
    items.push(initialFixture(id, rearmFacts(index), { traits },
      { superiorReachable: lane === 3, relevantKnowledge: lane === 3 ? 'CONFIRMADO' : 'DESCONOCIDO',
        dutyMode: lane === 2 ? 'trabajar' : 'ninguno' }));
    const interval = index < 4 ? 1 : 1 + index % 7;
    configs.push({ id, interval, minGap: 0, firstPeriodicTurn: interval });
  }
  return stateFixture(items, configs);
}

function rearmFacts(index) {
  const common = { at: 'puesto', playerPresent: false, playerNeedsHelp: false,
    playerHelped: false, playerReachable: true, anomalyPresent: false,
    anomalyInvestigated: false, dutyPending: false, dutySatisfied: false,
    hasEvidence: false, superiorInformed: false, superiorAvailable: true,
    messengerAvailable: true, passageOpen: true, waited: false,
    dutyImportance: 10, danger: 0, urgency: 40 };
  if (index % 4 === 0) return { ...common, playerPresent: true,
    playerNeedsHelp: true, urgency: 80 };
  if (index % 4 === 1) return { ...common, anomalyPresent: true, urgency: 50 };
  if (index % 4 === 2) return { ...common, dutyPending: true,
    dutyImportance: 90, urgency: 20 };
  return { ...common, hasEvidence: true, danger: 60, urgency: 70 };
}

function staleCandidate(runtime) {
  const session = runtime.executionSession;
  if (session?.mode !== 'ACTIVE' || !session.plan.length ||
      factsMatch(runtime.world, session.goal) || !factsMatch(runtime.world, session.relevance)) return null;
  const action = GOAP_ACTIONS.find(item => item.id === session.plan[0]);
  const requiredAt = action?.preconditions.at;
  if (!requiredAt || !factsMatch(runtime.world, action.preconditions)) return null;
  const at = requiredAt === 'puesto' ? 'jugador' : 'puesto';
  const changed = { ...runtime.world, at, playerReachable: true,
    passageOpen: true, superiorAvailable: true };
  if (factsMatch(changed, session.goal) || !factsMatch(changed, session.relevance) ||
      factsMatch(changed, action.preconditions)) return null;
  return { at, playerReachable: true, passageOpen: true, superiorAvailable: true };
}

function obsoleteCandidate(runtime) {
  const session = runtime.executionSession;
  if (session?.mode !== 'ACTIVE' || factsMatch(runtime.world, session.goal)) return null;
  const field = { HELP_PLAYER: 'playerNeedsHelp', INVESTIGATE_ANOMALY: 'anomalyPresent',
    REPORT_SUPERIOR: 'hasEvidence', FULFILL_DUTY: 'dutyPending' }[session.goalId];
  return field && runtime.world[field] === true ? { [field]: false } : null;
}

function nextInput(state, turn, random) {
  const pending = new Map(), schedulerEvents = [];
  const add = (index, update, memoryEvents = []) => {
    const runtime = state.npcs[index];
    const previous = pending.get(runtime.id);
    const world = { ...(previous?.world ?? runtime.world), ...update };
    pending.set(runtime.id, observationFixture(runtime, world, {},
      [...(previous?.memoryEvents ?? []), ...memoryEvents]));
  };
  const request = turn % 31 === 7 ? 'DEFERRED' : turn % 7 === 3 ? 'STALE'
    : turn % 11 === 4 ? 'OBSOLETE' : turn % 17 === 5 ? 'EXTERNAL' : null;
  let scenario = null;
  if (request) {
    const offset = random() % (NPC_COUNT - 1);
    for (let step = 0; step < NPC_COUNT - 1; step++) {
      const index = (offset + step) % (NPC_COUNT - 1);
      const runtime = state.npcs[index];
      const update = request === 'STALE' || request === 'DEFERRED'
        ? staleCandidate(runtime)
        : request === 'OBSOLETE' ? obsoleteCandidate(runtime)
          : runtime.executionSession?.mode === 'ACTIVE' &&
            !factsMatch(runtime.world, runtime.executionSession.goal)
            ? { ...runtime.executionSession.goal } : null;
      if (update === null) continue;
      add(index, update);
      if (request === 'STALE' || request === 'DEFERRED') {
        schedulerEvents.push({ npcId: runtime.id, kind: 'PLAN_INVALIDATED' });
      }
      scenario = { kind: request, npcId: runtime.id,
        staleAction: request === 'STALE' || request === 'DEFERRED'
          ? runtime.executionSession.plan[0] : null };
      break;
    }
  }
  // Rearmar un solo trabajo por turno distribuye el esfuerzo entre los cuatro goals.
  const first = (turn + random() % 5) % (NPC_COUNT - 1);
  for (let step = 0; step < NPC_COUNT - 1; step++) {
    const index = (first + step) % (NPC_COUNT - 1);
    if (state.npcs[index].executionSession === null &&
        state.npcs[index].id !== scenario?.npcId) {
      add(index, rearmFacts(index));
      break;
    }
  }
  if (turn % 11 === 0) {
    const index = random() % (NPC_COUNT - 1);
    if (state.npcs[index].id !== scenario?.npcId) {
      const world = pending.get(state.npcs[index].id)?.world ?? state.npcs[index].world;
      add(index, { danger: (world.danger + 17) % 101 });
    }
  }
  if (turn % 37 === 0) {
    const index = random() % (NPC_COUNT - 1);
    if (state.npcs[index].id !== scenario?.npcId) {
      const world = pending.get(state.npcs[index].id)?.world ?? state.npcs[index].world;
      add(index, { playerPresent: !world.playerPresent,
        playerNeedsHelp: !world.playerPresent, playerHelped: false });
    }
  }
  if (turn % 17 === 0) {
    const index = random() % (NPC_COUNT - 1);
    if (state.npcs[index].id !== scenario?.npcId) {
      const world = pending.get(state.npcs[index].id)?.world ?? state.npcs[index].world;
      add(index, { anomalyPresent: !world.anomalyPresent, anomalyInvestigated: false });
    }
  }
  if (turn % 29 === 0) {
    const index = random() % (NPC_COUNT - 1);
    const kind = turn % 58 === 0 ? 'PLAYER_LIED' : 'PLAYER_HELPED_ME';
    const event = memoryEventFixture(turn, kind, `memory-${turn}-${index}`);
    add(index, {}, [event]);
  }
  const observations = [...pending.values()].sort((a, b) =>
    a.npcId < b.npcId ? -1 : a.npcId > b.npcId ? 1 : 0);
  return { input: { observations, schedulerEvents }, scenario };
}

function metrics(seed) {
  return { seed, globalTurns: GLOBAL_TURNS, npcCount: NPC_COUNT,
    schedulerDispatches: 0, schedulerDeferred: 0, schedulerBudgetExhaustedTicks: 0,
    decisionCalls: 0, executionCalls: 0, planSessionsCreated: 0,
    decisionGoalsAlreadySatisfied: 0, emptyPlanSessionsCreated: 0,
    stepsApplied: 0, goalsReached: 0, goalsReachedExternally: 0,
    replansReady: 0, stalePlansForced: 0, stalePlansPrevented: 0,
    replanFollowupActions: 0, executionPlanningDeferred: 0,
    pendingReplanRecoveries: 0, executionNoPlan: 0, intentReevaluations: 0,
    decisionNoPlan: 0, decisionPlanningDeferred: 0, unmappedUtilityActions: 0,
    memoryEventsApplied: 0, memoryChangedEventsGenerated: 0,
    worldChangedEventsGenerated: 0, maxActiveSessions: 0,
    brainCallsWithoutDispatch: 0, utilityCallsWhileSessionActive: 0,
    actionsExecutedDuringPlanCreation: 0, maxActionsPerDispatch: 0,
    relationBaseMutations: 0, digest: null };
}

export function runStress(seed, turns = GLOBAL_TURNS) {
  assert.equal(turns, GLOBAL_TURNS);
  const random = generator(seed);
  const report = metrics(seed);
  const hash = createHash('sha256');
  const awaitingReplanAction = new Map();
  let state = initialState();
  for (let turn = 1; turn <= turns; turn++) {
    const before = state;
    const { input, scenario } = nextInput(before, turn, random);
    const options = { scheduler: { maxDispatches: scenario ? NPC_COUNT : turn % 13 === 0 ? 2 : 8 },
      planner: scenario?.kind === 'DEFERRED' || (!scenario && turn % 97 === 0)
        ? { maxExpansions: 0 } : {} };
    const result = tickAutonomousLoop(before, turn, input, options);
    const next = result.state;
    assert.equal(next.clock, turn);
    assert.equal(next.scheduler.clock, turn);
    assert.equal(result.dispatchResults.length, result.scheduler.dispatches.length);
    assert.deepEqual(result.dispatchResults.map(item => item.npcId),
      result.scheduler.dispatches.map(item => item.npcId));
    const dispatchById = new Map(result.dispatchResults.map(item => [item.npcId, item]));
    const observations = new Map(input.observations.map(item => [item.npcId, item]));
    const expectedWorldChanged = [], expectedMemoryChanged = [];
    for (const oldRuntime of before.npcs) {
      const newRuntime = next.npcs.find(item => item.id === oldRuntime.id);
      const observation = observations.get(oldRuntime.id);
      const trace = dispatchById.get(oldRuntime.id);
      if (awaitingReplanAction.has(oldRuntime.id)) {
        if (observation && !equalFacts(observation.world, oldRuntime.world)) {
          awaitingReplanAction.delete(oldRuntime.id);
        } else if (trace) {
          assert.equal(trace.path, 'EXECUTION');
          const expected = awaitingReplanAction.get(oldRuntime.id);
          assert.equal(trace.executed, expected.action);
          assert.ok(turn > expected.turn);
          report.replanFollowupActions++;
          awaitingReplanAction.delete(oldRuntime.id);
        }
      }
      assert.deepEqual(newRuntime.npc.relationPlayer, oldRuntime.npc.relationPlayer);
      if (JSON.stringify(newRuntime.npc.relationPlayer) !== JSON.stringify(oldRuntime.npc.relationPlayer)) report.relationBaseMutations++;
      if (observation) {
        if (!equalFacts(oldRuntime.world, observation.world) ||
            !equalFacts(oldRuntime.utilityContext, observation.utilityContext)) expectedWorldChanged.push(oldRuntime.id);
        if (observation.memoryEvents.length) expectedMemoryChanged.push(oldRuntime.id);
        report.memoryEventsApplied += observation.memoryEvents.length;
      }
      if (!trace) {
        assert.deepEqual(newRuntime.npc.behaviorState, oldRuntime.npc.behaviorState);
        assert.deepEqual(newRuntime.executionSession, oldRuntime.executionSession);
      } else {
        assert.equal(trace.path, oldRuntime.executionSession === null ? 'DECISION' : 'EXECUTION');
        if (trace.path === 'DECISION') {
          report.decisionCalls++;
          if (oldRuntime.executionSession !== null) report.utilityCallsWhileSessionActive++;
          if (trace.executed !== null) report.actionsExecutedDuringPlanCreation++;
        } else {
          report.executionCalls++;
          assert.deepEqual(newRuntime.npc.behaviorState, oldRuntime.npc.behaviorState);
        }
        const actions = trace.executed === null ? 0 : 1;
        report.maxActionsPerDispatch = Math.max(report.maxActionsPerDispatch, actions);
        if (!result.scheduler.dispatches.some(item => item.npcId === oldRuntime.id)) report.brainCallsWithoutDispatch++;
      }
    }
    assert.deepEqual(result.generatedEvents.worldChanged, expectedWorldChanged);
    assert.deepEqual(result.generatedEvents.memoryChanged, expectedMemoryChanged);
    report.worldChangedEventsGenerated += result.generatedEvents.worldChanged.length;
    report.memoryChangedEventsGenerated += result.generatedEvents.memoryChanged.length;
    report.schedulerDispatches += result.scheduler.dispatches.length;
    report.schedulerDeferred += result.scheduler.deferredCount;
    if (result.status === 'SCHEDULER_BUDGET_EXHAUSTED') report.schedulerBudgetExhaustedTicks++;
    if (scenario) {
      const trace = dispatchById.get(scenario.npcId);
      assert.ok(trace, `scenario ${scenario.kind} sin dispatch en turno ${turn}`);
      assert.equal(trace.path, 'EXECUTION');
      if (scenario.kind === 'STALE' || scenario.kind === 'DEFERRED') {
        report.stalePlansForced++;
        assert.equal(trace.executed, null);
        assert.notEqual(trace.status, 'GOAL_REACHED');
        assert.ok(['REPLAN_READY', 'PLANNING_DEFERRED', 'NO_PLAN_FOR_GOAL'].includes(trace.status));
        report.stalePlansPrevented++;
        if (scenario.kind === 'DEFERRED') {
          assert.equal(trace.status, 'PLANNING_DEFERRED');
          assert.equal(next.npcs.find(item => item.id === scenario.npcId).executionSession.mode,
            'REPLAN_PENDING');
        }
      } else if (scenario.kind === 'OBSOLETE') {
        assert.equal(trace.status, 'INTENT_REEVALUATION_REQUIRED');
        assert.equal(trace.executed, null);
      } else {
        assert.equal(trace.status, 'GOAL_REACHED');
        assert.equal(trace.executed, null);
      }
    }
    for (const trace of result.dispatchResults) {
      const prior = before.npcs.find(item => item.id === trace.npcId);
      const current = next.npcs.find(item => item.id === trace.npcId);
      if (trace.status === 'PLAN_SESSION_CREATED') {
        report.planSessionsCreated++;
        if (!current.executionSession?.plan.length) report.emptyPlanSessionsCreated++;
        assert.ok(current.executionSession?.plan.length >= 1);
      }
      if (trace.status === 'DECISION_GOAL_ALREADY_SATISFIED') {
        report.decisionGoalsAlreadySatisfied++;
        assert.equal(current.executionSession, null);
      }
      if (trace.status === 'STEP_APPLIED') report.stepsApplied++;
      if (trace.status === 'GOAL_REACHED') {
        report.goalsReached++;
        if (trace.executed === null) report.goalsReachedExternally++;
      }
      if (trace.status === 'REPLAN_READY') {
        report.replansReady++;
        assert.equal(trace.executed, null);
        assert.ok(current.executionSession?.plan.length >= 1);
        awaitingReplanAction.set(trace.npcId,
          { action: current.executionSession.plan[0], turn });
        if (prior.executionSession?.mode === 'REPLAN_PENDING') report.pendingReplanRecoveries++;
      }
      if (trace.status === 'PLANNING_DEFERRED') report.executionPlanningDeferred++;
      if (trace.status === 'NO_PLAN_FOR_GOAL') report.executionNoPlan++;
      if (trace.status === 'INTENT_REEVALUATION_REQUIRED') report.intentReevaluations++;
      if (trace.status === 'DECISION_NO_PLAN') report.decisionNoPlan++;
      if (trace.status === 'DECISION_PLANNING_DEFERRED') report.decisionPlanningDeferred++;
      if (trace.status === 'UTILITY_ACTION_UNMAPPED') report.unmappedUtilityActions++;
    }
    report.maxActiveSessions = Math.max(report.maxActiveSessions,
      next.npcs.filter(item => item.executionSession !== null).length);
    hash.update(JSON.stringify({ turn, result }));
    state = next;
  }
  assert.equal(report.schedulerDispatches, report.decisionCalls + report.executionCalls);
  assert.equal(report.stalePlansPrevented, report.stalePlansForced);
  for (const key of ['brainCallsWithoutDispatch', 'utilityCallsWhileSessionActive',
    'actionsExecutedDuringPlanCreation', 'emptyPlanSessionsCreated',
    'relationBaseMutations']) assert.equal(report[key], 0);
  assert.ok(report.maxActionsPerDispatch <= 1);
  for (const [key, minimum] of Object.entries({ stepsApplied: 250, replansReady: 25,
    intentReevaluations: 10, planSessionsCreated: 100,
    decisionGoalsAlreadySatisfied: 1, decisionPlanningDeferred: 1,
    executionPlanningDeferred: 1, pendingReplanRecoveries: 1,
    goalsReachedExternally: 1, stalePlansForced: 25,
    replanFollowupActions: 1, schedulerBudgetExhaustedTicks: 1 })) {
    assert.ok(report[key] >= minimum,
      `seed ${seed}: ${key}=${report[key]} < ${minimum}`);
  }
  report.digest = hash.digest('hex');
  return report;
}

if (process.argv[1]?.endsWith('stress.mjs')) {
  const reports = SEEDS.map(seed => runStress(seed));
  const repeat = runStress(1337);
  assert.deepEqual(repeat, reports[0]);
  for (const report of reports) process.stdout.write(`${JSON.stringify(report)}\n`);
  process.stdout.write(`repeat1337=${repeat.digest}\n`);
}
