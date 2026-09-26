export const GAO_SHUN_CANON = {
  source: {
    file: "grulla-blanca_ver74.html",
    blob: "d34f7ea3f9de9344130aa072fac34d14a7a474d6",
    object: "NPC_DEF.gao_shun"
  },
  id: "gao_shun",
  nombre: "Gao Shun",
  categoria: "funcional",
  rol: "Guardia de la Puerta Roja",
  sala_inicial: "casa_guardia",
  sala_inicial_clasificacion: "CANÓNICO",
  movilidad: "RUTA",
  territorio_normal: [
    "casa_guardia",
    "deposito_comun",
    "puerta",
    "registro"
  ],
  transito_tecnico: [
    "tablon_encargos",
    "patio_servicios",
    "patio",
    "sala_jade"
  ],
  posicion_valida: [
    "casa_guardia",
    "deposito_comun",
    "patio",
    "patio_servicios",
    "puerta",
    "registro",
    "sala_jade",
    "tablon_encargos"
  ],
  rutas: [[
    "casa_guardia",
    "deposito_comun",
    "tablon_encargos",
    "patio_servicios",
    "patio",
    "sala_jade",
    "registro",
    "puerta"
  ]],
  gates_en_ruta: [],
  anclajes_documentados: [
    "M01 (según escena, junto a Tao Ming)",
    "M04 (ANCLADO en puerta_roja/puerta)"
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

export const GAO_SHUN_POLICY_STATUS = "EXPERIMENTAL_NON_CANONICAL";

export const GAO_SHUN_ALLOWED_INTENTS = [
  "HOLD_POST",
  "PATROL_ROUTE",
  "OBSERVE_TARGET",
  "WARN_TARGET",
  "BLOCK_PASSAGE",
  "RETURN_POST"
];
