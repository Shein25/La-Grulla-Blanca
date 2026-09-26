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

T('status explicitly non-canonical',()=>assert.equal(SURVIVAL_EVOLUTION_STATUS,'EXPERIMENTAL_NON_CANONICAL_SURVIVAL_V01_FINAL_CANDIDATE'));

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

T('smarter evolved profiles take more finishing risks when both sides are low',()=>{
  const ids=['rata_qi','serpiente_qi','lobo_espiritual','guardian_coral'];
  const rates=ids.map(id=>defenseRate(id,{signals:{SELF_LOW_HP:1,PLAYER_LOW_HP:1},runs:4000}));
  assert.ok(rates[0]>rates[1] && rates[1]>rates[2] && rates[2]>rates[3],JSON.stringify({ids,rates}));
});

T('all four defensive families are represented with intentional distribution',()=>{
  const counts={};
  for(const policy of Object.values(SURVIVAL_POLICIES)){
    counts[policy.effect.kind]=(counts[policy.effect.kind]||0)+1;
  }
  assert.deepEqual(counts,{
    EVADE_NEXT:7,
    DEFENSE_UP:3,
    MITIGATE_NEXT:3,
    ABSORB_RESERVE:5
  });
});

T('defensive effects stay inside conservative stage-one caps',()=>{
  for(const [id,policy] of Object.entries(SURVIVAL_POLICIES)){
    const effect=policy.effect;
    assert.equal(effect.cooldownRounds,2,id);
    if(effect.kind==='EVADE_NEXT'){
      assert.equal(effect.durationActions,1,id);
      assert.ok(effect.evasionBonus>=20&&effect.evasionBonus<=30,id);
    }else if(effect.kind==='DEFENSE_UP'){
      assert.equal(effect.durationActions,1,id);
      assert.ok(effect.defenseBonus>=3&&effect.defenseBonus<=5,id);
    }else if(effect.kind==='MITIGATE_NEXT'){
      assert.equal(effect.durationHits,1,id);
      assert.ok(effect.damageReductionPct>=35&&effect.damageReductionPct<=40,id);
    }else if(effect.kind==='ABSORB_RESERVE'){
      assert.ok(effect.absorbPerHit>=3&&effect.absorbPerHit<=5,id);
      assert.equal(effect.reserve,effect.absorbPerHit*2,id);
    }else{
      assert.fail(`${id}: effect kind desconocido ${effect.kind}`);
    }
  }
});

T('synthetic smoke only: four defense mechanics remain mechanically distinct',()=>{
  const hitChance=(attack,defense,evasion=5)=>{
    let hits=0;
    for(let roll=1;roll<=20;roll++){
      if(roll===1)continue;
      if(roll===20||roll+attack>=defense+Math.max(0,Math.round((evasion-5)/5)))hits++;
    }
    return hits/20;
  };
  const prevented=(effect,{attack,defense,damage})=>{
    const base=hitChance(attack,defense,5);
    if(effect.kind==='EVADE_NEXT'){
      return (base-hitChance(attack,defense,5+effect.evasionBonus))*damage;
    }
    if(effect.kind==='DEFENSE_UP'){
      return (base-hitChance(attack,defense+effect.defenseBonus,5))*damage;
    }
    if(effect.kind==='MITIGATE_NEXT'){
      return base*Math.floor(damage*effect.damageReductionPct/100);
    }
    if(effect.kind==='ABSORB_RESERVE'){
      return base*Math.min(damage,effect.absorbPerHit,effect.reserve);
    }
    throw new Error(effect.kind);
  };

  const evasive=SURVIVAL_POLICIES.rata_qi.effect;
  const flat=SURVIVAL_POLICIES.centinela_pluma.effect;
  const mitigate=SURVIVAL_POLICIES.eco_caido.effect;
  const absorb=SURVIVAL_POLICIES.guardian_coral.effect;

  const inaccurateHeavy={attack:4,defense:12,damage:20};
  const accurateSmall={attack:10,defense:12,damage:4};
  const accurateHeavy={attack:10,defense:12,damage:20};

  assert.ok(prevented(evasive,inaccurateHeavy)>prevented(absorb,inaccurateHeavy));
  assert.ok(prevented(absorb,accurateSmall)>prevented(mitigate,accurateSmall));
  assert.ok(prevented(mitigate,accurateHeavy)>prevented(absorb,accurateHeavy));

  const evade20=SURVIVAL_POLICIES.serpiente_qi.effect;
  const flat3=SURVIVAL_POLICIES.lobo_espiritual.effect;
  const sameScenario={attack:6,defense:12,damage:10};
  const evadeValue=prevented(evade20,sameScenario);
  assert.ok(evadeValue>prevented(flat3,sameScenario));
  assert.ok(evadeValue<prevented(flat,sameScenario));
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
