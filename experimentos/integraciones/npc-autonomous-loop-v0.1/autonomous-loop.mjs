import { createMemoryState, memoryStats, recordMemory } from '../../memoria/motor-npc-vivo-v0.3-memory/memory.mjs';
import { decideFromMemory } from '../../memoria/motor-npc-vivo-v0.3.2-decision/decision-pipeline.mjs';
import { createSchedulerState, EVENT_KINDS, tickScheduler } from '../../scheduler/npc-lifecycle-v0.1/scheduler.mjs';
import { createExecutionSession, advanceExecutionSession } from '../../execution/npc-executor-replanning-v0.1/execution-session.mjs';
import { GOAP_ACTIONS } from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import { factsMatch } from '../../goap/motor-npc-vivo-v0.2-goap/goap.mjs';
import { validateNpc, validateActionContext } from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';

const CONTEXT_FIELDS = ['playerPresent', 'playerRequestsHelp', 'playerRank', 'dutyImportance',
  'danger', 'missionUrgency', 'anomalyPresent', 'awayFromPost', 'superiorReachable',
  'relevantKnowledge', 'dutyMode'];
const MAX = Number.MAX_SAFE_INTEGER;

function fail(message) { throw new TypeError(`Autonomous loop: ${message}`); }
function lexical(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
function id(value, label) {
  if (typeof value !== 'string' || value.trim().length === 0) fail(`${label} debe ser string no vacío`);
  return value;
}
function safeTurn(value, label) {
  if (!Number.isSafeInteger(value) || value < 0) fail(`${label} debe ser entero seguro >= 0`);
  return value;
}
function increment(value, label) {
  if (value === MAX) throw new RangeError(`${label} excede entero seguro`);
  return value + 1;
}

function descriptors(value, label, asArray = false) {
  try {
    if (asArray ? !Array.isArray(value) : value === null || typeof value !== 'object' || Array.isArray(value)) fail(`${label} debe ser ${asArray ? 'array' : 'objeto plano'}`);
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== (asArray ? Array.prototype : Object.prototype) && !(prototype === null && !asArray)) fail(`${label} tiene herencia`);
    const keys = Reflect.ownKeys(value);
    if (keys.some(key => typeof key !== 'string')) fail(`${label} contiene Symbol`);
    return keys.map(key => {
      const descriptor = Object.getOwnPropertyDescriptor(value, key);
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(`${label}.${key} es accessor`);
      return [key, descriptor.value];
    });
  } catch (error) {
    if (error instanceof TypeError && error.message.startsWith('Autonomous loop:')) throw error;
    fail(`${label} no admite inspección estructural`);
  }
}

function record(value, fields, label, optional = []) {
  const entries = descriptors(value, label);
  const allowed = [...fields, ...optional];
  if (entries.some(([key]) => !allowed.includes(key)) || fields.some(field => !entries.some(([key]) => key === field))) fail(`${label} tiene campos inválidos`);
  return Object.fromEntries(entries);
}

function array(value, label) {
  const entries = descriptors(value, label, true);
  const length = entries.find(([key]) => key === 'length')?.[1];
  if (!Number.isSafeInteger(length) || length < 0 || entries.length !== length + 1) fail(`${label} tiene huecos o propiedades extra`);
  const byKey = new Map(entries);
  const result = [];
  for (let index = 0; index < length; index++) {
    if (!byKey.has(String(index))) fail(`${label}[${index}] es hueco`);
    result.push(byKey.get(String(index)));
  }
  return result;
}

function copyPlain(value, label, seen = new WeakSet()) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (value === null || typeof value !== 'object') fail(`${label} contiene valor no primitivo compatible`);
  if (seen.has(value)) fail(`${label} contiene ciclo`);
  seen.add(value);
  let result;
  if (Array.isArray(value)) {
    result = array(value, label).map((item, index) => copyPlain(item, `${label}[${index}]`, seen));
  } else {
    result = Object.fromEntries(descriptors(value, label).sort(([a], [b]) => lexical(a, b))
      .map(([key, item]) => [key, copyPlain(item, `${label}.${key}`, seen)]));
  }
  seen.delete(value);
  return result;
}

