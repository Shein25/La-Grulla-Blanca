export function heWorld(overrides={}){
  return {
    at:"puesto",playerPresent:false,playerNeedsHelp:false,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:true,dutySatisfied:false,
    dutyImportance:100,danger:75,urgency:95,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function heContext(world){
  return {
    playerPresent:false,playerRequestsHelp:false,playerRank:1,dutyImportance:world.dutyImportance,
    danger:world.danger,missionUrgency:world.urgency,anomalyPresent:false,awayFromPost:false,
    superiorReachable:false,relevantKnowledge:"SABE",dutyMode:"trabajar"
  };
}
export const HE_ZHEN_SCENARIOS={m16Formations:{world:heWorld(),description:"M16 Nodo Central / Formaciones."}};
