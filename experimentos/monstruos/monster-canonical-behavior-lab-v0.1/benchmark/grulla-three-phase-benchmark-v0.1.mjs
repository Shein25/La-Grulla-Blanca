import {
  GRULLA_ABILITIES as A,
  initialGrullaBrainState,
  enterGrullaPhase,
  chooseGrullaIntent,
  observeResolvedPlayerAction,
  grullaTechniqueEffectiveness
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

export const STATUS='EXPERIMENTAL_CALIBRATION_ONLY_V01';
const CRIT_MULT=1.5, EVA_BASE=5;

// Snapshot mínimo de ver74: tres raíces de LianQi y ramas disponibles hasta maestría 2.
const ROOTS={
 fuego:{tech:'palma',attack:1,defense:0,element:'fuego',baseCost:7,baseDamage:'2d6+2',r1:[{burn:['1d3',2]},{damage:'+1d4'},{attack:3}],r2:[{cost:-1},{attack:4},{critMin:19}]},
 metal:{tech:'filo',attack:2,defense:0,element:'metal',baseCost:6,baseDamage:'1d10+3',r1:[{attack:3},{damage:'+1d4'},{critMin:19}],r2:[{cost:-1,critMin:19},{attack:4},{debil:[-2,1]}]},
 agua:{tech:'latigo',attack:0,defense:2,element:'agua',baseCost:6,baseDamage:'2d6',r1:[{debil:[-1,1]},{damage:'+1d4'},{attack:3}],r2:[{cost:-1},{attack:4},{critMin:19}]}
};

const GEAR={attack:2,defense:7,basic:'1d8'};
const PHASE={
 1:{hp:150,attack:3,defense:13,basic:'1d6+2'},
 2:{hp:100,attack:3,defense:13,basic:'1d6+3'},
 3:{hp:50,attack:5,defense:12,basic:'1d8+4'}
};

// Efectos provisionales: sólo reutilizan conceptos que Combate ya soporta.
const FX={
 [A.GOLPE_ALA]:{kind:'ATTACK'},
 [A.CAMPANADA_PICO]:{kind:'ATTACK',attackBonus:3,damage:'2d6+2'},
 [A.PATA_INMOVIL]:{kind:'DEFENSE_NEXT',p1:3,p3:5},
 [A.TORMENTA_MIL_PLUMAS]:{kind:'ATTACK',attackBonus:3,damage:'2d6+3',drain:2},
 [A.CERRAR_ALAS]:{kind:'ABSORB',perHit:4,reserve:8},
 [A.RECORDAR_FILO]:{kind:'EVADE_NEXT',bonus:20},
 [A.ECO_MERIDIANO]:{kind:'DRAIN',drain:4},
 [A.PICOTAZO_BLANCO]:{kind:'ATTACK',attackBonus:2},
 [A.CAMPANA_SIN_DUENO]:{kind:'ATTACK',attackBonus:5,damage:'2d8+5',drain:4},
 [A.ALA_VACIA]:{kind:'EVADE_NEXT',bonus:25},
 [A.SILENCIO_ENTRE_CAMPANAS]:{kind:'PREP'},
 [A.ROMPER_RITMO]:{kind:'ATTACK',attackBonus:4,damage:'2d8+3'},
 [A.BUSCAR_PULSO]:{kind:'PREP'}
};

function rng32(seed){let x=seed|0;return ()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296;};}
function d20(r){return 1+Math.floor(r()*20);}
function roll(expr,r){let z=0;for(const raw of String(expr||0).replace(/\s/g,'').match(/[+-]?[^+-]+/g)||[]){const sign=raw[0]==='-'?-1:1;const t=raw.replace(/^[+-]/,'');if(t.includes('d')){const q=t.split('d'),n=Number(q[0])||1,f=Number(q[1]);for(let i=0;i<n;i++)z+=sign*(1+Math.floor(r()*f));}else z+=sign*(Number(t)||0);}return z;}
function impact(r,atk,def,critMin=20,eva=5){const x=d20(r);if(x===1)return [false,false];if(x===20||x>=critMin)return [true,x>=critMin];const extra=Math.max(0,Math.round((eva-EVA_BASE)/5));return [x+atk>=def+extra,false];}
function damage(expr,crit,mult,r){const n=roll(expr,r);return crit?Math.ceil(n*mult):n;}

function build(root,o1,o2){
 const q=ROOTS[root],mods=[q.r1[o1-1],q.r2[o2-1]];
 let cost=q.baseCost,expr=q.baseDamage,attackBonus=0,critMin=20,burn=null,debil=null;
 for(const m of mods){if(m.cost)cost+=m.cost;if(m.damage)expr+=m.damage;if(m.attack)attackBonus+=m.attack;if(m.critMin)critMin=Math.min(critMin,m.critMin);if(m.burn)burn=m.burn;if(m.debil)debil=m.debil;}
 // Afinidad principal exacta de statsTecnica(): -1 qi, +1 daño, suelo 70%.
 cost=Math.max(Math.ceil(q.baseCost*.7),Math.max(1,cost-1));expr+='+1';
 return {root,tech:q.tech,element:q.element,hp:28,maxHp:28,qi:110,maxQi:110,attack:1+q.attack+3+GEAR.attack,defense:10+q.defense+GEAR.defense,basic:GEAR.basic,cost,expr,attackBonus,critMin,critMult:1.5,burn,debil,potions:1};
}

