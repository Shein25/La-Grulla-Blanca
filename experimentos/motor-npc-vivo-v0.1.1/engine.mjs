export const KNOWLEDGE = Object.freeze({
  DESCONOCIDO: 0,
  SOSPECHA: 1,
  SABE: 2,
  CONFIRMADO: 3,
});

export const RANKS = Object.freeze({
  ASPIRANTE: 0,
  EXTERNO: 1,
  INTERNO: 2,
  PRIMERA_ALA: 3,
  INSTRUCTOR: 4,
  ANCIANO: 5,
  CONSEJO: 6,
});

export const ACTION_ORDER = Object.freeze([
  'vigilar',
  'trabajar',
  'patrullar',
  'hablar_jugador',
  'ayudar_jugador',
  'investigar',
  'informar_superior',
  'regresar_puesto',
  'esperar',
]);

export const DUTY_MODES = Object.freeze(['vigilar', 'trabajar', 'patrullar', 'ninguno']);

const REQUIRED_TRAITS = Object.freeze([
  'disciplina', 'sociabilidad', 'curiosidad', 'prudencia', 'lealtad_institucional', 'empatia',
]);
const REQUIRED_RELATION = Object.freeze([
  'afinidad', 'confianza', 'respeto', 'deuda', 'temor', 'rivalidad',
]);
const REQUIRED_KNOWLEDGE = Object.freeze(['R1', 'R2', 'R3']);
const REQUIRED_ACTION_CONTEXT = Object.freeze([
  'playerPresent', 'playerRequestsHelp', 'playerRank', 'dutyImportance', 'danger', 'missionUrgency',
  'anomalyPresent', 'awayFromPost', 'superiorReachable', 'relevantKnowledge', 'dutyMode',
]);

const clamp = (n, min = 0, max = 100) => Math.max(min, Math.min(max, n));
const pct = n => clamp(n);
const rankNorm = rank => clamp(rank / 6 * 100);
const KNOWLEDGE_STATES = Object.freeze(['DESCONOCIDO', 'SOSPECHA', 'SABE', 'CONFIRMADO']);
const isKnowledgeState = state => typeof state === 'string' && KNOWLEDGE_STATES.includes(state);
const knowledgeNorm = state => clamp(KNOWLEDGE[state] / 3 * 100);
const isPlainObject = x => {
  if (!x || typeof x !== 'object' || Array.isArray(x)) return false;
  const proto = Object.getPrototypeOf(x);
  return proto === Object.prototype || proto === null;
};

function readOwnData(obj, key, path, errors) {
  const desc = Object.getOwnPropertyDescriptor(obj, key);
  if (!desc) {
    errors.push(`Falta ${path}`);
    return undefined;
  }
  if (!Object.hasOwn(desc, 'value')) {
    errors.push(`${path} debe ser una propiedad de datos; accessors no permitidos`);
    return undefined;
  }
  return desc.value;
}

function exactKeys(obj, required, path, errors) {
  if (!isPlainObject(obj)) { errors.push(`Falta ${path}`); return; }
  const keys = Object.keys(obj).sort();
  const expected = [...required].sort();
  if (keys.join('|') !== expected.join('|')) {
    const missing = expected.filter(k => !keys.includes(k));
    const extra = keys.filter(k => !expected.includes(k));
    if (missing.length) errors.push(`${path}: faltan ${missing.join(', ')}`);
    if (extra.length) errors.push(`${path}: sobran ${extra.join(', ')}`);
  }
}

function validatePctFields(obj, required, path, errors) {
  exactKeys(obj, required, path, errors);
  if (!isPlainObject(obj)) return;
  for (const key of required) {
    const value = readOwnData(obj, key, `${path}.${key}`, errors);
    if (value !== undefined && (!Number.isFinite(value) || value < 0 || value > 100)) errors.push(`${path}.${key} fuera de 0..100`);
  }
}

