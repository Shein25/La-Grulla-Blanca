import fs from 'node:fs';
import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {baseCombat,seededRng,canonicalAbilityIds} from '../adapter/canonical-combat-adapter.mjs';
import {
  SURVIVAL_POLICIES,survivalUnlockXp,survivalEvolutionStage,survivalAbilityId,
  buildSurvivalAbilityCatalog,buildSurvivalMonsterInput
} from '../adaptive/survival-evolution-v0.1.mjs';

const data=JSON.parse(fs.readFileSync(new URL('../canonical/MOBS_ver74.snapshot.json',import.meta.url),'utf8'));
const M=data.mobs;
const ids=Object.keys(M).filter(id=>id!=='muneco_practica').sort();

function decide(id,{signals={},seed=1,cooldown=false,round=1,mode='DECISION_EXPERIMENTAL'}={}){
  const def=M[id],xp=survivalUnlockXp(def);
  const stage=survivalEvolutionStage({mobId:id,def,survivalXp:xp});
  return chooseMonsterIntent({
    monster:buildSurvivalMonsterInput({mobId:id,def,round,survivalXp:xp,mode,survivalCooldown:cooldown}),
    profiles:PROFILES,
    abilities:buildSurvivalAbilityCatalog({mobId:id,def,stage}),
    combat:baseCombat(round,{
      selfHp:signals.SELF_LOW_HP?0.2:0.8,
      playerHp:signals.PLAYER_LOW_HP?0.2:0.8,
      signals
    }),
    memory:[],
    social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false},
    rng:seededRng(seed)
  });
}

function rate(id,signals,runs=2000){
  const sid=survivalAbilityId(id);
  let n=0;
  for(let seed=1;seed<=runs;seed++) if(decide(id,{signals,seed}).abilityId===sid)n++;
  return n/runs;
}

function hitChance(attack,defense,evasion=5){
  let hits=0;
  for(let roll=1;roll<=20;roll++){
    if(roll===1)continue;
    const evasionExtra=Math.max(0,Math.round((evasion-5)/5));
    if(roll===20||roll+attack>=defense+evasionExtra)hits++;
  }
  return hits/20;
}

function expectedPrevented(effect,{attack,defense,damage}){
  const baseHit=hitChance(attack,defense,5);
  let protectedHit=baseHit;
  let preventedOnHit=0;

  if(effect.kind==='EVADE_NEXT'){
    protectedHit=hitChance(attack,defense,5+effect.evasionBonus);
    return {
      baseHit,
      protectedHit,
      expectedPrevented:(baseHit-protectedHit)*damage
    };
  }
  if(effect.kind==='DEFENSE_UP'){
    protectedHit=hitChance(attack,defense+effect.defenseBonus,5);
    return {
      baseHit,
      protectedHit,
      expectedPrevented:(baseHit-protectedHit)*damage
    };
  }
  if(effect.kind==='MITIGATE_NEXT'){
    preventedOnHit=Math.floor(damage*effect.damageReductionPct/100);
  }else if(effect.kind==='ABSORB_RESERVE'){
    preventedOnHit=Math.min(damage,effect.absorbPerHit,effect.reserve);
  }else{
    throw new RangeError(`defense kind desconocido: ${effect.kind}`);
  }
  return {
    baseHit,
    protectedHit,
    expectedPrevented:baseHit*preventedOnHit
  };
}

const MECHANIC_SCENARIOS=Object.freeze({
  inaccurateHeavy:Object.freeze({attack:4,defense:12,damage:20}),
  balancedMedium:Object.freeze({attack:6,defense:12,damage:10}),
  accurateSmall:Object.freeze({attack:10,defense:12,damage:4}),
  accurateHeavy:Object.freeze({attack:10,defense:12,damage:20})
});

const rows=[];
let cadenceViolations=0;
for(const id of ids){
  const def=M[id],policy=SURVIVAL_POLICIES[id];
  const row={
    id,
    unlockXp:survivalUnlockXp(def),
    defenseKind:policy.effect.kind,
    healthy:rate(id,{},1000),
    low:rate(id,{SELF_LOW_HP:1},2000),
    heavy:rate(id,{TOOK_HEAVY_HIT:1},1000),
    critical:rate(id,{SELF_LOW_HP:1,TOOK_HEAVY_HIT:1},1000),
    bothLow:rate(id,{SELF_LOW_HP:1,PLAYER_LOW_HP:1},2000),
    mechanics:Object.fromEntries(
      Object.entries(MECHANIC_SCENARIOS).map(([name,scenario])=>[
        name,
        expectedPrevented(policy.effect,scenario)
      ])
    )
  };
  if(def.tecnica){
    const r=decide(id,{
      round:def.tecnica.cada,
      mode:'CADENCE_COMPAT',
      signals:{SELF_LOW_HP:1,TOOK_HEAVY_HIT:1},
      seed:2026
    });
    if(r.abilityId!==canonicalAbilityIds(id).technique)cadenceViolations++;
  }
  rows.push(row);
}

console.log(JSON.stringify({
  benchmark:'MONSTER_ADAPTIVE_SURVIVAL_V01',
  rows,
  cadenceViolations
},null,2));
