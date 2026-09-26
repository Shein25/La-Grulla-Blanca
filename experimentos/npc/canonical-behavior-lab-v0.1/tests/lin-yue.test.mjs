import assert from 'node:assert/strict';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {LIN_YUE_CANON,LIN_YUE_POLICY_STATUS,LIN_YUE_M16_REQUIRED_CAPABILITY} from '../canonical/lin-yue.mjs';
import {LIN_YUE_UTILITY_PROFILE} from '../profiles/lin-yue-utility-profile.mjs';
import {LIN_YUE_SCENARIOS,linContext,playerHelpedMemory} from '../scenarios/lin-yue.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const runtime=(state)=>state.npcs.find(x=>x.id==='lin_yue_lab');
const one=(result)=>result.dispatchResults[0];

function stateFor(scenario){
  const world=structuredClone(scenario.world);
  const utilityContext=linContext(world,scenario.contextOverrides);
  return createAutonomousLoopState({
    npcs:[{npc:structuredClone(LIN_YUE_UTILITY_PROFILE),world,utilityContext}],
    schedulerConfigs:[{id:'lin_yue_lab',interval:1,minGap:0,firstPeriodicTurn:1}]
  });
}

T('canon source is Lin Yue',()=>assert.equal(LIN_YUE_CANON.id,'lin_yue'));
T('both canonical routes stay inside posicion_valida',()=>assert.equal(LIN_YUE_CANON.rutas.every(route=>route.every(x=>LIN_YUE_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(LIN_YUE_CANON.posicion_valida.includes(LIN_YUE_CANON.sala_inicial),true));
T('Utility traits explicitly non-canonical',()=>assert.equal(LIN_YUE_POLICY_STATUS.utilityTraits,'EXPERIMENTAL_NON_CANONICAL'));
T('base relations explicitly non-canonical',()=>assert.equal(LIN_YUE_POLICY_STATUS.baseRelations,'EXPERIMENTAL_NON_CANONICAL'));
T('M16 route initiative is explicit physical capability gap',()=>assert.equal(LIN_YUE_POLICY_STATUS.m16RouteInitiative,'CANONICAL_REQUIREMENT_CAPABILITY_GAP_PHYSICAL_NAVIGATION'));
T('Utility profile validates',()=>assert.deepEqual(validateNpc(LIN_YUE_UTILITY_PROFILE),[]));

T('social baseline chooses conversation and creates no GOAP session',()=>{
  const first=tickAutonomousLoop(stateFor(LIN_YUE_SCENARIOS.socialBaseline),1);
  assert.equal(one(first).path,'DECISION');
  assert.equal(one(first).utilityAction,'hablar_jugador');
  assert.equal(one(first).status,'UTILITY_ACTION_UNMAPPED');
  assert.equal(one(first).goalId,null);
  assert.equal(runtime(first.state).executionSession,null);
  assert.deepEqual(one(first).derivedRelations,LIN_YUE_UTILITY_PROFILE.relationPlayer);
});

T('PLAYER_HELPED_ME is recorded and changes derived relations only through Memory/Relations',()=>{
  const initial=stateFor(LIN_YUE_SCENARIOS.socialAfterPlayerHelped);
  const rt=runtime(initial);
  const observation={
    npcId:rt.id,
    world:structuredClone(rt.world),
    utilityContext:structuredClone(rt.utilityContext),
    memoryEvents:[playerHelpedMemory(1)]
  };
  const withMemory=tickAutonomousLoop(initial,1,{observations:[observation]});
  assert.deepEqual(withMemory.generatedEvents.memoryChanged,['lin_yue_lab']);
  assert.deepEqual(one(withMemory).derivedRelations,{
    afinidad:52,
    confianza:50,
    respeto:50,
    deuda:8,
    temor:0,
    rivalidad:0
  });
  assert.deepEqual(runtime(withMemory.state).npc.relationPlayer,LIN_YUE_UTILITY_PROFILE.relationPlayer);
});

T('social memory flips decision from talk to help',()=>{
  const baseline=tickAutonomousLoop(stateFor(LIN_YUE_SCENARIOS.socialBaseline),1);
  const initial=stateFor(LIN_YUE_SCENARIOS.socialAfterPlayerHelped);
  const rt=runtime(initial);
  const observation={npcId:rt.id,world:structuredClone(rt.world),utilityContext:structuredClone(rt.utilityContext),memoryEvents:[playerHelpedMemory(1)]};
  const withMemory=tickAutonomousLoop(initial,1,{observations:[observation]});
  assert.equal(one(baseline).utilityAction,'hablar_jugador');
  assert.equal(one(withMemory).utilityAction,'ayudar_jugador');
  assert.equal(one(withMemory).goalId,'HELP_PLAYER');
  assert.equal(one(withMemory).status,'PLAN_SESSION_CREATED');
});

T('help decision creates a multi-step GOAP plan',()=>{
  const initial=stateFor(LIN_YUE_SCENARIOS.socialAfterPlayerHelped);
  const rt=runtime(initial);
  const observation={npcId:rt.id,world:structuredClone(rt.world),utilityContext:structuredClone(rt.utilityContext),memoryEvents:[playerHelpedMemory(1)]};
  const first=tickAutonomousLoop(initial,1,{observations:[observation]});
  assert.deepEqual(runtime(first.state).executionSession.plan,['ir_jugador','ayudar_jugador']);
});

T('help plan executes across later dispatches and reaches goal',()=>{
  const initial=stateFor(LIN_YUE_SCENARIOS.socialAfterPlayerHelped);
  const rt=runtime(initial);
  const observation={npcId:rt.id,world:structuredClone(rt.world),utilityContext:structuredClone(rt.utilityContext),memoryEvents:[playerHelpedMemory(1)]};
  const first=tickAutonomousLoop(initial,1,{observations:[observation]});
  const second=tickAutonomousLoop(first.state,2);
  const third=tickAutonomousLoop(second.state,3);
  assert.equal(one(second).path,'EXECUTION');
  assert.equal(one(second).executed,'ir_jugador');
  assert.equal(one(second).status,'STEP_APPLIED');
  assert.equal(one(third).path,'EXECUTION');
  assert.equal(one(third).executed,'ayudar_jugador');
  assert.equal(one(third).status,'GOAL_REACHED');
  assert.equal(runtime(third.state).world.playerHelped,true);
  assert.equal(runtime(third.state).executionSession,null);
});

T('current GOAP vocabulary cannot physically express canonical M16 route initiative',()=>{
  const serialized=JSON.stringify(GOAP_ACTIONS).toLowerCase();
  assert.equal(serialized.includes('patio_marcial'),false);
  assert.equal(serialized.includes('sala_formas'),false);
  assert.equal(serialized.includes('patio_campana'),false);
  assert.equal(serialized.includes('rutas'),false);
  assert.equal(LIN_YUE_M16_REQUIRED_CAPABILITY,'SELF_INITIATED_ROUTE_TRAVEL_TO_RUTAS');
});

T('tests do not mutate canonical profile',()=>{
  const before=JSON.stringify(LIN_YUE_CANON);
  tickAutonomousLoop(stateFor(LIN_YUE_SCENARIOS.socialBaseline),1);
  assert.equal(JSON.stringify(LIN_YUE_CANON),before);
});

T('tests do not mutate Utility calibration profile',()=>{
  const before=JSON.stringify(LIN_YUE_UTILITY_PROFILE);
  const initial=stateFor(LIN_YUE_SCENARIOS.socialAfterPlayerHelped);
  const rt=runtime(initial);
  const observation={npcId:rt.id,world:structuredClone(rt.world),utilityContext:structuredClone(rt.utilityContext),memoryEvents:[playerHelpedMemory(1)]};
  tickAutonomousLoop(initial,1,{observations:[observation]});
  assert.equal(JSON.stringify(LIN_YUE_UTILITY_PROFILE),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
