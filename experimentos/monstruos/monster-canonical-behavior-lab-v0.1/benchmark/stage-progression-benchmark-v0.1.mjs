import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';
import {NATIVE_STAGE_BY_MOB} from '../adaptive/stage-progression-v0.1.mjs';

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
    if(c==="'"||c==='"'||c==='\x60'){quote=c;continue;}
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

const PROFILES=Object.freeze({
  MINIMAL:Object.freeze({
    label:'uniforme inicial, espada de madera, sin consumibles',
    loadout:{
      1:{attack:0,defense:1,basic:'1d6'},
      2:{attack:0,defense:1,basic:'1d6'},
      3:{attack:0,defense:1,basic:'1d6'},
      4:{attack:0,defense:1,basic:'1d6'}
    },
    potion:false
  }),
  PREPARED:Object.freeze({
    label:'sensibilidad: equipo razonable de etapa + 1 poción de sangre',
    loadout:{
      1:{attack:0,defense:1,basic:'1d6'},
      2:{attack:1,defense:3,basic:'1d8'},
      3:{attack:2,defense:5,basic:'1d8'},
      4:{attack:2,defense:7,basic:'1d8'}
    },
    potion:true
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

function hits(d20,attack,defense,critMin=20,evasion=5){
  if(d20===1)return false;
  if(d20===20||d20>=critMin)return true;
  const extra=Math.max(0,Math.round((evasion-5)/5));
  return d20+attack>=defense+extra;
}

function techniqueConfig(root,stage,o1=0,o2=0,profile='MINIMAL'){
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
  // Afinidad principal: +1 daño y -1 qi; suelo global de 70%.
  damage+='+1';
  cost=Math.max(Math.ceil(t.coste*.7),cost-1);
  const gear=PROFILES[profile].loadout[stage];
  return {
    root,element:t.elemento,
    hp:16+4*(stage-1),maxHp:16+4*(stage-1),qi:VASO[stage],
    attack:1+(RAICES[root].ataque||0)+(stage-1)+gear.attack,
    defense:10+(RAICES[root].defensa||0)+gear.defense,
    basic:gear.basic,
    damage,attackBonus,critMin,critMult,cost,burn,debil,
    potions:PROFILES[profile].potion?1:0
  };
}

function configsFor(stage,profile){
  const out=[];
  for(const root of Object.keys(RAICES)){
    if(stage===1)out.push(techniqueConfig(root,stage,0,0,profile));
    else if(stage===2)for(let a=1;a<=3;a++)out.push(techniqueConfig(root,stage,a,0,profile));
    else for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)out.push(techniqueConfig(root,stage,a,b,profile));
  }
  return out;
}

function duel(mobId,basePlayer,seed){
  const rng=rng32(seed),mob={...MOBS[mobId]},p={...basePlayer};
  let round=0,mobBurn=null,mobDebuff=0,mobDebuffTurns=0,playerDots=[];

  for(let turn=0;turn<30;turn++){
    round++;

    let usedPotion=false;
    if(p.potions>0&&p.hp<=p.maxHp*.35){
      p.potions--;
      p.hp=Math.min(p.maxHp,p.hp+roll('3d6+6',rng));
      usedPotion=true;
    }

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
      if(hits(d20,attack,mob.defensa,critMin,5)){
        let dmg=roll(damageExpr,rng);
        if(d20>=critMin&&d20!==1)dmg=Math.ceil(dmg*critMult);
        const rel=usesTechnique?relation(element,mob.elemento):0;
        if(rel)dmg=Math.max(1,Math.round(dmg*(1+rel*BONO_ELEMENTAL)));
        mob.hp-=dmg;
        if(usesTechnique&&dmg>0&&p.burn)mobBurn={...p.burn};
        if(usesTechnique&&dmg>0&&p.debil){
          mobDebuff=p.debil.attack;
          mobDebuffTurns=p.debil.turns;
        }
      }
    }

    if(mob.hp<=0)return {win:true,rounds:round,hp:p.hp};

    let mobAttack=mob.ataque+(mobDebuffTurns>0?mobDebuff:0);
    let mobDamage=mob.daño;
    const tech=mob.tecnica;
    const techniqueTurn=!!(tech&&round%tech.cada===0);
    if(techniqueTurn){
      if(tech.ataque)mobAttack+=tech.ataque;
      if(tech.daño)mobDamage=tech.daño;
    }

    const enemyD20=1+Math.floor(rng()*20);
    if(hits(enemyD20,mobAttack,p.defense,20,5)){
      let dmg=roll(mobDamage,rng);
      if(enemyD20===20)dmg=Math.ceil(dmg*1.5);
      p.hp-=dmg;
      if(techniqueTurn&&dmg>0&&tech.veneno)playerDots.push({damage:tech.veneno.daño,turns:tech.veneno.turnos||1});
      if(techniqueTurn&&dmg>0&&tech.quemadura)playerDots.push({damage:tech.quemadura.daño,turns:tech.quemadura.turnos||1});
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

function runProfile(profile,runsPerBuild){
  const rows=[];
  for(const [mobId,assignment] of Object.entries(NATIVE_STAGE_BY_MOB)){
    const stage=assignment.stage,configs=configsFor(stage,profile);
    let wins=0,total=0,rounds=0,hpOnWin=0;
    const configRates=[];
    let ci=0;
    for(const pc of configs){
      let configWins=0;
      for(let run=0;run<runsPerBuild;run++){
        const seed=stage*10000000+ci*10000+run*41+mobId.length*73+(profile==='PREPARED'?999:0);
        const result=duel(mobId,pc,seed);
        total++;rounds+=result.rounds;
        if(result.win){wins++;configWins++;hpOnWin+=result.hp;}
      }
      configRates.push(configWins/runsPerBuild);
      ci++;
    }
    configRates.sort((a,b)=>a-b);
    rows.push({
      mobId,stage,role:assignment.role,region:assignment.region,
      winRate:wins/total,
      p10:configRates[Math.floor((configRates.length-1)*.1)],
      median:configRates[Math.floor((configRates.length-1)*.5)],
      p90:configRates[Math.floor((configRates.length-1)*.9)],
      avgRounds:rounds/total,
      hpOnWin:wins?hpOnWin/wins:0
    });
  }
  return rows;
}

const arg=process.argv.find(x=>x.startsWith('--runs='));
const runsPerBuild=arg?Math.max(50,Number(arg.split('=')[1])||500):500;

console.log(JSON.stringify({
  benchmark:'MONSTER_NATIVE_STAGE_PROGRESSION_V01',
  runsPerBuild,
  configCounts:{1:3,2:9,3:27,4:27},
  profiles:Object.fromEntries(Object.entries(PROFILES).map(([id,p])=>[id,p.label])),
  minimal:runProfile('MINIMAL',runsPerBuild),
  prepared:runProfile('PREPARED',runsPerBuild)
},null,2));
