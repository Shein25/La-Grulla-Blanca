export function qiaoWorld(overrides = {}) {
  return {
    at: "puesto",
    playerPresent: false,
    playerNeedsHelp: false,
    playerHelped: false,
    playerReachable: true,
    anomalyPresent: false,
    anomalyInvestigated: false,
    dutyPending: true,
    dutySatisfied: false,
    dutyImportance: 90,
    danger: 5,
    urgency: 10,
    hasEvidence: false,
    superiorInformed: false,
    superiorAvailable: true,
    messengerAvailable: true,
    passageOpen: true,
    waited: false,
    ...overrides
  };
}

export function qiaoContext(world, overrides = {}) {
  return {
    playerPresent: world.playerPresent,
    playerRequestsHelp: world.playerNeedsHelp && !world.playerHelped,
    playerRank: 1,
    dutyImportance: world.dutyImportance,
    danger: world.danger,
    missionUrgency: world.urgency,
    anomalyPresent: world.anomalyPresent && !world.anomalyInvestigated,
    awayFromPost: world.at !== "puesto",
    superiorReachable: true,
    relevantKnowledge: "SOSPECHA",
    dutyMode: "trabajar",
    ...overrides
  };
}

export const QIAO_REN_SCENARIOS = {
  routineDuty: {
    description: "Deber institucional ordinario en Disciplina.",
    world: qiaoWorld(),
    contextOverrides: { dutyMode: "trabajar" }
  },
  m16CoordinationWithEvidence: {
    description: "Coordinación institucional de crisis con evidencia ya disponible.",
    world: qiaoWorld({
      dutyPending: true,
      dutyImportance: 95,
      danger: 75,
      urgency: 85,
      hasEvidence: true
    }),
    contextOverrides: { dutyMode: "trabajar", superiorReachable: true }
  },
  returnToPost: {
    description: "Qiao Ren fuera de su puesto de referencia sin objetivo superior activo.",
    world: qiaoWorld({
      at: "superior",
      dutyPending: false,
      dutySatisfied: true,
      dutyImportance: 95,
      danger: 5,
      urgency: 5
    }),
    contextOverrides: { dutyMode: "ninguno", superiorReachable: true }
  }
};
