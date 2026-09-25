const OPS = new Set(['EQ','NEQ','GT','GTE','LT','LTE','IN']);
const SOURCES = new Set(['event','runtime']);

export class ContractError extends TypeError {
  constructor(message){ super(`ReactiveRoutineFSM: ${message}`); this.name='ContractError'; }
}

function isPlainObject(value){
  if(value===null || typeof value!=='object' || Array.isArray(value)) return false;
  const p=Object.getPrototypeOf(value);
  return p===Object.prototype || p===null;
}

function fail(message){ throw new ContractError(message); }

function ownData(obj,key,label){
  let d;
  try { d=Object.getOwnPropertyDescriptor(obj,key); }
  catch { fail(`${label}.${key} no se pudo inspeccionar`); }
  if(!d) fail(`${label}.${key} es obligatorio`);
  if(!('value' in d)) fail(`${label}.${key} no admite accessors`);
  if(d.value===undefined) fail(`${label}.${key} no puede ser undefined`);
  return d.value;
}

function exactKeys(obj, allowed, label){
  if(!isPlainObject(obj)) fail(`${label} debe ser objeto plano`);
  let keys;
  try { keys=Reflect.ownKeys(obj); }
  catch { fail(`${label} no se pudo inspeccionar`); }
  if(keys.some(k=>typeof k!=='string')) fail(`${label} no admite Symbols`);
  for(const k of keys) if(!allowed.includes(k)) fail(`${label}.${k} no está permitido`);
  return keys;
}

function capturePrimitive(value,label){
  if(value===null) return null;
  if(['string','number','boolean'].includes(typeof value)){
    if(typeof value==='number' && !Number.isFinite(value)) fail(`${label} debe ser finito`);
    return value;
  }
  fail(`${label} debe ser primitivo JSON`);
}

function captureFacts(input,label='event.facts'){
  if(!isPlainObject(input)) fail(`${label} debe ser objeto plano`);
  const out=Object.create(null);
  for(const key of Reflect.ownKeys(input)){
    if(typeof key!=='string') fail(`${label} no admite Symbols`);
    const value=ownData(input,key,label);
    out[key]=capturePrimitive(value,`${label}.${key}`);
  }
  return out;
}

function captureEvent(input){
  exactKeys(input,['type','facts'],'event');
  const type=ownData(input,'type','event');
  const facts=ownData(input,'facts','event');
  if(typeof type!=='string' || !type.trim()) fail('event.type debe ser string no vacío');
  return {type, facts:captureFacts(facts)};
}

function captureGuard(g,label='guard'){
  if(g===null) return null;
  if(!isPlainObject(g)) fail(`${label} debe ser objeto plano`);
  const keys=Reflect.ownKeys(g);
  if(keys.some(k=>typeof k!=='string')) fail(`${label} no admite Symbols`);
  const hasAll=Object.hasOwn(g,'all'), hasAny=Object.hasOwn(g,'any'), hasNot=Object.hasOwn(g,'not');
  const compoundCount=[hasAll,hasAny,hasNot].filter(Boolean).length;
  if(compoundCount){
    if(compoundCount!==1 || keys.length!==1) fail(`${label} compuesto debe tener exactamente all, any o not`);
    if(hasNot) return {not:captureGuard(ownData(g,'not',label),`${label}.not`)};
    const field=hasAll?'all':'any';
    const arr=ownData(g,field,label);
    if(!Array.isArray(arr) || arr.length===0) fail(`${label}.${field} debe ser array no vacío`);
    return {[field]:arr.map((x,i)=>captureGuard(x,`${label}.${field}[${i}]`))};
  }
  exactKeys(g,['source','key','op','value'],label);
  const source=ownData(g,'source',label), key=ownData(g,'key',label), op=ownData(g,'op',label), value=ownData(g,'value',label);
  if(!SOURCES.has(source)) fail(`${label}.source inválido`);
  if(typeof key!=='string' || !key) fail(`${label}.key debe ser string no vacío`);
  if(!OPS.has(op)) fail(`${label}.op inválido`);
  if(op==='IN'){
    if(!Array.isArray(value) || value.length===0) fail(`${label}.value para IN debe ser array no vacío`);
    return {source,key,op,value:value.map((v,i)=>capturePrimitive(v,`${label}.value[${i}]`))};
  }
  return {source,key,op,value:capturePrimitive(value,`${label}.value`)};
}

function captureEmit(value,label){
  if(value===undefined) return [];
  if(!Array.isArray(value)) fail(`${label} debe ser array`);
  const out=[]; const seen=new Set();
  for(let i=0;i<value.length;i++){
    const x=value[i];
    if(typeof x!=='string' || !x.trim()) fail(`${label}[${i}] debe ser string no vacío`);
    if(seen.has(x)) fail(`${label} no admite intents duplicados`);
    seen.add(x); out.push(x);
  }
  return out;
}

