import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRuntime as createFSM,stepFSM,validateMachine} from '../vendor/fsm-engine.mjs';
import {createRuntime as createBT,tickBehaviorTree,validateTree} from '../vendor/bt-engine.mjs';
import * as P from '../policies/functional-policies.mjs';
import {FUNCTIONAL_SCENARIOS as S} from '../scenarios/functional.scenarios.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/NPC_DEF_ver74.snapshot.json',import.meta.url),'utf8'));
const NPC=data.npc_def;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function runF(m,evs){let rt=createFSM(m),out=[];for(const e of evs){const r=stepFSM(m,rt,e);out.push(r);rt=r.nextRuntime;}return out;}
function runB(t,ticks){let rt=createBT(t),out=[];for(const x of ticks){const r=tickBehaviorTree(t,rt,x);out.push(r);rt=r.nextRuntime;}return out;}
function canonBasic(id){const c=NPC[id];assert.equal(c.id,id);assert.ok(c.posicion_valida.includes(c.sala_inicial));assert.equal(c.rutas.every(r=>r.every(x=>c.posicion_valida.includes(x))),true);}
function white(rows,arr){const set=new Set(arr);for(const r of rows)for(const i of r.emitted)assert.equal(set.has(i),true);}

for(const id of ['feng_zhi','ma_qiren','lu_cheng','ning_cai','wen_tao','yu_shun','ma_gu','ren_bo','xu_an','mei_shufen']){
  T(`${id}: canonical baseline valid`,()=>canonBasic(id));
}

T('all functional machines/trees validate',()=>{
  validateMachine(P.FENG_ZHI_FSM);validateTree(P.MA_QIREN_BT);validateMachine(P.LU_CHENG_FSM);validateMachine(P.NING_CAI_FSM);
  validateTree(P.WEN_TAO_BT);validateMachine(P.YU_SHUN_FSM);validateMachine(P.MA_GU_FSM);validateTree(P.REN_BO_BT);
  validateTree(P.XU_AN_BT);validateMachine(P.MEI_SHUFEN_FSM);
});

T('Feng supports Discipline routinely',()=>assert.deepEqual(runF(P.FENG_ZHI_FSM,S.feng_zhi.ordinary)[0].emitted,['SUPPORT_DISCIPLINE']));
T('Feng does not invent M16 role',()=>assert.deepEqual(runF(P.FENG_ZHI_FSM,S.feng_zhi.m16Unclosed)[0].emitted,[]));
T('Feng whitelist',()=>white(runF(P.FENG_ZHI_FSM,S.feng_zhi.ordinary),P.FENG_ZHI_ALLOWED));

T('Ma Qiren routine manages stock',()=>assert.deepEqual(runB(P.MA_QIREN_BT,S.ma_qiren.routine)[0].emitted,['MANAGE_STOCK']));
T('Ma Qiren crisis preempts stock work',()=>{const tr=runB(P.MA_QIREN_BT,S.ma_qiren.crisis);assert.equal(tr[1].preemptedAction,'manage_stock');assert.deepEqual(tr[1].emitted,['DISTRIBUTE_SUPPLIES']);});
T('Ma Qiren canon says distributes supplies',()=>assert.ok(NPC.ma_qiren.territorio_por_etapa.M16.includes('Distribuye suministros')));
T('Ma Qiren whitelist',()=>white(runB(P.MA_QIREN_BT,S.ma_qiren.crisis),P.MA_QIREN_ALLOWED));

T('Lu Cheng is canonically anchored',()=>assert.equal(NPC.lu_cheng.movilidad,'ANCLADO'));
T('Lu Cheng emergency repair intent',()=>assert.deepEqual(runF(P.LU_CHENG_FSM,S.lu_cheng.crisis)[0].emitted,['REPAIR_EMERGENCY_EQUIPMENT']));
T('Lu Cheng policy has no movement',()=>assert.equal(/MOVE|PATROL|ROUTE/.test(JSON.stringify(P.LU_CHENG_FSM)),false));
T('Lu Cheng whitelist',()=>white([...runF(P.LU_CHENG_FSM,S.lu_cheng.ordinary),...runF(P.LU_CHENG_FSM,S.lu_cheng.crisis)],P.LU_CHENG_ALLOWED));

T('Ning Cai is canonically anchored',()=>assert.equal(NPC.ning_cai.movilidad,'ANCLADO'));
T('Ning Cai emergency production intent',()=>assert.deepEqual(runF(P.NING_CAI_FSM,S.ning_cai.crisis)[0].emitted,['PRODUCE_EMERGENCY_PROTECTIONS']));
T('Ning Cai policy has no movement',()=>assert.equal(/MOVE|PATROL|ROUTE/.test(JSON.stringify(P.NING_CAI_FSM)),false));
T('Ning Cai whitelist',()=>white([...runF(P.NING_CAI_FSM,S.ning_cai.ordinary),...runF(P.NING_CAI_FSM,S.ning_cai.crisis)],P.NING_CAI_ALLOWED));

