import {GRULLA_ABILITIES as A} from './grulla-boss-brain-v0.1.mjs';

export const GRULLA_COUNTERPLAY_STATUS='EXPERIMENTAL_NON_CANONICAL_COUNTERPLAY_MATRIX_V01';

export const UNIVERSAL_PLAYER_TOOLS=Object.freeze([
  'BASIC',
  'DEFEND'
]);

export const OPTIONAL_PLAYER_TOOLS=Object.freeze({
  EVADE:'paso_nube',
  GUARD:'piel_cobre',
  CONTROL:'filamento'
});

export const GRULLA_COUNTERPLAY_MATRIX=Object.freeze({
  [A.GOLPE_ALA]:Object.freeze({
    threat:'NORMAL',
    universal:Object.freeze(['BASIC','DEFEND']),
    optional:Object.freeze([]),
    note:'ataque legible normal; no exige técnica especial'
  }),
  [A.CAMPANADA_PICO]:Object.freeze({
    threat:'HEAVY_TELEGRAPHED',
    universal:Object.freeze(['DEFEND']),
    optional:Object.freeze(['EVADE','GUARD','CONTROL']),
    note:'el jugador mínimo puede defender; Paso/Piel/Filamento ofrecen rutas mejores'
  }),
  [A.PATA_INMOVIL]:Object.freeze({
    threat:'SELF_DEFENSE',
    universal:Object.freeze(['BASIC']),
    optional:Object.freeze(['CONTROL']),
    note:'no conviene gastar la mejor ofensiva contra una ventana defensiva'
  }),

  [A.TORMENTA_MIL_PLUMAS]:Object.freeze({
    threat:'HEAVY_QI_PRESSURE',
    universal:Object.freeze(['DEFEND']),
    optional:Object.freeze(['EVADE','GUARD','CONTROL']),
    note:'respuesta universal disponible; las técnicas opcionales preservan recursos de forma distinta'
  }),
  [A.CERRAR_ALAS]:Object.freeze({
    threat:'SELF_DEFENSE',
    universal:Object.freeze(['BASIC']),
    optional:Object.freeze(['CONTROL']),
    note:'ceder daño por una acción barata sigue siendo respuesta válida'
  }),
  [A.RECORDAR_FILO]:Object.freeze({
    threat:'ANTI_REPEAT_PREP',
    universal:Object.freeze(['BASIC']),
    optional:Object.freeze(['CONTROL']),
    note:'mostrar otra herramienta rompe la lectura; Filamento puede además negar la preparación'
  }),
  [A.ECO_MERIDIANO]:Object.freeze({
    threat:'QI_PRESSURE',
    universal:Object.freeze(['BASIC','DEFEND']),
    optional:Object.freeze(['CONTROL']),
    note:'no gastar qi durante la ventana es counterplay suficiente'
  }),

  [A.PICOTAZO_BLANCO]:Object.freeze({
    threat:'PRECISE_ATTACK',
    universal:Object.freeze(['DEFEND']),
    optional:Object.freeze(['EVADE','GUARD','CONTROL']),
    note:'ataque preciso, pero no invalida opciones defensivas'
  }),
  [A.CAMPANA_SIN_DUENO]:Object.freeze({
    threat:'HEAVY_QI_PRESSURE',
    universal:Object.freeze(['DEFEND']),
    optional:Object.freeze(['EVADE','GUARD','CONTROL']),
    note:'remate fuerte; el toolkit mínimo conserva una respuesta'
  }),
  [A.ALA_VACIA]:Object.freeze({
    threat:'SELF_EVASION',
    universal:Object.freeze(['BASIC']),
    optional:Object.freeze(['CONTROL']),
    note:'ataque básico evita malgastar qi durante la evasión'
  }),
  [A.SILENCIO_ENTRE_CAMPANAS]:Object.freeze({
    threat:'PLAN_PREP_ANTI_REPEAT',
    universal:Object.freeze(['BASIC']),
    optional:Object.freeze(['CONTROL']),
    note:'BASIC rompe el patrón; Filamento puede interrumpir la preparación'
  }),
  [A.ROMPER_RITMO]:Object.freeze({
    threat:'PLAN_FINISHER',
    universal:Object.freeze(['DEFEND']),
    optional:Object.freeze(['EVADE','GUARD','CONTROL']),
    note:'si el jugador dejó armar el plan todavía tiene una defensa universal'
  }),
  [A.BUSCAR_PULSO]:Object.freeze({
    threat:'PLAN_PREP_QI',
    universal:Object.freeze(['BASIC','DEFEND']),
    optional:Object.freeze(['CONTROL']),
    note:'una acción sin qi rompe el plan; Filamento añade una salida activa'
  })
});

export function counterplayForGrullaIntent(intentId){
  const x=GRULLA_COUNTERPLAY_MATRIX[intentId];
  if(!x)throw new RangeError('intención Grulla sin counterplay declarado: '+intentId);
  return x;
}

export function validateGrullaCounterplayMatrix(){
  const abilityIds=Object.values(A);
  const missing=abilityIds.filter(id=>!GRULLA_COUNTERPLAY_MATRIX[id]);
  const extra=Object.keys(GRULLA_COUNTERPLAY_MATRIX).filter(id=>!abilityIds.includes(id));
  const optionalOnly=[];
  const unknownOptional=[];

  for(const [id,row] of Object.entries(GRULLA_COUNTERPLAY_MATRIX)){
    if(!row.universal?.some(x=>UNIVERSAL_PLAYER_TOOLS.includes(x)))optionalOnly.push(id);
    for(const tool of row.optional||[]){
      if(!Object.hasOwn(OPTIONAL_PLAYER_TOOLS,tool))unknownOptional.push(id+':'+tool);
    }
  }

  return Object.freeze({
    ok:missing.length===0&&extra.length===0&&optionalOnly.length===0&&unknownOptional.length===0,
    missing:Object.freeze(missing),
    extra:Object.freeze(extra),
    optionalOnly:Object.freeze(optionalOnly),
    unknownOptional:Object.freeze(unknownOptional)
  });
}
