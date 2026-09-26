import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,resolve} from 'node:path';

import snapshot from '../canonical/MOBS_ver74.snapshot.json' with {type:'json'};
import {SURVIVAL_POLICIES} from '../adaptive/survival-evolution-v0.1.mjs';

const here=dirname(fileURLToPath(import.meta.url));
const html=readFileSync(resolve(here,'../../../../grulla-blanca_ver74.html'),'utf8');
const M=snapshot.mobs;

function extractObject(marker){
  const markerAt=html.indexOf(marker);
  if(markerAt<0)throw new Error(`no se encontró ${marker}`);
  const start=html.indexOf('{',markerAt);
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
    if(c==='{')depth++;
    else if(c==='}'&&--depth===0)return html.slice(start,i+1);
  }
  throw new Error(`objeto sin cierre: ${marker}`);
}

const TECNICAS=new Function(`return (${extractObject('const TECNICAS =')})`)();
const RAMAS=new Function(`return (${extractObject('const RAMAS =')})`)();
const RAICES=new Function(`return (${extractObject('const RAICES =')})`)();
const ITEMS=new Function(`return (${extractObject('const ITEMS =')})`)();

const BONO_ELEMENTAL=Number((html.match(/const BONO_ELEMENTAL\s*=\s*([0-9.]+)/)||[])[1]);
const ESQUIVA_INNATA=Number((html.match(/const ESQUIVA_INNATA\s*=\s*([0-9.]+)/)||[])[1]);
const CRIT_MIN_TOPE=Number((html.match(/const CRIT_MIN_TOPE\s*=\s*([0-9]+)/)||[])[1]);
if(!Number.isFinite(BONO_ELEMENTAL)||!Number.isFinite(ESQUIVA_INNATA)||!Number.isFinite(CRIT_MIN_TOPE)){
  throw new Error('constantes de combate de ver74 no encontradas');
}

const CICLO_ELEMENTOS=['fuego','metal','viento','tierra','agua'];

function relacionElemental(a,b){
  if(!a||!b||a===b)return 0;
  const i=CICLO_ELEMENTOS.indexOf(a),j=CICLO_ELEMENTOS.indexOf(b);
  if(i<0||j<0)return 0;
  if((i+1)%CICLO_ELEMENTOS.length===j)return 1;
  if((j+1)%CICLO_ELEMENTOS.length===i)return -1;
  return 0;
}

function diceDistribution(expr){
  const terms=String(expr||'0').replace(/\s/g,'').match(/[+-]?[^+-]+/g)||[];
  let dist=new Map([[0,1]]);
  for(const raw of terms){
    const sign=raw.startsWith('-')?-1:1;
    const body=raw.replace(/^[+-]/,'');
    let term;
    if(body.includes('d')){
      const [nRaw,facesRaw]=body.split('d');
      const n=Number(nRaw||1),faces=Number(facesRaw);
      term=new Map([[0,1]]);
      for(let k=0;k<n;k++){
        const next=new Map();
        for(const [base,p0] of term)for(let roll=1;roll<=faces;roll++){
          const v=base+sign*roll;
          next.set(v,(next.get(v)||0)+p0/faces);
        }
        term=next;
      }
    }else{
      term=new Map([[sign*(Number(body)||0),1]]);
    }
    const next=new Map();
    for(const [a,pa] of dist)for(const [b,pb] of term){
      next.set(a+b,(next.get(a+b)||0)+pa*pb);
    }
    dist=next;
  }
  return dist;
}

function meanDice(expr){
  let total=0;
  for(const [v,p] of diceDistribution(expr))total+=v*p;
  return total;
}

function hit(roll,attack,defense,critMin=20,evasion=ESQUIVA_INNATA){
  if(roll===1)return false;
  if(roll===20||roll>=critMin)return true;
  const evasionExtra=Math.max(0,Math.round((evasion-ESQUIVA_INNATA)/5));
  return roll+attack>=defense+evasionExtra;
}

function lianQiIVAttack(rootId,gearAttack){
  // crearPersonaje: 1 + raíz.ataque. Tres consagraciones hasta LianQi IV,
  // cada una ejecuta p.ataque += 1.
  return 1+(RAICES[rootId]?.ataque||0)+3+gearAttack;
}

