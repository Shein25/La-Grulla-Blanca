import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveAgendaCatchUp as resolve } from './agenda-resolver.mjs';
import { standardSlots, standardEntity, makeState as state, makeCatchUp as request, variedEntities } from './fixtures.mjs';

const run = (s = state(), r = request()) => resolve(s, r);
const at = (fromTurn, toTurn) => ({ areaId: 'area_alpha', fromTurn, toTurn, elapsedTurns: toTurn - fromTurn });
const throws = (s, r = request()) => assert.throws(() => run(s, r), TypeError);
const one = (s = state(), r = request()) => run(s, r).state.entities[0];
const clone = value => structuredClone(value);

test('estructura, status y syncedTurn', () => { const x = run(); assert.equal(x.status, 'AGENDA_CATCH_UP_APPLIED'); assert.equal(x.state.syncedTurn, 30); assert.equal(x.state.version, 1); });
test('Golden A mismo slot sin cambio visible', () => { const x = run(state(), at(10, 15)); assert.equal(x.state.entities[0].currentActivity, 'REST'); assert.equal(x.summary.entityUpdates.length, 0); assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, 0); });
test('Golden B cambio de slot', () => { const x = run(); assert.equal(x.state.entities[0].currentActivity, 'TRAIN'); assert.equal(x.state.entities[0].logicalRoomId, 'room_training'); assert.deepEqual(x.summary.entityUpdates[0], { entityId: 'npc_a', fromSlotId: 'rest', toSlotId: 'train', previousRoomId: 'room_dormitory', roomId: 'room_training', previousActivity: 'REST', activity: 'TRAIN', finalPhase: 30, fullCyclesElapsed: 0 }); });
test('Golden C boundary exacto', () => { const x = run(state(), at(10, 20)); assert.equal(x.summary.entityUpdates[0].toSlotId, 'train'); assert.equal(x.summary.entityUpdates[0].finalPhase, 20); });
test('Golden D ciclo completo sin cambio visible', () => { const x = run(state(), at(10, 110)); assert.equal(x.summary.entityUpdates.length, 0); assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, 1); assert.equal(x.summary.elapsedTurns, 100); });
test('Golden E muchos ciclos y remainder', () => { const x = run(state(), at(10, 12_165)); assert.equal(x.state.entities[0].currentActivity, 'STUDY'); assert.equal(x.summary.entityUpdates[0].finalPhase, 65); assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, 121); });
test('Golden F offset cambia resultado', () => { const s = state({ entities: [standardEntity('npc_b', 25), standardEntity('npc_a', 0)] }); const x = run(s); assert.deepEqual(x.state.entities.map(e => e.currentActivity), ['TRAIN', 'TRAIN']); const y = run(s, at(10, 65)); assert.deepEqual(y.state.entities.map(e => e.currentActivity), ['STUDY', 'EAT']); });
test('Golden G huge elapsed hasta MAX_SAFE_INTEGER', () => { const max = Number.MAX_SAFE_INTEGER; const x = run(state(), at(10, max)); const phase = Number(BigInt(max) % 100n); assert.equal(x.summary.cycleSummaries[0].finalPhase, phase); assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, Number(BigInt(max - 10) / 100n)); });
test('Golden H múltiples NPC diferentes', () => { const s = state({ entities: variedEntities() }); const x = run(s, at(10, 25)); assert.deepEqual(x.state.entities.map(e => e.id), ['npc_fixed', 'npc_guard', 'npc_scholar', 'npc_worker']); assert.deepEqual(x.state.entities.map(e => e.currentActivity), ['WORK', 'GUARD', 'EAT', 'WORK']); assert.equal(x.summary.cycleSummaries.length, 4); });
test('un solo slot permite elapsed enorme sin update', () => { const s = state({ entities: [variedEntities().find(e => e.id === 'npc_fixed')] }); const x = run(s, at(10, Number.MAX_SAFE_INTEGER)); assert.equal(x.summary.entityUpdates.length, 0); assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, Number(BigInt(Number.MAX_SAFE_INTEGER - 10) / 100n)); });
test('entidades vacías', () => { const x = run(state({ entities: [] })); assert.deepEqual(x.state.entities, []); assert.deepEqual(x.summary.cycleSummaries, []); });
test('slot input desordenado se canonicaliza', () => { const e = standardEntity(); e.agenda.slots.reverse(); assert.deepEqual(one(state({ entities: [e] })).agenda.slots.map(s => s.id), ['rest', 'train', 'study', 'meal']); });
test('entidades se ordenan sin locale', () => { const e = ['中', 'é', 'A'].map(id => standardEntity(id)); assert.deepEqual(run(state({ entities: e })).state.entities.map(x => x.id), ['A', 'é', '中']); });
test('offset en boundary inicial es consistente', () => { const e = standardEntity('b', 10); assert.equal(e.currentActivity, 'TRAIN'); assert.equal(one(state({ entities: [e] })).currentActivity, 'TRAIN'); });
test('intervalo [start,end) selecciona último slot', () => { const x = run(state(), at(10, 80)); assert.equal(x.state.entities[0].currentActivity, 'EAT'); });
test('offset + turn usa BigInt sin overflow', () => { const max = Number.MAX_SAFE_INTEGER; const e = { id: 'e', logicalRoomId: 'r', currentActivity: 'A', agenda: { cycleLength: max, offset: max - 1, slots: [{ id: 'a', start: 0, end: max, roomId: 'r', activity: 'A' }] } }; const x = run(state({ syncedTurn: max - 1, entities: [e] }), at(max - 1, max)); assert.equal(x.summary.cycleSummaries[0].finalPhase, Number((BigInt(max) + BigInt(max - 1)) % BigInt(max))); });
test('visible room change solo', () => { const e = standardEntity(); e.agenda.slots[1].activity = 'REST'; const x = run(state({ entities: [e] })); assert.equal(x.summary.entityUpdates.length, 1); assert.equal(x.summary.entityUpdates[0].previousActivity, x.summary.entityUpdates[0].activity); });
test('visible activity change solo', () => { const e = standardEntity(); e.agenda.slots[1].roomId = 'room_dormitory'; const x = run(state({ entities: [e] })); assert.equal(x.summary.entityUpdates.length, 1); assert.equal(x.summary.entityUpdates[0].previousRoomId, x.summary.entityUpdates[0].roomId); });
test('slot cambia pero estado visible igual: sin update', () => { const e = standardEntity(); e.agenda.slots[1].roomId = 'room_dormitory'; e.agenda.slots[1].activity = 'REST'; const x = run(state({ entities: [e] })); assert.equal(x.summary.entityUpdates.length, 0); assert.equal(x.summary.cycleSummaries[0].toSlotId, 'train'); });
test('fullCyclesElapsed usa división exacta', () => { const max = Number.MAX_SAFE_INTEGER; const e = { id: 'e', logicalRoomId: 'r', currentActivity: 'A', agenda: { cycleLength: 3, offset: 0, slots: [{ id: 'a', start: 0, end: 3, roomId: 'r', activity: 'A' }] } }; const x = run(state({ entities: [e] }), at(10, max)); assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, Number(BigInt(max - 10) / 3n)); });
test('summary ordenado por entity.id', () => { const x = run(state({ entities: [standardEntity('z'), standardEntity('a')] })); assert.deepEqual(x.summary.entityUpdates.map(u => u.entityId), ['a', 'z']); assert.deepEqual(x.summary.cycleSummaries.map(u => u.entityId), ['a', 'z']); });
test('input intacto', () => { const s = state({ entities: [standardEntity('z'), standardEntity('a')] }); const r = request(); const before = clone([s, r]); run(s, r); assert.deepEqual([s, r], before); });
test('input congelado funciona', () => { const s = state(); const e = s.entities[0]; for (const slot of e.agenda.slots) Object.freeze(slot); Object.freeze(e.agenda.slots); Object.freeze(e.agenda); Object.freeze(e); Object.freeze(s.entities); Object.freeze(s); assert.equal(run(s).state.entities[0].currentActivity, 'TRAIN'); });
test('output desacoplado de input y otras ejecuciones', () => { const s = state(); const first = run(s), second = run(s); first.state.entities[0].agenda.slots[0].id = 'changed'; first.state.entities[0].logicalRoomId = 'changed'; first.summary.entityUpdates[0].roomId = 'changed'; first.summary.cycleSummaries.push({}); assert.deepEqual(second, run(s)); assert.equal(s.entities[0].agenda.slots[0].id, 'rest'); });
test('agendas idénticas no comparten referencias de output', () => { const x = run(state({ entities: [standardEntity('a'), standardEntity('b')] })); x.state.entities[0].agenda.slots[0].roomId = 'changed'; assert.equal(x.state.entities[1].agenda.slots[0].roomId, 'room_dormitory'); });
test('determinismo', () => assert.deepEqual(run(), run()));

