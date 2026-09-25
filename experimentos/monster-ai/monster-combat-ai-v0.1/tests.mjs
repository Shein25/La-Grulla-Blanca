import assert from 'node:assert/strict';
import { chooseMonsterIntent, ContractError, STATUS } from './engine.mjs';
import { PROFILES, SOCIAL_PROFILES } from './profiles.mjs';
import {
  ABILITIES, MONSTERS, baseCombat, baseSocial, SAMPLE_MEMORY,
  createSeededRng, ZERO_RNG
} from './fixtures.mjs';

let passCount = 0;
let failCount = 0;
const failures = [];

function test(name, fn) {
  try {
    fn();
    passCount += 1;
    console.log(`PASS  ${name}`);
  } catch (err) {
    failCount += 1;
    failures.push({ name, err });
    console.log(`FAIL  ${name}`);
    console.log(`      ${err.message}`);
  }
}

function deepFreezeClone(value) {
  // Deep-freeze a structured clone so fixtures stay reusable across tests.
  const clone = structuredClone(value);
  const stack = [clone];
  const seen = new WeakSet();
  while (stack.length) {
    const cur = stack.pop();
    if (cur === null || typeof cur !== 'object' || seen.has(cur)) continue;
    seen.add(cur);
    Object.freeze(cur);
    for (const k of Object.getOwnPropertyNames(cur)) stack.push(cur[k]);
  }
  return clone;
}

function run(overrides = {}) {
  const input = {
    monster: overrides.monster || MONSTERS.wolf_fixture,
    profiles: overrides.profiles || PROFILES,
    abilities: overrides.abilities || ABILITIES,
    combat: overrides.combat || baseCombat(),
    memory: 'memory' in overrides ? overrides.memory : SAMPLE_MEMORY,
    social: 'social' in overrides ? overrides.social : baseSocial(),
    rng: overrides.rng || createSeededRng(overrides.seed ?? 1337)
  };
  return chooseMonsterIntent(input);
}

// ---------------------------------------------------------------------------
// GOLDEN A — INSTINTIVO ignora memoria
// ---------------------------------------------------------------------------
test('GOLDEN A — INSTINTIVO ignora memoria', () => {
  const r1 = run({ monster: MONSTERS.rata_fixture, memory: [], seed: 7 });
  const r2 = run({ monster: MONSTERS.rata_fixture, memory: SAMPLE_MEMORY, seed: 7 });
  assert.deepEqual(r1, r2, 'la decisión no debe cambiar al variar memory bajo INSTINTIVO');
  assert.equal(r1.debug.activeMemory.length, 0);
});

// ---------------------------------------------------------------------------
// GOLDEN B — REACTIVO usa sólo el último evento
// ---------------------------------------------------------------------------
test('GOLDEN B — REACTIVO usa sólo último evento', () => {
  const memBase = [
    { category: 'DEFENSA_ABSORCION', result: 'EFECTIVA', round: 1 },
    { category: 'DEFENSA_ABSORCION', result: 'EFECTIVA', round: 2 }
  ];
  const memChangedOld = [
    { category: 'RECUPERACION', result: 'EFECTIVA', round: 1 }, // evento viejo (A) cambiado
    { category: 'DEFENSA_ABSORCION', result: 'EFECTIVA', round: 2 }
  ];
  const memChangedRecent = [
    { category: 'DEFENSA_ABSORCION', result: 'EFECTIVA', round: 1 },
    { category: 'RECUPERACION', result: 'EFECTIVA', round: 2 } // evento reciente (B) cambiado
  ];

  const rBase = run({ monster: MONSTERS.serpiente_fixture, memory: memBase, seed: 3 });
  const rOld = run({ monster: MONSTERS.serpiente_fixture, memory: memChangedOld, seed: 3 });
  const rRecent = run({ monster: MONSTERS.serpiente_fixture, memory: memChangedRecent, seed: 3 });

  assert.equal(rBase.debug.scoreByAbility.veneno_lento, rOld.debug.scoreByAbility.veneno_lento,
    'cambiar el evento viejo (fuera de memoryDepth=1) no debe alterar el score');
  assert.notEqual(rBase.debug.scoreByAbility.veneno_lento, rRecent.debug.scoreByAbility.veneno_lento,
    'cambiar el evento reciente (dentro de memoryDepth=1) sí debe alterar el score');
});

