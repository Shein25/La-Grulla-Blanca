import test from 'node:test';
import assert from 'node:assert/strict';
import { resolveAreaCatchUp as resolve } from './catchup-resolver.mjs';
import { makeState as state, makeCatchUp as request, goldenEvents } from './fixtures.mjs';

const clone = value => structuredClone(value);
const run = (s = state(), r = request()) => resolve(s, r);
const timer = remainingTurns => ({ id: 't', remainingTurns });
const meter = (value, ratePerTurn, min = 0, max = 100) => ({ id: 'm', value, ratePerTurn, min, max });
const entity = (timers = [], meters = [], id = 'e') => ({ id, timers, meters });
const event = (id, dueTurn, targetId = null) => ({ id, targetId, kind: 'SYNTHETIC', dueTurn });
const withEntity = (timers = [], meters = []) => state({ entities: [entity(timers, meters)] });
const at = (fromTurn, elapsedTurns) => ({ areaId: 'area_alpha', fromTurn, toTurn: fromTurn + elapsedTurns, elapsedTurns });
const throws = (s, r = request()) => assert.throws(() => run(s, r), TypeError);

test('estructura válida y syncedTurn final', () => { const x = run(); assert.equal(x.status, 'CATCH_UP_APPLIED'); assert.equal(x.state.syncedTurn, 120); assert.equal(x.state.version, 1); });
test('Golden A: timer parcial', () => { const x = run(); assert.equal(x.state.entities[0].timers[0].remainingTurns, 30); assert.deepEqual(x.summary.completedTimers, []); });
test('Golden B: timer completo', () => { const x = run(withEntity([timer(50)]), at(100, 100)); assert.equal(x.state.entities[0].timers[0].remainingTurns, 0); assert.deepEqual(x.summary.completedTimers, [{ entityId: 'e', timerId: 't', previousRemainingTurns: 50, remainingTurns: 0 }]); });
test('Golden C: meter positivo saturado', () => assert.equal(run(withEntity([], [meter(30, 2)]), at(100, 1000)).state.entities[0].meters[0].value, 100));
test('Golden D: meter negativo saturado', () => assert.equal(run(withEntity([], [meter(80, -3)]), at(100, 1000)).state.entities[0].meters[0].value, 0));
test('Golden E: eventos vencidos y futuros', () => { const x = run(goldenEvents(), at(100, 120)); assert.deepEqual(x.summary.dueEvents.map(e => e.id), ['event_a', 'event_c']); assert.deepEqual(x.state.scheduledEvents.map(e => e.id), ['event_b']); });
test('Golden F: efectos simultáneos', () => { const s = state({ entities: [entity([timer(80)], [meter(30, 2), { id: 'hunger', value: 80, ratePerTurn: -1, min: 0, max: 100 }])], scheduledEvents: [event('late', 3000), event('due', 900)] }); const x = run(s, at(100, 2000)); assert.equal(x.state.syncedTurn, 2100); assert.equal(x.summary.completedTimers.length, 1); assert.deepEqual(x.summary.meterChanges.map(m => m.value), [0, 100]); assert.deepEqual(x.summary.dueEvents.map(e => e.id), ['due']); assert.deepEqual(x.state.scheduledEvents.map(e => e.id), ['late']); });
test('Golden G: mil millones de turns', () => { const x = run(state({ syncedTurn: 10 }), at(10, 1_000_000_000)); assert.equal(x.state.syncedTurn, 1_000_000_010); assert.equal(x.state.entities[0].meters[0].value, 100); });
test('timer previo cero no se completa', () => { const x = run(withEntity([timer(0)])); assert.equal(x.state.entities[0].timers[0].remainingTurns, 0); assert.equal(x.summary.completedTimers.length, 0); });
test('timer límite exacto', () => assert.equal(run(withEntity([timer(20)])).summary.completedTimers.length, 1));
test('timer no negativo de máximo seguro', () => assert.equal(run(withEntity([timer(Number.MAX_SAFE_INTEGER)])).state.entities[0].timers[0].remainingTurns, Number.MAX_SAFE_INTEGER - 20));
test('rate cero no genera cambio', () => assert.deepEqual(run(withEntity([], [meter(30, 0)])).summary.meterChanges, []));
test('meter llega exactamente al máximo', () => assert.equal(run(withEntity([], [meter(80, 1)])).state.entities[0].meters[0].value, 100));
test('meter llega exactamente al mínimo', () => assert.equal(run(withEntity([], [meter(20, -1)])).state.entities[0].meters[0].value, 0));
test('meter ya en máximo no genera cambio', () => assert.deepEqual(run(withEntity([], [meter(100, 5)])).summary.meterChanges, []));
test('meter ya en mínimo no genera cambio', () => assert.deepEqual(run(withEntity([], [meter(0, -5)])).summary.meterChanges, []));
test('meter sin saturar', () => assert.equal(run(withEntity([], [meter(20, 2)])).state.entities[0].meters[0].value, 60));
test('overflow positivo adversarial', () => assert.equal(run(withEntity([], [meter(0, Number.MAX_SAFE_INTEGER, -5, 8)]), at(100, Number.MAX_SAFE_INTEGER - 100)).state.entities[0].meters[0].value, 8));
test('overflow negativo adversarial', () => assert.equal(run(withEntity([], [meter(0, -Number.MAX_SAFE_INTEGER, -8, 5)]), at(100, Number.MAX_SAFE_INTEGER - 100)).state.entities[0].meters[0].value, -8));
test('rango completo de enteros seguros', () => { const m = meter(0, -1, -Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER); assert.equal(run(withEntity([], [m])).state.entities[0].meters[0].value, -20); });
test('entidades vacías', () => assert.deepEqual(run(state({ entities: [] })).state.entities, []));
test('colecciones internas vacías', () => { const x = run(withEntity()); assert.deepEqual(x.state.entities[0], entity()); });
test('eventos vacíos', () => assert.deepEqual(run().summary.dueEvents, []));
test('evento vence exactamente en toTurn', () => assert.equal(run(state({ scheduledEvents: [event('a', 120)] })).summary.dueEvents.length, 1));
test('evento posterior queda pendiente', () => assert.equal(run(state({ scheduledEvents: [event('a', 121)] })).state.scheduledEvents.length, 1));
test('empate de eventos se ordena por id', () => assert.deepEqual(run(state({ scheduledEvents: [event('z', 110), event('a', 110)] })).summary.dueEvents.map(e => e.id), ['a', 'z']));
test('eventos futuros también se ordenan', () => assert.deepEqual(run(state({ scheduledEvents: [event('z', 150), event('a', 150), event('b', 140)] })).state.scheduledEvents.map(e => e.id), ['b', 'a', 'z']));
test('target null permitido', () => assert.equal(run(state({ scheduledEvents: [event('a', 110)] })).summary.dueEvents[0].targetId, null));
test('entidades, timers y meters canónicos', () => { const s = state({ entities: [entity([{ id: 'z', remainingTurns: 1 }, { id: 'a', remainingTurns: 1 }], [{ ...meter(5, 1), id: 'z' }, meter(5, 1)], 'z'), entity([], [], 'a')] }); const x = run(s); assert.deepEqual(x.state.entities.map(e => e.id), ['a', 'z']); assert.deepEqual(x.state.entities[1].timers.map(t => t.id), ['a', 'z']); assert.deepEqual(x.state.entities[1].meters.map(m => m.id), ['m', 'z']); });
test('Unicode IDs ordenados sin locale', () => { const s = state({ entities: [entity([], [], 'é'), entity([], [], '中'), entity([], [], 'A')] }); assert.deepEqual(run(s).state.entities.map(e => e.id), ['A', 'é', '中']); });
test('inputs no mutados', () => { const s = state({ scheduledEvents: [event('a', 110)] }); const r = request(); const before = clone([s, r]); run(s, r); assert.deepEqual([s, r], before); });
test('inputs congelados funcionan', () => { const s = state({ entities: [entity([timer(10)], [meter(20, 1)])] }); Object.freeze(s.entities[0].timers[0]); Object.freeze(s.entities[0].timers); Object.freeze(s.entities[0].meters[0]); Object.freeze(s.entities[0].meters); Object.freeze(s.entities[0]); Object.freeze(s.entities); Object.freeze(s.scheduledEvents); Object.freeze(s); assert.equal(run(s).state.entities[0].timers[0].remainingTurns, 0); });
test('output desacoplado de inputs y ejecuciones', () => { const s = state({ scheduledEvents: [event('a', 110), event('b', 130)] }); const first = run(s); const second = run(s); first.state.entities[0].timers[0].remainingTurns = 999; first.state.entities.push(entity()); first.summary.dueEvents[0].id = 'changed'; first.summary.completedTimers.push({}); first.summary.meterChanges.push({}); first.state.scheduledEvents[0].id = 'changed'; assert.deepEqual(second, run(s)); assert.equal(s.scheduledEvents[0].id, 'a'); });
test('determinismo exacto', () => { const s = goldenEvents(); assert.deepEqual(run(s, at(100, 120)), run(s, at(100, 120))); });