const invalid = [
  ['state null', () => [null]], ['state array', () => [[]]], ['version', () => [state({ version: 2 })]],
  ['areaId vacío', () => [state({ areaId: '' })]], ['areaId espacios', () => [state({ areaId: '  ' })]],
  ['syncedTurn negativo', () => [state({ syncedTurn: -1 })]], ['syncedTurn float', () => [state({ syncedTurn: 1.5 })]],
  ['state extra', () => [{ ...state(), extra: 1 }]], ['state symbol', () => [Object.assign(state(), { [Symbol('x')]: 1 })]],
  ['state herencia', () => [Object.assign(Object.create({ x: 1 }), state())]],
  ['entities no array', () => [state({ entities: {} })]], ['entities hole', () => [state({ entities: Array(1) })]],
  ['entity no plana', () => [state({ entities: [Object.assign(Object.create({ x: 1 }), standardEntity())] })]],
  ['entity id vacío', () => [state({ entities: [standardEntity(' ')] })]],
  ['entity duplicada', () => [state({ entities: [standardEntity(), standardEntity()] })]],
  ['entity extra', () => [state({ entities: [{ ...standardEntity(), extra: 1 }] })]],
  ['logicalRoomId blanco', () => [state({ entities: [{ ...standardEntity(), logicalRoomId: ' ' }] })]],
  ['currentActivity blanca', () => [state({ entities: [{ ...standardEntity(), currentActivity: ' ' }] })]],
  ['agenda faltante', () => [state({ entities: [{ ...standardEntity(), agenda: undefined }] })]],
  ['agenda extra', () => { const e = standardEntity(); e.agenda.extra = 1; return [state({ entities: [e] })]; }],
  ['agenda herencia', () => { const e = standardEntity(); e.agenda = Object.assign(Object.create({ x: 1 }), e.agenda); return [state({ entities: [e] })]; }],
  ['cycleLength cero', () => { const e = standardEntity(); e.agenda.cycleLength = 0; return [state({ entities: [e] })]; }],
  ['cycleLength unsafe', () => { const e = standardEntity(); e.agenda.cycleLength = Number.MAX_SAFE_INTEGER + 1; return [state({ entities: [e] })]; }],
  ['offset negativo', () => { const e = standardEntity(); e.agenda.offset = -1; return [state({ entities: [e] })]; }],
  ['offset igual al ciclo', () => { const e = standardEntity(); e.agenda.offset = 100; return [state({ entities: [e] })]; }],
  ['offset float', () => { const e = standardEntity(); e.agenda.offset = 0.5; return [state({ entities: [e] })]; }],
  ['slots vacío', () => { const e = standardEntity(); e.agenda.slots = []; return [state({ entities: [e] })]; }],
  ['slots hole', () => { const e = standardEntity(); e.agenda.slots = Array(1); return [state({ entities: [e] })]; }],
  ['slots no array', () => { const e = standardEntity(); e.agenda.slots = {}; return [state({ entities: [e] })]; }],
  ['slot extra', () => { const e = standardEntity(); e.agenda.slots[0].extra = 1; return [state({ entities: [e] })]; }],
  ['slot Symbol', () => { const e = standardEntity(); e.agenda.slots[0][Symbol('x')] = 1; return [state({ entities: [e] })]; }],
  ['slot herencia', () => { const e = standardEntity(); e.agenda.slots[0] = Object.assign(Object.create({ x: 1 }), e.agenda.slots[0]); return [state({ entities: [e] })]; }],
  ['slot id blanco', () => { const e = standardEntity(); e.agenda.slots[0].id = ' '; return [state({ entities: [e] })]; }],
  ['slot id duplicado', () => { const e = standardEntity(); e.agenda.slots[1].id = 'rest'; return [state({ entities: [e] })]; }],
  ['slot room blanco', () => { const e = standardEntity(); e.agenda.slots[1].roomId = ' '; return [state({ entities: [e] })]; }],
  ['slot activity blanco', () => { const e = standardEntity(); e.agenda.slots[1].activity = ' '; return [state({ entities: [e] })]; }],
  ['slot start negativo', () => { const e = standardEntity(); e.agenda.slots[0].start = -1; return [state({ entities: [e] })]; }],
  ['slot end <= start', () => { const e = standardEntity(); e.agenda.slots[0].end = 0; return [state({ entities: [e] })]; }],
  ['slot end > cycle', () => { const e = standardEntity(); e.agenda.slots[3].end = 101; return [state({ entities: [e] })]; }],
  ['slot start NaN', () => { const e = standardEntity(); e.agenda.slots[0].start = NaN; return [state({ entities: [e] })]; }],
  ['slot end Infinity', () => { const e = standardEntity(); e.agenda.slots[0].end = Infinity; return [state({ entities: [e] })]; }],
  ['gap', () => { const e = standardEntity(); e.agenda.slots[1].start = 21; return [state({ entities: [e] })]; }],
  ['overlap', () => { const e = standardEntity(); e.agenda.slots[1].start = 19; return [state({ entities: [e] })]; }],
  ['no empieza en cero', () => { const e = standardEntity(); e.agenda.slots[0].start = 1; return [state({ entities: [e] })]; }],
  ['no termina en cycleLength', () => { const e = standardEntity(); e.agenda.slots[3].end = 99; return [state({ entities: [e] })]; }],
  ['snapshot room inconsistente', () => { const e = standardEntity(); e.logicalRoomId = 'room_training'; return [state({ entities: [e] })]; }],
  ['snapshot activity inconsistente', () => { const e = standardEntity(); e.currentActivity = 'TRAIN'; return [state({ entities: [e] })]; }],
  ['request area distinta', () => [state(), request({ areaId: 'other' })]],
  ['request from distinto', () => [state(), request({ fromTurn: 11 })]],
  ['request elapsed incorrecto', () => [state(), request({ elapsedTurns: 21 })]],
  ['request cero', () => [state(), request({ toTurn: 10, elapsedTurns: 0 })]],
  ['request regresivo', () => [state(), request({ toTurn: 9, elapsedTurns: 1 })]],
  ['request unsafe', () => [state(), request({ toTurn: Number.MAX_SAFE_INTEGER + 1 })]],
  ['request extra', () => [state(), { ...request(), extra: 1 }]],
  ['request Symbol', () => [state(), Object.assign(request(), { [Symbol('x')]: 1 })]],
  ['request herencia', () => [state(), Object.assign(Object.create({ x: 1 }), request())]],
];
for (const [name, make] of invalid) test(`rechaza ${name}`, () => throws(...make()));

