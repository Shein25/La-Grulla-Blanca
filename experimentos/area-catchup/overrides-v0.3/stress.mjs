import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { resolveOverrideCatchUp } from './override-resolver.mjs';

const seed = Number(process.argv[2] ?? 1337);
if (!Number.isSafeInteger(seed) || seed < 0) throw new TypeError('seed inválida');
let randomState = seed >>> 0;
function random() { randomState = (Math.imul(randomState, 1664525) + 1013904223) >>> 0; return randomState; }
function pick(n) { return random() % n; }
const lexical = (a, b) => a < b ? -1 : a > b ? 1 : 0;
const scenarios = 10_000;
const elapsedChoices = [1, 2, 10, 100, 10_000, 1_000_000, 1_000_000_000];

function oraclePosition(turn, agenda, overrides) {
  const phase = Number((BigInt(turn) + BigInt(agenda.offset)) % BigInt(agenda.cycleLength));
  const matches = agenda.slots.filter(slot => slot.start <= phase && phase < slot.end);
  assert.equal(matches.length, 1, 'fase con exactamente un slot');
  const active = overrides.filter(o => o.startTurn <= turn && (o.endTurn === null || turn < o.endTurn));
  active.sort((a, b) => b.priority - a.priority || b.startTurn - a.startTurn || lexical(a.id, b.id));
  const winner = active[0];
  return { slot: matches[0], winner, activeCount: active.length,
    roomId: winner?.roomId ?? matches[0].roomId, activity: winner?.activity ?? matches[0].activity,
    sourceType: winner ? 'OVERRIDE' : 'AGENDA', sourceId: winner?.id ?? matches[0].id };
}

function fixture(label) {
  const entities = [];
  for (let i = 0; i < 128; i++) {
    const cycleLength = i === 0 ? 1 : 12 + pick(1989);
    const offset = pick(cycleLength);
    const slotCount = i === 0 ? 1 : 1 + pick(12);
    const slots = [];
    let start = 0;
    for (let j = 0; j < slotCount; j++) {
      const remaining = cycleLength - start;
      const left = slotCount - j;
      const length = left === 1 ? remaining : 1 + pick(remaining - left + 1);
      slots.push({ id: `slot_${String(j).padStart(2, '0')}`, start, end: start + length,
        roomId: `room_${j % 5}`, activity: `ACT_${j % 7}` });
      start += length;
    }
    const agenda = { cycleLength, offset, slots: slots.reverse() };
    const overrides = [];
    for (let j = 0, n = pick(13); j < n; j++) {
      let startTurn, endTurn;
      switch (j % 5) {
        case 0: startTurn = pick(11); endTurn = j % 2 ? null : 11 + pick(1_000_000_000); break;
        case 1: startTurn = 11 + pick(500); endTurn = startTurn + 1 + pick(1000); break;
        case 2: startTurn = 11 + pick(1_000_000_000); endTurn = null; break;
        case 3: startTurn = Number.MAX_SAFE_INTEGER - 1000 + pick(1000); endTurn = null; break;
        default: startTurn = 11 + pick(1_000_000_000); endTurn = startTurn + 1 + pick(1_000_000_000);
      }
      overrides.push({ id: `override_${String(j).padStart(2, '0')}`, kind: `SYNTHETIC_${j % 4}`,
        priority: j % 3 === 0 ? 10 : pick(21), startTurn, endTurn,
        roomId: `override_room_${j % 4}`, activity: `OVERRIDE_ACT_${j % 6}` });
    }
    const initial = oraclePosition(10, agenda, overrides);
    entities.push({ id: `npc_${String(i).padStart(3, '0')}`, logicalRoomId: initial.roomId,
      currentActivity: initial.activity, currentSourceType: initial.sourceType,
      currentSourceId: initial.sourceId, agenda, overrides: overrides.reverse() });
  }
  return { version: 1, areaId: `area_${label}`, syncedTurn: 10, entities: entities.reverse() };
}

const states = Array.from({ length: 4 }, (_, i) => fixture(i));
const originals = states.map(s => JSON.stringify(s));
const digest = createHash('sha256');
let entitiesProcessed = 0, overridesProcessed = 0, agendaFinalStates = 0, overrideFinalStates = 0;
let visibleChanges = 0, sourceChanges = 0, expiredOverrides = 0, futureOverridesRemaining = 0;
let activeOverridesRemaining = 0, shadowedOverrides = 0, totalElapsedTurns = 0n;
let maxElapsedTurns = 0, fullCyclesCollapsed = 0n;

