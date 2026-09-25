export const JIANG_RUI_UTILITY_PROFILE = {
  id: "jiang_rui_lab",
  name: "Jiang Rui",
  role: "Capitán de patrulla",
  traits: {
    disciplina: 85,
    sociabilidad: 45,
    curiosidad: 65,
    prudencia: 75,
    lealtad_institucional: 85,
    empatia: 50
  },
  relationPlayer: {
    afinidad: 40,
    confianza: 40,
    respeto: 55,
    deuda: 0,
    temor: 0,
    rivalidad: 0
  },
  knowledge: {
    R1: "SOSPECHA",
    R2: "DESCONOCIDO",
    R3: "DESCONOCIDO"
  },
  behaviorState: {
    lastAction: null,
    consecutiveTurns: 0
  }
};

export const UTILITY_ACTION_TO_INTENT = Object.freeze({
  patrullar: "PATROL_ROUTE",
  investigar: "INVESTIGATE_ROUTE_ANOMALY",
  informar_superior: "REPORT_SUPERIOR",
  regresar_puesto: "RETURN_POST",
  esperar: "HOLD_POST"
});
