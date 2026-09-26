import assert from 'node:assert/strict';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {chooseAction,validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {MEI_LIAN_CANON,MEI_LIAN_POLICY_STATUS,MEI_LIAN_REQUIRED_CAPABILITY} from '../canonical/mei-lian.mjs';
import {MEI_LIAN_UTILITY_PROFILE} from '../profiles/mei-lian-utility-profile.mjs';
import {MEI_LIAN_SCENARIOS,meiContext} from '../scenarios/mei-lian.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const runtime=(state)=>state.npcs.find(x=>x.id==='mei_lian_lab');
const one=(result)=>result.dispatchResults[0];

function stateFor(scenario){
  const world=structuredClone(scenario.world);
  const utilityContext=meiContext(world);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(MEI_LIAN_UTILITY_PROFILE),world,utilityContext}],
    schedulerConfigs:[{id:'mei_lian_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon source is Mei Lian',()=>assert.equal(MEI_LIAN_CANON.id,'mei_lian'));
T('canonical routes stay inside posicion_valida',()=>assert.equal(MEI_LIAN_CANON.rutas.every(route=>route.every(x=>MEI_LIAN_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(MEI_LIAN_CANON.posicion_valida.includes(MEI_LIAN_CANON.sala_inicial),true));
T('M16 conditional front is canonical requirement',()=>assert.equal(MEI_LIAN_POLICY_STATUS.m16ConditionalFront,'CANONICAL_REQUIREMENT'));
T('front identity gap is explicit',()=>assert.equal(MEI_LIAN_POLICY_STATUS.frontIdentity,'CANONICAL_DOMAIN_CAPABILITY_GAP'));
T('Utility profile validates',()=>assert.deepEqual(validateNpc(MEI_LIAN_UTILITY_PROFILE),[]));

T('isolated Utility collapses SAUCES and MEDICINA to same action',()=>{
  const a=chooseAction(MEI_LIAN_UTILITY_PROFILE,meiContext(MEI_LIAN_SCENARIOS.m16Sauces.world));
  const b=chooseAction(MEI_LIAN_UTILITY_PROFILE,meiContext(MEI_LIAN_SCENARIOS.m16Medicina.world));
  assert.equal(a.action,'trabajar');
  assert.equal(b.action,'trabajar');
  assert.equal(a.score,b.score);
});
T('adding front to raw Utility context does not create domain semantics',()=>{
  const c=meiContext(MEI_LIAN_SCENARIOS.m16Sauces.world);
  c.front='SAUCES';
  const d=chooseAction(MEI_LIAN_UTILITY_PROFILE,c);
  assert.equal(d.action,'trabajar');
});
T('Autonomous Loop rejects unsupported front field',()=>{
  const world=structuredClone(MEI_LIAN_SCENARIOS.m16Sauces.world);
  const utilityContext=meiContext(world);
  utilityContext.front='SAUCES';
  assert.throws(()=>createAutonomousLoopState({
    npcs:[{npc:structuredClone(MEI_LIAN_UTILITY_PROFILE),world,utilityContext}],
    schedulerConfigs:[{id:'mei_lian_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  }));
});
T('SAUCES abstraction plans generic fulfill-duty',()=>{
  const first=tickAutonomousLoop(stateFor(MEI_LIAN_SCENARIOS.m16Sauces),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});
T('MEDICINA abstraction plans identical generic fulfill-duty',()=>{
  const first=tickAutonomousLoop(stateFor(MEI_LIAN_SCENARIOS.m16Medicina),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});
T('required M16 distinction remains unrepresented',()=>assert.equal(MEI_LIAN_REQUIRED_CAPABILITY,'M16_FRONT_ASSIGNMENT_SAUCES_OR_MEDICINA'));
T('tests do not mutate canon or profile',()=>{
  const c=JSON.stringify(MEI_LIAN_CANON),p=JSON.stringify(MEI_LIAN_UTILITY_PROFILE);
  tickAutonomousLoop(stateFor(MEI_LIAN_SCENARIOS.m16Sauces),1);
  assert.equal(JSON.stringify(MEI_LIAN_CANON),c);
  assert.equal(JSON.stringify(MEI_LIAN_UTILITY_PROFILE),p);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
