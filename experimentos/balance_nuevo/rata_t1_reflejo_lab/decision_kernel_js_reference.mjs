import {readFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';

const [,,pythonJson,adaptiveRoot]=process.argv;
if(!pythonJson||!adaptiveRoot)throw new Error('usage: node decision_kernel_js_reference.mjs PYTHON_JSON ADAPTIVE_ROOT');

const enginePath=adaptiveRoot+'/experimentos/monstruos/monster-canonical-behavior-lab-v0.1/vendor/monster-engine.mjs';
const profilesPath=adaptiveRoot+'/experimentos/monstruos/monster-canonical-behavior-lab-v0.1/vendor/profiles.mjs';
const {chooseMonsterIntent}=await import(pathToFileURL(enginePath));
const {PROFILES}=await import(pathToFileURL(profilesPath));

const cases=JSON.parse(readFileSync(pythonJson,'utf8'));
const BASIC='rata_qi__basic';
const SURV='rata_qi__survival_1';
const CD=SURV+'__cooldown';

function rng(seed){
  let a=seed>>>0;
  return {random(){
    a|=0;a=(a+0x6d2b79f5)|0;
    let t=Math.imul(a^(a>>>15),1|a);
    t=(t+Math.imul(t^(t>>>7),61|t))^t;
    return ((t^(t>>>14))>>>0)/4294967296;
  }};
}
const abilities={
  [BASIC]:{
    id:BASIC,intentCategory:'OFENSIVA',tags:['BASE_ATTACK'],
    telegraph:'Ataque básico de rata de qi.',requirements:{signalsAll:[]},
    utility:{base:40,signalWeights:{PLAYER_LOW_HP:5},memoryWeights:{},socialWeights:{}}
  },
  [SURV]:{
    id:SURV,intentCategory:'DEFENSA',tags:['SURVIVAL_EVOLUTION_1','EVADE_NEXT'],
    telegraph:'Reflejo de Madriguera.',cooldownKey:CD,requirements:{signalsAll:[]},
    utility:{base:18,signalWeights:{SELF_LOW_HP:22,TOOK_HEAVY_HIT:10,PLAYER_LOW_HP:3},memoryWeights:{},socialWeights:{}}
  }
};

let failed=0;
for(const c of cases){
  const recent=c.recent_actions.map(x=>x==='BASIC'?BASIC:SURV);
  const d=chooseMonsterIntent({
    monster:{
      id:'rata_qi',profileId:'REACTIVO_1',socialProfileId:'COLONIA',
      effectiveKit:[BASIC,SURV],preferences:{OFENSIVA:1,CONTROL:1,DEFENSA:1},
      recentAbilityIds:recent,cooldowns:{[CD]:!!c.cooldown},
    },
    profiles:PROFILES,abilities,
    combat:{round:1,self:{hpRatio:1},player:{hpRatio:1},signals:c.signals},
    memory:[],social:{alliesAlive:0,sameSpeciesAllies:0,outnumbersPlayer:false},
    rng:rng(c.seed),
  });
  const bs=d.debug.scoreByAbility[BASIC] ?? null;
  const ss=d.debug.scoreByAbility[SURV] ?? null;
  const close=(a,b)=>a===null&&b===null || (typeof a==='number'&&typeof b==='number'&&Math.abs(a-b)<1e-12);
  if(d.abilityId!==c.ability_id || !close(bs,c.basic_score) || !close(ss,c.survival_score) || d.debug.tieBrokenByRng!==c.tie_broken_by_rng){
    failed++;
    console.error('PARITY FAIL',c.name,{python:c,js:{ability:d.abilityId,basic:bs,survival:ss,tie:d.debug.tieBrokenByRng}});
  }
}
if(failed)process.exit(1);
console.log('PASS: Python Rata T1 mirror matches original JS kernel on',cases.length,'cases');
