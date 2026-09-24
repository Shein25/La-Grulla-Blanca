import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { tickAutonomousLoop } from './autonomous-loop.mjs';
import { initialFixture, memoryEventFixture, observationFixture, stateFixture } from './fixtures.mjs';

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
    const world = index % 3 === 0
      ? { playerPresent: false, playerNeedsHelp: false, anomalyPresent: true,
        urgency: 30, dutyImportance: 40 }
      : index % 3 === 1
        ? { playerPresent: false, playerNeedsHelp: false, dutyPending: true,
          urgency: 20, dutyImportance: 80 }
        : { urgency: 75 };
    const traits = { empatia: 30 + index * 4, curiosidad: 20 + index * 3,
      disciplina: 25 + index * 4, sociabilidad: 20 + index * 3 };
    items.push(initialFixture(id, world, { traits }));
    configs.push({ id, interval: 1 + index % 7, minGap: index % 2,
      firstPeriodicTurn: 1 + index % 7 });
  }
  return stateFixture(items, configs);
}

function nextInput(state, turn, random) {
  const observations = [], schedulerEvents = [];
  const add = (index, update, memoryEvents = []) => {
    const runtime = state.npcs[index];
    const previous = observations.find(item => item.npcId === runtime.id);
    if (previous) {
      previous.world = { ...previous.world, ...update };
      previous.utilityContext = observationFixture({ ...runtime,
        world: previous.world, utilityContext: previous.utilityContext }, update).utilityContext;
      previous.memoryEvents.push(...memoryEvents);
    } else observations.push(observationFixture(runtime, update, {}, memoryEvents));
  };
  if (turn % 11 === 0) {
    const index = random() % NPC_COUNT, world = state.npcs[index].world;
    add(index, { danger: (world.danger + 17) % 101 });
  }
  if (turn % 37 === 0) {
    const index = random() % NPC_COUNT, world = state.npcs[index].world;
    add(index, { playerPresent: !world.playerPresent,
      playerNeedsHelp: !world.playerPresent, playerHelped: false });
  }
  if (turn % 17 === 0) {
    const index = random() % NPC_COUNT, world = state.npcs[index].world;
    add(index, { anomalyPresent: !world.anomalyPresent, anomalyInvestigated: false });
  }
  if (turn % 43 === 0) {
    const activeHelp = state.npcs.findIndex(item => item.executionSession?.goalId === 'HELP_PLAYER');
    const index = activeHelp >= 0 ? activeHelp : random() % NPC_COUNT;
    const world = state.npcs[index].world;
    const update = turn % 86 === 0 && activeHelp >= 0
      ? { playerNeedsHelp: false }
      : { at: world.at === 'puesto' ? 'jugador' : 'puesto',
        playerReachable: !world.playerReachable };
    add(index, update);
    schedulerEvents.push({ npcId: state.npcs[index].id, kind: 'PLAN_INVALIDATED' });
  }
  if (turn % 29 === 0) {
    const index = random() % NPC_COUNT;
    const kind = turn % 58 === 0 ? 'PLAYER_LIED' : 'PLAYER_HELPED_ME';
    const event = memoryEventFixture(turn, kind, `memory-${turn}-${index}`);
    add(index, {}, [event]);
  }
  observations.sort((a, b) => a.npcId < b.npcId ? -1 : a.npcId > b.npcId ? 1 : 0);
  return { observations, schedulerEvents };
}

function metrics(seed) {
  return { seed, globalTurns: GLOBAL_TURNS, npcCount: NPC_COUNT,
    schedulerDispatches: 0, schedulerDeferred: 0, schedulerBudgetExhaustedTicks: 0,
    decisionCalls: 0, executionCalls: 0, planSessionsCreated: 0,
    stepsApplied: 0, goalsReached: 0, replansReady: 0,
    executionPlanningDeferred: 0, executionNoPlan: 0, intentReevaluations: 0,
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
  let state = initialState();
  for (let turn = 1; turn <= turns; turn++) {
    const before = state;
    const input = nextInput(before, turn, random);
    const options = { scheduler: { maxDispatches: turn % 13 === 0 ? 2 : 5 },
      planner: turn % 97 === 0 ? { maxExpansions: 0 } : {} };
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
    for (const trace of result.dispatchResults) {
      if (trace.status === 'PLAN_SESSION_CREATED') report.planSessionsCreated++;
      if (trace.status === 'STEP_APPLIED') report.stepsApplied++;
      if (trace.status === 'GOAL_REACHED') report.goalsReached++;
      if (trace.status === 'REPLAN_READY') report.replansReady++;
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
  for (const key of ['brainCallsWithoutDispatch', 'utilityCallsWhileSessionActive',
    'actionsExecutedDuringPlanCreation', 'relationBaseMutations']) assert.equal(report[key], 0);
  assert.ok(report.maxActionsPerDispatch <= 1);
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
