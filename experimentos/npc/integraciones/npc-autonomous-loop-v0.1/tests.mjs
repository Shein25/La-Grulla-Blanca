import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createAutonomousLoopState, tickAutonomousLoop } from './autonomous-loop.mjs';
import { initialFixture, memoryEventFixture, observationFixture, stateFixture } from './fixtures.mjs';

const tick = (state, turn, input = {}, options = {}) => tickAutonomousLoop(state, turn, input, options);
const one = result => result.dispatchResults[0];
const runtime = (state, id = 'npc_helper') => state.npcs.find(item => item.id === id);
const advance = (state, turns) => {
  let result;
  for (let turn = 1; turn <= turns; turn++) { result = tick(state, turn); state = result.state; }
  return result;
};
const clone = value => structuredClone(value);
const expectInvalid = (name, fn, pattern = /./) => test(name, () => assert.throws(fn, pattern));

test('Golden A: first dispatch creates a session without executing', () => {
  const result = tick(stateFixture(), 1);
  assert.equal(one(result).schedulerReason, 'PERIODIC');
  assert.equal(one(result).status, 'PLAN_SESSION_CREATED');
  assert.equal(one(result).path, 'DECISION');
  assert.equal(one(result).executed, null);
  assert.equal(runtime(result.state).world.at, 'puesto');
  assert.ok(runtime(result.state).executionSession);
});

test('Golden B: next dispatch applies exactly one step and does not decide', () => {
  const result = tick(advance(stateFixture(), 1).state, 2);
  assert.equal(one(result).status, 'STEP_APPLIED');
  assert.equal(one(result).path, 'EXECUTION');
  assert.equal(one(result).executed, 'ir_jugador');
  assert.equal(runtime(result.state).world.at, 'jugador');
  assert.equal(runtime(result.state).executionSession.stepCount, 1);
});

test('Golden C: last step reaches goal and closes session', () => {
  const result = tick(advance(stateFixture(), 2).state, 3);
  assert.equal(one(result).status, 'GOAL_REACHED');
  assert.equal(one(result).path, 'EXECUTION');
  assert.equal(one(result).executed, 'ayudar_jugador');
  assert.equal(runtime(result.state).executionSession, null);
  assert.equal(runtime(result.state).world.playerHelped, true);
});

test('Golden D: a new intention may be chosen only on later dispatch', () => {
  const result = tick(advance(stateFixture(), 3).state, 4);
  assert.equal(one(result).path, 'DECISION');
  assert.equal(one(result).utilityAction, 'hablar_jugador');
});

test('Golden E: lost relevance closes session without same-dispatch Utility', () => {
  const state = advance(stateFixture(), 1).state;
  const observation = observationFixture(runtime(state), { playerNeedsHelp: false });
  const result = tick(state, 2, { observations: [observation] });
  assert.deepEqual(result.generatedEvents.worldChanged, ['npc_helper']);
  assert.equal(one(result).path, 'EXECUTION');
  assert.equal(one(result).status, 'INTENT_REEVALUATION_REQUIRED');
  assert.equal(one(result).utilityAction, null);
  assert.equal(runtime(result.state).executionSession, null);
});

test('Golden F: invalid next step replans without action or Utility', () => {
  const state = advance(stateFixture(), 2).state;
  const observation = observationFixture(runtime(state), { at: 'puesto' });
  const result = tick(state, 3, { observations: [observation] });
  assert.equal(one(result).status, 'REPLAN_READY');
  assert.equal(one(result).path, 'EXECUTION');
  assert.equal(one(result).executed, null);
  assert.equal(runtime(result.state).executionSession.plan[0], 'ir_jugador');
});

test('Golden G: social memory changes actual Utility selection', () => {
  const initial = stateFixture([initialFixture('npc_helper', {}, { traits: { empatia: 0, sociabilidad: 75 } })]);
  const baseline = tick(initial, 1);
  const observation = observationFixture(runtime(initial), {}, {}, [memoryEventFixture(1)]);
  const withMemory = tick(initial, 1, { observations: [observation] });
  assert.equal(one(baseline).utilityAction, 'hablar_jugador');
  assert.equal(one(withMemory).utilityAction, 'ayudar_jugador');
  assert.deepEqual(withMemory.generatedEvents.memoryChanged, ['npc_helper']);
  assert.equal(one(withMemory).derivedRelations.confianza, 60);
});

