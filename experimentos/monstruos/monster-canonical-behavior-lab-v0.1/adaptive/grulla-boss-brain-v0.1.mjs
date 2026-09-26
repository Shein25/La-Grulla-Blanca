export const GRULLA_BRAIN_STATUS='EXPERIMENTAL_NON_CANONICAL_GRULLA_BRAIN_V01';

export const GRULLA_PHASES=Object.freeze({
  VOTO_INMOVIL:1,
  ALAS_RECUERDAN:2,
  CAMPANA_SIN_DUENO:3
});

export const GRULLA_ABILITIES=Object.freeze({
  GOLPE_ALA:'grulla__golpe_ala',
  CAMPANADA_PICO:'grulla__campanada_pico',
  PATA_INMOVIL:'grulla__pata_inmovil',
  TORMENTA_MIL_PLUMAS:'grulla__tormenta_mil_plumas',
  CERRAR_ALAS:'grulla__cerrar_alas',
  RECORDAR_FILO:'grulla__recordar_filo',
  ECO_MERIDIANO:'grulla__eco_meridiano',
  PICOTAZO_BLANCO:'grulla__picotazo_blanco',
  CAMPANA_SIN_DUENO:'grulla__campana_sin_dueno',
  ALA_VACIA:'grulla__ala_vacia',
  SILENCIO_ENTRE_CAMPANAS:'grulla__silencio_entre_campanas',
  ROMPER_RITMO:'grulla__romper_ritmo',
  BUSCAR_PULSO:'grulla__buscar_pulso'
});

export const GRULLA_COUNTER_RESPONSES=Object.freeze({
  ofensiva:Object.freeze({
    id:'TRAZO_VACIO',
    label:'Trazo Vacío',
    telegraph:'La Grulla deja de seguir el golpe: ya conoce exactamente dónde termina.',
    primarySuppression:'DAMAGE_AND_SECONDARY'
  }),
  esquiva:Object.freeze({
    id:'PULSO_FIJADO',
    label:'Pulso Fijado',
    telegraph:'La mirada abandona tu silueta y escucha el pulso que mueve tus pasos.',
    primarySuppression:'EVASION'
  }),
  guardia:Object.freeze({
    id:'RESONANCIA_INTERNA',
    label:'Resonancia Interior',
    telegraph:'La campana cambia de tono hasta resonar dentro de la misma guardia.',
    primarySuppression:'GUARD'
  }),
  fortificacion:Object.freeze({
    id:'CAMPANA_INVERSA',
    label:'Campana Inversa',
    telegraph:'El eco encuentra las mismas juntas cada vez que endureces la postura.',
    primarySuppression:'DEFENSE_BUFF'
  }),
  control:Object.freeze({
    id:'ANCLA_DEL_VOTO',
    label:'Ancla del Voto',
    telegraph:'La pata inmóvil fija el vínculo. El mismo lazo ya no encuentra dónde cerrar.',
    primarySuppression:'CONTROL'
  }),
  desconocida:Object.freeze({
    id:'PATRON_COMPRENDIDO',
    label:'Patrón Comprendido',
    telegraph:'La Grulla reconoce la circulación exacta de esa técnica.',
    primarySuppression:'FULL_EFFECT'
  })
});

const A=GRULLA_ABILITIES;
const PHASE1_CYCLE=Object.freeze([A.GOLPE_ALA,A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL]);
const TELEGRAPH=Object.freeze({
  [A.GOLPE_ALA]:'Un ala blanca se tensa para golpear.',
  [A.CAMPANADA_PICO]:'Las campanas del ancla vibran al unísono.',
  [A.PATA_INMOVIL]:'La Grulla hunde una pata y cierra su postura.',
  [A.TORMENTA_MIL_PLUMAS]:'Las plumas recuerdan una tormenta que ya ocurrió.',
  [A.CERRAR_ALAS]:'Las alas se cierran sobre el vínculo.',
  [A.RECORDAR_FILO]:'La mirada repasa exactamente cómo has atacado.',
  [A.ECO_MERIDIANO]:'La campana responde al pulso de tu qi.',
  [A.PICOTAZO_BLANCO]:'El pico encuentra una línea directa.',
  [A.CAMPANA_SIN_DUENO]:'El silencio se hunde antes de una campanada sin dueño.',
  [A.ALA_VACIA]:'El contorno de un ala deja de ocupar el mismo lugar.',
  [A.SILENCIO_ENTRE_CAMPANAS]:'La Grulla deja un hueco deliberado en el ritmo.',
  [A.ROMPER_RITMO]:'El hueco se cierra sobre el patrón que repetiste.',
  [A.BUSCAR_PULSO]:'La cabeza se inclina, escuchando tu circulación.'
});

