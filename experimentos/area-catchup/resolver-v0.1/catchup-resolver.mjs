// Laboratorio sintético: transforma un snapshot temporal sin ejecutar turnos.
function fail(message) {
  throw new TypeError(`Area catch-up: ${message}`);
}

function record(value, fields, label) {
  try {
    if (value === null || typeof value !== 'object' || Array.isArray(value)) fail(`${label} debe ser objeto plano`);
    const prototype = Object.getPrototypeOf(value);
    if (prototype !== Object.prototype && prototype !== null) fail(`${label} tiene herencia`);
    const keys = Reflect.ownKeys(value);
    if (keys.length !== fields.length || keys.some(key => typeof key !== 'string' || !fields.includes(key))) fail(`${label} tiene campos inválidos`);
    const result = Object.create(null);
    for (const field of fields) {
      const descriptor = Object.getOwnPropertyDescriptor(value, field);
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(`${label}.${field} es accesor o falta`);
      result[field] = descriptor.value;
    }
    return result;
  } catch (error) {
    if (error instanceof TypeError && error.message.startsWith('Area catch-up:')) throw error;
    fail(`${label} no admite inspección estructural`);
  }
}

function array(value, label) {
  try {
    if (!Array.isArray(value) || Object.getPrototypeOf(value) !== Array.prototype) fail(`${label} debe ser array ordinario`);
    const length = Object.getOwnPropertyDescriptor(value, 'length');
    if (!length || !Object.hasOwn(length, 'value')) fail(`${label} no tiene longitud válida`);
    const keys = Reflect.ownKeys(value);
    if (keys.length !== length.value + 1) fail(`${label} tiene huecos o propiedades extra`);
    const result = [];
    for (let index = 0; index < length.value; index++) {
      const descriptor = Object.getOwnPropertyDescriptor(value, String(index));
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) fail(`${label}[${index}] es hueco o accesor`);
      result.push(descriptor.value);
    }
    return result;
  } catch (error) {
    if (error instanceof TypeError && error.message.startsWith('Area catch-up:')) throw error;
    fail(`${label} no admite inspección estructural`);
  }
}

function id(value, label) {
  if (typeof value !== 'string' || value.length === 0) fail(`${label} debe ser string no vacío`);
  return value;
}

function integer(value, label, nonnegative = false) {
  if (!Number.isSafeInteger(value) || (nonnegative && value < 0)) fail(`${label} debe ser entero seguro${nonnegative ? ' no negativo' : ''}`);
  return value;
}

