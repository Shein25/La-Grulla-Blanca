export const MEI_LIAN_CANON={
  source:{file:"grulla-blanca_ver74.html",blob:"d34f7ea3f9de9344130aa072fac34d14a7a474d6",object:"NPC_DEF.mei_lian"},
  id:"mei_lian",
  nombre:"Mei Lian",
  categoria:"companero",
  rol:"Aspirante — saber médico/local, puente Secta-Sauces",
  sala_inicial:"patio",
  sala_inicial_clasificacion:"ELECCION_TECNICA_3C5",
  movilidad:"RUTA",
  territorio_normal:["patio","patio_cabanas","patio_servicios"],
  transito_tecnico:[],
  posicion_valida:["patio","patio_cabanas","patio_servicios"],
  rutas:[["patio","patio_cabanas"],["patio","patio_servicios"]],
  gates_en_ruta:[],
  territorio_por_etapa:{
    LI:"Patio → Medicina → Jardines.",
    LII:"Jardines → rutas orientales → Sauces Bajos.",
    LIII:"Medicina + Jardines + Sauces; Sala de Meridianos, Chen Bo, archivos clínicos.",
    M16:"SAUCES o MEDICINA según estado y responsables disponibles.",
    M17:"NO_CERRADO_EN_FUENTE",
    EPILOGO:"CANÓNICO: Estado final PUENTE_SECTA_SAUCES."
  },
  anclajes_documentados:[
    "M02–M03 (MEI_01_LO_QUE_YA_SABIA)",
    "M05 (MEI_02_NOMBRE_FORMAL, MEI_03_REGRESO_SAUCES)",
    "M10 (MEI_04_DOS_CASAS)",
    "M16 (MEI_05_SAUCES_M16, autónoma)"
  ],
  conocimiento_inicial:{R1:"SOSPECHA",R2:"DESCONOCIDO",R3:"DESCONOCIDO",R4:"DESCONOCIDO",R5:"DESCONOCIDO",R6:"DESCONOCIDO",R7:"DESCONOCIDO",R8:"DESCONOCIDO",R9:"DESCONOCIDO",R10:"DESCONOCIDO"}
};

export const MEI_LIAN_POLICY_STATUS={
  utilityTraits:"EXPERIMENTAL_NON_CANONICAL",
  m16ConditionalFront:"CANONICAL_REQUIREMENT",
  frontIdentity:"CANONICAL_DOMAIN_CAPABILITY_GAP"
};

export const MEI_LIAN_REQUIRED_CAPABILITY="M16_FRONT_ASSIGNMENT_SAUCES_OR_MEDICINA";
