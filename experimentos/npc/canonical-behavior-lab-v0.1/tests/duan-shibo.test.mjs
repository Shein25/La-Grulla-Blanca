import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createAutonomousLoopState,tickAutonomousLoop} from '../../integraciones/npc-autonomous-loop-v0.1/autonomous-loop.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {validateNpc} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {DUAN_SHIBO_UTILITY_PROFILE} from '../profiles/duan-shibo-utility-profile.mjs';
import {DUAN_SHIBO_SCENARIOS,duanContext} from '../scenarios/duan-shibo.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const CANON=data.npc_def.duan_shibo;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};
const one=r=>r.dispatchResults[0],runtime=s=>s.npcs[0];
function stateFor(){const world=structuredClone(DUAN_SHIBO_SCENARIOS.m16Resources.world);return createAutonomousLoopState({npcs:[{npc:structuredClone(DUAN_SHIBO_UTILITY_PROFILE),world,utilityContext:duanContext(world)}],schedulerConfigs:[{id:'duan_shibo_lab',interval:1,minGap:0,firstPeriodicTurn:1}]});}

T('canon is Duan Shibo',()=>assert.equal(CANON.id,'duan_shibo'));
T('routes valid',()=>assert.equal(CANON.rutas.every(r=>r.every(x=>CANON.posicion_valida.includes(x))),true));
T('M16 canon makes him principal Recursos authority',()=>assert.ok(CANON.territorio_por_etapa.M16.includes('responsable principal')));
T('canonical R6 is SOSPECHA',()=>assert.equal(CANON.conocimiento_inicial.R6,'SOSPECHA'));
T('current projection validates',()=>assert.deepEqual(validateNpc(DUAN_SHIBO_UTILITY_PROFILE),[]));
T('adding R6 is rejected by current schema',()=>{const n=structuredClone(DUAN_SHIBO_UTILITY_PROFILE);n.knowledge.R6='SOSPECHA';assert.ok(validateNpc(n).some(x=>x.includes('sobran R6')));});
T('M16 selects generic work goal',()=>{const r=tickAutonomousLoop(stateFor(),1);assert.equal(one(r).utilityAction,'trabajar');assert.equal(one(r).goalId,'FULFILL_DUTY');assert.deepEqual(runtime(r.state).executionSession.plan,['cumplir_deber']);});
T('generic resource duty reaches symbolic completion',()=>{const a=tickAutonomousLoop(stateFor(),1);const b=tickAutonomousLoop(a.state,2);assert.equal(one(b).status,'GOAL_REACHED');assert.equal(runtime(b.state).world.dutySatisfied,true);});
T('GOAP has no concrete resource allocation state',()=>{const s=JSON.stringify(GOAP_ACTIONS).toLowerCase();for(const x of ['inventory','inventario','recurso','carro','stock','supply'])assert.equal(s.includes(x),false);});
T('cumplir_deber is boolean-only',()=>assert.deepEqual(GOAP_ACTIONS.find(x=>x.id==='cumplir_deber').effects,{dutyPending:false,dutySatisfied:true}));
console.log(`\nPASS: ${pass}`);console.log(`FAIL: ${fail}`);if(fail)process.exitCode=1;