for (let i = 0; i < scenarios; i++) {
  const state = states[i % states.length];
  const elapsedTurns = i % 9 === 7 ? 1 + pick(1_500_000_000) :
    i % 9 === 8 ? Number.MAX_SAFE_INTEGER - 10 - pick(1000) : elapsedChoices[i % 9];
  const catchUp = { areaId: state.areaId, fromTurn: 10, toTurn: 10 + elapsedTurns, elapsedTurns };
  const beforeRequest = JSON.stringify(catchUp);
  const result = resolveOverrideCatchUp(state, catchUp);
  const serialized = JSON.stringify(result);
  assert.equal(JSON.stringify(resolveOverrideCatchUp(state, catchUp)), serialized, 'determinismo');
  assert.equal(JSON.stringify(state), originals[i % states.length], 'input state mutado');
  assert.equal(JSON.stringify(catchUp), beforeRequest, 'request mutado');
  assert.equal(result.status, 'OVERRIDE_CATCH_UP_APPLIED');
  assert.equal(result.state.syncedTurn, catchUp.toTurn);
  assert.deepEqual(result.state.entities.map(e => e.id), state.entities.map(e => e.id).sort(lexical), 'orden de entidades');
  assert.equal(result.summary.entitySummaries.length, 128);
  const sourceById = new Map(state.entities.map(e => [e.id, e]));
  const summaryById = new Map(result.summary.entitySummaries.map(s => [s.entityId, s]));
  const updateById = new Map(result.summary.entityUpdates.map(u => [u.entityId, u]));
  assert.equal(summaryById.size, 128);
  assert.equal(updateById.size, result.summary.entityUpdates.length);
  for (const entity of result.state.entities) {
    entitiesProcessed++;
    const original = sourceById.get(entity.id);
    overridesProcessed += original.overrides.length;
    const slots = entity.agenda.slots;
    assert.equal(slots[0].start, 0);
    assert.equal(slots.at(-1).end, entity.agenda.cycleLength);
    for (let j = 1; j < slots.length; j++) assert.equal(slots[j - 1].end, slots[j].start);
    assert.deepEqual(slots.map(s => s.id), [...original.agenda.slots].sort((a, b) => a.start - b.start).map(s => s.id));
    const expected = oraclePosition(catchUp.toTurn, original.agenda, original.overrides);
    assert.deepEqual([entity.logicalRoomId, entity.currentActivity, entity.currentSourceType, entity.currentSourceId],
      [expected.roomId, expected.activity, expected.sourceType, expected.sourceId]);
    const summary = summaryById.get(entity.id);
    assert.equal(summary.baseSlotId, expected.slot.id);
    assert.equal(summary.winningOverrideId, expected.winner?.id ?? null);
    assert.equal(summary.finalSourceId, expected.sourceId);
    assert.equal(summary.remainingOverrides, entity.overrides.length);
    const cycles = BigInt(elapsedTurns) / BigInt(entity.agenda.cycleLength);
    assert.equal(summary.fullCyclesElapsed, Number(cycles));
    fullCyclesCollapsed += cycles;
    const expectedRemaining = original.overrides.filter(o => o.endTurn === null || o.endTurn > catchUp.toTurn)
      .sort((a, b) => a.startTurn - b.startTurn || b.priority - a.priority || lexical(a.id, b.id));
    assert.deepEqual(entity.overrides, expectedRemaining, 'expiración y orden persistente');
    for (const o of entity.overrides) {
      if (o.startTurn > catchUp.toTurn) futureOverridesRemaining++;
      else { assert.ok(o.endTurn === null || o.endTurn > catchUp.toTurn); activeOverridesRemaining++; }
    }
    shadowedOverrides += Math.max(0, expected.activeCount - 1);
    if (expected.winner) overrideFinalStates++; else agendaFinalStates++;
    const visible = original.logicalRoomId !== entity.logicalRoomId || original.currentActivity !== entity.currentActivity;
    const source = original.currentSourceType !== entity.currentSourceType || original.currentSourceId !== entity.currentSourceId;
    if (visible) visibleChanges++;
    if (source) sourceChanges++;
    if (visible || source) {
      const update = updateById.get(entity.id);
      assert.equal(update.visibleChanged, visible);
      assert.equal(update.sourceChanged, source);
      assert.equal(update.sourceId, expected.sourceId);
    } else assert.equal(updateById.has(entity.id), false);
  }
  const expectedExpired = state.entities.flatMap(e => e.overrides.filter(o => o.endTurn !== null && o.endTurn <= catchUp.toTurn)
    .map(o => ({ entityId: e.id, overrideId: o.id, kind: o.kind, priority: o.priority,
      startTurn: o.startTurn, endTurn: o.endTurn })))
    .sort((a, b) => a.endTurn - b.endTurn || lexical(a.entityId, b.entityId) || lexical(a.overrideId, b.overrideId));
  assert.deepEqual(result.summary.expiredOverrides, expectedExpired);
  expiredOverrides += expectedExpired.length;
  if (i % 1000 === 0) {
    const another = resolveOverrideCatchUp(state, catchUp);
    another.state.entities[0].agenda.slots[0].roomId = 'mutated';
    another.state.entities[0].overrides.push({});
    another.summary.entitySummaries.push({});
    assert.equal(JSON.stringify(state), originals[i % states.length], 'output comparte input');
    assert.equal(JSON.stringify(result), serialized, 'outputs separados');
  }
  totalElapsedTurns += BigInt(elapsedTurns);
  maxElapsedTurns = Math.max(maxElapsedTurns, elapsedTurns);
  digest.update(serialized);
  digest.update('\n');
}

console.log(JSON.stringify({ seed, scenarios, entitiesProcessed, overridesProcessed, agendaFinalStates,
  overrideFinalStates, visibleChanges, sourceChanges, expiredOverrides, futureOverridesRemaining,
  activeOverridesRemaining, shadowedOverrides, totalElapsedTurns: totalElapsedTurns.toString(),
  maxElapsedTurns, fullCyclesCollapsed: fullCyclesCollapsed.toString(), digest: digest.digest('hex') }));
