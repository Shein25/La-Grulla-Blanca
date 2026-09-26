export const ZHAO_WEN_CANON={
  source:{file:"grulla-blanca_ver74.html",blob:"d34f7ea3f9de9344130aa072fac34d14a7a474d6",object:"NPC_DEF.zhao_wen"},
  id:"zhao_wen",
  nombre:"Zhao Wen",
  categoria:"companero",
  rol:"Aspirante — piezas documentales / análisis",
  sala_inicial:"sala_comun_externos",
  sala_inicial_clasificacion:"ELECCION_TECNICA_3C5",
  movilidad:"RUTA",
  territorio_normal:["sala_comun_externos","patio_cabanas","lavadero_externos"],
  transito_tecnico:[],
  posicion_valida:["lavadero_externos","patio_cabanas","sala_comun_externos"],
  rutas:[
    ["sala_comun_externos","patio_cabanas"],
    ["sala_comun_externos","lavadero_externos"]
  ],
  gates_en_ruta:[],
  territorio_por_etapa:{
    LI:"Patio → Sala Común → tablones/textos; todavía no Archivo profundo.",
    LII:"Patio → Administración → primeras salas de Archivo; Registro/escribas.",
    LIII:"Archivos: Catálogo → Copistas → Lectura → Archivo Histórico; no accede a Restringido antes que el jugador.",
    M16:"Archivo/Formaciones o apoyo transversal según versión canónica final; no necesariamente responsable principal.",
    M17:"NO_CERRADO_EN_FUENTE",
    EPILOGO:"CANÓNICO: Estado final INCERTIDUMBRE_RESPONSABLE."
  },
  anclajes_documentados:[
    "M02–M04 (ZHAO_01_NOTAS_EN_EL_MARGEN)",
    "M06 (ZHAO_02_NO_ES_PRUEBA)",
    "M09 (ZHAO_03_ARCHIVO_CERRADO, ARCHIVO_RESTRINGIDO concedido por Qiao Ren)",
    "M09–M11 (ZHAO_04_ZHAO_LUO)",
    "M16 (ZHAO_05_DECIDIR_INCOMPLETO)"
  ],
  conocimiento_inicial:{R1:"DESCONOCIDO",R2:"DESCONOCIDO",R3:"DESCONOCIDO",R4:"DESCONOCIDO",R5:"DESCONOCIDO",R6:"DESCONOCIDO",R7:"DESCONOCIDO",R8:"DESCONOCIDO",R9:"DESCONOCIDO",R10:"DESCONOCIDO"}
};

export const ZHAO_WEN_POLICY_STATUS={
  utilityTraits:"EXPERIMENTAL_NON_CANONICAL",
  dialogueCalibration:"EXPERIMENTAL_MECHANICS_TEST",
  restrictedArchiveAccess:"CANONICAL_REQUIREMENT_CAPABILITY_GAP"
};

export const ZHAO_WEN_REQUIRED_ACCESS_CAPABILITY="ARCHIVO_RESTRINGIDO_PERMISSION";
