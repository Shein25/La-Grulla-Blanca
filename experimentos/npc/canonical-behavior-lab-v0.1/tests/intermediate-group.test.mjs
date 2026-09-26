import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRuntime as createFSM,stepFSM,validateMachine} from '../vendor/fsm-engine.mjs';
import {createRuntime as createBT,tickBehaviorTree,validateTree} from '../vendor/bt-engine.mjs';
import {
  SHEN_BAOJUN_FSM,SHEN_BAOJUN_ALLOWED,
  MADRE_WEN_FSM,MADRE_WEN_ALLOWED,
  TAO_MING_FSM,TAO_MING_ALLOWED,
  SU_LIAN_BT,SU_LIAN_ALLOWED,
  CHEN_BO_BT,CHEN_BO_ALLOWED,
  YAO_FEN_BT,YAO_FEN_ALLOWED,
  INTERMEDIATE_POLICY_STATUS
} from '../policies/intermediate-policies.mjs';
import {INTERMEDIATE_SCENARIOS as S} from '../scenarios/intermediate.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const NPC=data.npc_def;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function runFSM(machine,events){
  let rt=createFSM(machine),out=[];
  for(const e of events){const r=stepFSM(machine,rt,e);out.push(r);rt=r.nextRuntime;}
  return out;
}
function runBT(tree,ticks){
  let rt=createBT(tree),out=[];
  for(const t of ticks){const r=tickBehaviorTree(tree,rt,t);out.push(r);rt=r.nextRuntime;}
  return out;
}
function canonBasic(id){
  const c=NPC[id];
  assert.equal(c.id,id);
  assert.ok(c.posicion_valida.includes(c.sala_inicial));
  assert.equal(c.rutas.every(r=>r.every(x=>c.posicion_valida.includes(x))),true);
}
function whitelist(rows,allowed){
  const set=new Set(allowed);
  for(const r of rows) for(const i of r.emitted) assert.equal(set.has(i),true);
}

for(const id of ['shen_baojun','madre_wen','tao_ming','su_lian','chen_bo','yao_fen']){
  T(`${id}: canonical movement baseline valid`,()=>canonBasic(id));
}

T('all intermediate machines/trees validate',()=>{
  validateMachine(SHEN_BAOJUN_FSM);
  validateMachine(MADRE_WEN_FSM);
  validateMachine(TAO_MING_FSM);
  validateTree(SU_LIAN_BT);
  validateTree(CHEN_BO_BT);
  validateTree(YAO_FEN_BT);
});

T('Shen M03 training emits basic training intent',()=>assert.deepEqual(runFSM(SHEN_BAOJUN_FSM,S.shen_baojun.m03)[0].emitted,['TEACH_BASIC_TRAINING']));
T('Shen does not invent M16 role when source is unclosed',()=>assert.deepEqual(runFSM(SHEN_BAOJUN_FSM,S.shen_baojun.m16Unclosed)[0].emitted,[]));
T('Shen whitelist',()=>whitelist([...runFSM(SHEN_BAOJUN_FSM,S.shen_baojun.ordinary),...runFSM(SHEN_BAOJUN_FSM,S.shen_baojun.m03)],SHEN_BAOJUN_ALLOWED));

T('Madre Wen supports external continuity',()=>assert.deepEqual(runFSM(MADRE_WEN_FSM,S.madre_wen.ordinary)[0].emitted,['SUPPORT_EXTERNALS']));
T('Madre Wen M01 integration is explicit',()=>assert.deepEqual(runFSM(MADRE_WEN_FSM,S.madre_wen.m01)[0].emitted,['INTEGRATE_ASPIRANTS']));
T('Madre Wen does not invent formal M16 front',()=>assert.deepEqual(runFSM(MADRE_WEN_FSM,S.madre_wen.m16Unclosed)[0].emitted,[]));
T('Madre whitelist',()=>whitelist([...runFSM(MADRE_WEN_FSM,S.madre_wen.ordinary),...runFSM(MADRE_WEN_FSM,S.madre_wen.m01)],MADRE_WEN_ALLOWED));

