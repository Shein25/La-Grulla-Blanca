import assert from 'node:assert/strict';
import { DIRECTION_ORDER, findRoute, validateGraph } from './pathfinder.mjs';
import { exits, labGraph } from './fixtures.mjs';

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log(`PASS ${name}`); }
  catch (error) { failed++; console.error(`FAIL ${name}`, error); }
}
function route(start = 'lab_a', goal = 'lab_d', options = {}, graph = labGraph()) {
  return findRoute(graph, start, goal, options);
}
function badGraph(change) {
  const graph = labGraph();
  change(graph);
  assert.throws(() => route('lab_a', 'lab_d', {}, graph), TypeError);
}
function assertRouteValid(graph, output, blockedExits = []) {
  if (output.status !== 'ROUTE_FOUND') return;
  assert.equal(output.rooms.length, output.steps.length + 1);
  assert.equal(output.distance, output.steps.length);
  assert.equal(output.rooms[0], output.startRoomId);
  assert.equal(output.rooms.at(-1), output.goalRoomId);
  assert.equal(new Set(output.rooms).size, output.rooms.length);
  const byId = new Map(graph.rooms.map(room => [room.id, room]));
  for (let i = 0; i < output.steps.length; i++) {
    const step = output.steps[i];
    assert.equal(step.from, output.rooms[i]);
    assert.equal(step.to, output.rooms[i + 1]);
    assert.equal(byId.get(step.from).exits[step.direction], step.to);
    assert.ok(!blockedExits.some(x => x.from === step.from && x.direction === step.direction));
  }
}

// Oracle de test independiente: relajación de distancias sobre todas las aristas.
// No comparte cola, padres, desempate ni helpers con el BFS de producción.
function oracleDistance(graph, start, goal, blockedExits = []) {
  const distance = new Map(graph.rooms.map(room => [room.id, Infinity]));
  distance.set(start, 0);
  for (let pass = 0; pass < graph.rooms.length - 1; pass++) {
    let changed = false;
    for (const room of graph.rooms) {
      for (const [direction, target] of Object.entries(room.exits)) {
        if (target === null || blockedExits.some(x => x.from === room.id && x.direction === direction)) continue;
        const candidate = distance.get(room.id) + 1;
        if (candidate < distance.get(target)) { distance.set(target, candidate); changed = true; }
      }
    }
    if (!changed) break;
  }
  return Number.isFinite(distance.get(goal)) ? distance.get(goal) : null;
}

