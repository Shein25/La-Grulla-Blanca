import { createAutonomousLoopState } from './autonomous-loop.mjs';

export function npcFixture(id = 'npc_helper', profile = {}) {
  const traits = { disciplina: 30, sociabilidad: 45, curiosidad: 25, prudencia: 20,
    lealtad_institucional: 30, empatia: 90, ...profile.traits };
  const relationPlayer = { afinidad: 50, confianza: 50, respeto: 50, deuda: 0,
    temor: 0, rivalidad: 0, ...profile.relationPlayer };
  return { id, name: `Synthetic ${id}`, role: 'test', traits, relationPlayer,
    knowledge: { R1: 'DESCONOCIDO', R2: 'DESCONOCIDO', R3: 'DESCONOCIDO', ...profile.knowledge },
    behaviorState: { lastAction: null, consecutiveTurns: 0, ...profile.behaviorState } };
}

export function worldFixture(overrides = {}) {
  return { at: 'puesto', playerPresent: true, playerNeedsHelp: true, playerHelped: false,
    playerReachable: true, anomalyPresent: false, anomalyInvestigated: false,
    dutyPending: false, dutySatisfied: false, dutyImportance: 10, danger: 0, urgency: 80,
    hasEvidence: false, superiorInformed: false, superiorAvailable: true,
    messengerAvailable: true, passageOpen: true, waited: false, ...overrides };
}

export function contextFixture(world, overrides = {}) {
  return { playerPresent: world.playerPresent,
    playerRequestsHelp: world.playerNeedsHelp && !world.playerHelped,
    playerRank: 1, dutyImportance: world.dutyImportance, danger: world.danger,
    missionUrgency: world.urgency,
    anomalyPresent: world.anomalyPresent && !world.anomalyInvestigated,
    awayFromPost: world.at !== 'puesto', superiorReachable: true,
    relevantKnowledge: 'DESCONOCIDO', dutyMode: 'ninguno', ...overrides };
}

export function initialFixture(id = 'npc_helper', worldOverrides = {}, profile = {}, contextOverrides = {}) {
  const world = worldFixture(worldOverrides);
  return { npc: npcFixture(id, profile), world,
    utilityContext: contextFixture(world, contextOverrides) };
}

export function stateFixture(items = [initialFixture()], configs = null) {
  return createAutonomousLoopState({ npcs: items,
    schedulerConfigs: configs ?? items.map(item => ({ id: item.npc.id,
      interval: 1, minGap: 0, firstPeriodicTurn: 1 })) });
}

export function observationFixture(runtime, worldOverrides = {}, contextOverrides = {}, memoryEvents = []) {
  const world = { ...runtime.world, ...worldOverrides };
  const { playerRank, superiorReachable, relevantKnowledge, dutyMode } = runtime.utilityContext;
  return { npcId: runtime.id, world,
    utilityContext: contextFixture(world, { playerRank, superiorReachable, relevantKnowledge,
      dutyMode, ...contextOverrides }),
    memoryEvents };
}

export function memoryEventFixture(turn, kind = 'PLAYER_HELPED_ME', key = `memory-${turn}`) {
  return { key, kind, subject: 'player', value: true,
    importance: 100, confidence: 100, turn };
}