export function validateNpc(npc) {
  const errors = [];
  if (!isPlainObject(npc)) return ['NPC inválido'];

  const id = readOwnData(npc, 'id', 'id', errors);
  const name = readOwnData(npc, 'name', 'name', errors);
  const role = readOwnData(npc, 'role', 'role', errors);
  const traits = readOwnData(npc, 'traits', 'traits', errors);
  const relationPlayer = readOwnData(npc, 'relationPlayer', 'relationPlayer', errors);
  const knowledge = readOwnData(npc, 'knowledge', 'knowledge', errors);
  const behaviorState = readOwnData(npc, 'behaviorState', 'behaviorState', errors);

  if (id !== undefined && (typeof id !== 'string' || !id.trim())) errors.push('id inválido');
  if (name !== undefined && (typeof name !== 'string' || !name.trim())) errors.push('name inválido');
  if (role !== undefined && (typeof role !== 'string' || !role.trim())) errors.push('role inválido');

  validatePctFields(traits, REQUIRED_TRAITS, 'traits', errors);
  validatePctFields(relationPlayer, REQUIRED_RELATION, 'relationPlayer', errors);

  exactKeys(knowledge, REQUIRED_KNOWLEDGE, 'knowledge', errors);
  if (isPlainObject(knowledge)) {
    for (const key of REQUIRED_KNOWLEDGE) {
      const value = readOwnData(knowledge, key, `knowledge.${key}`, errors);
      if (value !== undefined && !isKnowledgeState(value)) errors.push(`knowledge.${key} inválido: ${value}`);
    }
  }

  if (!isPlainObject(behaviorState)) {
    if (behaviorState !== undefined) errors.push('behaviorState inválido');
  } else {
    exactKeys(behaviorState, ['lastAction', 'consecutiveTurns'], 'behaviorState', errors);
    const lastAction = readOwnData(behaviorState, 'lastAction', 'behaviorState.lastAction', errors);
    const consecutiveTurns = readOwnData(behaviorState, 'consecutiveTurns', 'behaviorState.consecutiveTurns', errors);
    if (lastAction !== undefined && !(lastAction === null || ACTION_ORDER.includes(lastAction))) errors.push('behaviorState.lastAction inválido');
    if (consecutiveTurns !== undefined && (!Number.isInteger(consecutiveTurns) || consecutiveTurns < 0)) errors.push('behaviorState.consecutiveTurns inválido');
    if (lastAction === null && consecutiveTurns !== undefined && consecutiveTurns !== 0) errors.push('behaviorState inconsistente: sin acción debe tener consecutiveTurns=0');
    if (lastAction !== undefined && lastAction !== null && consecutiveTurns !== undefined && consecutiveTurns < 1) errors.push('behaviorState inconsistente: con acción debe tener consecutiveTurns>=1');
  }
  return errors;
}

export function validateActionContext(context) {
  const errors = [];
  if (!isPlainObject(context)) return ['Contexto inválido'];

  const values = {};
  for (const key of REQUIRED_ACTION_CONTEXT) values[key] = readOwnData(context, key, `context.${key}`, errors);

  for (const key of ['playerPresent', 'playerRequestsHelp', 'anomalyPresent', 'awayFromPost', 'superiorReachable']) {
    const value = values[key];
    if (value !== undefined && typeof value !== 'boolean') errors.push(`context.${key} debe ser boolean`);
  }
  for (const key of ['dutyImportance', 'danger', 'missionUrgency']) {
    const value = values[key];
    if (value !== undefined && (!Number.isFinite(value) || value < 0 || value > 100)) errors.push(`context.${key} fuera de 0..100`);
  }
  if (values.playerRank !== undefined && (!Number.isInteger(values.playerRank) || values.playerRank < 0 || values.playerRank > 6)) errors.push('context.playerRank fuera de 0..6');
  if (values.relevantKnowledge !== undefined && !isKnowledgeState(values.relevantKnowledge)) errors.push('context.relevantKnowledge inválido');
  if (values.dutyMode !== undefined && !DUTY_MODES.includes(values.dutyMode)) errors.push('context.dutyMode inválido');
  return errors;
}

