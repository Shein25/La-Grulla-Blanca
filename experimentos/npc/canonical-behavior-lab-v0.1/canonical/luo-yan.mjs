export const LUO_YAN_CANON={
  source:{file:"grulla-blanca_ver74.html",blob:"d34f7ea3f9de9344130aa072fac34d14a7a474d6",object:"NPC_DEF.luo_yan"},
  id:"luo_yan",
  nombre:"Luo Yan",
  categoria:"companero",
  rol:"Aspirante — protocolo/historia oficial, lealtad institucional",
  sala_inicial:"registro",
  sala_inicial_clasificacion:"ELECCION_TECNICA_3C5",
  movilidad:"RUTA",
  territorio_normal:["registro","puerta","sala_jade"],
  transito_tecnico:[],
  posicion_valida:["puerta","registro","sala_jade"],
  rutas:[["registro","puerta"],["registro","sala_jade"]],
  gates_en_ruta:[],
  territorio_por_etapa:{
    LI:"Puerta Roja → Registro → puestos próximos; patrullas.",
    LII:"Patrullas/servicio institucional; cómodo con la idea de que la secta protege, patrulla y norma.",
    LIII:"Administración → Formaciones/Archivo por asuntos oficiales.",
    M16:"FORMACIONES / coordinación institucional en varios frentes.",
    M17:"NO_CERRADO_EN_FUENTE",
    EPILOGO:"CANÓNICO: LEALTAD_RESPONSABLE; único con reacción concreta a LIBERAR/CUSTODIAR."
  },
  anclajes_documentados:[
    "M01–M03 (LUO_01_ASI_SE_HACE)",
    "M06 (LUO_02_POR_ALGO_EXISTE)",
    "M09 (LUO_03_ZHAO_ARCHIVOS)",
    "M10 (LUO_04_GUO_SEGUNDA_RAMA)",
    "M16 (LUO_05_FORMACIONES_M16)"
  ],
  conocimiento_inicial:{
    R1:"SOSPECHA",R2:"DESCONOCIDO",R3:"DESCONOCIDO",R4:"DESCONOCIDO",R5:"SABE",
    R6:"DESCONOCIDO",R7:"DESCONOCIDO",R8:"DESCONOCIDO",R9:"DESCONOCIDO",R10:"DESCONOCIDO"
  }
};

export const LUO_YAN_POLICY_STATUS={
  utilityTraits:"EXPERIMENTAL_NON_CANONICAL",
  knowledgeR5:"CANONICAL_REQUIREMENT_CAPABILITY_GAP",
  epilogueChoice:"CANONICAL_DOMAIN_CAPABILITY_GAP"
};

export const LUO_YAN_REQUIRED_CAPABILITIES={
  knowledge:"KNOWLEDGE_SCHEMA_R1_TO_R10",
  epilogue:"LIBERAR_CUSTODIAR_DOMAIN_OUTCOME"
};
