import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,baseCombat,seededRng} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay,TACTICAL_OVERLAY_STATUS} from '../tactics/tactical-overlay-v0.1.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const M=data.mobs;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function decide(id,round,{memory=[],social={alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false},signals={},seed=1,recentAbilityIds=[],mode='DECISION_EXPERIMENTAL'}={}){
  const def=M[id];
  const base=buildCanonicalAbilityCatalog(id,def);
  const abilities=applyTacticalOverlay(id,base);
  const monster=buildCandidateMonsterInput({mobId:id,def,round,mode,recentAbilityIds});
  return chooseMonsterIntent({
    monster,profiles:PROFILES,abilities,
    combat:baseCombat(round,{signals}),memory,social,rng:seededRng(seed)
  });
}

T('overlay status is explicit',()=>assert.equal(TACTICAL_OVERLAY_STATUS,'EXPERIMENTAL_NON_CANONICAL_REUSE_AUDITED_WEIGHTS'));

T('overlay does not mutate canonical ability catalog',()=>{
  const base=buildCanonicalAbilityCatalog('guardian_coral',M.guardian_coral);
  const before=JSON.stringify(base);
  applyTacticalOverlay('guardian_coral',base);
  assert.equal(JSON.stringify(base),before);
});

T('basic offensive reuses PLAYER_LOW_HP +5',()=>{
  const id='lobo_espiritual';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).basic];
  assert.deepEqual(a.utility.signalWeights,{PLAYER_LOW_HP:5});
});

T('offensive technique reuses PLAYER_LOW_HP +6',()=>{
  const id='lobo_espiritual';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.signalWeights,{PLAYER_LOW_HP:6});
});

T('control technique reuses DEFENSA_ABSORCION -8 memory weight',()=>{
  const id='guardian_coral';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.memoryWeights,{DEFENSA_ABSORCION:-8});
});

T('MANADA technique receives conservative MANADA_WITH_ALLY +5',()=>{
  const id='lobo_espiritual';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.socialWeights,{MANADA_WITH_ALLY:5});
});

T('OPORTUNISTA technique reuses OPORTUNISTA_LOW_HP +15',()=>{
  const id='mono_pildoras';
  const a=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,M[id]))[canonicalAbilityIds(id).technique];
  assert.deepEqual(a.utility.socialWeights,{OPORTUNISTA_LOW_HP:15});
});

T('INSTINTIVO still ignores memory even when control technique has memory weight',()=>{
  const id='sapo_ceniza',round=M[id].tecnica.cada;
  const mem=Array.from({length:4},(_,i)=>({category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:i}));
  const a=decide(id,round,{memory:[],seed:7});
  const b=decide(id,round,{memory:mem,seed:7});
  assert.equal(b.debug.activeMemory.length,0);
  assert.deepEqual(a.debug.scoreByAbility,b.debug.scoreByAbility);
});

T('REACTIVO_1 sees only last memory and keeps poison technique attractive',()=>{
  const id='serpiente_qi',round=M[id].tecnica.cada;
  const mem=Array.from({length:3},(_,i)=>({category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:i}));
  const r=decide(id,round,{memory:mem,signals:{PLAYER_LOW_HP:1},seed:11});
  assert.equal(r.debug.activeMemory.length,1);
  assert.equal(r.abilityId,canonicalAbilityIds(id).technique);
});

T('TACTICO_3 can abandon repeatedly ineffective control technique',()=>{
  const id='guardian_coral',round=M[id].tecnica.cada;
  const none=decide(id,round,{memory:[],signals:{PLAYER_LOW_HP:1},seed:88});
  const mem=Array.from({length:3},(_,i)=>({category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:i}));
  const adapted=decide(id,round,{memory:mem,signals:{PLAYER_LOW_HP:1},seed:88});
  assert.equal(none.abilityId,canonicalAbilityIds(id).technique);
  assert.equal(adapted.debug.activeMemory.length,3);
  assert.equal(adapted.abilityId,canonicalAbilityIds(id).basic);
});

T('MANADA social flag can flip repeated lobo technique back into use',()=>{
  const id='lobo_espiritual',round=M[id].tecnica.cada,tech=canonicalAbilityIds(id).technique;
  const recent=[tech,tech,tech];
  const alone=decide(id,round,{signals:{PLAYER_LOW_HP:1},recentAbilityIds:recent,seed:42,social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false}});
  const pack=decide(id,round,{signals:{PLAYER_LOW_HP:1,ALLY_PRESENT:1},recentAbilityIds:recent,seed:42,social:{alliesAlive:2,sameSpeciesAllies:2,outnumbersPlayer:true}});
  assert.equal(alone.abilityId,canonicalAbilityIds(id).basic);
  assert.equal(pack.abilityId,tech);
});

T('OPORTUNISTA low-player state can flip repeated drain technique into use',()=>{
  const id='mono_pildoras',round=M[id].tecnica.cada,tech=canonicalAbilityIds(id).technique;
  const recent=[tech,tech,tech,tech];
  const normal=decide(id,round,{signals:{PLAYER_LOW_HP:0},recentAbilityIds:recent,seed:33,social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false}});
  const low=decide(id,round,{signals:{PLAYER_LOW_HP:1},recentAbilityIds:recent,seed:33,social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false}});
  assert.equal(normal.abilityId,canonicalAbilityIds(id).basic);
  assert.equal(low.abilityId,tech);
});

T('CADENCE_COMPAT remains authoritative despite tactical overlay',()=>{
  for(const id of ['serpiente_qi','lobo_espiritual','guardian_coral','mono_pildoras','mantis_nube']){
    const def=M[id], ids=canonicalAbilityIds(id);
    for(let round=1;round<=def.tecnica.cada;round++){
      const r=decide(id,round,{
        mode:'CADENCE_COMPAT',
        memory:Array.from({length:4},(_,i)=>({category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:i})),
        social:{alliesAlive:4,sameSpeciesAllies:4,outnumbersPlayer:true},
        signals:{PLAYER_LOW_HP:1,ALLY_PRESENT:1,OUTNUMBER_PLAYER:1},
        recentAbilityIds:[ids.technique,ids.technique,ids.technique,ids.technique],
        seed:100+round
      });
      const expected=round%def.tecnica.cada===0?ids.technique:ids.basic;
      assert.equal(r.abilityId,expected,id+':'+round);
    }
  }
});

T('same tactical input and seed stays deterministic',()=>{
  const id='guardian_coral',round=M[id].tecnica.cada;
  const opts={
    memory:Array.from({length:3},(_,i)=>({category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:i})),
    signals:{PLAYER_LOW_HP:1},
    seed:20260925
  };
  assert.deepEqual(decide(id,round,opts),decide(id,round,opts));
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
