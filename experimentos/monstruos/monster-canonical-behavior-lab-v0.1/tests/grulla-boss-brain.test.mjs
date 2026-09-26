import assert from 'node:assert/strict';
import {
  GRULLA_ABILITIES as A,
  initialGrullaBrainState,
  enterGrullaPhase,
  chooseGrullaIntent,
  observeResolvedPlayerAction,
  interruptGrullaPlan,
  grullaCapabilitySnapshot
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};
const fixed=()=>.5;
const tech=(id,element='fuego',qiSpent=6,damageBand='NORMAL')=>({type:'TECHNIQUE',techniqueId:id,element,qiSpent,damageBand});

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

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
