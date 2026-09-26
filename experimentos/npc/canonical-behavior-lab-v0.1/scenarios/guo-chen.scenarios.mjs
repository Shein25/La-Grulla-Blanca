export function guoWorld(overrides={}){
  return {
    at:"puesto",playerPresent:false,playerNeedsHelp:false,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:true,dutySatisfied:false,
    dutyImportance:90,danger:45,urgency:70,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function guoContext(world,overrides={}){
  return {
    playerPresent:world.playerPresent,playerRequestsHelp:world.playerNeedsHelp&&!world.playerHelped,
    playerRank:1,dutyImportance:world.dutyImportance,danger:world.danger,missionUrgency:world.urgency,
    anomalyPresent:world.anomalyPresent&&!world.anomalyInvestigated,awayFromPost:world.at!=="puesto",
    superiorReachable:false,relevantKnowledge:"DESCONOCIDO",dutyMode:"trabajar",...overrides
  };
}
export const GUO_CHEN_SCENARIOS={
  m16MaterialWork:{
    semanticDuty:"M16_RESOURCE_WORK",
    description:"Trabajo material legítimo durante M16.",
    world:guoWorld({dutyImportance:95,danger:55,urgency:80})
  },
  adversarialSecondBranchEncodedAsGenericDuty:{
    semanticDuty:"SECOND_BRANCH_GRAFT_DECISION",
    description:"Prueba adversarial: demuestra por qué una decisión irreversible no puede codificarse como duty genérico.",
    world:guoWorld({dutyImportance:100,danger:20,urgency:70})
  }
};