T('Tao routine registers routine job',()=>assert.deepEqual(runFSM(TAO_MING_FSM,S.tao_ming.routine)[0].emitted,['REGISTER_ROUTINE_JOB']));
T('Tao M16 switches to emergency mode',()=>{
  const tr=runFSM(TAO_MING_FSM,S.tao_ming.crisis);
  assert.equal(tr[1].to,'EMERGENCY');
  assert.deepEqual(tr[1].emitted,['REGISTER_EMERGENCY']);
  assert.equal(tr[2].to,'EMERGENCY');
  assert.deepEqual(tr[2].emitted,['REGISTER_EMERGENCY']);
  assert.equal(tr[3].to,'ROUTINE');
  assert.deepEqual(tr[4].emitted,['REGISTER_ROUTINE_JOB']);
});
T('Tao whitelist',()=>whitelist(runFSM(TAO_MING_FSM,S.tao_ming.crisis),TAO_MING_ALLOWED));

T('Su tutorial emits TEACH_HERBALISM',()=>assert.deepEqual(runBT(SU_LIAN_BT,S.su_lian.tutorial)[0].emitted,['TEACH_HERBALISM']));
T('Su M16 garden crisis preempts tutorial',()=>{
  const tr=runBT(SU_LIAN_BT,S.su_lian.crisis);
  assert.equal(tr[1].preemptedAction,'teach_herbalism');
  assert.deepEqual(tr[1].emitted,['MANAGE_GARDEN_CRISIS']);
});
T('Su canon marks principal JARDINES front',()=>assert.ok(NPC.su_lian.territorio_por_etapa.M16.includes('responsable principal')));
T('Su whitelist',()=>whitelist(runBT(SU_LIAN_BT,S.su_lian.crisis),SU_LIAN_ALLOWED));

T('Chen exam emits RUN_SPIRITUAL_EXAM',()=>assert.deepEqual(runBT(CHEN_BO_BT,S.chen_bo.exam)[0].emitted,['RUN_SPIRITUAL_EXAM']));
T('Chen M16 prioritizes patients over exam',()=>{
  const tr=runBT(CHEN_BO_BT,S.chen_bo.crisis);
  assert.equal(tr[1].preemptedAction,'run_exam');
  assert.deepEqual(tr[1].emitted,['PRIORITIZE_PATIENTS']);
});
T('Chen canon says prioritizes patients in M16',()=>assert.ok(NPC.chen_bo.territorio_por_etapa.M16.includes('prioriza pacientes')));
T('Chen whitelist',()=>whitelist(runBT(CHEN_BO_BT,S.chen_bo.crisis),CHEN_BO_ALLOWED));

T('Yao lesson emits TEACH_ALCHEMY',()=>assert.deepEqual(runBT(YAO_FEN_BT,S.yao_fen.lesson)[0].emitted,['TEACH_ALCHEMY']));
T('Yao medicine crisis preempts alchemy lesson',()=>{
  const tr=runBT(YAO_FEN_BT,S.yao_fen.crisis);
  assert.equal(tr[1].preemptedAction,'teach_alchemy');
  assert.deepEqual(tr[1].emitted,['SUPPLY_MEDICINE']);
});
T('Yao canon marks co-responsible Medicina front',()=>assert.ok(NPC.yao_fen.territorio_por_etapa.M16.includes('Co-responsable')));
T('Yao whitelist',()=>whitelist(runBT(YAO_FEN_BT,S.yao_fen.crisis),YAO_FEN_ALLOWED));

T('policy statuses remain explicit',()=>{
  assert.equal(INTERMEDIATE_POLICY_STATUS.shen_baojun,'EXPERIMENTAL_MINIMAL_EVENT_FSM');
  assert.equal(INTERMEDIATE_POLICY_STATUS.madre_wen,'EXPERIMENTAL_MINIMAL_EVENT_FSM');
  assert.equal(INTERMEDIATE_POLICY_STATUS.tao_ming,'CANON_SUPPORTED_MODE_SWITCH_FSM');
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
