export const QIAO_REN_CANON = {
  source: {
    file: "grulla-blanca_ver74.html",
    blob: "d34f7ea3f9de9344130aa072fac34d14a7a474d6",
    object: "NPC_DEF.qiao_ren"
  },
  id: "qiao_ren",
  nombre: "Qiao Ren",
  categoria: "autoridad",
  rol: "Disciplina y Administración",
  sala_inicial: "pabellon_disciplina",
  sala_inicial_clasificacion: "CANÓNICO",
  movilidad: "RUTA",
  territorio_normal: [
    "pabellon_disciplina",
    "corredor_norte",
    "interior_sala_consejo"
  ],
  transito_tecnico: [
    "escalinata_interior",
    "interior_umbral_sur",
    "interior_patio_blanco",
    "interior_patio_internos",
    "interior_sala_estudio",
    "interior_corredor_consejo",
    "interior_antesala_consejo"
  ],
  posicion_valida: [
    "corredor_norte",
    "escalinata_interior",
    "interior_antesala_consejo",
    "interior_corredor_consejo",
    "interior_patio_blanco",
    "interior_patio_internos",
    "interior_sala_consejo",
    "interior_sala_estudio",
    "interior_umbral_sur",
    "pabellon_disciplina"
  ],
  rutas: [[
    "pabellon_disciplina",
    "corredor_norte",
    "escalinata_interior",
    "interior_umbral_sur",
    "interior_patio_blanco",
    "interior_patio_internos",
    "interior_sala_estudio",
    "interior_corredor_consejo",
    "interior_antesala_consejo",
    "interior_sala_consejo"
  ]],
  gates_en_ruta: ["SECTA_INTERIOR"],
  territorio_por_etapa: {
    LI: "RUTA entre Disciplina/Interior/Consejo.",
    LII: "RUTA entre Disciplina/Interior/Consejo.",
    LIII: "RUTA entre Disciplina/Interior/Consejo.",
    M16: "Coordinación institucional durante M16; no responsable de un frente concreto.",
    M17: "Asiste; debe autorizar la excepción que habilita NUCLEO_PROFUNDO.",
    EPILOGO: "PROPUESTA_HISTORICA"
  },
  anclajes_documentados: [
    "M03 (cierre de misión, ANCLADA en pabellon_disciplina)",
    "M07",
    "M16 (coordinación)",
    "M17",
    "comparecencia/epílogo"
  ],
  conocimiento_inicial: {
    R1: "SOSPECHA",
    R2: "DESCONOCIDO",
    R3: "DESCONOCIDO",
    R4: "DESCONOCIDO",
    R5: "SOSPECHA",
    R6: "DESCONOCIDO",
    R7: "DESCONOCIDO",
    R8: "DESCONOCIDO",
    R9: "DESCONOCIDO",
    R10: "DESCONOCIDO"
  }
};

export const QIAO_REN_POLICY_STATUS = {
  utilityTraits: "EXPERIMENTAL_NON_CANONICAL",
  routineDuty: "EXPERIMENTAL_CANON_COMPATIBLE",
  crisisCoordination: "CANON_SUPPORTED_M16_POLICY_HYPOTHESIS",
  m17Authorization: "CANONICAL_REQUIREMENT_CAPABILITY_GAP"
};

export const QIAO_REN_M17_REQUIRED_CAPABILITY = "AUTHORIZE_EXCEPTION_NUCLEO_PROFUNDO";
