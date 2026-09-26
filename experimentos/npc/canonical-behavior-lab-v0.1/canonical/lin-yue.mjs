export const LIN_YUE_CANON = {
  source: {
    file: "grulla-blanca_ver74.html",
    blob: "d34f7ea3f9de9344130aa072fac34d14a7a474d6",
    object: "NPC_DEF.lin_yue"
  },
  id: "lin_yue",
  nombre: "Lin Yue",
  categoria: "companero",
  rol: "Aspirante — enlace territorial / rutas",
  sala_inicial: "patio_marcial",
  sala_inicial_clasificacion: "ELECCION_TECNICA_3C5",
  movilidad: "RUTA",
  territorio_normal: [
    "patio_marcial",
    "sala_formas",
    "patio_campana"
  ],
  transito_tecnico: [],
  posicion_valida: [
    "patio_campana",
    "patio_marcial",
    "sala_formas"
  ],
  rutas: [
    ["patio_marcial","sala_formas"],
    ["patio_marcial","patio_campana"]
  ],
  gates_en_ruta: [],
  territorio_por_etapa: {
    LI: "Patio Exterior + Marcial (C1 §K).",
    LII: "añade rutas y Puesto del Valle: Patio → Marcial → Puerta Roja → rutas de patrulla; también Bosques, Producción.",
    LIII: "Marcial → rutas → Recinto Interior ocasional; Marcial Alto.",
    M16: "ANCLADA en Rutas; responsable/ancla principal junto a Jiang Rui/Ren Bo. Va a RUTAS por iniciativa propia (LIN_05_RUTAS_M16) salvo circunstancia narrativa distinta.",
    M17: "NO_CERRADO_EN_FUENTE",
    EPILOGO: "CANÓNICO: Estado final COORDINADORA_TERRITORIAL."
  },
  anclajes_documentados: [
    "M01–M03 (LIN_01_PRIMERA_RUTA)",
    "M04 (LIN_02_DOS_RITMOS)",
    "M05–M07 (LIN_03_NO_LLEGAS_A_TODO)",
    "M16 (LIN_05_RUTAS_M16, autónoma)"
  ],
  conocimiento_inicial: {
    R1: "DESCONOCIDO",
    R2: "DESCONOCIDO",
    R3: "DESCONOCIDO",
    R4: "DESCONOCIDO",
    R5: "DESCONOCIDO",
    R6: "DESCONOCIDO",
    R7: "DESCONOCIDO",
    R8: "DESCONOCIDO",
    R9: "DESCONOCIDO",
    R10: "DESCONOCIDO"
  }
};

export const LIN_YUE_POLICY_STATUS = {
  utilityTraits: "EXPERIMENTAL_NON_CANONICAL",
  baseRelations: "EXPERIMENTAL_NON_CANONICAL",
  socialMemoryFlip: "EXPERIMENTAL_MECHANICS_TEST",
  m16RouteInitiative: "CANONICAL_REQUIREMENT_CAPABILITY_GAP_PHYSICAL_NAVIGATION"
};

export const LIN_YUE_M16_REQUIRED_CAPABILITY = "SELF_INITIATED_ROUTE_TRAVEL_TO_RUTAS";