T('Wen Tao routine repairs formation component',()=>assert.deepEqual(runB(P.WEN_TAO_BT,S.wen_tao.routine)[0].emitted,['REPAIR_FORMATION_COMPONENT']));
T('Wen Tao critical node preempts routine repair',()=>{const tr=runB(P.WEN_TAO_BT,S.wen_tao.crisis);assert.equal(tr[1].preemptedAction,'repair');assert.deepEqual(tr[1].emitted,['STABILIZE_CRITICAL_NODE']);});
T('Wen Tao canon says critical node in M16',()=>assert.ok(NPC.wen_tao.territorio_por_etapa.M16.includes('nodo crítico')));
T('Wen Tao whitelist',()=>white(runB(P.WEN_TAO_BT,S.wen_tao.crisis),P.WEN_TAO_ALLOWED));

T('Yu Shun M09 copies/restores records',()=>assert.deepEqual(runF(P.YU_SHUN_FSM,S.yu_shun.m09)[0].emitted,['COPY_RESTORE_RECORDS']));
T('Yu Shun does not invent M16 role',()=>assert.deepEqual(runF(P.YU_SHUN_FSM,S.yu_shun.m16Unclosed)[0].emitted,[]));
T('Yu Shun whitelist',()=>white([...runF(P.YU_SHUN_FSM,S.yu_shun.ordinary),...runF(P.YU_SHUN_FSM,S.yu_shun.m09)],P.YU_SHUN_ALLOWED));

T('Ma Gu routine supervises quarry',()=>assert.deepEqual(runF(P.MA_GU_FSM,S.ma_gu.ordinary)[0].emitted,['SUPERVISE_QUARRY']));
T('Ma Gu M16 supports Resource front',()=>assert.deepEqual(runF(P.MA_GU_FSM,S.ma_gu.crisis)[0].emitted,['SUPPORT_RESOURCE_FRONT']));
T('Ma Gu canon says quarry is not separate front',()=>assert.ok(NPC.ma_gu.territorio_por_etapa.M16.includes('no un frente separado')));
T('Ma Gu whitelist',()=>white([...runF(P.MA_GU_FSM,S.ma_gu.ordinary),...runF(P.MA_GU_FSM,S.ma_gu.crisis)],P.MA_GU_ALLOWED));

T('Ren Bo patrol intent',()=>assert.deepEqual(runB(P.REN_BO_BT,S.ren_bo.patrol)[0].emitted,['PATROL_ROUTES']));
T('Ren Bo crisis preempts patrol',()=>{const tr=runB(P.REN_BO_BT,S.ren_bo.crisis);assert.equal(tr[1].preemptedAction,'patrol');assert.deepEqual(tr[1].emitted,['SECURE_ROUTES']);});
T('Ren Bo canon co-responsible RUTAS',()=>assert.ok(NPC.ren_bo.territorio_por_etapa.M16.includes('co-responsable')));
T('Ren Bo whitelist',()=>white(runB(P.REN_BO_BT,S.ren_bo.crisis),P.REN_BO_ALLOWED));

T('Xu An community representation intent',()=>assert.deepEqual(runB(P.XU_AN_BT,S.xu_an.community)[0].emitted,['REPRESENT_SAUCES']));
T('Xu An crisis preempts community routine',()=>{const tr=runB(P.XU_AN_BT,S.xu_an.crisis);assert.equal(tr[1].preemptedAction,'represent');assert.deepEqual(tr[1].emitted,['COORDINATE_SAUCES']);});
T('Xu An canon principal SAUCES',()=>assert.ok(NPC.xu_an.territorio_por_etapa.M16.includes('responsable principal')));
T('Xu An whitelist',()=>white(runB(P.XU_AN_BT,S.xu_an.crisis),P.XU_AN_ALLOWED));

T('Mei Shufen ordinary herbalist intent',()=>assert.deepEqual(runF(P.MEI_SHUFEN_FSM,S.mei_shufen.ordinary)[0].emitted,['TEND_LOCAL_HERBS']));
T('Mei Shufen supports Sauces during crisis',()=>assert.deepEqual(runF(P.MEI_SHUFEN_FSM,S.mei_shufen.crisis)[0].emitted,['SUPPORT_SAUCES_HERBALIST']));
T('Mei Shufen damaged outcome continues support rather than death',()=>assert.deepEqual(runF(P.MEI_SHUFEN_FSM,S.mei_shufen.damaged)[0].emitted,['CONTINUE_SUPPORT_AFTER_DAMAGE']));
T('Mei Shufen canon explicitly forbids automatic death',()=>assert.ok(NPC.mei_shufen.territorio_por_etapa.M16.includes('no destruye el asentamiento ni mata')));
T('Mei Shufen policy contains no death/destruction intent',()=>{const s=JSON.stringify(P.MEI_SHUFEN_FSM).toLowerCase();for(const x of ['death','die','kill','matar','morir','destroy','destruir'])assert.equal(s.includes(x),false);});
T('Mei Shufen whitelist',()=>white([...runF(P.MEI_SHUFEN_FSM,S.mei_shufen.ordinary),...runF(P.MEI_SHUFEN_FSM,S.mei_shufen.crisis),...runF(P.MEI_SHUFEN_FSM,S.mei_shufen.damaged)],P.MEI_SHUFEN_ALLOWED));

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
