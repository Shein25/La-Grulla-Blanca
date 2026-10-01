export const RATA_QI_ADAPTIVE_ARSENAL_STATUS='EXPERIMENTAL_NEW_ENGINE_PENDING_NUMERIC_CALIBRATION_V02';
export const RATA_QI_T4_PARAMS_STATUS='PENDING_T0_T4_REBALANCE';

export const RATA_QI_T4_ABILITY=Object.freeze({
  id:'rata_qi__mordisco_frenetico_t4',
  name:'Mordisco Frenético',
  unlockTier:4,
  intentCategory:'OFENSIVA',
  tags:Object.freeze([
    'EXPERIMENTAL_NEW_ENGINE',
    'ADAPTIVE_T4',
    'OFENSIVA',
    'MULTIIMPACTO',
    'INSTINTIVO'
  ]),
  telegraph:'La rata encorva el lomo; el qi robado chisporrotea entre sus incisivos antes de lanzarse en una ráfaga de mordiscos.',
  requirements:Object.freeze({
    anySignals:Object.freeze(['SELF_LOW_HP','SURVIVAL_EVADE_SUCCEEDED'])
  }),
  effect:Object.freeze({
    kind:'MULTI_HIT_BASIC_SCALAR',
    paramsStatus:RATA_QI_T4_PARAMS_STATUS
  }),
  design:Object.freeze({
    identity:'Ráfaga física instintiva basada en el ataque básico nuevo de la especie.',
    numericRule:'Ningún número de impactos, escalar, precisión, penetración, cooldown o daño queda fijado antes de cerrar T0 y recalibrar T1-T4.',
    identityGuard:'No añade memoria táctica, drenaje de Qi, control ni invocaciones por defecto.',
    tierDecay:'Si effectiveAdaptiveTier baja de T4 a T3, la habilidad sale del effectiveKit.'
  })
});

export const RATA_QI_ADAPTIVE_PROGRESSION=Object.freeze({
  T0:Object.freeze({abilities:Object.freeze(['BASIC_ATTACK']),note:'Base natural; parámetros exclusivamente del perfil T0 nuevo.'}),
  T1:Object.freeze({abilities:Object.freeze(['rata_qi__survival_1']),note:'Reflejo de Madriguera; parámetros pendientes de recalibración.'}),
  T2:Object.freeze({abilities:Object.freeze([]),note:'Reconocimiento persistente y defensa anticipatoria; habilidad activa concreta PENDIENTE.'}),
  T3:Object.freeze({abilities:Object.freeze([]),note:'Counter específico de especie; habilidad activa concreta PENDIENTE.'}),
  T4:Object.freeze({abilities:Object.freeze([RATA_QI_T4_ABILITY.id]),note:'Mordisco Frenético conserva identidad, con parámetros PENDIENTES.'})
});

export function rataQiAdaptiveAbilityIds(effectiveAdaptiveTier){
  if(!Number.isInteger(effectiveAdaptiveTier)||effectiveAdaptiveTier<0||effectiveAdaptiveTier>4){
    throw new RangeError('effectiveAdaptiveTier debe ser entero 0..4');
  }
  const ids=[];
  if(effectiveAdaptiveTier>=1)ids.push('rata_qi__survival_1');
  if(effectiveAdaptiveTier>=4)ids.push(RATA_QI_T4_ABILITY.id);
  return Object.freeze(ids.sort());
}
