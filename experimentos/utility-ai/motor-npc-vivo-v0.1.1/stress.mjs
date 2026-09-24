import assert from 'node:assert/strict';
import { chooseAction, evaluateDialogueTopic, validateActionContext, validateDialogueContext, validateNpc } from './engine.mjs';

const N=Math.max(1,Number(process.argv[2]||10000));
let seed=Number(process.argv[3]||1337)>>>0;
const rnd=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/2**32};
const r100=()=>Math.floor(rnd()*101), pick=a=>a[Math.floor(rnd()*a.length)];
const states=['DESCONOCIDO','SOSPECHA','SABE','CONFIRMADO'];
const actions=['vigilar','trabajar','patrullar','hablar_jugador','ayudar_jugador','investigar','informar_superior','regresar_puesto','esperar'];
const dutyModes=['vigilar','trabajar','patrullar','ninguno'];
const counts=new Map();

for (const bad of ['toString','constructor','__proto__']) {
  const baseNpc={
    id:'preflight',name:'Preflight',role:'Test',
    traits:{disciplina:50,sociabilidad:50,curiosidad:50,prudencia:50,lealtad_institucional:50,empatia:50},
    relationPlayer:{afinidad:50,confianza:50,respeto:50,deuda:0,temor:0,rivalidad:0},
    knowledge:{R1:'SABE',R2:'SABE',R3:'SABE'},
    behaviorState:{lastAction:null,consecutiveTurns:0},
  };
  baseNpc.knowledge.R1=bad;
  assert.notDeepEqual(validateNpc(baseNpc),[],`knowledge heredado aceptado: ${bad}`);

  const baseContext={
    playerPresent:true,playerRequestsHelp:false,playerRank:2,dutyImportance:0,dutyMode:'ninguno',
    danger:0,missionUrgency:0,anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:bad,topicSensitivity:50,formalRestriction:0,
  };
  assert.notDeepEqual(validateActionContext(baseContext),[],`relevantKnowledge heredado aceptado: ${bad}`);
}

const inheritedContext=Object.create({
  playerPresent:true,playerRequestsHelp:false,playerRank:2,dutyImportance:0,dutyMode:'ninguno',
  danger:0,missionUrgency:0,anomalyPresent:false,awayFromPost:false,superiorReachable:false,
  relevantKnowledge:'SABE',topicSensitivity:50,formalRestriction:0,
});
assert.notDeepEqual(validateActionContext(inheritedContext),[],'contexto heredado aceptado');

{
  const getterNpc={
    id:'getter',name:'Getter',role:'Preflight',
    traits:{disciplina:50,sociabilidad:50,curiosidad:50,prudencia:50,lealtad_institucional:50,empatia:50},
    relationPlayer:{afinidad:50,confianza:50,respeto:50,deuda:0,temor:0,rivalidad:0},
    knowledge:{R1:'SABE',R2:'SABE',R3:'SABE'},
    behaviorState:{lastAction:null,consecutiveTurns:0},
  };
  let reads=0;
  Object.defineProperty(getterNpc.knowledge,'R1',{enumerable:true,get(){reads++;return reads<3?'SABE':'toString'}});
  assert.notDeepEqual(validateNpc(getterNpc),[],'getter de knowledge aceptado');
  assert.equal(reads,0,'el getter de knowledge fue ejecutado por el validador');
}

{
  const getterContext={
    playerPresent:true,playerRequestsHelp:false,playerRank:2,dutyImportance:0,dutyMode:'ninguno',
    danger:0,missionUrgency:0,anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:'SABE',topicSensitivity:50,formalRestriction:0,
  };
  let reads=0;
  Object.defineProperty(getterContext,'relevantKnowledge',{enumerable:true,get(){reads++;return reads<3?'SABE':'constructor'}});
  assert.notDeepEqual(validateActionContext(getterContext),[],'getter de relevantKnowledge aceptado');
  assert.equal(reads,0,'el getter de relevantKnowledge fue ejecutado por el validador');
}

{
  const npc={
    id:'undefined',name:'Undefined',role:'Preflight',
    traits:{disciplina:50,sociabilidad:50,curiosidad:50,prudencia:50,lealtad_institucional:50,empatia:50},
    relationPlayer:{afinidad:50,confianza:50,respeto:50,deuda:0,temor:0,rivalidad:0},
    knowledge:{R1:'SABE',R2:'SABE',R3:'SABE'},
    behaviorState:{lastAction:null,consecutiveTurns:0},
  };
  npc.knowledge.R1=undefined;
  assert.notDeepEqual(validateNpc(npc),[],'knowledge undefined aceptado');
}

{
  const context={
    playerPresent:true,playerRequestsHelp:false,playerRank:2,dutyImportance:0,dutyMode:'ninguno',
    danger:0,missionUrgency:0,anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:undefined,topicSensitivity:50,formalRestriction:0,
  };
  assert.notDeepEqual(validateActionContext(context),[],'relevantKnowledge undefined aceptado');
}

{
  const dialogue={playerRank:2,topicSensitivity:undefined,formalRestriction:0};
  assert.notDeepEqual(validateDialogueContext(dialogue),[],'topicSensitivity undefined aceptado');
}

