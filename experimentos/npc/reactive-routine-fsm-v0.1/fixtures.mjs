export const GUARD_MACHINE = {
  id:'fixture_guard', initialState:'POST', states:{
    POST:{on:{
      TICK:[{priority:10,target:'PATROL',guard:{source:'event',key:'patrolDue',op:'EQ',value:true},emit:['START_PATROL']}],
      SUSPICIOUS:[{priority:10,target:'ALERT',emit:['OBSERVE']}],
      HOSTILE:[{priority:10,target:'COMBAT',emit:['BLOCK_PASSAGE']}],
    }},
    PATROL:{on:{
      SUSPICIOUS:[{priority:10,target:'ALERT',emit:['OBSERVE']}],
      HOSTILE:[{priority:10,target:'COMBAT',emit:['BLOCK_PASSAGE']}],
      PATROL_COMPLETE:[{priority:10,target:'RETURN',emit:['RETURN_POST']}],
    }},
    ALERT:{on:{
      CLEARED:[{priority:10,target:'RETURN',emit:['RETURN_POST']}],
      PERSISTS:[{priority:10,target:'WARN',emit:['WARN_TARGET']}],
      HOSTILE:[{priority:20,target:'COMBAT',emit:['BLOCK_PASSAGE']}],
    }},
    WARN:{on:{
      COMPLIES:[{priority:10,target:'RETURN',emit:['RETURN_POST']}],
      HOSTILE:[{priority:20,target:'COMBAT',emit:['BLOCK_PASSAGE']}],
      CLEARED:[{priority:10,target:'RETURN',emit:['RETURN_POST']}],
    }},
    COMBAT:{on:{THREAT_ENDED:[{priority:10,target:'RETURN',emit:['RETURN_POST']}]}},
    RETURN:{on:{ARRIVED:[{priority:10,target:'POST',emit:['RESUME_DUTY']}]}},
  }
};

export const WORKER_MACHINE = {
  id:'fixture_worker', initialState:'PREP', states:{
    PREP:{on:{
      TICK:[{priority:10,target:'SERVE',guard:{source:'event',key:'phase',op:'EQ',value:'SERVICE'},emit:['BEGIN_SERVICE']}],
      ALARM:[{priority:50,target:'EMERGENCY',emit:['SECURE_SUPPLIES']}],
    }},
    SERVE:{on:{
      TICK:[{priority:10,target:'PREP',guard:{source:'event',key:'phase',op:'EQ',value:'PREP'},emit:['BEGIN_PREP']}],
      TASK_COMPLETE:[{priority:10,target:'CLEAN',emit:['CLEAN_WORKSPACE']}],
      ALARM:[{priority:50,target:'EMERGENCY',emit:['SECURE_SUPPLIES']}],
    }},
    CLEAN:{on:{
      TASK_COMPLETE:[{priority:10,target:'PREP',emit:['BEGIN_PREP']}],
      ALARM:[{priority:50,target:'EMERGENCY',emit:['SECURE_SUPPLIES']}],
    }},
    EMERGENCY:{on:{CLEAR:[{priority:10,target:'RETURN',emit:['RETURN_WORKSTATION']}]}},
    RETURN:{on:{ARRIVED:[{priority:10,target:'PREP',emit:['BEGIN_PREP']}]}},
  }
};

export const PATROLLER_MACHINE = {
  id:'fixture_patroller', initialState:'POST', states:{
    POST:{on:{TICK:[{priority:10,target:'PATROL',guard:{source:'event',key:'patrolDue',op:'EQ',value:true},emit:['START_PATROL']}]}},
    PATROL:{on:{
      SUSPICIOUS:[{priority:10,target:'ALERT',emit:['INVESTIGATE']}],
      HOSTILE:[{priority:20,target:'COMBAT',emit:['ENGAGE']}],
      PATROL_COMPLETE:[{priority:10,target:'RETURN',emit:['RETURN_POST']}],
    }},
    ALERT:{on:{
      CLEARED:[{priority:10,target:'RETURN',emit:['RETURN_POST']}],
      HOSTILE:[{priority:20,target:'COMBAT',emit:['ENGAGE']}],
    }},
    COMBAT:{on:{THREAT_ENDED:[{priority:10,target:'RETURN',emit:['RETURN_POST']}]}},
    RETURN:{on:{ARRIVED:[{priority:10,target:'POST',emit:['RESUME_PATROL_CYCLE']}]}},
  }
};
