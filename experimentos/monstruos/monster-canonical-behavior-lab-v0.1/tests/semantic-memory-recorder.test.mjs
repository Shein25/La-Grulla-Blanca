import assert from 'node:assert/strict';
import {semanticEventFromOutcome,recordSemanticOutcome} from '../integration/semantic-memory-recorder-v0.1.mjs';

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('absorption effective maps exactly',()=>{
  assert.deepEqual(semanticEventFromOutcome({type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true}),
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:2});
});
T('absorption failure maps exactly',()=>{
  assert.deepEqual(semanticEventFromOutcome({type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:false}),
    {category:'DEFENSA_ABSORCION',result:'FALLIDA',round:2});
});
T('recovery maps exactly',()=>{
  assert.deepEqual(semanticEventFromOutcome({type:'PLAYER_RECOVERY_RESOLVED',round:3,effective:true}),
    {category:'RECUPERACION',result:'EFECTIVA',round:3});
});
T('unknown outcomes are ignored rather than invented',()=>{
  assert.equal(semanticEventFromOutcome({type:'PLAYER_DODGE_RESOLVED',round:3,effective:true}),null);
});
T('recorder preserves chronological order',()=>{
  let m=[];
  m=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true});
  m=recordSemanticOutcome(m,{type:'PLAYER_RECOVERY_RESOLVED',round:3,effective:false});
  assert.deepEqual(m.map(x=>x.round),[2,3]);
});
T('older future-incompatible outcome is rejected',()=>{
  const m=[{category:'RECUPERACION',result:'EFECTIVA',round:4}];
  assert.throws(()=>recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:3,effective:true}),/preceder/);
});
T('input memory is never mutated',()=>{
  const m=[{category:'RECUPERACION',result:'EFECTIVA',round:1}];
  const before=JSON.stringify(m);
  const next=recordSemanticOutcome(m,{type:'PLAYER_ABSORPTION_RESOLVED',round:2,effective:true});
  assert.equal(JSON.stringify(m),before);
  assert.notEqual(next,m);
});
T('returned memory/events are frozen',()=>{
  const m=recordSemanticOutcome([],{type:'PLAYER_RECOVERY_RESOLVED',round:1,effective:true});
  assert.equal(Object.isFrozen(m),true);
  assert.equal(Object.isFrozen(m[0]),true);
});
T('extra fields are rejected to prevent hidden inference',()=>{
  assert.throws(()=>semanticEventFromOutcome({type:'PLAYER_RECOVERY_RESOLVED',round:1,effective:true,hpAfter:99}),/campo no permitido/);
});
T('invalid effective is rejected',()=>{
  assert.throws(()=>semanticEventFromOutcome({type:'PLAYER_RECOVERY_RESOLVED',round:1,effective:1}),/boolean/);
});


console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
