import {GRULLA_ABILITIES as A} from '../adaptive/grulla-boss-brain-v0.1.mjs';
import {
  GRULLA_ABILITY_CONTRACT,
  grullaAbilityContract
} from '../adaptive/grulla-boss-ability-contract-v0.1.mjs';

export const GRULLA_RUNTIME_STATUS='EXPERIMENTAL_INTEGRATION_READY_GRULLA_RUNTIME_V01';

function freezeDeep(value){
  if(!value||typeof value!=='object'||Object.isFrozen(value))return value;
  for(const v of Object.values(value))freezeDeep(v);
  return Object.freeze(value);
}
function clone(value){return value===undefined?undefined:JSON.parse(JSON.stringify(value));}
function phaseOf(phase){
  if(!Number.isInteger(phase)||phase<1||phase>3)throw new RangeError('phase debe ser 1..3');
  return phase;
}
function finiteNonNegative(v,label){
  if(typeof v!=='number'||!Number.isFinite(v)||v<0)throw new TypeError(label+' debe ser número finito >= 0');
  return v;
}
function safeIntegerNonNegative(v,label){
  if(!Number.isSafeInteger(v)||v<0)throw new TypeError(label+' debe ser entero seguro >= 0');
  return v;
}

export const GRULLA_PHASE_RUNTIME=freezeDeep({
  1:{
    id:'EL_VOTO_INMOVIL',
    hpPool:150,
    attack:4,
    defense:13,
    brain:'PROGRAMADA',
    cycle:[A.GOLPE_ALA,A.GOLPE_ALA,A.CAMPANADA_PICO,A.PATA_INMOVIL]
  },
  2:{
    id:'LAS_ALAS_RECUERDAN',
    hpPool:100,
    attack:4,
    defense:13,
    brain:'ADAPTATIVA',
    profile:'CHAIN_A'
  },
  3:{
    id:'LA_CAMPANA_SIN_DUENO',
    hpPool:50,
    attack:4,
    defense:13,
    brain:'MAESTRA',
    profile:'M_A'
  }
});

export const GRULLA_EXECUTION_RUNTIME=freezeDeep({
  1:{
    [A.GOLPE_ALA]:{
      kind:'ATTACK',
      attackBonus:0,
      damage:{count:1,sides:6,flat:2}
    },
    [A.CAMPANADA_PICO]:{
      kind:'ATTACK',
      attackBonus:0,
      damage:{count:2,sides:6,flat:2},
      telegraphed:true
    },
    [A.PATA_INMOVIL]:{
      kind:'SELF_DEFENSE',
      defenseBonus:3,
      appliesTo:'NEXT_PLAYER_OFFENSIVE_ACTION',
      preparesPhase1Resonance:true
    }
  },
  2:{
    [A.GOLPE_ALA]:{
      kind:'ATTACK',
      attackBonus:0,
      damage:{count:1,sides:4,flat:0}
    },
    [A.TORMENTA_MIL_PLUMAS]:{
      kind:'ATTACK_RESOURCE',
      attackBonus:0,
      damage:{count:1,sides:6,flat:1},
      qiDrainOnDamage:1
    },
    [A.CERRAR_ALAS]:{
      kind:'SELF_DEFENSE',
      guardPerHit:3,
      guardCapacity:6
    },
    [A.RECORDAR_FILO]:{
      kind:'ADAPTIVE_PREP',
      evasionBonus:10,
      appliesTo:'NEXT_PLAYER_OFFENSIVE_ACTION'
    },
    [A.ECO_MERIDIANO]:{
      kind:'RESOURCE_PRESSURE',
      qiDrain:3,
      condition:'PLAYER_RESOLVED_ACTION_SPENT_QI'
    }
  },
  3:{
    [A.PICOTAZO_BLANCO]:{
      kind:'ATTACK',
      attackBonus:1,
      damage:{count:1,sides:4,flat:1}
    },
    [A.CAMPANA_SIN_DUENO]:{
      kind:'ATTACK_RESOURCE',
      attackBonus:1,
      damage:{count:1,sides:6,flat:2},
      qiDrainOnDamage:2
    },
    [A.ALA_VACIA]:{
      kind:'SELF_DEFENSE',
      evasionBonus:10,
      appliesTo:'NEXT_PLAYER_OFFENSIVE_ACTION'
    },
    [A.PATA_INMOVIL]:{
      kind:'SELF_DEFENSE',
      defenseBonus:3,
      appliesTo:'NEXT_PLAYER_OFFENSIVE_ACTION',
      preparesPhase1Resonance:false
    },
    [A.SILENCIO_ENTRE_CAMPANAS]:{
      kind:'PLAN_PREP',
      planId:'ROMPER_REPETICION',
      breakable:true
    },
    [A.ROMPER_RITMO]:{
      kind:'PLAN_FINISHER',
      attackBonus:2,
      damage:{count:1,sides:6,flat:2},
      requiresPlan:'ROMPER_REPETICION'
    },
    [A.BUSCAR_PULSO]:{
      kind:'PLAN_PREP',
      planId:'CAZAR_CIRCULACION',
      breakable:true,
      followup:A.CAMPANA_SIN_DUENO
    }
  }
});