const VALID_ACTION_TYPES=new Set(['BASIC','TECHNIQUE','CONTROL','DEFEND','RECOVER','UTILITY']);
const VALID_TECHNIQUE_ROLES=new Set(['ofensiva','guardia','fortificacion','esquiva','control']);
const MAX_HISTORY=8;

function plain(x,label){
  if(!x||typeof x!=='object'||Array.isArray(x))throw new TypeError(label+' debe ser objeto');
}
function phaseOk(phase){
  if(![1,2,3].includes(phase))throw new RangeError('phase debe ser 1..3');
}
function freezeState(s){
  return Object.freeze({
    ...s,
    history:Object.freeze(s.history.map(x=>Object.freeze({...x}))),
    recentIntents:Object.freeze([...s.recentIntents]),
    phaseMemory:Object.freeze({...s.phaseMemory}),
    plan:s.plan?Object.freeze({...s.plan}):null,
    techniqueCounter:s.techniqueCounter?Object.freeze({...s.techniqueCounter}):null
  });
}
function actionCopy(a){
  plain(a,'playerAction');
  if(!VALID_ACTION_TYPES.has(a.type))throw new TypeError('playerAction.type inválido: '+a.type);
  if(a.techniqueId!==undefined&&typeof a.techniqueId!=='string')throw new TypeError('techniqueId inválido');
  if(a.techniqueRole!==undefined&&a.techniqueRole!==null&&!VALID_TECHNIQUE_ROLES.has(a.techniqueRole)){
    throw new TypeError('techniqueRole inválido: '+a.techniqueRole);
  }
  if(a.element!==undefined&&typeof a.element!=='string')throw new TypeError('element inválido');
  if(a.qiSpent!==undefined&&(!Number.isFinite(a.qiSpent)||a.qiSpent<0))throw new TypeError('qiSpent inválido');
  if(a.damageBand!==undefined&&!['NONE','LOW','NORMAL','HEAVY'].includes(a.damageBand))throw new TypeError('damageBand inválido');
  return Object.freeze({
    type:a.type,
    techniqueId:a.techniqueId??null,
    techniqueRole:a.techniqueRole??(a.type==='CONTROL'?'control':null),
    element:a.element??null,
    qiSpent:Number(a.qiSpent||0),
    damageBand:a.damageBand??'NONE'
  });
}
function tail(a,n){return a.slice(Math.max(0,a.length-n));}
function same(values){return values.length>1&&values[0]!=null&&values.every(v=>v===values[0]);}
function recent(state,id,depth=1){return state.recentIntents.slice(-depth).includes(id);}

export function initialGrullaBrainState({phase=1,phaseMemory={}}={}){
  phaseOk(phase);plain(phaseMemory,'phaseMemory');
  return freezeState({phase,turn:0,history:[],recentIntents:[],phaseMemory:{...phaseMemory},plan:null,techniqueCounter:null});
}

function summarize(history){
  const t=new Map(),e=new Map();
  let offense=0,defend=0,recover=0,control=0,qiActions=0,techniqueUses=0,nonTechniqueActions=0,basicUses=0;
  for(const a of history){
    if(['BASIC','TECHNIQUE','CONTROL'].includes(a.type))offense++;
    if(a.type==='BASIC')basicUses++;
    if(a.type==='DEFEND')defend++;
    if(a.type==='RECOVER')recover++;
    if(a.type==='CONTROL')control++;
    if(a.qiSpent>0)qiActions++;
    if(a.techniqueId){techniqueUses++;t.set(a.techniqueId,(t.get(a.techniqueId)||0)+1);}
    else nonTechniqueActions++;
    if(a.element)e.set(a.element,(e.get(a.element)||0)+1);
  }
  const dominant=map=>[...map.entries()].sort((x,y)=>y[1]-x[1]||x[0].localeCompare(y[0]))[0]?.[0]||null;
  const dominantTechnique=dominant(t);
  const dominantTechniqueRole=history.findLast?.(a=>a.techniqueId===dominantTechnique)?.techniqueRole
    ?? [...history].reverse().find(a=>a.techniqueId===dominantTechnique)?.techniqueRole
    ?? null;
  const singleSkillReliance=techniqueUses>=3&&t.size===1&&basicUses===0;
  return {
    dominantTechnique,dominantTechniqueRole,dominantElement:dominant(e),
    offense,defend,recover,control,qiActions,
    techniqueUses,uniqueTechniques:t.size,nonTechniqueActions,basicUses,
    singleSkillReliance,
    pureSingleSkillSpam:singleSkillReliance&&nonTechniqueActions===0
  };
}

