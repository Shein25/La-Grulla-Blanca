import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chooseMonsterIntent,STATUS} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {
  ADAPTER_STATUS,PROFILE_ASSIGNMENTS,HARNESS_DEFAULT_ASSIGNMENT,
  techniqueDue,techniqueWarning,canonicalAbilityIds,
  buildCanonicalAbilityCatalog,buildMonsterInput,
  baseCombat,neutralSocial,seededRng
} from '../adapter/canonical-combat-adapter.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const M=data.mobs;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function decide(mobId,round,{mode='CADENCE_COMPAT',memory=[],social=neutralSocial(),seed=1337,recentAbilityIds=[]}={}){
  const def=M[mobId];
  const abilities=buildCanonicalAbilityCatalog(mobId,def);
  const monster=buildMonsterInput({mobId,def,round,mode,recentAbilityIds});
  return chooseMonsterIntent({
    monster,profiles:PROFILES,abilities,
    combat:baseCombat(round),memory,social,rng:seededRng(seed)
  });
}

T('adapter is explicitly experimental',()=>assert.equal(ADAPTER_STATUS,'EXPERIMENTAL_NON_CANONICAL'));
T('default assignment is only harness fallback',()=>{
  assert.equal(HARNESS_DEFAULT_ASSIGNMENT.profileId,'INSTINTIVO');
  assert.equal(HARNESS_DEFAULT_ASSIGNMENT.socialProfileId,'SOLITARIO');
});

T('five representative assignments are explicit',()=>{
  assert.deepEqual(Object.keys(PROFILE_ASSIGNMENTS).sort(),[
    'devorador_niebla','lobo_espiritual','mantis_nube','rata_qi','serpiente_qi'
  ]);
});
T('representative cognitive ladder is wired 0..4',()=>{
  assert.equal(PROFILE_ASSIGNMENTS.rata_qi.profileId,'INSTINTIVO');
  assert.equal(PROFILE_ASSIGNMENTS.serpiente_qi.profileId,'REACTIVO_1');
  assert.equal(PROFILE_ASSIGNMENTS.lobo_espiritual.profileId,'CAZADOR_2');
  assert.equal(PROFILE_ASSIGNMENTS.devorador_niebla.profileId,'TACTICO_3');
  assert.equal(PROFILE_ASSIGNMENTS.mantis_nube.profileId,'MASTER_4');
});

T('all 19 canonical mobs build a cadence-compatible monster input',()=>{
  for(const [id,def] of Object.entries(M)){
    for(let round=0;round<=12;round++){
      const input=buildMonsterInput({mobId:id,def,round,mode:'CADENCE_COMPAT'});
      assert.equal(input.effectiveKit.length,1,id+':round '+round);
    }
  }
});

T('CADENCE_COMPAT selects basic or technique exactly by canonical cadence',()=>{
  for(const [id,def] of Object.entries(M)){
    const ids=canonicalAbilityIds(id);
    for(let round=0;round<=12;round++){
      const r=decide(id,round,{mode:'CADENCE_COMPAT',seed:round+1});
      assert.equal(r.status,STATUS.INTENT_SELECTED,id);
      const expected=def.tecnica&&techniqueDue(def,round)?ids.technique:ids.basic;
      assert.equal(r.abilityId,expected,id+':round '+round);
    }
  }
});

T('technique warning is exactly the preceding cadence round',()=>{
  for(const [id,def] of Object.entries(M)){
    if(!def.tecnica)continue;
    const cada=def.tecnica.cada;
    assert.equal(techniqueWarning(def,cada-1),true,id);
    assert.equal(techniqueDue(def,cada),true,id);
  }
});

T('three mobs without technique always expose only basic attack',()=>{
  const ids=Object.entries(M).filter(([,m])=>!m.tecnica).map(([id])=>id).sort();
  assert.deepEqual(ids,['eco_caido','muneco_practica','rata_qi']);
  for(const id of ids){
    const ability=canonicalAbilityIds(id).basic;
    for(const round of [0,1,2,3,7]) assert.equal(decide(id,round).abilityId,ability);
  }
});

