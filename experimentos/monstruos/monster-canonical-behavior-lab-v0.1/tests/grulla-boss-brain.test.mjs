import assert from 'node:assert/strict';
import {
  GRULLA_ABILITIES as A,
  initialGrullaBrainState,
  enterGrullaPhase,
  chooseGrullaIntent,
  observeResolvedPlayerAction,
  interruptGrullaPlan,
  grullaCapabilitySnapshot,
  grullaTechniqueEffectiveness
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const fixed=()=>.5;
const tech=(id,element='fuego',qiSpent=6,damageBand='NORMAL',techniqueRole='ofensiva')=>({type:'TECHNIQUE',techniqueId:id,techniqueRole,element,qiSpent,damageBand});

T('Fase I is programmed and ignores player pattern',()=>{
  let s=initialGrullaBrainState({phase:1});
  const got=[];
  for(let i=0;i<8;i++){
    const r=chooseGrullaIntent({state:s,context:{playerHpRatio:.5,playerQiRatio:.5},rng:fixed});
    got.push(r.intent.id);s=r.state;
    s=observeResolvedPlayerAction(s,i%2?tech('palma'):{type:'DEFEND'}).state;
  }
  assert.deepEqual(got,[A.GOLPE_ALA,A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL,A.GOLPE_ALA,A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL]);
});

T('Fase II punishes repeated technique with Recordar el Filo',()=>{
  let s=initialGrullaBrainState({phase:2});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  const r=chooseGrullaIntent({state:s,context:{playerHpRatio:.8,playerQiRatio:.5,selfHpRatio:.8},rng:fixed});
  assert.equal(r.intent.id,A.RECORDAR_FILO);
});

T('Fase II distinguishes qi-heavy play from elemental spam',()=>{
  let s=initialGrullaBrainState({phase:2});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('filo','metal')).state;
  const r=chooseGrullaIntent({state:s,context:{playerHpRatio:.8,playerQiRatio:.5,selfHpRatio:.8},rng:fixed});
  assert.equal(r.intent.id,A.ECO_MERIDIANO);
});

T('Fase II inherits only a summary from Fase I',()=>{
  let s=initialGrullaBrainState({phase:1});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=enterGrullaPhase(s,2);
  assert.equal(s.history.length,0);
  assert.equal(s.phaseMemory.phase1.dominantTechnique,'palma');
  assert.equal(s.phaseMemory.phase1.dominantElement,'fuego');
});

T('Fase III anti-repeat plan can be broken by variation',()=>{
  let s=initialGrullaBrainState({phase:3});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  const r=chooseGrullaIntent({state:s,context:{playerHpRatio:.7,playerQiRatio:.4,selfHpRatio:.8},rng:fixed});
  assert.equal(r.intent.id,A.SILENCIO_ENTRE_CAMPANAS);
  const o=observeResolvedPlayerAction(r.state,tech('filo','metal'));
  assert.equal(o.event,'PLAN_BROKEN_BY_VARIATION');
  assert.equal(o.state.plan,null);
});

T('Fase III completes anti-repeat plan only after observed repetition',()=>{
  let s=initialGrullaBrainState({phase:3});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  let r=chooseGrullaIntent({state:s,context:{playerHpRatio:.7,playerQiRatio:.4,selfHpRatio:.8},rng:fixed});
  let o=observeResolvedPlayerAction(r.state,tech('palma','fuego'));
  assert.equal(o.event,'PLAN_ARMED');
  r=chooseGrullaIntent({state:o.state,context:{playerHpRatio:.7,playerQiRatio:.3,selfHpRatio:.8},rng:fixed});
  assert.equal(r.intent.id,A.ROMPER_RITMO);
  assert.equal(r.intent.committed,true);
  o=observeResolvedPlayerAction(r.state,{type:'DEFEND'});
  assert.equal(o.event,'PLAN_COMPLETED');
});

