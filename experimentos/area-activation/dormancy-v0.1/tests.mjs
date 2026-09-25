import assert from 'node:assert/strict';
import { createAreaActivationState, activatePlayerArea } from './area-activation.mjs';
import { labAreas, syntheticAreas } from './fixtures.mjs';

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log(`PASS ${name}`); }
  catch (error) { failed++; console.error(`FAIL ${name}`, error); }
}
const make = () => createAreaActivationState(labAreas());
const activate = (state, turn, id = 'area_alpha') => activatePlayerArea(state, turn, id);
function badState(change) {
  const state = activate(make(), 1).state;
  change(state);
  assert.throws(() => activate(state, 2), TypeError);
}
function noGetter(fn) {
  let calls = 0;
  assert.throws(() => fn(() => { calls++; throw Error('getter ejecutado'); }), TypeError);
  assert.equal(calls, 0);
}
function byId(state, id) { return state.areas.find(area => area.id === id); }

test('estado inicial exacto y áreas ordenadas', () => {
  const state = make();
  assert.equal(state.version, 1);
  assert.equal(state.clock, null);
  assert.equal(state.activeAreaId, null);
  assert.deepEqual(state.areas.map(x => x.id), [
    'area_alpha', 'area_beta', 'area_delta', 'area_gamma', 'area_isolated',
  ]);
  assert.ok(state.areas.every(x => x.lastSimulatedTurn === 0));
});
test('orden de configs no altera estado', () => {
  assert.deepEqual(createAreaActivationState(labAreas()),
    createAreaActivationState([...labAreas()].reverse()));
});
test('Golden A: activación inicial en turn 0 sin catch-up', () => {
  const out = activate(make(), 0);
  assert.equal(out.status, 'INITIAL_ACTIVATION');
  assert.equal(out.previousAreaId, null);
  assert.equal(out.activeAreaId, 'area_alpha');
  assert.equal(out.catchUp, null);
  assert.equal(out.deactivation, null);
  assert.deepEqual(out.activation, { areaId: 'area_alpha', atTurn: 0 });
  assert.equal(out.state.clock, 0);
});
test('Golden B: activación tardía produce 0 a 100', () => {
  const out = activate(make(), 100);
  assert.deepEqual(out.catchUp, {
    areaId: 'area_alpha', fromTurn: 0, toTurn: 100, elapsedTurns: 100,
  });
  assert.equal(byId(out.state, 'area_alpha').lastSimulatedTurn, 100);
});
test('Golden C: cambio A a B actualiza origen y destino', () => {
  const first = activate(make(), 0);
  const out = activate(first.state, 150, 'area_beta');
  assert.equal(out.status, 'AREA_SWITCHED');
  assert.equal(out.previousAreaId, 'area_alpha');
  assert.equal(out.activeAreaId, 'area_beta');
  assert.deepEqual(out.deactivation, { areaId: 'area_alpha', atTurn: 150 });
  assert.deepEqual(out.activation, { areaId: 'area_beta', atTurn: 150 });
  assert.equal(byId(out.state, 'area_alpha').lastSimulatedTurn, 150);
  assert.equal(byId(out.state, 'area_beta').lastSimulatedTurn, 150);
  assert.deepEqual(out.catchUp, { areaId: 'area_beta', fromTurn: 0,
    toTurn: 150, elapsedTurns: 150 });
});
test('Golden D: reentrada A tras salida 150 y vuelta 450', () => {
  const a = activate(make(), 0);
  const b = activate(a.state, 150, 'area_beta');
  const back = activate(b.state, 450, 'area_alpha');
  assert.equal(back.status, 'AREA_SWITCHED');
  assert.deepEqual(back.catchUp, { areaId: 'area_alpha',
    fromTurn: 150, toTurn: 450, elapsedTurns: 300 });
  assert.equal(byId(back.state, 'area_alpha').lastSimulatedTurn, 450);
});
test('Golden E: misma área no reactiva ni cambia lastSimulatedTurn', () => {
  const first = activate(make(), 0);
  const out = activate(first.state, 100);
  assert.equal(out.status, 'ALREADY_ACTIVE');
  assert.equal(out.catchUp, null);
  assert.equal(out.activation, null);
  assert.equal(out.deactivation, null);
  assert.equal(out.state.clock, 100);
  assert.equal(byId(out.state, 'area_alpha').lastSimulatedTurn, 0);
  const leave = activate(out.state, 150, 'area_beta');
  assert.equal(byId(leave.state, 'area_alpha').lastSimulatedTurn, 150);
});
test('Golden F: salto de un millón de turns produce un catch-up', () => {
  const b = activate(make(), 0, 'area_beta');
  const a = activate(b.state, 100, 'area_alpha');
  const back = activate(a.state, 1_000_100, 'area_beta');
  assert.deepEqual(back.catchUp, { areaId: 'area_beta',
    fromTurn: 100, toTurn: 1_000_100, elapsedTurns: 1_000_000 });
  assert.ok(!Array.isArray(back.catchUp));
});
test('Golden G: terceras áreas no cambian durante A a B', () => {
  const a = activate(make(), 10);
  const before = new Map(a.state.areas.map(x => [x.id, x.lastSimulatedTurn]));
  const b = activate(a.state, 150, 'area_beta');
  for (const id of ['area_gamma', 'area_delta', 'area_isolated']) {
    assert.equal(byId(b.state, id).lastSimulatedTurn, before.get(id));
  }
});
test('sólo activeAreaId representa el área activa', () => {
  const out = activate(make(), 25);
  assert.equal(out.state.activeAreaId, 'area_alpha');
  assert.ok(out.state.areas.every(area => Object.keys(area).join('|') === 'id|lastSimulatedTurn'));
});
test('switch exige elapsed positivo; sólo activación en turn 0 omite catchUp', () => {
  const state = activate(make(), 10).state;
  state.areas.find(area => area.id === 'area_beta').lastSimulatedTurn = 10;
  const out = activate(state, 11, 'area_beta');
  assert.deepEqual(out.catchUp, { areaId: 'area_beta', fromTurn: 10,
    toTurn: 11, elapsedTurns: 1 });
  const initial = createAreaActivationState([{ id: 'area_only' }]);
  assert.equal(activatePlayerArea(initial, 0, 'area_only').catchUp, null);
});
test('área desconocida e ID inválido se rechazan', () => {
  assert.throws(() => activate(make(), 1, 'missing'), TypeError);
  for (const id of ['', '  ', null, undefined, 42, Symbol('x')]) {
    assert.throws(() => activatePlayerArea(make(), 1, id), TypeError);
  }
});
test('clock inicial arbitrario, luego estrictamente creciente', () => {
  let state = activate(make(), 10).state;
  state = activate(state, 20).state;
  state = activate(state, 100, 'area_beta').state;
  assert.equal(state.clock, 100);
});
test('clock igual, pasado, negativo, float y no finito se rechazan', () => {
  const state = activate(make(), 10).state;
  for (const value of [10, 9, -1, 1.5, NaN, Infinity,
    -Infinity, Number.MAX_SAFE_INTEGER + 1, undefined]) {
    assert.throws(() => activatePlayerArea(state, value, 'area_alpha'), TypeError);
  }
});
test('MAX_SAFE_INTEGER como primer turn conserva elapsed exacto', () => {
  const out = activate(make(), Number.MAX_SAFE_INTEGER);
  assert.equal(out.catchUp.elapsedTurns, Number.MAX_SAFE_INTEGER);
  assert.equal(out.state.clock, Number.MAX_SAFE_INTEGER);
});
test('una sola área soporta continuidad', () => {
  const state = createAreaActivationState([{ id: 'area_sola' }]);
  const first = activatePlayerArea(state, 0, 'area_sola');
  const second = activatePlayerArea(first.state, 1_000_000, 'area_sola');
  assert.equal(second.status, 'ALREADY_ACTIVE');
  assert.equal(second.catchUp, null);
});
test('mil áreas sintéticas y sólo target se activa', () => {
  const state = createAreaActivationState(syntheticAreas(1000));
  const out = activatePlayerArea(state, 100, 'area_999');
  assert.equal(out.state.areas.length, 1000);
  assert.equal(out.state.activeAreaId, 'area_999');
  assert.equal(out.state.areas.filter(x => x.lastSimulatedTurn === 100).length, 1);
});
test('Unicode en id es válido', () => {
  const state = createAreaActivationState([{ id: 'área_雪' }]);
  assert.equal(activatePlayerArea(state, 25, 'área_雪').activeAreaId, 'área_雪');
});
test('configs vacías, duplicados e id inválido se rechazan', () => {
  assert.throws(() => createAreaActivationState([]), TypeError);
  assert.throws(() => createAreaActivationState([{ id: 'a' }, { id: 'a' }]), TypeError);
  for (const id of ['', '  ', null, undefined, 5, Symbol('x')]) {
    assert.throws(() => createAreaActivationState([{ id }]), TypeError);
  }
});
test('config no plana, extra, Symbol y heredada se rechazan', () => {
  assert.throws(() => createAreaActivationState([new Date()]), TypeError);
  assert.throws(() => createAreaActivationState([{ id: 'a', extra: 1 }]), TypeError);
  assert.throws(() => createAreaActivationState([{ id: 'a', [Symbol('x')]: 1 }]), TypeError);
  assert.throws(() => createAreaActivationState([Object.create({ id: 'a' })]), TypeError);
});
test('getter y setter-only en config se rechazan sin ejecución', () => {
  noGetter(get => {
    const config = {};
    Object.defineProperty(config, 'id', { get });
    return createAreaActivationState([config]);
  });
  const config = {};
  Object.defineProperty(config, 'id', { set(_) {} });
  assert.throws(() => createAreaActivationState([config]), TypeError);
});
test('Proxy get hostil no se ejecuta al capturar config', () => {
  let calls = 0;
  const proxy = new Proxy({ id: 'area_proxy' }, {
    get() { calls++; throw Error('get hostil'); },
  });
  assert.equal(createAreaActivationState([proxy]).areas[0].id, 'area_proxy');
  assert.equal(calls, 0);
});
test('Proxy traps estructurales se rechazan controladamente', () => {
  for (const trap of ['getPrototypeOf', 'ownKeys', 'getOwnPropertyDescriptor']) {
    const proxy = new Proxy({ id: 'area_proxy' }, { [trap]() { throw Error('hostil'); } });
    assert.throws(() => createAreaActivationState([proxy]), TypeError);
  }
});
test('configs con holes e índice accessor se rechazan sin ejecución', () => {
  const configs = [{ id: 'a' }, { id: 'b' }]; delete configs[0];
  assert.throws(() => createAreaActivationState(configs), TypeError);
  noGetter(get => {
    const array = [{ id: 'a' }];
    Object.defineProperty(array, '0', { get });
    return createAreaActivationState(array);
  });
});
test('state version y clock inválidos se rechazan', () => {
  badState(s => { s.version = 2; });
  for (const clock of [NaN, Infinity, -Infinity, -1, 1.5, Number.MAX_SAFE_INTEGER + 1]) {
    badState(s => { s.clock = clock; });
  }
});
test('state activeAreaId inválido, desconocido y no string/null', () => {
  badState(s => { s.activeAreaId = 'missing'; });
  for (const activeAreaId of ['', 42, undefined, Symbol('x')]) {
    badState(s => { s.activeAreaId = activeAreaId; });
  }
});
test('state duplicado, lastSimulated inválido o futuro', () => {
  badState(s => { s.areas.push({ ...s.areas[0] }); });
  for (const value of [-1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1, 2]) {
    badState(s => { s.areas[0].lastSimulatedTurn = value; });
  }
});
test('estado inicial contradictorio se rechaza', () => {
  const state = make(); state.activeAreaId = 'area_alpha';
  assert.throws(() => activate(state, 1), TypeError);
  const other = make(); other.areas[0].lastSimulatedTurn = 1;
  assert.throws(() => activate(other, 1), TypeError);
});
test('clock no null puede tener cero áreas activas y se inicializa al entrar', () => {
  const state = make(); state.clock = 10;
  const out = activate(state, 11);
  assert.equal(out.status, 'INITIAL_ACTIVATION');
  assert.equal(out.catchUp.elapsedTurns, 11);
});
test('state getter y setter-only se rechazan sin ejecución', () => {
  noGetter(get => {
    const state = activate(make(), 1).state;
    Object.defineProperty(state, 'activeAreaId', { get });
    return activate(state, 2);
  });
  const state = activate(make(), 1).state;
  Object.defineProperty(state.areas[0], 'lastSimulatedTurn', { set(_) {} });
  assert.throws(() => activate(state, 2), TypeError);
});
test('state heredada, extra y Symbol se rechazan', () => {
  badState(s => { s.extra = 1; });
  badState(s => { s[Symbol('x')] = 1; });
  badState(s => { delete s.activeAreaId; Object.setPrototypeOf(s, { activeAreaId: 'area_alpha' }); });
  badState(s => { s.areas[0].extra = 1; });
});
test('state areas con holes, accessor y Symbol se rechazan', () => {
  badState(s => { delete s.areas[0]; });
  badState(s => { s.areas[Symbol('x')] = 1; });
  noGetter(get => {
    const state = activate(make(), 1).state;
    Object.defineProperty(state.areas, '0', { get });
    return activate(state, 2);
  });
});
test('Proxy hostil en state se rechaza y get trap no se ejecuta', () => {
  const state = activate(make(), 1).state;
  assert.throws(() => activate(new Proxy(state, {
    ownKeys() { throw Error('hostil'); },
  }), 2), TypeError);
  let calls = 0;
  const proxy = new Proxy(state, { get() { calls++; throw Error('get hostil'); } });
  assert.equal(activate(proxy, 2).status, 'ALREADY_ACTIVE');
  assert.equal(calls, 0);
});
test('state anterior y configs originales permanecen intactos', () => {
  const configs = labAreas();
  const state = createAreaActivationState(configs);
  const before = structuredClone({ configs, state });
  activate(state, 100);
  assert.deepEqual({ configs, state }, before);
});
test('mutar output no contamina input ni ejecución posterior', () => {
  const state = make();
  const expected = activate(state, 100);
  const out = activate(state, 100);
  out.state.areas[0].id = 'evil';
  out.catchUp.elapsedTurns = 999;
  out.activation.areaId = 'evil';
  assert.deepEqual(state, make());
  assert.deepEqual(activate(state, 100), expected);
});
test('resultados previos quedan independientes', () => {
  const first = activate(make(), 100);
  const before = structuredClone(first);
  const second = activate(first.state, 200, 'area_beta');
  second.state.areas[0].lastSimulatedTurn = 999;
  second.catchUp.fromTurn = 999;
  assert.deepEqual(first, before);
});
test('mismos inputs producen resultado completo idéntico', () => {
  const state = make();
  assert.deepEqual(activate(state, 100), activate(state, 100));
});
test('gran elapsed no crea arrays de turns ni cambia terceros', () => {
  const state = activate(make(), 10).state;
  const before = structuredClone(state);
  const out = activate(state, 1_000_010, 'area_beta');
  assert.equal(out.catchUp.elapsedTurns, 1_000_010);
  assert.equal(Object.keys(out.catchUp).length, 4);
  assert.equal(byId(out.state, 'area_gamma').lastSimulatedTurn, 0);
  assert.deepEqual(state, before);
});
test('input inválido no modifica estado anterior', () => {
  const state = activate(make(), 10).state;
  const before = structuredClone(state);
  assert.throws(() => activate(state, 11, 'missing'), TypeError);
  assert.deepEqual(state, before);
});

console.log(`${passed}/${passed + failed} PASS`);
if (failed) process.exitCode = 1;