const invalid = [
  ['state null', () => [null]], ['state array', () => [[]]], ['version', () => [state({ version: 2 })]],
  ['areaId vacío', () => [state({ areaId: '' })]], ['syncedTurn float', () => [state({ syncedTurn: 1.5 })]],
  ['state extra', () => [{ ...state(), extra: true }]], ['state Symbol', () => [Object.assign(state(), { [Symbol('x')]: 1 })]],
  ['state heredado', () => [Object.assign(Object.create({ inherited: true }), state())]],
  ['entities no array', () => [state({ entities: {} })]], ['entities hole', () => [state({ entities: Array(1) })]],
  ['entidad no plana', () => [state({ entities: [new (class E { constructor() { this.id='e'; this.timers=[]; this.meters=[]; } })()] })]],
  ['entidad extra', () => [state({ entities: [{ ...entity(), extra: 1 }] })]],
  ['entidad duplicada', () => [state({ entities: [entity(), entity()] })]],
  ['entidad ID vacío', () => [state({ entities: [entity([], [], '')] })]],
  ['timers no array', () => [state({ entities: [{ ...entity(), timers: {} }] })]],
  ['meters no array', () => [state({ entities: [{ ...entity(), meters: {} }] })]],
  ['timers hole', () => [state({ entities: [entity(Array(1))] })]],
  ['meters hole', () => [state({ entities: [entity([], Array(1))] })]],
  ['timer duplicado', () => [state({ entities: [entity([timer(1), timer(2)])] })]],
  ['timer negativo', () => [withEntity([timer(-1)])]], ['timer float', () => [withEntity([timer(1.2)])]],
  ['timer NaN', () => [withEntity([timer(NaN)])]], ['timer Infinity', () => [withEntity([timer(Infinity)])]],
  ['timer unsafe', () => [withEntity([timer(Number.MAX_SAFE_INTEGER + 1)])]],
  ['timer extra', () => [withEntity([{ ...timer(1), extra: 2 }])]],
  ['meter duplicado', () => [withEntity([], [meter(1, 1), meter(2, 1)])]],
  ['meter min > max', () => [withEntity([], [meter(1, 1, 2, 0)])]],
  ['meter value < min', () => [withEntity([], [meter(-1, 1)])]],
  ['meter value > max', () => [withEntity([], [meter(101, 1)])]],
  ['meter NaN', () => [withEntity([], [meter(NaN, 1)])]],
  ['meter rate Infinity', () => [withEntity([], [meter(1, Infinity)])]],
  ['meter unsafe', () => [withEntity([], [meter(1, Number.MAX_SAFE_INTEGER + 1)])]],
  ['meter extra', () => [withEntity([], [{ ...meter(1, 1), extra: 2 }])]],
  ['event ID vacío', () => [state({ scheduledEvents: [event('', 110)] })]],
  ['event duplicado', () => [state({ scheduledEvents: [event('a', 110), event('a', 111)] })]],
  ['event kind vacío', () => [state({ scheduledEvents: [{ ...event('a', 110), kind: '' }] })]],
  ['event target inválido', () => [state({ scheduledEvents: [event('a', 110, 'missing')] })]],
  ['event due previo', () => [state({ scheduledEvents: [event('a', 100)] })]],
  ['event due unsafe', () => [state({ scheduledEvents: [event('a', Number.MAX_SAFE_INTEGER + 1)] })]],
  ['event extra', () => [state({ scheduledEvents: [{ ...event('a', 110), extra: 1 }] })]],
  ['event hole', () => [state({ scheduledEvents: Array(1) })]],
  ['catchUp area distinto', () => [state(), request({ areaId: 'other' })]],
  ['catchUp from distinto', () => [state(), request({ fromTurn: 99 })]],
  ['catchUp elapsed incorrecto', () => [state(), request({ elapsedTurns: 21 })]],
  ['catchUp cero', () => [state(), request({ toTurn: 100, elapsedTurns: 0 })]],
  ['catchUp regresivo', () => [state(), request({ toTurn: 99, elapsedTurns: 1 })]],
  ['catchUp float', () => [state(), request({ toTurn: 120.5 })]],
  ['catchUp unsafe', () => [state(), request({ toTurn: Number.MAX_SAFE_INTEGER + 1 })]],
  ['catchUp extra', () => [state(), { ...request(), extra: 1 }]],
  ['catchUp Symbol', () => [state(), Object.assign(request(), { [Symbol('x')]: 1 })]],
  ['catchUp heredado', () => [state(), Object.assign(Object.create({ inherited: true }), request())]],
];
for (const [name, make] of invalid) test(`rechaza ${name}`, () => throws(...make()));