export const PIEL_G345_D1=freezeDeep({
  id:'G345_D1',
  techniqueId:'piel_cobre',
  role:'guardia',
  base:{
    cost:5,
    guard:3,
    multiplier:1
  },
  costFloor:4,
  tier1:{
    cobre_endurecido:{guard:4},
    cobre_flexible:{multiplierDelta:1},
    cobre_sobrio:{costDelta:-1}
  },
  tier2:{
    aliento_economico:{costDelta:-1},
    cobre_grueso:{guard:5},
    placas_continuas:{multiplierDelta:1}
  }
});

export const PHASE1_RESONANCE=freezeDeep({
  id:'RESONANCIA_FASE1',
  sourceAbility:A.PATA_INMOVIL,
  consumesOnAbility:A.GOLPE_ALA,
  multiplier:1.75,
  trigger:'NEXT_GOLPE_ALA_HITS_WHILE_PIEL_ACTIVE',
  order:'MULTIPLY_RAW_DAMAGE_THEN_ABSORB',
  consumeOnMiss:true,
  bypassesGuard:false,
  shattersGuard:false
});

export function resolvePielG345D1({tier1=null,tier2=null}={}){
  if(tier1!==null&&!Object.hasOwn(PIEL_G345_D1.tier1,tier1))throw new RangeError('tier1 inválido');
  if(tier2!==null&&!Object.hasOwn(PIEL_G345_D1.tier2,tier2))throw new RangeError('tier2 inválido');

  let cost=PIEL_G345_D1.base.cost;
  let guard=PIEL_G345_D1.base.guard;
  let multiplier=PIEL_G345_D1.base.multiplier;

  for(const mod of [
    tier1?PIEL_G345_D1.tier1[tier1]:null,
    tier2?PIEL_G345_D1.tier2[tier2]:null
  ]){
    if(!mod)continue;
    if(mod.guard!==undefined)guard=mod.guard;
    if(mod.multiplierDelta!==undefined)multiplier+=mod.multiplierDelta;
    if(mod.costDelta!==undefined)cost+=mod.costDelta;
  }

  cost=Math.max(PIEL_G345_D1.costFloor,cost);
  return freezeDeep({
    techniqueId:PIEL_G345_D1.techniqueId,
    role:PIEL_G345_D1.role,
    cost,
    guard,
    multiplier,
    capacity:guard*multiplier
  });
}