function facts(value, label) {
  const entries = descriptors(value, label);
  if (entries.some(([key]) => key.length === 0)) fail(`${label} tiene clave vacía`);
  for (const [key, item] of entries) {
    if (!(item === null || typeof item === 'boolean' || typeof item === 'string' ||
      (typeof item === 'number' && Number.isFinite(item)))) fail(`${label}.${key} debe ser fact primitivo`);
  }
  return Object.fromEntries(entries.sort(([a], [b]) => lexical(a, b)));
}

function context(value) {
  const raw = record(value, CONTEXT_FIELDS, 'utilityContext');
  const snapshot = Object.fromEntries(CONTEXT_FIELDS.map(key => [key, raw[key]]));
  const errors = validateActionContext(snapshot);
  if (errors.length) fail(`utilityContext inválido: ${errors.join(' · ')}`);
  return snapshot;
}

function coherent(world, ctx) {
  for (const key of ['playerPresent', 'playerNeedsHelp', 'playerHelped', 'anomalyPresent', 'anomalyInvestigated']) {
    if (typeof world[key] !== 'boolean') fail(`world.${key} debe ser boolean`);
  }
  if (typeof world.at !== 'string') fail('world.at debe ser string');
  for (const key of ['dutyImportance', 'danger', 'urgency']) {
    if (typeof world[key] !== 'number' || !Number.isFinite(world[key])) fail(`world.${key} debe ser número finito`);
  }
  const pairs = [
    [ctx.playerPresent, world.playerPresent],
    [ctx.playerRequestsHelp, world.playerNeedsHelp && !world.playerHelped],
    [ctx.anomalyPresent, world.anomalyPresent && !world.anomalyInvestigated],
    [ctx.awayFromPost, world.at !== 'puesto'],
    [ctx.dutyImportance, world.dutyImportance],
    [ctx.danger, world.danger],
    [ctx.missionUrgency, world.urgency],
  ];
  if (pairs.some(([actual, expected]) => !Object.is(actual, expected))) fail('world y utilityContext incoherentes');
}

function syncContext(world, ctx) {
  return { ...ctx, playerPresent: world.playerPresent,
    playerRequestsHelp: world.playerNeedsHelp && !world.playerHelped,
    anomalyPresent: world.anomalyPresent && !world.anomalyInvestigated,
    awayFromPost: world.at !== 'puesto', dutyImportance: world.dutyImportance,
    danger: world.danger, missionUrgency: world.urgency };
}

function factsEqual(a, b) {
  const ak = Object.keys(a).sort(), bk = Object.keys(b).sort();
  return ak.length === bk.length && ak.every((key, index) => key === bk[index] && Object.is(a[key], b[key]));
}

function captureNpc(value) {
  const npc = copyPlain(value, 'npc');
  record(npc, ['id', 'name', 'role', 'traits', 'relationPlayer', 'knowledge', 'behaviorState'], 'npc');
  const errors = validateNpc(npc);
  if (errors.length) fail(`npc inválido: ${errors.join(' · ')}`);
  safeTurn(npc.behaviorState.consecutiveTurns, 'npc.behaviorState.consecutiveTurns');
  return npc;
}

function captureSession(value) {
  if (value === null) return null;
  const session = copyPlain(value, 'executionSession');
  record(session, ['version', 'mode', 'goalId', 'goal', 'relevance', 'plan', 'stepCount', 'replanCount'], 'executionSession');
  if (session.version !== 1 || !['ACTIVE', 'REPLAN_PENDING'].includes(session.mode)) fail('executionSession mode/version inválido');
  id(session.goalId, 'executionSession.goalId');
  facts(session.goal, 'executionSession.goal'); facts(session.relevance, 'executionSession.relevance');
  if (session.mode === 'ACTIVE') {
    for (const actionId of array(session.plan, 'executionSession.plan')) id(actionId, 'executionSession.plan ID');
  } else if (session.plan !== null) fail('REPLAN_PENDING requiere plan null');
  safeTurn(session.stepCount, 'executionSession.stepCount');
  safeTurn(session.replanCount, 'executionSession.replanCount');
  return session;
}

