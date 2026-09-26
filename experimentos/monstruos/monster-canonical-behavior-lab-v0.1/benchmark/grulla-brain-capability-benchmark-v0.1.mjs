import {
  GRULLA_ABILITIES as A,
  initialGrullaBrainState,
  chooseGrullaIntent,
  observeResolvedPlayerAction
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

const fixed=()=>.5;
const tech=(id,element,qiSpent=6,damageBand='NORMAL')=>({type:'TECHNIQUE',techniqueId:id,element,qiSpent,damageBand});

const PLAYER_PROFILES={
  SPAMMER:{
    label:'repite la misma técnica/elemento',
    act:()=>tech('palma','fuego',6,'NORMAL')
  },
  QI_BURNER:{
    label:'varía técnica pero gasta qi cada turno',
    act:({turn})=>turn%2?tech('palma','fuego',7):tech('filo','metal',7)
  },
  TURTLE:{
    label:'defiende/recupera con frecuencia',
    act:({turn})=>[
      {type:'DEFEND'},
      {type:'RECOVER'},
      {type:'DEFEND'},
      tech('filo','metal',5,'LOW')
    ][turn%4]
  },
  VARIED:{
    label:'mezcla básicos, técnicas, control y defensa',
    act:({turn})=>[
      {type:'BASIC',damageBand:'LOW'},
      tech('palma','fuego',5),
      {type:'DEFEND'},
      tech('filo','metal',5),
      {type:'CONTROL',techniqueId:'filamento',element:'viento',qiSpent:4,damageBand:'NONE'},
      {type:'RECOVER'}
    ][turn%6]
  },
  GOOD_READER:{
    label:'lee intención y rompe deliberadamente los planes',
    act:({turn,intent})=>{
      if([A.CAMPANADA_PICO,A.TORMENTA_MIL_PLUMAS,A.CAMPANA_SIN_DUENO].includes(intent.id))return {type:'DEFEND'};
      if(intent.id===A.SILENCIO_ENTRE_CAMPANAS)return turn%2?tech('filo','metal',5):{type:'BASIC',damageBand:'LOW'};
      if(intent.id===A.BUSCAR_PULSO||intent.id===A.RECORDAR_FILO)return {type:'BASIC',damageBand:'LOW'};
      return turn%3===0?tech('palma','fuego',5):turn%3===1?tech('filo','metal',5):{type:'BASIC',damageBand:'LOW'};
    }
  }
};

const counterIds=new Set([
  A.RECORDAR_FILO,A.ECO_MERIDIANO,A.CERRAR_ALAS,
  A.SILENCIO_ENTRE_CAMPANAS,A.ROMPER_RITMO,A.BUSCAR_PULSO,
  A.ALA_VACIA,A.PATA_INMOVIL
]);
const heavyIds=new Set([A.CAMPANADA_PICO,A.TORMENTA_MIL_PLUMAS,A.CAMPANA_SIN_DUENO]);

function runPhase(profileId,phase,turns){
  const profile=PLAYER_PROFILES[profileId];
  let state=initialGrullaBrainState({phase});
  let qi=1;
  const intents=[],events=[];
  let counters=0,heavy=0,defensive=0;

  for(let turn=0;turn<turns;turn++){
    const r=chooseGrullaIntent({
      state,
      context:{
        playerHpRatio:.65,
        playerQiRatio:qi,
        selfHpRatio:turn>turns*.75?.28:.75
      },
      rng:fixed
    });

    intents.push(r.intent.id);
    if(counterIds.has(r.intent.id))counters++;
    if(heavyIds.has(r.intent.id))heavy++;
    if([A.CERRAR_ALAS,A.PATA_INMOVIL,A.ALA_VACIA].includes(r.intent.id))defensive++;

    const action=profile.act({turn,intent:r.intent,state:r.state});
    qi=Math.max(0,qi-(action.qiSpent||0)/110);
    if(action.type==='RECOVER')qi=Math.min(1,qi+.25);

    const o=observeResolvedPlayerAction(r.state,action);
    if(o.event!=='NONE')events.push(o.event);
    state=o.state;
  }

  return {
    phase,turns,counters,heavy,defensive,
    planArmed:events.filter(x=>x==='PLAN_ARMED').length,
    planBroken:events.filter(x=>x.startsWith('PLAN_BROKEN')).length,
    planCompleted:events.filter(x=>x==='PLAN_COMPLETED').length,
    uniqueIntents:new Set(intents).size,
    intents
  };
}

const results={};
for(const id of Object.keys(PLAYER_PROFILES)){
  results[id]={
    label:PLAYER_PROFILES[id].label,
    phase1:runPhase(id,1,8),
    phase2:runPhase(id,2,12),
    phase3:runPhase(id,3,16)
  };
}

console.log(JSON.stringify({
  benchmark:'GRULLA_BRAIN_CAPABILITY_V01',
  status:'EXPERIMENTAL_NON_CANONICAL',
  purpose:'medir si los tres cerebros distinguen hábitos observables sin future-read',
  results
},null,2));