export function enterGrullaPhase(state,phase){
  plain(state,'state');phaseOk(phase);
  const memory={...state.phaseMemory};
  if(state.phase===1)memory.phase1=summarize(state.history);
  if(state.phase===2)memory.phase2=summarize(state.history);

  let techniqueCounter=state.techniqueCounter?{...state.techniqueCounter}:null;
  if(phase===2&&memory.phase1?.singleSkillReliance){
    techniqueCounter={
      techniqueId:memory.phase1.dominantTechnique,
      techniqueRole:memory.phase1.dominantTechniqueRole??null,
      locked:true,
      source:'PHASE1_SINGLE_SKILL_RELIANCE'
    };
  }

  return freezeState({phase,turn:0,history:[],recentIntents:[],phaseMemory:memory,plan:null,techniqueCounter});
}

function signals(state,context){
  const h=tail(state.history,state.phase===3?4:3);
  const l2=tail(h,2),l3=tail(h,3);
  return {
    techniqueRepeat:same(l2.map(x=>x.techniqueId)),
    elementRepeat:same(l2.map(x=>x.element)),
    offenseStreak:l2.length===2&&l2.every(x=>['BASIC','TECHNIQUE','CONTROL'].includes(x.type)),
    qiStreak:l2.length===2&&l2.every(x=>x.qiSpent>0),
    controlRecent:l3.some(x=>x.type==='CONTROL'),
    recoverRecent:l2.some(x=>x.type==='RECOVER'),
    heavyRecent:l2.some(x=>x.damageBand==='HEAVY'),
    playerLowHp:context.playerHpRatio!==undefined&&context.playerHpRatio<=.30,
    selfLowHp:context.selfHpRatio!==undefined&&context.selfHpRatio<=.30,
    playerQiLow:context.playerQiRatio!==undefined&&context.playerQiRatio<=.25,
    playerQiHigh:context.playerQiRatio!==undefined&&context.playerQiRatio>=.65,
    last:h.at(-1)||null
  };
}
function choose(entries,rng){
  const next=typeof rng==='function'?rng:()=>.5;
  return entries
    .map(e=>({...e,score:e.score+(Number(next())-.5)*e.jitter}))
    .sort((x,y)=>y.score-x.score||x.id.localeCompare(y.id))[0];
}
function intent(id,brain,extra={}){
  return Object.freeze({id,telegraph:TELEGRAPH[id],brain,...extra});
}
function remember(state,id,extra={}){
  return freezeState({...state,turn:state.turn+1,recentIntents:[...state.recentIntents,id].slice(-4),...extra});
}