// ---------------------------------------------------------------------------
// GOLDEN C — CAZADOR usa máximo 2 eventos
// ---------------------------------------------------------------------------
test('GOLDEN C — CAZADOR usa máximo 2', () => {
  const tenEvents = [];
  for (let i = 0; i < 10; i += 1) {
    tenEvents.push({ category: 'RECUPERACION', result: i < 8 ? 'FALLIDA' : 'EFECTIVA', round: i });
  }
  const r = run({ monster: MONSTERS.wolf_fixture, memory: tenEvents, seed: 11 });
  assert.equal(r.debug.activeMemory.length, 2, 'CAZADOR_2 debe usar exactamente 2 eventos como máximo');
  assert.deepEqual(r.debug.activeMemory.map((e) => e.round), [8, 9]);

  const alteredOld = tenEvents.map((e, i) => (i < 8 ? { ...e, result: 'EFECTIVA' } : e));
  const rAltered = run({ monster: MONSTERS.wolf_fixture, memory: alteredOld, seed: 11 });
  assert.equal(r.debug.scoreByAbility.acechar, rAltered.debug.scoreByAbility.acechar,
    'alterar eventos fuera de la ventana de profundidad no debe cambiar el score');
});

// ---------------------------------------------------------------------------
// GOLDEN D — TACTICO usa máximo 3
// ---------------------------------------------------------------------------
test('GOLDEN D — TACTICO usa máximo 3', () => {
  const events = [];
  for (let i = 0; i < 6; i += 1) {
    events.push({ category: 'DEFENSA_ABSORCION', result: 'EFECTIVA', round: i });
  }
  const r = run({ monster: MONSTERS.devorador_fixture, memory: events, seed: 5 });
  assert.equal(r.debug.activeMemory.length, 3);
  const alteredCutoff = events.map((e, i) => (i < 3 ? { ...e, result: 'FALLIDA' } : e));
  const rAltered = run({ monster: MONSTERS.devorador_fixture, memory: alteredCutoff, seed: 5 });
  assert.equal(r.debug.scoreByAbility.estudio_tactico, rAltered.debug.scoreByAbility.estudio_tactico);
});

// ---------------------------------------------------------------------------
// GOLDEN E — MASTER usa máximo 4
// ---------------------------------------------------------------------------
test('GOLDEN E — MASTER usa máximo 4', () => {
  const events = [];
  for (let i = 0; i < 7; i += 1) {
    events.push({ category: 'RECUPERACION', result: 'EFECTIVA', round: i });
  }
  const r = run({ monster: MONSTERS.mantis_fixture, memory: events, seed: 9 });
  assert.equal(r.debug.activeMemory.length, 4);
});

// ---------------------------------------------------------------------------
// GOLDEN F — cooldown bloquea incluso a la de mayor score
// ---------------------------------------------------------------------------
test('GOLDEN F — cooldown', () => {
  const monster = { ...MONSTERS.mantis_fixture, cooldowns: { ataque_devastador_cd: true } };
  const r = run({ monster, seed: 2 });
  assert.notEqual(r.abilityId, 'ataque_devastador');
});

// ---------------------------------------------------------------------------
// GOLDEN G — requisito no cumplido
// ---------------------------------------------------------------------------
test('GOLDEN G — requisito', () => {
  const combat = baseCombat({ signals: { ALLY_PRESENT: 0 } });
  const r = run({ monster: MONSTERS.wolf_fixture, combat, seed: 4 });
  assert.notEqual(r.abilityId, 'tres_flancos');
  const considered = r.debug.considered.find((c) => c.abilityId === 'tres_flancos');
  assert.equal(considered.reason, 'REQUIREMENTS_NOT_MET');
});