export function validateDialogueContext(context) {
  const errors = [];
  if (!isPlainObject(context)) return ['Contexto de diálogo inválido'];

  const playerRank = readOwnData(context, 'playerRank', 'dialogue.playerRank', errors);
  const topicSensitivity = readOwnData(context, 'topicSensitivity', 'dialogue.topicSensitivity', errors);
  const formalRestriction = readOwnData(context, 'formalRestriction', 'dialogue.formalRestriction', errors);

  if (playerRank !== undefined && (!Number.isInteger(playerRank) || playerRank < 0 || playerRank > 6)) errors.push('dialogue.playerRank fuera de 0..6');
  for (const [key, value] of [['topicSensitivity', topicSensitivity], ['formalRestriction', formalRestriction]]) {
    if (value !== undefined && (!Number.isFinite(value) || value < 0 || value > 100)) errors.push(`dialogue.${key} fuera de 0..100`);
  }
  return errors;
}

function assertValidNpc(npc) {
  const errors = validateNpc(npc);
  if (errors.length) throw new TypeError(`NPC inválido: ${errors.join(' · ')}`);
}
function assertValidActionContext(context) {
  const errors = validateActionContext(context);
  if (errors.length) throw new TypeError(`Contexto inválido: ${errors.join(' · ')}`);
}
function assertValidDialogueContext(context) {
  const errors = validateDialogueContext(context);
  if (errors.length) throw new TypeError(`Contexto de diálogo inválido: ${errors.join(' · ')}`);
}

function trait(npc, key) { return pct(npc.traits[key]); }
function rel(npc, key) { return pct(npc.relationPlayer[key]); }
function ctx(context, key) { return pct(context[key]); }

function score(name, base, parts = [], available = true, reasonUnavailable = '') {
  if (!available) return { name, available: false, score: -Infinity, raw: -Infinity, contributions: [], reasonUnavailable };
  const contributions = parts.map(([label, value]) => ({ label, value }));
  const raw = base + contributions.reduce((sum, x) => sum + x.value, 0);
  return { name, available: true, raw, score: clamp(raw), contributions };
}

function inertiaBonus(npc, action) {
  const state = npc.behaviorState;
  if (state.lastAction !== action || state.consecutiveTurns < 1) return 0;
  return Math.max(0, 8 - state.consecutiveTurns * 2); // 6, 4, 2, 0...
}

function addInertia(npc, action, parts) {
  const bonus = inertiaBonus(npc, action);
  if (bonus > 0) parts.push(['inercia decreciente', bonus]);
  return parts;
}

function compareEvaluated(a, b) {
  if (a.available !== b.available) return a.available ? -1 : 1;
  if (!a.available && !b.available) return ACTION_ORDER.indexOf(a.name) - ACTION_ORDER.indexOf(b.name);
  if (b.score !== a.score) return b.score - a.score;
  if (b.raw !== a.raw) return b.raw - a.raw;
  return ACTION_ORDER.indexOf(a.name) - ACTION_ORDER.indexOf(b.name);
}

