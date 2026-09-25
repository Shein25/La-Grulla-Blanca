import assert from 'node:assert/strict';
import { createMemoryState, recordMemory } from '../motor-npc-vivo-v0.3-memory/memory.mjs';
import { ACTION_TO_GOAL, decideFromMemory } from './decision-pipeline.mjs';
import { goldenNpc, goldenContext, goldenWorld } from './fixtures.mjs';

let passed = 0;
let failed = 0;
function test(name, run) {
  try { run(); passed++; console.log(`PASS ${name}`); }
  catch (error) { failed++; console.error(`FAIL ${name}`, error); }
}
function event(key, kind, subject = 'jugador', expiresTurn = null) {
  return { key, kind, subject, value: true, importance: 100,
    confidence: 100, turn: 1, expiresTurn };
}
function memoryOf(...events) {
  let memory = createMemoryState();
  for (const item of events) memory = recordMemory(memory, item);
  return memory;
}
function run(npc = goldenNpc(), memory = createMemoryState(), turn = 0,
  context = goldenContext(), world = goldenWorld(), options = {}) {
  return decideFromMemory(npc, memory, turn, context, world, options);
}
function score(out, action) {
  return out.utilityDecision.ranking.find(item => item.name === action).score;
}
function approx(actual, expected) { assert.ok(Math.abs(actual - expected) < 1e-9, `${actual} != ${expected}`); }
function checkFiniteNumbers(value) {
  if (typeof value === 'number') assert.ok(Number.isFinite(value));
  else if (Array.isArray(value)) value.forEach(checkFiniteNumbers);
  else if (value && typeof value === 'object') Object.values(value).forEach(checkFiniteNumbers);
}

test('mapping exacto de nueve acciones', () => {
  assert.deepEqual(ACTION_TO_GOAL, {
    ayudar_jugador: 'HELP_PLAYER', investigar: 'INVESTIGATE_ANOMALY',
    informar_superior: 'REPORT_SUPERIOR', vigilar: 'FULFILL_DUTY',
    trabajar: 'FULFILL_DUTY', patrullar: 'FULFILL_DUTY',
    regresar_puesto: 'RETURN_POST', esperar: 'WAIT_SAFE', hablar_jugador: null,
  });
});

test('Golden A: sin memoria investiga y planifica una acción', () => {
  const out = run();
  assert.equal(out.status, 'PLAN_READY');
  assert.deepEqual(out.relationDerivation.relations, goldenNpc().relationPlayer);
  assert.equal(out.utilityDecision.action, 'investigar');
  approx(score(out, 'investigar'), 55.2);
  approx(score(out, 'ayudar_jugador'), 52.03333333333333);
  assert.deepEqual(out.mapping, { utilityAction: 'investigar', goalId: 'INVESTIGATE_ANOMALY' });
  assert.deepEqual(out.plan.plan, ['investigar_anomalia']);
  assert.equal(out.plan.status, 'PLAN_FOUND');
  assert.deepEqual(out.plan.goal, out.goal);
  assert.deepEqual(out.plan.relevance, out.relevance);
  assert.equal(out.plan.utilityAction, 'investigar');
});

test('Golden B: PLAYER_HELPED_ME cambia decisión, goal y plan', () => {
  const memory = memoryOf(event('player:helped_me', 'PLAYER_HELPED_ME'));
  const out = run(goldenNpc(), memory, 1);
  assert.deepEqual(out.relationDerivation.relations, {
    afinidad: 47, confianza: 45, respeto: 50, deuda: 8, temor: 0, rivalidad: 0,
  });
  assert.equal(out.relationDerivation.contributions.length, 1);
  assert.equal(out.utilityDecision.action, 'ayudar_jugador');
  approx(score(out, 'ayudar_jugador'), 58.67333333333333);
  approx(score(out, 'investigar'), 55.2);
  assert.equal(out.goalId, 'HELP_PLAYER');
  assert.equal(out.status, 'PLAN_READY');
  assert.deepEqual(out.plan.plan, ['ir_jugador', 'ayudar_jugador']);
  assert.equal(out.plan.goalId, 'HELP_PLAYER');
  assert.equal(out.plan.utilityAction, 'ayudar_jugador');
});

test('Golden C: PLAYER_LIED sobre superior invierte la decisión', () => {
  const npc = goldenNpc();
  npc.relationPlayer = { afinidad: 47, confianza: 45, respeto: 50,
    deuda: 8, temor: 0, rivalidad: 0 };
  const before = run(npc);
  const after = run(npc, memoryOf(event('lie', 'PLAYER_LIED', 'superior')), 1);
  assert.equal(before.utilityDecision.action, 'ayudar_jugador');
  assert.deepEqual(after.relationDerivation.relations, {
    afinidad: 47, confianza: 27, respeto: 44, deuda: 8, temor: 0, rivalidad: 12,
  });
  assert.equal(after.utilityDecision.action, 'investigar');
  approx(score(after, 'investigar'), 55.2);
  approx(score(after, 'ayudar_jugador'), 52.31333333333333);
  assert.equal(after.goalId, 'INVESTIGATE_ANOMALY');
  assert.deepEqual(after.plan.plan, ['investigar_anomalia']);
});

