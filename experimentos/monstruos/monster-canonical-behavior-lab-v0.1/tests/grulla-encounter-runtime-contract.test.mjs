import assert from 'node:assert/strict';

import {GRULLA_ABILITIES as A} from '../adaptive/grulla-boss-brain-v0.1.mjs';
import {
  GRULLA_PHASE_RUNTIME,
  GRULLA_EXECUTION_RUNTIME,
  PIEL_G345_D1,
  PHASE1_RESONANCE,
  grullaPhaseProfile,
  resolvePielG345D1,
  resolvePhase1ResonantHit,
  bindGrullaRuntimeIntent,
  validateGrullaRuntimeContract
} from '../integration/grulla-encounter-runtime-contract-v0.1.mjs';

let pass=0,fail=0;
const T=(name,fn)=>{
  try{ fn(); pass++; console.log('PASS',name); }
  catch(err){ fail++; console.error('FAIL',name); console.error(err.stack||err); }
};

T('runtime contract covers every declared Grulla phase ability',()=>{
  const v=validateGrullaRuntimeContract();
  assert.equal(v.ok,true);
  assert.equal(v.totalHp,300);
  assert.deepEqual(v.missing,[]);
  assert.deepEqual(v.extra,[]);
  assert.deepEqual(v.invalid,[]);
});

T('phase pools and baseline stats match the closed three-phase encounter',()=>{
  assert.deepEqual(
    [1,2,3].map(p=>{
      const x=grullaPhaseProfile(p);
      return [x.hpPool,x.attack,x.defense];
    }),
    [
      [150,4,13],
      [100,4,13],
      [50,4,13]
    ]
  );
  assert.equal(Object.isFrozen(GRULLA_PHASE_RUNTIME),true);
});

T('Phase I runtime preserves the closed programmed cycle and damage',()=>{
  assert.deepEqual(
    GRULLA_PHASE_RUNTIME[1].cycle,
    [A.GOLPE_ALA,A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL]
  );
  assert.deepEqual(
    GRULLA_EXECUTION_RUNTIME[1][A.GOLPE_ALA].damage,
    {count:1,sides:6,flat:2}
  );
  assert.deepEqual(
    GRULLA_EXECUTION_RUNTIME[1][A.CAMPANADA_PICO].damage,
    {count:2,sides:6,flat:2}
  );
});

T('Pata prepares Resonance only in Phase I, not Phase III',()=>{
  const p1=bindGrullaRuntimeIntent({
    phase:1,
    intent:{id:A.PATA_INMOVIL}
  });
  const p3=bindGrullaRuntimeIntent({
    phase:3,
    intent:{id:A.PATA_INMOVIL}
  });

  assert.equal(p1.execution.defenseBonus,3);
  assert.equal(p1.execution.preparesPhase1Resonance,true);
  assert.equal(p3.execution.defenseBonus,3);
  assert.equal(p3.execution.preparesPhase1Resonance,false);
});

T('G345_D1 base and specialized Piel are exact',()=>{
  assert.equal(PIEL_G345_D1.id,'G345_D1');

  assert.deepEqual(
    resolvePielG345D1(),
    {
      techniqueId:'piel_cobre',
      role:'guardia',
      cost:5,
      guard:3,
      multiplier:1,
      capacity:3
    }
  );

  assert.deepEqual(
    resolvePielG345D1({
      tier1:'cobre_flexible',
      tier2:'cobre_grueso'
    }),
    {
      techniqueId:'piel_cobre',
      role:'guardia',
      cost:5,
      guard:5,
      multiplier:2,
      capacity:10
    }
  );
});

T('G345_D1 respects the 70 percent cost floor',()=>{
  const p=resolvePielG345D1({
    tier1:'cobre_sobrio',
    tier2:'aliento_economico'
  });
  assert.equal(p.cost,4);
  assert.equal(p.guard,3);
  assert.equal(p.capacity,3);
});

T('Resonance multiplies raw damage before Piel absorbs',()=>{
  assert.equal(PHASE1_RESONANCE.multiplier,1.75);
  const r=resolvePhase1ResonantHit({
    prepared:true,
    hit:true,
    rawDamage:10,
    guardActive:true,
    guardPerHit:5,
    guardCapacity:10
  });

  assert.equal(r.resonanceTriggered,true);
  assert.equal(r.baseDamage,10);
  assert.equal(r.afterResonance,18);
  assert.equal(r.absorbed,5);
  assert.equal(r.hpDamage,13);
  assert.equal(r.remainingCapacity,5);
  assert.equal(r.resonanceConsumed,true);
});

