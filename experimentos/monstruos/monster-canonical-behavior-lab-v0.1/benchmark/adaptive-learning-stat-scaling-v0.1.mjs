import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';

import {NATIVE_STAGE_BY_MOB} from '../adaptive/stage-progression-v0.1.mjs';
import {SURVIVAL_POLICIES} from '../adaptive/survival-evolution-v0.1.mjs';

const here=dirname(fileURLToPath(import.meta.url));
const html=readFileSync(resolve(here,'../../../../grulla-blanca_ver74.html'),'utf8');

function extractValue(marker){
  const markerAt=html.indexOf(marker);
  if(markerAt<0)throw new Error(`no se encontró ${marker}`);
  const eq=html.indexOf('=',markerAt);
  let start=eq+1;
  while(start<html.length&&!'{['.includes(html[start]))start++;
  const open=html[start],close=open==='{'?'}':']';
  let depth=0,quote=null,escape=false;
  for(let i=start;i<html.length;i++){
    const c=html[i];
    if(quote){
      if(escape){escape=false;continue;}
      if(c==='\\'){escape=true;continue;}
      if(c===quote)quote=null;
      continue;
    }
    if(c==="'"||c==='"'||c==='`'){quote=c;continue;}
    if(c===open)depth++;
    else if(c===close&&--depth===0)return html.slice(start,i+1);
  }
  throw new Error(`valor sin cierre: ${marker}`);
}

const MOBS=new Function(`return (${extractValue('const MOBS =')})`)();
const RAICES=new Function(`return (${extractValue('const RAICES =')})`)();
const TECNICAS=new Function(`return (${extractValue('const TECNICAS =')})`)();
const RAMAS=new Function(`return (${extractValue('const RAMAS =')})`)();

const VASO={1:25,2:45,3:75,4:110};
const ELEMENTS=['fuego','metal','viento','tierra','agua'];
const BONO_ELEMENTAL=.20;
const ESQUIVA_INNATA=5;

const PREPARED_LOADOUT={
  1:{attack:0,defense:1,basic:'1d6'},
  2:{attack:1,defense:3,basic:'1d8'},
  3:{attack:2,defense:5,basic:'1d8'},
  4:{attack:2,defense:7,basic:'1d8'}
};

export const LEARNING_STAT_CURVES=Object.freeze({
  A_FIXED:Object.freeze({
    label:'E1 + estadísticas canónicas',
    hpPerTier:0,
    damagePerTier:0,
    hitBonus:tier=>0,
    evasionBonus:tier=>0,
    critSteps:tier=>0
  }),

  C_GENTLE:Object.freeze({
    label:'HP/daño +2.5% por Tier; HIT +1 desde T3; EVA +5 y CRIT +5pp sólo T4',
    hpPerTier:.025,
    damagePerTier:.025,
    hitBonus:tier=>tier>=3?1:0,
    evasionBonus:tier=>tier>=4?5:0,
    critSteps:tier=>tier>=4?1:0
  }),

  C_STAGGERED:Object.freeze({
    label:'HP/daño +2.5% por Tier; HIT +1 desde T2; EVA +5 desde T3; CRIT +5pp en T4',
    hpPerTier:.025,
    damagePerTier:.025,
    hitBonus:tier=>tier>=2?1:0,
    evasionBonus:tier=>tier>=3?5:0,
    critSteps:tier=>tier>=4?1:0
  }),

  C_MEDIUM:Object.freeze({
    label:'HP/daño +3% por Tier; HIT/EVA/CRIT avanzan cada dos Tiers',
    hpPerTier:.03,
    damagePerTier:.03,
    hitBonus:tier=>Math.floor(tier/2),
    evasionBonus:tier=>5*Math.floor(tier/2),
    critSteps:tier=>Math.floor(tier/2)
  }),

  C_AGGRESSIVE:Object.freeze({
    label:'STRESS: HP/daño +5% por Tier; HIT +1, EVA +5 y CRIT +5pp por Tier',
    hpPerTier:.05,
    damagePerTier:.05,
    hitBonus:tier=>tier,
    evasionBonus:tier=>5*tier,
    critSteps:tier=>tier
  })
});

function relation(a,b){
  if(!a||!b||a===b)return 0;
  const i=ELEMENTS.indexOf(a),j=ELEMENTS.indexOf(b);
  if(i<0||j<0)return 0;
  if((i+1)%ELEMENTS.length===j)return 1;
  if((j+1)%ELEMENTS.length===i)return -1;
  return 0;
}

function rng32(seed){
  let x=seed|0;
  return ()=>{
    x^=x<<13;x^=x>>>17;x^=x<<5;
    return (x>>>0)/4294967296;
  };
}

