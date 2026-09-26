export const SEMANTIC_MEMORY_STATUS='EXPERIMENTAL_RECORDER_V01';

const TYPES=Object.freeze({
  PLAYER_ABSORPTION_RESOLVED:'DEFENSA_ABSORCION',
  PLAYER_RECOVERY_RESOLVED:'RECUPERACION'
});

function plain(x){
  if(!x||typeof x!=='object'||Array.isArray(x))throw new TypeError('outcome debe ser objeto plano');
  const p=Object.getPrototypeOf(x);
  if(p!==Object.prototype&&p!==null)throw new TypeError('outcome debe ser objeto plano');
  return x;
}
function roundOf(v,label='round'){
  if(!Number.isInteger(v)||v<0)throw new TypeError(`${label} debe ser entero >= 0`);
  return v;
}
function validateMemory(memory){
  if(!Array.isArray(memory))throw new TypeError('memory debe ser array');
  let prev=-1;
  return memory.map((e,i)=>{
    plain(e);
    const keys=Object.keys(e).sort().join('|');
    if(keys!=='category|result|round')throw new TypeError(`memory[${i}] shape inválido`);
    const round=roundOf(e.round,`memory[${i}].round`);
    if(round<prev)throw new TypeError('memory debe estar en orden cronológico ascendente');
    prev=round;
    if(typeof e.category!=='string'||!e.category)throw new TypeError('memory.category inválida');
    if(!['EFECTIVA','FALLIDA','NEUTRA'].includes(e.result))throw new TypeError('memory.result inválido');
    return {category:e.category,result:e.result,round};
  });
}
function freezeEvent(e){return Object.freeze({...e});}

export function semanticEventFromOutcome(outcome){
  const o=plain(outcome);
  const allowed=['type','round','effective'];
  const keys=Object.keys(o);
  for(const k of keys)if(!allowed.includes(k))throw new TypeError(`outcome campo no permitido: ${k}`);
  if(typeof o.type!=='string'||!o.type)throw new TypeError('outcome.type inválido');
  const category=TYPES[o.type];
  if(!category)return null;
  const round=roundOf(o.round);
  if(typeof o.effective!=='boolean')throw new TypeError('outcome.effective debe ser boolean');
  return freezeEvent({category,result:o.effective?'EFECTIVA':'FALLIDA',round});
}

export function recordSemanticOutcome(memory,outcome){
  const current=validateMemory(memory);
  const event=semanticEventFromOutcome(outcome);
  if(!event)return Object.freeze(current.map(freezeEvent));
  const last=current.at(-1);
  if(last&&event.round<last.round)throw new TypeError('outcome no puede preceder la memoria existente');
  return Object.freeze([...current.map(freezeEvent),event]);
}
