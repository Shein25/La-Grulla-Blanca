import assert from 'node:assert/strict';

import {GRULLA_ABILITIES as A} from '../adaptive/grulla-boss-brain-v0.1.mjs';

import {
  initialGrullaEncounterSession,
  grullaSessionProfile,
  gateGrullaSessionPlayerTechnique,
  observeGrullaSessionPlayerResolved,
  chooseGrullaSessionIntent,
  markGrullaSessionIntentResolved,
  resolveGrullaSessionPhase1Wing,
  applyGrullaSessionBossDamage,
  enterNextGrullaSessionPhase
} from '../integration/grulla-encounter-session-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{
  try{ fn(); pass++; console.log('PASS',name); }
  catch(err){ fail++; console.error('FAIL',name); console.error(err.stack||err); }
};
const fixed=()=>.5;

T('session starts in closed Phase I profile',()=>{
  const s=initialGrullaEncounterSession();
  assert.equal(s.phase,1);
  assert.equal(s.phaseHp,150);
  assert.equal(grullaSessionProfile(s).defense,13);
});

T('Phase I controller emits the closed programmed cycle',()=>{
  let s=initialGrullaEncounterSession();
  const got=[];
  for(let i=0;i<4;i++){
    const x=chooseGrullaSessionIntent(s,{context:{},rng:fixed});
    got.push(x.intent.id);
    s=x.session;
  }
  assert.deepEqual(got,[A.GOLPE_ALA,A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL]);
});

T('resolved Pata prepares Phase I Resonance and next wing consumes it on miss',()=>{
  let s=initialGrullaEncounterSession();

  // advance brain to Pata
  let x;
  for(let i=0;i<4;i++){
    x=chooseGrullaSessionIntent(s,{context:{},rng:fixed});
    s=x.session;
  }
  assert.equal(x.intent.id,A.PATA_INMOVIL);

  s=markGrullaSessionIntentResolved(s,x.runtime);
  assert.equal(s.phase1ResonancePrepared,true);

  const wing=resolveGrullaSessionPhase1Wing(s,{
    hit:false,
    rawDamage:7,
    guardActive:true,
    guardPerHit:5,
    guardCapacity:10
  });

  assert.equal(wing.resolution.resonanceConsumed,true);
  assert.equal(wing.resolution.hpDamage,0);
  assert.equal(wing.session.phase1ResonancePrepared,false);
});

T('Phase I Resonance uses x1.75 before G345 absorption',()=>{
  let s=initialGrullaEncounterSession();

  let x;
  for(let i=0;i<4;i++){
    x=chooseGrullaSessionIntent(s,{context:{},rng:fixed});
    s=x.session;
  }
  s=markGrullaSessionIntentResolved(s,x.runtime);

  const wing=resolveGrullaSessionPhase1Wing(s,{
    hit:true,
    rawDamage:10,
    guardActive:true,
    guardPerHit:5,
    guardCapacity:10
  });

  assert.equal(wing.resolution.afterResonance,18);
  assert.equal(wing.resolution.absorbed,5);
  assert.equal(wing.resolution.hpDamage,13);
  assert.equal(wing.resolution.remainingCapacity,5);
});

T('two exclusive Phase I technique uses survive transition as inherited lock',()=>{
  let s=initialGrullaEncounterSession();

  for(let i=0;i<2;i++){
    const o=observeGrullaSessionPlayerResolved(s,{
      kind:'TECHNIQUE',
      techniqueId:'palma',
      techniqueType:'ofensiva',
      element:'fuego',
      qiSpent:6,
      damage:6
    });
    s=o.session;
  }

  s=applyGrullaSessionBossDamage(s,150).session;
  s=enterNextGrullaSessionPhase(s);

  assert.equal(s.phase,2);
  assert.equal(s.phaseHp,100);
  assert.equal(s.brainState.techniqueCounter.techniqueId,'palma');

  const gate=gateGrullaSessionPlayerTechnique(s,{
    kind:'TECHNIQUE',
    techniqueId:'palma',
    techniqueType:'ofensiva',
    element:'fuego',
    qiSpent:6
  });
  assert.equal(gate.blocked,true);
  assert.equal(gate.counterMode,'TRAZO_VACIO');
});

T('BASIC in Phase I prevents inherited single-skill lock',()=>{
  let s=initialGrullaEncounterSession();

  s=observeGrullaSessionPlayerResolved(s,{
    kind:'TECHNIQUE',
    techniqueId:'palma',
    techniqueType:'ofensiva',
    element:'fuego',
    qiSpent:6,
    damage:6
  }).session;

  s=observeGrullaSessionPlayerResolved(s,{
    kind:'BASIC',
    damage:4
  }).session;

  s=observeGrullaSessionPlayerResolved(s,{
    kind:'TECHNIQUE',
    techniqueId:'palma',
    techniqueType:'ofensiva',
    element:'fuego',
    qiSpent:6,
    damage:6
  }).session;

  s=applyGrullaSessionBossDamage(s,150).session;
  s=enterNextGrullaSessionPhase(s);

  assert.equal(s.brainState.techniqueCounter,null);
});

T('third resolved technique locks and fourth is gated',()=>{
  let s=initialGrullaEncounterSession({phase:2});

  for(let i=0;i<3;i++){
    s=observeGrullaSessionPlayerResolved(s,{
      kind:'TECHNIQUE',
      techniqueId:'paso_nube',
      techniqueType:'esquiva',
      element:'viento',
      qiSpent:5,
      damage:0
    }).session;
  }

  const gate=gateGrullaSessionPlayerTechnique(s,{
    kind:'TECHNIQUE',
    techniqueId:'paso_nube',
    techniqueType:'esquiva',
    element:'viento',
    qiSpent:5
  });

  assert.equal(gate.blocked,true);
  assert.equal(gate.counterMode,'PULSO_FIJADO');
});

T('Phase transitions require the current HP pool to be defeated',()=>{
  const s=initialGrullaEncounterSession();
  assert.throws(()=>enterNextGrullaSessionPhase(s),/PHASE_NOT_DEFEATED/);
});

T('defeating Phase II enters Phase III with fresh 50 HP and preserved memory summary',()=>{
  let s=initialGrullaEncounterSession({phase:2});
  s=observeGrullaSessionPlayerResolved(s,{
    kind:'TECHNIQUE',
    techniqueId:'filamento',
    techniqueType:'control',
    element:'agua',
    qiSpent:6,
    damage:0
  }).session;

  s=applyGrullaSessionBossDamage(s,100).session;
  s=enterNextGrullaSessionPhase(s);

  assert.equal(s.phase,3);
  assert.equal(s.phaseHp,50);
  assert.ok(s.brainState.phaseMemory.phase2);
});

T('boss damage never spills into the next phase',()=>{
  let s=initialGrullaEncounterSession();
  const d=applyGrullaSessionBossDamage(s,999);
  assert.equal(d.appliedDamage,150);
  assert.equal(d.session.phaseHp,0);

  s=enterNextGrullaSessionPhase(d.session);
  assert.equal(s.phaseHp,100);
});

T('Phase III has no automatic post-phase transition in this contract',()=>{
  let s=initialGrullaEncounterSession({phase:3});
  s=applyGrullaSessionBossDamage(s,50).session;
  assert.throws(()=>enterNextGrullaSessionPhase(s),/no tiene transición posterior/);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
