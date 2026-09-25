export const BASE_CONTEXT = Object.freeze({
  playerPresent: true,
  playerRequestsHelp: true,
  playerRank: 2,
  dutyImportance: 65,
  danger: 45,
  missionUrgency: 55,
  anomalyPresent: true,
  awayFromPost: false,
  superiorReachable: true,
  relevantKnowledge: 'SABE',
  topicSensitivity: 55,
  formalRestriction: 25,
});

export const SCENARIOS = Object.freeze({
  misma_situacion: {
    title: 'Misma situación para tres personalidades',
    context: { ...BASE_CONTEXT },
  },
  puesto_critico: {
    title: 'Puesto crítico, pedido de ayuda moderado',
    context: {
      ...BASE_CONTEXT,
      dutyImportance: 100,
      missionUrgency: 35,
      danger: 25,
      anomalyPresent: false,
    },
  },
  crisis_personal: {
    title: 'Jugador pide ayuda en crisis urgente',
    context: {
      ...BASE_CONTEXT,
      dutyImportance: 35,
      missionUrgency: 95,
      danger: 80,
      anomalyPresent: false,
    },
  },
  anomalia: {
    title: 'Anomalía sin pedido de ayuda',
    context: {
      ...BASE_CONTEXT,
      playerRequestsHelp: false,
      dutyImportance: 40,
      missionUrgency: 50,
      danger: 35,
      anomalyPresent: true,
    },
  },
  retorno_puesto: {
    title: 'NPC fuera de su puesto',
    context: {
      ...BASE_CONTEXT,
      playerRequestsHelp: false,
      anomalyPresent: false,
      awayFromPost: true,
      dutyImportance: 90,
      missionUrgency: 10,
      danger: 10,
    },
  },
});
