import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { EVENT_KINDS, REASON_ORDER, REASON_PRIORITY,
  createSchedulerState, tickScheduler } from './scheduler.mjs';
import { syntheticConfigs } from './fixtures.mjs';

const seed = Number(process.argv[2] ?? 1337);
const turns = Number(process.argv[3] ?? 5000);
if (!Number.isSafeInteger(seed) || !Number.isSafeInteger(turns) || turns < 1) {
  throw new TypeError('Uso: node stress.mjs [seed entero seguro] [turns>=1]');
}
function rng(initial) {
  let value = initial >>> 0;
  return () => {
    value ^= value << 13; value ^= value >>> 17; value ^= value << 5;
    return value >>> 0;
  };
}
const random = rng(seed);
const configs = syntheticConfigs(64);
const originalConfigs = JSON.stringify(configs);
let state = createSchedulerState(configs);
let clock = -1;
let externalDispatchUnits = 0;
const hash = createHash('sha256');
const report = {
  seed, turns, npcs: configs.length, events: 0, periodicOccurrences: 0,
  dispatches: 0, periodicDispatches: 0, urgentDispatches: 0,
  coalescedEvents: 0, coalescingRatio: 0, budgetExhaustedTicks: 0,
  maxPendingNpcs: 0, maxReasonsPerDispatch: 0, maxReasonCount: 0,
};

function ordered(reasons) {
  for (let i = 1; i < reasons.length; i++) {
    const before = reasons[i - 1], after = reasons[i];
    assert.ok(REASON_PRIORITY[before.kind] > REASON_PRIORITY[after.kind] ||
      (REASON_PRIORITY[before.kind] === REASON_PRIORITY[after.kind] &&
        REASON_ORDER.indexOf(before.kind) < REASON_ORDER.indexOf(after.kind)));
  }
}
function validReasons(reasons, currentTurn) {
  ordered(reasons);
  const kinds = new Set();
  for (const reason of reasons) {
    assert.ok(!kinds.has(reason.kind)); kinds.add(reason.kind);
    assert.ok(Number.isSafeInteger(reason.count) && reason.count >= 1);
    assert.ok(Number.isSafeInteger(reason.firstTurn) &&
      Number.isSafeInteger(reason.lastTurn));
    assert.ok(reason.firstTurn <= reason.lastTurn && reason.lastTurn <= currentTurn);
    report.maxReasonCount = Math.max(report.maxReasonCount, reason.count);
  }
}

for (let index = 0; index < turns; index++) {
  clock += 1 + random() % 5;
  const events = [];
  const eventCount = random() % 11;
  for (let i = 0; i < eventCount; i++) {
    events.push({
      npcId: configs[random() % configs.length].id,
      kind: EVENT_KINDS[random() % EVENT_KINDS.length],
    });
  }
  if (index % 11 === 0) {
    const npcId = configs[random() % configs.length].id;
    for (let i = 0; i < 12; i++) events.push({ npcId, kind: 'MEMORY_CHANGED' });
  }
  if (index % 97 === 0) {
    const npcId = configs[random() % configs.length].id;
    for (let i = 0; i < 15; i++) events.push({ npcId, kind: 'PLAN_INVALIDATED' });
  }
  const options = { maxDispatches: 1 + random() % 12 };
  const previous = state;
  const before = JSON.stringify({ state, events, options });
  for (const npc of previous.npcs) {
    if (clock >= npc.nextPeriodicTurn) {
      report.periodicOccurrences += Math.floor(
        (clock - npc.nextPeriodicTurn) / npc.interval) + 1;
    }
  }
  const result = tickScheduler(state, clock, events, options);
  assert.equal(JSON.stringify({ state, events, options }), before, 'input mutado');
  assert.equal(result.state.clock, clock);
  assert.ok(result.dispatches.length <= options.maxDispatches);
  assert.equal(result.eligibleCount >= result.dispatches.length, true);
  assert.equal(result.status === 'BUDGET_EXHAUSTED',
    result.eligibleCount > options.maxDispatches);
  const dispatchedIds = new Set();
  const nextById = new Map(result.state.npcs.map(npc => [npc.id, npc]));
  const dispatchedById = new Map(result.dispatches.map(dispatch => [dispatch.npcId, dispatch]));
  for (const dispatch of result.dispatches) {
    assert.ok(!dispatchedIds.has(dispatch.npcId), 'más de un dispatch por NPC/tick');
    dispatchedIds.add(dispatch.npcId);
    assert.equal(dispatch.turn, clock);
    assert.equal(dispatch.dominantReason, dispatch.reasons[0].kind);
    validReasons(dispatch.reasons, clock);
    report.maxReasonsPerDispatch = Math.max(report.maxReasonsPerDispatch,
      dispatch.reasons.length);
    if (dispatch.reasons.some(reason => reason.kind === 'PERIODIC')) report.periodicDispatches++;
    if (dispatch.reasons.some(reason => reason.kind === 'PLAN_INVALIDATED')) report.urgentDispatches++;
    if (dispatch.reasons.some(reason => reason.kind !== 'PERIODIC')) externalDispatchUnits++;
    assert.deepEqual(nextById.get(dispatch.npcId).pendingReasons, []);
    assert.equal(nextById.get(dispatch.npcId).lastDispatchTurn, clock);
  }
  let pending = 0;
  for (const old of previous.npcs) {
    const next = nextById.get(old.id);
    assert.ok(next.nextPeriodicTurn > clock);
    assert.ok(next.lastDispatchTurn === null || next.lastDispatchTurn <= clock);
    validReasons(next.pendingReasons, clock);
    if (next.pendingReasons.length) pending++;
    const dispatched = dispatchedById.get(old.id);
    for (const oldReason of old.pendingReasons) {
      const carried = (dispatched?.reasons ?? next.pendingReasons)
        .find(reason => reason.kind === oldReason.kind);
      assert.ok(carried, 'razón pendiente perdida');
      assert.equal(carried.firstTurn, oldReason.firstTurn);
      assert.ok(carried.count >= oldReason.count);
    }
  }
  assert.equal(result.deferredCount, pending);
  report.maxPendingNpcs = Math.max(report.maxPendingNpcs, pending);
  report.events += events.length;
  report.dispatches += result.dispatches.length;
  if (result.status === 'BUDGET_EXHAUSTED') report.budgetExhaustedTicks++;
  hash.update(JSON.stringify(result));
  state = result.state;
}

assert.equal(JSON.stringify(configs), originalConfigs, 'configs mutadas');
const pendingExternalUnits = state.npcs.filter(npc =>
  npc.pendingReasons.some(reason => reason.kind !== 'PERIODIC')).length;
report.coalescedEvents = report.events - externalDispatchUnits - pendingExternalUnits;
assert.ok(report.coalescedEvents >= 0);
assert.ok(report.dispatches < report.events + report.periodicOccurrences,
  'no hubo reducción de trabajo');
report.coalescingRatio = report.dispatches /
  (report.events + report.periodicOccurrences);
report.digest = hash.digest('hex');
console.log(JSON.stringify(report));