export function resolvePhase1ResonantHit({
  prepared,
  hit,
  rawDamage,
  guardActive,
  guardPerHit=0,
  guardCapacity=0
}){
  if(typeof prepared!=='boolean')throw new TypeError('prepared debe ser boolean');
  if(typeof hit!=='boolean')throw new TypeError('hit debe ser boolean');
  if(typeof guardActive!=='boolean')throw new TypeError('guardActive debe ser boolean');
  finiteNonNegative(rawDamage,'rawDamage');
  finiteNonNegative(guardPerHit,'guardPerHit');
  finiteNonNegative(guardCapacity,'guardCapacity');

  const baseDamage=hit?rawDamage:0;
  const resonanceTriggered=prepared&&hit&&guardActive;
  const afterResonance=resonanceTriggered
    ?Math.ceil(baseDamage*PHASE1_RESONANCE.multiplier)
    :baseDamage;

  const canAbsorb=hit&&guardActive&&guardCapacity>0&&guardPerHit>0;
  const absorbed=canAbsorb?Math.min(afterResonance,guardPerHit,guardCapacity):0;
  const hpDamage=afterResonance-absorbed;
  const remainingCapacity=Math.max(0,guardCapacity-absorbed);

  return freezeDeep({
    prepared,
    hit,
    resonanceTriggered,
    resonanceConsumed:prepared,
    baseDamage,
    afterResonance,
    absorbed,
    hpDamage,
    remainingCapacity
  });
}

export function grullaPhaseProfile(phase){
  return GRULLA_PHASE_RUNTIME[phaseOf(phase)];
}

export function bindGrullaRuntimeIntent({phase,intent}){
  phase=phaseOf(phase);
  if(!intent||typeof intent!=='object'||typeof intent.id!=='string')throw new TypeError('intent inválido');

  const declared=grullaAbilityContract(intent.id);
  if(!declared.phase.includes(phase)){
    throw new RangeError('ABILITY_PHASE_VIOLATION: '+intent.id+' no pertenece a Fase '+phase);
  }

  const runtime=GRULLA_EXECUTION_RUNTIME[phase]?.[intent.id];
  if(!runtime)throw new RangeError('MISSING_RUNTIME_EXECUTION: '+phase+':'+intent.id);

  if(runtime.requiresPlan&&!intent.committed){
    const err=new RangeError('PLAN_COMMIT_REQUIRED: '+intent.id);
    err.code='PLAN_COMMIT_REQUIRED';
    throw err;
  }

  return freezeDeep({
    kind:'GRULLA_RUNTIME_INTENT',
    phase,
    abilityId:intent.id,
    consumesAction:declared.consumesAction,
    execution:clone(runtime)
  });
}

export function validateGrullaRuntimeContract(){
  const missing=[];
  const extra=[];
  const invalid=[];

  for(const [abilityId,declared] of Object.entries(GRULLA_ABILITY_CONTRACT)){
    for(const phase of declared.phase){
      const runtime=GRULLA_EXECUTION_RUNTIME[phase]?.[abilityId];
      if(!runtime)missing.push(phase+':'+abilityId);
      else if(runtime.kind!==declared.kind)invalid.push(phase+':'+abilityId+':kind');
    }
  }

  for(const [phaseKey,entries] of Object.entries(GRULLA_EXECUTION_RUNTIME)){
    const phase=Number(phaseKey);
    for(const abilityId of Object.keys(entries)){
      const declared=GRULLA_ABILITY_CONTRACT[abilityId];
      if(!declared||!declared.phase.includes(phase))extra.push(phase+':'+abilityId);
    }
  }

  const totalHp=Object.values(GRULLA_PHASE_RUNTIME).reduce((sum,p)=>sum+p.hpPool,0);
  if(totalHp!==300)invalid.push('TOTAL_HP');
  if(GRULLA_PHASE_RUNTIME[1].defense!==13||GRULLA_PHASE_RUNTIME[2].defense!==13||GRULLA_PHASE_RUNTIME[3].defense!==13){
    invalid.push('PHASE_DEFENSE');
  }
  if(PHASE1_RESONANCE.multiplier!==1.75)invalid.push('PHASE1_RESONANCE_MULTIPLIER');

  return freezeDeep({
    ok:missing.length===0&&extra.length===0&&invalid.length===0,
    missing,
    extra,
    invalid,
    totalHp
  });
}
