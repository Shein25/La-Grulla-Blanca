export const JIANG_RUI_CANON = {
  source: {
    file: "grulla-blanca_ver74.html",
    blob: "d34f7ea3f9de9344130aa072fac34d14a7a474d6",
    object: "NPC_DEF.jiang_rui"
  },
  id: "jiang_rui",
  nombre: "Jiang Rui",
  categoria: "intermedio",
  rol: "Capitán de patrulla",
  sala_inicial: "puesto_valle",
  sala_inicial_clasificacion: "ELECCION_TECNICA_3C5",
  movilidad: "RUTA",
  territorio_normal: [
    "puesto_valle",
    "valle_explanada",
    "patio_puesto_valle"
  ],
  transito_tecnico: [],
  posicion_valida: [
    "patio_puesto_valle",
    "puesto_valle",
    "valle_explanada"
  ],
  rutas: [
    ["puesto_valle","valle_explanada"],
    ["puesto_valle","patio_puesto_valle"]
  ],
  gates_en_ruta: [],
  territorio_por_etapa: {
    LI: "Puerta/Puesto (T211 §3).",
    LII: "rutas completas (clave propia LII).",
    LIII: "territorio + investigación (clave propia LIII).",
    M16: "ANCLADO Rutas (T211 §3); rutas/Bosques (T244); responsable principal (junto a Ren Bo) del frente RUTAS (T281).",
    M17: "NO_CERRADO_EN_FUENTE",
    EPILOGO: "CANÓNICO (T211 §3): patrulla/reparaciones."
  },
  anclajes_documentados: [
    "M04–M07 (ANCLADO en Cruce Patrullas → Sala Informes según avance)",
    "M16 (responsable Rutas)"
  ],
  conocimiento_inicial: {
    R1: "SOSPECHA",
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

export const JIANG_RUI_POLICY_STATUS = {
  patrol: "CANON_SUPPORTED_POLICY_HYPOTHESIS",
  investigate: "CANON_SUPPORTED_LIII_POLICY_HYPOTHESIS",
  routeCrisis: "CANON_SUPPORTED_M16_POLICY_HYPOTHESIS",
  utilityTraits: "EXPERIMENTAL_NON_CANONICAL"
};

export const JIANG_RUI_ALLOWED_INTENTS = [
  "HOLD_POST",
  "PATROL_ROUTE",
  "INVESTIGATE_ROUTE_ANOMALY",
  "REPORT_SUPERIOR",
  "RETURN_POST"
];