function roll(expr,rng){
  let total=0;
  for(const part of String(expr||0).replace(/\s/g,'').split('+')){
    if(!part)continue;
    if(part.includes('d')){
      const [n0,f0]=part.split('d'),n=Number(n0)||1,faces=Number(f0);
      for(let i=0;i<n;i++)total+=1+Math.floor(rng()*faces);
    }else total+=Number(part)||0;
  }
  return total;
}

function hits(d20,attack,defense,critMin=20,evasion=ESQUIVA_INNATA){
  if(d20===1)return false;
  if(d20===20||d20>=critMin)return true;
  const evasionExtra=Math.max(0,Math.round((evasion-ESQUIVA_INNATA)/5));
  return d20+attack>=defense+evasionExtra;
}

function techniqueConfig(root,stage,o1=0,o2=0){
  const t=TECNICAS[RAICES[root].tecnica];
  let damage=t.daño,attackBonus=0,critMin=20,critMult=1.5,cost=t.coste,burn=null,debil=null;
  const depth=Math.min(2,stage-1);

  for(const [rank,opt] of [[1,o1],[2,o2]]){
    if(rank>depth||!opt)continue;
    const mod=RAMAS[RAICES[root].tecnica]?.[rank]?.[opt-1]?.mod||{};
    if(mod.daño)damage+=mod.daño;
    if(mod.ataque)attackBonus+=mod.ataque;
    if(mod.critMin)critMin=Math.min(critMin,mod.critMin);
    if(mod.critMult)critMult+=mod.critMult-1.5;
    if(mod.coste)cost+=mod.coste;
    if(mod.quemadura)burn={damage:mod.quemadura.daño,turns:mod.quemadura.turnos||1};
    if(mod.debil)debil={attack:mod.debil.ataque||0,turns:mod.debil.turnos||1};
  }

  damage+='+1';
  cost=Math.max(Math.ceil(t.coste*.7),cost-1);
  const gear=PREPARED_LOADOUT[stage];

  return {
    root,element:t.elemento,
    hp:16+4*(stage-1),maxHp:16+4*(stage-1),qi:VASO[stage],
    attack:1+(RAICES[root].ataque||0)+(stage-1)+gear.attack,
    defense:10+(RAICES[root].defensa||0)+gear.defense,
    basic:gear.basic,
    damage,attackBonus,critMin,critMult,cost,burn,debil,
    potions:1
  };
}

function configsFor(stage){
  const out=[];
  for(const root of Object.keys(RAICES)){
    if(stage===1)out.push(techniqueConfig(root,stage));
    else if(stage===2){
      for(let a=1;a<=3;a++)out.push(techniqueConfig(root,stage,a,0));
    }else{
      for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)out.push(techniqueConfig(root,stage,a,b));
    }
  }
  return out;
}

function scaledMob(base,tier,curveId){
  const curve=LEARNING_STAT_CURVES[curveId];
  if(!curve)throw new RangeError(`curve desconocida: ${curveId}`);
  if(!Number.isInteger(tier)||tier<0||tier>4)throw new RangeError('tier debe ser 0..4');

  const hpFactor=1+curve.hpPerTier*tier;
  return {
    ...base,
    hp:Math.round(base.hp*hpFactor),
    maxHp:Math.round(base.hp*hpFactor),
    damageMultiplier:1+curve.damagePerTier*tier,
    hitBonus:curve.hitBonus(tier),
    persistentEvasion:ESQUIVA_INNATA+curve.evasionBonus(tier),
    critMin:Math.max(16,20-curve.critSteps(tier))
  };
}

/*
 * Envelope E1 usado para comparar modelos estadísticos:
 * - la defensa sólo es elegible a HP bajo;
 * - golpe fuerte + HP bajo => defensa prioritaria;
 * - HP bajo sin golpe fuerte => ~50%;
 * - CADENCE_COMPAT conserva la técnica canónica en su ronda;
 * - la acción defensiva consume el turno;
 * - cooldown de dos rondas completas.
 *
 * No sustituye al executor productivo: es Monte Carlo comparativo.
 */
