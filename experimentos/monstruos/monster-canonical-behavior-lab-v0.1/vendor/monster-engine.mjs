// Monster Combat AI v0.1 — Deterministic Decision Kernel
// "La IA decide. El motor resuelve." — este archivo SOLO decide.
//
// No modifica HP, estados, cooldowns, memoria, snapshot, catálogos ni el monstruo.
// No usa Math.random(). Toda aleatoriedad llega por `rng` inyectado.
//
// Ver README.md para el contrato completo (scoring, elegibilidad, tie-break,
// memoria por profundidad, contexto social, hardening).

export const STATUS = Object.freeze({
  INTENT_SELECTED: 'INTENT_SELECTED',
  NO_ELIGIBLE_INTENT: 'NO_ELIGIBLE_INTENT'
});

export const TIE_TOLERANCE = 1e-9;

export class ContractError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'ContractError';
    this.code = code || 'CONTRACT_ERROR';
  }
}

function fail(code, message) {
  throw new ContractError(message, code);
}

function isFiniteNumber(x) {
  return typeof x === 'number' && Number.isFinite(x);
}

function isPlainObject(x) {
  return x !== null && typeof x === 'object' && !Array.isArray(x);
}

function isNonEmptyString(x) {
  return typeof x === 'string' && x.length > 0;
}

function deepFreeze(value, seen = new WeakSet()) {
  if (value === null || typeof value !== 'object') return value;
  if (seen.has(value)) return value;
  seen.add(value);
  for (const key of Object.getOwnPropertyNames(value)) {
    deepFreeze(value[key], seen);
  }
  return Object.freeze(value);
}

// ---------------------------------------------------------------------------
// Validación de fronteras (hardening). Errores contractuales para input
// malformado; NO_ELIGIBLE_INTENT queda reservado para estado válido sin
// acciones disponibles (ver sección 15 del prompt).
// ---------------------------------------------------------------------------

function validateProfiles(profiles) {
  if (!isPlainObject(profiles)) fail('INVALID_PROFILES', 'profiles debe ser un objeto');
  for (const [key, p] of Object.entries(profiles)) {
    if (!isPlainObject(p)) fail('INVALID_PROFILE', `perfil ${key} inválido`);
    const { memoryDepth, repetitionPenalty, jitter, usesMemory, usesSocial } = p;
    if (!Number.isInteger(memoryDepth) || memoryDepth < 0) {
      fail('INVALID_PROFILE', `memoryDepth inválido en perfil ${key}`);
    }
    if (!isFiniteNumber(repetitionPenalty) || repetitionPenalty < 0) {
      fail('INVALID_PROFILE', `repetitionPenalty inválido en perfil ${key}`);
    }
    if (!isFiniteNumber(jitter) || jitter < 0) {
      fail('INVALID_PROFILE', `jitter inválido en perfil ${key}`);
    }
    if (typeof usesMemory !== 'boolean' || typeof usesSocial !== 'boolean') {
      fail('INVALID_PROFILE', `usesMemory/usesSocial inválidos en perfil ${key}`);
    }
  }
}

function validateWeightMap(map, label) {
  if (map === undefined) return;
  if (!isPlainObject(map)) fail('INVALID_ABILITY', `${label} debe ser un objeto`);
  for (const [k, v] of Object.entries(map)) {
    if (!isFiniteNumber(v)) fail('INVALID_ABILITY', `${label}.${k} no es finito`);
  }
}

