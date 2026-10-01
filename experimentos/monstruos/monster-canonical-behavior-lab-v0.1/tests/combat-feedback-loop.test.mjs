import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {buildCandidateMonsterInput} from '../adapter/candidate-assignment-adapter.mjs';
import {absorptionOutcomeFromResolvedHit} from '../integration/resolved-combat-signal-adapter-v0.1.mjs';
import {recordSemanticOutcome} from '../integration/semantic-memory-recorder-v0.1.mjs';

const M=JSON.parse(readFileSync(new URL('../canonical/monsters.json',import.meta.url),'utf8')).profiles;
let pass=0,fail=0;
const T=(n,fn)=>{try{fn();pass++;console.log('PASS',n)}catch(e){fail++;console.error('FAIL',n);console.error(e.stack||e)}};

T('resolved absorption still becomes semantic memory',()=>{
  let memory=[];
  for(let r=1;r<=3;r++){
    const outcome=absorptionOutcomeFromResolvedHit({round:r,absorbido:4});
    memory=recordSemanticOutcome(memory,outcome);
  }
  assert.deepEqual(memory,[
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:1},
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:2},
    {category:'DEFENSA_ABSORCION',result:'EFECTIVA',round:3}
  ]);
});

T('full monster feedback loop waits for READY T0 stats',()=>{
  assert.throws(
    ()=>buildCandidateMonsterInput({mobId:'guardian_coral',def:M.guardian_coral,round:1,mode:'DECISION_EXPERIMENTAL'}),
    /not READY/
  );
});

console.log(`\nPASS: ${pass}`);
console.log(`FAIL: ${fail}`);
if(fail)process.exitCode=1;