{
  let gets=0;
  const base={
    playerPresent:false,playerRequestsHelp:false,playerRank:2,dutyImportance:0,dutyMode:'ninguno',
    danger:0,missionUrgency:0,anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:'SABE',topicSensitivity:50,formalRestriction:0,
  };
  const proxy=new Proxy(base,{
    get(target,key,receiver){
      gets++;
      if(key==='missionUrgency') return NaN;
      return Reflect.get(target,key,receiver);
    },
  });
  assert.deepEqual(validateActionContext(proxy),[],'Proxy estable por descriptor no validó');
  const decision=chooseAction({
    id:'proxy',name:'Proxy',role:'Preflight',
    traits:{disciplina:50,sociabilidad:50,curiosidad:50,prudencia:50,lealtad_institucional:50,empatia:50},
    relationPlayer:{afinidad:50,confianza:50,respeto:50,deuda:0,temor:0,rivalidad:0},
    knowledge:{R1:'SABE',R2:'SABE',R3:'SABE'},
    behaviorState:{lastAction:null,consecutiveTurns:0},
  },proxy);
  assert.ok(Number.isFinite(decision.score)&&Number.isFinite(decision.raw),'Proxy produjo utilidad no finita');
  assert.equal(gets,0,'se ejecutó get trap del contexto');
}

{
  let gets=0;
  const proxy=new Proxy({playerRank:2,topicSensitivity:50,formalRestriction:0},{
    get(target,key,receiver){
      gets++;
      if(key==='topicSensitivity') return NaN;
      return Reflect.get(target,key,receiver);
    },
  });
  assert.deepEqual(validateDialogueContext(proxy),[],'Proxy de diálogo no validó por descriptor');
  const npc={
    id:'proxy-dialogue',name:'Proxy Dialogue',role:'Preflight',
    traits:{disciplina:50,sociabilidad:50,curiosidad:50,prudencia:50,lealtad_institucional:50,empatia:50},
    relationPlayer:{afinidad:50,confianza:50,respeto:50,deuda:0,temor:0,rivalidad:0},
    knowledge:{R1:'SABE',R2:'SABE',R3:'SABE'},
    behaviorState:{lastAction:null,consecutiveTurns:0},
  };
  const d=evaluateDialogueTopic(npc,'R1',proxy);
  assert.ok(Number.isFinite(d.disclosure)&&Number.isFinite(d.raw),'Proxy produjo disclosure no finito');
  assert.equal(gets,0,'se ejecutó get trap de diálogo');
}

{
  const npc={
    id:'proxy-npc',name:'Proxy NPC',role:'Preflight',
    traits:{disciplina:50,sociabilidad:50,curiosidad:50,prudencia:50,lealtad_institucional:50,empatia:50},
    relationPlayer:{afinidad:50,confianza:50,respeto:50,deuda:0,temor:0,rivalidad:0},
    knowledge:{R1:'SABE',R2:'SABE',R3:'SABE'},
    behaviorState:{lastAction:null,consecutiveTurns:0},
  };
  let gets=0;
  npc.traits=new Proxy(npc.traits,{
    get(target,key,receiver){
      gets++;
      if(key==='disciplina') throw new Error('late trap');
      return Reflect.get(target,key,receiver);
    },
  });
  assert.deepEqual(validateNpc(npc),[],'Proxy anidado no validó por descriptor');
  const base={
    playerPresent:true,playerRequestsHelp:false,playerRank:2,dutyImportance:50,dutyMode:'vigilar',
    danger:0,missionUrgency:0,anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:'SABE',topicSensitivity:50,formalRestriction:0,
  };
  const decision=chooseAction(npc,base);
  assert.ok(Number.isFinite(decision.score)&&Number.isFinite(decision.raw),'Proxy NPC produjo utilidad no finita');
  assert.equal(gets,0,'se ejecutó get trap anidado del NPC');
}

for(let i=0;i<N;i++){
  const last=rnd()<0.25?pick(actions):null;
  const npc={
    id:`stress_${i}`,name:'Stress NPC',role:'Fixture aleatorio',
    traits:{disciplina:r100(),sociabilidad:r100(),curiosidad:r100(),prudencia:r100(),lealtad_institucional:r100(),empatia:r100()},
    relationPlayer:{afinidad:r100(),confianza:r100(),respeto:r100(),deuda:r100(),temor:r100(),rivalidad:r100()},
    knowledge:{R1:pick(states),R2:pick(states),R3:pick(states)},
    behaviorState:{lastAction:last,consecutiveTurns:last?1+Math.floor(rnd()*6):0},
  };
  assert.deepEqual(validateNpc(npc),[]);

  const playerPresent=rnd()<0.7;
  const context={
    playerPresent,playerRequestsHelp:playerPresent&&rnd()<0.45,playerRank:Math.floor(rnd()*7),
    dutyImportance:r100(),dutyMode:pick(dutyModes),danger:r100(),missionUrgency:r100(),anomalyPresent:rnd()<0.4,
    awayFromPost:rnd()<0.25,superiorReachable:rnd()<0.9,relevantKnowledge:pick(states),
    topicSensitivity:r100(),formalRestriction:r100(),
  };
  assert.deepEqual(validateActionContext(context),[]);

  const a=chooseAction(npc,context),b=chooseAction(npc,context);
  assert.deepEqual(a,b,'No determinista');
  assert.ok(Number.isFinite(a.score)&&a.score>=0&&a.score<=100);
  assert.ok(Number.isFinite(a.raw));
  assert.ok(a.ranking.some(x=>x.name===a.action&&x.available));

  if(!playerPresent){
    assert.equal(a.ranking.find(x=>x.name==='hablar_jugador').available,false);
    assert.equal(a.ranking.find(x=>x.name==='ayudar_jugador').available,false);
  }

  const d=evaluateDialogueTopic(npc,'R1',context);
  if(npc.knowledge.R1==='DESCONOCIDO'){assert.equal(d.mode,'NO_SABE');assert.equal(d.disclosure,0)}
  if(npc.knowledge.R1==='SOSPECHA')assert.notEqual(d.mode,'COMPARTE');
  counts.set(a.action,(counts.get(a.action)||0)+1);
}

console.log(`Stress PASS: ${N} casos · seed final ${seed}`);
console.log(Object.fromEntries([...counts.entries()].sort((a,b)=>b[1]-a[1])));