test('DIRECTION_ORDER exacto', () => {
  assert.deepEqual(DIRECTION_ORDER, ['norte', 'este', 'sur', 'oeste', 'arriba', 'abajo']);
});
test('grafo válido y fixture de trece rooms', () => {
  const graph = labGraph();
  assert.equal(validateGraph(graph), true);
  assert.equal(graph.rooms.length, 13);
});
test('ruta directa', () => {
  const out = route('lab_a', 'lab_b');
  assert.equal(out.status, 'ROUTE_FOUND');
  assert.deepEqual(out.rooms, ['lab_a', 'lab_b']);
  assert.deepEqual(out.steps, [{ from: 'lab_a', direction: 'norte', to: 'lab_b' }]);
  assert.equal(out.distance, 1);
  assertRouteValid(labGraph(), out);
});
test('ruta de múltiples pasos', () => {
  const out = route('lab_a', 'lab_tower');
  assert.deepEqual(out.rooms, ['lab_a', 'lab_b', 'lab_d', 'lab_upper_1', 'lab_tower']);
  assert.deepEqual(out.steps.map(x => x.direction), ['norte', 'este', 'arriba', 'arriba']);
  assertRouteValid(labGraph(), out);
});
test('start == goal devuelve ALREADY_THERE', () => {
  assert.deepEqual(route('lab_a', 'lab_a'), {
    status: 'ALREADY_THERE', startRoomId: 'lab_a', goalRoomId: 'lab_a',
    rooms: ['lab_a'], steps: [], distance: 0, visitedCount: 1,
  });
});
test('BFS elige ruta corta frente a la larga', () => {
  const out = route();
  assert.equal(out.distance, 2);
  assert.notDeepEqual(out.rooms, ['lab_a', 'lab_long_1', 'lab_long_2', 'lab_d']);
});
test('desempate norte antes de este', () => {
  assert.deepEqual(route().rooms, ['lab_a', 'lab_b', 'lab_d']);
});
test('orden de rooms y propiedades no modifica el desempate', () => {
  const graph = labGraph();
  graph.rooms.reverse();
  for (const room of graph.rooms) room.exits = Object.fromEntries(Object.entries(room.exits).reverse());
  assert.deepEqual(route('lab_a', 'lab_d', {}, graph).rooms, ['lab_a', 'lab_b', 'lab_d']);
});
test('ciclo no produce loop y conserva ruta mínima', () => {
  const out = route('lab_c', 'lab_b');
  assert.deepEqual(out.rooms, ['lab_c', 'lab_a', 'lab_b']);
  assert.ok(out.visitedCount <= labGraph().rooms.length);
});
test('componente desconectada devuelve NO_ROUTE', () => {
  const out = route('lab_a', 'lab_y');
  assert.equal(out.status, 'NO_ROUTE');
  assert.equal(out.distance, null);
  assert.deepEqual(out.steps, []);
});
test('conexión unidireccional no se inventa de vuelta', () => {
  assert.deepEqual(route('lab_oneway_a', 'lab_oneway_b').rooms,
    ['lab_oneway_a', 'lab_oneway_b']);
  assert.equal(route('lab_oneway_b', 'lab_oneway_a').status, 'NO_ROUTE');
});
test('verticalidad arriba', () => {
  const out = route('lab_d', 'lab_tower');
  assert.deepEqual(out.steps.map(x => x.direction), ['arriba', 'arriba']);
});
test('verticalidad abajo', () => {
  const out = route('lab_tower', 'lab_d');
  assert.deepEqual(out.steps.map(x => x.direction), ['abajo', 'abajo']);
});
test('bloqueo temporal obliga ruta alternativa', () => {
  const graph = labGraph(), before = structuredClone(graph);
  const blockedExits = [{ from: 'lab_a', direction: 'norte' }];
  const out = route('lab_a', 'lab_d', { blockedExits }, graph);
  assert.deepEqual(out.rooms, ['lab_a', 'lab_c', 'lab_d']);
  assertRouteValid(graph, out, blockedExits);
  assert.deepEqual(graph, before);
});
test('bloqueos completos devuelven NO_ROUTE', () => {
  const out = route('lab_a', 'lab_d', { blockedExits: [
    { from: 'lab_a', direction: 'norte' },
    { from: 'lab_a', direction: 'este' },
    { from: 'lab_a', direction: 'sur' },
  ] });
  assert.equal(out.status, 'NO_ROUTE');
  assert.equal(out.visitedCount, 1);
});
test('maxVisited interrumpe con SEARCH_LIMIT', () => {
  const out = route('lab_a', 'lab_d', { maxVisited: 1 });
  assert.equal(out.status, 'SEARCH_LIMIT');
  assert.equal(out.visitedCount, 1);
  assert.notEqual(out.status, 'NO_ROUTE');
});
test('límite suficiente encuentra ruta', () => {
  const out = route('lab_a', 'lab_d', { maxVisited: 5 });
  assert.equal(out.status, 'ROUTE_FOUND');
  assert.equal(out.visitedCount, 5);
});
test('límite exacto para agotar componente devuelve NO_ROUTE', () => {
  assert.equal(route('lab_isolated', 'lab_a', { maxVisited: 1 }).status, 'NO_ROUTE');
});