function accessor(object, key, descriptor = { get() { throw Error('getter ejecutado'); }, enumerable: true, configurable: true }) { Object.defineProperty(object, key, descriptor); return object; }
test('getter de state no se ejecuta', () => throws(accessor(state(), 'areaId')));
test('getter de catchUp no se ejecuta', () => throws(state(), accessor(request(), 'fromTurn')));
test('setter-only de catchUp rechazado', () => throws(state(), accessor(request(), 'areaId', { set(_) { throw Error('setter ejecutado'); }, enumerable: true, configurable: true })));
test('getter anidado de timer no se ejecuta', () => throws(state({ entities: [entity([accessor(timer(1), 'remainingTurns')])] })));
test('getter anidado de meter no se ejecuta', () => throws(withEntity([], [accessor(meter(1, 1), 'value')])));
test('getter anidado de event no se ejecuta', () => throws(state({ scheduledEvents: [accessor(event('a', 110), 'kind')] })));
test('accessor index en entities', () => { const a = [entity()]; accessor(a, '0'); throws(state({ entities: a })); });
test('accessor index en timers', () => { const a = [timer(1)]; accessor(a, '0'); throws(state({ entities: [entity(a)] })); });
test('accessor index en meters', () => { const a = [meter(1, 1)]; accessor(a, '0'); throws(withEntity([], a)); });
test('accessor index en events', () => { const a = [event('a', 110)]; accessor(a, '0'); throws(state({ scheduledEvents: a })); });
test('Symbol en array rechazado', () => { const a = [entity()]; a[Symbol('x')] = 1; throws(state({ entities: a })); });
test('campo heredado en timer rechazado', () => { const t = Object.assign(Object.create({ inherited: true }), timer(1)); throws(withEntity([t])); });
test('Proxy hostil de state rechazado', () => throws(new Proxy(state(), { ownKeys() { throw Error('trap'); } })));
test('Proxy hostil de array rechazado', () => throws(state({ entities: new Proxy([entity()], { getOwnPropertyDescriptor() { throw Error('trap'); } }) })));
test('Proxy hostil de catchUp rechazado', () => throws(state(), new Proxy(request(), { getPrototypeOf() { throw Error('trap'); } })));

test('oracle BigInt independiente: combinaciones aleatorias y extremos', () => {
  let seed = 42;
  const random = () => ((seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0) / 2 ** 32);
  for (let i = 0; i < 1000; i++) {
    const elapsed = [1, 2, 10, 100, 1_000_000_000, Number.MAX_SAFE_INTEGER - 100][i % 6];
    const min = i % 3 === 0 ? -Number.MAX_SAFE_INTEGER : -1000;
    const max = i % 3 === 0 ? Number.MAX_SAFE_INTEGER : 1000;
    const value = min === -1000 ? Math.floor(random() * 2001) - 1000 : 0;
    const rate = i % 7 === 0 ? Number.MAX_SAFE_INTEGER : i % 7 === 1 ? -Number.MAX_SAFE_INTEGER : Math.floor(random() * 101) - 50;
    const actual = run(withEntity([], [meter(value, rate, min, max)]), at(100, elapsed)).state.entities[0].meters[0].value;
    const raw = BigInt(value) + BigInt(rate) * BigInt(elapsed);
    const expected = Number(raw < BigInt(min) ? BigInt(min) : raw > BigInt(max) ? BigInt(max) : raw);
    assert.equal(actual, expected, `case ${i}`);
  }
});
