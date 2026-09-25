// Fixtures sintéticos — Monster Combat AI v0.1
//
// Nada aquí es dato canónico de producción. Las habilidades, monstruos y
// snapshots son inventados exclusivamente para este laboratorio.

// ---------------------------------------------------------------------------
// RNG determinista seeded (mulberry32). Sólo para tests/stress del
// laboratorio. El kernel (engine.mjs) NUNCA importa esto: sólo recibe la
// interfaz { random(): number } inyectada por quien lo llama.
// ---------------------------------------------------------------------------

export function createSeededRng(seed) {
  let a = seed >>> 0;
  return {
    random() {
      a |= 0;
      a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    }
  };
}

export const ZERO_RNG = Object.freeze({ random: () => 0 });

// ---------------------------------------------------------------------------
// Catálogo de habilidades sintéticas
// ---------------------------------------------------------------------------

export const ABILITIES = Object.freeze({
  mordida: Object.freeze({
    id: 'mordida',
    intentCategory: 'OFENSIVA',
    tags: Object.freeze(['OFENSIVA']),
    telegraph: 'El monstruo abre las fauces y se lanza al cuerpo a cuerpo.',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 40,
      signalWeights: Object.freeze({ PLAYER_LOW_HP: 5 }),
      memoryWeights: Object.freeze({}),
      socialWeights: Object.freeze({})
    })
  }),

  acechar: Object.freeze({
    id: 'acechar',
    intentCategory: 'PREPARACION',
    tags: Object.freeze(['PREPARACION', 'CAZA']),
    telegraph: 'El lobo baja el cuerpo y mide tu respiración.',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 42,
      signalWeights: Object.freeze({ PLAYER_LOW_HP: 8 }),
      memoryWeights: Object.freeze({ RECUPERACION: 12 }),
      socialWeights: Object.freeze({ MANADA_WITH_ALLY: 5 })
    })
  }),

  tres_flancos: Object.freeze({
    id: 'tres_flancos',
    intentCategory: 'CONTROL',
    tags: Object.freeze(['CONTROL', 'COORDINACION']),
    telegraph: 'La manada se reparte alrededor tuyo en tres puntos.',
    requirements: Object.freeze({ signalsAll: ['ALLY_PRESENT'] }),
    utility: Object.freeze({
      base: 30,
      signalWeights: Object.freeze({ OUTNUMBER_PLAYER: 6 }),
      memoryWeights: Object.freeze({}),
      socialWeights: Object.freeze({ MANADA_WITH_ALLY: 20 })
    })
  }),

  golpe_certero: Object.freeze({
    id: 'golpe_certero',
    intentCategory: 'OFENSIVA',
    tags: Object.freeze(['OFENSIVA', 'FINISHER']),
    telegraph: 'Busca el ángulo exacto para un golpe decisivo.',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 35,
      signalWeights: Object.freeze({ PLAYER_LOW_HP: 10 }),
      memoryWeights: Object.freeze({}),
      socialWeights: Object.freeze({ OPORTUNISTA_LOW_HP: 15 })
    })
  }),

  retirada: Object.freeze({
    id: 'retirada',
    intentCategory: 'EVASION',
    tags: Object.freeze(['EVASION', 'RETIRADA']),
    telegraph: 'Retrocede buscando espacio.',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 20,
      signalWeights: Object.freeze({ SELF_LOW_HP: 12 }),
      memoryWeights: Object.freeze({}),
      socialWeights: Object.freeze({ 'REBAÑO_SELF_LOW_HP': 25 })
    })
  }),

  veneno_lento: Object.freeze({
    id: 'veneno_lento',
    intentCategory: 'CONTROL',
    tags: Object.freeze(['CONTROL']),
    telegraph: 'Ataca buscando inocular veneno.',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 28,
      signalWeights: Object.freeze({}),
      memoryWeights: Object.freeze({ DEFENSA_ABSORCION: -8 }),
      socialWeights: Object.freeze({})
    })
  }),

  estudio_tactico: Object.freeze({
    id: 'estudio_tactico',
    intentCategory: 'PREPARACION',
    tags: Object.freeze(['PREPARACION']),
    telegraph: 'Observa tu patrón antes de comprometerse.',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 18,
      signalWeights: Object.freeze({}),
      memoryWeights: Object.freeze({ DEFENSA_ABSORCION: 10, RECUPERACION: 6 }),
      socialWeights: Object.freeze({})
    })
  }),

  ataque_devastador: Object.freeze({
    id: 'ataque_devastador',
    intentCategory: 'OFENSIVA',
    tags: Object.freeze(['OFENSIVA', 'FINISHER']),
    telegraph: 'Concentra toda su fuerza en un único golpe.',
    cooldownKey: 'ataque_devastador_cd',
    requirements: Object.freeze({ signalsAll: [] }),
    utility: Object.freeze({
      base: 50,
      signalWeights: Object.freeze({ PLAYER_LOW_HP: 6 }),
      memoryWeights: Object.freeze({}),
      socialWeights: Object.freeze({})
    })
  })
});

