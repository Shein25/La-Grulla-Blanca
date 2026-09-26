export const GAO_SHUN_SCENARIOS = {
  routine: {
    description: "Patrulla programada, finalización y retorno a puesto.",
    fsm: [
      {type:"PATROL_DUE",facts:{}},
      {type:"PATROL_COMPLETE",facts:{}},
      {type:"ARRIVED",facts:{}}
    ],
    bt: [
      {facts:{patrolDue:true},actionResults:{}},
      {facts:{patrolDue:true},actionResults:{patrol:"SUCCESS"}},
      {facts:{},actionResults:{}}
    ]
  },
  escalation: {
    description: "Sospecha observada, persistencia, hostilidad y fin de amenaza.",
    fsm: [
      {type:"SUSPICIOUS",facts:{}},
      {type:"PERSISTS",facts:{}},
      {type:"HOSTILE",facts:{}},
      {type:"THREAT_ENDED",facts:{}},
      {type:"ARRIVED",facts:{}}
    ],
    bt: [
      {facts:{suspicious:true},actionResults:{}},
      {facts:{suspicious:true,persistentSuspicion:true},actionResults:{observe:"SUCCESS"}},
      {facts:{hostile:true},actionResults:{warn:"RUNNING"}},
      {facts:{},actionResults:{block:"SUCCESS"}}
    ]
  },
  interruption: {
    description: "Patrulla interrumpida por amenaza hostil.",
    fsm: [
      {type:"PATROL_DUE",facts:{}},
      {type:"HOSTILE",facts:{}},
      {type:"THREAT_ENDED",facts:{}},
      {type:"ARRIVED",facts:{}}
    ],
    bt: [
      {facts:{patrolDue:true},actionResults:{}},
      {facts:{patrolDue:true,hostile:true},actionResults:{patrol:"RUNNING"}},
      {facts:{},actionResults:{block:"SUCCESS"}}
    ]
  }
};
