import { createHash } from 'node:crypto';
import { chooseMonsterIntent, ContractError } from './engine.mjs';
import { PROFILES } from './profiles.mjs';
import { ABILITIES, MONSTERS, createSeededRng } from './fixtures.mjs';

const SEEDS = [1337, 1, 42, 999, 20260924];
const DECISIONS_PER_SEED = 10000;
const REPEAT_SEED = 1337;

const PROFILE_IDS = Object.keys(PROFILES);
const MONSTER_TEMPLATES = Object.values(MONSTERS);
const ABILITY_IDS = Object.keys(ABILITIES);
const MEMORY_CATEGORIES = ['DEFENSA_ABSORCION', 'RECUPERACION', 'CONTROL_FALLIDO', 'HUIDA'];
const MEMORY_RESULTS = ['EFECTIVA', 'FALLIDA', 'NEUTRA'];
const SOCIAL_PROFILE_IDS = ['SOLITARIO', 'TERRITORIAL', 'MANADA', 'COLONIA', 'OPORTUNISTA', 'RED', 'REBAÑO'];

// Generador de casos coherentes: usa la propia RNG del stress (independiente
// del rng inyectado al kernel) para armar escenarios plausibles, no basura.
function makeCaseGenerator(seed) {
  const genRng = createSeededRng(seed ^ 0x9e3779b9);
  const rand = () => genRng.random();
  const pick = (arr) => arr[Math.floor(rand() * arr.length)];
  const randInt = (min, max) => min + Math.floor(rand() * (max - min + 1));

  return function generateCase() {
    const template = pick(MONSTER_TEMPLATES);
    const kitSize = randInt(1, ABILITY_IDS.length);
    const shuffledAbilities = [...ABILITY_IDS].sort(() => rand() - 0.5);
    const effectiveKit = shuffledAbilities.slice(0, kitSize);

    const preferences = {};
    for (const cat of ['OFENSIVA', 'DEFENSA', 'EVASION', 'CONTROL', 'PREPARACION']) {
      preferences[cat] = Math.round(rand() * 200) / 100; // 0.00 .. 2.00
    }

    const recentAbilityIds = [];
    const recentCount = randInt(0, 3);
    for (let i = 0; i < recentCount; i += 1) recentAbilityIds.push(pick(effectiveKit));

    const cooldowns = {};
    for (const id of effectiveKit) {
      const ability = ABILITIES[id];
      if (ability.cooldownKey && rand() < 0.3) cooldowns[ability.cooldownKey] = true;
    }

    const monster = {
      id: `${template.id}_stress`,
      profileId: pick(PROFILE_IDS),
      socialProfileId: pick(SOCIAL_PROFILE_IDS),
      effectiveKit,
      preferences,
      recentAbilityIds,
      cooldowns
    };

    const memoryLen = randInt(0, 8);
    const memory = [];
    for (let i = 0; i < memoryLen; i += 1) {
      memory.push({ category: pick(MEMORY_CATEGORIES), result: pick(MEMORY_RESULTS), round: i });
    }

    const combat = {
      round: randInt(1, 30),
      self: { hpRatio: Math.round(rand() * 100) / 100, statuses: [] },
      player: { hpRatio: Math.round(rand() * 100) / 100, visibleStates: [] },
      signals: {
        SELF_LOW_HP: rand() < 0.3 ? 1 : 0,
        PLAYER_LOW_HP: rand() < 0.3 ? 1 : 0,
        PLAYER_ABSORPTION: rand() < 0.2 ? 1 : 0,
        PLAYER_EVASION: rand() < 0.2 ? 1 : 0,
        ALLY_PRESENT: rand() < 0.5 ? 1 : 0,
        OUTNUMBER_PLAYER: rand() < 0.3 ? 1 : 0
      }
    };

    const social = {
      alliesAlive: randInt(0, 3),
      sameSpeciesAllies: randInt(0, 3),
      outnumbersPlayer: rand() < 0.4
    };

    return { monster, profiles: PROFILES, abilities: ABILITIES, combat, memory, social };
  };
}

// Semilla determinista derivada de (seed, índice de decisión). Reemplaza el
// stream continuo de RNG usado en REV1: con un stream continuo, "repetir la
// misma decisión" para medir side effects reales (corrección #3) no era
// directo, porque consumir RNG de más desincronizaba todo lo que venía
// después. Con una semilla por-escenario, cada decisión es reproducible de
// forma aislada sin afectar a las demás, y la corrida completa sigue siendo
// 100% determinista a partir de (seed, DECISIONS_PER_SEED).
function scenarioSeed(seed, index) {
  return (Math.imul(seed ^ 0x9e3779b9, 0x85ebca6b) ^ Math.imul(index + 1, 0xc2b2ae35)) >>> 0;
}

