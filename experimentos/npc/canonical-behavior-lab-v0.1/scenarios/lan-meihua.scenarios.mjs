export function lanWorld(overrides={}){
  return {
    at:"puesto",playerPresent:false,playerNeedsHelp:false,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:true,dutySatisfied:false,
    dutyImportance:100,danger:70,urgency:95,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function lanContext(world,overrides={}){
  return {
    playerPresent:false,playerRequestsHelp:false,playerRank:1,dutyImportance:world.dutyImportance,
    danger:world.danger,missionUrgency:world.urgency,anomalyPresent:false,awayFromPost:false,
    superiorReachable:false,relevantKnowledge:"SOSPECHA",dutyMode:"trabajar",...overrides
  };
}
export const LAN_MEIHUA_SCENARIOS={
  m16Medicine:{
    description:"Frente MEDICINA M16 abstraído como deber genérico.",
    world:lanWorld()
  }
};
