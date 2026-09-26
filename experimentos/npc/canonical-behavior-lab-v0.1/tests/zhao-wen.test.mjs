import assert from 'node:assert/strict';
import {evaluateDialogueTopic,validateNpc,validateDialogueContext} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {ZHAO_WEN_CANON,ZHAO_WEN_POLICY_STATUS,ZHAO_WEN_REQUIRED_ACCESS_CAPABILITY} from '../canonical/zhao-wen.mjs';
import {ZHAO_WEN_DIALOGUE_PROFILE} from '../profiles/zhao-wen-dialogue-profile.mjs';
import {ZHAO_WEN_DIALOGUE_SCENARIOS} from '../scenarios/zhao-wen.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('canon source is Zhao Wen',()=>assert.equal(ZHAO_WEN_CANON.id,'zhao_wen'));
T('canonical routes stay inside posicion_valida',()=>assert.equal(ZHAO_WEN_CANON.rutas.every(route=>route.every(x=>ZHAO_WEN_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(ZHAO_WEN_CANON.posicion_valida.includes(ZHAO_WEN_CANON.sala_inicial),true));
T('all canonical initial knowledge entries are DESCONOCIDO',()=>assert.equal(Object.values(ZHAO_WEN_CANON.conocimiento_inicial).every(x=>x==='DESCONOCIDO'),true));
T('Utility traits explicitly non-canonical',()=>assert.equal(ZHAO_WEN_POLICY_STATUS.utilityTraits,'EXPERIMENTAL_NON_CANONICAL'));
T('restricted archive access gap is explicit',()=>assert.equal(ZHAO_WEN_POLICY_STATUS.restrictedArchiveAccess,'CANONICAL_REQUIREMENT_CAPABILITY_GAP'));
T('dialogue profile validates',()=>assert.deepEqual(validateNpc(ZHAO_WEN_DIALOGUE_PROFILE),[]));

T('ordinary dialogue context validates',()=>assert.deepEqual(validateDialogueContext(ZHAO_WEN_DIALOGUE_SCENARIOS.ordinary.context),[]));
T('unknown R1 returns NO_SABE',()=>{
  const r=evaluateDialogueTopic(ZHAO_WEN_DIALOGUE_PROFILE,'R1',ZHAO_WEN_DIALOGUE_SCENARIOS.ordinary.context);
  assert.equal(r.state,'DESCONOCIDO');
  assert.equal(r.mode,'NO_SABE');
  assert.equal(r.disclosure,0);
});
T('unknown R2 and R3 also return NO_SABE',()=>{
  for(const topic of ['R2','R3']){
    const r=evaluateDialogueTopic(ZHAO_WEN_DIALOGUE_PROFILE,topic,ZHAO_WEN_DIALOGUE_SCENARIOS.ordinary.context);
    assert.equal(r.mode,'NO_SABE');
    assert.equal(r.disclosure,0);
  }
});
T('maximum social relation cannot reveal unknown knowledge',()=>{
  const npc=structuredClone(ZHAO_WEN_DIALOGUE_PROFILE);
  npc.relationPlayer={afinidad:100,confianza:100,respeto:100,deuda:100,temor:0,rivalidad:0};
  const r=evaluateDialogueTopic(npc,'R1',ZHAO_WEN_DIALOGUE_SCENARIOS.maxTrustStillUnknown.context);
  assert.equal(r.mode,'NO_SABE');
  assert.equal(r.disclosure,0);
});
T('higher player rank cannot reveal unknown knowledge',()=>{
  const r=evaluateDialogueTopic(ZHAO_WEN_DIALOGUE_PROFILE,'R1',ZHAO_WEN_DIALOGUE_SCENARIOS.maxTrustStillUnknown.context);
  assert.equal(r.mode,'NO_SABE');
  assert.equal(r.raw,0);
});
T('current GOAP vocabulary does not represent ARCHIVO_RESTRINGIDO permission',()=>{
  const serialized=JSON.stringify(GOAP_ACTIONS).toLowerCase();
  assert.equal(serialized.includes('archivo_restringido'),false);
  assert.equal(serialized.includes('restricted_archive'),false);
  assert.equal(ZHAO_WEN_REQUIRED_ACCESS_CAPABILITY,'ARCHIVO_RESTRINGIDO_PERMISSION');
});
T('tests do not mutate canonical profile',()=>{
  const before=JSON.stringify(ZHAO_WEN_CANON);
  evaluateDialogueTopic(ZHAO_WEN_DIALOGUE_PROFILE,'R1',ZHAO_WEN_DIALOGUE_SCENARIOS.ordinary.context);
  assert.equal(JSON.stringify(ZHAO_WEN_CANON),before);
});
T('tests do not mutate dialogue calibration profile',()=>{
  const before=JSON.stringify(ZHAO_WEN_DIALOGUE_PROFILE);
  evaluateDialogueTopic(ZHAO_WEN_DIALOGUE_PROFILE,'R1',ZHAO_WEN_DIALOGUE_SCENARIOS.maxTrustStillUnknown.context);
  assert.equal(JSON.stringify(ZHAO_WEN_DIALOGUE_PROFILE),before);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
