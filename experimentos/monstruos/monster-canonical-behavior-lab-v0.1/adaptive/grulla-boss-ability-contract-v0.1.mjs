import {GRULLA_ABILITIES as A} from './grulla-boss-brain-v0.1.mjs';

export const GRULLA_ABILITY_CONTRACT_STATUS='EXPERIMENTAL_NON_CANONICAL_GRULLA_ABILITY_CONTRACT_V01';

export const GRULLA_ABILITY_CONTRACT=Object.freeze({
  [A.GOLPE_ALA]:Object.freeze({
    phase:[1,2],
    kind:'ATTACK',
    consumesAction:true,
    profile:'BASIC',
    tags:Object.freeze(['PHYSICAL','READABLE'])
  }),
  [A.CAMPANADA_PICO]:Object.freeze({
    phase:[1],
    kind:'ATTACK',
    consumesAction:true,
    profile:'HEAVY_TELEGRAPHED',
    tags:Object.freeze(['HEAVY','TELEGRAPHED','PUNISH_GREED'])
  }),
  [A.PATA_INMOVIL]:Object.freeze({
    phase:[1,3],
    kind:'SELF_DEFENSE',
    consumesAction:true,
    profile:'ANCHOR',
    tags:Object.freeze(['DEFENSE','TENACITY','READABLE'])
  }),
  [A.TORMENTA_MIL_PLUMAS]:Object.freeze({
    phase:[2],
    kind:'ATTACK_RESOURCE',
    consumesAction:true,
    profile:'PRESSURE_QI',
    tags:Object.freeze(['DAMAGE','QI_DRAIN','TELEGRAPHED'])
  }),
  [A.CERRAR_ALAS]:Object.freeze({
    phase:[2],
    kind:'SELF_DEFENSE',
    consumesAction:true,
    profile:'GUARD',
    tags:Object.freeze(['GUARD','ANTI_BURST'])
  }),
  [A.RECORDAR_FILO]:Object.freeze({
    phase:[2],
    kind:'ADAPTIVE_PREP',
    consumesAction:true,
    profile:'READ_REPETITION',
    tags:Object.freeze(['MEMORY','ANTI_REPEAT','NO_FUTURE_READ'])
  }),
  [A.ECO_MERIDIANO]:Object.freeze({
    phase:[2],
    kind:'RESOURCE_PRESSURE',
    consumesAction:true,
    profile:'PUNISH_QI_STREAK',
    tags:Object.freeze(['QI_PRESSURE','MEMORY','NO_SILENCE'])
  }),
  [A.PICOTAZO_BLANCO]:Object.freeze({
    phase:[3],
    kind:'ATTACK',
    consumesAction:true,
    profile:'PRECISE',
    tags:Object.freeze(['PRECISION','FINISHER_LIGHT'])
  }),
  [A.CAMPANA_SIN_DUENO]:Object.freeze({
    phase:[3],
    kind:'ATTACK_RESOURCE',
    consumesAction:true,
    profile:'HEAVY_QI_PRESSURE',
    tags:Object.freeze(['HEAVY','QI_DRAIN','TELEGRAPHED'])
  }),
  [A.ALA_VACIA]:Object.freeze({
    phase:[3],
    kind:'SELF_DEFENSE',
    consumesAction:true,
    profile:'EVASION',
    tags:Object.freeze(['EVASION','ANTI_OFFENSE'])
  }),
  [A.SILENCIO_ENTRE_CAMPANAS]:Object.freeze({
    phase:[3],
    kind:'PLAN_PREP',
    consumesAction:true,
    profile:'ANTI_REPEAT',
    tags:Object.freeze(['PLAN','TELEGRAPHED','BREAKABLE'])
  }),
  [A.ROMPER_RITMO]:Object.freeze({
    phase:[3],
    kind:'PLAN_FINISHER',
    consumesAction:true,
    profile:'ANTI_REPEAT_FINISHER',
    requiresPlan:'ROMPER_REPETICION',
    tags:Object.freeze(['PLAN','PRECISION','PUNISH_REPEAT'])
  }),
  [A.BUSCAR_PULSO]:Object.freeze({
    phase:[3],
    kind:'PLAN_PREP',
    consumesAction:true,
    profile:'ANTI_QI_STREAK',
    tags:Object.freeze(['PLAN','QI_READ','TELEGRAPHED','BREAKABLE'])
  })
});

export function grullaAbilityContract(abilityId){
  const def=GRULLA_ABILITY_CONTRACT[abilityId];
  if(!def)throw new RangeError('habilidad Grulla sin contrato: '+abilityId);
  return def;
}

export function validateGrullaAbilityContract(){
  const ids=Object.values(A);
  const missing=ids.filter(id=>!GRULLA_ABILITY_CONTRACT[id]);
  const extra=Object.keys(GRULLA_ABILITY_CONTRACT).filter(id=>!ids.includes(id));
  const invalid=[];
  for(const [id,def] of Object.entries(GRULLA_ABILITY_CONTRACT)){
    if(!Array.isArray(def.phase)||!def.phase.length)invalid.push(id+':phase');
    if(typeof def.kind!=='string'||!def.kind)invalid.push(id+':kind');
    if(def.consumesAction!==true)invalid.push(id+':consumesAction');
    if(typeof def.profile!=='string'||!def.profile)invalid.push(id+':profile');
  }
  return Object.freeze({
    ok:missing.length===0&&extra.length===0&&invalid.length===0,
    missing:Object.freeze(missing),
    extra:Object.freeze(extra),
    invalid:Object.freeze(invalid)
  });
}