function accessor(object, key, descriptor = { get() { throw Error('getter ejecutado'); }, enumerable: true, configurable: true }) { Object.defineProperty(object, key, descriptor); return object; }
test('state getter no ejecutado', () => throws(accessor(state(), 'areaId')));
test('request getter no ejecutado', () => throws(state(), accessor(request(), 'fromTurn')));
test('request setter-only rechazado', () => throws(state(), accessor(request(), 'areaId', { set(_) { throw Error('setter ejecutado'); }, enumerable: true, configurable: true })));
test('entity getter no ejecutado', () => throws(state({ entities: [accessor(standardEntity(), 'id')] })));
test('agenda getter no ejecutado', () => { const e = standardEntity(); accessor(e.agenda, 'cycleLength'); throws(state({ entities: [e] })); });
test('slot getter no ejecutado', () => { const e = standardEntity(); accessor(e.agenda.slots[0], 'roomId'); throws(state({ entities: [e] })); });
test('entities accessor index', () => { const a = [standardEntity()]; accessor(a, '0'); throws(state({ entities: a })); });
test('slots accessor index', () => { const e = standardEntity(); accessor(e.agenda.slots, '0'); throws(state({ entities: [e] })); });
test('array Symbol', () => { const a = [standardEntity()]; a[Symbol('x')] = 1; throws(state({ entities: a })); });
test('Proxy state hostil', () => throws(new Proxy(state(), { ownKeys() { throw Error('trap'); } })));
test('Proxy agenda hostil', () => { const e = standardEntity(); e.agenda = new Proxy(e.agenda, { getOwnPropertyDescriptor() { throw Error('trap'); } }); throws(state({ entities: [e] })); });
test('Proxy slots hostil', () => { const e = standardEntity(); e.agenda.slots = new Proxy(e.agenda.slots, { getPrototypeOf() { throw Error('trap'); } }); throws(state({ entities: [e] })); });