function captureRuntime(raw) {
  const value = record(raw, ['id', 'npc', 'memory', 'world', 'utilityContext', 'executionSession'], 'runtime');
  id(value.id, 'runtime.id');
  const npc = captureNpc(value.npc);
  if (npc.id !== value.id) fail('runtime.id no coincide con npc.id');
  const memory = copyPlain(value.memory, 'runtime.memory');
  const world = facts(value.world, 'runtime.world');
  const utilityContext = context(value.utilityContext);
  coherent(world, utilityContext);
  return { id: value.id, npc, memory, world, utilityContext,
    executionSession: captureSession(value.executionSession) };
}

function captureState(state) {
  const top = record(state, ['version', 'clock', 'scheduler', 'npcs'], 'state');
  if (top.version !== 1) fail('state.version debe ser 1');
  if (top.clock !== null) safeTurn(top.clock, 'state.clock');
  const scheduler = copyPlain(top.scheduler, 'state.scheduler');
  if (scheduler?.clock !== top.clock) fail('state.clock y scheduler.clock difieren');
  const npcs = array(top.npcs, 'state.npcs').map(captureRuntime);
  const ids = new Set();
  for (const runtime of npcs) {
    if (ids.has(runtime.id)) fail('runtime.id duplicado');
    ids.add(runtime.id);
    memoryStats(runtime.memory, top.clock ?? 0); // El módulo Memory valida su contrato.
  }
  const schedulerIds = array(scheduler.npcs, 'state.scheduler.npcs').map(item => id(record(item,
    ['id', 'interval', 'minGap', 'nextPeriodicTurn', 'lastDispatchTurn', 'pendingReasons'], 'scheduler NPC').id, 'scheduler NPC id'));
  if (schedulerIds.length !== ids.size || schedulerIds.some(item => !ids.has(item))) fail('IDs de scheduler y runtimes no coinciden');
  npcs.sort((a, b) => lexical(a.id, b.id));
  return { version: 1, clock: top.clock, scheduler, npcs };
}

function captureMemoryEvent(raw, currentTurn) {
  const event = record(raw, ['key', 'kind', 'subject', 'value', 'importance', 'confidence', 'turn'], 'memory event', ['expiresTurn']);
  id(event.key, 'memory event.key');
  if (event.turn !== currentTurn) fail('memory event.turn debe coincidir con currentTurn');
  return copyPlain(event, 'memory event');
}

function captureInput(input, currentTurn, ids) {
  const top = record(input, [], 'input', ['observations', 'schedulerEvents']);
  const observations = array(top.observations ?? [], 'input.observations').map(raw => {
    const observation = record(raw, ['npcId', 'world', 'utilityContext', 'memoryEvents'], 'observation');
    id(observation.npcId, 'observation.npcId');
    if (!ids.has(observation.npcId)) fail('observation NPC inexistente');
    const world = facts(observation.world, 'observation.world');
    const utilityContext = context(observation.utilityContext);
    coherent(world, utilityContext);
    const memoryEvents = array(observation.memoryEvents, 'observation.memoryEvents')
      .map(event => captureMemoryEvent(event, currentTurn));
    const keys = new Set();
    for (const event of memoryEvents) {
      if (keys.has(event.key)) fail('memory event.key duplicada en tick');
      keys.add(event.key);
    }
    memoryEvents.sort((a, b) => lexical(a.key, b.key));
    return { npcId: observation.npcId, world, utilityContext, memoryEvents };
  });
  const seen = new Set();
  for (const observation of observations) {
    if (seen.has(observation.npcId)) fail('observation.npcId duplicado');
    seen.add(observation.npcId);
  }
  observations.sort((a, b) => lexical(a.npcId, b.npcId));
  const schedulerEvents = array(top.schedulerEvents ?? [], 'input.schedulerEvents').map(raw => {
    const event = record(raw, ['npcId', 'kind'], 'scheduler event');
    id(event.npcId, 'scheduler event.npcId');
    if (!ids.has(event.npcId) || !EVENT_KINDS.includes(event.kind)) fail('scheduler event inválido');
    return event;
  });
  return { observations, schedulerEvents };
}