function duel(mobId,basePlayer,seed,tier,curveId){
  const rng=rng32(seed);
  const base=MOBS[mobId];
  const policy=SURVIVAL_POLICIES[mobId]?.effect;
  if(!policy)throw new RangeError(`sin E1 para ${mobId}`);

  const mob=scaledMob(base,tier,curveId);
  const p={...basePlayer};

  let round=0;
  let mobBurn=null,mobDebuff=0,mobDebuffTurns=0,playerDots=[];
  let defenseState=null,absorbReserve=0,defenseCooldownUntil=0,lastPlayerDamage=0;

  for(let turn=0;turn<30;turn++){
    round++;

    let usedPotion=false;
    if(p.potions>0&&p.hp<=p.maxHp*.35){
      p.potions--;
      p.hp=Math.min(p.maxHp,p.hp+roll('3d6+6',rng));
      usedPotion=true;
    }

    lastPlayerDamage=0;

    if(!usedPotion){
      const usesTechnique=p.qi>=p.cost;
      let attack=p.attack,damageExpr=p.basic,critMin=20,critMult=1.5,element=null;
      if(usesTechnique){
        p.qi-=p.cost;
        attack+=p.attackBonus;
        damageExpr=p.damage;
        critMin=p.critMin;
        critMult=p.critMult;
        element=p.element;
      }

      const d20=1+Math.floor(rng()*20);
      let protectedDefense=mob.defensa;
      let protectedEvasion=mob.persistentEvasion;

      if(defenseState?.kind==='DEFENSE_UP')protectedDefense+=defenseState.defenseBonus;
      if(defenseState?.kind==='EVADE_NEXT')protectedEvasion+=defenseState.evasionBonus;

      const connected=hits(d20,attack,protectedDefense,critMin,protectedEvasion);

      if(defenseState?.kind==='EVADE_NEXT'||defenseState?.kind==='DEFENSE_UP'){
        defenseState=null;
      }

      if(connected){
        let dmg=roll(damageExpr,rng);
        if(d20>=critMin&&d20!==1)dmg=Math.ceil(dmg*critMult);

        const elemental=usesTechnique?relation(element,mob.elemento):0;
        if(elemental)dmg=Math.max(1,Math.round(dmg*(1+elemental*BONO_ELEMENTAL)));

        if(defenseState?.kind==='MITIGATE_NEXT'){
          dmg=Math.max(0,dmg-Math.floor(dmg*defenseState.damageReductionPct/100));
          defenseState=null;
        }

        if(absorbReserve>0&&policy.kind==='ABSORB_RESERVE'){
          const absorbed=Math.min(dmg,policy.absorbPerHit,absorbReserve);
          dmg-=absorbed;
          absorbReserve-=absorbed;
        }

        mob.hp-=dmg;
        lastPlayerDamage=dmg;

        if(usesTechnique&&dmg>0&&p.burn)mobBurn={...p.burn};
        if(usesTechnique&&dmg>0&&p.debil){
          mobDebuff=p.debil.attack;
          mobDebuffTurns=p.debil.turns;
        }
      }
    }

    if(mob.hp<=0)return {win:true,rounds:round,hp:p.hp};

    const tech=mob.tecnica;
    const techniqueTurn=!!(tech&&round%tech.cada===0);
    const low=mob.hp/mob.maxHp<=.35;
    const heavy=lastPlayerDamage>=Math.max(5,mob.maxHp*.20);

    let defended=false;
    if(tier>=1&&!techniqueTurn&&round>=defenseCooldownUntil&&low){
      const chance=heavy?1:.5;
      if(rng()<chance){
        defended=true;
        defenseCooldownUntil=round+3;
        if(policy.kind==='ABSORB_RESERVE')absorbReserve=policy.reserve;
        else defenseState={...policy};
      }
    }

    if(!defended){
      let mobAttack=mob.ataque+mob.hitBonus+(mobDebuffTurns>0?mobDebuff:0);
      let mobDamage=mob.daño;

      if(techniqueTurn){
        if(tech.ataque)mobAttack+=tech.ataque;
        if(tech.daño)mobDamage=tech.daño;
      }

      const enemyD20=1+Math.floor(rng()*20);
      if(hits(enemyD20,mobAttack,p.defense,mob.critMin,ESQUIVA_INNATA)){
        let dmg=roll(mobDamage,rng);
        if(enemyD20>=mob.critMin&&enemyD20!==1)dmg=Math.ceil(dmg*1.5);
        dmg=Math.max(1,Math.round(dmg*mob.damageMultiplier));
        p.hp-=dmg;

        if(techniqueTurn&&dmg>0&&tech.veneno){
          playerDots.push({damage:tech.veneno.daño,turns:tech.veneno.turnos||1});
        }
        if(techniqueTurn&&dmg>0&&tech.quemadura){
          playerDots.push({damage:tech.quemadura.daño,turns:tech.quemadura.turnos||1});
        }
      }
    }

    if(p.hp<=0)return {win:false,rounds:round,hp:0};

    const kept=[];
    for(const dot of playerDots){
      p.hp-=roll(dot.damage,rng);
      dot.turns--;
      if(dot.turns>0)kept.push(dot);
    }
    playerDots=kept;
    if(p.hp<=0)return {win:false,rounds:round,hp:0};

    if(mobBurn){
      mob.hp-=roll(mobBurn.damage,rng);
      mobBurn.turns--;
      if(mobBurn.turns<=0)mobBurn=null;
    }

    if(mob.hp<=0)return {win:true,rounds:round,hp:p.hp};
    if(mobDebuffTurns>0)mobDebuffTurns--;
  }

  return {win:p.hp>mob.hp,rounds:30,hp:p.hp};
}

