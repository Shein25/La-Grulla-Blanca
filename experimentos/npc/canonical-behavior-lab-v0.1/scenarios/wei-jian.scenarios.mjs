export const WEI_JIAN_SCENARIOS={
  training:{
    description:"Supervisión marcial ordinaria.",
    ticks:[
      {facts:{highThreat:false,suspicious:false,trainingDue:true},actionResults:{}}
    ]
  },
  suspiciousDuringTraining:{
    description:"Una anomalía interrumpe entrenamiento activo.",
    ticks:[
      {facts:{highThreat:false,suspicious:false,trainingDue:true},actionResults:{}},
      {facts:{highThreat:false,suspicious:true,trainingDue:true},actionResults:{training:"RUNNING"}}
    ]
  },
  crisisDuringTraining:{
    description:"Amenaza de seguridad M16 interrumpe inmediatamente entrenamiento activo.",
    ticks:[
      {facts:{highThreat:false,suspicious:false,trainingDue:true},actionResults:{}},
      {facts:{highThreat:true,suspicious:true,trainingDue:true},actionResults:{training:"RUNNING"}}
    ]
  },
  resumeAfterCrisis:{
    description:"Finalizada la respuesta, si el entrenamiento sigue pendiente vuelve a supervisión.",
    ticks:[
      {facts:{highThreat:false,suspicious:false,trainingDue:true},actionResults:{}},
      {facts:{highThreat:true,suspicious:false,trainingDue:true},actionResults:{training:"RUNNING"}},
      {facts:{highThreat:false,suspicious:false,trainingDue:true},actionResults:{security_response:"SUCCESS"}}
    ]
  }
};
