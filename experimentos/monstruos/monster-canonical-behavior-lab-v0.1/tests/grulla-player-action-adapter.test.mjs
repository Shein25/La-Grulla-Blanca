import assert from 'node:assert/strict';

import {
  damageBandFromResolvedDamage,
  basicActionFromResolved,
  defendActionFromResolved,
  recoverActionFromResolved,
  techniqueActionFromResolved,
  playerActionFromResolvedCombat
} from '../integration/grulla-player-action-adapter-v0.1.mjs';

import {
  initialGrullaBrainState,
  observeResolvedPlayerAction,
  grullaTechniqueEffectiveness
} from '../adaptive/grulla-boss-brain-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{
  try{ fn(); pass++; console.log('PASS',name); }
  catch(err){ fail++; console.error('FAIL',name); console.error(err.stack||err); }
};

T('damage bands use the closed heavy threshold',()=>{
  assert.equal(damageBandFromResolvedDamage(0),'NONE');
  assert.equal(damageBandFromResolvedDamage(7),'NORMAL');
  assert.equal(damageBandFromResolvedDamage(8),'HEAVY');
});

T('basic attack maps to BASIC with resolved damage only',()=>{
  const a=basicActionFromResolved({damage:6});
  assert.deepEqual(a,{
    type:'BASIC',
    techniqueId:null,
    techniqueRole:null,
    element:null,
    qiSpent:0,
    damageBand:'NORMAL'
  });
  assert.equal(Object.isFrozen(a),true);
});

T('DEFENDER maps to DEFEND and recovery maps to RECOVER',()=>{
  assert.equal(defendActionFromResolved().type,'DEFEND');
  assert.equal(recoverActionFromResolved({vidaRecuperada:5,qiRecuperado:0}).type,'RECOVER');
});

T('offensive technique preserves id role element qi and resolved damage',()=>{
  const a=techniqueActionFromResolved({
    techniqueId:'palma',
    techniqueType:'ofensiva',
    element:'fuego',
    qiSpent:6,
    damage:11
  });
  assert.deepEqual(a,{
    type:'TECHNIQUE',
    techniqueId:'palma',
    techniqueRole:'ofensiva',
    element:'fuego',
    qiSpent:6,
    damageBand:'HEAVY'
  });
});

T('Filamento maps to CONTROL, not generic TECHNIQUE',()=>{
  const a=techniqueActionFromResolved({
    techniqueId:'filamento',
    techniqueType:'control',
    element:'agua',
    qiSpent:6,
    damage:0
  });
  assert.equal(a.type,'CONTROL');
  assert.equal(a.techniqueRole,'control');
});

T('hybrid technique does not invent an element if none was resolved',()=>{
  const a=techniqueActionFromResolved({
    techniqueId:'brasa_vendaval',
    techniqueType:'ofensiva',
    elements:['fuego','viento'],
    qiSpent:11,
    damage:12
  });
  assert.equal(a.element,null);
});

T('hybrid technique may carry an explicitly resolved element',()=>{
  const a=techniqueActionFromResolved({
    techniqueId:'brasa_vendaval',
    techniqueType:'ofensiva',
    elements:['fuego','viento'],
    resolvedElement:'viento',
    qiSpent:11,
    damage:12
  });
  assert.equal(a.element,'viento');
});

T('generic resolved signal dispatcher preserves semantics',()=>{
  const a=playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'paso_nube',
    techniqueType:'esquiva',
    element:'viento',
    qiSpent:5,
    damage:0
  });
  assert.equal(a.type,'TECHNIQUE');
  assert.equal(a.techniqueRole,'esquiva');
  assert.equal(a.damageBand,'NONE');
});

T('three resolved Paso uses trigger Pulso Fijado in the brain',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++){
    const a=playerActionFromResolvedCombat({
      kind:'TECHNIQUE',
      techniqueId:'paso_nube',
      techniqueType:'esquiva',
      element:'viento',
      qiSpent:5,
      damage:0
    });
    s=observeResolvedPlayerAction(s,a).state;
  }
  const eff=grullaTechniqueEffectiveness(s,playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'paso_nube',
    techniqueType:'esquiva',
    element:'viento',
    qiSpent:5,
    damage:0
  }));
  assert.equal(eff.blocked,true);
  assert.equal(eff.counterMode,'PULSO_FIJADO');
  assert.equal(eff.suppressEvasion,true);
});

T('three resolved Piel uses trigger Resonancia Interna in the brain',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++){
    s=observeResolvedPlayerAction(s,playerActionFromResolvedCombat({
      kind:'TECHNIQUE',
      techniqueId:'piel_cobre',
      techniqueType:'guardia',
      element:'tierra',
      qiSpent:5,
      damage:0
    })).state;
  }
  const eff=grullaTechniqueEffectiveness(s,playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5,
    damage:0
  }));
  assert.equal(eff.counterMode,'RESONANCIA_INTERNA');
  assert.equal(eff.suppressGuard,true);
});

T('three resolved Filamento uses trigger Ancla del Voto',()=>{
  let s=initialGrullaBrainState({phase:2});
  for(let i=0;i<3;i++){
    s=observeResolvedPlayerAction(s,playerActionFromResolvedCombat({
      kind:'TECHNIQUE',
      techniqueId:'filamento',
      techniqueType:'control',
      element:'agua',
      qiSpent:6,
      damage:0
    })).state;
  }
  const eff=grullaTechniqueEffectiveness(s,playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'filamento',
    techniqueType:'control',
    element:'agua',
    qiSpent:6,
    damage:0
  }));
  assert.equal(eff.counterMode,'ANCLA_DEL_VOTO');
  assert.equal(eff.suppressControl,true);
});

T('resolved BASIC breaks a learned technique lock',()=>{
  let s=initialGrullaBrainState({phase:2});
  const piel=()=>playerActionFromResolvedCombat({
    kind:'TECHNIQUE',
    techniqueId:'piel_cobre',
    techniqueType:'guardia',
    element:'tierra',
    qiSpent:5,
    damage:0
  });
  for(let i=0;i<3;i++)s=observeResolvedPlayerAction(s,piel()).state;
  assert.ok(s.techniqueCounter);
  const o=observeResolvedPlayerAction(s,playerActionFromResolvedCombat({kind:'BASIC',damage:4}));
  assert.equal(o.event,'TECHNIQUE_COUNTER_BROKEN_BY_VARIATION');
  assert.equal(o.state.techniqueCounter,null);
});

T('invalid technique role is rejected instead of guessed',()=>{
  assert.throws(
    ()=>techniqueActionFromResolved({
      techniqueId:'x',
      techniqueType:'misteriosa',
      qiSpent:1,
      damage:0
    }),
    /techniqueType inválido/
  );
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