test('oracle independiente BigInt: turns, offsets y ciclos aleatorios', () => {
  let seed = 42;
  const random = () => (seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0);
  for (let i = 0; i < 1000; i++) {
    const cycleLength = 1 + random() % 1000;
    const offset = random() % cycleLength;
    const cut = cycleLength === 1 ? 1 : 1 + random() % (cycleLength - 1);
    const slots = cycleLength === 1 ? [{ id: 'a', start: 0, end: 1, roomId: 'r_a', activity: 'A' }] :
      [{ id: 'a', start: 0, end: cut, roomId: 'r_a', activity: 'A' }, { id: 'b', start: cut, end: cycleLength, roomId: 'r_b', activity: 'B' }];
    const fromTurn = random() % 1_000_000;
    const toTurn = i % 4 === 0 ? Number.MAX_SAFE_INTEGER : fromTurn + 1 + random() % 1_000_000_000;
    const fromPhase = Number((BigInt(fromTurn) + BigInt(offset)) % BigInt(cycleLength));
    const initial = slots.filter(s => s.start <= fromPhase && fromPhase < s.end)[0];
    const e = { id: 'e', logicalRoomId: initial.roomId, currentActivity: initial.activity, agenda: { cycleLength, offset, slots } };
    const x = run(state({ syncedTurn: fromTurn, entities: [e] }), at(fromTurn, toTurn));
    const finalPhase = Number((BigInt(toTurn) + BigInt(offset)) % BigInt(cycleLength));
    const expected = slots.filter(s => s.start <= finalPhase && finalPhase < s.end)[0];
    assert.equal(x.state.entities[0].currentActivity, expected.activity);
    assert.equal(x.state.entities[0].logicalRoomId, expected.roomId);
    assert.equal(x.summary.cycleSummaries[0].finalPhase, finalPhase);
    assert.equal(x.summary.cycleSummaries[0].fullCyclesElapsed, Number(BigInt(toTurn - fromTurn) / BigInt(cycleLength)));
  }
});