export function evaluateActions(npc, context) {
  assertValidNpc(npc);
  assertValidActionContext(context);

  const playerPresent = context.playerPresent;
  const playerRequestsHelp = context.playerRequestsHelp && playerPresent;
  const anomalyPresent = context.anomalyPresent;
  const awayFromPost = context.awayFromPost;
  const superiorReachable = context.superiorReachable;

  const discipline = trait(npc, 'disciplina');
  const sociability = trait(npc, 'sociabilidad');
  const curiosity = trait(npc, 'curiosidad');
  const prudence = trait(npc, 'prudencia');
  const institutional = trait(npc, 'lealtad_institucional');
  const empathy = trait(npc, 'empatia');

  const affinity = rel(npc, 'afinidad');
  const trust = rel(npc, 'confianza');
  const respect = rel(npc, 'respeto');
  const debt = rel(npc, 'deuda');
  const fear = rel(npc, 'temor');
  const rivalry = rel(npc, 'rivalidad');

  const duty = ctx(context, 'dutyImportance');
  const danger = ctx(context, 'danger');
  const urgency = ctx(context, 'missionUrgency');
  const playerRank = rankNorm(context.playerRank);
  const relevantKnowledge = knowledgeNorm(context.relevantKnowledge);

  const scores = [];
  scores.push(score('vigilar', 8, addInertia(npc, 'vigilar', [
    ['disciplina', discipline * 0.34], ['lealtad institucional', institutional * 0.24],
    ['importancia del puesto', duty * 0.30], ['prudencia', prudence * 0.10], ['urgencia externa', -urgency * 0.12],
  ]), context.dutyMode === 'vigilar', 'No tiene una guardia activa asignada.'));

  scores.push(score('trabajar', 7, addInertia(npc, 'trabajar', [
    ['disciplina', discipline * 0.27], ['lealtad institucional', institutional * 0.19],
    ['importancia de la tarea', duty * 0.27], ['urgencia externa', -urgency * 0.08],
  ]), context.dutyMode === 'trabajar', 'No tiene una tarea de trabajo activa asignada.'));

  scores.push(score('patrullar', 6, addInertia(npc, 'patrullar', [
    ['disciplina', discipline * 0.22], ['prudencia', prudence * 0.16], ['importancia del puesto', duty * 0.13],
    ['peligro', danger * 0.13], ['curiosidad', curiosity * 0.08],
  ]), context.dutyMode === 'patrullar', 'No tiene una patrulla activa asignada.'));

  scores.push(score('hablar_jugador', 5, addInertia(npc, 'hablar_jugador', [
    ['sociabilidad', sociability * 0.27], ['afinidad', affinity * 0.17], ['confianza', trust * 0.18],
    ['respeto', respect * 0.11], ['rango del jugador', playerRank * 0.08],
    ['conocimiento relevante', relevantKnowledge * 0.08], ['rivalidad', -rivalry * 0.10], ['temor', -fear * 0.05],
  ]), playerPresent, 'El jugador no está presente.'));

  scores.push(score('ayudar_jugador', 4, addInertia(npc, 'ayudar_jugador', [
    ['empatía', empathy * 0.29], ['afinidad', affinity * 0.22], ['confianza', trust * 0.24], ['deuda', debt * 0.20],
    ['respeto', respect * 0.10], ['rango del jugador', playerRank * 0.07], ['urgencia', urgency * 0.23],
    ['importancia del puesto', -duty * 0.25], ['prudencia ante peligro', -prudence * danger / 500], ['rivalidad', -rivalry * 0.12],
  ]), playerRequestsHelp, 'El jugador no está presente o no pidió ayuda.'));

  scores.push(score('investigar', 5, addInertia(npc, 'investigar', [
    ['curiosidad', curiosity * 0.48], ['audacia', (100 - prudence) * 0.19], ['urgencia', urgency * 0.13],
    ['peligro', danger * 0.08], ['deber institucional', institutional * 0.06],
  ]), anomalyPresent, 'No hay una anomalía que investigar.'));

  scores.push(score('informar_superior', 4, addInertia(npc, 'informar_superior', [
    ['prudencia', prudence * 0.24], ['disciplina', discipline * 0.20], ['lealtad institucional', institutional * 0.20],
    ['peligro', danger * 0.20], ['urgencia', urgency * 0.18],
  ]), superiorReachable && (anomalyPresent || danger >= 35 || urgency >= 50), 'No existe motivo suficiente o el superior no es alcanzable.'));

  scores.push(score('regresar_puesto', 10, addInertia(npc, 'regresar_puesto', [
    ['disciplina', discipline * 0.38], ['lealtad institucional', institutional * 0.24],
    ['importancia del puesto', duty * 0.25], ['prudencia', prudence * 0.08],
  ]), awayFromPost, 'El NPC ya está en su puesto/territorio de referencia.'));

  scores.push(score('esperar', 3, addInertia(npc, 'esperar', [
    ['prudencia', prudence * 0.18], ['baja curiosidad', (100 - curiosity) * 0.08],
    ['baja urgencia', (100 - urgency) * 0.06], ['bajo peligro', (100 - danger) * 0.04],
  ])));

  return scores;
}

