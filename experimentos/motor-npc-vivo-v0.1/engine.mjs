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

const clamp = (n, min = 0, max = 100) => Math.max(min, Math.min(max, n));
const pct = n => clamp(Number(n) || 0);
const rankNorm = rank => clamp((Number(rank) || 0) / 6 * 100);
const knowledgeNorm = state => clamp((KNOWLEDGE[state] ?? 0) / 3 * 100);

function trait(npc, key) { return pct(npc?.traits?.[key]); }
function rel(npc, key) { return pct(npc?.relationPlayer?.[key]); }
function ctx(context, key) { return pct(context?.[key]); }

function score(name, base, parts = [], available = true, reasonUnavailable = '') {
  if (!available) {
    return { name, available: false, score: -Infinity, raw: -Infinity, contributions: [], reasonUnavailable };
  }
  const contributions = parts.map(([label, value]) => ({ label, value: Number(value) || 0 }));
  const raw = base + contributions.reduce((s, x) => s + x.value, 0);
  return { name, available: true, raw, score: clamp(raw), contributions };
}

export function evaluateActions(npc, context = {}) {
  const playerPresent = !!context.playerPresent;
  const playerRequestsHelp = !!context.playerRequestsHelp && playerPresent;
  const anomalyPresent = !!context.anomalyPresent;
  const awayFromPost = !!context.awayFromPost;
  const superiorReachable = context.superiorReachable !== false;

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
  const relevantKnowledge = knowledgeNorm(context.relevantKnowledge || 'DESCONOCIDO');
  const inertia = npc?.lastAction;

  const scores = [];
  const addInertia = (action, parts) => {
    if (inertia === action) parts.push(['inercia de conducta', 6]);
    return parts;
  };

  scores.push(score('vigilar', 8, addInertia('vigilar', [
    ['disciplina', discipline * 0.34],
    ['lealtad institucional', institutional * 0.24],
    ['importancia del puesto', duty * 0.30],
    ['prudencia', prudence * 0.10],
    ['urgencia externa', -urgency * 0.12],
  ])));

  scores.push(score('trabajar', 7, addInertia('trabajar', [
    ['disciplina', discipline * 0.27],
    ['lealtad institucional', institutional * 0.19],
    ['importancia de la tarea', duty * 0.27],
    ['urgencia externa', -urgency * 0.08],
  ])));

  scores.push(score('patrullar', 6, addInertia('patrullar', [
    ['disciplina', discipline * 0.22],
    ['prudencia', prudence * 0.16],
    ['importancia del puesto', duty * 0.13],
    ['peligro', danger * 0.13],
    ['curiosidad', curiosity * 0.08],
  ])));

  scores.push(score('hablar_jugador', 5, addInertia('hablar_jugador', [
    ['sociabilidad', sociability * 0.27],
    ['afinidad', affinity * 0.17],
    ['confianza', trust * 0.18],
    ['respeto', respect * 0.11],
    ['rango del jugador', playerRank * 0.08],
    ['conocimiento relevante', relevantKnowledge * 0.08],
    ['rivalidad', -rivalry * 0.10],
    ['temor', -fear * 0.05],
  ]), playerPresent, 'El jugador no está presente.'));

  scores.push(score('ayudar_jugador', 4, addInertia('ayudar_jugador', [
    ['empatía', empathy * 0.29],
    ['afinidad', affinity * 0.22],
    ['confianza', trust * 0.24],
    ['deuda', debt * 0.20],
    ['respeto', respect * 0.10],
    ['rango del jugador', playerRank * 0.07],
    ['urgencia', urgency * 0.23],
    ['importancia del puesto', -duty * 0.25],
    ['prudencia ante peligro', -prudence * danger / 500],
    ['rivalidad', -rivalry * 0.12],
  ]), playerRequestsHelp, 'El jugador no está presente o no pidió ayuda.'));

  scores.push(score('investigar', 5, addInertia('investigar', [
    ['curiosidad', curiosity * 0.48],
    ['audacia', (100 - prudence) * 0.19],
    ['urgencia', urgency * 0.13],
    ['peligro', danger * 0.08],
    ['deber institucional', institutional * 0.06],
  ]), anomalyPresent, 'No hay una anomalía que investigar.'));

  scores.push(score('informar_superior', 4, addInertia('informar_superior', [
    ['prudencia', prudence * 0.24],
    ['disciplina', discipline * 0.20],
    ['lealtad institucional', institutional * 0.20],
    ['peligro', danger * 0.20],
    ['urgencia', urgency * 0.18],
  ]), superiorReachable && (anomalyPresent || danger >= 35 || urgency >= 50), 'No existe motivo suficiente o el superior no es alcanzable.'));

  scores.push(score('regresar_puesto', 10, addInertia('regresar_puesto', [
    ['disciplina', discipline * 0.38],
    ['lealtad institucional', institutional * 0.24],
    ['importancia del puesto', duty * 0.25],
    ['prudencia', prudence * 0.08],
  ]), awayFromPost, 'El NPC ya está en su puesto/territorio de referencia.'));

  scores.push(score('esperar', 3, addInertia('esperar', [
    ['prudencia', prudence * 0.18],
    ['baja curiosidad', (100 - curiosity) * 0.08],
    ['baja urgencia', (100 - urgency) * 0.06],
    ['bajo peligro', (100 - danger) * 0.04],
  ])));

  return scores;
}