T('Fase III qi plan is breakable with a zero-qi action',()=>{
  let s=initialGrullaBrainState({phase:3});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('filo','metal')).state;
  const r=chooseGrullaIntent({state:s,context:{playerHpRatio:.7,playerQiRatio:.8,selfHpRatio:.8},rng:fixed});
  assert.equal(r.intent.id,A.BUSCAR_PULSO);
  const o=observeResolvedPlayerAction(r.state,{type:'BASIC',damageBand:'LOW'});
  assert.equal(o.event,'PLAN_BROKEN_BY_RESOURCE_DISCIPLINE');
});

T('interruption clears a prepared plan',()=>{
  let s=initialGrullaBrainState({phase:3});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  const r=chooseGrullaIntent({state:s,context:{playerHpRatio:.7,playerQiRatio:.4,selfHpRatio:.8},rng:fixed});
  assert.ok(r.state.plan);
  assert.equal(interruptGrullaPlan(r.state).plan,null);
});

T('capability snapshot does not expose future or hidden player data',()=>{
  let s=initialGrullaBrainState({phase:3});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  const snap=grullaCapabilitySnapshot(s,{playerHpRatio:.5,playerQiRatio:.5});
  assert.equal(snap.brain,'MAESTRA');
  assert.equal(Object.hasOwn(snap,'futureAction'),false);
  assert.equal(Object.hasOwn(snap,'inventory'),false);
  assert.equal(Object.hasOwn(snap,'playerCooldowns'),false);
});

T('future/hidden context fields do not change the decision',()=>{
  let s=initialGrullaBrainState({phase:2});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  const a=chooseGrullaIntent({state:s,context:{playerHpRatio:.8,playerQiRatio:.5,selfHpRatio:.8},rng:fixed}).intent.id;
  const b=chooseGrullaIntent({state:s,context:{playerHpRatio:.8,playerQiRatio:.5,selfHpRatio:.8,futureAction:'DEFEND',inventory:['elixir'],secretCooldown:99},rng:fixed}).intent.id;
  assert.equal(a,b);
});



T('pure single-skill spam in Fase I is hard-countered on entry to Fase II',()=>{
  let s=initialGrullaBrainState({phase:1});
  for(let i=0;i<4;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=enterGrullaPhase(s,2);
  assert.equal(s.techniqueCounter.techniqueId,'palma');
  assert.equal(s.techniqueCounter.locked,true);
  const e=grullaTechniqueEffectiveness(s,tech('palma','fuego'));
  assert.equal(e.blocked,true);
  assert.equal(e.multiplier,0);
  assert.equal(e.suppressEffects,true);
  assert.equal(e.suppressDamage,true);
  assert.equal(e.suppressControl,true);
  assert.equal(e.suppressAfflictions,true);
  assert.equal(e.suppressResourceEffects,true);
});

T('three consecutive uses lock a technique and variation breaks the lock',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  assert.equal(s.techniqueCounter.techniqueId,'palma');
  assert.equal(grullaTechniqueEffectiveness(s,tech('palma','fuego')).multiplier,0);
  const other=tech('filo','metal');
  assert.equal(grullaTechniqueEffectiveness(s,other).multiplier,1);
  const o=observeResolvedPlayerAction(s,other);
  assert.equal(o.event,'TECHNIQUE_COUNTER_BROKEN_BY_VARIATION');
  assert.equal(o.state.techniqueCounter,null);
});

T('100 percent same-skill strategy deals zero effective damage after Fase I learning',()=>{
  let s=initialGrullaBrainState({phase:1});
  for(let i=0;i<4;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=enterGrullaPhase(s,2);
  let effectiveDamage=0;
  for(let i=0;i<20;i++){
    const action=tech('palma','fuego');
    const eff=grullaTechniqueEffectiveness(s,action);
    effectiveDamage+=999*eff.multiplier;
    s=observeResolvedPlayerAction(s,action).state;
  }
  assert.equal(effectiveDamage,0);
});


T('defending or recovering does not erase a learned technique counter',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  assert.equal(s.techniqueCounter.techniqueId,'palma');

  s=observeResolvedPlayerAction(s,{type:'DEFEND'}).state;
  assert.equal(s.techniqueCounter.techniqueId,'palma');
  assert.equal(grullaTechniqueEffectiveness(s,tech('palma','fuego')).blocked,true);

  s=observeResolvedPlayerAction(s,{type:'RECOVER'}).state;
  assert.equal(s.techniqueCounter.techniqueId,'palma');
  assert.equal(grullaTechniqueEffectiveness(s,tech('palma','fuego')).blocked,true);
});