test('Golden H: deferred NPC receives observation but no brain transition', () => {
  const state = stateFixture([initialFixture('npc_a'), initialFixture('npc_b')]);
  const observation = observationFixture(runtime(state, 'npc_b'), { danger: 5 });
  const result = tick(state, 1, { observations: [observation] }, { scheduler: { maxDispatches: 1 } });
  assert.equal(result.dispatchResults.length, 1);
  assert.equal(one(result).npcId, 'npc_b');
  assert.equal(runtime(result.state, 'npc_a').executionSession, null);
  assert.equal(runtime(result.state, 'npc_a').npc.behaviorState.lastAction, null);
  assert.equal(runtime(result.state, 'npc_b').world.danger, 5);
  assert.ok(result.state.scheduler.npcs.find(item => item.id === 'npc_a').pendingReasons.length > 0);
});

test('Golden I: three NPCs retain independent sessions and profiles', () => {
  const items = [initialFixture('npc_guard', { dutyPending: true, dutyImportance: 90 },
    { traits: { disciplina: 100, empatia: 0 } }, { dutyMode: 'vigilar' }),
  initialFixture('npc_helper'), initialFixture('npc_scholar', { playerPresent: false,
    playerNeedsHelp: false, anomalyPresent: true }, { traits: { curiosidad: 100 } })];
  const configs = [{ id: 'npc_guard', interval: 1, minGap: 0, firstPeriodicTurn: 1 },
    { id: 'npc_helper', interval: 2, minGap: 0, firstPeriodicTurn: 2 },
    { id: 'npc_scholar', interval: 3, minGap: 0, firstPeriodicTurn: 3 }];
  let state = stateFixture(items, configs);
  assert.deepEqual(state.npcs.map(x => x.id), ['npc_guard', 'npc_helper', 'npc_scholar']);
  const first = tick(state, 1); state = first.state;
  assert.deepEqual(first.dispatchResults.map(x => x.npcId), ['npc_guard']);
  assert.ok(runtime(state, 'npc_guard').executionSession);
  assert.equal(runtime(state, 'npc_helper').executionSession, null);
  const second = tick(state, 2); state = second.state;
  assert.deepEqual(second.dispatchResults.map(x => x.npcId), ['npc_guard', 'npc_helper']);
  assert.ok(runtime(state, 'npc_helper').executionSession);
  assert.equal(runtime(state, 'npc_scholar').executionSession, null);
  const third = tick(state, 3);
  assert.ok(runtime(third.state, 'npc_scholar').executionSession);
});

test('Golden J: only emitted dispatches consume budget', () => {
  const result = tick(stateFixture([initialFixture('npc_a'), initialFixture('npc_b'), initialFixture('npc_c')]),
    1, {}, { scheduler: { maxDispatches: 1 } });
  assert.equal(result.status, 'SCHEDULER_BUDGET_EXHAUSTED');
  assert.equal(result.scheduler.dispatches.length, 1);
  assert.equal(result.dispatchResults.length, 1);
  assert.equal(result.scheduler.deferredCount, 2);
});

test('Golden K: equal observation does not emit WORLD_CHANGED', () => {
  const state = stateFixture();
  const result = tick(state, 1, { observations: [observationFixture(runtime(state))] });
  assert.deepEqual(result.generatedEvents.worldChanged, []);
});

test('Golden L: memory-only observation emits only MEMORY_CHANGED', () => {
  const state = stateFixture();
  const result = tick(state, 1, { observations: [observationFixture(runtime(state), {}, {},
    [memoryEventFixture(1)])] });
  assert.deepEqual(result.generatedEvents.worldChanged, []);
  assert.deepEqual(result.generatedEvents.memoryChanged, ['npc_helper']);
});

test('Golden M: unmapped talk never creates or executes GOAP', () => {
  const result = tick(stateFixture([initialFixture('npc_helper',
    { playerNeedsHelp: false, playerHelped: true })]), 1);
  assert.equal(one(result).utilityAction, 'hablar_jugador');
  assert.equal(one(result).status, 'UTILITY_ACTION_UNMAPPED');
  assert.equal(one(result).executed, null);
  assert.equal(runtime(result.state).executionSession, null);
});