export function chooseGrullaIntent({state,context={},rng=()=>.5}){
  plain(state,'state');plain(context,'context');phaseOk(state.phase);
  const s=signals(state,context);

  if(state.phase===1){
    const id=PHASE1_CYCLE[state.turn%PHASE1_CYCLE.length];
    return {intent:intent(id,'PROGRAMADA',{reason:'CICLO_INMOVIL'}),state:remember(state,id)};
  }

  if(state.phase===3&&state.plan?.armed&&state.plan.followup){
    const id=state.plan.followup;
    return {intent:intent(id,'MAESTRA',{reason:'PLAN_COMPROMETIDO',planId:state.plan.id,committed:true}),state:remember(state,id)};
  }

  if(state.phase===2){
    const inherited=state.phaseMemory?.phase1||{};
    const inheritedRepeat=(inherited.dominantTechnique&&s.last?.techniqueId===inherited.dominantTechnique)?1:0;
    const entries=[
      {id:A.GOLPE_ALA,score:30,jitter:1},
      {id:A.TORMENTA_MIL_PLUMAS,score:28+(s.playerQiHigh?12:0)+(s.playerLowHp?10:0)-(recent(state,A.TORMENTA_MIL_PLUMAS,2)?40:0),jitter:1},
      {id:A.CERRAR_ALAS,score:18+(s.offenseStreak?18:0)+(s.heavyRecent?20:0)+(s.selfLowHp?16:0)-(recent(state,A.CERRAR_ALAS,2)?35:0),jitter:.8},
      {id:A.RECORDAR_FILO,score:12+(s.techniqueRepeat?38:0)+(s.elementRepeat?18:0)+inheritedRepeat*8-(recent(state,A.RECORDAR_FILO,2)?42:0),jitter:.6},
      {id:A.ECO_MERIDIANO,score:12+(s.qiStreak?34:0)+(s.playerQiLow?8:0)+(s.recoverRecent?6:0)-(recent(state,A.ECO_MERIDIANO,2)?40:0),jitter:.6}
    ];
    if(s.controlRecent)entries.find(x=>x.id===A.CERRAR_ALAS).score+=8;
    const c=choose(entries,rng);
    return {intent:intent(c.id,'ADAPTATIVA',{reason:'UTILITY_MEMORY'}),state:remember(state,c.id)};
  }

  const entries=[
    {id:A.PICOTAZO_BLANCO,score:25+(s.playerLowHp?8:0),jitter:.5},
    {id:A.CAMPANA_SIN_DUENO,score:24+(s.playerLowHp?24:0)+(s.playerQiHigh?8:0)-(recent(state,A.CAMPANA_SIN_DUENO,2)?45:0),jitter:.5},
    {id:A.ALA_VACIA,score:16+(s.offenseStreak?17:0)+(s.heavyRecent?14:0)-(recent(state,A.ALA_VACIA,2)?30:0),jitter:.4},
    {id:A.PATA_INMOVIL,score:15+(s.selfLowHp?15:0)+(s.controlRecent?10:0)-(recent(state,A.PATA_INMOVIL,2)?30:0),jitter:.4},
    {id:A.SILENCIO_ENTRE_CAMPANAS,score:10+(s.techniqueRepeat?32:0)+(s.elementRepeat?18:0)-(recent(state,A.SILENCIO_ENTRE_CAMPANAS,3)?50:0),jitter:.2},
    {id:A.BUSCAR_PULSO,score:10+(s.qiStreak?28:0)+(s.playerQiHigh?10:0)-(recent(state,A.BUSCAR_PULSO,3)?50:0),jitter:.2}
  ];
  const c=choose(entries,rng);
  let plan=null;
  if(c.id===A.SILENCIO_ENTRE_CAMPANAS){
    const ref=tail(state.history,1)[0]||null;
    plan={id:'ROMPER_REPETICION',armed:false,followup:A.ROMPER_RITMO,referenceTechnique:ref?.techniqueId||null,referenceElement:ref?.element||null};
  }else if(c.id===A.BUSCAR_PULSO){
    plan={id:'CAZAR_CIRCULACION',armed:false,followup:A.CAMPANA_SIN_DUENO};
  }
  return {intent:intent(c.id,'MAESTRA',{reason:'UTILITY_PLANIFICADA',planId:plan?.id||null}),state:remember(state,c.id,{plan})};
}

function counterResponseFor(role){
  return GRULLA_COUNTER_RESPONSES[role]||GRULLA_COUNTER_RESPONSES.desconocida;
}

export function grullaCounterAnnouncement(state){
  plain(state,'state');
  const counter=state.techniqueCounter;
  if(!counter?.locked)return null;
  const response=counterResponseFor(counter.techniqueRole);
  return Object.freeze({
    techniqueId:counter.techniqueId,
    techniqueRole:counter.techniqueRole??null,
    counterMode:response.id,
    counterLabel:response.label,
    telegraph:response.telegraph,
    source:counter.source
  });
}

export function grullaTechniqueEffectiveness(state,playerAction){
  plain(state,'state');
  const action=actionCopy(playerAction);
  const counter=state.techniqueCounter;
  const blocked=!!(
    state.phase>=2&&
    counter?.locked&&
    action.techniqueId&&
    action.techniqueId===counter.techniqueId
  );
  const role=counter?.techniqueRole??action.techniqueRole??null;
  const response=counterResponseFor(role);
  return Object.freeze({
    multiplier:blocked?0:1,
    blocked,
    consumeQi:true,
    refundQi:false,
    suppressEffects:blocked,
    suppressDamage:blocked,
    suppressControl:blocked,
    suppressAfflictions:blocked,
    suppressResourceEffects:blocked,
    suppressGuard:blocked&&role==='guardia',
    suppressDefenseBuff:blocked&&role==='fortificacion',
    suppressEvasion:blocked&&role==='esquiva',
    techniqueId:action.techniqueId,
    techniqueRole:role,
    counteredTechniqueId:counter?.techniqueId??null,
    counterMode:blocked?response.id:null,
    counterLabel:blocked?response.label:null,
    telegraph:blocked?response.telegraph:null,
    primarySuppression:blocked?response.primarySuppression:null,
    reason:blocked?'TECHNIQUE_FULLY_READ':'NORMAL'
  });
}

