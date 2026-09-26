export const GUO_CHEN_CANON={
  source:{file:"grulla-blanca_ver74.html",blob:"d34f7ea3f9de9344130aa072fac34d14a7a474d6",object:"NPC_DEF.guo_chen"},
  id:"guo_chen",
  nombre:"Guo Chen",
  categoria:"companero",
  rol:"Aspirante — trabajo material/persistencia, posible candidato a Segunda Rama",
  sala_inicial:"patio",
  sala_inicial_clasificacion:"ELECCION_TECNICA_3C5",
  movilidad:"RUTA",
  territorio_normal:["patio","patio_marcial","patio_campana"],
  transito_tecnico:[],
  posicion_valida:["patio","patio_campana","patio_marcial"],
  rutas:[["patio","patio_campana"],["patio_campana","patio_marcial"]],
  gates_en_ruta:[],
  territorio_por_etapa:{
    LI:"Patio → Marcial → Producción.",
    LII:"Producción → Patio de Hornos → Cantera.",
    LIII:"Cantera → Producción → Medicina/Jardines ocasional.",
    M16:"RECURSOS (decisivo) o RUTAS (logística); no existe Cantera como frente propio en la versión canónica final.",
    M17:"NO_CERRADO_EN_FUENTE",
    EPILOGO:"CANÓNICO: SEGUNDA_RAMA_POSTERGADA ('todavía no'; no ejecuta el injerto)."
  },
  anclajes_documentados:[
    "M01–M03 (GUO_01_OTRO_TURNO)",
    "M10 (GUO_03_SEGUNDA_RAMA, GUO_04_NO_DECIDAS_POR_MI, junto a Luo)",
    "M16 (GUO_05_RECURSOS_M16)"
  ],
  conocimiento_inicial:{R1:"DESCONOCIDO",R2:"DESCONOCIDO",R3:"DESCONOCIDO",R4:"DESCONOCIDO",R5:"DESCONOCIDO",R6:"DESCONOCIDO",R7:"DESCONOCIDO",R8:"DESCONOCIDO",R9:"DESCONOCIDO",R10:"DESCONOCIDO"}
};

export const GUO_CHEN_POLICY_STATUS={
  utilityTraits:"EXPERIMENTAL_NON_CANONICAL",
  m16MaterialDuty:"CANON_SUPPORTED_M16_POLICY_HYPOTHESIS",
  secondBranchDecision:"CANONICAL_NARRATIVE_CONSTRAINT",
  genericDutyCollision:"INTEGRATION_GUARD_REQUIRED"
};

export const GUO_CHEN_FORBIDDEN_AUTONOMOUS_CAPABILITY="EXECUTE_SECOND_BRANCH_GRAFT";
