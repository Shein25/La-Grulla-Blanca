import assert from 'node:assert/strict';
import {GRULLA_ABILITIES as A} from '../adaptive/grulla-boss-brain-v0.1.mjs';
import {
  UNIVERSAL_PLAYER_TOOLS,
  OPTIONAL_PLAYER_TOOLS,
  GRULLA_COUNTERPLAY_MATRIX,
  counterplayForGrullaIntent,
  validateGrullaCounterplayMatrix
} from '../adaptive/grulla-counterplay-matrix-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('every Grulla intent has declared counterplay',()=>{
  const v=validateGrullaCounterplayMatrix();
  assert.equal(v.ok,true);
  assert.deepEqual(v.missing,[]);
  assert.deepEqual(v.extra,[]);
});

T('no Grulla intent requires an optional manual to survive',()=>{
  const v=validateGrullaCounterplayMatrix();
  assert.deepEqual(v.optionalOnly,[]);
  for(const row of Object.values(GRULLA_COUNTERPLAY_MATRIX)){
    assert.ok(row.universal.some(x=>UNIVERSAL_PLAYER_TOOLS.includes(x)));
  }
});

T('Paso, Piel and Filamento remain optional enhancements only',()=>{
  assert.equal(OPTIONAL_PLAYER_TOOLS.EVADE,'paso_nube');
  assert.equal(OPTIONAL_PLAYER_TOOLS.GUARD,'piel_cobre');
  assert.equal(OPTIONAL_PLAYER_TOOLS.CONTROL,'filamento');
});

T('all heavy or finisher attacks retain universal DEFEND',()=>{
  for(const id of [
    A.CAMPANADA_PICO,
    A.TORMENTA_MIL_PLUMAS,
    A.PICOTAZO_BLANCO,
    A.CAMPANA_SIN_DUENO,
    A.ROMPER_RITMO
  ]){
    assert.ok(counterplayForGrullaIntent(id).universal.includes('DEFEND'),id);
  }
});

T('phase III plan preparations can be broken without optional techniques',()=>{
  assert.ok(counterplayForGrullaIntent(A.SILENCIO_ENTRE_CAMPANAS).universal.includes('BASIC'));
  assert.ok(counterplayForGrullaIntent(A.BUSCAR_PULSO).universal.some(x=>x==='BASIC'||x==='DEFEND'));
});

T('Filamento is an optional interruption route for both phase III preparations',()=>{
  assert.ok(counterplayForGrullaIntent(A.SILENCIO_ENTRE_CAMPANAS).optional.includes('CONTROL'));
  assert.ok(counterplayForGrullaIntent(A.BUSCAR_PULSO).optional.includes('CONTROL'));
});

T('Paso and Piel are alternatives to DEFEND on telegraphed heavy attacks',()=>{
  for(const id of [A.CAMPANADA_PICO,A.TORMENTA_MIL_PLUMAS,A.CAMPANA_SIN_DUENO,A.ROMPER_RITMO]){
    const row=counterplayForGrullaIntent(id);
    assert.ok(row.optional.includes('EVADE'),id);
    assert.ok(row.optional.includes('GUARD'),id);
  }
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
