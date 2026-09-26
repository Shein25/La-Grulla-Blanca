export function linWorld(overrides = {}) {
  return {
    at: "puesto",
    playerPresent: true,
    playerNeedsHelp: true,
    playerHelped: false,
    playerReachable: true,
    anomalyPresent: false,
    anomalyInvestigated: false,
    dutyPending: false,
    dutySatisfied: false,
    dutyImportance: 20,
    danger: 10,
    urgency: 40,
    hasEvidence: false,
    superiorInformed: false,
    superiorAvailable: true,
    messengerAvailable: true,
    passageOpen: true,
    waited: false,
    ...overrides
  };
}

export function linContext(world, overrides = {}) {
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
    relevantKnowledge: "DESCONOCIDO",
    dutyMode: "ninguno",
    ...overrides
  };
}

export function playerHelpedMemory(turn = 1) {
  return {
    key: "player-helped-lin-yue",
    kind: "PLAYER_HELPED_ME",
    subject: "player",
    value: true,
    importance: 100,
    confidence: 100,
    turn
  };
}

export const LIN_YUE_SCENARIOS = {
  socialBaseline: {
    description: "Jugador presente y pide ayuda; sin memoria social previa.",
    world: linWorld(),
    contextOverrides: {}
  },
  socialAfterPlayerHelped: {
    description: "Mismo contexto, pero se registra memoria PLAYER_HELPED_ME antes de decidir.",
    world: linWorld(),
    contextOverrides: {},
    memoryKind: "PLAYER_HELPED_ME"
  },
  m16RouteInitiative: {
    description: "Requisito canónico de desplazamiento autónomo a RUTAS en M16; usado como prueba de capacidad.",
    requiredCapability: "SELF_INITIATED_ROUTE_TRAVEL_TO_RUTAS"
  }
};
