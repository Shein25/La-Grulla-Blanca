import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { DIRECTION_ORDER, findRoute } from './pathfinder.mjs';
import { exits } from './fixtures.mjs';

const seed = Number(process.argv[2] ?? 1337);
const queryCount = Number(process.argv[3] ?? 600);
if (!Number.isSafeInteger(seed) || !Number.isSafeInteger(queryCount) || queryCount < 5) {
  throw new TypeError('Uso: node stress.mjs [seed entero seguro] [queries>=5]');
}
function rng(initial) {
  let state = initial >>> 0;
  return () => {
    state ^= state << 13; state ^= state >>> 17; state ^= state << 5;
    return state >>> 0;
  };
}
const random = rng(seed);

function generatedGraph() {
  const rooms = Array.from({ length: 160 }, (_, i) => ({ id: `synthetic_${i}`, exits: exits() }));
  rooms[0].exits.norte = rooms[1].id;
  rooms[0].exits.este = rooms[2].id;
  rooms[1].exits.este = rooms[3].id;
  rooms[2].exits.norte = rooms[3].id;
  rooms[3].exits.este = rooms[4].id;
  for (let i = 4; i < 140; i++) {
    rooms[i].exits.norte = rooms[i === 139 ? 4 : i + 1].id;
    rooms[i].exits.este = rooms[4 + random() % 136].id;
    if (random() % 3 === 0) rooms[i].exits.arriba = rooms[4 + random() % 136].id;
  }
  for (let i = 140; i < 160; i++) {
    rooms[i].exits.sur = rooms[i === 159 ? 140 : i + 1].id;
    if (random() % 2 === 0) rooms[i].exits.oeste = rooms[140 + random() % 20].id;
  }
  return { version: 1, rooms };
}

const graph = generatedGraph();
const beforeGraph = JSON.stringify(graph);
const byId = new Map(graph.rooms.map(room => [room.id, room]));
const report = {
  seed, rooms: graph.rooms.length, queries: 0, routeFound: 0,
  alreadyThere: 0, noRoute: 0, searchLimit: 0,
  blockedAlternativeRoutes: 0, maxDistance: 0, averageDistance: 0,
  maxVisited: 0,
};
const hash = createHash('sha256');
let sumDistance = 0;

function verify(out, start, goal, options) {
  assert.equal(out.startRoomId, start);
  assert.equal(out.goalRoomId, goal);
  assert.ok(out.visitedCount >= 1 && out.visitedCount <= graph.rooms.length);
  assert.ok(out.visitedCount <= (options.maxVisited ?? 10000));
  report.maxVisited = Math.max(report.maxVisited, out.visitedCount);
  if (out.status === 'ROUTE_FOUND') {
    report.routeFound++;
    assert.equal(out.rooms.length, out.steps.length + 1);
    assert.equal(out.distance, out.steps.length);
    assert.equal(out.rooms[0], start);
    assert.equal(out.rooms.at(-1), goal);
    assert.equal(new Set(out.rooms).size, out.rooms.length);
    for (let i = 0; i < out.steps.length; i++) {
      const step = out.steps[i];
      assert.equal(step.from, out.rooms[i]);
      assert.equal(step.to, out.rooms[i + 1]);
      assert.ok(DIRECTION_ORDER.includes(step.direction));
      assert.equal(byId.get(step.from).exits[step.direction], step.to);
      assert.ok(!(options.blockedExits ?? []).some(x =>
        x.from === step.from && x.direction === step.direction));
    }
    sumDistance += out.distance;
    report.maxDistance = Math.max(report.maxDistance, out.distance);
  } else if (out.status === 'ALREADY_THERE') {
    report.alreadyThere++;
    assert.equal(start, goal);
    assert.deepEqual(out.rooms, [start]);
    assert.deepEqual(out.steps, []);
    assert.equal(out.distance, 0);
  } else if (out.status === 'NO_ROUTE') {
    report.noRoute++;
    assert.equal(out.distance, null);
    assert.deepEqual(out.rooms, []);
    assert.deepEqual(out.steps, []);
  } else if (out.status === 'SEARCH_LIMIT') {
    report.searchLimit++;
    assert.equal(out.visitedCount, options.maxVisited);
    assert.equal(out.distance, null);
  } else throw Error(`Estado inesperado: ${out.status}`);
}

function query(start, goal, options = {}) {
  const beforeOptions = JSON.stringify(options);
  const out = findRoute(graph, start, goal, options);
  assert.equal(JSON.stringify(options), beforeOptions, 'options mutado');
  assert.deepEqual(findRoute(graph, start, goal, options), out, 'resultado no determinista');
  verify(out, start, goal, options);
  report.queries++;
  hash.update(JSON.stringify({ start, goal, options, out }));
  return out;
}

const direct = query('synthetic_0', 'synthetic_3');
const blocked = query('synthetic_0', 'synthetic_3', {
  blockedExits: [{ from: 'synthetic_0', direction: 'norte' }],
});
assert.deepEqual(direct.rooms, ['synthetic_0', 'synthetic_1', 'synthetic_3']);
assert.deepEqual(blocked.rooms, ['synthetic_0', 'synthetic_2', 'synthetic_3']);
report.blockedAlternativeRoutes++;
query('synthetic_0', 'synthetic_150');
query('synthetic_0', 'synthetic_3', { maxVisited: 1 });
query('synthetic_0', 'synthetic_0');

while (report.queries < queryCount) {
  const start = `synthetic_${random() % graph.rooms.length}`;
  const goal = `synthetic_${random() % graph.rooms.length}`;
  const options = {};
  if (random() % 5 === 0) {
    const candidates = DIRECTION_ORDER.filter(direction => byId.get(start).exits[direction] !== null);
    if (candidates.length) {
      options.blockedExits = [{ from: start, direction: candidates[random() % candidates.length] }];
    }
  }
  if (random() % 7 === 0) options.maxVisited = 1 + random() % 5;
  let unblocked = null;
  if (options.blockedExits && options.maxVisited === undefined) {
    unblocked = findRoute(graph, start, goal);
  }
  const out = query(start, goal, options);
  if (unblocked?.status === 'ROUTE_FOUND' && out.status === 'ROUTE_FOUND' &&
      JSON.stringify(unblocked.rooms) !== JSON.stringify(out.rooms)) {
    report.blockedAlternativeRoutes++;
  }
}
assert.equal(JSON.stringify(graph), beforeGraph, 'graph mutado');
assert.ok(report.routeFound > 0 && report.noRoute > 0 && report.searchLimit > 0);
assert.ok(report.blockedAlternativeRoutes > 0);
report.averageDistance = sumDistance / report.routeFound;
report.digest = hash.digest('hex');
console.log(JSON.stringify(report));