test('subject no indica actor para PLAYER_HELPED_ME', () => {
  const a = run(goldenNpc(), memoryOf(event('help', 'PLAYER_HELPED_ME', 'jugador')), 1);
  const b = run(goldenNpc(), memoryOf(event('help', 'PLAYER_HELPED_ME', 'superior')), 1);
  assert.deepEqual(a, b);
});

test('sin fallback: una ayuda imposible conserva la intención', () => {
  const world = { ...goldenWorld(), playerReachable: false };
  const out = run(goldenNpc(), memoryOf(event('help', 'PLAYER_HELPED_ME')), 1,
    goldenContext(), world);
  assert.equal(out.status, 'NO_PLAN');
  assert.equal(out.utilityDecision.action, 'ayudar_jugador');
  assert.equal(out.goalId, 'HELP_PLAYER');
  assert.equal(out.plan.status, 'NO_PLAN');
  assert.equal(out.plan.plan, null);
});

test('hablar_jugador queda unmapped sin inventar goal', () => {
  const context = { ...goldenContext(), playerRequestsHelp: false,
    anomalyPresent: false, missionUrgency: 0 };
  const world = { ...goldenWorld(), playerNeedsHelp: false,
    anomalyPresent: false, urgency: 0 };
  const npc = goldenNpc();
  npc.traits.sociabilidad = 100;
  npc.relationPlayer.afinidad = 100;
  npc.relationPlayer.confianza = 100;
  const out = run(npc, createMemoryState(), 0, context, world);
  assert.equal(out.utilityDecision.action, 'hablar_jugador');
  assert.equal(out.status, 'UTILITY_ACTION_UNMAPPED');
  assert.equal(out.goalId, null);
  assert.equal(out.plan, null);
});

test('maxExpansions=0 conserva SEARCH_LIMIT', () => {
  const out = run(goldenNpc(), createMemoryState(), 0,
    goldenContext(), goldenWorld(), { maxExpansions: 0 });
  assert.equal(out.status, 'PLANNING_DEFERRED');
  assert.equal(out.plan.status, 'SEARCH_LIMIT');
  assert.equal(out.goalId, 'INVESTIGATE_ANOMALY');
});

test('maxFrontier=1 conserva FRONTIER_LIMIT', () => {
  const out = run(goldenNpc(), createMemoryState(), 0,
    goldenContext(), goldenWorld(), { maxFrontier: 1 });
  assert.equal(out.status, 'PLANNING_DEFERRED');
  assert.equal(out.plan.status, 'FRONTIER_LIMIT');
});

test('relaciones nunca se acumulan entre llamadas', () => {
  const npc = goldenNpc();
  const memory = memoryOf(event('help', 'PLAYER_HELPED_ME'));
  const first = run(npc, memory, 1);
  const second = run(npc, memory, 1);
  assert.deepEqual(first, second);
  assert.equal(npc.relationPlayer.afinidad, 35);
});

test('memorias con entries en otro orden dan resultado completo idéntico', () => {
  const memory = memoryOf(event('z', 'PLAYER_LIED'),
    event('a', 'PLAYER_HELPED_ME'), event('m', 'ORDER_RECEIVED'));
  const reversed = { ...memory, entries: [...memory.entries].reverse() };
  assert.deepEqual(run(goldenNpc(), memory, 1), run(goldenNpc(), reversed, 1));
});

test('expiración e irrelevancia conservan base y trazan ignorados', () => {
  const memory = memoryOf(event('expired', 'PLAYER_HELPED_ME', 'jugador', 1),
    event('irrelevant', 'ORDER_RECEIVED'));
  const out = run(goldenNpc(), memory, 2);
  assert.deepEqual(out.relationDerivation.relations, goldenNpc().relationPlayer);
  assert.equal(out.relationDerivation.contributions.length, 0);
  assert.deepEqual(out.relationDerivation.ignoredMemories.map(x => x.memoryKey), ['irrelevant']);
});

test('inputs intactos y resultado desacoplado de todos ellos', () => {
  const npc = goldenNpc(), memory = memoryOf(event('help', 'PLAYER_HELPED_ME'));
  const context = goldenContext(), world = goldenWorld(), options = { maxExpansions: 50 };
  const before = structuredClone({ npc, memory, context, world, options });
  const first = run(npc, memory, 1, context, world, options);
  assert.deepEqual({ npc, memory, context, world, options }, before);
  first.relationDerivation.relations.afinidad = 0;
  first.utilityDecision.ranking[0].score = 0;
  first.plan.finalState.at = 'otro';
  first.plan.goal.playerHelped = false;
  assert.deepEqual({ npc, memory, context, world, options }, before);
  assert.deepEqual(run(npc, memory, 1, context, world, options),
    run(npc, memory, 1, context, world, options));
});

