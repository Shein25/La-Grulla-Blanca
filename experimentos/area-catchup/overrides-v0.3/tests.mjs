import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveOverrideCatchUp as resolve } from './override-resolver.mjs';
import { makeState as state, makeCatchUp as request, makeEntity as entity, makeOverride as override, entityAt } from './fixtures.mjs';

const run = (s = state(), r = request()) => resolve(s, r);
const at = (fromTurn, toTurn) => ({ areaId: 'area_alpha', fromTurn, toTurn, elapsedTurns: toTurn - fromTurn });
const throws = (s, r = request()) => assert.throws(() => run(s, r), TypeError);
const clone = value => structuredClone(value);

test('estructura, status y syncedTurn final', () => { const x = run(); assert.equal(x.status, 'OVERRIDE_CATCH_UP_APPLIED'); assert.equal(x.state.syncedTurn, 30); assert.equal(x.summary.entitySummaries.length, 1); });
test('Golden A sin override: agenda REST a TRAIN', () => { const x = run(); assert.deepEqual([x.state.entities[0].currentSourceType, x.state.entities[0].currentSourceId, x.state.entities[0].currentActivity], ['AGENDA', 'train', 'TRAIN']); assert.equal(x.summary.entityUpdates.length, 1); });
test('Golden B override empieza durante dormancia', () => { const x = run(state({ entities: [entity({ overrides: [override()] })] })); assert.deepEqual([x.state.entities[0].currentSourceType, x.state.entities[0].currentSourceId, x.state.entities[0].logicalRoomId, x.state.entities[0].currentActivity], ['OVERRIDE', 'medical', 'room_infirmary', 'RECOVER']); });
test('Golden C override expira y vuelve a agenda actual', () => { const x = run(state({ entities: [entity({ overrides: [override({ endTurn: 50 })] })] }), at(10, 80)); assert.equal(x.state.entities[0].currentSourceType, 'AGENDA'); assert.equal(x.state.entities[0].currentSourceId, 'meal'); assert.equal(x.state.entities[0].overrides.length, 0); assert.deepEqual(x.summary.expiredOverrides.map(o => o.overrideId), ['medical']); });
test('Golden D start boundary activo', () => { const x = run(state({ entities: [entity({ overrides: [override({ startTurn: 30 })] })] })); assert.equal(x.state.entities[0].currentSourceId, 'medical'); });
test('Golden E end boundary inactivo', () => { const x = run(state({ entities: [entity({ overrides: [override({ endTurn: 30 })] })] })); assert.equal(x.state.entities[0].currentSourceType, 'AGENDA'); assert.equal(x.summary.expiredOverrides.length, 1); });
test('Golden F mayor prioridad gana', () => { const a = override({ id: 'a', priority: 100, roomId: 'r_a' }); const b = override({ id: 'b', priority: 200, roomId: 'r_b' }); assert.equal(run(state({ entities: [entity({ overrides: [a, b] })] })).state.entities[0].currentSourceId, 'b'); });
test('Golden G empate por inicio más reciente', () => { const a = override({ id: 'a', startTurn: 20 }); const b = override({ id: 'b', startTurn: 25 }); assert.equal(run(state({ entities: [entity({ overrides: [a, b] })] })).state.entities[0].currentSourceId, 'b'); });
test('Golden G empate por ID lexicográfico', () => { const a = override({ id: 'a' }); const b = override({ id: 'b' }); assert.equal(run(state({ entities: [entity({ overrides: [b, a] })] })).state.entities[0].currentSourceId, 'a'); });
test('Golden H override ya activo en snapshot', () => { const o = override({ startTurn: 20, endTurn: 100 }); const s = state({ syncedTurn: 50, entities: [entityAt(50, [o])] }); const x = run(s, at(50, 70)); assert.equal(x.state.entities[0].currentSourceType, 'OVERRIDE'); assert.equal(x.state.entities[0].currentSourceId, 'medical'); });
test('Golden I override indefinido', () => { const x = run(state({ entities: [entity({ overrides: [override({ endTurn: null })] })] }), at(10, Number.MAX_SAFE_INTEGER)); assert.equal(x.state.entities[0].currentSourceId, 'medical'); assert.equal(x.state.entities[0].overrides.length, 1); });
test('Golden J mismo aspecto pero source distinto', () => { const o = override({ startTurn: 30, roomId: 'room_training', activity: 'TRAIN' }); const e = entity({ logicalRoomId: 'room_training', currentActivity: 'TRAIN', currentSourceId: 'train', overrides: [o] }); const x = run(state({ syncedTurn: 25, entities: [e] }), at(25, 30)); assert.equal(x.summary.entityUpdates[0].visibleChanged, false); assert.equal(x.summary.entityUpdates[0].sourceChanged, true); assert.equal(x.state.entities[0].currentSourceType, 'OVERRIDE'); });
test('Golden K override sombreado expira igualmente', () => { const a = override({ id: 'a', priority: 100, endTurn: 40 }); const b = override({ id: 'b', priority: 200, endTurn: 100 }); const x = run(state({ entities: [entity({ overrides: [a, b] })] }), at(10, 50)); assert.equal(x.state.entities[0].currentSourceId, 'b'); assert.deepEqual(x.summary.expiredOverrides.map(o => o.overrideId), ['a']); });
test('Golden L huge elapsed: activo, futuro y expirado', () => { const max = Number.MAX_SAFE_INTEGER; const a = override({ id: 'active', endTurn: null, priority: 100 }); const b = override({ id: 'future', startTurn: max, endTurn: null }); const c = override({ id: 'expired', endTurn: 40 }); const x = run(state({ entities: [entity({ overrides: [a, b, c] })] }), at(10, max - 1)); assert.equal(x.state.entities[0].currentSourceId, 'active'); assert.deepEqual(x.state.entities[0].overrides.map(o => o.id), ['active', 'future']); assert.deepEqual(x.summary.expiredOverrides.map(o => o.overrideId), ['expired']); assert.equal(x.summary.entitySummaries[0].fullCyclesElapsed, Number(BigInt(max - 11) / 100n)); });
test('kind es metadata sin semántica mágica', () => { const o = override({ kind: 'ALARM', roomId: 'room_x', activity: 'WAIT' }); const x = run(state({ entities: [entity({ overrides: [o] })] })); assert.equal(x.state.entities[0].logicalRoomId, 'room_x'); assert.equal(x.state.entities[0].currentActivity, 'WAIT'); });
test('override futuro permanece', () => { const x = run(state({ entities: [entity({ overrides: [override({ startTurn: 80 })] })] })); assert.equal(x.state.entities[0].currentSourceType, 'AGENDA'); assert.equal(x.state.entities[0].overrides.length, 1); });
test('overrides solapados válidos', () => { const a = override({ id: 'a', startTurn: 20, endTurn: 300 }); const b = override({ id: 'b', startTurn: 200, endTurn: 400 }); const x = run(state({ entities: [entity({ overrides: [a, b] })] }), at(10, 250)); assert.equal(x.state.entities[0].currentSourceId, 'b'); });
test('priority MAX_SAFE_INTEGER válido', () => { const x = run(state({ entities: [entity({ overrides: [override({ priority: Number.MAX_SAFE_INTEGER })] })] })); assert.equal(x.state.entities[0].currentSourceId, 'medical'); });
test('expirados ordenados por endTurn, entityId, overrideId', () => { const ea = entity({ id: 'a', overrides: [override({ id: 'z', endTurn: 50 }), override({ id: 'a', endTurn: 40 })] }); const eb = entity({ id: 'b', overrides: [override({ id: 'b', endTurn: 40 })] }); const x = run(state({ entities: [eb, ea] }), at(10, 60)); assert.deepEqual(x.summary.expiredOverrides.map(o => [o.endTurn, o.entityId, o.overrideId]), [[40, 'a', 'a'], [40, 'b', 'b'], [50, 'a', 'z']]); });
test('overrides persistentes ordenados por start, prioridad desc, ID', () => { const os = [override({ id: 'z', startTurn: 50, priority: 1 }), override({ id: 'b', startTurn: 20, priority: 2 }), override({ id: 'a', startTurn: 20, priority: 2 }), override({ id: 'c', startTurn: 20, priority: 3 })]; const x = run(state({ entities: [entity({ overrides: os })] })); assert.deepEqual(x.state.entities[0].overrides.map(o => o.id), ['c', 'a', 'b', 'z']); });
test('orden del input no decide el ganador', () => { const a = override({ id: 'a', priority: 200 }); const b = override({ id: 'b', priority: 100 }); const s1 = state({ entities: [entity({ overrides: [a, b] })] }); const s2 = state({ entities: [entity({ overrides: [b, a] })] }); assert.deepEqual(run(s1), run(s2)); });
test('summary para cada entidad sin cambio visible', () => { const x = run(state(), at(10, 110)); assert.equal(x.summary.entityUpdates.length, 0); assert.equal(x.summary.entitySummaries[0].fullCyclesElapsed, 1); assert.equal(x.summary.entitySummaries[0].finalSourceId, 'rest'); });
test('array entities vacío', () => { const x = run(state({ entities: [] })); assert.deepEqual(x.state.entities, []); assert.deepEqual(x.summary.entitySummaries, []); });
test('un solo slot', () => { const e = entity({ agenda: { cycleLength: 1, offset: 0, slots: [{ id: 'always', start: 0, end: 1, roomId: 'r', activity: 'A' }] }, logicalRoomId: 'r', currentActivity: 'A', currentSourceId: 'always' }); const x = run(state({ entities: [e] }), at(10, Number.MAX_SAFE_INTEGER)); assert.equal(x.summary.entityUpdates.length, 0); assert.equal(x.summary.entitySummaries[0].fullCyclesElapsed, Number.MAX_SAFE_INTEGER - 10); });
test('BigInt turn + offset sin overflow', () => { const max = Number.MAX_SAFE_INTEGER; const e = entity({ agenda: { cycleLength: max, offset: max - 1, slots: [{ id: 'all', start: 0, end: max, roomId: 'r', activity: 'A' }] }, logicalRoomId: 'r', currentActivity: 'A', currentSourceId: 'all' }); assert.equal(run(state({ syncedTurn: max - 1, entities: [e] }), at(max - 1, max)).state.entities[0].currentSourceId, 'all'); });
test('entidades y slots canónicos', () => { const a = entity({ id: 'z' }); a.agenda.slots.reverse(); const b = entity({ id: 'a' }); const x = run(state({ entities: [a, b] })); assert.deepEqual(x.state.entities.map(e => e.id), ['a', 'z']); assert.deepEqual(x.state.entities[1].agenda.slots.map(s => s.id), ['rest', 'train', 'study', 'meal']); });
test('Unicode IDs ordenados sin locale', () => { const x = run(state({ entities: ['中', 'é', 'A'].map(id => entity({ id })) })); assert.deepEqual(x.state.entities.map(e => e.id), ['A', 'é', '中']); });
test('inputs intactos', () => { const s = state({ entities: [entity({ overrides: [override()] })] }); const r = request(); const before = clone([s, r]); run(s, r); assert.deepEqual([s, r], before); });
test('inputs congelados funcionan', () => { const s = state({ entities: [entity({ overrides: [override()] })] }); const e = s.entities[0]; for (const slot of e.agenda.slots) Object.freeze(slot); Object.freeze(e.agenda.slots); Object.freeze(e.agenda); Object.freeze(e.overrides[0]); Object.freeze(e.overrides); Object.freeze(e); Object.freeze(s.entities); Object.freeze(s); assert.equal(run(s).state.entities[0].currentSourceId, 'medical'); });
test('outputs desacoplados de input y otras ejecuciones', () => { const s = state({ entities: [entity({ overrides: [override({ endTurn: 25 })] })] }); const a = run(s), b = run(s); a.state.entities[0].agenda.slots[0].id = 'changed'; a.summary.expiredOverrides[0].overrideId = 'changed'; a.summary.entityUpdates.push({}); a.summary.entitySummaries[0].remainingOverrides = 999; assert.deepEqual(b, run(s)); assert.equal(s.entities[0].overrides[0].id, 'medical'); });
test('agendas y overrides no se comparten entre entidades', () => { const x = run(state({ entities: [entity({ id: 'a', overrides: [override()] }), entity({ id: 'b', overrides: [override()] })] })); x.state.entities[0].agenda.slots[0].id = 'changed'; x.state.entities[0].overrides[0].id = 'changed'; assert.equal(x.state.entities[1].agenda.slots[0].id, 'rest'); assert.equal(x.state.entities[1].overrides[0].id, 'medical'); });
test('determinismo', () => assert.deepEqual(run(), run()));