// ---------------------------------------------------------------------------
// GOLDEN H — no future-read
// ---------------------------------------------------------------------------
test('GOLDEN H — no future-read', () => {
  const combatClean = baseCombat();
  const combatWithFuture = { ...baseCombat(), futurePlayerAction: 'DEFENDER' };
  const r1 = run({ combat: combatClean, seed: 6 });
  const r2 = run({ combat: combatWithFuture, seed: 6 });
  assert.equal(r1.abilityId, r2.abilityId, 'un campo ajeno no permitido no debe influir en la decisión');
});

// ---------------------------------------------------------------------------
// GOLDEN I — preferencias distintas -> decisiones distintas
// ---------------------------------------------------------------------------
test('GOLDEN I — preferencias', () => {
  const combat = baseCombat({ signals: { ALLY_PRESENT: 1, OUTNUMBER_PLAYER: 1, PLAYER_LOW_HP: 0 } });
  const monsterA = { ...MONSTERS.wolf_fixture, preferences: { CONTROL: 2.0, PREPARACION: 0.2, OFENSIVA: 0.2 } };
  const monsterB = { ...MONSTERS.wolf_fixture, preferences: { CONTROL: 0.2, PREPARACION: 2.0, OFENSIVA: 0.2 } };
  const rA = run({ monster: monsterA, combat, seed: 8 });
  const rB = run({ monster: monsterB, combat, seed: 8 });
  assert.notEqual(rA.abilityId, rB.abilityId, 'preferencias distintas deben poder cambiar la selección');
});

// ---------------------------------------------------------------------------
// GOLDEN J — social != cognición
// ---------------------------------------------------------------------------
test('GOLDEN J — social != cognición', () => {
  const monsterManada = MONSTERS.wolf_fixture;
  const monsterSolitario = { ...MONSTERS.wolf_fixture, socialProfileId: 'SOLITARIO' };
  const rManada = run({ monster: monsterManada, seed: 1 });
  const rSolitario = run({ monster: monsterSolitario, seed: 1 });
  assert.notEqual(
    rManada.debug.scoreByAbility.tres_flancos,
    rSolitario.debug.scoreByAbility.tres_flancos,
    'cambiar el perfil social debe afectar el score social'
  );
  assert.equal(rManada.debug.activeMemory.length, rSolitario.debug.activeMemory.length,
    'cambiar el perfil social no debe afectar memoryDepth (memoria proviene del perfil cognitivo)');
});

// ---------------------------------------------------------------------------
// GOLDEN K — anti-repetición más fuerte en perfiles avanzados
// ---------------------------------------------------------------------------
test('GOLDEN K — anti-repetición', () => {
  assert.ok(PROFILES.TACTICO_3.repetitionPenalty > PROFILES.INSTINTIVO.repetitionPenalty);
  assert.ok(PROFILES.MASTER_4.repetitionPenalty > PROFILES.INSTINTIVO.repetitionPenalty);
});

// ---------------------------------------------------------------------------
// GOLDEN L — determinismo
// ---------------------------------------------------------------------------
test('GOLDEN L — determinismo', () => {
  const r1 = run({ seed: 20260924 });
  const r2 = run({ seed: 20260924 });
  assert.deepEqual(r1, r2);
});

// ---------------------------------------------------------------------------
// GOLDEN M — reorder invariance
// ---------------------------------------------------------------------------
test('GOLDEN M — reorder invariance', () => {
  const monster1 = { ...MONSTERS.wolf_fixture, effectiveKit: ['mordida', 'acechar', 'tres_flancos'] };
  const monster2 = { ...MONSTERS.wolf_fixture, effectiveKit: ['tres_flancos', 'mordida', 'acechar'] };
  const reorderedAbilities = {
    tres_flancos: ABILITIES.tres_flancos,
    acechar: ABILITIES.acechar,
    mordida: ABILITIES.mordida
  };
  const r1 = run({ monster: monster1, abilities: ABILITIES, seed: 42 });
  const r2 = run({ monster: monster2, abilities: reorderedAbilities, seed: 42 });
  assert.equal(r1.abilityId, r2.abilityId);
});