function validateAbilities(abilities) {
  if (!isPlainObject(abilities)) fail('INVALID_ABILITIES', 'abilities debe ser un objeto {id: def}');
  for (const [key, def] of Object.entries(abilities)) {
    if (!isPlainObject(def)) fail('INVALID_ABILITY', `habilidad ${key} inválida`);
    if (def.id !== key) fail('INVALID_ABILITY', `habilidad ${key}: id no coincide con la clave del catálogo`);
    if (!isNonEmptyString(def.id)) fail('INVALID_ABILITY', `habilidad ${key}: id inválido`);
    if (!isNonEmptyString(def.intentCategory)) {
      fail('INVALID_ABILITY', `habilidad ${key}: intentCategory inválido`);
    }
    if (def.tags !== undefined && !Array.isArray(def.tags)) {
      fail('INVALID_ABILITY', `habilidad ${key}: tags debe ser array`);
    }
    if (!isNonEmptyString(def.telegraph)) {
      fail('INVALID_ABILITY', `habilidad ${key}: telegraph inválido`);
    }
    if (def.requirements !== undefined) {
      if (!isPlainObject(def.requirements)) fail('INVALID_ABILITY', `habilidad ${key}: requirements inválido`);
      if (def.requirements.signalsAll !== undefined && !Array.isArray(def.requirements.signalsAll)) {
        fail('INVALID_ABILITY', `habilidad ${key}: requirements.signalsAll debe ser array`);
      }
    }
    if (!isPlainObject(def.utility)) fail('INVALID_ABILITY', `habilidad ${key}: utility requerido`);
    if (!isFiniteNumber(def.utility.base)) fail('INVALID_ABILITY', `habilidad ${key}: utility.base no es finito`);
    validateWeightMap(def.utility.signalWeights, `habilidad ${key}: utility.signalWeights`);
    validateWeightMap(def.utility.memoryWeights, `habilidad ${key}: utility.memoryWeights`);
    validateWeightMap(def.utility.socialWeights, `habilidad ${key}: utility.socialWeights`);
  }
}

function validateMonster(monster, profiles) {
  if (!isPlainObject(monster)) fail('INVALID_MONSTER', 'monster debe ser un objeto');
  if (!isNonEmptyString(monster.id)) fail('INVALID_MONSTER', 'monster.id inválido');
  if (!isNonEmptyString(monster.profileId) || !profiles[monster.profileId]) {
    fail('UNKNOWN_PROFILE', `profileId desconocido: ${monster.profileId}`);
  }
  if (!Array.isArray(monster.effectiveKit)) fail('INVALID_MONSTER', 'monster.effectiveKit debe ser array');
  const seen = new Set();
  for (const id of monster.effectiveKit) {
    if (!isNonEmptyString(id)) fail('INVALID_MONSTER', 'effectiveKit contiene un id inválido');
    if (seen.has(id)) fail('DUPLICATE_KIT_ID', `id duplicado en effectiveKit: ${id}`);
    seen.add(id);
  }
  if (monster.preferences !== undefined) {
    if (!isPlainObject(monster.preferences)) fail('INVALID_MONSTER', 'monster.preferences debe ser un objeto');
    for (const [k, v] of Object.entries(monster.preferences)) {
      if (!isFiniteNumber(v)) fail('INVALID_MONSTER', `monster.preferences.${k} no es finito`);
    }
  }
  if (monster.recentAbilityIds !== undefined) {
    if (!Array.isArray(monster.recentAbilityIds)) fail('INVALID_MONSTER', 'monster.recentAbilityIds debe ser array');
    for (const id of monster.recentAbilityIds) {
      if (typeof id !== 'string') fail('INVALID_MONSTER', 'recentAbilityIds contiene un elemento no-string');
    }
  }
  if (monster.cooldowns !== undefined) {
    if (!isPlainObject(monster.cooldowns)) {
      fail('INVALID_MONSTER', 'monster.cooldowns debe ser un objeto {cooldownKey: boolean}');
    }
    // Contrato estricto: sólo se aceptan los booleanos true/false. Ningún
    // valor "truthy" alternativo (1, "false", [], {}, NaN, -1, ...) es
    // válido: aceptarlos silenciosamente ocultaría bugs de integración
    // futuros (REV2, corrección #2).
    for (const [cdKey, cdValue] of Object.entries(monster.cooldowns)) {
      if (cdValue !== true && cdValue !== false) {
        fail(
          'INVALID_COOLDOWN',
          `monster.cooldowns.${cdKey} debe ser estrictamente true o false (recibido: ${JSON.stringify(cdValue)})`
        );
      }
    }
  }
}

function validateCombat(combat) {
  if (!isPlainObject(combat)) fail('INVALID_COMBAT', 'combat debe ser un objeto');
  if (!Number.isInteger(combat.round) || combat.round < 0) {
    fail('INVALID_COMBAT', 'combat.round debe ser un entero >= 0');
  }
  if (!isPlainObject(combat.self)) fail('INVALID_COMBAT', 'combat.self requerido');
  if (!isPlainObject(combat.player)) fail('INVALID_COMBAT', 'combat.player requerido');
  for (const side of ['self', 'player']) {
    const hp = combat[side].hpRatio;
    if (!isFiniteNumber(hp) || hp < 0 || hp > 1) {
      fail('INVALID_COMBAT', `combat.${side}.hpRatio fuera de rango [0,1]`);
    }
  }
  if (combat.signals !== undefined) {
    if (!isPlainObject(combat.signals)) fail('INVALID_COMBAT', 'combat.signals debe ser un objeto');
    for (const [k, v] of Object.entries(combat.signals)) {
      if (v !== 0 && v !== 1 && v !== true && v !== false) {
        fail('INVALID_COMBAT', `combat.signals.${k} debe ser booleano o 0/1`);
      }
    }
  }
}

