export const PEI_LUO_CANON = {
  source: {
    file: "grulla-blanca_ver74.html",
    blob: "d34f7ea3f9de9344130aa072fac34d14a7a474d6",
    object: "NPC_DEF.pei_luo"
  },
  id: "pei_luo",
  nombre: "Pei Luo",
  categoria: "funcional",
  rol: "Responsable de Cocina/Comedor",
  sala_inicial: "cocina_comunal",
  sala_inicial_clasificacion: "ELECCION_TECNICA_3C5",
  movilidad: "RUTA",
  territorio_normal: [
    "cocina_comunal",
    "comedor_externos"
  ],
  transito_tecnico: [],
  posicion_valida: [
    "cocina_comunal",
    "comedor_externos"
  ],
  rutas: [[
    "cocina_comunal",
    "comedor_externos"
  ]],
  gates_en_ruta: [],
  territorio_por_etapa: {
    LI: "NO_CERRADO_EN_FUENTE",
    LII: "NO_CERRADO_EN_FUENTE",
    LIII: "NO_CERRADO_EN_FUENTE",
    M16: "Organiza raciones durante la crisis (T211 §10); no es responsable de ningún frente de los 6 de T281.",
    M17: "NO_CERRADO_EN_FUENTE",
    EPILOGO: "NO_CERRADO_EN_FUENTE"
  },
  anclajes_documentados: [],
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

export const PEI_LUO_POLICY_STATUS = {
  normalRoutine: "EXPERIMENTAL_NON_CANONICAL",
  crisisRations: "CANON_SUPPORTED_M16_POLICY_HYPOTHESIS"
};

export const PEI_LUO_ALLOWED_INTENTS = [
  "PREPARE_RATIONS",
  "MOVE_TO_DINING",
  "SERVE_RATIONS",
  "RETURN_KITCHEN",
  "RESET_KITCHEN",
  "ORGANIZE_CRISIS_RATIONS"
];
