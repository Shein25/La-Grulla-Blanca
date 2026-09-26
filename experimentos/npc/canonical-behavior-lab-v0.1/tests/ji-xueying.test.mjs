import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRuntime,stepFSM,validateMachine} from '../vendor/fsm-engine.mjs';
import {JI_XUEYING_FSM,JI_XUEYING_ALLOWED_INTENTS,JI_XUEYING_POLICY_STATUS} from '../policies/ji-xueying-fsm.mjs';
import {JI_XUEYING_SCENARIOS} from '../scenarios/ji-xueying.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const CANON=data.npc_def.ji_xueying;

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};
const allowed=new Set(JI_XUEYING_ALLOWED_INTENTS);
function run(events){
  let rt=createRuntime(JI_XUEYING_FSM),out=[];
  for(const e of events){
    const r=stepFSM(JI_XUEYING_FSM,rt,e);
    out.push({state:r.to,intents:r.emitted,transitioned:r.transitioned});
    rt=r.nextRuntime;
  }
  return out;
}

T('canon is Ji Xueying',()=>assert.equal(CANON.id,'ji_xueying'));
T('canon movement is ANCLADO',()=>assert.equal(CANON.movilidad,'ANCLADO'));
T('canon has exactly one valid room',()=>assert.deepEqual(CANON.posicion_valida,['interior_sala_consejo']));
T('canon has no routes',()=>assert.deepEqual(CANON.rutas,[]));
T('canon explicitly says she should not roam',()=>assert.ok(CANON.territorio_por_etapa.LI.includes('no debe aparecer paseando')));
T('M17 canon says she presides Council',()=>assert.ok(CANON.territorio_por_etapa.M17.includes('preside')));
T('minimal FSM validates',()=>assert.doesNotThrow(()=>validateMachine(JI_XUEYING_FSM)));
T('architecture is explicitly experimental',()=>assert.equal(JI_XUEYING_POLICY_STATUS.architecture,'EXPERIMENTAL_MINIMAL_EVENT_FSM'));

T('ordinary ticks only hold Council position',()=>{
  const tr=run(JI_XUEYING_SCENARIOS.ordinary);
  assert.equal(tr.every(x=>x.state==='COUNCIL'),true);
  assert.deepEqual(tr.flatMap(x=>x.intents),['HOLD_COUNCIL_POSITION','HOLD_COUNCIL_POSITION','HOLD_COUNCIL_POSITION']);
});
T('M17 emits PRESIDE_COUNCIL without changing state',()=>{
  const tr=run(JI_XUEYING_SCENARIOS.m17);
  assert.equal(tr.every(x=>x.state==='COUNCIL'),true);
  assert.deepEqual(tr[1].intents,['PRESIDE_COUNCIL']);
});
T('unknown event does not invent behavior or movement',()=>{
  const tr=run(JI_XUEYING_SCENARIOS.unknownEvent);
  assert.equal(tr[0].state,'COUNCIL');
  assert.deepEqual(tr[0].intents,[]);
});
T('all emitted intents stay inside whitelist',()=>{
  for(const s of Object.values(JI_XUEYING_SCENARIOS)) for(const row of run(s)) for(const i of row.intents) assert.equal(allowed.has(i),true);
});
T('policy contains no movement intent',()=>{
  const serialized=JSON.stringify(JI_XUEYING_FSM).toLowerCase();
  for(const x of ['move','patrol','return_post','route','caminar','mover']) assert.equal(serialized.includes(x),false);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
