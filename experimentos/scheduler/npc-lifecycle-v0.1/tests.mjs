import assert from 'node:assert/strict';
import { EVENT_KINDS, REASON_ORDER, REASON_PRIORITY,
  createSchedulerState, tickScheduler } from './scheduler.mjs';
import { goldenConfig } from './fixtures.mjs';

let passed = 0, failed = 0;
function test(name, fn) {
  try { fn(); passed++; console.log(`PASS ${name}`); }
  catch (error) { failed++; console.error(`FAIL ${name}`, error); }
}
const event = (kind, npcId = 'scheduler_a') => ({ npcId, kind });
const make = (overrides = {}) => createSchedulerState([goldenConfig('scheduler_a', overrides)]);
const tick = (state, turn, events = [], options = {}) => tickScheduler(state, turn, events, options);
function badState(change) {
  const state = tick(make({ firstPeriodicTurn: 100 }), 1).state;
  change(state);
  assert.throws(() => tick(state, 2), TypeError);
}
function noGetter(run) {
  let calls = 0;
  assert.throws(() => run(() => { calls++; throw Error('getter ejecutado'); }), TypeError);
  assert.equal(calls, 0);
}

test('constantes exactas', () => {
  assert.deepEqual(EVENT_KINDS, [
    'PLAN_INVALIDATED', 'ACTION_FINISHED', 'MEMORY_CHANGED', 'WORLD_CHANGED',
  ]);
  assert.deepEqual(REASON_ORDER, [...EVENT_KINDS, 'PERIODIC']);
  assert.deepEqual(REASON_PRIORITY, {
    PLAN_INVALIDATED: 100, ACTION_FINISHED: 80,
    MEMORY_CHANGED: 60, WORLD_CHANGED: 50, PERIODIC: 10,
  });
});
test('estado inicial y orden canónico independiente de configs', () => {
  const configs = [goldenConfig('scheduler_c'), goldenConfig('scheduler_a'), goldenConfig('scheduler_b')];
  const a = createSchedulerState(configs);
  const b = createSchedulerState([...configs].reverse());
  assert.deepEqual(a, b);
  assert.deepEqual(a.npcs.map(x => x.id), ['scheduler_a', 'scheduler_b', 'scheduler_c']);
  assert.equal(a.clock, null);
});
test('Golden A: quieto antes del vencimiento', () => {
  const out = tick(make(), 1);
  assert.equal(out.status, 'DISPATCH_COMPLETE');
  assert.deepEqual(out.dispatches, []);
  assert.equal(out.state.npcs[0].nextPeriodicTurn, 10);
});
test('Golden B: PERIODIC al turn 10', () => {
  const out = tick(make(), 10);
  assert.equal(out.dispatches.length, 1);
  assert.equal(out.dispatches[0].dominantReason, 'PERIODIC');
  assert.deepEqual(out.dispatches[0].reasons, [
    { kind: 'PERIODIC', firstTurn: 10, lastTurn: 10, count: 1 },
  ]);
  assert.equal(out.state.npcs[0].nextPeriodicTurn, 20);
});
test('Golden C: cuatro eventos, un dispatch y count coalescido', () => {
  const out = tick(make({ firstPeriodicTurn: 100 }), 1, [
    event('MEMORY_CHANGED'), event('MEMORY_CHANGED'),
    event('WORLD_CHANGED'), event('ACTION_FINISHED'),
  ]);
  assert.equal(out.dispatches.length, 1);
  assert.equal(out.dispatches[0].dominantReason, 'ACTION_FINISHED');
  assert.deepEqual(out.dispatches[0].reasons.map(x => [x.kind, x.count]), [
    ['ACTION_FINISHED', 1], ['MEMORY_CHANGED', 2], ['WORLD_CHANGED', 1],
  ]);
});
test('Golden D: cooldown retiene razón original hasta turn 25', () => {
  const initial = make({ firstPeriodicTurn: 20, interval: 100, minGap: 5 });
  const first = tick(initial, 20);
  const pending = tick(first.state, 22, [event('MEMORY_CHANGED')]);
  assert.deepEqual(pending.dispatches, []);
  assert.equal(pending.deferredCount, 1);
  assert.deepEqual(pending.state.npcs[0].pendingReasons, [
    { kind: 'MEMORY_CHANGED', firstTurn: 22, lastTurn: 22, count: 1 },
  ]);
  const ready = tick(pending.state, 25);
  assert.equal(ready.dispatches[0].reasons[0].firstTurn, 22);
  assert.equal(ready.state.npcs[0].lastDispatchTurn, 25);
});
test('Golden E: PLAN_INVALIDATED salta minGap', () => {
  const first = tick(make({ firstPeriodicTurn: 20, interval: 100, minGap: 10 }), 20);
  const urgent = tick(first.state, 21, [event('PLAN_INVALIDATED')]);
  assert.equal(urgent.dispatches.length, 1);
  assert.equal(urgent.dispatches[0].dominantReason, 'PLAN_INVALIDATED');
});
test('sólo PLAN_INVALIDATED salta cooldown', () => {
  for (const kind of EVENT_KINDS.filter(x => x !== 'PLAN_INVALIDATED')) {
    const first = tick(make({ firstPeriodicTurn: 20, interval: 100, minGap: 10 }), 20);
    const next = tick(first.state, 21, [event(kind)]);
    assert.deepEqual(next.dispatches, []);
    assert.equal(next.deferredCount, 1);
  }
});
test('Golden F: salto periódico 10/15/20/25 coalesce y avanza a 30', () => {
  const out = tick(make({ firstPeriodicTurn: 10, interval: 5 }), 27);
  assert.equal(out.dispatches.length, 1);
  assert.deepEqual(out.dispatches[0].reasons, [
    { kind: 'PERIODIC', firstTurn: 10, lastTurn: 25, count: 4 },
  ]);
  assert.equal(out.state.npcs[0].nextPeriodicTurn, 30);
});
test('Golden G: budget retiene pendientes y carga finita termina', () => {
  const configs = ['scheduler_a', 'scheduler_b', 'scheduler_c']
    .map(id => goldenConfig(id, { firstPeriodicTurn: 100, minGap: 0 }));
  let state = createSchedulerState(configs);
  const events = configs.map(x => event('MEMORY_CHANGED', x.id));
  const first = tick(state, 1, events, { maxDispatches: 1 });
  assert.equal(first.status, 'BUDGET_EXHAUSTED');
  assert.equal(first.eligibleCount, 3);
  assert.equal(first.deferredCount, 2);
  assert.deepEqual(first.dispatches.map(x => x.npcId), ['scheduler_a']);
  assert.ok(first.state.npcs.slice(1).every(x => x.pendingReasons[0].firstTurn === 1));
  const second = tick(first.state, 2, [], { maxDispatches: 1 });
  const third = tick(second.state, 3, [], { maxDispatches: 1 });
  assert.deepEqual(second.dispatches.map(x => x.npcId), ['scheduler_b']);
  assert.deepEqual(third.dispatches.map(x => x.npcId), ['scheduler_c']);
  assert.ok(second.dispatches[0].reasons[0].firstTurn === 1);
  assert.ok(third.dispatches[0].reasons[0].firstTurn === 1);
  assert.equal(third.deferredCount, 0);
});
test('PLAN_INVALIDATED gana ante PERIODIC bajo budget', () => {
  const state = createSchedulerState([
    goldenConfig('scheduler_a', { firstPeriodicTurn: 10 }),
    goldenConfig('scheduler_b', { firstPeriodicTurn: 100 }),
  ]);
  const out = tick(state, 10, [event('PLAN_INVALIDATED', 'scheduler_b')], { maxDispatches: 1 });
  assert.deepEqual(out.dispatches.map(x => x.npcId), ['scheduler_b']);
  assert.equal(out.state.npcs[0].pendingReasons[0].kind, 'PERIODIC');
});
test('evento y PERIODIC simultáneos producen un dispatch', () => {
  const out = tick(make(), 10, [event('MEMORY_CHANGED')]);
  assert.equal(out.dispatches.length, 1);
  assert.equal(out.dispatches[0].dominantReason, 'MEMORY_CHANGED');
  assert.deepEqual(out.dispatches[0].reasons.map(x => x.kind), ['MEMORY_CHANGED', 'PERIODIC']);
});
test('pending y evento nuevo acumulan razones', () => {
  const first = tick(make({ firstPeriodicTurn: 20, interval: 100, minGap: 5 }), 20);
  const a = tick(first.state, 21, [event('MEMORY_CHANGED')]);
  const b = tick(a.state, 22, [event('WORLD_CHANGED')]);
  assert.deepEqual(b.state.npcs[0].pendingReasons.map(x => x.kind),
    ['MEMORY_CHANGED', 'WORLD_CHANGED']);
  const c = tick(b.state, 25);
  assert.deepEqual(c.dispatches[0].reasons.map(x => x.firstTurn), [21, 22]);
});
test('evento repetido entre ticks conserva first/last/count', () => {
  let state = tick(make({ firstPeriodicTurn: 20, interval: 100, minGap: 10 }), 20).state;
  for (const turn of [21, 22, 23]) state = tick(state, turn, [event('MEMORY_CHANGED')]).state;
  assert.deepEqual(state.npcs[0].pendingReasons, [
    { kind: 'MEMORY_CHANGED', firstTurn: 21, lastTurn: 23, count: 3 },
  ]);
  assert.deepEqual(tick(state, 30).dispatches[0].reasons, state.npcs[0].pendingReasons);
});
test('periodicidad pendiente y salto posterior acumulan count sin backlog', () => {
  const first = tick(make({ firstPeriodicTurn: 10, interval: 5, minGap: 100 }), 10);
  const pending = tick(first.state, 27);
  assert.deepEqual(pending.dispatches, []);
  assert.deepEqual(pending.state.npcs[0].pendingReasons, [
    { kind: 'PERIODIC', firstTurn: 15, lastTurn: 25, count: 3 },
  ]);
  const jumped = tick(pending.state, 100);
  assert.equal(jumped.dispatches.length, 0);
  assert.equal(jumped.state.npcs[0].pendingReasons[0].count, 18);
  assert.equal(jumped.state.npcs[0].nextPeriodicTurn, 105);
});
test('salto 10 a 1000 genera un único dispatch periódico con 199 vencimientos', () => {
  const out = tick(make({ firstPeriodicTurn: 10, interval: 5 }), 1000);
  assert.equal(out.dispatches.length, 1);
  assert.deepEqual(out.dispatches[0].reasons, [
    { kind: 'PERIODIC', firstTurn: 10, lastTurn: 1000, count: 199 },
  ]);
  assert.equal(out.state.npcs[0].nextPeriodicTurn, 1005);
});
test('cooldown pendiente sin elegibles conserva DISPATCH_COMPLETE', () => {
  const first = tick(make({ firstPeriodicTurn: 20, interval: 100, minGap: 10 }), 20);
  const out = tick(first.state, 21, [event('WORLD_CHANGED')]);
  assert.equal(out.status, 'DISPATCH_COMPLETE');
  assert.equal(out.eligibleCount, 0);
  assert.equal(out.deferredCount, 1);
});
test('urgencia incluye razones previas y las limpia en un único dispatch', () => {
  const first = tick(make({ firstPeriodicTurn: 20, interval: 100, minGap: 10 }), 20);
  const pending = tick(first.state, 21, [event('MEMORY_CHANGED')]);
  const urgent = tick(pending.state, 22, [event('PLAN_INVALIDATED')]);
  assert.deepEqual(urgent.dispatches[0].reasons.map(x => x.kind),
    ['PLAN_INVALIDATED', 'MEMORY_CHANGED']);
  assert.equal(urgent.dispatches[0].reasons[1].firstTurn, 21);
  assert.deepEqual(urgent.state.npcs[0].pendingReasons, []);
});
test('orden entre NPC: dominante, antigüedad y ID', () => {
  const configs = ['scheduler_c', 'scheduler_b', 'scheduler_a']
    .map(id => goldenConfig(id, { firstPeriodicTurn: 100, minGap: 0 }));
  const state = createSchedulerState(configs);
  const out = tick(state, 1, [
    event('WORLD_CHANGED', 'scheduler_a'),
    event('MEMORY_CHANGED', 'scheduler_c'),
    event('MEMORY_CHANGED', 'scheduler_b'),
  ], { maxDispatches: 3 });
  assert.deepEqual(out.dispatches.map(x => x.npcId),
    ['scheduler_b', 'scheduler_c', 'scheduler_a']);
});
test('pendiente más antiguo gana tras misma prioridad', () => {
  const configs = ['scheduler_a', 'scheduler_b']
    .map(id => goldenConfig(id, { firstPeriodicTurn: 100, minGap: 0 }));
  const first = tick(createSchedulerState(configs), 1, [event('MEMORY_CHANGED', 'scheduler_b')]);
  const second = tick(first.state, 2, [event('MEMORY_CHANGED', 'scheduler_a')], { maxDispatches: 1 });
  // scheduler_b ya fue despachado: construir dos pending con firstTurn distintos.
  const state = structuredClone(second.state);
  state.npcs[0].pendingReasons = [{ kind: 'MEMORY_CHANGED', firstTurn: 2, lastTurn: 2, count: 1 }];
  state.npcs[1].pendingReasons = [{ kind: 'MEMORY_CHANGED', firstTurn: 1, lastTurn: 1, count: 1 }];
  const out = tick(state, 3, [], { maxDispatches: 1 });
  assert.equal(out.dispatches[0].npcId, 'scheduler_b');
});
test('evento externo PERIODIC se rechaza', () => {
  assert.throws(() => tick(make(), 1, [event('PERIODIC')]), TypeError);
});
test('evento para NPC inexistente se rechaza', () => {
  assert.throws(() => tick(make(), 1, [event('MEMORY_CHANGED', 'missing')]), TypeError);
});
test('orden de eventos equivalentes no cambia resultado', () => {
  const a = [event('WORLD_CHANGED'), event('MEMORY_CHANGED'), event('WORLD_CHANGED')];
  assert.deepEqual(tick(make(), 1, a), tick(make(), 1, [...a].reverse()));
});
test('mismos inputs producen resultado idéntico', () => {
  const state = make(), events = [event('MEMORY_CHANGED')], options = { maxDispatches: 1 };
  assert.deepEqual(tick(state, 1, events, options), tick(state, 1, events, options));
});
test('clock inicial arbitrario y saltos posteriores válidos', () => {
  let state = tick(make({ firstPeriodicTurn: 10, interval: 5 }), 10).state;
  state = tick(state, 20).state;
  state = tick(state, 100).state;
  assert.equal(state.clock, 100);
  assert.equal(state.npcs[0].nextPeriodicTurn, 105);
});
test('clock igual, retroceso, negativo, float y no finito rechazados', () => {
  const state = tick(make(), 5).state;
  for (const turn of [5, 4, -1, 1.5, NaN, Infinity, -Infinity, undefined]) {
    assert.throws(() => tick(state, turn), TypeError);
  }
});
test('overflow de nextPeriodicTurn produce RangeError', () => {
  assert.throws(() => tick(make({ firstPeriodicTurn: Number.MAX_SAFE_INTEGER,
    interval: 1 }), Number.MAX_SAFE_INTEGER), RangeError);
});
test('overflow de pending count produce RangeError', () => {
  const state = tick(make({ firstPeriodicTurn: 100 }), 0).state;
  state.npcs[0].pendingReasons = [{ kind: 'MEMORY_CHANGED', firstTurn: 0,
    lastTurn: 0, count: Number.MAX_SAFE_INTEGER }];
  assert.throws(() => tick(state, 1, [event('MEMORY_CHANGED')]), RangeError);
});
test('config duplicada, id vacío e intervalo inválido', () => {
  assert.throws(() => createSchedulerState([goldenConfig(), goldenConfig()]), TypeError);
  assert.throws(() => createSchedulerState([goldenConfig(' ')]), TypeError);
  for (const interval of [0, -1, 1.5, NaN, Infinity, Symbol('x')]) {
    assert.throws(() => createSchedulerState([goldenConfig('scheduler_a', { interval })]), TypeError);
  }
});
test('config minGap y firstPeriodicTurn inválidos', () => {
  for (const value of [-1, 1.5, NaN, Infinity, undefined]) {
    assert.throws(() => createSchedulerState([goldenConfig('scheduler_a', { minGap: value })]), TypeError);
    assert.throws(() => createSchedulerState([goldenConfig('scheduler_a', { firstPeriodicTurn: value })]), TypeError);
  }
});
test('config getter y setter-only rechazados sin ejecución', () => {
  noGetter(get => {
    const config = goldenConfig();
    Object.defineProperty(config, 'interval', { get });
    return createSchedulerState([config]);
  });
  const config = goldenConfig();
  Object.defineProperty(config, 'id', { set(_) {} });
  assert.throws(() => createSchedulerState([config]), TypeError);
});
test('config heredada, Proxy y Symbol rechazados', () => {
  const config = goldenConfig();
  delete config.interval;
  assert.throws(() => createSchedulerState([
    Object.assign(Object.create({ interval: 10 }), config),
  ]), TypeError);
  assert.throws(() => createSchedulerState([new Proxy(goldenConfig(), {
    ownKeys() { throw Error('hostil'); },
  })]), TypeError);
  assert.throws(() => createSchedulerState([{ ...goldenConfig(), [Symbol('x')]: 1 }]), TypeError);
});
test('config array holes e índice accessor rechazados sin ejecución', () => {
  const array = [goldenConfig(), goldenConfig('scheduler_b')];
  delete array[0];
  assert.throws(() => createSchedulerState(array), TypeError);
  noGetter(get => {
    const configs = [goldenConfig()];
    Object.defineProperty(configs, '0', { get });
    return createSchedulerState(configs);
  });
});
test('state versión, clock y NPC duplicados rechazados', () => {
  badState(s => { s.version = 2; });
  badState(s => { s.clock = NaN; });
  badState(s => { s.npcs.push(structuredClone(s.npcs[0])); });
});
test('state pending reason inválida, count 0 y futuro rechazados', () => {
  badState(s => { s.npcs[0].pendingReasons = [{ kind: 'UNKNOWN', firstTurn: 1, lastTurn: 1, count: 1 }]; });
  badState(s => { s.npcs[0].pendingReasons = [{ kind: 'MEMORY_CHANGED', firstTurn: 1, lastTurn: 1, count: 0 }]; });
  badState(s => { s.npcs[0].pendingReasons = [{ kind: 'MEMORY_CHANGED', firstTurn: 2, lastTurn: 2, count: 1 }]; });
  badState(s => { s.npcs[0].pendingReasons = [{ kind: 'MEMORY_CHANGED', firstTurn: 1, lastTurn: 1, count: Number.MAX_SAFE_INTEGER + 1 }]; });
});
test('state pending reason duplicada se rechaza y orden externo se canoniza', () => {
  badState(s => { s.npcs[0].pendingReasons = [
    { kind: 'MEMORY_CHANGED', firstTurn: 1, lastTurn: 1, count: 1 },
    { kind: 'MEMORY_CHANGED', firstTurn: 1, lastTurn: 1, count: 1 },
  ]; });
  const state = tick(make({ firstPeriodicTurn: 100 }), 1).state;
  state.npcs[0].pendingReasons = [
    { kind: 'WORLD_CHANGED', firstTurn: 1, lastTurn: 1, count: 1 },
    { kind: 'MEMORY_CHANGED', firstTurn: 1, lastTurn: 1, count: 1 },
  ];
  const out = tick(state, 2);
  assert.deepEqual(out.dispatches[0].reasons.map(x => x.kind),
    ['MEMORY_CHANGED', 'WORLD_CHANGED']);
});
test('state nextPeriodicTurn inválido y lastDispatchTurn futuro', () => {
  badState(s => { s.npcs[0].nextPeriodicTurn = 1; });
  badState(s => { s.npcs[0].nextPeriodicTurn = Infinity; });
  badState(s => { s.npcs[0].lastDispatchTurn = 2; });
});
test('state getter y Proxy rechazados sin ejecución', () => {
  noGetter(get => {
    const state = tick(make(), 1).state;
    Object.defineProperty(state.npcs[0], 'pendingReasons', { get });
    return tick(state, 2);
  });
  const state = tick(make(), 1).state;
  assert.throws(() => tick(new Proxy(state, { getPrototypeOf() { throw Error('hostil'); } }), 2), TypeError);
});
test('events holes, índice accessor y no array rechazados', () => {
  const events = [event('MEMORY_CHANGED')];
  delete events[0];
  assert.throws(() => tick(make(), 1, events), TypeError);
  noGetter(get => {
    const array = [event('MEMORY_CHANGED')];
    Object.defineProperty(array, '0', { get });
    return tick(make(), 1, array);
  });
  assert.throws(() => tick(make(), 1, {}), TypeError);
});
test('event getter, heredado, extra, Symbol e inválido rechazados', () => {
  noGetter(get => {
    const item = event('MEMORY_CHANGED');
    Object.defineProperty(item, 'kind', { get });
    return tick(make(), 1, [item]);
  });
  assert.throws(() => tick(make(), 1, [Object.assign(
    Object.create({ npcId: 'scheduler_a' }), { kind: 'MEMORY_CHANGED' })]), TypeError);
  assert.throws(() => tick(make(), 1, [{ ...event('MEMORY_CHANGED'), extra: 1 }]), TypeError);
  assert.throws(() => tick(make(), 1, [{ ...event('MEMORY_CHANGED'), [Symbol('x')]: 1 }]), TypeError);
  assert.throws(() => tick(make(), 1, [event('UNKNOWN')]), TypeError);
  assert.throws(() => tick(make(), 1, [event('MEMORY_CHANGED', '')]), TypeError);
});
test('options getter, rango, extra y Symbol rechazados', () => {
  noGetter(get => {
    const options = {};
    Object.defineProperty(options, 'maxDispatches', { get });
    return tick(make(), 1, [], options);
  });
  for (const maxDispatches of [0, -1, 1.5, NaN, Infinity, undefined]) {
    assert.throws(() => tick(make(), 1, [], { maxDispatches }), TypeError);
  }
  assert.throws(() => tick(make(), 1, [], { extra: 1 }), TypeError);
  assert.throws(() => tick(make(), 1, [], { [Symbol('x')]: 1 }), TypeError);
});
test('inputs intactos y resultados desacoplados', () => {
  const configs = [goldenConfig()], state = createSchedulerState(configs);
  const events = [event('MEMORY_CHANGED')], options = { maxDispatches: 1 };
  const before = structuredClone({ configs, state, events, options });
  const first = tick(state, 1, events, options);
  assert.deepEqual({ configs, state, events, options }, before);
  const expected = tick(state, 1, events, options);
  first.state.npcs[0].id = 'evil';
  first.dispatches[0].reasons[0].count = 999;
  assert.deepEqual({ configs, state, events, options }, before);
  assert.deepEqual(tick(state, 1, events, options), expected);
});
test('estado vacío válido y sin trabajo', () => {
  const out = tick(createSchedulerState([]), 0);
  assert.equal(out.status, 'DISPATCH_COMPLETE');
  assert.deepEqual(out.dispatches, []);
});

console.log(`${passed}/${passed + failed} PASS`);
if (failed) process.exitCode = 1;