export function validateMachine(input){
  exactKeys(input,['id','initialState','states'],'machine');
  const id=ownData(input,'id','machine'), initialState=ownData(input,'initialState','machine'), statesIn=ownData(input,'states','machine');
  if(typeof id!=='string' || !id.trim()) fail('machine.id debe ser string no vacío');
  if(typeof initialState!=='string' || !initialState.trim()) fail('machine.initialState debe ser string no vacío');
  if(!isPlainObject(statesIn)) fail('machine.states debe ser objeto plano');
  const stateNames=Reflect.ownKeys(statesIn);
  if(stateNames.length===0 || stateNames.some(k=>typeof k!=='string' || !k)) fail('machine.states debe tener estados con IDs string');
  if(!stateNames.includes(initialState)) fail('machine.initialState no existe en states');

  const states=Object.create(null);
  for(const stateName of stateNames){
    const state=ownData(statesIn,stateName,'machine.states');
    exactKeys(state,['on'],`machine.states.${stateName}`);
    const onIn=ownData(state,'on',`machine.states.${stateName}`);
    if(!isPlainObject(onIn)) fail(`machine.states.${stateName}.on debe ser objeto plano`);
    const on=Object.create(null);
    for(const eventType of Reflect.ownKeys(onIn)){
      if(typeof eventType!=='string' || !eventType) fail('event type inválido');
      const arr=ownData(onIn,eventType,`machine.states.${stateName}.on`);
      if(!Array.isArray(arr) || arr.length===0) fail(`transiciones ${stateName}/${eventType} deben ser array no vacío`);
      const priorities=new Set();
      const transitions=arr.map((t,i)=>{
        const label=`machine.states.${stateName}.on.${eventType}[${i}]`;
        exactKeys(t,['priority','target','guard','emit'],label);
        const priority=ownData(t,'priority',label), target=ownData(t,'target',label);
        if(!Number.isSafeInteger(priority)) fail(`${label}.priority debe ser entero seguro`);
        if(priorities.has(priority)) fail(`${stateName}/${eventType} tiene priority duplicada ${priority}`);
        priorities.add(priority);
        if(typeof target!=='string' || !stateNames.includes(target)) fail(`${label}.target desconocido`);
        const guard=Object.hasOwn(t,'guard') ? captureGuard(ownData(t,'guard',label),`${label}.guard`) : null;
        const emit=Object.hasOwn(t,'emit') ? captureEmit(ownData(t,'emit',label),`${label}.emit`) : [];
        return {priority,target,guard,emit};
      });
      transitions.sort((a,b)=>b.priority-a.priority);
      on[eventType]=transitions;
    }
    states[stateName]={on};
  }
  return {id,initialState,states};
}

function runtimeSnapshot(input,machine){
  exactKeys(input,['machineId','state','stateAge','step'],'runtime');
  const machineId=ownData(input,'machineId','runtime'), state=ownData(input,'state','runtime'), stateAge=ownData(input,'stateAge','runtime'), step=ownData(input,'step','runtime');
  if(machineId!==machine.id) fail('runtime.machineId no coincide con machine.id');
  if(typeof state!=='string' || !Object.hasOwn(machine.states,state)) fail('runtime.state desconocido');
  if(!Number.isSafeInteger(stateAge) || stateAge<0) fail('runtime.stateAge debe ser entero >= 0');
  if(!Number.isSafeInteger(step) || step<0) fail('runtime.step debe ser entero >= 0');
  return {machineId,state,stateAge,step};
}

function getSourceValue(cond,event,runtime){
  if(cond.source==='event') return event.facts[cond.key];
  if(cond.source==='runtime') return runtime[cond.key];
  return undefined;
}

function cmp(actual,op,expected){
  if(op==='EQ') return Object.is(actual,expected);
  if(op==='NEQ') return !Object.is(actual,expected);
  if(op==='GT') return typeof actual==='number' && actual>expected;
  if(op==='GTE') return typeof actual==='number' && actual>=expected;
  if(op==='LT') return typeof actual==='number' && actual<expected;
  if(op==='LTE') return typeof actual==='number' && actual<=expected;
  if(op==='IN') return expected.some(v=>Object.is(v,actual));
  return false;
}

function guardMatches(g,event,runtime){
  if(g===null) return true;
  if(g.all) return g.all.every(x=>guardMatches(x,event,runtime));
  if(g.any) return g.any.some(x=>guardMatches(x,event,runtime));
  if(g.not) return !guardMatches(g.not,event,runtime);
  return cmp(getSourceValue(g,event,runtime),g.op,g.value);
}

export function createRuntime(machineInput){
  const machine=validateMachine(machineInput);
  return {machineId:machine.id,state:machine.initialState,stateAge:0,step:0};
}

export function stepFSM(machineInput,runtimeInput,eventInput){
  const machine=validateMachine(machineInput);
  const runtime=runtimeSnapshot(runtimeInput,machine);
  const event=captureEvent(eventInput);
  const candidates=machine.states[runtime.state].on[event.type] || [];
  const chosen=candidates.find(t=>guardMatches(t.guard,event,runtime)) || null;
  const next={
    machineId:runtime.machineId,
    state:chosen ? chosen.target : runtime.state,
    stateAge:chosen ? 0 : runtime.stateAge+1,
    step:runtime.step+1,
  };
  return {
    transitioned:Boolean(chosen),
    from:runtime.state,
    to:next.state,
    eventType:event.type,
    emitted:chosen ? [...chosen.emit] : [],
    nextRuntime:next,
  };
}