test('Golden N: decision planning can defer without session', () => {
  const result = tick(stateFixture(), 1, {}, { planner: { maxExpansions: 0 } });
  assert.equal(one(result).status, 'DECISION_PLANNING_DEFERRED');
  assert.equal(runtime(result.state).executionSession, null);
});

test('Golden O: execution replanning can defer with pending session', () => {
  const state = advance(stateFixture(), 2).state;
  const result = tick(state, 3, { observations: [observationFixture(runtime(state), { at: 'puesto' })] },
    { planner: { maxExpansions: 0 } });
  assert.equal(one(result).status, 'PLANNING_DEFERRED');
  assert.equal(one(result).path, 'EXECUTION');
  assert.equal(runtime(result.state).executionSession.mode, 'REPLAN_PENDING');
});

test('Golden P: derived relation is temporary', () => {
  const state = stateFixture();
  const result = tick(state, 1, { observations: [observationFixture(runtime(state), {}, {},
    [memoryEventFixture(1)])] });
  assert.equal(one(result).derivedRelations.confianza, 60);
  assert.equal(runtime(result.state).npc.relationPlayer.confianza, 50);
  assert.equal(runtime(state).npc.relationPlayer.confianza, 50);
});

test('Golden Q: behavior state changes only on decision', () => {
  let state = stateFixture();
  for (let turn = 1; turn <= 3; turn++) {
    const result = tick(state, turn); state = result.state;
    assert.equal(runtime(state).npc.behaviorState.lastAction, 'ayudar_jugador');
    assert.equal(runtime(state).npc.behaviorState.consecutiveTurns, 1);
  }
  const next = tick(state, 4);
  assert.equal(runtime(next.state).npc.behaviorState.lastAction, 'hablar_jugador');
  assert.equal(runtime(next.state).npc.behaviorState.consecutiveTurns, 1);
});

test('Golden R: every dispatch has exactly one path and at most one action', () => {
  let state = stateFixture();
  for (let turn = 1; turn <= 15; turn++) {
    const result = tick(state, turn); state = result.state;
    assert.equal(result.dispatchResults.length, result.scheduler.dispatches.length);
    for (const trace of result.dispatchResults) {
      assert.ok(['DECISION', 'EXECUTION'].includes(trace.path));
      if (trace.path === 'DECISION') assert.equal(trace.executed, null);
      if (trace.path === 'EXECUTION') assert.equal(trace.utilityAction, null);
      assert.ok(trace.executed === null || typeof trace.executed === 'string');
    }
  }
});

test('clock starts null and follows scheduler through sparse turns', () => {
  let state = stateFixture();
  assert.equal(state.clock, null); assert.equal(state.scheduler.clock, null);
  for (const turn of [0, 2, 19]) {
    state = tick(state, turn).state;
    assert.equal(state.clock, turn); assert.equal(state.scheduler.clock, turn);
  }
});

test('no dispatch means no decision or execution', () => {
  const state = stateFixture([initialFixture()], [{ id: 'npc_helper', interval: 10, minGap: 0, firstPeriodicTurn: 10 }]);
  const result = tick(state, 1);
  assert.deepEqual(result.dispatchResults, []);
  assert.equal(runtime(result.state).npc.behaviorState.lastAction, null);
  assert.equal(runtime(result.state).executionSession, null);
});

test('external scheduler events pass through without artificial deduplication', () => {
  const state = stateFixture();
  const result = tick(state, 1, { schedulerEvents: [
    { npcId: 'npc_helper', kind: 'WORLD_CHANGED' },
    { npcId: 'npc_helper', kind: 'WORLD_CHANGED' }] });
  assert.equal(result.dispatchResults.length, 1);
  assert.equal(result.scheduler.dispatches[0].reasons.find(x => x.kind === 'WORLD_CHANGED').count, 2);
});

test('observation context change alone emits WORLD_CHANGED', () => {
  const state = stateFixture();
  const result = tick(state, 1, { observations: [observationFixture(runtime(state), {},
    { superiorReachable: false })] });
  assert.deepEqual(result.generatedEvents.worldChanged, ['npc_helper']);
});

test('world uses Object.is, including negative zero', () => {
  const state = stateFixture();
  const result = tick(state, 1, { observations: [observationFixture(runtime(state), { marker: -0 })] });
  assert.deepEqual(result.generatedEvents.worldChanged, ['npc_helper']);
  assert.ok(Object.is(runtime(result.state).world.marker, -0));
});

