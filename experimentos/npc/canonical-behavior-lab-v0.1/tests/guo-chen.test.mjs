import assert from 'node:assert/strict';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {GUO_CHEN_CANON,GUO_CHEN_POLICY_STATUS,GUO_CHEN_FORBIDDEN_AUTONOMOUS_CAPABILITY} from '../canonical/guo-chen.mjs';
import {GUO_CHEN_UTILITY_PROFILE} from '../profiles/guo-chen-utility-profile.mjs';
import {GUO_CHEN_SCENARIOS,guoContext} from '../scenarios/guo-chen.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const runtime=(state)=>state.npcs.find(x=>x.id==='guo_chen_lab');
const one=(result)=>result.dispatchResults[0];

function stateFor(scenario){
  const world=structuredClone(scenario.world);
  const utilityContext=guoContext(world);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(GUO_CHEN_UTILITY_PROFILE),world,utilityContext}],
    schedulerConfigs:[{id:'guo_chen_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon source is Guo Chen',()=>assert.equal(GUO_CHEN_CANON.id,'guo_chen'));
T('canonical routes stay inside posicion_valida',()=>assert.equal(GUO_CHEN_CANON.rutas.every(route=>route.every(x=>GUO_CHEN_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(GUO_CHEN_CANON.posicion_valida.includes(GUO_CHEN_CANON.sala_inicial),true));
T('epilogue keeps second branch postponed',()=>assert.ok(GUO_CHEN_CANON.territorio_por_etapa.EPILOGO.includes('SEGUNDA_RAMA_POSTERGADA')));
T('NO_DECIDAS_POR_MI anchor is preserved',()=>assert.ok(GUO_CHEN_CANON.anclajes_documentados.some(x=>x.includes('NO_DECIDAS_POR_MI'))));
T('second branch is marked narrative constraint',()=>assert.equal(GUO_CHEN_POLICY_STATUS.secondBranchDecision,'CANONICAL_NARRATIVE_CONSTRAINT'));
T('generic duty collision requires integration guard',()=>assert.equal(GUO_CHEN_POLICY_STATUS.genericDutyCollision,'INTEGRATION_GUARD_REQUIRED'));
T('Utility profile validates',()=>assert.deepEqual(validateNpc(GUO_CHEN_UTILITY_PROFILE),[]));

T('M16 material work creates generic duty plan',()=>{
  const first=tickAutonomousLoop(stateFor(GUO_CHEN_SCENARIOS.m16MaterialWork),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});
T('M16 material duty can execute to symbolic completion',()=>{
  const first=tickAutonomousLoop(stateFor(GUO_CHEN_SCENARIOS.m16MaterialWork),1);
  const second=tickAutonomousLoop(first.state,2);
  assert.equal(one(second).executed,'cumplir_deber');
  assert.equal(one(second).status,'GOAL_REACHED');
  assert.equal(runtime(second.state).world.dutySatisfied,true);
});

T('adversarial second-branch duty collapses to same generic plan',()=>{
  const first=tickAutonomousLoop(stateFor(GUO_CHEN_SCENARIOS.adversarialSecondBranchEncodedAsGenericDuty),1);
  assert.equal(one(first).utilityAction,'trabajar');
  assert.equal(one(first).goalId,'FULFILL_DUTY');
  assert.deepEqual(runtime(first.state).executionSession.plan,['cumplir_deber']);
});
T('GOAP has no explicit second-branch or graft action',()=>{
  const serialized=JSON.stringify(GOAP_ACTIONS).toLowerCase();
  for(const term of ['segunda_rama','segunda rama','injerto','graft']) assert.equal(serialized.includes(term),false);
  assert.equal(GUO_CHEN_FORBIDDEN_AUTONOMOUS_CAPABILITY,'EXECUTE_SECOND_BRANCH_GRAFT');
});
T('cumplir_deber is too generic to encode irreversible semantics',()=>{
  const action=GOAP_ACTIONS.find(x=>x.id==='cumplir_deber');
  assert.ok(action);
  assert.deepEqual(action.effects,{dutyPending:false,dutySatisfied:true});
});
T('tests do not mutate canon or calibration profile',()=>{
  const c=JSON.stringify(GUO_CHEN_CANON),p=JSON.stringify(GUO_CHEN_UTILITY_PROFILE);
  tickAutonomousLoop(stateFor(GUO_CHEN_SCENARIOS.m16MaterialWork),1);
  tickAutonomousLoop(stateFor(GUO_CHEN_SCENARIOS.adversarialSecondBranchEncodedAsGenericDuty),1);
  assert.equal(JSON.stringify(GUO_CHEN_CANON),c);
  assert.equal(JSON.stringify(GUO_CHEN_UTILITY_PROFILE),p);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