test('traza completa sólo contiene números finitos', () => checkFiniteNumbers(run()));

for (const field of ['relationPlayer', 'traits', 'id', 'behaviorState']) {
  test(`NPC getter ${field} rechazado sin ejecución`, () => {
    let calls = 0;
    const npc = goldenNpc();
    Object.defineProperty(npc, field, { get() { calls++; throw Error('ejecutado'); } });
    assert.throws(() => run(npc), TypeError);
    assert.equal(calls, 0);
  });
}
test('NPC propiedad heredada y objeto no plano rechazados', () => {
  const npc = goldenNpc();
  delete npc.relationPlayer;
  assert.throws(() => run(npc), TypeError);
  const inherited = Object.assign(Object.create({ relationPlayer: goldenNpc().relationPlayer }), npc);
  assert.throws(() => run(inherited), TypeError);
  assert.throws(() => run(new Date()), TypeError);
});

for (const field of ['playerPresent', 'missionUrgency']) {
  test(`context getter ${field} rechazado sin ejecución`, () => {
    let calls = 0;
    const context = goldenContext();
    Object.defineProperty(context, field, { get() { calls++; throw Error('ejecutado'); } });
    assert.throws(() => run(goldenNpc(), createMemoryState(), 0, context), TypeError);
    assert.equal(calls, 0);
  });
}
test('context heredado, no plano y valor inválido rechazados', () => {
  const context = goldenContext();
  delete context.playerPresent;
  assert.throws(() => run(goldenNpc(), createMemoryState(), 0, context), TypeError);
  assert.throws(() => run(goldenNpc(), createMemoryState(), 0,
    Object.assign(Object.create({ playerPresent: true }), context)), TypeError);
  assert.throws(() => run(goldenNpc(), createMemoryState(), 0,
    { ...goldenContext(), playerRank: 99 }), TypeError);
});

test('world getters enumerables y no enumerables rechazados sin ejecución', () => {
  for (const enumerable of [true, false]) {
    let calls = 0;
    const world = goldenWorld();
    Object.defineProperty(world, enumerable ? 'danger' : 'hidden', {
      enumerable, get() { calls++; throw Error('ejecutado'); },
    });
    assert.throws(() => run(goldenNpc(), createMemoryState(), 0, goldenContext(), world), TypeError);
    assert.equal(calls, 0);
  }
});
for (const [name, fact] of [
  ['Symbol', { [Symbol('hostile')]: true }], ['NaN', { extra: NaN }],
  ['Infinity', { extra: Infinity }], ['-Infinity', { extra: -Infinity }],
  ['objeto', { extra: {} }], ['array', { extra: [] }],
  ['function', { extra() {} }],
]) {
  test(`world ${name} rechazado`, () => {
    assert.throws(() => run(goldenNpc(), createMemoryState(), 0,
      goldenContext(), { ...goldenWorld(), ...fact }), TypeError);
  });
}

const contradictions = [
  ['playerPresent', { playerPresent: false }],
  ['playerRequestsHelp/playerNeedsHelp', { playerNeedsHelp: false }],
  ['playerRequestsHelp/playerHelped', { playerHelped: true }],
  ['anomalyPresent', { anomalyPresent: false }],
  ['anomalyInvestigated', { anomalyInvestigated: true }],
  ['awayFromPost/at', { at: 'jugador' }],
  ['dutyImportance', { dutyImportance: 21 }],
  ['danger', { danger: 21 }],
  ['missionUrgency/urgency', { urgency: 61 }],
];
for (const [name, change] of contradictions) {
  test(`contradicción ${name} rechazada`, () => {
    assert.throws(() => run(goldenNpc(), createMemoryState(), 0,
      goldenContext(), { ...goldenWorld(), ...change }), /incoherentes/);
  });
}

test('plannerOptions getter rechazado sin ejecución', () => {
  let calls = 0;
  const options = {};
  Object.defineProperty(options, 'maxExpansions', { get() { calls++; throw Error('ejecutado'); } });
  assert.throws(() => run(goldenNpc(), createMemoryState(), 0,
    goldenContext(), goldenWorld(), options), TypeError);
  assert.equal(calls, 0);
});
test('plannerOptions inválido conserva validación GOAP', () => {
  assert.throws(() => run(goldenNpc(), createMemoryState(), 0,
    goldenContext(), goldenWorld(), { maxExpansions: -1 }), TypeError);
});

console.log(`${passed}/${passed + failed} PASS`);
if (failed) process.exitCode = 1;
