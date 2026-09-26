import assert from 'node:assert/strict';
import {absorptionOutcomeFromResolvedHit,recoveryOutcomeFromResolvedDelta} from '../integration/resolved-combat-signal-adapter-v0.1.mjs';
import {recordSemanticOutcome} from '../integration/semantic-memory-recorder-v0.1.mjs';

let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('positive resolved absorption maps effective true',()=>{
  assert.deepEqual(absorptionOutcomeFromResolvedHit({round:3,absorbido:4}),{
    type:'PLAYER_ABSORPTION_RESOLVED',round:3,effective:true
  });
});
T('zero resolved absorption maps effective false',()=>{
  assert.deepEqual(absorptionOutcomeFromResolvedHit({round:3,absorbido:0}),{
    type:'PLAYER_ABSORPTION_RESOLVED',round:3,effective:false
  });
});
T('absorption output is frozen',()=>assert.equal(Object.isFrozen(absorptionOutcomeFromResolvedHit({round:1,absorbido:1})),true));
T('absorption rejects negative/nonfinite values',()=>{
  assert.throws(()=>absorptionOutcomeFromResolvedHit({round:1,absorbido:-1}));
  assert.throws(()=>absorptionOutcomeFromResolvedHit({round:1,absorbido:Infinity}));
});
T('absorption rejects hidden log/HP fields',()=>{
  assert.throws(()=>absorptionOutcomeFromResolvedHit({round:1,absorbido:1,hpAfter:30}),/shape inválido/);
  assert.throws(()=>absorptionOutcomeFromResolvedHit({round:1,absorbido:1,mensaje:'absorbe 1'}),/shape inválido/);
});
T('absorption rejects invalid round',()=>assert.throws(()=>absorptionOutcomeFromResolvedHit({round:-1,absorbido:1})));

T('resolved HP recovery maps effective true',()=>{
  assert.deepEqual(recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:5,qiRecuperado:0}),{
    type:'PLAYER_RECOVERY_RESOLVED',round:2,effective:true
  });
});
T('resolved qi recovery maps effective true',()=>{
  assert.equal(recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:0,qiRecuperado:8}).effective,true);
});
T('zero recovery maps effective false',()=>{
  assert.equal(recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:0,qiRecuperado:0}).effective,false);
});
T('recovery rejects raw before/after state and messages',()=>{
  assert.throws(()=>recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:5,qiRecuperado:0,hpBefore:10}),/shape inválido/);
  assert.throws(()=>recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:5,qiRecuperado:0,mensaje:'+5 vida'}),/shape inválido/);
});
T('recovery rejects negative deltas',()=>assert.throws(()=>recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:-1,qiRecuperado:0})));
T('adapter output feeds semantic recorder without translation',()=>{
  let memory=[];
  memory=recordSemanticOutcome(memory,absorptionOutcomeFromResolvedHit({round:1,absorbido:3}));
  memory=recordSemanticOutcome(memory,recoveryOutcomeFromResolvedDelta({round:2,vidaRecuperada:0,qiRecuperado:6}));
  assert.deepEqual(memory,[
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:1},
    {category:'RECUPERACION',result:'EFECTIVA',round:2}
  ]);
});
T('same-round resolved signals preserve insertion order',()=>{
  let memory=[];
  memory=recordSemanticOutcome(memory,absorptionOutcomeFromResolvedHit({round:4,absorbido:0}));
  memory=recordSemanticOutcome(memory,recoveryOutcomeFromResolvedDelta({round:4,vidaRecuperada:0,qiRecuperado:0}));
  assert.deepEqual(memory.map(x=>x.category),['DEFENSA_ABSORCION','RECUPERACION']);
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
