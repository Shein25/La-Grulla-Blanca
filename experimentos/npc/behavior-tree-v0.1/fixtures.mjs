export const GUARD_TREE={id:'fixture_bt_guard',root:{id:'root',type:'selector',children:[
 {id:'hostile_seq',type:'sequence',children:[{id:'is_hostile',type:'condition',test:{key:'hostile',op:'EQ',value:true}},{id:'engage',type:'action',intent:'ENGAGE'}]},
 {id:'suspicious_seq',type:'sequence',children:[{id:'is_suspicious',type:'condition',test:{key:'suspicious',op:'EQ',value:true}},{id:'warn',type:'action',intent:'WARN_TARGET'}]},
 {id:'patrol',type:'action',intent:'PATROL'}
]}};

export const WORKER_TREE={id:'fixture_bt_worker',root:{id:'root',type:'selector',children:[
 {id:'alarm_seq',type:'sequence',children:[{id:'alarm',type:'condition',test:{key:'alarm',op:'EQ',value:true}},{id:'secure',type:'action',intent:'SECURE_SUPPLIES'}]},
 {id:'service_seq',type:'sequence',children:[{id:'service_due',type:'condition',test:{key:'phase',op:'EQ',value:'SERVICE'}},{id:'serve',type:'action',intent:'SERVE'}]},
 {id:'prep',type:'action',intent:'PREPARE'}
]}};

export const SUPERVISOR_TREE={id:'fixture_bt_supervisor',root:{id:'root',type:'selector',children:[
 {id:'crisis_seq',type:'sequence',children:[{id:'crisis',type:'condition',test:{key:'crisis',op:'EQ',value:true}},{id:'coordinate',type:'action',intent:'COORDINATE_RESPONSE'}]},
 {id:'request_seq',type:'sequence',children:[{id:'request',type:'condition',test:{key:'playerRequest',op:'EQ',value:true}},{id:'assist',type:'action',intent:'ASSIST_PLAYER'}]},
 {id:'inspect',type:'action',intent:'INSPECT_DUTY'}
]}};
