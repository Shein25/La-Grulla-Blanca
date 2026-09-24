import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createAreaActivationState, activatePlayerArea } from './area-activation.mjs';
import { syntheticAreas } from './fixtures.mjs';

const seed = Number(process.argv[2] ?? 1337);
const updates = Number(process.argv[3] ?? 20000);
if (!Number.isSafeInteger(seed) || !Number.isSafeInteger(updates) || updates < 1) {
  throw new TypeError('Uso: node stress.mjs [seed entero seguro] [updates>=1]');
}
function rng(initial) {
  let value = initial >>> 0;
  return () => {
    value ^= value << 13; value ^= value >>> 17; value ^= value << 5;
    return value >>> 0;
  };
}
const random = rng(seed);
const configs = syntheticAreas(32);
const originalConfigs = JSON.stringify(configs);
let state = createAreaActivationState(configs);
const oracle = {
  clock: null,
  activeAreaId: null,
  last: new Map(configs.map(config => [config.id, 0])),
};
let currentTurn = -1;
const hash = createHash('sha256');
const report = {
  seed, updates, areas: configs.length,
  initialActivations: 0, switches: 0, alreadyActive: 0,
  catchUpRequests: 0, collapsedDormantTurns: 0,
  maxElapsedTurns: 0, averageElapsedTurns: 0,
};

for (let index = 0; index < updates; index++) {
  currentTurn += 1 + random() % 25;
  if (index % 113 === 0) currentTurn += 10_000 + random() % 100_000;
  assert.ok(Number.isSafeInteger(currentTurn) && currentTurn >= 0);
  if (oracle.clock !== null) assert.ok(currentTurn > oracle.clock);
  const target = oracle.activeAreaId !== null && random() % 4 === 0
    ? oracle.activeAreaId : configs[random() % configs.length].id;
  const previous = oracle.activeAreaId;
  const oldLast = new Map(oracle.last);
  const inputBefore = JSON.stringify(state);
  const result = activatePlayerArea(state, currentTurn, target);
  assert.equal(JSON.stringify(state), inputBefore, 'input mutado');
  assert.deepEqual(activatePlayerArea(state, currentTurn, target), result,
    'resultado no determinista');
  assert.equal(result.previousAreaId, previous);
  assert.equal(result.activeAreaId, target);
  assert.equal(result.state.activeAreaId, target);
  assert.equal(result.state.clock, currentTurn);
  assert.ok(oracle.last.has(result.state.activeAreaId));
  assert.deepEqual(result.state.areas.map(area => area.id),
    [...oracle.last.keys()].sort());
  assert.ok(result.state.areas.every(area =>
    Object.keys(area).length === 2 &&
    Number.isSafeInteger(area.lastSimulatedTurn) &&
    area.lastSimulatedTurn >= 0 && area.lastSimulatedTurn <= currentTurn));

  if (previous === target) {
    report.alreadyActive++;
    assert.equal(result.status, 'ALREADY_ACTIVE');
    assert.equal(result.catchUp, null);
    assert.equal(result.activation, null);
    assert.equal(result.deactivation, null);
  } else {
    if (previous === null) {
      report.initialActivations++;
      assert.equal(result.status, 'INITIAL_ACTIVATION');
      assert.equal(result.deactivation, null);
    } else {
      report.switches++;
      assert.equal(result.status, 'AREA_SWITCHED');
      assert.deepEqual(result.deactivation, { areaId: previous, atTurn: currentTurn });
      oracle.last.set(previous, currentTurn);
    }
    assert.deepEqual(result.activation, { areaId: target, atTurn: currentTurn });
    const fromTurn = oldLast.get(target);
    const expectedElapsed = currentTurn - fromTurn;
    assert.ok(Number.isSafeInteger(expectedElapsed) && expectedElapsed >= 0);
    const expectedCatchUp = expectedElapsed === 0 ? null
      : { areaId: target, fromTurn, toTurn: currentTurn,
        elapsedTurns: expectedElapsed };
    assert.deepEqual(result.catchUp, expectedCatchUp);
    if (result.catchUp) {
      report.catchUpRequests++;
      report.collapsedDormantTurns += result.catchUp.elapsedTurns;
      report.maxElapsedTurns = Math.max(report.maxElapsedTurns,
        result.catchUp.elapsedTurns);
      assert.equal(result.catchUp.elapsedTurns,
        result.catchUp.toTurn - result.catchUp.fromTurn);
    }
    oracle.last.set(target, currentTurn);
    oracle.activeAreaId = target;
  }
  for (const area of result.state.areas) {
    assert.equal(area.lastSimulatedTurn, oracle.last.get(area.id));
    if (area.id !== previous && area.id !== target) {
      assert.equal(area.lastSimulatedTurn, oldLast.get(area.id), 'tercera área mutada');
    }
  }
  oracle.clock = currentTurn;
  state = result.state;
  hash.update(JSON.stringify(result));
}

assert.equal(JSON.stringify(configs), originalConfigs, 'configs mutadas');
assert.equal(report.initialActivations, 1);
assert.equal(report.initialActivations + report.switches + report.alreadyActive, updates);
assert.ok(report.switches > 0 && report.alreadyActive > 0);
assert.ok(report.catchUpRequests > 0);
assert.ok(report.collapsedDormantTurns > report.catchUpRequests);
report.averageElapsedTurns = report.collapsedDormantTurns / report.catchUpRequests;
report.digest = hash.digest('hex');
console.log(JSON.stringify(report));
