export function duanWorld(overrides={}){
  return {
    at:"puesto",playerPresent:false,playerNeedsHelp:false,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:true,dutySatisfied:false,
    dutyImportance:100,danger:50,urgency:90,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function duanContext(world){
  return {
    playerPresent:false,playerRequestsHelp:false,playerRank:1,dutyImportance:world.dutyImportance,
    danger:world.danger,missionUrgency:world.urgency,anomalyPresent:false,awayFromPost:false,
    superiorReachable:false,relevantKnowledge:"SOSPECHA",dutyMode:"trabajar"
  };
}
export const DUAN_SHIBO_SCENARIOS={m16Resources:{world:duanWorld(),description:"M16 Recursos/Producción."}};
