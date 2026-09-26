export function meiWorld(overrides={}){
  return {
    at:"puesto",playerPresent:false,playerNeedsHelp:false,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:true,dutySatisfied:false,
    dutyImportance:90,danger:60,urgency:85,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function meiContext(world,overrides={}){
  return {
    playerPresent:world.playerPresent,playerRequestsHelp:world.playerNeedsHelp&&!world.playerHelped,
    playerRank:1,dutyImportance:world.dutyImportance,danger:world.danger,missionUrgency:world.urgency,
    anomalyPresent:world.anomalyPresent&&!world.anomalyInvestigated,awayFromPost:world.at!=="puesto",
    superiorReachable:false,relevantKnowledge:"SOSPECHA",dutyMode:"trabajar",...overrides
  };
}
export const MEI_LIAN_SCENARIOS={
  m16Sauces:{
    domainFront:"SAUCES",
    description:"M16 resuelto narrativamente hacia SAUCES.",
    world:meiWorld()
  },
  m16Medicina:{
    domainFront:"MEDICINA",
    description:"M16 resuelto narrativamente hacia MEDICINA.",
    world:meiWorld()
  }
};