test('observation and memory events are canonically ordered', () => {
  const state = stateFixture([initialFixture('npc_b'), initialFixture('npc_a')]);
  const input = { observations: [observationFixture(runtime(state, 'npc_b'), {}, {},
    [memoryEventFixture(1, 'PLAYER_LIED', 'z'), memoryEventFixture(1, 'PLAYER_HELPED_ME', 'a')]),
  observationFixture(runtime(state, 'npc_a'), {}, {}, [memoryEventFixture(1)])] };
  const result = tick(state, 1, input);
  assert.deepEqual(result.generatedEvents.memoryChanged, ['npc_a', 'npc_b']);
  assert.deepEqual(runtime(result.state, 'npc_b').memory.entries.map(x => x.key), ['a', 'z']);
});

test('input, state, and options remain unchanged', () => {
  const state = stateFixture();
  const input = { observations: [observationFixture(runtime(state), {}, {}, [memoryEventFixture(1)])] };
  const options = { scheduler: { maxDispatches: 1 }, planner: { maxFrontier: 50 } };
  const before = [clone(state), clone(input), clone(options)];
  tick(state, 1, input, options);
  assert.deepEqual([state, input, options], before);
});

test('output mutation cannot affect replay or earlier result', () => {
  const state = stateFixture();
  const a = tick(state, 1); const b = tick(state, 1);
  a.state.npcs[0].world.at = 'corrupt'; a.dispatchResults[0].status = 'corrupt';
  a.generatedEvents.worldChanged.push('corrupt');
  assert.deepEqual(b, tick(state, 1));
  assert.equal(b.dispatchResults[0].status, 'PLAN_SESSION_CREATED');
});

test('same input produces exact deterministic output', () => {
  const state = stateFixture([initialFixture('npc_z'), initialFixture('npc_a')]);
  assert.deepEqual(tick(state, 1), tick(state, 1));
});

test('memory updates are applied before decision', () => {
  const state = stateFixture();
  const result = tick(state, 1, { observations: [observationFixture(runtime(state), {}, {},
    [memoryEventFixture(1)])] });
  assert.equal(runtime(result.state).memory.entries.length, 1);
  assert.equal(one(result).derivedRelations.confianza, 60);
});

test('replan ready waits until later dispatch for first new step', () => {
  const state = advance(stateFixture(), 2).state;
  const replanned = tick(state, 3, { observations: [observationFixture(runtime(state), { at: 'puesto' })] });
  assert.equal(one(replanned).executed, null);
  const next = tick(replanned.state, 4);
  assert.equal(one(next).executed, 'ir_jugador');
});

test('pending replan retries on later dispatch', () => {
  const state = advance(stateFixture(), 2).state;
  const pending = tick(state, 3, { observations: [observationFixture(runtime(state), { at: 'puesto' })] },
    { planner: { maxExpansions: 0 } });
  const ready = tick(pending.state, 4);
  assert.equal(one(ready).status, 'REPLAN_READY');
  assert.equal(runtime(ready.state).executionSession.mode, 'ACTIVE');
});

test('same chosen action increments inertia on later decisions', () => {
  const state = stateFixture([initialFixture('npc_helper', { playerNeedsHelp: false, playerHelped: true })]);
  const first = tick(state, 1); const second = tick(first.state, 2);
  assert.equal(runtime(second.state).npc.behaviorState.lastAction, 'hablar_jugador');
  assert.equal(runtime(second.state).npc.behaviorState.consecutiveTurns, 2);
});

function alreadyWaitedState() {
  return stateFixture([initialFixture('npc_helper',
    { waited: true, playerPresent: false, playerNeedsHelp: false,
      dutyImportance: 0, urgency: 0, danger: 0 },
    { traits: { disciplina: 0, sociabilidad: 0, curiosidad: 0, prudencia: 0,
      lealtad_institucional: 0, empatia: 0 } }, { superiorReachable: false })]);
}

test('REV2: empty PLAN_READY reports already satisfied and creates no session', () => {
  const result = tick(alreadyWaitedState(), 1);
  assert.equal(one(result).path, 'DECISION');
  assert.equal(one(result).utilityAction, 'esperar');
  assert.equal(one(result).status, 'DECISION_GOAL_ALREADY_SATISFIED');
  assert.equal(one(result).executed, null);
  assert.equal(runtime(result.state).executionSession, null);
});

