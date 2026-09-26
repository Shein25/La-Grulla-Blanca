import assert from 'node:assert/strict';
import {GRULLA_ABILITIES as A} from '../adaptive/grulla-boss-brain-v0.1.mjs';
import {
  GRULLA_ABILITY_CONTRACT,
  grullaAbilityContract,
  validateGrullaAbilityContract
} from '../adaptive/grulla-boss-ability-contract-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{try{fn();pass++;console.log('PASS',name)}catch(e){fail++;console.error('FAIL',name);console.error(e.stack||e)}};

T('every Grulla brain ability has exactly one execution contract',()=>{
  const v=validateGrullaAbilityContract();
  assert.equal(v.ok,true);
  assert.deepEqual(v.missing,[]);
  assert.deepEqual(v.extra,[]);
  assert.deepEqual(v.invalid,[]);
  assert.equal(Object.keys(GRULLA_ABILITY_CONTRACT).length,Object.values(A).length);
});

T('every Grulla intent consumes the monster action',()=>{
  for(const id of Object.values(A)){
    assert.equal(grullaAbilityContract(id).consumesAction,true,id);
  }
});

T('phase I remains readable and contains no adaptive/plan action',()=>{
  const allowed=new Set([A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL]);
  for(const id of allowed){
    const d=grullaAbilityContract(id);
    assert.ok(d.phase.includes(1),id);
    assert.equal(d.kind==='PLAN_PREP'||d.kind==='ADAPTIVE_PREP',false,id);
  }
});

T('phase II contains memory responses but no short plan finisher',()=>{
  const ids=[A.GOLPE_ALA,A.TORMENTA_MIL_PLUMAS,A.CERRAR_ALAS,A.RECORDAR_FILO,A.ECO_MERIDIANO];
  for(const id of ids)assert.ok(grullaAbilityContract(id).phase.includes(2),id);
  assert.equal(grullaAbilityContract(A.RECORDAR_FILO).kind,'ADAPTIVE_PREP');
  assert.equal(grullaAbilityContract(A.ECO_MERIDIANO).kind,'RESOURCE_PRESSURE');
});

T('phase III plan preparation is explicitly breakable',()=>{
  for(const id of [A.SILENCIO_ENTRE_CAMPANAS,A.BUSCAR_PULSO]){
    const d=grullaAbilityContract(id);
    assert.equal(d.kind,'PLAN_PREP');
    assert.ok(d.tags.includes('BREAKABLE'));
    assert.ok(d.tags.includes('TELEGRAPHED'));
  }
});

T('Romper el Ritmo cannot exist outside its committed plan',()=>{
  const d=grullaAbilityContract(A.ROMPER_RITMO);
  assert.equal(d.kind,'PLAN_FINISHER');
  assert.equal(d.requiresPlan,'ROMPER_REPETICION');
});

T('no ability contract introduces technique silence',()=>{
  for(const d of Object.values(GRULLA_ABILITY_CONTRACT)){
    assert.equal(d.tags.includes('SILENCE'),false);
    assert.equal(d.tags.includes('DISABLE_TECHNIQUES'),false);
  }
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
