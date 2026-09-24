import test from 'node:test';
import assert from 'node:assert/strict';
import { createExecutionSession as create, advanceExecutionSession as advance } from './execution-session.mjs';
import { makeWorld, makeActions, makeInitialConfig } from './fixtures.mjs';

const session = (changes = {}) => create(makeInitialConfig(changes));
const world = makeWorld;
const actions = makeActions;
const run = (s = session(), w = world(), a = actions(), options = {}) => advance(s, w, a, options);
const clone = value => structuredClone(value);
const throws = (s, w = world(), a = actions(), options = {}) => assert.throws(() => advance(s, w, a, options), TypeError);

test('create: estructura, copias y contadores cero', () => { const s = session(); assert.deepEqual([s.version, s.mode, s.goalId, s.stepCount, s.replanCount], [1, 'ACTIVE', 'HELP_PLAYER', 0, 0]); assert.deepEqual(s.plan, ['ir_a', 'usar_a']); });
test('Golden A plan normal de dos pasos', () => { const first = run(); assert.equal(first.status, 'STEP_APPLIED'); assert.equal(first.executed, 'ir_a'); assert.deepEqual(first.session.plan, ['usar_a']); assert.equal(first.session.stepCount, 1); const second = run(first.session, first.world); assert.equal(second.status, 'GOAL_REACHED'); assert.equal(second.executed, 'usar_a'); assert.equal(second.session, null); assert.deepEqual(second.counters, { stepCount: 2, replanCount: 0 }); });
test('Golden B goal alcanzado externamente', () => { const x = run(session(), world({ playerHelped: true })); assert.equal(x.status, 'GOAL_REACHED'); assert.equal(x.executed, null); assert.equal(x.session, null); assert.equal(x.counters.stepCount, 0); });
test('Golden C relevance obsoleta', () => { const x = run(session(), world({ playerNeedsHelp: false })); assert.equal(x.status, 'INTENT_REEVALUATION_REQUIRED'); assert.equal(x.executed, null); assert.equal(x.goalObsolete, true); assert.equal(x.replan, null); assert.equal(x.session, null); });
test('Golden D precondition cambia entre llamadas', () => { const first = run(); const changed = { ...first.world, routeAOpen: false }; const second = run(first.session, changed); assert.equal(second.status, 'REPLAN_READY'); assert.equal(second.executed, null); assert.deepEqual(second.session.plan, ['volver', 'ir_b', 'usar_b']); assert.deepEqual(second.world, changed); assert.equal(second.session.replanCount, 1); const third = run(second.session, second.world); assert.equal(third.status, 'STEP_APPLIED'); assert.equal(third.executed, 'volver'); });
test('Golden E acción desaparece del catálogo', () => { const first = run(); const catalog = actions().filter(a => a.id !== 'usar_a'); const second = run(first.session, first.world, catalog); assert.equal(second.status, 'REPLAN_READY'); assert.equal(second.executed, null); assert.deepEqual(second.session.plan, ['volver', 'ir_b', 'usar_b']); });
test('Golden F NO_PLAN mantiene goal y limpia plan stale', () => { const x = run(session(), world({ routeAOpen: false, routeBOpen: false })); assert.equal(x.status, 'NO_PLAN_FOR_GOAL'); assert.equal(x.session.mode, 'REPLAN_PENDING'); assert.equal(x.session.plan, null); assert.equal(x.session.goalId, 'HELP_PLAYER'); assert.equal(x.session.replanCount, 1); assert.equal(x.replan.plannerStatus, 'NO_PLAN'); });
test('Golden G SEARCH_LIMIT se difiere', () => { const x = run(session({ plan: [] }), world(), actions(), { maxExpansions: 0 }); assert.equal(x.status, 'PLANNING_DEFERRED'); assert.equal(x.replan.plannerStatus, 'SEARCH_LIMIT'); assert.equal(x.session.mode, 'REPLAN_PENDING'); assert.equal(x.session.plan, null); });
test('Golden H retry desde pending', () => { const first = run(session(), world({ routeAOpen: false, routeBOpen: false })); const second = run(first.session, world({ routeAOpen: false, routeBOpen: true })); assert.equal(second.status, 'REPLAN_READY'); assert.deepEqual(second.session.plan, ['ir_b', 'usar_b']); assert.equal(second.session.replanCount, 2); assert.equal(second.executed, null); });
test('Golden I goal alcanzado mientras pending', () => { const first = run(session(), world({ routeAOpen: false, routeBOpen: false })); const second = run(first.session, world({ playerHelped: true })); assert.equal(second.status, 'GOAL_REACHED'); assert.equal(second.executed, null); assert.equal(second.replan, null); assert.equal(second.session, null); assert.equal(second.counters.replanCount, 1); });
test('Golden J relevance muere mientras pending', () => { const first = run(session(), world({ routeAOpen: false, routeBOpen: false })); const second = run(first.session, world({ playerNeedsHelp: false })); assert.equal(second.status, 'INTENT_REEVALUATION_REQUIRED'); assert.equal(second.replan, null); assert.equal(second.session, null); assert.equal(second.counters.replanCount, 1); });
test('Golden K plan vacío y goal no satisfecho', () => { const x = run(session({ plan: [] })); assert.equal(x.status, 'REPLAN_READY'); assert.deepEqual(x.session.plan, ['ir_a', 'usar_a']); assert.equal(x.executed, null); });
test('Golden L atomicidad: replan no ejecuta primer paso', () => { const s = session({ plan: ['desconocida'] }); const w = world(); const x = run(s, w); assert.equal(x.status, 'REPLAN_READY'); assert.equal(x.executed, null); assert.deepEqual(x.world, w); assert.equal(x.session.stepCount, 0); assert.equal(x.session.replanCount, 1); assert.deepEqual(x.session.plan, ['ir_a', 'usar_a']); });
test('goal satisfecho tiene prioridad sobre relevance obsoleta', () => { const x = run(session(), world({ playerHelped: true, playerNeedsHelp: false })); assert.equal(x.status, 'GOAL_REACHED'); assert.equal(x.replan, null); });
test('world extra irrelevante sobrevive al paso', () => { const x = run(session(), world({ unrelated: 99 })); assert.equal(x.world.unrelated, 99); });
test('IDs de plan repetidos se aceptan en create', () => assert.deepEqual(session({ plan: ['ir_a', 'ir_a'] }).plan, ['ir_a', 'ir_a']));
test('goal y relevance vacíos son válidos', () => { const x = run(session({ goal: {}, relevance: {}, plan: [] })); assert.equal(x.status, 'GOAL_REACHED'); assert.equal(x.executed, null); });
test('FRONTIER_LIMIT no se confunde con NO_PLAN', () => { const x = run(session({ plan: [] }), world(), actions(), { maxFrontier: 1 }); assert.equal(x.status, 'PLANNING_DEFERRED'); assert.equal(x.replan.plannerStatus, 'FRONTIER_LIMIT'); });
test('COST_OVERFLOW no se confunde con NO_PLAN', () => { const catalog = [ { id: 'a', cost: Number.MAX_SAFE_INTEGER, preconditions: { p0: true }, effects: { p1: true } }, { id: 'b', cost: 1, preconditions: { p1: true }, effects: { p2: true } } ]; const s = create({ goalId: 'G', goal: { p2: true }, relevance: {}, plan: [] }); const x = run(s, { p0: true }, catalog); assert.equal(x.status, 'PLANNING_DEFERRED'); assert.equal(x.replan.plannerStatus, 'COST_OVERFLOW'); });
test('replan pending no usa Executor: plan null permitido', () => { const first = run(session(), world({ routeAOpen: false, routeBOpen: false })); assert.equal(first.session.plan, null); const second = run(first.session, world({ playerHelped: true }), []); assert.equal(second.status, 'GOAL_REACHED'); });
test('replan conserva exactamente el mismo goal y goalId', () => { const s = session(); const x = run(s, world({ routeAOpen: false, routeBOpen: true })); assert.equal(x.status, 'REPLAN_READY'); assert.deepEqual(x.session.goal, s.goal); assert.equal(x.session.goalId, s.goalId); });
test('replan GOAP no depende del orden del catálogo', () => { const s = session({ plan: [] }); const a = run(s, world(), actions()); const b = run(s, world(), actions().reverse()); assert.deepEqual(a, b); });
test('no plan no elige fallback', () => { const x = run(session(), world({ routeAOpen: false, routeBOpen: false })); assert.equal(x.session.goalId, 'HELP_PLAYER'); assert.equal(x.status, 'NO_PLAN_FOR_GOAL'); });
test('contador stepCount sólo aumenta con acción', () => { const a = run(session(), world({ playerHelped: true })); assert.equal(a.counters.stepCount, 0); const b = run(); assert.equal(b.counters.stepCount, 1); });
test('contador replanCount sólo aumenta con intento', () => { const a = run(); assert.equal(a.counters.replanCount, 0); const b = run(session(), world({ playerNeedsHelp: false })); assert.equal(b.counters.replanCount, 0); const c = run(session({ plan: [] })); assert.equal(c.counters.replanCount, 1); });
test('stepCount overflow arroja RangeError', () => { const s = { ...session(), stepCount: Number.MAX_SAFE_INTEGER }; assert.throws(() => run(s), RangeError); assert.equal(s.stepCount, Number.MAX_SAFE_INTEGER); });
test('replanCount overflow arroja RangeError', () => { const s = { ...session({ plan: [] }), replanCount: Number.MAX_SAFE_INTEGER }; assert.throws(() => run(s), RangeError); assert.equal(s.replanCount, Number.MAX_SAFE_INTEGER); });
test('contadores cerca del máximo siguen siendo seguros', () => { const s = { ...session(), stepCount: Number.MAX_SAFE_INTEGER - 1 }; const x = run(s); assert.equal(x.session.stepCount, Number.MAX_SAFE_INTEGER); });
test('captura goal/relevance/plan desacoplada de originales', () => { const input = makeInitialConfig(); const s = create(input); input.goal.playerHelped = false; input.relevance.playerPresent = false; input.plan[0] = 'changed'; assert.deepEqual(s.goal, { playerHelped: true }); assert.deepEqual(s.relevance, { playerPresent: true, playerNeedsHelp: true }); assert.equal(s.plan[0], 'ir_a'); });
test('inputs no mutados en advance', () => { const s = session(), w = world(), a = actions(), o = { maxExpansions: 100 }; const before = clone([s, w, a, o]); run(s, w, a, o); assert.deepEqual([s, w, a, o], before); });
test('inputs congelados funcionan', () => { const s = session(), w = world(), a = actions(), o = { maxExpansions: 100 }; Object.freeze(s.goal); Object.freeze(s.relevance); Object.freeze(s.plan); Object.freeze(s); Object.freeze(w); Object.freeze(o); for (const item of a) { Object.freeze(item.preconditions); Object.freeze(item.effects); Object.freeze(item); } Object.freeze(a); assert.equal(run(s, w, a, o).status, 'STEP_APPLIED'); });
test('outputs desacoplados de inputs y otras ejecuciones', () => { const s = session(), w = world(); const a = run(s, w), b = run(s, w); a.session.goal.playerHelped = false; a.session.plan[0] = 'changed'; a.world.at = 'changed'; assert.deepEqual(b, run(s, w)); assert.equal(w.at, 'puesto'); });
test('determinismo', () => assert.deepEqual(run(), run()));

