export const MONSTER_STAGE_PROGRESSION_STATUS='EXPERIMENTAL_NON_CANONICAL_STAGE_PROGRESSION_V01';

export const STAGE_ROLES=Object.freeze([
  'NORMAL',
  'SKIRMISHER',
  'TANK',
  'ELITE',
  'APEX_BRIDGE',
  'BOSS'
]);

export const STAGE_BANDS=Object.freeze({
  1:Object.freeze({
    playerStage:'LianQi I',
    ecologicalBand:['secta_exterior','bosques'],
    description:'amenazas menores, fauna espiritual inicial y primer depredador serio'
  }),
  2:Object.freeze({
    playerStage:'LianQi II',
    ecologicalBand:['cantera_vetas'],
    description:'criaturas endurecidas por vetas, calor y mineral; primeros jefes regionales'
  }),
  3:Object.freeze({
    playerStage:'LianQi III',
    ecologicalBand:['aguas_barrancos'],
    description:'fauna acuática espiritual, drenaje y encuentros únicos de presión alta'
  }),
  4:Object.freeze({
    playerStage:'LianQi IV',
    ecologicalBand:['alturas'],
    description:'fauna de altura, depredadores avanzados y guardianes finales del Arco I'
  })
});

export const NATIVE_STAGE_BY_MOB=Object.freeze({
  rata_qi:Object.freeze({stage:1,role:'NORMAL',region:'secta_exterior'}),
  avispa_jade:Object.freeze({stage:1,role:'NORMAL',region:'bosques'}),
  serpiente_qi:Object.freeze({stage:1,role:'NORMAL',region:'bosques'}),
  mono_pildoras:Object.freeze({stage:1,role:'SKIRMISHER',region:'bosques'}),
  lobo_espiritual:Object.freeze({stage:1,role:'APEX_BRIDGE',region:'bosques'}),

  sapo_ceniza:Object.freeze({stage:2,role:'NORMAL',region:'cantera_vetas'}),
  escarabajo_hierro:Object.freeze({stage:2,role:'TANK',region:'cantera_vetas'}),
  eco_caido:Object.freeze({stage:2,role:'ELITE',region:'cantera_vetas'}),
  sapo_caldera:Object.freeze({stage:2,role:'BOSS',region:'cantera_vetas'}),
  rey_escarabajo:Object.freeze({stage:2,role:'BOSS',region:'cantera_vetas'}),

  pez_lunar:Object.freeze({stage:3,role:'NORMAL',region:'aguas_barrancos'}),
  anguila_estelar:Object.freeze({stage:3,role:'SKIRMISHER',region:'aguas_barrancos'}),
  sombra_ahogada:Object.freeze({stage:3,role:'ELITE',region:'aguas_barrancos'}),
  guardian_coral:Object.freeze({stage:3,role:'BOSS',region:'aguas_barrancos'}),

  devorador_niebla:Object.freeze({stage:4,role:'NORMAL',region:'alturas'}),
  halcon_tormenta:Object.freeze({stage:4,role:'SKIRMISHER',region:'alturas'}),
  mantis_nube:Object.freeze({stage:4,role:'BOSS',region:'alturas'}),
  centinela_pluma:Object.freeze({stage:4,role:'BOSS',region:'alturas'})
});

// La etapa del jugador limita QUÉ puede aprender una población, pero no concede
// estadísticas automáticamente. adaptiveXp/encuentros seguirá decidiendo SI lo aprende.
export const ADAPTIVE_CAPABILITY_BY_STAGE_DELTA=Object.freeze({
  0:Object.freeze({
    tier:1,
    label:'SUPERVIVENCIA',
    capabilities:['SURVIVAL_ACTION']
  }),
  1:Object.freeze({
    tier:2,
    label:'RECONOCIMIENTO_DE_PATRONES',
    capabilities:['SURVIVAL_ACTION','PERSISTENT_PATTERN_MEMORY','PREEMPTIVE_SURVIVAL_ELIGIBLE']
  }),
  2:Object.freeze({
    tier:3,
    label:'CONTRAADAPTACION',
    capabilities:['SURVIVAL_ACTION','PERSISTENT_PATTERN_MEMORY','PREEMPTIVE_SURVIVAL_ELIGIBLE','SPECIES_COUNTER_BRANCH_ELIGIBLE']
  }),
  3:Object.freeze({
    tier:4,
    label:'ADAPTACION_MADURA',
    capabilities:['SURVIVAL_ACTION','PERSISTENT_PATTERN_MEMORY','PREEMPTIVE_SURVIVAL_ELIGIBLE','SPECIES_COUNTER_BRANCH_ELIGIBLE','SECONDARY_ADAPTATION_ELIGIBLE']
  })
});

export function nativeStageOf(mobId){
  const x=NATIVE_STAGE_BY_MOB[mobId];
  if(!x)throw new RangeError(`monstruo sin etapa nativa: ${mobId}`);
  return x.stage;
}

export function stageRelation(mobId,playerStage){
  if(!Number.isInteger(playerStage)||playerStage<1||playerStage>4){
    throw new RangeError('playerStage debe ser 1..4');
  }
  const nativeStage=nativeStageOf(mobId);
  const delta=playerStage-nativeStage;
  return Object.freeze({
    mobId,
    nativeStage,
    playerStage,
    delta,
    relation:delta<0?'AHEAD_OF_PLAYER':delta===0?'NATIVE_MATCH':'PLAYER_OUTGREW_NATIVE_STAGE'
  });
}

export function adaptiveCapabilityCeiling(mobId,playerStage){
  const relation=stageRelation(mobId,playerStage);
  // Un monstruo encontrado antes de su etapa nativa no recibe una bonificación:
  // ya es una amenaza adelantada. La capa adaptativa empieza al alcanzar su banda.
  const delta=Math.max(0,Math.min(3,relation.delta));
  return Object.freeze({
    ...relation,
    ...ADAPTIVE_CAPABILITY_BY_STAGE_DELTA[delta]
  });
}