function validateMemory(memory) {
  if (memory === undefined) return;
  if (!Array.isArray(memory)) fail('INVALID_MEMORY', 'memory debe ser un array');
  for (const ev of memory) {
    if (!isPlainObject(ev)) fail('INVALID_MEMORY', 'evento de memoria inválido');
    if (!isNonEmptyString(ev.category)) fail('INVALID_MEMORY', 'evento de memoria sin category válida');
    if (ev.result !== undefined && typeof ev.result !== 'string') {
      fail('INVALID_MEMORY', 'evento de memoria: result debe ser string');
    }
    if (ev.round !== undefined && (!Number.isInteger(ev.round) || ev.round < 0)) {
      fail('INVALID_MEMORY', 'evento de memoria: round inválido');
    }
  }
}

function validateSocial(social) {
  if (social === undefined) return;
  if (!isPlainObject(social)) fail('INVALID_SOCIAL', 'social debe ser un objeto');
  if (social.alliesAlive !== undefined && (!Number.isInteger(social.alliesAlive) || social.alliesAlive < 0)) {
    fail('INVALID_SOCIAL', 'social.alliesAlive inválido');
  }
  if (social.sameSpeciesAllies !== undefined && (!Number.isInteger(social.sameSpeciesAllies) || social.sameSpeciesAllies < 0)) {
    fail('INVALID_SOCIAL', 'social.sameSpeciesAllies inválido');
  }
  if (social.outnumbersPlayer !== undefined && typeof social.outnumbersPlayer !== 'boolean') {
    fail('INVALID_SOCIAL', 'social.outnumbersPlayer inválido');
  }
}

function makeRngGate(rng) {
  if (!isPlainObject(rng) || typeof rng.random !== 'function') {
    fail('INVALID_RNG', 'rng.random debe ser una función');
  }
  return function next() {
    const v = rng.random();
    if (!isFiniteNumber(v) || v < 0 || v >= 1) {
      fail('INVALID_RNG', `rng.random() devolvió un valor fuera de [0,1): ${v}`);
    }
    return v;
  };
}

// ---------------------------------------------------------------------------
// Elegibilidad
// ---------------------------------------------------------------------------

function isOnCooldown(ability, monster) {
  if (!ability.cooldownKey) return false;
  const cooldowns = monster.cooldowns || {};
  // validateMonster ya garantizó que todo valor presente es estrictamente
  // true/false; una clave ausente equivale a "no está en cooldown".
  return cooldowns[ability.cooldownKey] === true;
}

function meetsRequirements(ability, signals) {
  const required = (ability.requirements && ability.requirements.signalsAll) || [];
  for (const signalName of required) {
    const v = signals[signalName];
    if (!(v === 1 || v === true)) return false;
  }
  return true;
}

// ---------------------------------------------------------------------------
// Contexto social: flags derivados y declarativos (ver README sección 10).
// ---------------------------------------------------------------------------

function computeSocialFlags(socialProfileId, social, signals) {
  const alliesAlive = social.alliesAlive || 0;
  const sameSpeciesAllies = social.sameSpeciesAllies || 0;
  const allyPresent = alliesAlive > 0 || signals.ALLY_PRESENT === 1 || signals.ALLY_PRESENT === true;
  const outnumber = social.outnumbersPlayer === true || signals.OUTNUMBER_PLAYER === 1 || signals.OUTNUMBER_PLAYER === true;
  const playerLowHp = signals.PLAYER_LOW_HP === 1 || signals.PLAYER_LOW_HP === true;
  const selfLowHp = signals.SELF_LOW_HP === 1 || signals.SELF_LOW_HP === true;

  return {
    MANADA_WITH_ALLY: socialProfileId === 'MANADA' && allyPresent,
    COLONIA_WITH_ALLY: socialProfileId === 'COLONIA' && (sameSpeciesAllies > 0 || allyPresent),
    OPORTUNISTA_LOW_HP: socialProfileId === 'OPORTUNISTA' && playerLowHp,
    REBAÑO_SELF_LOW_HP: socialProfileId === 'REBAÑO' && selfLowHp,
    TERRITORIAL_SOLO: socialProfileId === 'TERRITORIAL' && alliesAlive === 0,
    OUTNUMBER_PLAYER: outnumber
  };
}