// ---------------------------------------------------------------------------
// GOLDEN N — no mutation (deep-freeze)
// ---------------------------------------------------------------------------
test('GOLDEN N — no mutation', () => {
  const monster = deepFreezeClone(MONSTERS.wolf_fixture);
  const combat = deepFreezeClone(baseCombat());
  const memory = deepFreezeClone(SAMPLE_MEMORY);
  const social = deepFreezeClone(baseSocial());
  const abilities = deepFreezeClone(ABILITIES);
  const profiles = deepFreezeClone(PROFILES);
  const result = chooseMonsterIntent({
    monster, profiles, abilities, combat, memory, social, rng: createSeededRng(1)
  });
  assert.equal(result.status, STATUS.INTENT_SELECTED);
  assert.throws(() => { result.debug.tieBrokenByRng = true; }, TypeError);
});

// ---------------------------------------------------------------------------
// GOLDEN O / Q — no execution / no hidden stat adaptation
// ---------------------------------------------------------------------------
test('GOLDEN O and Q — no execution / no hidden stat adaptation', () => {
  const monster = MONSTERS.wolf_fixture;
  const combat = baseCombat();
  const before = JSON.stringify({ monster, combat, memory: SAMPLE_MEMORY });
  chooseMonsterIntent({
    monster, profiles: PROFILES, abilities: ABILITIES, combat,
    memory: SAMPLE_MEMORY, social: baseSocial(), rng: createSeededRng(1)
  });
  const after = JSON.stringify({ monster, combat, memory: SAMPLE_MEMORY });
  assert.equal(before, after, 'ni HP, ni statuses, ni memoria deben cambiar tras decidir');
});

// ---------------------------------------------------------------------------
// GOLDEN P — instance isolation
// ---------------------------------------------------------------------------
test('GOLDEN P — instance isolation', () => {
  const wolfA = { ...MONSTERS.wolf_fixture, id: 'wolf_A', recentAbilityIds: ['acechar', 'acechar'] };
  const wolfB = { ...MONSTERS.wolf_fixture, id: 'wolf_B', recentAbilityIds: [] };
  const rA1 = run({ monster: wolfA, seed: 1 });
  const rB1 = run({ monster: wolfB, seed: 1 });
  const rA2 = run({ monster: wolfA, seed: 1 });
  assert.deepEqual(rA1, rA2, 'llamar dos veces con el mismo input no debe acumular estado');
  assert.notEqual(rA1.debug.scoreByAbility.acechar, rB1.debug.scoreByAbility.acechar,
    'instancias con distinto recentAbilityIds deben decidir de forma independiente');
});

// ---------------------------------------------------------------------------
// GOLDEN R — no eligible
// ---------------------------------------------------------------------------
test('GOLDEN R — no eligible', () => {
  const monster = { ...MONSTERS.wolf_fixture, effectiveKit: [] };
  const r = run({ monster, seed: 1 });
  assert.equal(r.status, STATUS.NO_ELIGIBLE_INTENT);
  assert.equal(r.reason, 'NO_ELIGIBLE_ABILITY');
});