T('Resonance is consumed on a missed next wing attack',()=>{
  const r=resolvePhase1ResonantHit({
    prepared:true,
    hit:false,
    rawDamage:12,
    guardActive:true,
    guardPerHit:5,
    guardCapacity:10
  });

  assert.equal(r.resonanceTriggered,false);
  assert.equal(r.afterResonance,0);
  assert.equal(r.absorbed,0);
  assert.equal(r.hpDamage,0);
  assert.equal(r.remainingCapacity,10);
  assert.equal(r.resonanceConsumed,true);
});

T('without active Piel, prepared Resonance does not amplify damage',()=>{
  const r=resolvePhase1ResonantHit({
    prepared:true,
    hit:true,
    rawDamage:8,
    guardActive:false,
    guardPerHit:0,
    guardCapacity:0
  });

  assert.equal(r.resonanceTriggered,false);
  assert.equal(r.afterResonance,8);
  assert.equal(r.hpDamage,8);
  assert.equal(r.resonanceConsumed,true);
});

T('Phase II runtime is exactly CHAIN_A',()=>{
  const storm=GRULLA_EXECUTION_RUNTIME[2][A.TORMENTA_MIL_PLUMAS];
  const close=GRULLA_EXECUTION_RUNTIME[2][A.CERRAR_ALAS];
  const remember=GRULLA_EXECUTION_RUNTIME[2][A.RECORDAR_FILO];
  const eco=GRULLA_EXECUTION_RUNTIME[2][A.ECO_MERIDIANO];

  assert.deepEqual(storm.damage,{count:1,sides:6,flat:1});
  assert.equal(storm.attackBonus,0);
  assert.equal(storm.qiDrainOnDamage,1);
  assert.equal(close.guardPerHit,3);
  assert.equal(close.guardCapacity,6);
  assert.equal(remember.evasionBonus,10);
  assert.equal(eco.qiDrain,3);
});

T('Phase III runtime is exactly M_A',()=>{
  const pico=GRULLA_EXECUTION_RUNTIME[3][A.PICOTAZO_BLANCO];
  const camp=GRULLA_EXECUTION_RUNTIME[3][A.CAMPANA_SIN_DUENO];
  const ala=GRULLA_EXECUTION_RUNTIME[3][A.ALA_VACIA];
  const romper=GRULLA_EXECUTION_RUNTIME[3][A.ROMPER_RITMO];

  assert.equal(pico.attackBonus,1);
  assert.deepEqual(pico.damage,{count:1,sides:4,flat:1});

  assert.equal(camp.attackBonus,1);
  assert.deepEqual(camp.damage,{count:1,sides:6,flat:2});
  assert.equal(camp.qiDrainOnDamage,2);

  assert.equal(ala.evasionBonus,10);

  assert.equal(romper.attackBonus,2);
  assert.deepEqual(romper.damage,{count:1,sides:6,flat:2});
  assert.equal(romper.requiresPlan,'ROMPER_REPETICION');
});

T('Romper Ritmo cannot be bound without a committed plan',()=>{
  assert.throws(
    ()=>bindGrullaRuntimeIntent({
      phase:3,
      intent:{id:A.ROMPER_RITMO,committed:false}
    }),
    err=>err?.code==='PLAN_COMMIT_REQUIRED'
  );

  const r=bindGrullaRuntimeIntent({
    phase:3,
    intent:{id:A.ROMPER_RITMO,committed:true}
  });
  assert.equal(r.execution.requiresPlan,'ROMPER_REPETICION');
});

T('an ability cannot be executed in a phase outside its contract',()=>{
  assert.throws(
    ()=>bindGrullaRuntimeIntent({
      phase:1,
      intent:{id:A.CAMPANA_SIN_DUENO}
    }),
    /ABILITY_PHASE_VIOLATION/
  );
});

T('bound runtime instructions are frozen snapshots',()=>{
  const r=bindGrullaRuntimeIntent({
    phase:2,
    intent:{id:A.TORMENTA_MIL_PLUMAS}
  });
  assert.equal(Object.isFrozen(r),true);
  assert.equal(Object.isFrozen(r.execution),true);
  assert.equal(Object.isFrozen(r.execution.damage),true);
});

console.log('');
console.log('PASS: '+pass);
console.log('FAIL: '+fail);
if(fail)process.exitCode=1;
