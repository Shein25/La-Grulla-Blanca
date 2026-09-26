export const PEI_LUO_BT = {
  id: "pei_luo_bt_lab",
  root: {
    id: "root",
    type: "selector",
    children: [
      {
        id: "crisis_seq", type: "sequence", children: [
          {id:"crisis",type:"condition",test:{key:"crisis",op:"EQ",value:true}},
          {id:"organize_crisis",type:"action",intent:"ORGANIZE_CRISIS_RATIONS"}
        ]
      },
      {
        id: "serve_seq", type: "sequence", children: [
          {id:"at_dining",type:"condition",test:{key:"atDining",op:"EQ",value:true}},
          {id:"service_due",type:"condition",test:{key:"serviceDue",op:"EQ",value:true}},
          {id:"serve",type:"action",intent:"SERVE_RATIONS"}
        ]
      },
      {
        id: "move_out_seq", type: "sequence", children: [
          {id:"needs_move_out",type:"condition",test:{key:"serviceDue",op:"EQ",value:true}},
          {id:"move_out",type:"action",intent:"MOVE_TO_DINING"}
        ]
      },
      {
        id: "return_seq", type: "sequence", children: [
          {id:"needs_return",type:"condition",test:{key:"returnKitchen",op:"EQ",value:true}},
          {id:"return",type:"action",intent:"RETURN_KITCHEN"}
        ]
      },
      {
        id: "reset_seq", type: "sequence", children: [
          {id:"needs_reset",type:"condition",test:{key:"resetKitchen",op:"EQ",value:true}},
          {id:"reset",type:"action",intent:"RESET_KITCHEN"}
        ]
      },
      {id:"prepare",type:"action",intent:"PREPARE_RATIONS"}
    ]
  }
};
