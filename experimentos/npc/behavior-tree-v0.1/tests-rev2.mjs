import assert from 'node:assert/strict';
import {createRuntime,tickBehaviorTree} from './engine.mjs';
import {GUARD_TREE,SUPERVISOR_TREE} from './fixtures.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const tick=(tree,rt,facts={},actionResults={})=>tickBehaviorTree(tree,rt,{facts,actionResults});

T('REV2 SUCCESS completion is not preemption',()=>{
  let r=tick(GUARD_TREE,createRuntime(GUARD_TREE),{});
  r=tick(GUARD_TREE,r.nextRuntime,{}, {patrol:'SUCCESS'});
  assert.equal(r.status,'SUCCESS');
  assert.equal(r.preemptedAction,null);
});

T('REV2 FAILURE completion is not preemption',()=>{
  let r=tick(GUARD_TREE,createRuntime(GUARD_TREE),{});
  r=tick(GUARD_TREE,r.nextRuntime,{}, {patrol:'FAILURE'});
  assert.equal(r.status,'FAILURE');
  assert.equal(r.preemptedAction,null);
});

T('REV2 completed old action remains non-preempted when higher priority starts',()=>{
  let r=tick(GUARD_TREE,createRuntime(GUARD_TREE),{});
  r=tick(GUARD_TREE,r.nextRuntime,{hostile:true},{patrol:'SUCCESS'});
  assert.deepEqual(r.emitted,['ENGAGE']);
  assert.equal(r.runningAction,'engage');
  assert.equal(r.preemptedAction,null);
});

T('REV2 omitted result plus higher priority is real preemption',()=>{
  let r=tick(GUARD_TREE,createRuntime(GUARD_TREE),{});
  r=tick(GUARD_TREE,r.nextRuntime,{hostile:true},{});
  assert.equal(r.preemptedAction,'patrol');
  assert.deepEqual(r.emitted,['ENGAGE']);
});

T('REV2 RUNNING previous result plus higher priority is real preemption',()=>{
  let r=tick(GUARD_TREE,createRuntime(GUARD_TREE),{});
  r=tick(GUARD_TREE,r.nextRuntime,{hostile:true},{patrol:'RUNNING'});
  assert.equal(r.preemptedAction,'patrol');
  assert.deepEqual(r.emitted,['ENGAGE']);
});

T('REV2 supervisor normal completion is not preemption',()=>{
  let r=tick(SUPERVISOR_TREE,createRuntime(SUPERVISOR_TREE),{playerRequest:true});
  r=tick(SUPERVISOR_TREE,r.nextRuntime,{playerRequest:true},{assist:'SUCCESS'});
  assert.equal(r.preemptedAction,null);
});

console.log(`\nREV2 PASS: ${pass}`);
console.log(`REV2 FAIL: ${fail}`);
if(fail)process.exitCode=1;