// ---------------------------------------------------------------------------
// Tie-break determinista (sección 14 del prompt)
// ---------------------------------------------------------------------------
test('tie-break — empate exacto se resuelve por RNG de forma determinista y sin depender del orden', () => {
  const tiedAbilities = {
    ability_a: {
      id: 'ability_a', intentCategory: 'OFENSIVA', tags: [], telegraph: 'A',
      requirements: { signalsAll: [] },
      utility: { base: 10, signalWeights: {}, memoryWeights: {}, socialWeights: {} }
    },
    ability_b: {
      id: 'ability_b', intentCategory: 'OFENSIVA', tags: [], telegraph: 'B',
      requirements: { signalsAll: [] },
      utility: { base: 10, signalWeights: {}, memoryWeights: {}, socialWeights: {} }
    }
  };
  const monster = {
    id: 'tie_fixture', profileId: 'INSTINTIVO', socialProfileId: 'SOLITARIO',
    effectiveKit: ['ability_a', 'ability_b'], preferences: {}, recentAbilityIds: []
  };
  const monsterReordered = { ...monster, effectiveKit: ['ability_b', 'ability_a'] };
  const combat = baseCombat({ signals: {} });

  const r1 = chooseMonsterIntent({
    monster, profiles: PROFILES, abilities: tiedAbilities, combat,
    memory: [], social: baseSocial(), rng: { random: () => 0 }
  });
  const r2 = chooseMonsterIntent({
    monster: monsterReordered, profiles: PROFILES, abilities: tiedAbilities, combat,
    memory: [], social: baseSocial(), rng: { random: () => 0 }
  });

  assert.ok(r1.debug.tieBrokenByRng, 'un empate exacto debe marcarse como resuelto por RNG');
  assert.equal(r1.abilityId, r2.abilityId, 'el tie-break no debe depender del orden de effectiveKit');
});

// ---------------------------------------------------------------------------
// REV2 — Regresión #1: reorder invariance con jitter activo
//
// Esta es la regresión que exige la corrección: dos habilidades con score
// determinista IDÉNTICO (mismo base, sin señales/memoria/social) bajo un
// perfil con jitter > 0. Antes de la corrección, el jitter se asignaba
// habilidad por habilidad en el orden de iteración de `effectiveKit`, así
// que reordenar el kit reordenaba qué valor de rng.random() recibía cada
// habilidad y podía cambiar la ganadora. La corrección puntúa en un orden
// canónico (por ability.id) independiente del orden de entrada.
//
// Esta prueba FALLA contra la implementación previa a REV2 (verificado
// manualmente revirtiendo la Fase 2 de chooseMonsterIntent al recorrido
// directo de effectiveKit) y PASA contra la implementación corregida.
// ---------------------------------------------------------------------------
test('REV2 REGRESIÓN #1 — reorder invariance con jitter activo (INSTINTIVO)', () => {
  const jitterAbilities = {
    candidate_x: {
      id: 'candidate_x', intentCategory: 'NEUTRA', tags: [], telegraph: 'X',
      requirements: { signalsAll: [] },
      utility: { base: 10, signalWeights: {}, memoryWeights: {}, socialWeights: {} }
    },
    candidate_y: {
      id: 'candidate_y', intentCategory: 'NEUTRA', tags: [], telegraph: 'Y',
      requirements: { signalsAll: [] },
      utility: { base: 10, signalWeights: {}, memoryWeights: {}, socialWeights: {} }
    }
  };
  const combat = baseCombat({ signals: {} });
  const cleanCombat = { ...combat, signals: {} };

  const monsterOrderXY = {
    id: 'jitter_fixture', profileId: 'INSTINTIVO', socialProfileId: 'SOLITARIO',
    effectiveKit: ['candidate_x', 'candidate_y'], preferences: {}, recentAbilityIds: []
  };
  const monsterOrderYX = { ...monsterOrderXY, effectiveKit: ['candidate_y', 'candidate_x'] };
  const abilitiesOrderYX = { candidate_y: jitterAbilities.candidate_y, candidate_x: jitterAbilities.candidate_x };

  // Varias seeds: alguna debe producir jitter distinto para X e Y (rompiendo
  // el empate exacto), que es justamente el escenario donde el bug de orden
  // se manifestaba.
  for (const seed of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) {
    const rXY = chooseMonsterIntent({
      monster: monsterOrderXY, profiles: PROFILES, abilities: jitterAbilities, combat: cleanCombat,
      memory: [], social: baseSocial(), rng: createSeededRng(seed)
    });
    const rYX = chooseMonsterIntent({
      monster: monsterOrderYX, profiles: PROFILES, abilities: abilitiesOrderYX, combat: cleanCombat,
      memory: [], social: baseSocial(), rng: createSeededRng(seed)
    });
    assert.equal(
      rXY.abilityId, rYX.abilityId,
      `seed=${seed}: reordenar effectiveKit/abilities no debe cambiar la ganadora bajo jitter`
    );
    assert.equal(
      rXY.debug.scoreByAbility.candidate_x, rYX.debug.scoreByAbility.candidate_x,
      `seed=${seed}: el score de candidate_x no debe depender del orden`
    );
    assert.equal(
      rXY.debug.scoreByAbility.candidate_y, rYX.debug.scoreByAbility.candidate_y,
      `seed=${seed}: el score de candidate_y no debe depender del orden`
    );
  }
});

