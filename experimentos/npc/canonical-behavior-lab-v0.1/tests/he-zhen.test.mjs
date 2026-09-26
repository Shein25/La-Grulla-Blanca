import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {evaluateDialogueTopic,validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {HE_ZHEN_UTILITY_PROFILE} from '../profiles/he-zhen-utility-profile.mjs';
import {HE_ZHEN_SCENARIOS,heContext} from '../scenarios/he-zhen.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const CANON=data.npc_def.he_zhen;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};
const one=r=>r.dispatchResults[0],runtime=s=>s.npcs[0];
function stateFor(){const world=structuredClone(HE_ZHEN_SCENARIOS.m16Formations.world);return createAutonomousLoopState({npcs:[{npc:structuredClone(HE_ZHEN_UTILITY_PROFILE),world,utilityContext:heContext(world)}],schedulerConfigs:[{id:'he_zhen_lab',interval:1,minGap:0,firstPeriodicTurn:1}]});}

T('canon is He Zhen',()=>assert.equal(CANON.id,'he_zhen'));
T('routes valid',()=>assert.equal(CANON.rutas.every(r=>r.every(x=>CANON.posicion_valida.includes(x))),true));
T('M16 canon makes him principal Formaciones authority',()=>assert.ok(CANON.territorio_por_etapa.M16.includes('responsable principal')));
T('R2 and R7 are canonically SABE',()=>{assert.equal(CANON.conocimiento_inicial.R2,'SABE');assert.equal(CANON.conocimiento_inicial.R7,'SABE');});
T('current R1-R3 projection validates',()=>assert.deepEqual(validateNpc(HE_ZHEN_UTILITY_PROFILE),[]));
T('R2 can be evaluated as known',()=>{const r=evaluateDialogueTopic(HE_ZHEN_UTILITY_PROFILE,'R2',{playerRank:2,topicSensitivity:50,formalRestriction:55});assert.equal(r.state,'SABE');assert.notEqual(r.mode,'NO_SABE');});
T('adding canonical R7 is rejected',()=>{const n=structuredClone(HE_ZHEN_UTILITY_PROFILE);n.knowledge.R7='SABE';assert.ok(validateNpc(n).some(x=>x.includes('sobran R7')));});
T('M16 selects generic work goal',()=>{const r=tickAutonomousLoop(stateFor(),1);assert.equal(one(r).utilityAction,'trabajar');assert.equal(one(r).goalId,'FULFILL_DUTY');assert.deepEqual(runtime(r.state).executionSession.plan,['cumplir_deber']);});
T('generic formation duty reaches symbolic completion',()=>{const a=tickAutonomousLoop(stateFor(),1);const b=tickAutonomousLoop(a.state,2);assert.equal(one(b).status,'GOAL_REACHED');assert.equal(runtime(b.state).world.dutySatisfied,true);});
T('GOAP has no formation-network state',()=>{const s=JSON.stringify(GOAP_ACTIONS).toLowerCase();for(const x of ['formacion','formation','nodo','barrera','matriz','array'])assert.equal(s.includes(x),false);});
T('cumplir_deber remains boolean-only',()=>assert.deepEqual(GOAP_ACTIONS.find(x=>x.id==='cumplir_deber').effects,{dutyPending:false,dutySatisfied:true}));
console.log(`\nPASS: ${pass}`);console.log(`FAIL: ${fail}`);if(fail)process.exitCode=1;
