import assert from 'node:assert/strict';

import {
  initialGrullaBrainState,
  observeResolvedPlayerAction
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

import {
  playerActionFromResolvedCombat
} from '../integration/grulla-player-action-adapter-v0.1.mjs';

import {
  grullaTechniquePreResolutionGate
} from '../integration/grulla-technique-gate-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{
  try{ fn(); pass++; console.log('PASS',name); }
  catch(err){ fail++; console.error('FAIL',name); console.error(err.stack||err); }
};

function resolvedPiel(){
  return playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5,
    damage:0
  });
}

T('first three identical techniques are not pre-blocked',()=>{
  let s=initialGrullaBrainState({phase:2});

  for(let i=0;i<3;i++){
    const gate=grullaTechniquePreResolutionGate({
      brainState:s,
      techniqueId:'piel_cobre',
      techniqueType:'guardia',
      element:'tierra',
      qiSpent:5
    });
    assert.equal(gate.blocked,false,'uso '+(i+1));
    s=observeResolvedPlayerAction(s,resolvedPiel()).state;
  }

  assert.equal(s.techniqueCounter.techniqueId,'piel_cobre');
});

T('fourth identical technique is blocked after the third resolved use',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,resolvedPiel()).state;

  const gate=grullaTechniquePreResolutionGate({
    brainState:s,
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5
  });

  assert.equal(gate.blocked,true);
  assert.equal(gate.consumeQi,true);
  assert.equal(gate.refundQi,false);
  assert.equal(gate.suppressGuard,true);
  assert.equal(gate.counterMode,'RESONANCIA_INTERNA');
});

T('blocked offensive technique suppresses damage and secondary effects',()=>{
  let s=initialGrullaBrainState({phase:2});
  const tech=()=>playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'palma',
    techniqueType:'ofensiva',
    element:'fuego',
    qiSpent:6,
    damage:6
  });
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,tech()).state;

  const gate=grullaTechniquePreResolutionGate({
    brainState:s,
    techniqueId:'palma',
    techniqueType:'ofensiva',
    element:'fuego',
    qiSpent:6
  });

  assert.equal(gate.blocked,true);
  assert.equal(gate.suppressDamage,true);
  assert.equal(gate.suppressAfflictions,true);
  assert.equal(gate.suppressResourceEffects,true);
  assert.equal(gate.counterMode,'TRAZO_VACIO');
});

T('blocked Paso suppresses evasion only through its closed counter mode',()=>{
  let s=initialGrullaBrainState({phase:2});
  const paso=()=>playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'paso_nube',
    techniqueType:'esquiva',
    element:'viento',
    qiSpent:5,
    damage:0
  });
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,paso()).state;

  const gate=grullaTechniquePreResolutionGate({
    brainState:s,
    techniqueId:'paso_nube',
    techniqueType:'esquiva',
    element:'viento',
    qiSpent:5
  });

  assert.equal(gate.blocked,true);
  assert.equal(gate.suppressEvasion,true);
  assert.equal(gate.counterMode,'PULSO_FIJADO');
});

T('blocked Filamento suppresses control and damage/effects',()=>{
  let s=initialGrullaBrainState({phase:2});
  const fil=()=>playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'filamento',
    techniqueType:'control',
    element:'agua',
    qiSpent:6,
    damage:3
  });
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,fil()).state;

  const gate=grullaTechniquePreResolutionGate({
    brainState:s,
    techniqueId:'filamento',
    techniqueType:'control',
    element:'agua',
    qiSpent:6
  });

  assert.equal(gate.blocked,true);
  assert.equal(gate.suppressControl,true);
  assert.equal(gate.suppressDamage,true);
  assert.equal(gate.counterMode,'ANCLA_DEL_VOTO');
});

T('BASIC variation breaks lock before a future technique gate',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,resolvedPiel()).state;

  s=observeResolvedPlayerAction(s,playerActionFromResolvedCombat({
    kind:'BASIC',
    damage:4
  })).state;

  const gate=grullaTechniquePreResolutionGate({
    brainState:s,
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5
  });

  assert.equal(gate.blocked,false);
  assert.equal(gate.counterMode,null);
});

T('DEFENDER does not break a learned technique gate',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,resolvedPiel()).state;

  s=observeResolvedPlayerAction(s,playerActionFromResolvedCombat({
    kind:'DEFEND'
  })).state;

  const gate=grullaTechniquePreResolutionGate({
    brainState:s,
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5
  });

  assert.equal(gate.blocked,true);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