// ---------------------------------------------------------------------------
// Fixtures de monstruos (sección 17 del prompt maestro)
// ---------------------------------------------------------------------------

export const MONSTERS = Object.freeze({
  rata_fixture: Object.freeze({
    id: 'rata_fixture',
    profileId: 'INSTINTIVO',
    socialProfileId: 'COLONIA',
    effectiveKit: Object.freeze(['mordida', 'retirada']),
    preferences: Object.freeze({ OFENSIVA: 1.1, EVASION: 0.6 }),
    recentAbilityIds: Object.freeze(['mordida'])
  }),

  serpiente_fixture: Object.freeze({
    id: 'serpiente_fixture',
    profileId: 'REACTIVO_1',
    socialProfileId: 'SOLITARIO',
    effectiveKit: Object.freeze(['mordida', 'veneno_lento', 'retirada']),
    preferences: Object.freeze({ OFENSIVA: 0.9, CONTROL: 1.0, EVASION: 0.5 }),
    recentAbilityIds: Object.freeze([])
  }),

  wolf_fixture: Object.freeze({
    id: 'wolf_fixture',
    profileId: 'CAZADOR_2',
    socialProfileId: 'MANADA',
    effectiveKit: Object.freeze(['mordida', 'acechar', 'tres_flancos']),
    preferences: Object.freeze({
      OFENSIVA: 1.0,
      DEFENSA: 0.4,
      EVASION: 0.2,
      CONTROL: 0.3,
      PREPARACION: 0.6
    }),
    recentAbilityIds: Object.freeze([])
  }),

  devorador_fixture: Object.freeze({
    id: 'devorador_fixture',
    profileId: 'TACTICO_3',
    socialProfileId: 'SOLITARIO',
    effectiveKit: Object.freeze(['mordida', 'golpe_certero', 'estudio_tactico', 'retirada']),
    preferences: Object.freeze({ OFENSIVA: 1.0, PREPARACION: 0.8, EVASION: 0.3 }),
    recentAbilityIds: Object.freeze([])
  }),

  mantis_fixture: Object.freeze({
    id: 'mantis_fixture',
    profileId: 'MASTER_4',
    socialProfileId: 'SOLITARIO',
    effectiveKit: Object.freeze(['mordida', 'golpe_certero', 'estudio_tactico', 'ataque_devastador', 'retirada']),
    preferences: Object.freeze({ OFENSIVA: 1.0, PREPARACION: 0.9, EVASION: 0.2 }),
    recentAbilityIds: Object.freeze([])
  })
});

// ---------------------------------------------------------------------------
// Snapshot base reutilizable (sección 7.4)
// ---------------------------------------------------------------------------

export function baseCombat(overrides = {}) {
  return Object.freeze({
    round: 4,
    self: Object.freeze({ hpRatio: 0.72, statuses: Object.freeze([]) }),
    player: Object.freeze({ hpRatio: 0.41, visibleStates: Object.freeze(['ABSORCION_ACTIVA']) }),
    signals: Object.freeze(Object.assign({
      SELF_LOW_HP: 0,
      PLAYER_LOW_HP: 1,
      PLAYER_ABSORPTION: 1,
      PLAYER_EVASION: 0,
      ALLY_PRESENT: 1,
      OUTNUMBER_PLAYER: 1
    }, overrides.signals)),
    ...('round' in overrides ? { round: overrides.round } : {}),
    ...('self' in overrides ? { self: overrides.self } : {}),
    ...('player' in overrides ? { player: overrides.player } : {})
  });
}

export function baseSocial(overrides = {}) {
  return Object.freeze(Object.assign({
    alliesAlive: 1,
    sameSpeciesAllies: 1,
    outnumbersPlayer: true
  }, overrides));
}

export const SAMPLE_MEMORY = Object.freeze([
  Object.freeze({ category: 'DEFENSA_ABSORCION', result: 'EFECTIVA', round: 2 }),
  Object.freeze({ category: 'RECUPERACION', result: 'EFECTIVA', round: 3 })
]);