const invalidCreate = [
  ['input null', () => null], ['input array', () => []], ['input extra', () => ({ ...makeInitialConfig(), extra: 1 })],
  ['goalId blanco', () => makeInitialConfig({ goalId: '   ' })], ['goal no plano', () => makeInitialConfig({ goal: [] })],
  ['relevance no plano', () => makeInitialConfig({ relevance: [] })], ['plan no array', () => makeInitialConfig({ plan: {} })],
  ['plan hole', () => makeInitialConfig({ plan: Array(1) })], ['plan ID blanco', () => makeInitialConfig({ plan: [' '] })],
  ['goal nested', () => makeInitialConfig({ goal: { x: {} } })], ['goal NaN', () => makeInitialConfig({ goal: { x: NaN } })],
  ['relevance Infinity', () => makeInitialConfig({ relevance: { x: Infinity } })],
  ['goal Symbol', () => makeInitialConfig({ goal: Object.assign({ x: 1 }, { [Symbol('s')]: 2 }) })],
  ['goal heredado', () => makeInitialConfig({ goal: Object.assign(Object.create({ x: 1 }), { y: 2 }) })],
];
for (const [name, make] of invalidCreate) test(`create rechaza ${name}`, () => assert.throws(() => create(make()), TypeError));

const invalidAdvance = [
  ['session null', () => [null]], ['session extra', () => [{ ...session(), extra: 1 }]],
  ['session Symbol', () => [Object.assign(session(), { [Symbol('s')]: 1 })]],
  ['session heredada', () => [Object.assign(Object.create({ x: 1 }), session())]],
  ['mode inválido', () => [{ ...session(), mode: 'OTHER' }]], ['version inválida', () => [{ ...session(), version: 2 }]],
  ['goalId blanco', () => [{ ...session(), goalId: ' ' }]],
  ['ACTIVE plan null', () => [{ ...session(), plan: null }]],
  ['PENDING plan array', () => [{ ...session(), mode: 'REPLAN_PENDING' }]],
  ['stepCount negativo', () => [{ ...session(), stepCount: -1 }]],
  ['stepCount unsafe', () => [{ ...session(), stepCount: Number.MAX_SAFE_INTEGER + 1 }]],
  ['replanCount float', () => [{ ...session(), replanCount: 1.5 }]],
  ['plan hole', () => [{ ...session(), plan: Array(1) }]],
  ['plan extra index', () => { const p = ['ir_a']; p.extra = 1; return [{ ...session(), plan: p }]; }],
  ['world null', () => [session(), null]], ['world array', () => [session(), []]],
  ['world nested', () => [session(), world({ nested: {} })]],
  ['world NaN', () => [session(), world({ x: NaN })]],
  ['world Infinity', () => [session(), world({ x: Infinity })]],
  ['world Symbol', () => [session(), Object.assign(world(), { [Symbol('x')]: 1 })]],
  ['world heredado', () => [session(), Object.assign(Object.create({ x: 1 }), world())]],
  ['plannerOptions extra', () => [session(), world(), actions(), { unknown: 1 }]],
  ['plannerOptions maxExpansions negativo', () => [session(), world(), actions(), { maxExpansions: -1 }]],
  ['plannerOptions maxExpansions float', () => [session(), world(), actions(), { maxExpansions: 1.5 }]],
  ['plannerOptions maxFrontier cero', () => [session(), world(), actions(), { maxFrontier: 0 }]],
  ['plannerOptions Symbol', () => [session(), world(), actions(), { [Symbol('x')]: 1 }]],
  ['plannerOptions heredado', () => [session(), world(), actions(), Object.assign(Object.create({ x: 1 }), { maxFrontier: 1 })]],
];
for (const [name, make] of invalidAdvance) test(`advance rechaza ${name}`, () => throws(...make()));

