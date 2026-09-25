import assert from 'node:assert/strict';
import {ContractError,validateMachine,createRuntime,stepFSM} from './engine.mjs';
import {GUARD_MACHINE,WORKER_MACHINE,PATROLLER_MACHINE} from './fixtures.mjs';

let pass=0, fail=0;
function test(name,fn){
  try{fn(); pass++; console.log(`PASS ${name}`);}catch(e){fail++; console.error(`FAIL ${name}`); console.error(e.stack||e);}
}
function throws(fn){assert.throws(fn,ContractError);}

const clone=x=>structuredClone(x);

test('validates three fixtures',()=>{validateMachine(GUARD_MACHINE);validateMachine(WORKER_MACHINE);validateMachine(PATROLLER_MACHINE);});
test('initial runtime',()=>assert.deepEqual(createRuntime(GUARD_MACHINE),{machineId:'fixture_guard',state:'POST',stateAge:0,step:0}));
test('unhandled event does not transition and ages state',()=>{
  const r=stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'NOTHING',facts:{}});
  assert.equal(r.transitioned,false); assert.equal(r.nextRuntime.state,'POST'); assert.equal(r.nextRuntime.stateAge,1); assert.equal(r.nextRuntime.step,1);
});
test('transition resets age',()=>{
  const rt={machineId:'fixture_guard',state:'POST',stateAge:7,step:3};
  const r=stepFSM(GUARD_MACHINE,rt,{type:'SUSPICIOUS',facts:{}});
  assert.equal(r.nextRuntime.state,'ALERT'); assert.equal(r.nextRuntime.stateAge,0); assert.equal(r.nextRuntime.step,4);
});
test('guard false keeps state',()=>{
  const r=stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'TICK',facts:{patrolDue:false}});
  assert.equal(r.transitioned,false); assert.equal(r.nextRuntime.state,'POST');
});
test('guard true transitions',()=>{
  const r=stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'TICK',facts:{patrolDue:true}});
  assert.equal(r.to,'PATROL'); assert.deepEqual(r.emitted,['START_PATROL']);
});
test('highest priority wins among matching transitions',()=>{
  const m={id:'p',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',emit:['LOW']},{priority:2,target:'C',emit:['HIGH']}]}},B:{on:{}},C:{on:{}}}};
  const r=stepFSM(m,createRuntime(m),{type:'X',facts:{}}); assert.equal(r.to,'C'); assert.deepEqual(r.emitted,['HIGH']);
});
test('compound all guard',()=>{
  const m={id:'g',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{all:[{source:'event',key:'x',op:'GTE',value:2},{source:'event',key:'y',op:'EQ',value:true}]}}]}},B:{on:{}}}};
  assert.equal(stepFSM(m,createRuntime(m),{type:'X',facts:{x:2,y:true}}).to,'B');
});
test('compound any guard',()=>{
  const m={id:'g2',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{any:[{source:'event',key:'x',op:'EQ',value:1},{source:'event',key:'x',op:'EQ',value:2}]}}]}},B:{on:{}}}};
  assert.equal(stepFSM(m,createRuntime(m),{type:'X',facts:{x:2}}).to,'B');
});
test('compound not guard',()=>{
  const m={id:'g3',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{not:{source:'event',key:'blocked',op:'EQ',value:true}}}]}},B:{on:{}}}};
  assert.equal(stepFSM(m,createRuntime(m),{type:'X',facts:{blocked:false}}).to,'B');
});
test('IN guard',()=>{
  const m={id:'g4',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{source:'event',key:'phase',op:'IN',value:['A','B']}}]}},B:{on:{}}}};
  assert.equal(stepFSM(m,createRuntime(m),{type:'X',facts:{phase:'B'}}).to,'B');
});
test('runtime guard can use stateAge',()=>{
  const m={id:'age',initialState:'A',states:{A:{on:{TICK:[{priority:1,target:'B',guard:{source:'runtime',key:'stateAge',op:'GTE',value:2}}]}},B:{on:{}}}};
  let rt=createRuntime(m); rt=stepFSM(m,rt,{type:'TICK',facts:{}}).nextRuntime; rt=stepFSM(m,rt,{type:'TICK',facts:{}}).nextRuntime;
  const r=stepFSM(m,rt,{type:'TICK',facts:{}}); assert.equal(r.to,'B');
});
test('deterministic byte-equivalent result',()=>{
  const rt=createRuntime(GUARD_MACHINE), ev={type:'SUSPICIOUS',facts:{}};
  assert.deepEqual(stepFSM(GUARD_MACHINE,rt,ev),stepFSM(GUARD_MACHINE,rt,ev));
});
test('does not mutate machine runtime or event',()=>{
  const m=clone(GUARD_MACHINE), rt=createRuntime(m), ev={type:'TICK',facts:{patrolDue:true}};
  const before=[clone(m),clone(rt),clone(ev)]; stepFSM(m,rt,ev); assert.deepEqual([m,rt,ev],before);
});
test('emitted array is independent',()=>{
  const r=stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'SUSPICIOUS',facts:{}}); r.emitted.push('X');
  const r2=stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'SUSPICIOUS',facts:{}}); assert.deepEqual(r2.emitted,['OBSERVE']);
});
test('rejects unknown initial state',()=>{const m=clone(GUARD_MACHINE);m.initialState='NO';throws(()=>validateMachine(m));});
test('rejects unknown transition target',()=>{const m=clone(GUARD_MACHINE);m.states.POST.on.SUSPICIOUS[0].target='NO';throws(()=>validateMachine(m));});
test('rejects duplicate priority',()=>{const m=clone(GUARD_MACHINE);m.states.POST.on.SUSPICIOUS.push({priority:10,target:'ALERT'});throws(()=>validateMachine(m));});
test('rejects extra machine field',()=>{const m=clone(GUARD_MACHINE);m.extra=true;throws(()=>validateMachine(m));});
test('rejects extra transition field',()=>{const m=clone(GUARD_MACHINE);m.states.POST.on.SUSPICIOUS[0].action=()=>{};throws(()=>validateMachine(m));});
test('rejects callback-like emit',()=>{const m=clone(GUARD_MACHINE);m.states.POST.on.SUSPICIOUS[0].emit=[()=>{}];throws(()=>validateMachine(m));});
test('rejects inherited event',()=>{const ev=Object.create({type:'X',facts:{}});throws(()=>stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),ev));});
test('rejects accessor in event facts without executing it',()=>{
  let reads=0;const facts={};Object.defineProperty(facts,'x',{enumerable:true,get(){reads++;return 1;}});
  throws(()=>stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'X',facts}));assert.equal(reads,0);
});
test('rejects non-finite fact',()=>throws(()=>stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),{type:'X',facts:{x:NaN}})));
test('rejects invalid runtime state',()=>throws(()=>stepFSM(GUARD_MACHINE,{machineId:'fixture_guard',state:'NO',stateAge:0,step:0},{type:'X',facts:{}})));
test('guard flow: suspicious warn combat return post',()=>{
  let rt=createRuntime(GUARD_MACHINE);
  for(const ev of [{type:'SUSPICIOUS',facts:{}},{type:'PERSISTS',facts:{}},{type:'HOSTILE',facts:{}},{type:'THREAT_ENDED',facts:{}},{type:'ARRIVED',facts:{}}]) rt=stepFSM(GUARD_MACHINE,rt,ev).nextRuntime;
  assert.equal(rt.state,'POST');
});
test('worker flow: prep serve clean prep',()=>{
  let rt=createRuntime(WORKER_MACHINE);
  for(const ev of [{type:'TICK',facts:{phase:'SERVICE'}},{type:'TASK_COMPLETE',facts:{}},{type:'TASK_COMPLETE',facts:{}}]) rt=stepFSM(WORKER_MACHINE,rt,ev).nextRuntime;
  assert.equal(rt.state,'PREP');
});
test('worker emergency interrupts service',()=>{
  let rt=createRuntime(WORKER_MACHINE);rt=stepFSM(WORKER_MACHINE,rt,{type:'TICK',facts:{phase:'SERVICE'}}).nextRuntime;
  rt=stepFSM(WORKER_MACHINE,rt,{type:'ALARM',facts:{}}).nextRuntime;assert.equal(rt.state,'EMERGENCY');
});
test('patroller flow: patrol alert return post',()=>{
  let rt=createRuntime(PATROLLER_MACHINE);
  for(const ev of [{type:'TICK',facts:{patrolDue:true}},{type:'SUSPICIOUS',facts:{}},{type:'CLEARED',facts:{}},{type:'ARRIVED',facts:{}}]) rt=stepFSM(PATROLLER_MACHINE,rt,ev).nextRuntime;
  assert.equal(rt.state,'POST');
});
test('one event causes at most one transition',()=>{
  const m={id:'one',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B'}]}},B:{on:{X:[{priority:1,target:'C'}]}},C:{on:{}}}};
  const r=stepFSM(m,createRuntime(m),{type:'X',facts:{}}); assert.equal(r.to,'B'); assert.equal(r.nextRuntime.step,1);
});

console.log(`\nPASS: ${pass}`);console.log(`FAIL: ${fail}`);if(fail) process.exitCode=1;