function nextTechniqueCounter(state,action,nextHistory){
  if(state.phase<2)return state.techniqueCounter?{...state.techniqueCounter}:null;

  const current=state.techniqueCounter?{...state.techniqueCounter}:null;
  if(current?.locked){
    if(action.techniqueId===current.techniqueId)return current;

    // Defender, curarse o una utility sin técnica NO hacen olvidar una skill
    // ya comprendida. Para romper el conocimiento hay que mostrar una
    // alternativa táctica real: otra técnica/control o un ataque básico.
    const meaningfulVariation=
      action.type==='BASIC'||
      (action.techniqueId&&action.techniqueId!==current.techniqueId);

    return meaningfulVariation?null:current;
  }

  const last3=tail(nextHistory,3);
  if(
    last3.length===3&&
    last3.every(x=>x.techniqueId&&x.techniqueId===last3[0].techniqueId)
  ){
    return {
      techniqueId:last3[0].techniqueId,
      techniqueRole:last3[0].techniqueRole??null,
      locked:true,
      source:'THREE_CONSECUTIVE_SAME_SKILL'
    };
  }
  return null;
}

export function observeResolvedPlayerAction(state,playerAction){
  plain(state,'state');
  const action=actionCopy(playerAction);
  let plan=state.plan?{...state.plan}:null;
  let event='NONE';
  const nextHistory=[...state.history,action].slice(-MAX_HISTORY);
  const previousCounter=state.techniqueCounter;
  const techniqueCounter=nextTechniqueCounter(state,action,nextHistory);

  if(state.phase===3&&plan&&!plan.armed){
    if(plan.id==='ROMPER_REPETICION'){
      const repeatsTechnique=plan.referenceTechnique&&action.techniqueId===plan.referenceTechnique;
      const repeatsElement=plan.referenceElement&&action.element===plan.referenceElement&&['TECHNIQUE','CONTROL'].includes(action.type);
      if(repeatsTechnique||repeatsElement){plan.armed=true;event='PLAN_ARMED';}
      else {plan=null;event='PLAN_BROKEN_BY_VARIATION';}
    }else if(plan.id==='CAZAR_CIRCULACION'){
      if(action.qiSpent>0&&['TECHNIQUE','CONTROL'].includes(action.type)){plan.armed=true;event='PLAN_ARMED';}
      else {plan=null;event='PLAN_BROKEN_BY_RESOURCE_DISCIPLINE';}
    }
  }else if(state.phase===3&&plan?.armed){
    plan=null;
    event='PLAN_COMPLETED';
  }

  if(!previousCounter?.locked&&techniqueCounter?.locked&&event==='NONE'){
    event='TECHNIQUE_COUNTER_LOCKED';
  }else if(previousCounter?.locked&&!techniqueCounter&&event==='NONE'){
    event='TECHNIQUE_COUNTER_BROKEN_BY_VARIATION';
  }

  return {
    state:freezeState({...state,history:nextHistory,plan,techniqueCounter}),
    event
  };
}

export function interruptGrullaPlan(state){
  plain(state,'state');
  return freezeState({...state,plan:null});
}

export function grullaCapabilitySnapshot(state,context={}){
  plain(state,'state');
  const s=signals(state,context);
  return Object.freeze({
    phase:state.phase,
    turn:state.turn,
    brain:state.phase===1?'PROGRAMADA':state.phase===2?'ADAPTATIVA':'MAESTRA',
    memoryDepth:state.phase===1?0:4,
    signals:Object.freeze({...s,last:undefined}),
    plan:state.plan?Object.freeze({...state.plan}):null,
    techniqueCounter:state.techniqueCounter?Object.freeze({...state.techniqueCounter}):null,
    phaseMemory:Object.freeze({...state.phaseMemory})
  });
}