export function chooseAction(npc, context = {}) {
  const scores = evaluateActions(npc, context);
  const available = scores.filter(x => x.available);
  if (!available.length) throw new Error('No hay acciones disponibles.');
  available.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return ACTION_ORDER.indexOf(a.name) - ACTION_ORDER.indexOf(b.name);
  });
  const selected = available[0];
  return {
    action: selected.name,
    score: selected.score,
    ranking: scores.slice().sort((a, b) => (b.available - a.available) || (b.score - a.score)),
    explanation: selected.contributions
      .slice()
      .sort((a, b) => Math.abs(b.value) - Math.abs(a.value)),
  };
}

export function evaluateDialogueTopic(npc, topicId, context = {}) {
  const state = npc?.knowledge?.[topicId] || 'DESCONOCIDO';
  const level = KNOWLEDGE[state] ?? 0;
  const trust = rel(npc, 'confianza');
  const affinity = rel(npc, 'afinidad');
  const respect = rel(npc, 'respeto');
  const debt = rel(npc, 'deuda');
  const rivalry = rel(npc, 'rivalidad');
  const prudence = trait(npc, 'prudencia');
  const sociability = trait(npc, 'sociabilidad');
  const rank = rankNorm(context.playerRank);
  const sensitivity = pct(context.topicSensitivity ?? 50);
  const formalRestriction = pct(context.formalRestriction ?? 0);

  if (level === KNOWLEDGE.DESCONOCIDO) {
    return {
      topicId, state, mode: 'NO_SABE', disclosure: 0,
      explanation: ['El NPC no posee este conocimiento. Nunca puede revelarlo.'],
    };
  }

  const contributions = [
    ['confianza', trust * 0.30],
    ['afinidad', affinity * 0.14],
    ['respeto', respect * 0.13],
    ['deuda', debt * 0.16],
    ['rango del jugador', rank * 0.12],
    ['sociabilidad', sociability * 0.08],
    ['rivalidad', -rivalry * 0.17],
    ['prudencia', -prudence * 0.13],
    ['sensibilidad del tema', -sensitivity * 0.22],
    ['restricción institucional', -formalRestriction * 0.25],
    ['certeza propia', level * 8],
  ];
  const raw = 30 + contributions.reduce((s, [, v]) => s + v, 0);
  const disclosure = clamp(raw);

  let mode;
  if (state === 'SOSPECHA') mode = disclosure >= 42 ? 'INSINUA' : 'RESERVA';
  else if (disclosure >= 65) mode = 'COMPARTE';
  else if (disclosure >= 42) mode = 'INSINUA';
  else mode = 'RESERVA';

  return {
    topicId,
    state,
    mode,
    disclosure,
    explanation: contributions
      .map(([label, value]) => ({ label, value }))
      .sort((a, b) => Math.abs(b.value) - Math.abs(a.value)),
  };
}

export function simulateTurn(npc, context = {}) {
  const decision = chooseAction(npc, context);
  return {
    npcId: npc.id,
    action: decision.action,
    actionScore: decision.score,
    actionRanking: decision.ranking,
    actionExplanation: decision.explanation,
    nextNpc: { ...npc, lastAction: decision.action },
  };
}

export function validateNpc(npc) {
  const errors = [];
  if (!npc || typeof npc !== 'object') return ['NPC inválido'];
  if (!npc.id) errors.push('Falta id');
  for (const group of ['traits', 'relationPlayer']) {
    if (!npc[group] || typeof npc[group] !== 'object') errors.push(`Falta ${group}`);
    else for (const [k, v] of Object.entries(npc[group])) {
      if (!Number.isFinite(v) || v < 0 || v > 100) errors.push(`${group}.${k} fuera de 0..100`);
    }
  }
  if (!npc.knowledge || typeof npc.knowledge !== 'object') errors.push('Falta knowledge');
  else for (const [k, v] of Object.entries(npc.knowledge)) {
    if (!(v in KNOWLEDGE)) errors.push(`knowledge.${k} inválido: ${v}`);
  }
  return errors;
}