// ---------------------------------------------------------------------------
// REV2 — Regresión #2: cooldowns booleanos estrictos
// ---------------------------------------------------------------------------
test('REV2 REGRESIÓN #2 — cooldowns rechaza valores no estrictamente booleanos', () => {
  const invalidValues = ['false', 'true', 1, 0, -1, [], {}, NaN, null, 'yes', '1'];
  for (const bad of invalidValues) {
    const monster = { ...MONSTERS.mantis_fixture, cooldowns: { ataque_devastador_cd: bad } };
    assert.throws(
      () => run({ monster, seed: 1 }),
      ContractError,
      `cooldowns con valor ${JSON.stringify(bad)} debe lanzar ContractError`
    );
  }
});

test('REV2 REGRESIÓN #2 — cooldowns acepta estrictamente true/false', () => {
  const monsterTrue = { ...MONSTERS.mantis_fixture, cooldowns: { ataque_devastador_cd: true } };
  const monsterFalse = { ...MONSTERS.mantis_fixture, cooldowns: { ataque_devastador_cd: false } };
  const rTrue = run({ monster: monsterTrue, seed: 1 });
  const rFalse = run({ monster: monsterFalse, seed: 1 });
  assert.notEqual(rTrue.abilityId, 'ataque_devastador');
  assert.equal(rFalse.status, STATUS.INTENT_SELECTED);
});

// ---------------------------------------------------------------------------
// SECCIÓN 19 — TESTS ADVERSARIALES
// ---------------------------------------------------------------------------

test('adversarial — empty kit', () => {
  const r = run({ monster: { ...MONSTERS.wolf_fixture, effectiveKit: [] }, seed: 1 });
  assert.equal(r.status, STATUS.NO_ELIGIBLE_INTENT);
});

test('adversarial — unknown ability in kit', () => {
  const monster = { ...MONSTERS.wolf_fixture, effectiveKit: ['no_existe'] };
  const r = run({ monster, seed: 1 });
  assert.equal(r.status, STATUS.NO_ELIGIBLE_INTENT);
  assert.equal(r.debug.considered[0].reason, 'UNKNOWN_ABILITY_IN_KIT');
});

test('adversarial — duplicate kit IDs', () => {
  const monster = { ...MONSTERS.wolf_fixture, effectiveKit: ['mordida', 'mordida'] };
  assert.throws(() => run({ monster, seed: 1 }), ContractError);
});

test('adversarial — unknown profile', () => {
  const monster = { ...MONSTERS.wolf_fixture, profileId: 'NO_EXISTE' };
  assert.throws(() => run({ monster, seed: 1 }), ContractError);
});

test('adversarial — invalid RNG (no random function)', () => {
  assert.throws(() => run({ rng: {}, seed: undefined }), ContractError);
});

test('adversarial — RNG = 1 (fuera de [0,1))', () => {
  const rng = { random: () => 1 };
  assert.throws(() => run({ monster: MONSTERS.rata_fixture, rng }), ContractError);
});

test('adversarial — RNG < 0', () => {
  const rng = { random: () => -0.1 };
  assert.throws(() => run({ monster: MONSTERS.rata_fixture, rng }), ContractError);
});