test('REV2: empty plan needs no later EXECUTION cleanup', () => {
  const first = tick(alreadyWaitedState(), 1);
  const second = tick(first.state, 2);
  assert.equal(one(second).path, 'DECISION');
  assert.equal(one(second).status, 'DECISION_GOAL_ALREADY_SATISFIED');
  assert.equal(runtime(second.state).executionSession, null);
});

test('REV2: every session created by decision has at least one step', () => {
  const items = [initialFixture('npc_help'),
    initialFixture('npc_wait', { playerPresent: false, playerNeedsHelp: false, waited: true,
      urgency: 0, dutyImportance: 0 },
    { traits: { disciplina: 0, sociabilidad: 0, curiosidad: 0, prudencia: 0,
      lealtad_institucional: 0, empatia: 0 } }, { superiorReachable: false }),
    initialFixture('npc_duty', { playerPresent: false, playerNeedsHelp: false,
      dutyPending: true, dutyImportance: 90 }, { traits: { disciplina: 100, empatia: 0 } })];
  let state = stateFixture(items);
  for (let turn = 1; turn <= 12; turn++) {
    const result = tick(state, turn);
    for (const trace of result.dispatchResults.filter(x => x.status === 'PLAN_SESSION_CREATED')) {
      assert.ok(runtime(result.state, trace.npcId).executionSession.plan.length >= 1);
    }
    state = result.state;
  }
});

test('REV2: empty plan still updates Utility behavior and inertia', () => {
  const first = tick(alreadyWaitedState(), 1);
  assert.deepEqual(runtime(first.state).npc.behaviorState,
    { lastAction: 'esperar', consecutiveTurns: 1 });
  const second = tick(first.state, 2);
  assert.deepEqual(runtime(second.state).npc.behaviorState,
    { lastAction: 'esperar', consecutiveTurns: 2 });
});

test('REV2: external goal completion closes session without executing or deciding', () => {
  const state = tick(stateFixture(), 1).state;
  const result = tick(state, 2, { observations: [observationFixture(runtime(state),
    { playerHelped: true })] });
  assert.deepEqual(result.generatedEvents.worldChanged, ['npc_helper']);
  assert.equal(one(result).path, 'EXECUTION');
  assert.equal(one(result).status, 'GOAL_REACHED');
  assert.equal(one(result).executed, null);
  assert.equal(one(result).utilityAction, null);
  assert.equal(runtime(result.state).executionSession, null);
});

test('REV2: stale plan defers, recovers, then executes on separate dispatches', () => {
  const afterStep = advance(stateFixture(), 2).state;
  const pending = tick(afterStep, 3, { observations: [observationFixture(runtime(afterStep),
    { at: 'puesto' })] }, { planner: { maxExpansions: 0 } });
  assert.equal(one(pending).status, 'PLANNING_DEFERRED');
  assert.equal(one(pending).executed, null);
  assert.equal(runtime(pending.state).executionSession.mode, 'REPLAN_PENDING');
  const ready = tick(pending.state, 4);
  assert.equal(one(ready).status, 'REPLAN_READY');
  assert.equal(one(ready).executed, null);
  const stepped = tick(ready.state, 5);
  assert.equal(one(stepped).path, 'EXECUTION');
  assert.equal(one(stepped).executed, 'ir_jugador');
});

const badCreate = [
  ['duplicate NPC IDs', () => createAutonomousLoopState({ schedulerConfigs: [{ id: 'npc_helper', interval: 1, minGap: 0, firstPeriodicTurn: 1 }], npcs: [initialFixture(), initialFixture()] })],
  ['missing scheduler ID', () => createAutonomousLoopState({ schedulerConfigs: [], npcs: [initialFixture()] })],
  ['extra scheduler ID', () => createAutonomousLoopState({ schedulerConfigs: [{ id: 'npc_helper', interval: 1, minGap: 0, firstPeriodicTurn: 1 }], npcs: [] })],
  ['initial memory injection', () => createAutonomousLoopState({ schedulerConfigs: [{ id: 'npc_helper', interval: 1, minGap: 0, firstPeriodicTurn: 1 }], npcs: [{ ...initialFixture(), memory: {} }] })],
  ['extra creation field', () => createAutonomousLoopState({ schedulerConfigs: [], npcs: [], extra: 1 })],
  ['invalid NPC trait', () => stateFixture([initialFixture('npc_helper', {}, { traits: { empatia: 101 } })])],
  ['incoherent initial context', () => stateFixture([initialFixture('npc_helper', {}, {}, { playerRequestsHelp: false })])],
  ['incoherent initial world', () => stateFixture([initialFixture('npc_helper', { danger: NaN })])],
];
for (const [name, fn] of badCreate) expectInvalid(`creation rejects ${name}`, fn);

