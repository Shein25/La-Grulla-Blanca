export const RATA_QI_ADAPTIVE_ARSENAL_STATUS='EXPERIMENTAL_NON_CANONICAL_RATA_QI_ADAPTIVE_ARSENAL_V01';

export const RATA_QI_T4_ABILITY=Object.freeze({
  id:'rata_qi__mordisco_frenetico_t4',
  name:'Mordisco Frenético',
  unlockTier:4,
  intentCategory:'OFENSIVA',
  tags:Object.freeze([
    'EXPERIMENTAL_NON_CANONICAL',
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
    hits:2,
    damageScalarPerHit:0.75,
    independentHitRolls:true,
    defenseAppliedPerHit:true,
    absorptionAppliedPerHit:true,
    ignoresDefense:false,
    ignoresAbsorption:false,
    qiDrain:0,
    dot:null,
    control:null
  }),
  cooldownRounds:3,
  design:Object.freeze({
    recoveredConcept:'Mordisco frenético ya figuraba en el kit conceptual histórico de Rata de qi, con tendencia a aparecer cuando estaba herida.',
    newDecision:'Se reserva como candidata T4 y se concreta como ráfaga física de dos mordiscos. Los números son LAB y deben calibrarse con el balance T0 y la progresión T1-T4.',
    identityGuard:'No añade memoria táctica, penetración, drenaje de Qi, control ni invocaciones. La Rata sigue resolviendo el peligro mediante reflejo, movilidad y mordida.',
    tierDecay:'Si effectiveAdaptiveTier baja de T4 a T3, la habilidad sale del effectiveKit.'
  })
});

export const RATA_QI_ADAPTIVE_PROGRESSION=Object.freeze({
  T0:Object.freeze({abilities:Object.freeze(['BASIC_ATTACK']),note:'Base natural. El balance numérico T0 se calibra por separado.'}),
  T1:Object.freeze({abilities:Object.freeze(['rata_qi__survival_1']),note:'Reflejo de Madriguera; ya existente en Survival Evolution.'}),
  T2:Object.freeze({abilities:Object.freeze([]),note:'Capacidad vigente: reconocimiento persistente + defensa anticipatoria. Si se exige una habilidad activa nueva por Tier, queda PENDIENTE diseñarla.'}),
  T3:Object.freeze({abilities:Object.freeze([]),note:'Capacidad vigente: counter específico de especie. La habilidad activa concreta queda PENDIENTE.'}),
  T4:Object.freeze({abilities:Object.freeze([RATA_QI_T4_ABILITY.id]),note:'Segunda adaptación compatible: Mordisco Frenético.'})
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
