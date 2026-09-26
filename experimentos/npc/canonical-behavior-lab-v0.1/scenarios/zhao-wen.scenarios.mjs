export const ZHAO_WEN_DIALOGUE_SCENARIOS={
  ordinary:{
    description:"Consulta sobre un tema que Zhao Wen no conoce inicialmente.",
    topicId:"R1",
    context:{playerRank:1,topicSensitivity:20,formalRestriction:20}
  },
  maxTrustStillUnknown:{
    description:"Mismo tema DESCONOCIDO bajo relación/rango máximos; debe seguir sin revelar.",
    topicId:"R1",
    context:{playerRank:6,topicSensitivity:0,formalRestriction:0}
  },
  m09RestrictedArchive:{
    description:"M09 requiere permiso ARCHIVO_RESTRINGIDO concedido por Qiao Ren.",
    requiredCapability:"ARCHIVO_RESTRINGIDO_PERMISSION"
  }
};