test('start inexistente', () => assert.throws(() => route('missing', 'lab_a'), TypeError));
test('goal inexistente', () => assert.throws(() => route('lab_a', 'missing'), TypeError));
test('IDs start/goal vacíos o de tipo incorrecto', () => {
  for (const id of ['', '   ', null, undefined, 3, Symbol('x')]) {
    assert.throws(() => findRoute(labGraph(), id, 'lab_a'), TypeError);
    assert.throws(() => findRoute(labGraph(), 'lab_a', id), TypeError);
  }
});
test('graph no plano, versión incorrecta y rooms no array', () => {
  assert.throws(() => findRoute(null, 'a', 'b'), TypeError);
  badGraph(g => Object.setPrototypeOf(g, { version: 1 }));
  badGraph(g => { g.version = 2; });
  badGraph(g => { g.rooms = {}; });
  badGraph(g => { g.rooms = []; });
});
test('room duplicada y room no plana', () => {
  badGraph(g => { g.rooms[1].id = 'lab_a'; });
  badGraph(g => { g.rooms[1] = new Date(); });
});
test('id vacío y target inexistente, vacío o no string', () => {
  badGraph(g => { g.rooms[1].id = '   '; });
  badGraph(g => { g.rooms[0].exits.norte = 'missing'; });
  badGraph(g => { g.rooms[0].exits.norte = ''; });
  badGraph(g => { g.rooms[0].exits.norte = 3; });
});
test('dirección faltante o extra', () => {
  badGraph(g => { delete g.rooms[0].exits.norte; });
  badGraph(g => { g.rooms[0].exits.noreste = 'lab_b'; });
});
test('room exige exactamente id y exits', () => {
  badGraph(g => { g.rooms[0].extra = true; });
  badGraph(g => { delete g.rooms[0].id; });
});
test('getter en id o exits no se ejecuta', () => {
  for (const field of ['id', 'exits']) {
    let calls = 0;
    const graph = labGraph();
    Object.defineProperty(graph.rooms[0], field, { get() { calls++; throw Error('getter'); } });
    assert.throws(() => route('lab_a', 'lab_d', {}, graph), TypeError);
    assert.equal(calls, 0);
  }
});
test('getter y setter-only en dirección no se ejecutan', () => {
  let calls = 0;
  const graph = labGraph();
  Object.defineProperty(graph.rooms[0].exits, 'norte', { get() { calls++; throw Error('getter'); } });
  assert.throws(() => route('lab_a', 'lab_d', {}, graph), TypeError);
  assert.equal(calls, 0);
  badGraph(g => Object.defineProperty(g.rooms[0].exits, 'norte', { set(_) {} }));
});
test('hole y getter en índice de rooms rechazados sin ejecución', () => {
  badGraph(g => { delete g.rooms[0]; });
  let calls = 0;
  const graph = labGraph();
  Object.defineProperty(graph.rooms, '0', { get() { calls++; throw Error('getter'); } });
  assert.throws(() => route('lab_a', 'lab_d', {}, graph), TypeError);
  assert.equal(calls, 0);
});
test('Proxy con get hostil no invoca get', () => {
  let calls = 0;
  const graph = new Proxy(labGraph(), { get() { calls++; throw Error('get'); } });
  assert.equal(route('lab_a', 'lab_d', {}, graph).status, 'ROUTE_FOUND');
  assert.equal(calls, 0);
});
test('traps getPrototypeOf, ownKeys y descriptor se rechazan controladamente', () => {
  for (const trap of ['getPrototypeOf', 'ownKeys', 'getOwnPropertyDescriptor']) {
    const graph = new Proxy(labGraph(), { [trap]() { throw Error('trap hostil'); } });
    assert.throws(() => route('lab_a', 'lab_d', {}, graph), TypeError);
  }
});
test('Symbol keys en graph, rooms, room y exits rechazadas', () => {
  badGraph(g => { g[Symbol('x')] = true; });
  badGraph(g => { g.rooms[Symbol('x')] = true; });
  badGraph(g => { g.rooms[0][Symbol('x')] = true; });
  badGraph(g => { g.rooms[0].exits[Symbol('x')] = true; });
});
test('campos heredados no son aceptados', () => {
  badGraph(g => { delete g.version; Object.setPrototypeOf(g, { version: 1 }); });
  badGraph(g => { delete g.rooms[0].id; Object.setPrototypeOf(g.rooms[0], { id: 'lab_a' }); });
  badGraph(g => { delete g.rooms[0].exits.norte;
    Object.setPrototypeOf(g.rooms[0].exits, { norte: 'lab_b' }); });
});
test('exits no plano rechazado', () => badGraph(g => { g.rooms[0].exits = []; }));
test('options bloquea room y dirección inválidas y duplicados', () => {
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits: [{ from: 'missing', direction: 'norte' }] }), TypeError);
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits: [{ from: 'lab_a', direction: 'noreste' }] }), TypeError);
  const entry = { from: 'lab_a', direction: 'norte' };
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits: [entry, entry] }), TypeError);
});
test('blockedExit getter, herencia, symbol e índice accessor rechazados', () => {
  let calls = 0;
  const entry = { from: 'lab_a', direction: 'norte' };
  Object.defineProperty(entry, 'from', { get() { calls++; throw Error('getter'); } });
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits: [entry] }), TypeError);
  assert.equal(calls, 0);
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits: [
    Object.assign(Object.create({ from: 'lab_a' }), { direction: 'norte' }),
  ] }), TypeError);
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits: [
    { from: 'lab_a', direction: 'norte', [Symbol('x')]: 1 },
  ] }), TypeError);
  const blockedExits = [entry];
  Object.defineProperty(blockedExits, '0', { get() { calls++; throw Error('getter'); } });
  assert.throws(() => route('lab_a', 'lab_d', { blockedExits }), TypeError);
  assert.equal(calls, 0);
});
test('options maxVisited inválido, getter y extra rechazados', () => {
  for (const maxVisited of [0, -1, 1.5, NaN, Infinity, -Infinity, undefined, Symbol('x')]) {
    assert.throws(() => route('lab_a', 'lab_d', { maxVisited }), TypeError);
  }
  let calls = 0;
  const options = {};
  Object.defineProperty(options, 'maxVisited', { get() { calls++; throw Error('getter'); } });
  assert.throws(() => route('lab_a', 'lab_d', options), TypeError);
  assert.equal(calls, 0);
  assert.throws(() => route('lab_a', 'lab_d', { extra: 1 }), TypeError);
  assert.throws(() => route('lab_a', 'lab_d', { [Symbol('x')]: 1 }), TypeError);
});
test('grafo, rooms, exits, options y bloqueos intactos', () => {
  const graph = labGraph(), options = { blockedExits: [{ from: 'lab_a', direction: 'norte' }] };
  const before = structuredClone({ graph, options });
  route('lab_a', 'lab_d', options, graph);
  assert.deepEqual({ graph, options }, before);
});
test('mutar resultado no contamina input ni siguiente resultado', () => {
  const graph = labGraph(), options = { blockedExits: [{ from: 'lab_a', direction: 'norte' }] };
  const before = structuredClone({ graph, options });
  const expected = route('lab_a', 'lab_d', options, graph);
  const first = route('lab_a', 'lab_d', options, graph);
  first.rooms[0] = 'evil'; first.steps[0].to = 'evil'; first.distance = 999;
  assert.deepEqual({ graph, options }, before);
  assert.deepEqual(route('lab_a', 'lab_d', options, graph), expected);
});
test('mismos inputs producen resultado idéntico', () => {
  const graph = labGraph(), options = { blockedExits: [{ from: 'lab_a', direction: 'norte' }] };
  assert.deepEqual(route('lab_a', 'lab_d', options, graph), route('lab_a', 'lab_d', options, graph));
});
test('IDs Unicode y mapa con una sola room', () => {
  const graph = { version: 1, rooms: [{ id: 'área_雪', exits: exits() }] };
  assert.equal(validateGraph(graph), true);
  assert.equal(findRoute(graph, 'área_雪', 'área_雪').status, 'ALREADY_THERE');
});
test('oracle independiente verifica shortest path de todos los pares del fixture', () => {
  const graph = labGraph();
  for (const from of graph.rooms) for (const to of graph.rooms) {
    const expected = oracleDistance(graph, from.id, to.id);
    const out = findRoute(graph, from.id, to.id);
    if (expected === null) assert.equal(out.status, 'NO_ROUTE');
    else if (expected === 0) assert.equal(out.status, 'ALREADY_THERE');
    else { assert.equal(out.status, 'ROUTE_FOUND'); assert.equal(out.distance, expected); assertRouteValid(graph, out); }
  }
});
test('oracle independiente verifica grafo sintético generado y bloqueos', () => {
  let seed = 1337;
  const random = () => { seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5; return seed >>> 0; };
  const graph = { version: 1, rooms: Array.from({ length: 24 }, (_, i) =>
    ({ id: `gen_${i}`, exits: exits() })) };
  for (const room of graph.rooms) {
    for (const direction of DIRECTION_ORDER) {
      if (random() % 4 === 0) room.exits[direction] = `gen_${random() % graph.rooms.length}`;
    }
  }
  for (const from of graph.rooms) for (const to of graph.rooms) {
    const blockedExits = [{ from: from.id, direction: 'norte' }];
    const expected = oracleDistance(graph, from.id, to.id, blockedExits);
    const out = findRoute(graph, from.id, to.id, { blockedExits });
    if (expected === null) assert.equal(out.status, 'NO_ROUTE');
    else { assert.equal(out.distance, expected); assertRouteValid(graph, out, blockedExits); }
  }
});

console.log(`${passed}/${passed + failed} PASS`);
if (failed) process.exitCode = 1;
