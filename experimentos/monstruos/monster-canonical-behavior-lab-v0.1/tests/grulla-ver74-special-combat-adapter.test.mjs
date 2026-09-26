import assert from 'node:assert/strict';

import {GRULLA_ABILITIES as A} from '../adaptive/grulla-boss-brain-v0.1.mjs';
import {
  GRULLA_SPECIAL_COMBAT_TAG,
  isGrullaSpecialCombat,
  createGrullaSpecialCombatState,
  grullaSpecialProfile,
  gateGrullaSpecialTechnique,
  observeGrullaSpecialPlayerResolved,
  chooseGrullaSpecialEnemyAction,
  markGrullaSpecialEnemyActionResolved,
  resolveGrullaSpecialPhase1Wing,
  applyGrullaSpecialBossDamage,
  grullaSpecialPublicSnapshot
} from '../integration/grulla-ver74-special-combat-adapter-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{
  try{fn();pass++;console.log('PASS',name);}
  catch(err){fail++;console.error('FAIL',name);console.error(err.stack||err);}
};
const fixed=()=>.5;

T('special tag is explicit and does not match generic combat',()=>{
  assert.equal(GRULLA_SPECIAL_COMBAT_TAG,'grulla_boss_v01');
  assert.equal(isGrullaSpecialCombat('grulla_boss_v01'),true);
  assert.equal(isGrullaSpecialCombat(null),false);
  assert.equal(isGrullaSpecialCombat('practica'),false);
});

T('special state starts with closed Phase I pool',()=>{
  const s=createGrullaSpecialCombatState();
  const p=grullaSpecialProfile(s);
  assert.equal(s.session.phase,1);
  assert.equal(s.session.phaseHp,150);
  assert.equal(p.defense,13);
});

T('foreign special tag cannot silently create Grulla state',()=>{
  assert.throws(
    ()=>createGrullaSpecialCombatState({especial:'otro_especial'}),
    /NOT_GRULLA_SPECIAL_COMBAT/
  );
});

T('Phase I overkill transitions to fresh Phase II without defeating encounter',()=>{
  let s=createGrullaSpecialCombatState();
  const r=applyGrullaSpecialBossDamage(s,999);

  assert.equal(r.appliedDamage,150);
  assert.equal(r.phaseDefeated,true);
  assert.equal(r.encounterDefeated,false);
  assert.deepEqual(r.phaseTransition,{from:1,to:2,nextHp:100});
  assert.equal(r.state.session.phase,2);
  assert.equal(r.state.session.phaseHp,100);
});

T('Phase II overkill transitions to fresh Phase III',()=>{
  let s=createGrullaSpecialCombatState({phase:2});
  const r=applyGrullaSpecialBossDamage(s,999);

  assert.equal(r.appliedDamage,100);
  assert.equal(r.phaseDefeated,true);
  assert.equal(r.encounterDefeated,false);
  assert.deepEqual(r.phaseTransition,{from:2,to:3,nextHp:50});
  assert.equal(r.state.session.phaseHp,50);
});

T('only Phase III defeat ends the encounter',()=>{
  let s=createGrullaSpecialCombatState({phase:3});
  const r=applyGrullaSpecialBossDamage(s,999);

  assert.equal(r.appliedDamage,50);
  assert.equal(r.phaseDefeated,true);
  assert.equal(r.encounterDefeated,true);
  assert.equal(r.phaseTransition,null);
  assert.equal(r.state.session.phaseHp,0);
});

T('nonlethal boss damage keeps the same phase',()=>{
  let s=createGrullaSpecialCombatState();
  const r=applyGrullaSpecialBossDamage(s,40);

  assert.equal(r.phaseDefeated,false);
  assert.equal(r.encounterDefeated,false);
  assert.equal(r.phaseTransition,null);
  assert.equal(r.state.session.phase,1);
  assert.equal(r.state.session.phaseHp,110);
});

T('player resolved observation happens independently from technique gate',()=>{
  let s=createGrullaSpecialCombatState({phase:2});

  const signal={
    kind:'TECHNIQUE',
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5,
    damage:0
  };

  for(let i=0;i<3;i++){
    const gate=gateGrullaSpecialTechnique(s,signal);
    assert.equal(gate.blocked,false,'gate '+(i+1));
    s=observeGrullaSpecialPlayerResolved(s,signal).state;
  }

  const fourth=gateGrullaSpecialTechnique(s,signal);
  assert.equal(fourth.blocked,true);
  assert.equal(fourth.counterMode,'RESONANCIA_INTERNA');
});

T('BASIC observation breaks a learned special-combat gate',()=>{
  let s=createGrullaSpecialCombatState({phase:2});
  const piel={
    kind:'TECHNIQUE',
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5,
    damage:0
  };

  for(let i=0;i<3;i++)s=observeGrullaSpecialPlayerResolved(s,piel).state;
  assert.equal(gateGrullaSpecialTechnique(s,piel).blocked,true);

  const o=observeGrullaSpecialPlayerResolved(s,{kind:'BASIC',damage:4});
  s=o.state;

  assert.equal(o.event,'TECHNIQUE_COUNTER_BROKEN_BY_VARIATION');
  assert.equal(gateGrullaSpecialTechnique(s,piel).blocked,false);
});

T('Phase I Pata resolved arms Resonance through special adapter',()=>{
  let s=createGrullaSpecialCombatState();
  let chosen;

  for(let i=0;i<4;i++){
    chosen=chooseGrullaSpecialEnemyAction(s,{context:{},rng:fixed});
    s=chosen.state;
  }

  assert.equal(chosen.intent.id,A.PATA_INMOVIL);
  s=markGrullaSpecialEnemyActionResolved(s,chosen.runtime);

  assert.equal(grullaSpecialPublicSnapshot(s).resonancePrepared,true);
});

T('special Phase I wing applies Resonance then Piel and clears preparation',()=>{
  let s=createGrullaSpecialCombatState();
  let chosen;

  for(let i=0;i<4;i++){
    chosen=chooseGrullaSpecialEnemyAction(s,{context:{},rng:fixed});
    s=chosen.state;
  }
  s=markGrullaSpecialEnemyActionResolved(s,chosen.runtime);

  const wing=resolveGrullaSpecialPhase1Wing(s,{
    hit:true,
    rawDamage:10,
    guardActive:true,
    guardPerHit:5,
    guardCapacity:10
  });

  assert.equal(wing.resolution.afterResonance,18);
  assert.equal(wing.resolution.absorbed,5);
  assert.equal(wing.resolution.hpDamage,13);
  assert.equal(grullaSpecialPublicSnapshot(wing.state).resonancePrepared,false);
});

T('public snapshot exposes no brain history or hidden plan',()=>{
  const s=createGrullaSpecialCombatState({phase:3});
  const snap=grullaSpecialPublicSnapshot(s);

  assert.deepEqual(Object.keys(snap).sort(),[
    'attack','defense','phase','phaseHp','phaseId','phaseMaxHp','resonancePrepared'
  ]);
  assert.equal(Object.hasOwn(snap,'brainState'),false);
  assert.equal(Object.hasOwn(snap,'plan'),false);
  assert.equal(Object.hasOwn(snap,'history'),false);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