function maxLegalTierAtPlayerStage(mobId,playerStage){
  const native=NATIVE_STAGE_BY_MOB[mobId]?.stage;
  if(!native)throw new RangeError(`sin etapa nativa: ${mobId}`);
  const delta=playerStage-native;
  if(delta<0)return 0;
  return Math.min(4,delta+1);
}

function runEnvelope({curveId,playerStage,tierMode,runsPerBuild}){
  const rows=[];

  for(const [mobId,assignment] of Object.entries(NATIVE_STAGE_BY_MOB)){
    const nativeStage=assignment.stage;
    const tier=tierMode==='LEGAL_MAX'
      ? maxLegalTierAtPlayerStage(mobId,playerStage)
      : tierMode;

    const configs=configsFor(playerStage);
    let wins=0,total=0;
    let ci=0;

    for(const pc of configs){
      for(let run=0;run<runsPerBuild;run++){
        const seed=
          playerStage*100000000+
          nativeStage*10000000+
          tier*1000000+
          ci*10000+
          run*47+
          mobId.length*101+
          Object.keys(LEARNING_STAT_CURVES).indexOf(curveId)*997;

        if(duel(mobId,pc,seed,tier,curveId).win)wins++;
        total++;
      }
      ci++;
    }

    rows.push({
      mobId,
      nativeStage,
      role:assignment.role,
      tier,
      winRate:wins/total
    });
  }

  return rows;
}

function runNativeTier1({curveId,runsPerBuild}){
  const rows=[];

  for(const [mobId,assignment] of Object.entries(NATIVE_STAGE_BY_MOB)){
    const playerStage=assignment.stage;
    const configs=configsFor(playerStage);
    let wins=0,total=0;
    let ci=0;

    for(const pc of configs){
      for(let run=0;run<runsPerBuild;run++){
        const seed=
          playerStage*100000000+
          ci*10000+
          run*59+
          mobId.length*103+
          Object.keys(LEARNING_STAT_CURVES).indexOf(curveId)*991;

        if(duel(mobId,pc,seed,1,curveId).win)wins++;
        total++;
      }
      ci++;
    }

    rows.push({
      mobId,
      nativeStage:assignment.stage,
      role:assignment.role,
      tier:1,
      winRate:wins/total
    });
  }

  return rows;
}

function byBand(rows){
  const out={};
  for(let stage=1;stage<=4;stage++){
    const x=rows.filter(r=>r.nativeStage===stage);
    out[stage]=x.reduce((sum,r)=>sum+r.winRate,0)/x.length;
  }
  return out;
}

const arg=process.argv.find(x=>x.startsWith('--runs='));
const runsPerBuild=arg?Math.max(50,Number(arg.split('=')[1])||400):400;

const nativeA=runNativeTier1({curveId:'A_FIXED',runsPerBuild});
const nativeC=runNativeTier1({curveId:'C_STAGGERED',runsPerBuild});

const legal={};
for(const curveId of Object.keys(LEARNING_STAT_CURVES)){
  const rows=runEnvelope({
    curveId,
    playerStage:4,
    tierMode:'LEGAL_MAX',
    runsPerBuild
  });
  legal[curveId]={byBand:byBand(rows),rows};
}

console.log(JSON.stringify({
  benchmark:'ADAPTIVE_LEARNING_STAT_SCALING_V01',
  status:'EXPERIMENTAL_NON_CANONICAL_MODEL_C',
  runsPerBuild,
  semantics:{
    learningSpeed:'NO MODELADA: el benchmark fuerza Tier 1..4; no supone cantidad de kills',
    tierCeiling:'respeta nativeStage/playerStage; a LianQi IV: banda I→T4, II→T3, III→T2, IV→T1',
    hit:'bono plano de ataque/precisión d20',
    evasion:'cada +5 de esquiva cruza aproximadamente un breakpoint d20',
    crit:'cada paso de critMin equivale a +5 puntos porcentuales de crítico',
    cadence:'la técnica canónica sigue siendo autoritativa en su ronda'
  },
  curves:Object.fromEntries(Object.entries(LEARNING_STAT_CURVES).map(([id,c])=>[id,c.label])),
  nativeTier1:{
    A_FIXED:{byBand:byBand(nativeA),rows:nativeA},
    C_STAGGERED:{byBand:byBand(nativeC),rows:nativeC}
  },
  legalArc1AtLianQiIV:legal
},null,2));