// ---------------------------------------------------------------------------
// Memoria: sólo eventos dentro de la ventana permitida por el perfil.
// Se asume `memory` en orden cronológico ascendente (más reciente al final),
// tal como lo entrega el snapshot ya resuelto (ver sección 4.2 del prompt).
// ---------------------------------------------------------------------------

function windowedMemory(memory, memoryDepth, usesMemory) {
  if (!usesMemory || memoryDepth <= 0) return [];
  if (!memory || memory.length === 0) return [];
  return memory.slice(Math.max(0, memory.length - memoryDepth));
}

function memoryResultSign(result) {
  if (result === 'EFECTIVA') return 1;
  if (result === 'FALLIDA') return -1;
  return 0;
}

// ---------------------------------------------------------------------------
// Preferencias: modificador pequeño y acotado sobre intentCategory.
// ---------------------------------------------------------------------------

const PREFERENCE_SCALE = 20;
const PREFERENCE_DEFAULT = 1;
const PREFERENCE_MIN = 0;
const PREFERENCE_MAX = 2;

function preferenceModifier(preferences, ability) {
  const raw = preferences ? preferences[ability.intentCategory] : undefined;
  const clamped = isFiniteNumber(raw)
    ? Math.min(PREFERENCE_MAX, Math.max(PREFERENCE_MIN, raw))
    : PREFERENCE_DEFAULT;
  return (clamped - PREFERENCE_DEFAULT) * PREFERENCE_SCALE;
}

// ---------------------------------------------------------------------------
// Scoring: base + preferencias + señales + memoria + social - repetición + jitter
// ---------------------------------------------------------------------------

function scoreAbility({ ability, monster, profile, combat, memoryWindow, socialFlags, nextRandom }) {
  let score = ability.utility.base;
  const breakdown = { base: ability.utility.base };

  breakdown.preference = preferenceModifier(monster.preferences, ability);
  score += breakdown.preference;

  let signalContribution = 0;
  const signalWeights = ability.utility.signalWeights || {};
  const signals = combat.signals || {};
  for (const [signalName, weight] of Object.entries(signalWeights)) {
    const active = signals[signalName] === 1 || signals[signalName] === true;
    if (active) signalContribution += weight;
  }
  breakdown.signals = signalContribution;
  score += signalContribution;

  let memoryContribution = 0;
  const memoryWeights = ability.utility.memoryWeights || {};
  for (const ev of memoryWindow) {
    const w = memoryWeights[ev.category];
    if (w === undefined) continue;
    memoryContribution += w * memoryResultSign(ev.result);
  }
  breakdown.memory = memoryContribution;
  score += memoryContribution;

  let socialContribution = 0;
  const socialWeights = ability.utility.socialWeights || {};
  for (const [flagName, active] of Object.entries(socialFlags)) {
    if (!active) continue;
    const w = socialWeights[flagName];
    if (w === undefined) continue;
    socialContribution += w;
  }
  breakdown.social = socialContribution;
  score += socialContribution;

  const occurrences = monster.recentAbilityIds
    ? monster.recentAbilityIds.filter((id) => id === ability.id).length
    : 0;
  const repetitionPenalty = occurrences * profile.repetitionPenalty;
  breakdown.repetitionPenalty = -repetitionPenalty;
  score -= repetitionPenalty;

  let jitter = 0;
  if (profile.jitter > 0) {
    jitter = (nextRandom() * 2 - 1) * profile.jitter;
  }
  breakdown.jitter = jitter;
  score += jitter;

  if (!isFiniteNumber(score)) {
    fail('NON_FINITE_SCORE', `score no finito para habilidad ${ability.id}`);
  }

  return { score, breakdown };
}

// ---------------------------------------------------------------------------
// API pública
// ---------------------------------------------------------------------------