function lexical(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
function eventOrder(a, b) { return a.dueTurn - b.dueTurn || lexical(a.id, b.id); }

function snapshot(state, catchUp) {
  const source = record(state, ['version', 'areaId', 'syncedTurn', 'entities', 'scheduledEvents'], 'state');
  if (source.version !== 1) fail('version debe ser 1');
  id(source.areaId, 'areaId');
  integer(source.syncedTurn, 'syncedTurn', true);
  const request = record(catchUp, ['areaId', 'fromTurn', 'toTurn', 'elapsedTurns'], 'catchUp');
  id(request.areaId, 'catchUp.areaId');
  for (const field of ['fromTurn', 'toTurn', 'elapsedTurns']) integer(request[field], `catchUp.${field}`, true);
  if (request.areaId !== source.areaId || request.fromTurn !== source.syncedTurn ||
      request.toTurn <= request.fromTurn || request.elapsedTurns < 1 ||
      request.elapsedTurns !== request.toTurn - request.fromTurn) fail('catchUp no coincide con state');

  const entityIds = new Set();
  const entities = array(source.entities, 'entities').map((raw, index) => {
    const entity = record(raw, ['id', 'timers', 'meters'], `entities[${index}]`);
    id(entity.id, 'entity.id');
    if (entityIds.has(entity.id)) fail('entity.id duplicado');
    entityIds.add(entity.id);
    const timerIds = new Set();
    const timers = array(entity.timers, 'timers').map(rawTimer => {
      const timer = record(rawTimer, ['id', 'remainingTurns'], 'timer');
      id(timer.id, 'timer.id');
      if (timerIds.has(timer.id)) fail('timer.id duplicado');
      timerIds.add(timer.id);
      integer(timer.remainingTurns, 'remainingTurns', true);
      return { id: timer.id, remainingTurns: timer.remainingTurns };
    });
    const meterIds = new Set();
    const meters = array(entity.meters, 'meters').map(rawMeter => {
      const meter = record(rawMeter, ['id', 'value', 'ratePerTurn', 'min', 'max'], 'meter');
      id(meter.id, 'meter.id');
      if (meterIds.has(meter.id)) fail('meter.id duplicado');
      meterIds.add(meter.id);
      for (const field of ['value', 'ratePerTurn', 'min', 'max']) integer(meter[field], `meter.${field}`);
      if (meter.min > meter.value || meter.value > meter.max) fail('meter fuera de límites');
      return { id: meter.id, value: meter.value, ratePerTurn: meter.ratePerTurn, min: meter.min, max: meter.max };
    });
    return { id: entity.id, timers, meters };
  });
  const eventIds = new Set();
  const scheduledEvents = array(source.scheduledEvents, 'scheduledEvents').map(rawEvent => {
    const event = record(rawEvent, ['id', 'targetId', 'kind', 'dueTurn'], 'event');
    id(event.id, 'event.id');
    if (eventIds.has(event.id)) fail('event.id duplicado');
    eventIds.add(event.id);
    if (event.targetId !== null && !entityIds.has(id(event.targetId, 'event.targetId'))) fail('event.targetId inexistente');
    id(event.kind, 'event.kind');
    integer(event.dueTurn, 'event.dueTurn', true);
    if (event.dueTurn <= source.syncedTurn) fail('event.dueTurn ya vencido');
    return { id: event.id, targetId: event.targetId, kind: event.kind, dueTurn: event.dueTurn };
  });
  return { source, request, entities, scheduledEvents };
}

export function resolveAreaCatchUp(state, catchUp) {
  const { source, request, entities, scheduledEvents } = snapshot(state, catchUp);
  const completedTimers = [];
  const meterChanges = [];
  const elapsed = BigInt(request.elapsedTurns);
  entities.sort((a, b) => lexical(a.id, b.id));
  for (const entity of entities) {
    entity.timers.sort((a, b) => lexical(a.id, b.id));
    entity.meters.sort((a, b) => lexical(a.id, b.id));
    for (const timer of entity.timers) {
      const previous = timer.remainingTurns;
      timer.remainingTurns = Math.max(0, previous - request.elapsedTurns);
      if (previous > 0 && timer.remainingTurns === 0) completedTimers.push({ entityId: entity.id, timerId: timer.id, previousRemainingTurns: previous, remainingTurns: 0 });
    }
    for (const meter of entity.meters) {
      const previous = meter.value;
      // BigInt keeps the product and even (max - min) exact at the safe-integer extremes.
      const raw = BigInt(previous) + BigInt(meter.ratePerTurn) * elapsed;
      const capped = raw < BigInt(meter.min) ? BigInt(meter.min) : raw > BigInt(meter.max) ? BigInt(meter.max) : raw;
      meter.value = Number(capped); // The cap is a validated safe integer.
      if (meter.value !== previous) meterChanges.push({ entityId: entity.id, meterId: meter.id, previousValue: previous, value: meter.value });
    }
  }
  scheduledEvents.sort(eventOrder);
  const dueEvents = [];
  const pending = [];
  for (const event of scheduledEvents) (event.dueTurn <= request.toTurn ? dueEvents : pending).push(event);
  return {
    status: 'CATCH_UP_APPLIED',
    state: { version: 1, areaId: source.areaId, syncedTurn: request.toTurn, entities, scheduledEvents: pending },
    summary: { areaId: source.areaId, fromTurn: request.fromTurn, toTurn: request.toTurn,
      elapsedTurns: request.elapsedTurns, completedTimers, meterChanges, dueEvents }
  };
}
