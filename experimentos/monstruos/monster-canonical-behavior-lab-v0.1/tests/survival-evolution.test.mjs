import assert from 'node:assert/strict';
import fs from 'node:fs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {baseCombat,canonicalAbilityIds,seededRng} from '../adapter/canonical-combat-adapter.mjs';
import {
  SURVIVAL_EVOLUTION_STATUS,SURVIVAL_POLICIES,
  adaptationXpGain,survivalUnlockXp,survivalEvolutionStage,
  survivalAbilityId,buildSurvivalAbilityCatalog,buildSurvivalMonsterInput
} from '../adaptive/survival-evolution-v0.1.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const M=data.mobs;
const combatants=Object.keys(M).filter(id=>id!=='muneco_practica').sort();

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

function decide(id,{xp,round=1,signals={},social={alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false},seed=1,cooldown=false,mode='DECISION_EXPERIMENTAL'}={}){
  const def=M[id];
  const stage=survivalEvolutionStage({mobId:id,def,survivalXp:xp});
  return chooseMonsterIntent({
    monster:buildSurvivalMonsterInput({
      mobId:id,def,round,survivalXp:xp,mode,survivalCooldown:cooldown
    }),
    profiles:PROFILES,
    abilities:buildSurvivalAbilityCatalog({mobId:id,def,stage}),
    combat:baseCombat(round,{selfHp:signals.SELF_LOW_HP?0.2:0.8,playerHp:signals.PLAYER_LOW_HP?0.2:0.8,signals}),
    memory:[],
    social,
    rng:seededRng(seed)
  });
}

function defenseRate(id,{signals={},social,round=1,cooldown=false,mode='DECISION_EXPERIMENTAL',runs=1000}={}){
  const def=M[id],xp=survivalUnlockXp(def),sid=survivalAbilityId(id);
  let defense=0;
  for(let seed=1;seed<=runs;seed++){
    const r=decide(id,{xp,round,signals,social,seed,cooldown,mode});
    if(r.abilityId===sid)defense++;
  }
  return defense/runs;
}

T('status explicitly non-canonical',()=>assert.equal(SURVIVAL_EVOLUTION_STATUS,'EXPERIMENTAL_NON_CANONICAL_SURVIVAL_V01'));

T('all 18 combatants have exactly one survival policy',()=>{
  assert.deepEqual(Object.keys(SURVIVAL_POLICIES).sort(),combatants);
});

T('practice dummy has no survival policy',()=>{
  assert.equal(Object.hasOwn(SURVIVAL_POLICIES,'muneco_practica'),false);
});

T('adaptation XP rewards encounters, not idle calls',()=>{
  assert.equal(adaptationXpGain({rounds:0}),0);
  assert.equal(adaptationXpGain({rounds:1}),1);
  assert.equal(adaptationXpGain({rounds:4,reachedLowHp:true}),2);
  assert.equal(adaptationXpGain({rounds:4,heavyHitObserved:true}),2);
  assert.equal(adaptationXpGain({rounds:4,reachedLowHp:true,heavyHitObserved:true}),2);
});

T('common unlock is 6 XP and unique unlock is 4 XP',()=>{
  assert.equal(survivalUnlockXp(M.rata_qi),6);
  assert.equal(survivalUnlockXp(M.eco_caido),4);
});

T('stage zero preserves base kit and base cognitive profile',()=>{
  for(const id of combatants){
    const def=M[id],threshold=survivalUnlockXp(def);
    const before=buildSurvivalMonsterInput({mobId:id,def,round:1,survivalXp:threshold-1});
    assert.equal(before.adaptiveStage,0,id);
    assert.equal(before.effectiveKit.includes(survivalAbilityId(id)),false,id);
  }
});

T('stage one adds survival and advances cognition by at most one profile step',()=>{
  const expected={
    INSTINTIVO:'REACTIVO_1',REACTIVO_1:'CAZADOR_2',CAZADOR_2:'TACTICO_3',
    TACTICO_3:'MASTER_4',MASTER_4:'MASTER_4'
  };
  for(const id of combatants){
    const def=M[id],threshold=survivalUnlockXp(def);
    const pre=buildSurvivalMonsterInput({mobId:id,def,round:1,survivalXp:threshold-1});
    const evolved=buildSurvivalMonsterInput({mobId:id,def,round:1,survivalXp:threshold});
    assert.equal(evolved.adaptiveStage,1,id);
    assert.ok(evolved.effectiveKit.includes(survivalAbilityId(id)),id);
    assert.equal(evolved.profileId,expected[pre.profileId],id);
  }
});

T('no monster defends while healthy in 1000 seeded decisions',()=>{
  for(const id of combatants){
    const rate=defenseRate(id,{signals:{},runs:1000});
    assert.equal(rate,0,id+': '+rate);
  }
});

T('low HP creates a real survival decision instead of deterministic turtling',()=>{
  for(const id of combatants){
    const a=SURVIVAL_POLICIES[id];
    const social=a.socialWeights?.TERRITORIAL_SOLO
      ? {alliesAlive:1,sameSpeciesAllies:0,outnumbersPlayer:false}
      : {alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false};
    const rate=defenseRate(id,{signals:{SELF_LOW_HP:1},social,runs:2000});
    assert.ok(rate>=0.35 && rate<=0.65,id+': '+rate);
  }
});

T('low HP plus heavy hit strongly prioritizes survival',()=>{
  for(const id of combatants){
    const rate=defenseRate(id,{signals:{SELF_LOW_HP:1,TOOK_HEAVY_HIT:1},runs:1000});
    assert.ok(rate>=0.90,id+': '+rate);
  }
});

T('cooldown prevents consecutive survival actions',()=>{
  for(const id of combatants){
    const rate=defenseRate(id,{signals:{SELF_LOW_HP:1,TOOK_HEAVY_HIT:1},cooldown:true,runs:200});
    assert.equal(rate,0,id+': '+rate);
  }
});

T('CADENCE_COMPAT keeps canonical technique authoritative on due round',()=>{
  for(const id of combatants){
    const def=M[id];
    if(!def.tecnica)continue;
    const round=def.tecnica.cada;
    const threshold=survivalUnlockXp(def);
    const r=decide(id,{
      xp:threshold,round,mode:'CADENCE_COMPAT',
      signals:{SELF_LOW_HP:1,TOOK_HEAVY_HIT:1},
      seed:99
    });
    assert.equal(r.abilityId,canonicalAbilityIds(id).technique,id);
    assert.equal(r.debug.considered.length,1,id);
  }
});

T('attack-only monsters gain defense rather than invented offense',()=>{
  for(const id of ['rata_qi','eco_caido']){
    const def=M[id],stage=1;
    const catalog=buildSurvivalAbilityCatalog({mobId:id,def,stage});
    const ids=Object.keys(catalog).sort();
    assert.deepEqual(ids.sort(),[canonicalAbilityIds(id).basic,survivalAbilityId(id)].sort(),id);
    assert.equal(catalog[survivalAbilityId(id)].intentCategory,'DEFENSA',id);
  }
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
