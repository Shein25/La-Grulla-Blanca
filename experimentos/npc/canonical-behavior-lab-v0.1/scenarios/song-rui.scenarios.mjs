export function songWorld(overrides={}){
  return {
    at:"puesto",playerPresent:false,playerNeedsHelp:false,playerHelped:false,playerReachable:true,
    anomalyPresent:false,anomalyInvestigated:false,dutyPending:true,dutySatisfied:false,
    dutyImportance:95,danger:45,urgency:75,hasEvidence:false,superiorInformed:false,
    superiorAvailable:true,messengerAvailable:true,passageOpen:true,waited:false,...overrides
  };
}
export function songContext(world,overrides={}){
  return {
    playerPresent:world.playerPresent,playerRequestsHelp:false,playerRank:1,
    dutyImportance:world.dutyImportance,danger:world.danger,missionUrgency:world.urgency,
    anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:"SABE",dutyMode:"trabajar",...overrides
  };
}
export const SONG_RUI_SCENARIOS={
  r3Dialogue:{
    description:"R3 canónico = SABE y entra en el esquema actual.",
    topicId:"R3",
    dialogueContext:{playerRank:2,topicSensitivity:40,formalRestriction:45}
  },
  m16ArchiveProtection:{
    description:"Protección documental M16 abstraída como duty genérico.",
    world:songWorld()
  }
};
