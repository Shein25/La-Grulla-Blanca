import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { resolveAreaCatchUp } from './catchup-resolver.mjs';

const seed = Number(process.argv[2] ?? 1337);
if (!Number.isSafeInteger(seed) || seed < 0) throw new TypeError('seed debe ser entero seguro no negativo');
let randomState = seed >>> 0;
function random() { randomState = (Math.imul(randomState, 1664525) + 1013904223) >>> 0; return randomState; }
function pick(n) { return random() % n; }
const count = 2000;
const elapsedChoices = [1, 2, 10, 100, 10_000, 1_000_000, 1_000_000_000];

function fixture(label) {
  const entities = [];
  for (let e = 0; e < 128; e++) {
    const timers = [];
    const meters = [];
    for (let t = 0, n = pick(6); t < n; t++) timers.push({ id: `t_${t}`, remainingTurns: pick(1_000_001) });
    for (let m = 0, n = pick(6); m < n; m++) {
      const min = m === 0 ? -Number.MAX_SAFE_INTEGER : -1000;
      const max = m === 0 ? Number.MAX_SAFE_INTEGER : 1000;
      const value = m === 0 ? 0 : pick(2001) - 1000;
      const ratePerTurn = m === 0 ? (e % 2 ? Number.MAX_SAFE_INTEGER : -Number.MAX_SAFE_INTEGER) : pick(101) - 50;
      meters.push({ id: `m_${m}`, value, ratePerTurn, min, max });
    }
    entities.push({ id: `entity_${String(e).padStart(3, '0')}`, timers, meters });
  }
  const scheduledEvents = [];
  const eventCount = 500 + pick(1501);
  for (let i = 0; i < eventCount; i++) scheduledEvents.push({
    id: `event_${String(i).padStart(4, '0')}`, targetId: i % 3 === 0 ? null : entities[pick(128)].id,
    kind: 'SYNTHETIC', dueTurn: 101 + pick(1_500_000_000)
  });
  // Inputs deliberately need not be in canonical order.
  return { version: 1, areaId: `area_${label}`, syncedTurn: 100, entities: entities.reverse(), scheduledEvents: scheduledEvents.reverse() };
}

const states = Array.from({ length: 4 }, (_, i) => fixture(i));
const originals = states.map(s => JSON.stringify(s));
const digest = createHash('sha256');
let entitiesProcessed = 0, timersProcessed = 0, timersCompleted = 0, metersProcessed = 0;
let metersChanged = 0, scheduledEventsProcessed = 0, dueEvents = 0, totalElapsedTurns = 0n, maxElapsedTurns = 0;
const lexical = (a, b) => a < b ? -1 : a > b ? 1 : 0;
const eventOrder = (a, b) => a.dueTurn - b.dueTurn || lexical(a.id, b.id);

for (let i = 0; i < count; i++) {
  const state = states[i % states.length];
  const elapsedTurns = i % 8 === 7 ? 1 + pick(1_500_000_000) : elapsedChoices[i % 8];
  const catchUp = { areaId: state.areaId, fromTurn: 100, toTurn: 100 + elapsedTurns, elapsedTurns };
  const beforeRequest = JSON.stringify(catchUp);
  const result = resolveAreaCatchUp(state, catchUp);
  const serialized = JSON.stringify(result);
  assert.equal(JSON.stringify(resolveAreaCatchUp(state, catchUp)), serialized, 'determinismo');
  assert.equal(JSON.stringify(state), originals[i % states.length], 'input state mutado');
  assert.equal(JSON.stringify(catchUp), beforeRequest, 'catchUp mutado');
  assert.equal(result.state.syncedTurn, catchUp.toTurn);
  assert.equal(result.status, 'CATCH_UP_APPLIED');
  assert.equal(result.state.entities.length, state.entities.length);
  assert.deepEqual(result.state.entities.map(e => e.id), state.entities.map(e => e.id).sort(lexical), 'IDs de entidades');
  const byId = new Map(state.entities.map(e => [e.id, e]));
  let expectedCompleted = 0, expectedChanged = 0;
  for (const entity of result.state.entities) {
    entitiesProcessed++;
    const original = byId.get(entity.id);
    assert.deepEqual(entity.timers.map(t => t.id), original.timers.map(t => t.id).sort(lexical), 'IDs de timers');
    assert.deepEqual(entity.meters.map(m => m.id), original.meters.map(m => m.id).sort(lexical), 'IDs de meters');
    const oldTimers = new Map(original.timers.map(t => [t.id, t]));
    const oldMeters = new Map(original.meters.map(m => [m.id, m]));
    for (const timer of entity.timers) {
      timersProcessed++;
      const previous = oldTimers.get(timer.id).remainingTurns;
      // Oracle independiente: resta en BigInt y clamp a cero.
      const raw = BigInt(previous) - BigInt(elapsedTurns);
      assert.equal(timer.remainingTurns, Number(raw < 0n ? 0n : raw));
      assert.ok(timer.remainingTurns >= 0);
      if (previous > 0 && timer.remainingTurns === 0) expectedCompleted++;
    }
    for (const meter of entity.meters) {
      metersProcessed++;
      const old = oldMeters.get(meter.id);
      const raw = BigInt(old.value) + BigInt(old.ratePerTurn) * BigInt(elapsedTurns);
      const expected = raw < BigInt(old.min) ? BigInt(old.min) : raw > BigInt(old.max) ? BigInt(old.max) : raw;
      assert.equal(meter.value, Number(expected));
      assert.ok(meter.min <= meter.value && meter.value <= meter.max);
      if (meter.value !== old.value) expectedChanged++;
    }
  }
  assert.equal(result.summary.completedTimers.length, expectedCompleted);
  assert.equal(result.summary.meterChanges.length, expectedChanged);
  timersCompleted += expectedCompleted;
  metersChanged += expectedChanged;
  const expectedDue = state.scheduledEvents.filter(e => e.dueTurn <= catchUp.toTurn).sort(eventOrder);
  const expectedPending = state.scheduledEvents.filter(e => e.dueTurn > catchUp.toTurn).sort(eventOrder);
  assert.deepEqual(result.summary.dueEvents, expectedDue);
  assert.deepEqual(result.state.scheduledEvents, expectedPending);
  assert.equal(result.summary.dueEvents.length + result.state.scheduledEvents.length, state.scheduledEvents.length, 'IDs de eventos perdidos');
  assert.ok(result.summary.dueEvents.every(e => e.dueTurn > 100 && e.dueTurn <= catchUp.toTurn));
  assert.ok(result.state.scheduledEvents.every(e => e.dueTurn > result.state.syncedTurn));
  scheduledEventsProcessed += state.scheduledEvents.length;
  dueEvents += expectedDue.length;
  totalElapsedTurns += BigInt(elapsedTurns);
  maxElapsedTurns = Math.max(maxElapsedTurns, elapsedTurns);
  digest.update(serialized);
  digest.update('\n');
}

console.log(JSON.stringify({ seed, scenarios: count, catchUpCalls: count, entitiesProcessed, timersProcessed,
  timersCompleted, metersProcessed, metersChanged, scheduledEventsProcessed, dueEvents,
  totalElapsedTurns: totalElapsedTurns.toString(), maxElapsedTurns, digest: digest.digest('hex') }));
