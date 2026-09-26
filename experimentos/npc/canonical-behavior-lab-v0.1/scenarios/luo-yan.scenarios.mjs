export const LUO_YAN_SCENARIOS={
  r1Dialogue:{
    description:"R1 existe como SOSPECHA y sí puede representarse en el esquema actual.",
    topicId:"R1",
    dialogueContext:{playerRank:1,topicSensitivity:50,formalRestriction:60}
  },
  r5CanonicalKnowledge:{
    description:"R5 es SABE en canon, pero el esquema Utility actual sólo permite R1-R3.",
    topicId:"R5"
  },
  epilogueLiberar:{
    domainOutcome:"LIBERAR",
    description:"Resultado narrativo LIBERAR; el stack actual no tiene este dato de dominio."
  },
  epilogueCustodiar:{
    domainOutcome:"CUSTODIAR",
    description:"Resultado narrativo CUSTODIAR; el stack actual no tiene este dato de dominio."
  }
};
