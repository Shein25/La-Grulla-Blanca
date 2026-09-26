export const PEI_LUO_SCENARIOS = {
  routine: {
    description: "Rutina experimental cocina -> comedor -> cocina -> preparación.",
    fsm: [
      {type:"SERVICE_DUE",facts:{}},
      {type:"ARRIVED_DINING",facts:{}},
      {type:"SERVICE_COMPLETE",facts:{}},
      {type:"ARRIVED_KITCHEN",facts:{}},
      {type:"RESET_COMPLETE",facts:{}}
    ],
    bt: [
      {facts:{serviceDue:true,atDining:false},actionResults:{}},
      {facts:{serviceDue:true,atDining:true},actionResults:{move_out:"SUCCESS"}},
      {facts:{returnKitchen:true},actionResults:{serve:"SUCCESS"}},
      {facts:{resetKitchen:true},actionResults:{return:"SUCCESS"}},
      {facts:{},actionResults:{reset:"SUCCESS"}}
    ]
  },
  crisis_interrupts_service: {
    description: "Crisis M16 interrumpe una tarea normal de servicio.",
    fsm: [
      {type:"SERVICE_DUE",facts:{}},
      {type:"ARRIVED_DINING",facts:{}},
      {type:"CRISIS",facts:{}},
      {type:"CRISIS_ENDED",facts:{}},
      {type:"ARRIVED_KITCHEN",facts:{}},
      {type:"RESET_COMPLETE",facts:{}}
    ],
    bt: [
      {facts:{serviceDue:true,atDining:false},actionResults:{}},
      {facts:{serviceDue:true,atDining:true},actionResults:{move_out:"SUCCESS"}},
      {facts:{crisis:true,serviceDue:true,atDining:true},actionResults:{serve:"RUNNING"}},
      {facts:{returnKitchen:true},actionResults:{organize_crisis:"SUCCESS"}},
      {facts:{resetKitchen:true},actionResults:{return:"SUCCESS"}},
      {facts:{},actionResults:{reset:"SUCCESS"}}
    ]
  },
  crisis_from_prep: {
    description: "Crisis aparece mientras Pei Luo está en preparación normal.",
    fsm: [
      {type:"CRISIS",facts:{}},
      {type:"CRISIS_ENDED",facts:{}},
      {type:"ARRIVED_KITCHEN",facts:{}},
      {type:"RESET_COMPLETE",facts:{}}
    ],
    bt: [
      {facts:{},actionResults:{}},
      {facts:{crisis:true},actionResults:{prepare:"RUNNING"}},
      {facts:{returnKitchen:true},actionResults:{organize_crisis:"SUCCESS"}},
      {facts:{resetKitchen:true},actionResults:{return:"SUCCESS"}},
      {facts:{},actionResults:{reset:"SUCCESS"}}
    ]
  }
};