function captureOptions(options) {
  const top = record(options, [], 'options', ['scheduler', 'planner']);
  const scheduler = top.scheduler === undefined ? {} : record(top.scheduler, [], 'options.scheduler', ['maxDispatches']);
  if (Object.hasOwn(scheduler, 'maxDispatches')) safeTurn(scheduler.maxDispatches, 'maxDispatches');
  if (Object.hasOwn(scheduler, 'maxDispatches') && scheduler.maxDispatches < 1) fail('maxDispatches debe ser >= 1');
  const planner = top.planner === undefined ? {} : record(top.planner, [], 'options.planner', ['maxExpansions', 'maxFrontier']);
  if (Object.hasOwn(planner, 'maxExpansions') && (!Number.isInteger(planner.maxExpansions) || planner.maxExpansions < 0)) fail('maxExpansions inválido');
  if (Object.hasOwn(planner, 'maxFrontier') && (!Number.isInteger(planner.maxFrontier) || planner.maxFrontier < 1)) fail('maxFrontier inválido');
  return { scheduler, planner };
}

export function createAutonomousLoopState(input) {
  const top = record(input, ['schedulerConfigs', 'npcs'], 'create input');
  const schedulerConfigs = array(top.schedulerConfigs, 'schedulerConfigs').map(raw => copyPlain(raw, 'scheduler config'));
  const scheduler = createSchedulerState(schedulerConfigs);
  const npcs = array(top.npcs, 'npcs').map(raw => {
    const item = record(raw, ['npc', 'world', 'utilityContext'], 'initial NPC');
    const npc = captureNpc(item.npc);
    const world = facts(item.world, 'initial world');
    const utilityContext = context(item.utilityContext);
    coherent(world, utilityContext);
    return { id: npc.id, npc, memory: createMemoryState(), world, utilityContext, executionSession: null };
  });
  const ids = new Set();
  for (const runtime of npcs) {
    if (ids.has(runtime.id)) fail('npc.id duplicado');
    ids.add(runtime.id);
  }
  if (scheduler.npcs.length !== ids.size || scheduler.npcs.some(item => !ids.has(item.id))) fail('schedulerConfigs y NPC IDs no coinciden');
  npcs.sort((a, b) => lexical(a.id, b.id));
  return { version: 1, clock: null, scheduler, npcs };
}

