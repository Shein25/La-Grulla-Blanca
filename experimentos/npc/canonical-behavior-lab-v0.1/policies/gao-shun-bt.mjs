export const GAO_SHUN_BT = {
  id: "gao_shun_bt_lab",
  root: {
    id: "root",
    type: "selector",
    children: [
      {
        id: "hostile_seq", type: "sequence", children: [
          {id:"hostile",type:"condition",test:{key:"hostile",op:"EQ",value:true}},
          {id:"block",type:"action",intent:"BLOCK_PASSAGE"}
        ]
      },
      {
        id: "warn_seq", type: "sequence", children: [
          {id:"persistent",type:"condition",test:{key:"persistentSuspicion",op:"EQ",value:true}},
          {id:"warn",type:"action",intent:"WARN_TARGET"}
        ]
      },
      {
        id: "observe_seq", type: "sequence", children: [
          {id:"suspicious",type:"condition",test:{key:"suspicious",op:"EQ",value:true}},
          {id:"observe",type:"action",intent:"OBSERVE_TARGET"}
        ]
      },
      {
        id: "patrol_seq", type: "sequence", children: [
          {id:"patrol_due",type:"condition",test:{key:"patrolDue",op:"EQ",value:true}},
          {id:"patrol",type:"action",intent:"PATROL_ROUTE"}
        ]
      },
      {id:"hold",type:"action",intent:"HOLD_POST"}
    ]
  }
};
