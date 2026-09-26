import assert from 'node:assert/strict';
import {chooseAction,evaluateDialogueTopic,validateNpc,validateDialogueContext} from '../../utility-ai/motor-npc-vivo-v0.1.1/engine.mjs';
import {GOAP_ACTIONS} from '../../goap/motor-npc-vivo-v0.2-goap/actions.mjs';
import {LUO_YAN_CANON,LUO_YAN_POLICY_STATUS,LUO_YAN_REQUIRED_CAPABILITIES} from '../canonical/luo-yan.mjs';
import {LUO_YAN_UTILITY_PROFILE} from '../profiles/luo-yan-utility-profile.mjs';
import {LUO_YAN_SCENARIOS} from '../scenarios/luo-yan.scenarios.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('canon source is Luo Yan',()=>assert.equal(LUO_YAN_CANON.id,'luo_yan'));
T('canonical routes stay inside posicion_valida',()=>assert.equal(LUO_YAN_CANON.rutas.every(route=>route.every(x=>LUO_YAN_CANON.posicion_valida.includes(x))),true));
T('canonical initial room is valid',()=>assert.equal(LUO_YAN_CANON.posicion_valida.includes(LUO_YAN_CANON.sala_inicial),true));
T('canonical R1 is SOSPECHA',()=>assert.equal(LUO_YAN_CANON.conocimiento_inicial.R1,'SOSPECHA'));
T('canonical R5 is SABE',()=>assert.equal(LUO_YAN_CANON.conocimiento_inicial.R5,'SABE'));
T('Utility profile validates with current R1-R3 schema',()=>assert.deepEqual(validateNpc(LUO_YAN_UTILITY_PROFILE),[]));

T('adding canonical R5 is rejected by current Utility schema',()=>{
  const npc=structuredClone(LUO_YAN_UTILITY_PROFILE);
  npc.knowledge.R5='SABE';
  const errors=validateNpc(npc);
  assert.ok(errors.some(x=>x.includes('sobran R5')));
});
T('dialogue engine cannot query canonical R5 yet',()=>{
  assert.throws(
    ()=>evaluateDialogueTopic(LUO_YAN_UTILITY_PROFILE,'R5',LUO_YAN_SCENARIOS.r1Dialogue.dialogueContext),
    /Tema no definido/
  );
});
T('R1 dialogue context validates',()=>assert.deepEqual(validateDialogueContext(LUO_YAN_SCENARIOS.r1Dialogue.dialogueContext),[]));
T('R1 suspicion is represented without fabricating certainty',()=>{
  const r=evaluateDialogueTopic(LUO_YAN_UTILITY_PROFILE,'R1',LUO_YAN_SCENARIOS.r1Dialogue.dialogueContext);
  assert.equal(r.state,'SOSPECHA');
  assert.equal(r.mode,'RESERVA');
  assert.ok(r.disclosure>0 && r.disclosure<42);
});

T('epilogue outcome is marked as domain capability gap',()=>assert.equal(LUO_YAN_POLICY_STATUS.epilogueChoice,'CANONICAL_DOMAIN_CAPABILITY_GAP'));
T('GOAP vocabulary has no LIBERAR/CUSTODIAR action semantics',()=>{
  const serialized=JSON.stringify(GOAP_ACTIONS).toLowerCase();
  assert.equal(serialized.includes('liberar'),false);
  assert.equal(serialized.includes('custodiar'),false);
});
T('raw Utility ignores LIBERAR versus CUSTODIAR because outcome is not part of scoring model',()=>{
  const base={
    playerPresent:false,playerRequestsHelp:false,playerRank:1,
    dutyImportance:80,danger:25,missionUrgency:40,
    anomalyPresent:false,awayFromPost:false,superiorReachable:false,
    relevantKnowledge:'SOSPECHA',dutyMode:'trabajar'
  };
  const liberar=chooseAction(LUO_YAN_UTILITY_PROFILE,{...base,epilogueOutcome:'LIBERAR'});
  const custodiar=chooseAction(LUO_YAN_UTILITY_PROFILE,{...base,epilogueOutcome:'CUSTODIAR'});
  assert.equal(liberar.action,custodiar.action);
  assert.equal(liberar.score,custodiar.score);
  assert.deepEqual(LUO_YAN_REQUIRED_CAPABILITIES,{
    knowledge:'KNOWLEDGE_SCHEMA_R1_TO_R10',
    epilogue:'LIBERAR_CUSTODIAR_DOMAIN_OUTCOME'
  });
});
T('tests do not mutate canon or calibration profile',()=>{
  const c=JSON.stringify(LUO_YAN_CANON),p=JSON.stringify(LUO_YAN_UTILITY_PROFILE);
  evaluateDialogueTopic(LUO_YAN_UTILITY_PROFILE,'R1',LUO_YAN_SCENARIOS.r1Dialogue.dialogueContext);
  assert.equal(JSON.stringify(LUO_YAN_CANON),c);
  assert.equal(JSON.stringify(LUO_YAN_UTILITY_PROFILE),p);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