function runSeed(seed, decisionCount) {
  const generateCase = makeCaseGenerator(seed);

  const metrics = {
    decisions: 0,
    intentSelected: 0,
    noEligibleIntent: 0,
    selectionsByProfile: {},
    selectionsByAbility: {},
    memoryInfluencedCases: 0,
    socialInfluencedCases: 0,
    repeatPenaltyCases: 0,
    ties: 0,
    tiesResolvedByRng: 0,
    invalidSelections: 0,
    inputMutations: 0,
    executionSideEffects: 0,
    nondeterministicMismatches: 0
  };

  const canonicalResults = [];

  for (let i = 0; i < decisionCount; i += 1) {
    const scenario = generateCase();
    const seedForDecision = scenarioSeed(seed, i);
    const beforeSnapshot = JSON.stringify({
      monster: scenario.monster, combat: scenario.combat, memory: scenario.memory, social: scenario.social
    });

    let result;
    try {
      result = chooseMonsterIntent({ ...scenario, rng: createSeededRng(seedForDecision) });
    } catch (err) {
      if (err instanceof ContractError) {
        // Escenario mal formado por generación adversarial no es el objetivo
        // de este modo coherente; no debería ocurrir. Si ocurre, se cuenta
        // como selección inválida para que quede visible en las métricas.
        metrics.invalidSelections += 1;
        continue;
      }
      throw err;
    }

    const afterSnapshot = JSON.stringify({
      monster: scenario.monster, combat: scenario.combat, memory: scenario.memory, social: scenario.social
    });
    if (beforeSnapshot !== afterSnapshot) metrics.inputMutations += 1;

    // REV2 (corrección #3): executionSideEffects deja de ser un contador que
    // "queda en cero por construcción sin comprobar nada". Se mide de verdad:
    // se repite EXACTAMENTE la misma decisión (mismo escenario, RNG fresca
    // con la misma semilla) y se exige un resultado byte-idéntico. Cualquier
    // divergencia entre ambas corridas sólo puede venir de estado oculto,
    // fugas entre llamadas o un efecto colateral real — nunca de la propia
    // lógica de decisión, que es pura.
    let replay;
    let replayFailed = false;
    try {
      replay = chooseMonsterIntent({ ...scenario, rng: createSeededRng(seedForDecision) });
    } catch (err) {
      if (err instanceof ContractError) {
        replayFailed = true;
      } else {
        throw err;
      }
    }
    if (replayFailed || JSON.stringify(replay) !== JSON.stringify(result)) {
      metrics.executionSideEffects += 1;
    }

    metrics.decisions += 1;

    if (result.status === 'INTENT_SELECTED') {
      metrics.intentSelected += 1;
      metrics.selectionsByProfile[scenario.monster.profileId] =
        (metrics.selectionsByProfile[scenario.monster.profileId] || 0) + 1;
      metrics.selectionsByAbility[result.abilityId] =
        (metrics.selectionsByAbility[result.abilityId] || 0) + 1;

      // REV2 (corrección #3): memoryInfluencedCases ya no significa
      // "existía una ventana de memoria no vacía" (eso era un proxy débil:
      // la ventana podía estar llena de eventos con categorías que ninguna
      // habilidad pondera). Ahora mide influencia real: que la memoria haya
      // aportado un término distinto de cero al score de la habilidad
      // efectivamente elegida.
      const memoryWeighted = result.debug.considered.some((c) => c.abilityId === result.abilityId
        && c.breakdown && c.breakdown.memory !== 0);
      if (memoryWeighted) metrics.memoryInfluencedCases += 1;

      if (scenario.monster.recentAbilityIds.includes(result.abilityId)) metrics.repeatPenaltyCases += 1;
      if (result.debug.tieBrokenByRng) {
        metrics.ties += 1;
        metrics.tiesResolvedByRng += 1;
      }

      const socialWeighted = result.debug.considered.some((c) => c.abilityId === result.abilityId
        && c.breakdown && c.breakdown.social !== 0);
      if (socialWeighted) metrics.socialInfluencedCases += 1;

      if (!scenario.monster.effectiveKit.includes(result.abilityId)) metrics.invalidSelections += 1;
      if (!ABILITIES[result.abilityId]) metrics.invalidSelections += 1;
    } else {
      metrics.noEligibleIntent += 1;
    }

    canonicalResults.push(canonicalizeResult(scenario.monster.id, result));
  }

  return { metrics, canonicalResults };
}