const techAction=p=>({type:'TECHNIQUE',techniqueId:p.tech,techniqueRole:'ofensiva',element:p.element,qiSpent:p.cost,damageBand:'NORMAL'});
const basic=()=>({type:'BASIC',qiSpent:0,damageBand:'LOW'});
const defend=()=>({type:'DEFEND',qiSpent:0,damageBand:'NONE'});
const recover=()=>({type:'RECOVER',qiSpent:0,damageBand:'NONE'});

function choosePlayer(strategy,p,intent,brain,totalRound){
 const locked=brain.techniqueCounter?.locked&&brain.techniqueCounter.techniqueId===p.tech;
 const heavy=[A.CAMPANADA_PICO,A.TORMENTA_MIL_PLUMAS,A.CAMPANA_SIN_DUENO,A.ROMPER_RITMO].includes(intent.id);
 if(strategy==='PURE_SINGLE_SKILL')return p.qi>=p.cost?techAction(p):defend();
 if(strategy==='SINGLE_SKILL_WITH_DEFENSE')return heavy?defend():(p.qi>=p.cost?techAction(p):defend());
 if(strategy==='MINIMAL_ALTERNATE'){if(p.hp<=p.maxHp*.30&&p.potions>0)return recover();return totalRound%2?techAction(p):basic();}
 if(strategy==='MINIMAL_READER'){
   if(p.hp<=p.maxHp*.35&&p.potions>0)return recover();
   if(locked||[A.SILENCIO_ENTRE_CAMPANAS,A.BUSCAR_PULSO,A.RECORDAR_FILO].includes(intent.id))return basic();
   if(intent.id===A.ROMPER_RITMO||(heavy&&p.hp<=p.maxHp*.60))return defend();
   const last=brain.history.at(-1);
   if(p.qi>=p.cost&&last?.techniqueId!==p.tech)return techAction(p);
   return basic();
 }
 throw new RangeError('strategy '+strategy);
}

function newGuard(r){return [35+Math.floor(r()*16),25+Math.floor(r()*16)];}
function guardDamage(g,d){if(!g?.length||d<=0)return [d,g];const a=Math.floor(d*g[0]/100);return [d-a,g.slice(1)];}

function duel(base,strategy,seed){
 const r=rng32(seed),p={...base,hp:base.maxHp,qi:base.maxQi,potions:1};
 let brain=initialGrullaBrainState({phase:1}),guard=null,total=0;
 for(let phase=1;phase<=3;phase++){
   if(phase>1)brain=enterGrullaPhase(brain,phase);
   // La transición limpia estados aplicados a la manifestación anterior.
   const st=PHASE[phase];let bossHp=st.hp,defNext=0,evaNext=0,reserve=0,burn=null,debil=0,debilTurns=0;
   while(bossHp>0&&p.hp>0&&total<90){
     total++;
     const sel=chooseGrullaIntent({state:brain,context:{playerHpRatio:Math.max(0,p.hp/p.maxHp),playerQiRatio:Math.max(0,p.qi/p.maxQi),selfHpRatio:Math.max(0,bossHp/st.hp)},rng:r});
     const intent=sel.intent;brain=sel.state;
     let act=choosePlayer(strategy,p,intent,brain,total);

     if(act.type==='RECOVER'){p.potions--;p.hp=Math.min(p.maxHp,p.hp+roll('3d6+6',r));}
     else if(act.type==='DEFEND'){guard=newGuard(r);p.qi=Math.min(p.maxQi,p.qi+3);}
     else if(act.type==='TECHNIQUE'){
       if(p.qi<p.cost){act=defend();guard=newGuard(r);p.qi=Math.min(p.maxQi,p.qi+3);}
       else{
         p.qi-=p.cost;
         const eff=grullaTechniqueEffectiveness(brain,act);
         if(!eff.blocked){
           const hit=impact(r,p.attack+p.attackBonus,st.defense+defNext,p.critMin,EVA_BASE+evaNext);
           if(hit[0]){let dmg=damage(p.expr,hit[1],p.critMult,r);if(reserve>0){const a=Math.min(dmg,4,reserve);dmg-=a;reserve-=a;}bossHp-=dmg;act={...act,damageBand:dmg>=8?'HEAVY':'NORMAL'};if(dmg>0&&p.burn)burn={expr:p.burn[0],turns:p.burn[1]};if(dmg>0&&p.debil){debil=p.debil[0];debilTurns=p.debil[1];}}
         }
       }
     }else if(act.type==='BASIC'){
       const hit=impact(r,p.attack,st.defense+defNext,20,EVA_BASE+evaNext);
       if(hit[0]){let dmg=damage(p.basic,hit[1],CRIT_MULT,r);if(reserve>0){const a=Math.min(dmg,4,reserve);dmg-=a;reserve-=a;}bossHp-=dmg;act={...act,damageBand:dmg>=8?'HEAVY':'LOW'};}
     }
     if(['TECHNIQUE','BASIC','CONTROL'].includes(act.type)){defNext=0;evaNext=0;}
     if(bossHp<=0){brain=observeResolvedPlayerAction(brain,act).state;break;}

     const fx=FX[intent.id];
     if(fx.kind==='DEFENSE_NEXT')defNext=phase===1?fx.p1:fx.p3;
     else if(fx.kind==='ABSORB')reserve=fx.reserve;
     else if(fx.kind==='EVADE_NEXT')evaNext=fx.bonus;
     else if(fx.kind==='DRAIN')p.qi=Math.max(0,p.qi-fx.drain);
     else if(fx.kind==='ATTACK'){
       const hit=impact(r,st.attack+(fx.attackBonus||0)+(debilTurns>0?debil:0),p.defense,20,EVA_BASE);
       if(hit[0]){let dmg=damage(fx.damage||st.basic,hit[1],CRIT_MULT,r);const gd=guardDamage(guard,dmg);dmg=gd[0];guard=gd[1]?.length?gd[1]:null;p.hp-=dmg;if(dmg>0&&fx.drain)p.qi=Math.max(0,p.qi-fx.drain);}
     }
     if(burn&&bossHp>0){bossHp-=roll(burn.expr,r);burn.turns--;if(burn.turns<=0)burn=null;}
     if(debilTurns>0){debilTurns--;if(debilTurns<=0)debil=0;}
     brain=observeResolvedPlayerAction(brain,act).state;
   }
   if(p.hp<=0||bossHp>0)return {win:false,phaseReached:phase,rounds:total,hp:Math.max(0,p.hp),qi:p.qi};
 }
 return {win:true,phaseReached:3,rounds:total,hp:p.hp,qi:p.qi};
}

