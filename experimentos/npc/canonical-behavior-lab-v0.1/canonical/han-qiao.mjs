export const HAN_QIAO_CANON = {
  source:{file:"grulla-blanca_ver74.html",blob:"d34f7ea3f9de9344130aa072fac34d14a7a474d6",object:"NPC_DEF.han_qiao"},
  id:"han_qiao",
  nombre:"Han Qiao",
  categoria:"companero",
  rol:"Aspirante — recursos/contactos, logística",
  sala_inicial:"oficina_servicios",
  sala_inicial_clasificacion:"ELECCION_TECNICA_3C5",
  movilidad:"RUTA",
  territorio_normal:["oficina_servicios","patio_servicios","deposito_comun"],
  transito_tecnico:[],
  posicion_valida:["deposito_comun","oficina_servicios","patio_servicios"],
  rutas:[
    ["oficina_servicios","patio_servicios"],
    ["oficina_servicios","deposito_comun"]
  ],
  gates_en_ruta:[],
  territorio_por_etapa:{
    LI:"Patio, Registro, Marcial; comedor, servicios, almacén. Existe ambigüedad de área documentada.",
    LII:"Patio → Producción/almacenes → Puerta Roja → ocasionalmente Sauces.",
    LIII:"Administración → Archivo público → Recinto Interior limitado; permisos, contactos externos.",
    M16:"ANCLADO Recursos/Logística; responsable/apoyo del frente RECURSOS; puede asumir logística aunque no sea el responsable formal.",
    M17:"NO_CERRADO_EN_FUENTE",
    EPILOGO:"CANÓNICO: Estado final HERENCIA_APROPIADA."
  },
  anclajes_documentados:[
    "M01–M03 (HAN_01_TODO_PREPARADO)",
    "M05–M08 (HAN_02_PROCEDIMIENTO, HAN_03_EL_NOMBRE_FAMILIAR)",
    "M16 (HAN_05_RECURSOS_M16, autónoma)"
  ],
  conocimiento_inicial:{R1:"DESCONOCIDO",R2:"DESCONOCIDO",R3:"DESCONOCIDO",R4:"DESCONOCIDO",R5:"DESCONOCIDO",R6:"DESCONOCIDO",R7:"DESCONOCIDO",R8:"DESCONOCIDO",R9:"DESCONOCIDO",R10:"DESCONOCIDO"}
};

export const HAN_QIAO_POLICY_STATUS={
  utilityTraits:"EXPERIMENTAL_NON_CANONICAL",
  ordinaryHelp:"EXPERIMENTAL_MECHANICS_TEST",
  m16Logistics:"CANON_SUPPORTED_M16_POLICY_HYPOTHESIS",
  materialLogistics:"CANONICAL_DOMAIN_CAPABILITY_GAP"
};

export const HAN_QIAO_REQUIRED_MATERIAL_CAPABILITY="RESOURCE_ALLOCATION_AND_LOGISTICS";
