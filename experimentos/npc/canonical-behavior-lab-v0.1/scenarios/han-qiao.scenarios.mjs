export function hanWorld(overrides={}){
  return {
    at:"puesto",playerPresent:true,playerNeedsHelp:true,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:false,dutySatisfied:false,
    dutyImportance:20,danger:10,urgency:60,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function hanContext(world,overrides={}){
  return {
    playerPresent:world.playerPresent,
    playerRequestsHelp:world.playerNeedsHelp&&!world.playerHelped,
    playerRank:1,dutyImportance:world.dutyImportance,danger:world.danger,
    missionUrgency:world.urgency,anomalyPresent:world.anomalyPresent&&!world.anomalyInvestigated,
    awayFromPost:world.at!=="puesto",superiorReachable:true,relevantKnowledge:"DESCONOCIDO",
    dutyMode:"ninguno",...overrides
  };
}
export const HAN_QIAO_SCENARIOS={
  ordinaryHelp:{
    description:"Solicitud ordinaria del jugador con deber material bajo.",
    world:hanWorld(),
    contextOverrides:{dutyMode:"ninguno",superiorReachable:false}
  },
  m16Resources:{
    description:"Frente RECURSOS de M16 con deber logístico alto y solicitud simultánea del jugador.",
    world:hanWorld({dutyPending:true,dutyImportance:95,danger:55,urgency:80}),
    contextOverrides:{dutyMode:"trabajar",superiorReachable:false}
  }
};