const STRATEGIES=['PURE_SINGLE_SKILL','SINGLE_SKILL_WITH_DEFENSE','MINIMAL_ALTERNATE','MINIMAL_READER'];
const roots=Object.keys(ROOTS);
const arg=process.argv.find(x=>x.startsWith('--runs='));
const runs=arg?Math.max(50,Number(arg.split('=')[1])||500):500;
const rows=[];
for(const root of roots)for(let o1=1;o1<=3;o1++)for(let o2=1;o2<=3;o2++)for(const strategy of STRATEGIES){
 const p=build(root,o1,o2);let wins=0,rounds=0,hp=0,qi=0;
 for(let i=0;i<runs;i++){const seed=(roots.indexOf(root)+1)*100000000+o1*1000000+o2*10000+STRATEGIES.indexOf(strategy)*1000+i*97+1337;const z=duel(p,strategy,seed);wins+=z.win?1:0;rounds+=z.rounds;hp+=z.hp;qi+=z.qi;}
 rows.push({root,o1,o2,strategy,runs,winRate:wins/runs,avgRounds:rounds/runs,avgHp:hp/runs,avgQi:qi/runs});
}
function summary(strategy){const out={};for(const root of roots){const x=rows.filter(r=>r.strategy===strategy&&r.root===root);out[root]={avgWinRate:x.reduce((s,v)=>s+v.winRate,0)/x.length,minBuildWinRate:Math.min(...x.map(v=>v.winRate)),maxBuildWinRate:Math.max(...x.map(v=>v.winRate))};}return out;}
const invariants={
 pureSingleSkillZeroWins:rows.filter(r=>r.strategy==='PURE_SINGLE_SKILL').every(r=>r.winRate===0),
 singleSkillWithDefenseZeroWins:rows.filter(r=>r.strategy==='SINGLE_SKILL_WITH_DEFENSE').every(r=>r.winRate===0),
 everyRootHasMinimalReaderWins:roots.every(root=>rows.some(r=>r.root===root&&r.strategy==='MINIMAL_READER'&&r.winRate>0)),
 noOptionalTechniqueRequired:true
};
console.log(JSON.stringify({benchmark:'GRULLA_THREE_PHASE_BENCHMARK_V01',status:STATUS,runsPerBuild:runs,totalBuilds:27,assumptions:{player:'LianQi IV, maestria 2, 9 combinaciones por raiz, gear preparado +2 ATQ/+7 DEF/1d8',optionalTechniques:'Paso/Piel/Filamento NO usados',bossStats:'150/100/50 HP del combate previo de referencia; balance nuevo aun no canonico',intentOrder:'plan -> telegraph -> jugador -> intent comprometida -> observacion'},invariants,summary:Object.fromEntries(STRATEGIES.map(s=>[s,summary(s)])),rows},null,2));
if(!invariants.pureSingleSkillZeroWins)process.exitCode=2;
if(!invariants.singleSkillWithDefenseZeroWins)process.exitCode=3;
if(!invariants.everyRootHasMinimalReaderWins)process.exitCode=4;
