export const JIANG_RUI_BT = {
  id: "jiang_rui_bt_lab",
  root: {
    id: "root",
    type: "selector",
    children: [
      {
        id:"report_seq",type:"sequence",children:[
          {id:"high_risk",type:"condition",test:{key:"highRisk",op:"EQ",value:true}},
          {id:"superior_reachable",type:"condition",test:{key:"superiorReachable",op:"EQ",value:true}},
          {id:"report",type:"action",intent:"REPORT_SUPERIOR"}
        ]
      },
      {
        id:"investigate_seq",type:"sequence",children:[
          {id:"anomaly",type:"condition",test:{key:"anomaly",op:"EQ",value:true}},
          {id:"investigate",type:"action",intent:"INVESTIGATE_ROUTE_ANOMALY"}
        ]
      },
      {
        id:"return_seq",type:"sequence",children:[
          {id:"away",type:"condition",test:{key:"awayFromPost",op:"EQ",value:true}},
          {id:"return",type:"action",intent:"RETURN_POST"}
        ]
      },
      {
        id:"patrol_seq",type:"sequence",children:[
          {id:"patrol_due",type:"condition",test:{key:"patrolDue",op:"EQ",value:true}},
          {id:"patrol",type:"action",intent:"PATROL_ROUTE"}
        ]
      },
      {id:"hold",type:"action",intent:"HOLD_POST"}
    ]
  }
};