function canonicalizeResult(monsterId, result) {
  // Representación canónica y estable: sin timestamps, sin rutas, orden fijo.
  if (result.status === 'NO_ELIGIBLE_INTENT') {
    return { monsterId, status: result.status, reason: result.reason };
  }
  return {
    monsterId,
    status: result.status,
    abilityId: result.abilityId,
    tieBrokenByRng: result.debug.tieBrokenByRng,
    scoreByAbility: sortObjectKeys(result.debug.scoreByAbility)
  };
}

function sortObjectKeys(obj) {
  const out = {};
  for (const k of Object.keys(obj).sort()) out[k] = obj[k];
  return out;
}

function digestOf(canonicalResults) {
  const hash = createHash('sha256');
  hash.update(JSON.stringify(canonicalResults));
  return hash.digest('hex');
}

function main() {
  const digests = {};
  let totalDecisions = 0;
  const aggregate = {
    invalidSelections: 0, inputMutations: 0, executionSideEffects: 0, nondeterministicMismatches: 0
  };

  console.log('STRESS — Monster Combat AI v0.1');
  console.log(`decisions per seed: ${DECISIONS_PER_SEED}`);
  console.log('');

  for (const seed of SEEDS) {
    const { metrics, canonicalResults } = runSeed(seed, DECISIONS_PER_SEED);
    const digest = digestOf(canonicalResults);
    digests[seed] = digest;
    totalDecisions += metrics.decisions;
    aggregate.invalidSelections += metrics.invalidSelections;
    aggregate.inputMutations += metrics.inputMutations;
    aggregate.executionSideEffects += metrics.executionSideEffects;

    console.log(`seed ${seed}`);
    console.log(`  decisions=${metrics.decisions} intentSelected=${metrics.intentSelected} noEligibleIntent=${metrics.noEligibleIntent}`);
    console.log(`  ties=${metrics.ties} tiesResolvedByRng=${metrics.tiesResolvedByRng}`);
    console.log(`  memoryInfluencedCases=${metrics.memoryInfluencedCases} socialInfluencedCases=${metrics.socialInfluencedCases} repeatPenaltyCases=${metrics.repeatPenaltyCases}`);
    console.log(`  invalidSelections=${metrics.invalidSelections} inputMutations=${metrics.inputMutations} executionSideEffects=${metrics.executionSideEffects}`);
    console.log(`  selectionsByProfile=${JSON.stringify(sortObjectKeys(metrics.selectionsByProfile))}`);
    console.log(`  selectionsByAbility=${JSON.stringify(sortObjectKeys(metrics.selectionsByAbility))}`);
    console.log(`  digest=${digest}`);
    console.log('');
  }

  // Repetición de la seed 1337: debe dar digest idéntico byte a byte.
  const repeatRun = runSeed(REPEAT_SEED, DECISIONS_PER_SEED);
  const repeatDigest = digestOf(repeatRun.canonicalResults);
  const nondeterministicMismatches = repeatDigest === digests[REPEAT_SEED] ? 0 : 1;
  aggregate.nondeterministicMismatches = nondeterministicMismatches;

  console.log(`REPEATED SEED ${REPEAT_SEED} digest=${repeatDigest}`);
  console.log(`REPEATED SEED MATCH: ${nondeterministicMismatches === 0 ? 'YES' : 'NO'}`);
  console.log('');
  console.log(`TOTAL DECISIONS: ${totalDecisions}`);
  console.log(`invalidSelections=${aggregate.invalidSelections}`);
  console.log(`inputMutations=${aggregate.inputMutations}`);
  console.log(`executionSideEffects=${aggregate.executionSideEffects}`);
  console.log(`nondeterministicMismatches=${aggregate.nondeterministicMismatches}`);

  const criticalOk = aggregate.invalidSelections === 0
    && aggregate.inputMutations === 0
    && aggregate.executionSideEffects === 0
    && aggregate.nondeterministicMismatches === 0;

  console.log('');
  console.log(`STRESS RESULT: ${criticalOk ? 'PASS' : 'FAIL'}`);
  if (!criticalOk) process.exitCode = 1;
}

main();
