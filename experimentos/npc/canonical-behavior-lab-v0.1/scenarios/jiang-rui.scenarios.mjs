export const JIANG_RUI_SCENARIOS = {
  routine_patrol: {
    description: "Patrulla ordinaria de rutas.",
    fsm: [{type:"PATROL_DUE",facts:{}}],
    bt: [{facts:{patrolDue:true,anomaly:false,highRisk:false,superiorReachable:true,awayFromPost:false},actionResults:{}}],
    utility: {
      playerPresent:false,playerRequestsHelp:false,playerRank:0,
      dutyImportance:75,danger:10,missionUrgency:10,anomalyPresent:false,
      awayFromPost:false,superiorReachable:true,relevantKnowledge:"SOSPECHA",dutyMode:"patrullar"
    }
  },
  low_anomaly_no_superior: {
    description: "Anomalía leve en ruta y superior no alcanzable.",
    fsm: [{type:"ANOMALY",facts:{}}],
    bt: [{facts:{patrolDue:true,anomaly:true,highRisk:false,superiorReachable:false,awayFromPost:false},actionResults:{}}],
    utility: {
      playerPresent:false,playerRequestsHelp:false,playerRank:0,
      dutyImportance:75,danger:25,missionUrgency:35,anomalyPresent:true,
      awayFromPost:false,superiorReachable:false,relevantKnowledge:"SOSPECHA",dutyMode:"patrullar"
    }
  },
  high_anomaly_no_superior: {
    description: "Anomalía de riesgo alto sin superior alcanzable.",
    fsm: [{type:"ANOMALY",facts:{}}],
    bt: [{facts:{patrolDue:true,anomaly:true,highRisk:true,superiorReachable:false,awayFromPost:false},actionResults:{}}],
    utility: {
      playerPresent:false,playerRequestsHelp:false,playerRank:0,
      dutyImportance:75,danger:80,missionUrgency:85,anomalyPresent:true,
      awayFromPost:false,superiorReachable:false,relevantKnowledge:"SOSPECHA",dutyMode:"patrullar"
    }
  },
  low_anomaly_with_superior: {
    description: "Anomalía leve con superior alcanzable.",
    fsm: [{type:"ANOMALY",facts:{}}],
    bt: [{facts:{patrolDue:true,anomaly:true,highRisk:false,superiorReachable:true,awayFromPost:false},actionResults:{}}],
    utility: {
      playerPresent:false,playerRequestsHelp:false,playerRank:0,
      dutyImportance:75,danger:25,missionUrgency:35,anomalyPresent:true,
      awayFromPost:false,superiorReachable:true,relevantKnowledge:"SOSPECHA",dutyMode:"patrullar"
    }
  },
  away_from_post: {
    description: "Fuera del puesto sin amenaza activa.",
    fsm: [{type:"AWAY_FROM_POST",facts:{}}],
    bt: [{facts:{patrolDue:false,anomaly:false,highRisk:false,superiorReachable:true,awayFromPost:true},actionResults:{}}],
    utility: {
      playerPresent:false,playerRequestsHelp:false,playerRank:0,
      dutyImportance:85,danger:10,missionUrgency:10,anomalyPresent:false,
      awayFromPost:true,superiorReachable:true,relevantKnowledge:"SOSPECHA",dutyMode:"ninguno"
    }
  },
  m16_route_crisis: {
    description: "Crisis de rutas M16 con alto peligro y superior alcanzable.",
    fsm: [{type:"HIGH_RISK",facts:{}}],
    bt: [{facts:{patrolDue:true,anomaly:true,highRisk:true,superiorReachable:true,awayFromPost:false},actionResults:{}}],
    utility: {
      playerPresent:false,playerRequestsHelp:false,playerRank:0,
      dutyImportance:75,danger:70,missionUrgency:90,anomalyPresent:true,
      awayFromPost:false,superiorReachable:true,relevantKnowledge:"SOSPECHA",dutyMode:"patrullar"
    }
  }
};
