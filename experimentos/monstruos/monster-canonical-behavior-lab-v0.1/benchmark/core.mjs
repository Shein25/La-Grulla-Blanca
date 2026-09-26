import {chooseMonsterIntent} from '../vendor/monster-engine.mjs';
import {PROFILES} from '../vendor/profiles.mjs';
import {CANDIDATE_ASSIGNMENTS} from '../profiles/candidate-assignments.mjs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {buildCanonicalAbilityCatalog,canonicalAbilityIds,baseCombat,seededRng} from '../adapter/canonical-combat-adapter.mjs';
import {applyTacticalOverlay} from '../tactics/tactical-overlay-v0.1.mjs';

export const TIERS=Object.freeze({
  smoke:1_000,
  standard:10_000,
  deep:100_000,
  million:1_000_000
});

function rng(seed){
  let x=seed>>>0;
  return ()=>{
    x^=x<<13;x^=x>>>17;x^=x<<5;
    return (x>>>0)/4294967296;
  };
}

function mixSeed(seed,a,b){
  let x=(seed>>>0)^Math.imul((a+1)>>>0,0x9e3779b1)^Math.imul((b+1)>>>0,0x85ebca6b);
  x^=x>>>16;x=Math.imul(x,0x7feb352d);x^=x>>>15;x=Math.imul(x,0x846ca68b);x^=x>>>16;
  return x>>>0;
}

function fnv64Init(){return 0xcbf29ce484222325n;}
function fnv64Update(h,text){
  for(let i=0;i<text.length;i++){
    h^=BigInt(text.charCodeAt(i));
    h=BigInt.asUintN(64,h*0x100000001b3n);
  }
  return h;
}
function fnv64Hex(h){return h.toString(16).padStart(16,'0');}
function inc(obj,key){obj[key]=(obj[key]||0)+1;}

function scenario(def,random){
  const techEvery=def.tecnica?.cada||1;
  const dueRound=techEvery;
  const randomRound=1+Math.floor(random()*Math.max(4,techEvery));
  const techniqueId=null; // set by caller
  const memoryCount=Math.floor(random()*5);
  const memory=[];
  for(let i=0;i<memoryCount;i++){
    memory.push({
      category:random()<0.72?'DEFENSA_ABSORCION':'RECUPERACION',
      result:random()<0.68?'EFECTIVA':'FALLIDA',
      round:i
    });
  }
  const alliesAlive=Math.floor(random()*4);
  const sameSpeciesAllies=Math.min(alliesAlive,Math.floor(random()*4));
  const playerLow=random()<0.45;
  const allyPresent=alliesAlive>0;
  const outnumber=alliesAlive>=2;
  const repeats=Math.floor(random()*5);
  return {
    dueRound,randomRound,memory,repeats,
    signals:{
      PLAYER_LOW_HP:playerLow?1:0,
      ALLY_PRESENT:allyPresent?1:0,
      OUTNUMBER_PLAYER:outnumber?1:0
    },
    social:{alliesAlive,sameSpeciesAllies,outnumbersPlayer:outnumber}
  };
}

function decision(M,id,s,{memoryMode='full',socialMode='full',seed=1,mode='DECISION_EXPERIMENTAL'}={}){
  const def=M[id], ids=canonicalAbilityIds(id);
  const recentAbilityIds=Array.from({length:s.repeats},()=>ids.technique);
  const baseMonster=buildCandidateMonsterInput({mobId:id,def,round:mode==='CADENCE_COMPAT'?s.randomRound:s.dueRound,mode,recentAbilityIds});
  // Ablación social real: mantener las señales de combate intactas y neutralizar
  // únicamente la interpretación del perfil social. Algunos flags (MANADA,
  // OPORTUNISTA) se derivan también de combat.signals, por lo que vaciar sólo
  // el objeto social no los desactiva y confundiría la métrica.
  const monster=socialMode==='full'
    ? baseMonster
    : {...baseMonster,socialProfileId:'SOLITARIO'};
  const abilities=applyTacticalOverlay(id,buildCanonicalAbilityCatalog(id,def));
  const memory=memoryMode==='full'?s.memory:[];
  const social=socialMode==='full'?s.social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false};
  const round=mode==='CADENCE_COMPAT'?s.randomRound:s.dueRound;
  return chooseMonsterIntent({
    monster,profiles:PROFILES,abilities,
    combat:baseCombat(round,{signals:s.signals}),
    memory,social,rng:seededRng(seed)
  });
}