T('a basic attack is meaningful variation and breaks the learned technique counter',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  const o=observeResolvedPlayerAction(s,{type:'BASIC',damageBand:'LOW'});
  assert.equal(o.event,'TECHNIQUE_COUNTER_BROKEN_BY_VARIATION');
  assert.equal(o.state.techniqueCounter,null);
});

T('single-skill reliance in Fase I survives defensive filler and locks on Fase II entry',()=>{
  let s=initialGrullaBrainState({phase:1});
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,{type:'DEFEND'}).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=observeResolvedPlayerAction(s,{type:'RECOVER'}).state;
  s=observeResolvedPlayerAction(s,tech('palma','fuego')).state;
  s=enterGrullaPhase(s,2);
  assert.equal(s.techniqueCounter.techniqueId,'palma');
  assert.equal(s.techniqueCounter.techniqueRole,'ofensiva');
  assert.equal(s.techniqueCounter.source,'PHASE1_SINGLE_SKILL_RELIANCE');
});

T('learned offensive skill uses Trazo Vacio contract',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,tech('palma','fuego',6,'NORMAL','ofensiva')).state;
  const e=grullaTechniqueEffectiveness(s,tech('palma','fuego',6,'NORMAL','ofensiva'));
  assert.equal(e.counterMode,'TRAZO_VACIO');
  assert.equal(e.primarySuppression,'DAMAGE_AND_SECONDARY');
  assert.equal(e.suppressDamage,true);
  assert.equal(e.consumeQi,true);
  assert.equal(e.refundQi,false);
});

T('learned evasion skill uses Pulso Fijado contract',()=>{
  let s=initialGrullaBrainState({phase:2});
  const paso=()=>tech('paso_nube','viento',5,'NONE','esquiva');
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,paso()).state;
  const e=grullaTechniqueEffectiveness(s,paso());
  assert.equal(e.counterMode,'PULSO_FIJADO');
  assert.equal(e.primarySuppression,'EVASION');
  assert.equal(e.suppressEvasion,true);
});

T('learned guard skill uses Resonancia Interna contract',()=>{
  let s=initialGrullaBrainState({phase:2});
  const piel=()=>tech('piel_cobre','tierra',5,'NONE','guardia');
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,piel()).state;
  const e=grullaTechniqueEffectiveness(s,piel());
  assert.equal(e.counterMode,'RESONANCIA_INTERNA');
  assert.equal(e.primarySuppression,'GUARD');
  assert.equal(e.suppressGuard,true);
});

T('learned fortification skill uses Campana Inversa contract',()=>{
  let s=initialGrullaBrainState({phase:2});
  const espejo=()=>tech('espejo_luna','agua',8,'NONE','fortificacion');
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,espejo()).state;
  const e=grullaTechniqueEffectiveness(s,espejo());
  assert.equal(e.counterMode,'CAMPANA_INVERSA');
  assert.equal(e.primarySuppression,'DEFENSE_BUFF');
  assert.equal(e.suppressDefenseBuff,true);
});

T('learned control skill uses Ancla del Voto contract',()=>{
  let s=initialGrullaBrainState({phase:2});
  const filamento=()=>({type:'CONTROL',techniqueId:'filamento',techniqueRole:'control',element:'agua',qiSpent:6,damageBand:'NONE'});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,filamento()).state;
  const e=grullaTechniqueEffectiveness(s,filamento());
  assert.equal(e.counterMode,'ANCLA_DEL_VOTO');
  assert.equal(e.primarySuppression,'CONTROL');
  assert.equal(e.suppressControl,true);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
