import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { resolveAgendaCatchUp } from './agenda-resolver.mjs';

const seed = Number(process.argv[2] ?? 1337);
if (!Number.isSafeInteger(seed) || seed < 0) throw new TypeError('seed inválida');
let randomState = seed >>> 0;
function random() { randomState = (Math.imul(randomState, 1664525) + 1013904223) >>> 0; return randomState; }
function pick(n) { return random() % n; }
const lexical = (a, b) => a < b ? -1 : a > b ? 1 : 0;
const scenarios = 10_000;
const elapsedChoices = [1, 2, 10, 100, 10_000, 1_000_000, 1_000_000_000];

function oracleSlot(turn, agenda) {
  const phase = Number((BigInt(turn) + BigInt(agenda.offset)) % BigInt(agenda.cycleLength));
  const matches = agenda.slots.filter(slot => slot.start <= phase && phase < slot.end);
  assert.equal(matches.length, 1, 'cada fase pertenece exactamente a un slot');
  return { phase, slot: matches[0] };
}

function fixture(label) {
  const entities = [];
  for (let i = 0; i < 128; i++) {
    const cycleLength = i === 0 ? 1 : 12 + pick(1989);
    const offset = pick(cycleLength);
    const count = i === 0 ? 1 : 1 + pick(12);
    const slots = [];
    let start = 0;
    for (let j = 0; j < count; j++) {
      const remaining = cycleLength - start;
      const left = count - j;
      const length = left === 1 ? remaining : 1 + pick(remaining - left + 1);
      slots.push({ id: `slot_${String(j).padStart(2, '0')}`, start, end: start + length,
        roomId: `room_${j % 5}`, activity: `ACT_${j % 7}` });
      start += length;
    }
    const agenda = { cycleLength, offset, slots: slots.reverse() };
    const initial = oracleSlot(10, agenda).slot;
    entities.push({ id: `npc_${String(i).padStart(3, '0')}`, logicalRoomId: initial.roomId,
      currentActivity: initial.activity, agenda });
  }
  return { version: 1, areaId: `area_${label}`, syncedTurn: 10, entities: entities.reverse() };
}

const states = Array.from({ length: 4 }, (_, i) => fixture(i));
const originals = states.map(state => JSON.stringify(state));
const digest = createHash('sha256');
let entitiesProcessed = 0, visibleChanges = 0, roomChanges = 0, activityChanges = 0;
let totalElapsedTurns = 0n, maxElapsedTurns = 0, fullCyclesCollapsed = 0n, maxFullCyclesCollapsed = 0n;

for (let i = 0; i < scenarios; i++) {
  const state = states[i % states.length];
  const elapsedTurns = i % 9 === 7 ? 1 + pick(1_500_000_000) :
    i % 9 === 8 ? Number.MAX_SAFE_INTEGER - 10 - pick(1000) : elapsedChoices[i % 9];
  const catchUp = { areaId: state.areaId, fromTurn: 10, toTurn: 10 + elapsedTurns, elapsedTurns };
  const beforeRequest = JSON.stringify(catchUp);
  const result = resolveAgendaCatchUp(state, catchUp);
  const serialized = JSON.stringify(result);
  assert.equal(JSON.stringify(resolveAgendaCatchUp(state, catchUp)), serialized, 'determinismo');
  assert.equal(JSON.stringify(state), originals[i % states.length], 'input state mutado');
  assert.equal(JSON.stringify(catchUp), beforeRequest, 'request mutado');
  assert.equal(result.status, 'AGENDA_CATCH_UP_APPLIED');
  assert.equal(result.state.syncedTurn, catchUp.toTurn);
  assert.deepEqual(result.state.entities.map(e => e.id), state.entities.map(e => e.id).sort(lexical), 'orden de entidades');
  assert.equal(result.summary.cycleSummaries.length, 128);
  const sourceById = new Map(state.entities.map(e => [e.id, e]));
  const summaryById = new Map(result.summary.cycleSummaries.map(c => [c.entityId, c]));
  const updateById = new Map(result.summary.entityUpdates.map(u => [u.entityId, u]));
  assert.equal(summaryById.size, 128);
  assert.equal(updateById.size, result.summary.entityUpdates.length);
  for (const entity of result.state.entities) {
    entitiesProcessed++;
    const original = sourceById.get(entity.id);
    const slots = entity.agenda.slots;
    assert.deepEqual(slots.map(s => s.start), [...slots].sort((a, b) => a.start - b.start).map(s => s.start));
    assert.equal(slots[0].start, 0);
    assert.equal(slots.at(-1).end, entity.agenda.cycleLength);
    for (let j = 1; j < slots.length; j++) assert.equal(slots[j - 1].end, slots[j].start, 'sin gaps ni overlaps');
    const expected = oracleSlot(catchUp.toTurn, original.agenda);
    assert.equal(entity.logicalRoomId, expected.slot.roomId);
    assert.equal(entity.currentActivity, expected.slot.activity);
    assert.deepEqual(slots.map(s => s.id), [...original.agenda.slots].sort((a, b) => a.start - b.start).map(s => s.id), 'IDs de slots');
    const cycles = BigInt(elapsedTurns) / BigInt(original.agenda.cycleLength);
    const summary = summaryById.get(entity.id);
    assert.equal(summary.finalPhase, expected.phase);
    assert.equal(summary.toSlotId, expected.slot.id);
    assert.equal(summary.fullCyclesElapsed, Number(cycles));
    fullCyclesCollapsed += cycles;
    if (cycles > maxFullCyclesCollapsed) maxFullCyclesCollapsed = cycles;
    const changedRoom = original.logicalRoomId !== entity.logicalRoomId;
    const changedActivity = original.currentActivity !== entity.currentActivity;
    if (changedRoom || changedActivity) {
      visibleChanges++;
      assert.equal(updateById.get(entity.id).roomId, entity.logicalRoomId);
      assert.equal(updateById.get(entity.id).activity, entity.currentActivity);
    } else assert.equal(updateById.has(entity.id), false);
    if (changedRoom) roomChanges++;
    if (changedActivity) activityChanges++;
  }
  if (i % 1000 === 0) {
    const another = resolveAgendaCatchUp(state, catchUp);
    another.state.entities[0].agenda.slots[0].roomId = 'mutated';
    another.summary.cycleSummaries.push({});
    another.summary.entityUpdates.push({});
    assert.equal(JSON.stringify(state), originals[i % states.length], 'output comparte input');
    assert.equal(JSON.stringify(result), serialized, 'outputs de ejecuciones separados');
  }
  totalElapsedTurns += BigInt(elapsedTurns);
  maxElapsedTurns = Math.max(maxElapsedTurns, elapsedTurns);
  digest.update(serialized);
  digest.update('\n');
}

console.log(JSON.stringify({ seed, scenarios, entitiesProcessed, visibleChanges, roomChanges, activityChanges,
  totalElapsedTurns: totalElapsedTurns.toString(), maxElapsedTurns,
  fullCyclesCollapsed: fullCyclesCollapsed.toString(), maxFullCyclesCollapsed: maxFullCyclesCollapsed.toString(),
  digest: digest.digest('hex') }));
