import assert from 'node:assert/strict';
import {ContractError,MAX_GUARD_DEPTH,validateMachine,createRuntime,stepFSM} from './engine.mjs';
import {GUARD_MACHINE} from './fixtures.mjs';

let pass=0, fail=0;
function test(name,fn){ try{fn();pass++;console.log(`PASS ${name}`);}catch(e){fail++;console.error(`FAIL ${name}`);console.error(e.stack||e);} }
function throws(fn){assert.throws(fn,ContractError);}

// REV2 -- regresiones Claude H1-H6
test('REV2 H1 stateAge saturates and remains valid',()=>{const rt={machineId:'fixture_guard',state:'POST',stateAge:Number.MAX_SAFE_INTEGER,step:0};const r=stepFSM(GUARD_MACHINE,rt,{type:'NOTHING',facts:{}});assert.equal(r.nextRuntime.stateAge,Number.MAX_SAFE_INTEGER);assert.doesNotThrow(()=>stepFSM(GUARD_MACHINE,r.nextRuntime,{type:'NOTHING',facts:{}}));});
test('REV2 H1 step saturates and remains valid',()=>{const rt={machineId:'fixture_guard',state:'POST',stateAge:0,step:Number.MAX_SAFE_INTEGER};const r=stepFSM(GUARD_MACHINE,rt,{type:'NOTHING',facts:{}});assert.equal(r.nextRuntime.step,Number.MAX_SAFE_INTEGER);assert.doesNotThrow(()=>stepFSM(GUARD_MACHINE,r.nextRuntime,{type:'NOTHING',facts:{}}));});
test('REV2 H2 rejects forbidden runtime guard keys',()=>{for(const key of ['constructor','hasOwnProperty','__proto__','toString']){const m={id:'g',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{source:'runtime',key,op:'NEQ',value:'x'}}]}},B:{on:{}}}};throws(()=>validateMachine(m));}});
test('REV2 H2 allows declared runtime guard keys',()=>{for(const [key,value] of [['machineId','g'],['state','A'],['stateAge',0],['step',0]]){const m={id:'g',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{source:'runtime',key,op:'EQ',value}}]}},B:{on:{}}}};assert.doesNotThrow(()=>validateMachine(m));}});
test('REV2 H3 revoked machine proxy yields ContractError',()=>{const {proxy,revoke}=Proxy.revocable({...GUARD_MACHINE},{});revoke();throws(()=>validateMachine(proxy));});
test('REV2 H3 throwing getPrototypeOf proxy yields ContractError',()=>{const p=new Proxy({...GUARD_MACHINE},{getPrototypeOf(){throw new Error('boom')}});throws(()=>validateMachine(p));});
test('REV2 H3 hostile event proxy yields ContractError',()=>{const {proxy,revoke}=Proxy.revocable({type:'X',facts:{}},{});revoke();throws(()=>stepFSM(GUARD_MACHINE,createRuntime(GUARD_MACHINE),proxy));});
test('REV2 H4 rejects guard nesting beyond MAX_GUARD_DEPTH',()=>{let g={source:'event',key:'x',op:'EQ',value:1};for(let i=0;i<MAX_GUARD_DEPTH+1;i++)g={not:g};const m={id:'deep',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:g}]}},B:{on:{}}}};throws(()=>validateMachine(m));});
test('REV2 H4 accepts guard nesting at MAX_GUARD_DEPTH',()=>{let g={source:'event',key:'x',op:'EQ',value:1};for(let i=0;i<MAX_GUARD_DEPTH;i++)g={not:g};const m={id:'deepok',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:g}]}},B:{on:{}}}};assert.doesNotThrow(()=>validateMachine(m));});
test('REV2 H5 numeric comparators require numeric expected value',()=>{for(const op of ['GT','GTE','LT','LTE']){const m={id:'num',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{source:'event',key:'x',op,value:'not-a-number'}}]}},B:{on:{}}}};throws(()=>validateMachine(m));}});
test('REV2 H5 numeric runtime comparators require numeric runtime key',()=>{for(const key of ['machineId','state']){const m={id:'numrt',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{source:'runtime',key,op:'GT',value:1}}]}},B:{on:{}}}};throws(()=>validateMachine(m));}});
test('REV2 H5 NEQ absent fact remains explicitly true',()=>{const m={id:'neq',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',guard:{source:'event',key:'missing',op:'NEQ',value:'x'}}]}},B:{on:{}}}};assert.equal(stepFSM(m,createRuntime(m),{type:'X',facts:{}}).to,'B');});
test('REV2 H6 rejects extra property on emit array',()=>{const emit=['OK'];emit.extra='HIDDEN';const m={id:'arr',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',emit}]}},B:{on:{}}}};throws(()=>validateMachine(m));});
test('REV2 H6 rejects extra property on transition array',()=>{const transitions=[{priority:1,target:'B'}];transitions.extra='HIDDEN';const m={id:'arr2',initialState:'A',states:{A:{on:{X:transitions}},B:{on:{}}}};throws(()=>validateMachine(m));});
test('REV2 H6 rejects sparse emit arrays',()=>{const emit=[];emit[1]='OK';const m={id:'sparse',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',emit}]}},B:{on:{}}}};throws(()=>validateMachine(m));});
test('REV2 H6 rejects sparse transition arrays',()=>{const transitions=[];transitions[1]={priority:1,target:'B'};const m={id:'sparse2',initialState:'A',states:{A:{on:{X:transitions}},B:{on:{}}}};throws(()=>validateMachine(m));});
test('REV2 H6 rejects accessor array elements without executing them',()=>{let reads=0;const emit=[];Object.defineProperty(emit,'0',{enumerable:true,configurable:true,get(){reads++;return 'OK';}});emit.length=1;const m={id:'accarr',initialState:'A',states:{A:{on:{X:[{priority:1,target:'B',emit}]}},B:{on:{}}}};throws(()=>validateMachine(m));assert.equal(reads,0);});


console.log(`\nREV2 PASS: ${pass}`);console.log(`REV2 FAIL: ${fail}`);if(fail) process.exitCode=1;