const badTick = [
  ['negative turn', (s) => tick(s, -1)],
  ['fractional turn', (s) => tick(s, 1.5)],
  ['unsafe turn', (s) => tick(s, Number.MAX_SAFE_INTEGER + 1)],
  ['duplicate turn', (s) => tick(tick(s, 1).state, 1)],
  ['decreasing turn', (s) => tick(tick(s, 2).state, 1)],
  ['clock disagreement', (s) => tick({ ...s, clock: 3 }, 4)],
  ['duplicate observations', (s) => { const o = observationFixture(runtime(s)); return tick(s, 1, { observations: [o, o] }); }],
  ['unknown observation NPC', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), npcId: 'ghost' }] })],
  ['duplicate memory keys', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), {}, {}, [memoryEventFixture(1), memoryEventFixture(1)])] })],
  ['past memory turn', (s) => tick(s, 2, { observations: [observationFixture(runtime(s), {}, {}, [memoryEventFixture(1)])] })],
  ['future memory turn', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), {}, {}, [memoryEventFixture(2)])] })],
  ['incoherent observation', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), {}, { awayFromPost: true })] })],
  ['unknown scheduler NPC', (s) => tick(s, 1, { schedulerEvents: [{ npcId: 'ghost', kind: 'WORLD_CHANGED' }] })],
  ['unknown scheduler event', (s) => tick(s, 1, { schedulerEvents: [{ npcId: 'npc_helper', kind: 'FAKE' }] })],
  ['zero scheduler budget', (s) => tick(s, 1, {}, { scheduler: { maxDispatches: 0 } })],
  ['negative planner expansions', (s) => tick(s, 1, {}, { planner: { maxExpansions: -1 } })],
  ['zero planner frontier', (s) => tick(s, 1, {}, { planner: { maxFrontier: 0 } })],
  ['extra options', (s) => tick(s, 1, {}, { npcPlanner: {} })],
  ['extra planner option', (s) => tick(s, 1, {}, { planner: { beam: 3 } })],
  ['extra input field', (s) => tick(s, 1, { other: true })],
  ['extra observation field', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), extra: true }] })],
  ['extra runtime field', (s) => { const c = clone(s); c.npcs[0].extra = true; return tick(c, 1); }],
  ['runtime ID mismatch', (s) => { const c = clone(s); c.npcs[0].id = 'other'; return tick(c, 1); }],
  ['scheduler ID mismatch', (s) => { const c = clone(s); c.scheduler.npcs[0].id = 'other'; return tick(c, 1); }],
  ['nonfinite world fact', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), { marker: Infinity })] })],
  ['object world fact', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), { marker: {} })] })],
  ['empty world fact key', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), { '': 1 })] })],
  ['invalid memory event', (s) => tick(s, 1, { observations: [observationFixture(runtime(s), {}, {}, [{ ...memoryEventFixture(1), confidence: 101 }])] })],
];
for (const [name, fn] of badTick) expectInvalid(`tick rejects ${name}`, () => fn(stateFixture()));

function getterObject(base, key = 'evil') {
  const value = { ...base }; Object.defineProperty(value, key, { enumerable: true, get() { throw Error('getter invoked'); } }); return value;
}
function setterObject(base, key = 'evil') {
  const value = { ...base }; Object.defineProperty(value, key, { enumerable: true, set(_) {} }); return value;
}
function proxyObject(base) { return new Proxy(base, { ownKeys() { throw Error('hostile proxy'); } }); }
function holeArray(items) { const value = [...items]; value.length++; return value; }
function accessorArray(items) { const value = [...items]; Object.defineProperty(value, '0', { get() { throw Error('array getter'); } }); return value; }
function inherited(base) { return Object.assign(Object.create({ inherited: true }), base); }

