import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { createMemoryState, recordMemory } from '../motor-npc-vivo-v0.3-memory/memory.mjs';
import { decideFromMemory } from './decision-pipeline.mjs';
import { goldenNpc, goldenContext, goldenWorld } from './fixtures.mjs';

const rounds = Number(process.argv[2] ?? 500);
const seed = Number(process.argv[3] ?? 1337);
if (!Number.isSafeInteger(rounds) || rounds < 1 || !Number.isSafeInteger(seed)) {
  throw new TypeError('Uso: node stress.mjs [rounds>=1] [seed entero seguro]');
}

function rng(initial) {
  let state = initial >>> 0;
  return () => {
    state ^= state << 13; state ^= state >>> 17; state ^= state << 5;
    return (state >>> 0) / 0x100000000;
  };
}
const random = rng(seed);
const pick = (min, max) => min + Math.floor(random() * (max - min + 1));
const npcs = Array.from({ length: 16 }, (_, i) => {
  const npc = goldenNpc();
  npc.id = `synthetic_${i}`;
  npc.name = `Synthetic ${i}`;
  if (i > 0) {
    npc.traits.curiosidad = pick(40, 65);
    npc.traits.empatia = pick(45, 75);
    npc.traits.sociabilidad = pick(20, 80);
    npc.relationPlayer.afinidad = pick(25, 55);
    npc.relationPlayer.confianza = pick(25, 55);
  }
  return npc;
});

function event(key, kind, turn, importance, confidence, expiresTurn = null) {
  return { key, kind, subject: kind === 'PLAYER_LIED' ? 'superior' : 'jugador',
    value: true, importance, confidence, turn, expiresTurn };
}
function makeScenario(npc, round, index) {
  const mode = (round + index) % 6;
  const context = goldenContext();
  const world = goldenWorld();
  const options = {};
  let memory = createMemoryState();
  const importance = pick(40, 100), confidence = pick(40, 100);
  if (mode === 0 || mode === 3) {
    memory = recordMemory(memory, event('help', 'PLAYER_HELPED_ME', round,
      index === 0 ? 100 : importance, index === 0 ? 100 : confidence));
  } else if (mode === 1) {
    memory = recordMemory(memory, event('lie', 'PLAYER_LIED', round, importance, confidence));
  } else if (mode === 2) {
    memory = recordMemory(memory, event('expired', 'PLAYER_HELPED_ME', round,
      importance, confidence, round));
    memory = recordMemory(memory, event('irrelevant', 'ORDER_RECEIVED', round,
      importance, confidence));
  } else if (mode === 4) {
    memory = recordMemory(memory, event('irrelevant', 'SIGHTING_RELEVANT', round,
      importance, confidence));
  } else {
    memory = recordMemory(memory, event('help', 'PLAYER_HELPED_ME', round,
      importance, confidence));
    memory = recordMemory(memory, event('lie', 'PLAYER_LIED', round,
      pick(20, 80), pick(20, 80)));
  }
  const currentTurn = mode === 2 ? round + 1 : round;
  if (mode === 2) {
    context.playerRequestsHelp = false; world.playerNeedsHelp = false;
    context.anomalyPresent = false; world.anomalyPresent = false;
    context.missionUrgency = 0; world.urgency = 0;
    npc = structuredClone(npc);
    npc.traits.sociabilidad = 100;
    npc.relationPlayer.afinidad = 100;
    npc.relationPlayer.confianza = 100;
  }
  if (mode === 3) world.playerReachable = false;
  if (mode === 4) options.maxExpansions = 0;
  if (mode === 5) {
    context.dutyMode = ['vigilar', 'trabajar', 'patrullar'][pick(0, 2)];
    context.dutyImportance = 60; world.dutyImportance = 60;
  }
  return { npc, memory, currentTurn, context, world, options };
}

function finite(value) {
  if (typeof value === 'number') assert.ok(Number.isFinite(value), 'número no finito');
  else if (Array.isArray(value)) value.forEach(finite);
  else if (value && typeof value === 'object') Object.values(value).forEach(finite);
}

const counters = {
  seed, rounds, npcs: npcs.length, decisions: 0, memoryDecisionChanges: 0,
  planReady: 0, noPlan: 0, planningDeferred: 0, unmapped: 0,
  contributions: 0, ignoredMemories: 0,
};
const hash = createHash('sha256');
for (let round = 1; round <= rounds; round++) {
  for (let index = 0; index < npcs.length; index++) {
    const s = makeScenario(npcs[index], round, index);
    const inputsBefore = JSON.stringify(s);
    const out = decideFromMemory(s.npc, s.memory, s.currentTurn,
      s.context, s.world, s.options);
    assert.equal(JSON.stringify(s), inputsBefore, 'input mutado');
    counters.decisions++;
    counters.contributions += out.relationDerivation.contributions.length;
    counters.ignoredMemories += out.relationDerivation.ignoredMemories.length;
    for (const relation of Object.values(out.relationDerivation.relations)) {
      assert.ok(Number.isFinite(relation) && relation >= 0 && relation <= 100);
    }
    finite(out);
    if (out.status === 'PLAN_READY') {
      counters.planReady++;
      assert.equal(out.plan.status, 'PLAN_FOUND');
    } else if (out.status === 'NO_PLAN') {
      counters.noPlan++;
      assert.equal(out.plan.status, 'NO_PLAN');
    } else if (out.status === 'PLANNING_DEFERRED') {
      counters.planningDeferred++;
      assert.ok(['SEARCH_LIMIT', 'FRONTIER_LIMIT', 'COST_OVERFLOW'].includes(out.plan.status));
    } else if (out.status === 'UTILITY_ACTION_UNMAPPED') {
      counters.unmapped++;
      assert.equal(out.goalId, null);
      assert.equal(out.plan, null);
    } else throw new Error(`Estado inesperado ${out.status}`);
    if (out.relationDerivation.contributions.length) {
      const baseline = decideFromMemory(s.npc, createMemoryState(), 0,
        s.context, s.world, s.options);
      if (baseline.utilityDecision.action !== out.utilityDecision.action) {
        counters.memoryDecisionChanges++;
      }
    }
    hash.update(JSON.stringify(out));
  }
}
assert.ok(counters.memoryDecisionChanges > 0, 'la memoria nunca cambió una decisión');
assert.ok(counters.planReady > 0 && counters.noPlan > 0 && counters.unmapped > 0);
const report = { ...counters, digest: hash.digest('hex') };
console.log(JSON.stringify(report));
