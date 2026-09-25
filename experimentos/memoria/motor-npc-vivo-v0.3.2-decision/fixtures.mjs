import { BASE_WORLD } from '../../goap/motor-npc-vivo-v0.2-goap/world-fixtures.mjs';

// Identidades y escenarios exclusivamente sintéticos; no son NPC canónicos.
export function goldenNpc() {
  return {
    id: 'memory_flip', name: 'Memory Flip', role: 'Fixture sintético',
    traits: {
      disciplina: 50, sociabilidad: 30, curiosidad: 55, prudencia: 40,
      lealtad_institucional: 50, empatia: 60,
    },
    relationPlayer: {
      afinidad: 35, confianza: 35, respeto: 50, deuda: 0, temor: 0, rivalidad: 0,
    },
    knowledge: { R1: 'SABE', R2: 'DESCONOCIDO', R3: 'DESCONOCIDO' },
    behaviorState: { lastAction: null, consecutiveTurns: 0 },
  };
}

export function goldenContext() {
  return {
    playerPresent: true, playerRequestsHelp: true, playerRank: 2,
    dutyImportance: 20, danger: 20, missionUrgency: 60,
    anomalyPresent: true, awayFromPost: false, superiorReachable: false,
    relevantKnowledge: 'SABE', dutyMode: 'ninguno',
  };
}

export function goldenWorld() {
  return {
    ...BASE_WORLD,
    at: 'puesto', playerPresent: true, playerReachable: true,
    playerNeedsHelp: true, playerHelped: false,
    anomalyPresent: true, anomalyInvestigated: false,
    urgency: 60, danger: 20, dutyImportance: 20,
  };
}