const hostile = [
  ['top state getter', (s) => tick(getterObject(s), 1)],
  ['top state setter', (s) => tick(setterObject(s), 1)],
  ['top state inherited', (s) => tick(inherited(s), 1)],
  ['top state symbol', (s) => tick({ ...s, [Symbol('x')]: 1 }, 1)],
  ['top state proxy', (s) => tick(proxyObject(s), 1)],
  ['runtime getter', (s) => { const c = clone(s); c.npcs[0] = getterObject(c.npcs[0]); return tick(c, 1); }],
  ['runtime proxy', (s) => { const c = clone(s); c.npcs[0] = proxyObject(c.npcs[0]); return tick(c, 1); }],
  ['runtime array hole', (s) => tick({ ...s, npcs: holeArray(s.npcs) }, 1)],
  ['runtime accessor index', (s) => tick({ ...s, npcs: accessorArray(s.npcs) }, 1)],
  ['input getter', (s) => tick(s, 1, getterObject({}))],
  ['input symbol', (s) => tick(s, 1, { [Symbol('x')]: 1 })],
  ['input inherited', (s) => tick(s, 1, inherited({}))],
  ['observations array hole', (s) => tick(s, 1, { observations: holeArray([]) })],
  ['observations accessor index', (s) => tick(s, 1, { observations: accessorArray([observationFixture(runtime(s))]) })],
  ['observation getter', (s) => tick(s, 1, { observations: [getterObject(observationFixture(runtime(s)))] })],
  ['observation symbol', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), [Symbol('x')]: 1 }] })],
  ['world getter', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), world: getterObject(runtime(s).world) }] })],
  ['world setter', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), world: setterObject(runtime(s).world) }] })],
  ['world symbol', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), world: { ...runtime(s).world, [Symbol('x')]: 1 } }] })],
  ['world inherited', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), world: inherited(runtime(s).world) }] })],
  ['world proxy', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), world: proxyObject(runtime(s).world) }] })],
  ['context getter', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), utilityContext: getterObject(runtime(s).utilityContext) }] })],
  ['context symbol', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), utilityContext: { ...runtime(s).utilityContext, [Symbol('x')]: 1 } }] })],
  ['context inherited', (s) => tick(s, 1, { observations: [{ ...observationFixture(runtime(s)), utilityContext: inherited(runtime(s).utilityContext) }] })],
  ['scheduler events array hole', (s) => tick(s, 1, { schedulerEvents: holeArray([]) })],
  ['scheduler events accessor index', (s) => tick(s, 1, { schedulerEvents: accessorArray([{ npcId: 'npc_helper', kind: 'WORLD_CHANGED' }]) })],
  ['scheduler event getter', (s) => tick(s, 1, { schedulerEvents: [getterObject({ npcId: 'npc_helper', kind: 'WORLD_CHANGED' })] })],
  ['scheduler event symbol', (s) => tick(s, 1, { schedulerEvents: [{ npcId: 'npc_helper', kind: 'WORLD_CHANGED', [Symbol('x')]: 1 }] })],
  ['options getter', (s) => tick(s, 1, {}, getterObject({}))],
  ['options inherited', (s) => tick(s, 1, {}, inherited({}))],
  ['options symbol', (s) => tick(s, 1, {}, { [Symbol('x')]: 1 })],
  ['planner options getter', (s) => tick(s, 1, {}, { planner: getterObject({}) })],
];
for (const [name, fn] of hostile) expectInvalid(`hostile ${name}`, () => fn(stateFixture()), /./);

test('safe behavior counter overflow raises RangeError without modifying state', () => {
  const state = stateFixture([initialFixture('npc_helper', { playerNeedsHelp: false,
    playerHelped: true }, { behaviorState: { lastAction: 'hablar_jugador',
      consecutiveTurns: Number.MAX_SAFE_INTEGER } })]);
  const before = clone(state);
  assert.throws(() => tick(state, 1), RangeError);
  assert.deepEqual(state, before);
});

test('invalid late observation is atomic for input state', () => {
  const state = stateFixture([initialFixture('npc_a'), initialFixture('npc_b')]);
  const input = { observations: [observationFixture(runtime(state, 'npc_a'), {}, {}, [memoryEventFixture(1)]),
    observationFixture(runtime(state, 'npc_b'), {}, { playerPresent: false })] };
  const before = [clone(state), clone(input)];
  assert.throws(() => tick(state, 1, input));
  assert.deepEqual([state, input], before);
});