test('adversarial — NaN weight en catálogo', () => {
  const badAbilities = {
    ...ABILITIES,
    mordida: { ...ABILITIES.mordida, utility: { ...ABILITIES.mordida.utility, base: NaN } }
  };
  assert.throws(() => run({ abilities: badAbilities, seed: 1 }), ContractError);
});

test('adversarial — Infinity weight en catálogo', () => {
  const badAbilities = {
    ...ABILITIES,
    mordida: {
      ...ABILITIES.mordida,
      utility: { ...ABILITIES.mordida.utility, signalWeights: { PLAYER_LOW_HP: Infinity } }
    }
  };
  assert.throws(() => run({ abilities: badAbilities, seed: 1 }), ContractError);
});

test('adversarial — objetos anidados congelados (deep freeze) no rompen el kernel', () => {
  const monster = deepFreezeClone(MONSTERS.mantis_fixture);
  const r = run({ monster, seed: 1 });
  assert.equal(r.status, STATUS.INTENT_SELECTED);
});

test('adversarial — memory con más de 1000 entradas', () => {
  const bigMemory = [];
  for (let i = 0; i < 1500; i += 1) {
    bigMemory.push({ category: 'RECUPERACION', result: 'EFECTIVA', round: i });
  }
  const r = run({ monster: MONSTERS.wolf_fixture, memory: bigMemory, seed: 1 });
  assert.equal(r.debug.activeMemory.length, 2);
});

test('adversarial — pesos finitos enormes (positivo y negativo)', () => {
  const hugeAbilities = {
    ...ABILITIES,
    mordida: {
      ...ABILITIES.mordida,
      utility: { ...ABILITIES.mordida.utility, base: 1e15 }
    },
    acechar: {
      ...ABILITIES.acechar,
      utility: { ...ABILITIES.acechar.utility, base: -1e15 }
    }
  };
  const r = run({ abilities: hugeAbilities, seed: 1 });
  assert.equal(r.status, STATUS.INTENT_SELECTED);
  assert.equal(r.abilityId, 'mordida');
});

test('adversarial — signals vacío', () => {
  const combat = baseCombat({ signals: {} });
  // baseCombat merges overrides.signals con Object.assign sobre defaults; forzamos vacío real:
  const cleanCombat = { ...combat, signals: {} };
  const r = run({ combat: cleanCombat, seed: 1 });
  assert.equal(r.status, STATUS.INTENT_SELECTED);
});

test('adversarial — social ausente (opcional)', () => {
  const r = run({ social: undefined, seed: 1 });
  assert.equal(r.status, STATUS.INTENT_SELECTED);
});

test('adversarial — recentAbilityIds con IDs desconocidos', () => {
  const monster = { ...MONSTERS.wolf_fixture, recentAbilityIds: ['esto_no_existe', 'tampoco'] };
  const r = run({ monster, seed: 1 });
  assert.equal(r.status, STATUS.INTENT_SELECTED);
});

test('adversarial — llamadas repetidas producen el mismo resultado', () => {
  const results = [];
  for (let i = 0; i < 50; i += 1) results.push(run({ seed: 123 }));
  for (const r of results) assert.deepEqual(r, results[0]);
});

test('adversarial — mutar el objeto de retorno no debe alterar nada reutilizable', () => {
  const r = run({ seed: 1 });
  let threw = false;
  try { r.abilityId = 'HACKED'; } catch { threw = true; }
  const r2 = run({ seed: 1 });
  assert.ok(threw, 'el resultado debe estar congelado (strict mode)');
  assert.notEqual(r2.abilityId, 'HACKED');
});

// ---------------------------------------------------------------------------
// Resumen
// ---------------------------------------------------------------------------

console.log('');
console.log(`TOTAL: ${passCount + failCount}  PASS: ${passCount}  FAIL: ${failCount}`);
if (failCount > 0) {
  process.exitCode = 1;
}