const invalid = [
  ['state null', () => [null]], ['state array', () => [[]]], ['version', () => [state({ version: 2 })]],
  ['areaId vacío', () => [state({ areaId: ' ' })]], ['syncedTurn negativo', () => [state({ syncedTurn: -1 })]],
  ['syncedTurn float', () => [state({ syncedTurn: 1.5 })]], ['state extra', () => [{ ...state(), extra: 1 }]],
  ['state Symbol', () => [Object.assign(state(), { [Symbol('x')]: 1 })]],
  ['state herencia', () => [Object.assign(Object.create({ x: 1 }), state())]],
  ['entities no array', () => [state({ entities: {} })]], ['entities hole', () => [state({ entities: Array(1) })]],
  ['entity no plana', () => [state({ entities: [Object.assign(Object.create({ x: 1 }), entity())] })]],
  ['entity ID blanco', () => [state({ entities: [entity({ id: ' ' })] })]],
  ['entity duplicada', () => [state({ entities: [entity(), entity()] })]],
  ['entity extra', () => [state({ entities: [{ ...entity(), extra: 1 }] })]],
  ['currentSourceType inválido', () => [state({ entities: [entity({ currentSourceType: 'OTHER' })] })]],
  ['sourceId inexistente', () => [state({ entities: [entity({ currentSourceId: 'missing' })] })]],
  ['source AGENDA pero override gana', () => [state({ entities: [entity({ overrides: [override({ startTurn: 0 })] })] })]],
  ['source OVERRIDE no activo', () => [state({ entities: [entity({ currentSourceType: 'OVERRIDE', currentSourceId: 'medical', overrides: [override()] })] })]],
  ['room contradice source', () => [state({ entities: [entity({ logicalRoomId: 'room_other' })] })]],
  ['activity contradice source', () => [state({ entities: [entity({ currentActivity: 'OTHER' })] })]],
  ['agenda no plana', () => { const e = entity(); e.agenda = Object.assign(Object.create({ x: 1 }), e.agenda); return [state({ entities: [e] })]; }],
  ['agenda extra', () => { const e = entity(); e.agenda.extra = 1; return [state({ entities: [e] })]; }],
  ['cycleLength cero', () => { const e = entity(); e.agenda.cycleLength = 0; return [state({ entities: [e] })]; }],
  ['offset igual al ciclo', () => { const e = entity(); e.agenda.offset = 100; return [state({ entities: [e] })]; }],
  ['slots vacío', () => { const e = entity(); e.agenda.slots = []; return [state({ entities: [e] })]; }],
  ['slots hole', () => { const e = entity(); e.agenda.slots = Array(1); return [state({ entities: [e] })]; }],
  ['slot extra', () => { const e = entity(); e.agenda.slots[0].extra = 1; return [state({ entities: [e] })]; }],
  ['slot ID duplicado', () => { const e = entity(); e.agenda.slots[1].id = 'rest'; return [state({ entities: [e] })]; }],
  ['slot gaps', () => { const e = entity(); e.agenda.slots[1].start = 21; return [state({ entities: [e] })]; }],
  ['slot overlaps', () => { const e = entity(); e.agenda.slots[1].start = 19; return [state({ entities: [e] })]; }],
  ['slot fuera de rango', () => { const e = entity(); e.agenda.slots[3].end = 101; return [state({ entities: [e] })]; }],
  ['overrides no array', () => [state({ entities: [entity({ overrides: {} })] })]],
  ['overrides hole', () => [state({ entities: [entity({ overrides: Array(1) })] })]],
  ['override no plano', () => [state({ entities: [entity({ overrides: [Object.assign(Object.create({ x: 1 }), override())] })] })]],
  ['override ID duplicado', () => [state({ entities: [entity({ overrides: [override(), override()] })] })]],
  ['override ID blanco', () => [state({ entities: [entity({ overrides: [override({ id: '  ' })] })] })]],
  ['override kind blanco', () => [state({ entities: [entity({ overrides: [override({ kind: ' ' })] })] })]],
  ['override room blanco', () => [state({ entities: [entity({ overrides: [override({ roomId: ' ' })] })] })]],
  ['override activity blanco', () => [state({ entities: [entity({ overrides: [override({ activity: ' ' })] })] })]],
  ['override extra', () => [state({ entities: [entity({ overrides: [{ ...override(), extra: 1 }] })] })]],
  ['override Symbol', () => [state({ entities: [entity({ overrides: [Object.assign(override(), { [Symbol('x')]: 1 })] })] })]],
  ['priority negativo', () => [state({ entities: [entity({ overrides: [override({ priority: -1 })] })] })]],
  ['priority float', () => [state({ entities: [entity({ overrides: [override({ priority: 1.5 })] })] })]],
  ['priority NaN', () => [state({ entities: [entity({ overrides: [override({ priority: NaN })] })] })]],
  ['priority Infinity', () => [state({ entities: [entity({ overrides: [override({ priority: Infinity })] })] })]],
  ['priority unsafe', () => [state({ entities: [entity({ overrides: [override({ priority: Number.MAX_SAFE_INTEGER + 1 })] })] })]],
  ['startTurn negativo', () => [state({ entities: [entity({ overrides: [override({ startTurn: -1 })] })] })]],
  ['startTurn float', () => [state({ entities: [entity({ overrides: [override({ startTurn: 1.5 })] })] })]],
  ['endTurn <= startTurn', () => [state({ entities: [entity({ overrides: [override({ endTurn: 20 })] })] })]],
  ['endTurn stale', () => [state({ entities: [entity({ overrides: [override({ startTurn: 0, endTurn: 10 })] })] })]],
  ['endTurn NaN', () => [state({ entities: [entity({ overrides: [override({ endTurn: NaN })] })] })]],
  ['endTurn Infinity', () => [state({ entities: [entity({ overrides: [override({ endTurn: Infinity })] })] })]],
  ['endTurn unsafe', () => [state({ entities: [entity({ overrides: [override({ endTurn: Number.MAX_SAFE_INTEGER + 1 })] })] })]],
  ['request area', () => [state(), request({ areaId: 'other' })]],
  ['request from', () => [state(), request({ fromTurn: 11 })]],
  ['request elapsed', () => [state(), request({ elapsedTurns: 21 })]],
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
test('setter-only rechazado', () => throws(state(), accessor(request(), 'areaId', { set(_) { throw Error('setter ejecutado'); }, enumerable: true, configurable: true })));
test('entity getter no ejecutado', () => throws(state({ entities: [accessor(entity(), 'id')] })));
test('agenda getter no ejecutado', () => { const e = entity(); accessor(e.agenda, 'cycleLength'); throws(state({ entities: [e] })); });
test('slot getter no ejecutado', () => { const e = entity(); accessor(e.agenda.slots[0], 'roomId'); throws(state({ entities: [e] })); });
test('override getter no ejecutado', () => { const o = accessor(override(), 'priority'); throws(state({ entities: [entity({ overrides: [o] })] })); });
test('entities accessor index', () => { const a = [entity()]; accessor(a, '0'); throws(state({ entities: a })); });
test('slots accessor index', () => { const e = entity(); accessor(e.agenda.slots, '0'); throws(state({ entities: [e] })); });
test('overrides accessor index', () => { const a = [override()]; accessor(a, '0'); throws(state({ entities: [entity({ overrides: a })] })); });
test('array Symbol', () => { const a = [entity()]; a[Symbol('x')] = 1; throws(state({ entities: a })); });
test('Proxy ownKeys hostil', () => throws(new Proxy(state(), { ownKeys() { throw Error('trap'); } })));
test('Proxy getPrototypeOf hostil', () => { const e = entity(); e.agenda = new Proxy(e.agenda, { getPrototypeOf() { throw Error('trap'); } }); throws(state({ entities: [e] })); });
test('Proxy getOwnPropertyDescriptor hostil', () => { const e = entity(); e.overrides = new Proxy([override()], { getOwnPropertyDescriptor() { throw Error('trap'); } }); throws(state({ entities: [e] })); });
test('Proxy get trap no se ejecuta', () => { const proxied = new Proxy(state(), { get() { throw Error('get trap ejecutado'); } }); assert.equal(run(proxied).status, 'OVERRIDE_CATCH_UP_APPLIED'); });

test('oracle independiente BigInt: fases, prioridad y expiración aleatorias', () => {
  let seed = 42;
  const random = () => (seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0);
  for (let i = 0; i < 1000; i++) {
    const from = 10;
    const to = i % 4 === 0 ? Number.MAX_SAFE_INTEGER : 11 + random() % 1_000_000_000;
    const os = Array.from({ length: 1 + random() % 7 }, (_, j) => {
      const startTurn = 11 + random() % 1000;
      return override({ id: `o_${j}`, priority: random() % 5, startTurn,
        endTurn: j % 3 === 0 ? null : startTurn + 1 + random() % 1000,
        roomId: `r_${j}`, activity: `A_${j}` });
    });
    const x = run(state({ entities: [entity({ overrides: os })] }), at(from, to));
    const phase = Number(BigInt(to) % 100n);
    const slot = entity().agenda.slots.filter(s => s.start <= phase && phase < s.end)[0];
    const active = os.filter(o => o.startTurn <= to && (o.endTurn === null || to < o.endTurn));
    active.sort((a, b) => b.priority - a.priority || b.startTurn - a.startTurn || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    const winner = active[0];
    const final = x.state.entities[0];
    assert.equal(final.currentSourceType, winner ? 'OVERRIDE' : 'AGENDA');
    assert.equal(final.currentSourceId, winner?.id ?? slot.id);
    assert.equal(final.logicalRoomId, winner?.roomId ?? slot.roomId);
    assert.equal(final.currentActivity, winner?.activity ?? slot.activity);
    assert.equal(x.summary.expiredOverrides.length, os.filter(o => o.endTurn !== null && o.endTurn <= to).length);
    assert.equal(x.summary.entitySummaries[0].fullCyclesElapsed, Number(BigInt(to - from) / 100n));
  }
});