export function resolveRuns({tier='smoke',runs=null}={}){
  if(runs!==null){
    const n=Number(runs);
    if(!Number.isSafeInteger(n)||n<1)throw new TypeError('runs debe ser entero seguro >=1');
    return n;
  }
  if(!Object.hasOwn(TIERS,tier))throw new RangeError(`tier desconocido: ${tier}`);
  return TIERS[tier];
}

export function runMonsterBenchmark(M,{tier='smoke',runs=null,seed=1337,mob='all'}={}){
  const runsPerMob=resolveRuns({tier,runs});
  const ids=mob==='all'
    ? Object.keys(CANDIDATE_ASSIGNMENTS).sort()
    : [mob];
  for(const id of ids) if(!CANDIDATE_ASSIGNMENTS[id]||!M[id])throw new RangeError(`mob desconocido/no asignado: ${id}`);

  let digest=fnv64Init();
  const results={};

  ids.forEach((id,mobIndex)=>{
    const def=M[id], random=rng(mixSeed(seed,mobIndex,0));
    const metrics={
      runs:runsPerMob,
      selected:{},
      memoryChangedDecision:0,
      socialChangedDecision:0,
      combinedChangedVsNeutral:0,
      cadenceChecks:0,
      cadenceViolations:0,
      invalidSelections:0
    };
    const examples=[];

    for(let i=0;i<runsPerMob;i++){
      const s=scenario(def,random);
      const idsCanon=canonicalAbilityIds(id);
      const decisionSeed=mixSeed(seed,mobIndex,i+1);

      const full=decision(M,id,s,{seed:decisionSeed});
      const noMemory=decision(M,id,s,{memoryMode:'none',seed:decisionSeed});
      const noSocial=decision(M,id,s,{socialMode:'none',seed:decisionSeed});
      const neutral=decision(M,id,s,{memoryMode:'none',socialMode:'none',seed:decisionSeed});

      inc(metrics.selected,full.abilityId);
      if(full.abilityId!==noMemory.abilityId)metrics.memoryChangedDecision++;
      if(full.abilityId!==noSocial.abilityId)metrics.socialChangedDecision++;
      if(full.abilityId!==neutral.abilityId)metrics.combinedChangedVsNeutral++;

      const allowed=new Set([idsCanon.basic,...(def.tecnica?[idsCanon.technique]:[])]);
      if(!allowed.has(full.abilityId))metrics.invalidSelections++;

      if(i%10===0){
        metrics.cadenceChecks++;
        const cadence=decision(M,id,s,{seed:decisionSeed,mode:'CADENCE_COMPAT'});
        const expected=def.tecnica&&s.randomRound%def.tecnica.cada===0?idsCanon.technique:idsCanon.basic;
        if(cadence.abilityId!==expected)metrics.cadenceViolations++;
      }

      if(full.abilityId!==neutral.abilityId&&examples.length<20){
        examples.push({
          memory:s.memory,
          signals:s.signals,
          social:s.social,
          repeats:s.repeats,
          full:full.abilityId,
          neutral:neutral.abilityId
        });
      }

      digest=fnv64Update(digest,JSON.stringify([
        id,i,s.memory,s.signals,s.social,s.repeats,
        full.abilityId,noMemory.abilityId,noSocial.abilityId,neutral.abilityId
      ]));
    }

    metrics.percent={
      memoryChanged:metrics.memoryChangedDecision/runsPerMob*100,
      socialChanged:metrics.socialChangedDecision/runsPerMob*100,
      combinedChangedVsNeutral:metrics.combinedChangedVsNeutral/runsPerMob*100
    };
    results[id]={assignment:CANDIDATE_ASSIGNMENTS[id],metrics,examples};
  });

  return {
    benchmark:'MONSTER_BEHAVIOR_BENCHMARK_V01',
    tier,runsPerMob,seed:seed>>>0,mob,
    mobCount:ids.length,totalPrimaryDecisions:runsPerMob*ids.length,
    results,digest:fnv64Hex(digest)
  };
}
