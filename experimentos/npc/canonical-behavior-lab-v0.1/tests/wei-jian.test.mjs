import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRuntime,tickBehaviorTree,validateTree} from '../vendor/bt-engine.mjs';
import {ACTION_ORDER} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {WEI_JIAN_BT,WEI_JIAN_ALLOWED_INTENTS,WEI_JIAN_POLICY_STATUS} from '../policies/wei-jian-bt.mjs';
import {WEI_JIAN_SCENARIOS} from '../scenarios/wei-jian.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const CANON=data.npc_def.wei_jian;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};
const allowed=new Set(WEI_JIAN_ALLOWED_INTENTS);

function run(ticks){
  let rt=createRuntime(WEI_JIAN_BT),out=[];
  for(const t of ticks){
    const r=tickBehaviorTree(WEI_JIAN_BT,rt,t);
    out.push({intents:r.emitted,running:r.runningAction,preempted:r.preemptedAction,status:r.status});
    rt=r.nextRuntime;
  }
  return out;
}

T('canon is Wei Jian',()=>assert.equal(CANON.id,'wei_jian'));
T('canon role is martial authority',()=>assert.equal(CANON.rol,'Responsable marcial / Pabellón Marcial'));
T('canonical routes remain valid',()=>assert.equal(CANON.rutas.every(r=>r.every(x=>CANON.posicion_valida.includes(x))),true));
T('SECTA_INTERIOR gate remains canonical',()=>assert.deepEqual(CANON.gates_en_ruta,['SECTA_INTERIOR']));
T('M16 documents security/response',()=>assert.ok(CANON.territorio_por_etapa.M16.includes('Seguridad/respuesta')));
T('BT policy is explicitly experimental',()=>assert.equal(WEI_JIAN_POLICY_STATUS.behaviorTree,'EXPERIMENTAL_NON_CANONICAL'));
T('BT validates',()=>assert.doesNotThrow(()=>validateTree(WEI_JIAN_BT)));

for(const [name,s] of Object.entries(WEI_JIAN_SCENARIOS)){
  T(`${name}: intents stay in whitelist`,()=>{
    for(const row of run(s.ticks)) for(const intent of row.intents) assert.equal(allowed.has(intent),true);
  });
}

T('ordinary training selects SUPERVISE_TRAINING',()=>{
  assert.deepEqual(run(WEI_JIAN_SCENARIOS.training.ticks)[0].intents,['SUPERVISE_TRAINING']);
});
T('suspicion preempts training',()=>{
  const tr=run(WEI_JIAN_SCENARIOS.suspiciousDuringTraining.ticks);
  assert.equal(tr[1].preempted,'training');
  assert.deepEqual(tr[1].intents,['INVESTIGATE_MARTIAL_ANOMALY']);
});
T('security crisis preempts training over suspicion',()=>{
  const tr=run(WEI_JIAN_SCENARIOS.crisisDuringTraining.ticks);
  assert.equal(tr[1].preempted,'training');
  assert.deepEqual(tr[1].intents,['RESPOND_SECURITY']);
});
T('training can resume after terminal security response',()=>{
  const tr=run(WEI_JIAN_SCENARIOS.resumeAfterCrisis.ticks);
  assert.equal(tr[2].preempted,null);
  assert.deepEqual(tr[2].intents,['SUPERVISE_TRAINING']);
});
T('generic Utility vocabulary has no martial security response',()=>{
  assert.equal(ACTION_ORDER.includes('responder_seguridad'),false);
  assert.equal(ACTION_ORDER.includes('combatir'),false);
  assert.equal(ACTION_ORDER.includes('defender'),false);
});
T('BT does not encode canonical gate traversal',()=>{
  const serialized=JSON.stringify(WEI_JIAN_BT);
  assert.equal(serialized.includes('SECTA_INTERIOR'),false);
  assert.equal(WEI_JIAN_POLICY_STATUS.physicalNavigation,'CANONICAL_DOMAIN_CAPABILITY_GAP');
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