T('poison canonical techniques map to CONTROL + VENENO tag',()=>{
  for(const id of ['serpiente_qi','avispa_jade','sombra_ahogada']){
    const a=buildCanonicalAbilityCatalog(id,M[id])[canonicalAbilityIds(id).technique];
    assert.equal(a.intentCategory,'CONTROL',id);
    assert.ok(a.tags.includes('VENENO'),id);
  }
});
T('burn canonical techniques map to CONTROL + QUEMADURA tag',()=>{
  for(const id of ['sapo_ceniza','sapo_caldera']){
    const a=buildCanonicalAbilityCatalog(id,M[id])[canonicalAbilityIds(id).technique];
    assert.equal(a.intentCategory,'CONTROL',id);
    assert.ok(a.tags.includes('QUEMADURA'),id);
  }
});
T('Qi-drain canonical techniques map to CONTROL + DRENA_QI tag',()=>{
  for(const id of ['mono_pildoras','anguila_estelar','guardian_coral']){
    const a=buildCanonicalAbilityCatalog(id,M[id])[canonicalAbilityIds(id).technique];
    assert.equal(a.intentCategory,'CONTROL',id);
    assert.ok(a.tags.includes('DRENA_QI'),id);
  }
});
T('pure damage canonical techniques remain OFENSIVA',()=>{
  for(const id of ['lobo_espiritual','pez_lunar','centinela_pluma','devorador_niebla','escarabajo_hierro','rey_escarabajo','halcon_tormenta','mantis_nube']){
    const a=buildCanonicalAbilityCatalog(id,M[id])[canonicalAbilityIds(id).technique];
    assert.equal(a.intentCategory,'OFENSIVA',id);
  }
});

T('representative DECISION_EXPERIMENTAL exposes both choices only on due rounds',()=>{
  for(const id of ['serpiente_qi','lobo_espiritual','devorador_niebla','mantis_nube']){
    const def=M[id], ids=canonicalAbilityIds(id), round=def.tecnica.cada;
    const input=buildMonsterInput({mobId:id,def,round,mode:'DECISION_EXPERIMENTAL'});
    assert.deepEqual(input.effectiveKit,[ids.basic,ids.technique],id);
  }
});
T('unassigned mob cannot silently enter DECISION_EXPERIMENTAL',()=>{
  assert.throws(()=>buildMonsterInput({
    mobId:'pez_lunar',def:M.pez_lunar,round:3,mode:'DECISION_EXPERIMENTAL'
  }),RangeError);
});

T('representative due-round experimental selection prefers canonical technique with current neutral weights',()=>{
  for(const id of ['serpiente_qi','lobo_espiritual','devorador_niebla','mantis_nube']){
    const r=decide(id,M[id].tecnica.cada,{mode:'DECISION_EXPERIMENTAL',seed:9});
    assert.equal(r.abilityId,canonicalAbilityIds(id).technique,id);
  }
});

T('cognitive memory windows are wired 0/1/2/3/4',()=>{
  const memory=Array.from({length:7},(_,i)=>({category:'RECUPERACION',result:'EFECTIVA',round:i}));
  const cases=[
    ['rata_qi',0,0],
    ['serpiente_qi',M.serpiente_qi.tecnica.cada,1],
    ['lobo_espiritual',M.lobo_espiritual.tecnica.cada,2],
    ['devorador_niebla',M.devorador_niebla.tecnica.cada,3],
    ['mantis_nube',M.mantis_nube.tecnica.cada,4]
  ];
  for(const [id,round,n] of cases){
    const r=decide(id,round,{mode:'DECISION_EXPERIMENTAL',memory,seed:3});
    assert.equal(r.debug.activeMemory.length,n,id);
  }
});

T('canonical adapter does not add memory/social weights by itself',()=>{
  for(const id of Object.keys(M)){
    const catalog=buildCanonicalAbilityCatalog(id,M[id]);
    for(const a of Object.values(catalog)){
      assert.deepEqual(a.utility.memoryWeights,{},id+':'+a.id);
      assert.deepEqual(a.utility.socialWeights,{},id+':'+a.id);
      assert.deepEqual(a.utility.signalWeights,{},id+':'+a.id);
    }
  }
});

T('decision is pure over canonical snapshot and adapter inputs',()=>{
  const def=structuredClone(M.mantis_nube);
  const before=JSON.stringify(def);
  const r=decide('mantis_nube',3,{mode:'DECISION_EXPERIMENTAL',seed:42});
  assert.equal(JSON.stringify(def),before);
  assert.ok(Object.isFrozen(r));
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
