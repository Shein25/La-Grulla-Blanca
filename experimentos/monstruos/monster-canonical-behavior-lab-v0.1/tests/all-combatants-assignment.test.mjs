import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES,SOCIAL_PROFILES} from '../vendor/profiles.mjs';
import {CANDIDATE_ASSIGNMENTS,ASSIGNMENT_STATUS} from '../profiles/candidate-assignments.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,baseCombat,neutralSocial,seededRng} from '../adapter/canonical-combat-adapter.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const M=data.mobs;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function decide(id,round,{memory=[],social=neutralSocial(),seed=1}={}){
  const def=M[id];
  return chooseMonsterIntent({
    monster:buildCandidateMonsterInput({mobId:id,def,round,mode:'DECISION_EXPERIMENTAL'}),
    profiles:PROFILES,
    abilities:buildCanonicalAbilityCatalog(id,def),
    combat:baseCombat(round),
    memory,
    social,
    rng:seededRng(seed)
  });
}

T('assignment matrix is explicitly non-canonical',()=>assert.equal(ASSIGNMENT_STATUS,'EXPERIMENTAL_NON_CANONICAL'));
T('practice dummy has no candidate AI assignment',()=>assert.equal(Object.hasOwn(CANDIDATE_ASSIGNMENTS,'muneco_practica'),false));

T('all 18 combatants have exactly one candidate assignment',()=>{
  const combatants=Object.keys(M).filter(id=>id!=='muneco_practica').sort();
  assert.equal(combatants.length,18);
  assert.deepEqual(Object.keys(CANDIDATE_ASSIGNMENTS).sort(),combatants);
});

T('all cognitive profile ids exist',()=>{
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)) assert.ok(PROFILES[a.profileId],id);
});
T('all social profile ids exist',()=>{
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)) assert.ok(SOCIAL_PROFILES[a.socialProfileId],id);
});
T('every assignment has finite OFENSIVA/CONTROL preferences',()=>{
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)){
    assert.ok(Number.isFinite(a.preferences.OFENSIVA),id);
    assert.ok(Number.isFinite(a.preferences.CONTROL),id);
  }
});
T('candidate cognitive distribution remains 4/5/5/3/1',()=>{
  const c={};
  for(const a of Object.values(CANDIDATE_ASSIGNMENTS))c[a.profileId]=(c[a.profileId]||0)+1;
  assert.deepEqual(c,{INSTINTIVO:4,REACTIVO_1:5,CAZADOR_2:5,TACTICO_3:3,MASTER_4:1});
});

T('all 18 combatants enter DECISION_EXPERIMENTAL without contract error',()=>{
  for(const [id,def] of Object.entries(M)){
    if(id==='muneco_practica')continue;
    const round=def.tecnica?def.tecnica.cada:1;
    const r=decide(id,round,{seed:17});
    assert.equal(r.monsterId,id);
  }
});
T('practice dummy cannot enter candidate decision mode',()=>{
  assert.throws(()=>buildCandidateMonsterInput({mobId:'muneco_practica',def:M.muneco_practica,round:1}),RangeError);
});

T('all technique mobs expose basic + technique on due round',()=>{
  for(const [id,def] of Object.entries(M)){
    if(id==='muneco_practica'||!def.tecnica)continue;
    const input=buildCandidateMonsterInput({mobId:id,def,round:def.tecnica.cada,mode:'DECISION_EXPERIMENTAL'});
    const ids=canonicalAbilityIds(id);
    assert.deepEqual(input.effectiveKit,[ids.basic,ids.technique],id);
  }
});
T('non-technique combatants expose basic only',()=>{
  for(const id of ['rata_qi','eco_caido']){
    const x=buildCandidateMonsterInput({mobId:id,def:M[id],round:3,mode:'DECISION_EXPERIMENTAL'});
    assert.deepEqual(x.effectiveKit,[canonicalAbilityIds(id).basic],id);
  }
});

T('memory window matches each assigned cognitive profile depth',()=>{
  const memory=Array.from({length:8},(_,i)=>({category:'RECUPERACION',result:'EFECTIVA',round:i}));
  for(const [id,a] of Object.entries(CANDIDATE_ASSIGNMENTS)){
    const def=M[id],round=def.tecnica?def.tecnica.cada:1;
    const r=decide(id,round,{memory,seed:21});
    const p=PROFILES[a.profileId];
    assert.equal(r.debug.activeMemory.length,p.usesMemory?Math.min(p.memoryDepth,memory.length):0,id);
  }
});

T('memory currently does not change canonical ability scores',()=>{
  const id='guardian_coral',def=M[id],round=def.tecnica.cada;
  const empty=decide(id,round,{memory:[],seed:88});
  const memory=[
    {category:'RECUPERACION',result:'EFECTIVA',round:1},
    {category:'DEFENSA_ABSORCION',result:'FALLIDA',round:2},
    {category:'RECUPERACION',result:'EFECTIVA',round:3}
  ];
  const withMemory=decide(id,round,{memory,seed:88});
  assert.deepEqual(empty.debug.scoreByAbility,withMemory.debug.scoreByAbility);
  assert.notEqual(withMemory.debug.activeMemory.length,0);
});

T('social context currently does not change canonical ability scores',()=>{
  const id='lobo_espiritual',def=M[id],round=def.tecnica.cada;
  const alone=decide(id,round,{social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false},seed:99});
  const pack=decide(id,round,{social:{alliesAlive:3,sameSpeciesAllies:3,outnumbersPlayer:true},seed:99});
  assert.deepEqual(alone.debug.scoreByAbility,pack.debug.scoreByAbility);
});

T('same input and seed stays deterministic for all 18 assignments',()=>{
  for(const [id,def] of Object.entries(M)){
    if(id==='muneco_practica')continue;
    const round=def.tecnica?def.tecnica.cada:1;
    const a=decide(id,round,{seed:20260925});
    const b=decide(id,round,{seed:20260925});
    assert.deepEqual(a,b,id);
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