function accessor(object, key, descriptor = { get() { throw Error('getter ejecutado'); }, enumerable: true, configurable: true }) { Object.defineProperty(object, key, descriptor); return object; }
test('getter de create input no ejecutado', () => assert.throws(() => create(accessor(makeInitialConfig(), 'goal')), TypeError));
test('getter de goal no ejecutado', () => assert.throws(() => create(makeInitialConfig({ goal: accessor({ playerHelped: true }, 'playerHelped') })), TypeError));
test('getter de relevance no ejecutado', () => assert.throws(() => create(makeInitialConfig({ relevance: accessor({ playerPresent: true }, 'playerPresent') })), TypeError));
test('getter de session no ejecutado', () => throws(accessor(session(), 'goalId')));
test('getter de world no ejecutado', () => throws(session(), accessor(world(), 'at')));
test('setter-only de world rechazado', () => throws(session(), accessor(world(), 'at', { set(_) { throw Error('setter ejecutado'); }, enumerable: true, configurable: true })));
test('getter de plannerOptions no ejecutado', () => throws(session(), world(), actions(), accessor({ maxFrontier: 2 }, 'maxFrontier')));
test('plan accessor index rechazado', () => { const p = ['ir_a']; accessor(p, '0'); assert.throws(() => create(makeInitialConfig({ plan: p })), TypeError); });
test('Proxy ownKeys hostil', () => throws(new Proxy(session(), { ownKeys() { throw Error('trap'); } })));
test('Proxy getPrototypeOf hostil', () => throws(session(), new Proxy(world(), { getPrototypeOf() { throw Error('trap'); } })));
test('Proxy getOwnPropertyDescriptor hostil', () => throws(session(), world(), actions(), new Proxy({}, { getOwnPropertyDescriptor() { throw Error('trap'); } })));
test('Proxy get trap no se ejecuta', () => { const proxy = new Proxy(world(), { get() { throw Error('get trap ejecutado'); } }); assert.equal(run(session(), proxy).status, 'STEP_APPLIED'); });