export function chooseAction(npc, context) {
  const scores = evaluateActions(npc, context);
  const available = scores.filter(x => x.available).sort(compareEvaluated);
  if (!available.length) throw new Error('No hay acciones disponibles.');
  const selected = available[0];
  return {
    action: selected.name,
    score: selected.score,
    raw: selected.raw,
    ranking: scores.slice().sort(compareEvaluated),
    explanation: selected.contributions.slice().sort((a, b) => Math.abs(b.value) - Math.abs(a.value)),
    tieBreak: 'score > raw > ACTION_ORDER',
  };
}

export function evaluateDialogueTopic(npc, topicId, context) {
  assertValidNpc(npc);
  assertValidDialogueContext(context);
  if (!Object.hasOwn(npc.knowledge, topicId)) throw new RangeError(`Tema no definido para el laboratorio: ${topicId}`);

  const state = npc.knowledge[topicId];
  const level = KNOWLEDGE[state];
  const trust = rel(npc, 'confianza');
  const affinity = rel(npc, 'afinidad');
  const respect = rel(npc, 'respeto');
  const debt = rel(npc, 'deuda');
  const rivalry = rel(npc, 'rivalidad');
  const prudence = trait(npc, 'prudencia');
  const sociability = trait(npc, 'sociabilidad');
  const rank = rankNorm(context.playerRank);
  const sensitivity = pct(context.topicSensitivity);
  const formalRestriction = pct(context.formalRestriction);

  if (level === KNOWLEDGE.DESCONOCIDO) {
    return { topicId, state, mode: 'NO_SABE', disclosure: 0, explanation: ['El NPC no posee este conocimiento. Nunca puede revelarlo.'] };
  }

  const contributions = [
    ['confianza', trust * 0.30], ['afinidad', affinity * 0.14], ['respeto', respect * 0.13], ['deuda', debt * 0.16],
    ['rango del jugador', rank * 0.12], ['sociabilidad', sociability * 0.08], ['rivalidad', -rivalry * 0.17],
    ['prudencia', -prudence * 0.13], ['sensibilidad del tema', -sensitivity * 0.22],
    ['restricción institucional', -formalRestriction * 0.25], ['certeza propia', level * 8],
  ];
  const raw = 30 + contributions.reduce((sum, [, value]) => sum + value, 0);
  const disclosure = clamp(raw);

  let mode;
  if (state === 'SOSPECHA') mode = disclosure >= 42 ? 'INSINUA' : 'RESERVA';
  else if (disclosure >= 65) mode = 'COMPARTE';
  else if (disclosure >= 42) mode = 'INSINUA';
  else mode = 'RESERVA';

  return {
    topicId, state, mode, disclosure, raw,
    explanation: contributions.map(([label, value]) => ({ label, value })).sort((a, b) => Math.abs(b.value) - Math.abs(a.value)),
  };
}

export function simulateTurn(npc, context) {
  const decision = chooseAction(npc, context);
  const nextNpc = structuredClone(npc);
  const previous = nextNpc.behaviorState;
  if (previous.lastAction === decision.action) previous.consecutiveTurns += 1;
  else { previous.lastAction = decision.action; previous.consecutiveTurns = 1; }
  return {
    npcId: npc.id,
    action: decision.action,
    actionScore: decision.score,
    actionRaw: decision.raw,
    actionRanking: decision.ranking,
    actionExplanation: decision.explanation,
    nextNpc,
  };
}