export function chooseMonsterIntent(input) {
  if (!isPlainObject(input)) fail('INVALID_INPUT', 'input debe ser un objeto');
  const { monster, profiles, abilities, combat, memory, social, rng } = input;

  validateProfiles(profiles);
  validateAbilities(abilities);
  validateMonster(monster, profiles);
  validateCombat(combat);
  validateMemory(memory);
  validateSocial(social);
  const nextRandom = makeRngGate(rng);

  const profile = profiles[monster.profileId];
  const socialProfileId = monster.socialProfileId;
  const socialCtx = social || { alliesAlive: 0, sameSpeciesAllies: 0, outnumbersPlayer: false };
  const signals = combat.signals || {};

  const memoryWindow = windowedMemory(memory, profile.memoryDepth, profile.usesMemory);
  const socialFlags = profile.usesSocial
    ? computeSocialFlags(socialProfileId, socialCtx, signals)
    : {};

  // -------------------------------------------------------------------------
  // Fase 1 — Elegibilidad. Recorre effectiveKit en el orden que llegó (no
  // consume RNG: la elegibilidad es puramente determinista a partir de
  // catálogo/cooldowns/requirements, así que este orden es inofensivo).
  // -------------------------------------------------------------------------
  const entriesByAbilityId = new Map();
  const eligibleAbilities = [];

  for (const abilityId of monster.effectiveKit) {
    const ability = abilities[abilityId];
    const entry = { abilityId, eligible: false, reason: null, score: null };

    if (!ability) {
      entry.reason = 'UNKNOWN_ABILITY_IN_KIT';
    } else if (ability.disabled === true) {
      entry.reason = 'DISABLED';
    } else if (isOnCooldown(ability, monster)) {
      entry.reason = 'COOLDOWN';
    } else if (!meetsRequirements(ability, signals)) {
      entry.reason = 'REQUIREMENTS_NOT_MET';
    } else {
      entry.eligible = true;
      eligibleAbilities.push(ability);
    }

    entriesByAbilityId.set(abilityId, entry);
  }

  // -------------------------------------------------------------------------
  // Fase 2 — Scoring. REV2 (corrección #1): el consumo de RNG (jitter) debe
  // depender exclusivamente del CONJUNTO de habilidades elegibles, nunca del
  // orden en que effectiveKit o el catálogo `abilities` las enumeran. Por
  // eso se puntúa en un orden canónico (id ascendente) en vez del orden de
  // iteración de effectiveKit: así, reordenar effectiveKit o abilities no
  // cambia qué valor de rng.random() recibe cada habilidad.
  // -------------------------------------------------------------------------
  const canonicalOrder = [...eligibleAbilities].sort(
    (a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0)
  );

  const eligibleScored = [];
  for (const ability of canonicalOrder) {
    const { score, breakdown } = scoreAbility({
      ability, monster, profile, combat, memoryWindow, socialFlags, nextRandom
    });
    const entry = entriesByAbilityId.get(ability.id);
    entry.score = score;
    entry.breakdown = breakdown;
    eligibleScored.push({ ability, score });
  }

  // `considered` se expone en el orden original de effectiveKit (es
  // información de diagnóstico; no participa del cálculo).
  const considered = monster.effectiveKit.map((id) => entriesByAbilityId.get(id));

  const scoreByAbility = {};
  for (const c of considered) scoreByAbility[c.abilityId] = c.score;

  const debugBase = {
    considered,
    scoreByAbility,
    activeMemory: memoryWindow.map((ev) => ({ category: ev.category, result: ev.result, round: ev.round })),
    tieBrokenByRng: false
  };

  if (eligibleScored.length === 0) {
    return deepFreeze({
      status: STATUS.NO_ELIGIBLE_INTENT,
      monsterId: monster.id,
      reason: 'NO_ELIGIBLE_ABILITY',
      debug: debugBase
    });
  }

  const maxScore = Math.max(...eligibleScored.map((e) => e.score));
  const candidates = eligibleScored
    .filter((e) => Math.abs(e.score - maxScore) <= TIE_TOLERANCE)
    .sort((a, b) => (a.ability.id < b.ability.id ? -1 : a.ability.id > b.ability.id ? 1 : 0));

  let chosen;
  let tieBrokenByRng = false;
  if (candidates.length === 1) {
    chosen = candidates[0];
  } else {
    tieBrokenByRng = true;
    const idx = Math.floor(nextRandom() * candidates.length);
    chosen = candidates[Math.min(idx, candidates.length - 1)];
  }

  debugBase.tieBrokenByRng = tieBrokenByRng;

  return deepFreeze({
    status: STATUS.INTENT_SELECTED,
    monsterId: monster.id,
    abilityId: chosen.ability.id,
    intent: {
      id: chosen.ability.id,
      telegraph: chosen.ability.telegraph
    },
    debug: debugBase
  });
}