function maxAttackGear(){
  const bySlot={};
  for(const it of Object.values(ITEMS)){
    if(!it?.slot||!Number.isFinite(it.ataque))continue;
    bySlot[it.slot]=Math.max(bySlot[it.slot]||0,it.ataque);
  }
  return Object.values(bySlot).reduce((a,b)=>a+b,0);
}

function configLianQi(tid,o1,o2){
  const t=TECNICAS[tid];
  let damage=t.daño,attackBonus=0,critMin=20,critMult=t.critMult||1.5,burn=null,cost=t.coste;
  for(const [rank,opt] of [[1,o1],[2,o2]]){
    const m=RAMAS[tid]?.[rank]?.[opt-1]?.mod||{};
    if(m.daño)damage+=m.daño;
    if(m.ataque)attackBonus+=m.ataque;
    if(m.critMin)critMin=Math.min(critMin,m.critMin);
    if(m.critMult)critMult+=m.critMult-1.5;
    if(m.coste)cost+=m.coste;
    if(m.quemadura){
      burn=burn
        ? {damage:`${burn.damage}+${m.quemadura.daño}`,turns:Math.max(burn.turns,m.quemadura.turnos||1)}
        : {damage:m.quemadura.daño,turns:m.quemadura.turnos||1};
    }
  }
  // Afinidad con la raíz: -1 qi y +1 daño.
  damage+='+1';
  cost=Math.max(Math.ceil(t.coste*0.7),cost-1);
  return {tid,o1,o2,damage,attackBonus,critMin:Math.max(CRIT_MIN_TOPE,critMin),critMult,cost,burn};
}

function afterDefense(raw,effect){
  if(effect.kind==='MITIGATE_NEXT'){
    return Math.max(0,raw-Math.floor(raw*effect.damageReductionPct/100));
  }
  if(effect.kind==='ABSORB_RESERVE'){
    return Math.max(0,raw-Math.min(raw,effect.absorbPerHit));
  }
  return raw;
}

function expectedOneAction({mob,technique,conf,playerAttack,effect}){
  const direct=diceDistribution(conf.damage);
  const burnDist=conf.burn?diceDistribution(conf.burn.damage):null;
  let burnMeanPerTick=0;
  if(burnDist)for(const [v,p] of burnDist)burnMeanPerTick+=v*p;

  let base=0,protectedDamage=0,baseHit=0,protectedHit=0;
  let baseStatus=0,protectedStatus=0;

  const relation=relacionElemental(technique.elemento,mob.elemento);
  const multiplier=1+relation*BONO_ELEMENTAL;

  for(let roll=1;roll<=20;roll++){
    const pRoll=1/20;
    const hitBase=hit(roll,playerAttack+conf.attackBonus,mob.defensa,conf.critMin,ESQUIVA_INNATA);
    let protectedDefense=mob.defensa,protectedEvasion=ESQUIVA_INNATA;
    if(effect.kind==='DEFENSE_UP')protectedDefense+=effect.defenseBonus;
    if(effect.kind==='EVADE_NEXT')protectedEvasion+=effect.evasionBonus;
    const hitProtected=hit(roll,playerAttack+conf.attackBonus,protectedDefense,conf.critMin,protectedEvasion);

    if(hitBase){
      baseHit+=pRoll;
      baseStatus+=pRoll*(conf.burn?burnMeanPerTick*conf.burn.turns:0);
      for(const [rolled,pDamage] of direct){
        let dmg=roll>=conf.critMin?Math.ceil(rolled*conf.critMult):rolled;
        if(relation!==0)dmg=Math.max(1,Math.round(dmg*multiplier));
        base+=pRoll*pDamage*dmg;
      }
    }

    if(hitProtected){
      protectedHit+=pRoll;
      let statusCanApply=false;
      for(const [rolled,pDamage] of direct){
        let dmg=roll>=conf.critMin?Math.ceil(rolled*conf.critMult):rolled;
        if(relation!==0)dmg=Math.max(1,Math.round(dmg*multiplier));
        const final=afterDefense(dmg,effect);
        protectedDamage+=pRoll*pDamage*final;
        if(final>0)statusCanApply=true;
      }
      // En ver74 los estados ligados al golpe sólo se aplican si el daño final
      // sigue >0. La probabilidad de daño=0 es mínima pero se conserva el contrato.
      if(conf.burn&&statusCanApply){
        protectedStatus+=pRoll*burnMeanPerTick*conf.burn.turns;
      }
    }
  }

  return {
    baseDirect:base,
    protectedDirect:protectedDamage,
    baseStatus,
    protectedStatus,
    baseTotal:base+baseStatus,
    protectedTotal:protectedDamage+protectedStatus,
    prevented:(base+baseStatus)-(protectedDamage+protectedStatus),
    hitBefore:baseHit,
    hitAfter:protectedHit
  };
}

