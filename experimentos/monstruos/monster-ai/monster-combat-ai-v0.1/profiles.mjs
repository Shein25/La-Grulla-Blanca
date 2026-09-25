// Perfiles cognitivos y sociales sintéticos — Monster Combat AI v0.1
//
// Los perfiles cognitivos NO conocen nada del motor de combate real.
// Son puramente parámetros de decisión: memoria, anti-repetición, jitter.

export const PROFILES = Object.freeze({
  INSTINTIVO: Object.freeze({
    id: 'INSTINTIVO',
    memoryDepth: 0,
    repetitionPenalty: 3,
    jitter: 4,
    usesMemory: false,
    usesSocial: false
  }),
  REACTIVO_1: Object.freeze({
    id: 'REACTIVO_1',
    memoryDepth: 1,
    repetitionPenalty: 5,
    jitter: 3,
    usesMemory: true,
    usesSocial: false
  }),
  CAZADOR_2: Object.freeze({
    id: 'CAZADOR_2',
    memoryDepth: 2,
    repetitionPenalty: 8,
    jitter: 2,
    usesMemory: true,
    usesSocial: true
  }),
  TACTICO_3: Object.freeze({
    id: 'TACTICO_3',
    memoryDepth: 3,
    repetitionPenalty: 12,
    jitter: 1.5,
    usesMemory: true,
    usesSocial: true
  }),
  MASTER_4: Object.freeze({
    id: 'MASTER_4',
    memoryDepth: 4,
    repetitionPenalty: 16,
    jitter: 1,
    usesMemory: true,
    usesSocial: true
  })
});

// Los perfiles sociales v0.1 son sólo identificadores declarativos: el
// engine deriva flags booleanos (ver computeSocialFlags en engine.mjs) a
// partir de socialProfileId + contexto social + señales. No hay
// coordinación real, refuerzos, ni formación espacial (ver sección 10 del
// prompt maestro).
export const SOCIAL_PROFILES = Object.freeze({
  SOLITARIO: Object.freeze({ id: 'SOLITARIO' }),
  TERRITORIAL: Object.freeze({ id: 'TERRITORIAL' }),
  MANADA: Object.freeze({ id: 'MANADA' }),
  COLONIA: Object.freeze({ id: 'COLONIA' }),
  OPORTUNISTA: Object.freeze({ id: 'OPORTUNISTA' }),
  RED: Object.freeze({ id: 'RED' }),
  'REBAÑO': Object.freeze({ id: 'REBAÑO' })
});