export function tickAutonomousLoop(state, currentTurn, input = {}, options = {}) {
  const next = captureState(state);
  safeTurn(currentTurn, 'currentTurn');
  if (next.clock !== null && currentTurn <= next.clock) fail('currentTurn debe superar state.clock');
  const byId = new Map(next.npcs.map(runtime => [runtime.id, runtime]));
  const capturedInput = captureInput(input, currentTurn, new Set(byId.keys()));
  const capturedOptions = captureOptions(options);
  const worldChanged = [];
  const memoryChanged = [];
  for (const observation of capturedInput.observations) {
    const runtime = byId.get(observation.npcId);
    if (!factsEqual(runtime.world, observation.world) || !factsEqual(runtime.utilityContext, observation.utilityContext)) {
      worldChanged.push(observation.npcId);
    }
    runtime.world = observation.world;
    runtime.utilityContext = observation.utilityContext;
    for (const event of observation.memoryEvents) runtime.memory = recordMemory(runtime.memory, event);
    if (observation.memoryEvents.length) memoryChanged.push(observation.npcId);
  }
  const generatedSchedulerEvents = [
    ...worldChanged.map(npcId => ({ npcId, kind: 'WORLD_CHANGED' })),
    ...memoryChanged.map(npcId => ({ npcId, kind: 'MEMORY_CHANGED' })),
  ];
  const scheduled = tickScheduler(next.scheduler, currentTurn,
    [...generatedSchedulerEvents, ...capturedInput.schedulerEvents], capturedOptions.scheduler);
  next.clock = currentTurn;
  next.scheduler = scheduled.state;
  const dispatchResults = [];
  for (const dispatch of scheduled.dispatches) {
    const runtime = byId.get(dispatch.npcId);
    if (runtime.executionSession === null) {
      const decision = decideFromMemory(runtime.npc, runtime.memory, currentTurn,
        runtime.utilityContext, runtime.world, capturedOptions.planner);
      const utilityAction = decision.utilityDecision.action;
      const behavior = runtime.npc.behaviorState;
      const consecutiveTurns = behavior.lastAction === utilityAction
        ? increment(behavior.consecutiveTurns, 'behaviorState.consecutiveTurns')
        : 1;
      runtime.npc.behaviorState = { lastAction: utilityAction, consecutiveTurns };
      let status;
      if (decision.status === 'PLAN_READY') {
        if (decision.plan.plan.length === 0) {
          if (!factsMatch(runtime.world, decision.goal)) {
            throw new Error('Decision Pipeline devolvió un plan vacío para un goal no satisfecho');
          }
          status = 'DECISION_GOAL_ALREADY_SATISFIED';
        } else {
          runtime.executionSession = createExecutionSession({ goalId: decision.goalId,
            goal: decision.goal, relevance: decision.relevance, plan: decision.plan.plan });
          status = 'PLAN_SESSION_CREATED';
        }
      } else if (decision.status === 'UTILITY_ACTION_UNMAPPED') status = 'UTILITY_ACTION_UNMAPPED';
      else if (decision.status === 'NO_PLAN') status = 'DECISION_NO_PLAN';
      else if (decision.status === 'PLANNING_DEFERRED') status = 'DECISION_PLANNING_DEFERRED';
      else throw new Error(`Estado Decision Pipeline inesperado: ${decision.status}`);
      dispatchResults.push({ npcId: runtime.id, turn: currentTurn, schedulerReason: dispatch.dominantReason,
        path: 'DECISION', status, utilityAction, goalId: decision.goalId,
        executed: null, executionStatus: null, plannerStatus: decision.plan?.status ?? null,
        derivedRelations: { ...decision.relationDerivation.relations } });
    } else {
      const previousGoalId = runtime.executionSession.goalId;
      const execution = advanceExecutionSession(runtime.executionSession, runtime.world,
        GOAP_ACTIONS, capturedOptions.planner);
      runtime.world = execution.world;
      runtime.utilityContext = syncContext(runtime.world, runtime.utilityContext);
      runtime.executionSession = execution.session;
      dispatchResults.push({ npcId: runtime.id, turn: currentTurn, schedulerReason: dispatch.dominantReason,
        path: 'EXECUTION', status: execution.status, utilityAction: null, goalId: previousGoalId,
        executed: execution.executed, executionStatus: execution.status,
        plannerStatus: execution.replan?.plannerStatus ?? null, derivedRelations: null });
    }
  }
  return { status: scheduled.status === 'BUDGET_EXHAUSTED' ? 'SCHEDULER_BUDGET_EXHAUSTED' : 'TICK_COMPLETE',
    state: next,
    scheduler: { status: scheduled.status, dispatches: scheduled.dispatches,
      eligibleCount: scheduled.eligibleCount, deferredCount: scheduled.deferredCount },
    dispatchResults, generatedEvents: { worldChanged, memoryChanged } };
}