const rootArts=Object.entries(RAICES).map(([root,r])=>({root,tid:r.tecnica,technique:TECNICAS[r.tecnica]}));
const gearAttack=maxAttackGear();
const arsenal=rootArts.map(({root,tid,technique})=>{
  const configs=[];
  for(let o1=1;o1<=3;o1++)for(let o2=1;o2<=3;o2++)configs.push(configLianQi(tid,o1,o2));
  return {
    root,tid,name:technique.name,element:technique.elemento,
    qiMax:110,playerAttack:lianQiIVAttack(root,gearAttack),gearAttack,
    baseDamage:technique.daño,
    configuredMeanRange:[
      Math.min(...configs.map(c=>meanDice(c.damage))),
      Math.max(...configs.map(c=>meanDice(c.damage)))
    ],
    directRollRange:[
      Math.min(...configs.flatMap(c=>[...diceDistribution(c.damage).keys()])),
      Math.max(...configs.flatMap(c=>[...diceDistribution(c.damage).keys()]))
    ],
    attackBonusMax:Math.max(...configs.map(c=>c.attackBonus)),
    critMinBest:Math.min(...configs.map(c=>c.critMin)),
    costRange:[Math.min(...configs.map(c=>c.cost)),Math.max(...configs.map(c=>c.cost))],
    maxBurnExpected:Math.max(...configs.map(c=>c.burn?meanDice(c.burn.damage)*c.burn.turns:0))
  };
});

const monsters=[];
for(const [mobId,mob] of Object.entries(M)){
  if(mobId==='muneco_practica')continue;
  const effect=SURVIVAL_POLICIES[mobId].effect;
  const samples=[];
  for(const {root,tid,technique} of rootArts){
    for(let o1=1;o1<=3;o1++)for(let o2=1;o2<=3;o2++){
      const conf=configLianQi(tid,o1,o2);
      samples.push({
        root,tid,path:`${o1}${o2}`,
        ...expectedOneAction({
          mob,technique,conf,
          playerAttack:lianQiIVAttack(root,gearAttack),
          effect
        })
      });
    }
  }
  const avg=k=>samples.reduce((sum,x)=>sum+x[k],0)/samples.length;
  const ratios=samples.map(x=>x.baseTotal>0?100*x.prevented/x.baseTotal:0);
  monsters.push({
    mobId,hp:mob.hp,defense:mob.defensa,kind:effect.kind,effect,
    avgIncoming:+avg('baseTotal').toFixed(3),
    avgPrevented:+avg('prevented').toFixed(3),
    avgPreventedPct:+(ratios.reduce((a,b)=>a+b,0)/ratios.length).toFixed(2),
    preventedAsHpPct:+(100*avg('prevented')/mob.hp).toFixed(2),
    minPreventedPct:+Math.min(...ratios).toFixed(2),
    maxPreventedPct:+Math.max(...ratios).toFixed(2)
  });
}

console.log(JSON.stringify({
  benchmark:'PLAYER_ARSENAL_VS_SURVIVAL_E1_V01',
  scope:{
    arc:'Arco I / LianQi IV',
    branchRanks:[1,2],
    rootOffensiveArts:rootArts.map(x=>x.tid),
    gearAttack,
    note:'Rango 3 y técnicas ZhuJi se excluyen del balance objetivo; pertenecen a stress test futuro.'
  },
  arsenal,
  monsters
},null,2));
