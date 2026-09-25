# Adaptive Ecology v0.1 — REV2
## Population Pressure & Adaptation Resolver
### Especificación contractual para segunda revisión — 2026-09-25

**Estado:** REV2 DE DISEÑO. NO IMPLEMENTAR TODAVÍA.

Baseline de referencia:
`5812deb59cd1c133383b9af973486a702a26daf4`

Rama futura:
`experiment/monster-ecology-adaptation-v0.1`

## Objetivo

```text
caza repetida de una población local
→ pressure
→ tier derivado
→ adaptaciones reversibles por tier
→ effectiveKit
```

## Fuera de v0.1

- observations semánticas;
- selección por patrón;
- SPECIES_DEFEATED;
- POPULATION_CLEAR;
- REPEATED_HUNT;
- hysteresis;
- cooldown entre cambios de tier;
- aprendizaje irreversible;
- multiplayer;
- loot;
- stat scaling;
- cambio de cognitiveProfile;
- Monster Utility;
- combate;
- save productivo;
- Area Runtime/Dormancy reales.

## Unidad local

La unidad es `populationId + speciesId + territoryId`. Adaptive Ecology no calcula territorios. Dos poblaciones de la misma especie no comparten estado.

## Source of truth persistente

```js
{
  populationId,
  speciesId,
  territoryId,
  pressure,
  lastUpdate,
  recentEventIds
}
```

- `pressure`: entero 0..100.
- `lastUpdate`: tiempo lógico entero seguro.
- `recentEventIds`: ventana acotada sólo para deduplicación defensiva.

No se persisten:
- tier;
- activeAdaptations;
- effectiveKit.

## Config de especie

```js
{
  baseKit,
  thresholds: { tier1, tier2, tier3 },
  adaptationCatalog: {
    tier1: [...],
    tier2: [...],
    tier3: [...]
  },
  pressurePerKill,
  decayPerTimeUnit,
  dedupWindowSize
}
```

Los valores de balance no son canon todavía.

## Evento único de v0.1

Sólo:

```text
SPECIES_KILLED
```

Shape:

```js
{
  eventId,
  type: "SPECIES_KILLED",
  populationId,
  occurredAt
}
```

No existen otras familias de evento en v0.1. Esto elimina el doble conteo entre tipos por construcción.

## Deduplicación

Si `eventId` ya existe en `recentEventIds`:
- no suma pressure;
- no duplica el ID;
- informa `DUPLICATE_EVENT`.

Después de un evento válido, agregar ID y podar determinísticamente al máximo `dedupWindowSize`.

La ventana no pretende ser un event store histórico infinito.

## Tiempo y decay

La API recibe `now` lógico entero seguro.

`now >= lastUpdate`.

Decay lineal, cerrado y O(1):

```text
elapsed = now - lastUpdate
decay = elapsed * decayPerTimeUnit
pressureAfterDecay = max(0, pressure - decay)
```

Proteger overflow.

## Orden transaccional

```text
1 validar
2 decay hasta now
3 lastUpdate = now
4 comprobar dedup
5 comprobar populationId
6 aplicar pressurePerKill
7 clamp 0..100
8 actualizar recentEventIds
9 derivar tier
10 derivar activeAdaptations
11 derivar effectiveKit
12 devolver nextState + view + transition
```

## API

```js
advancePopulation({
  populationState,
  now,
  event = null,
  speciesConfig
})
```

Salida conceptual:

```js
{
  status,
  nextState,
  view: {
    tier,
    activeAdaptations,
    effectiveKit
  },
  transition: {
    pressureBefore,
    pressureAfterDecay,
    pressureAfterEvent,
    tierBefore,
    tierAfter,
    adaptationsAdded,
    adaptationsRemoved
  },
  debug
}
```

## Tier

No se persiste.

Se deriva sólo de:
```text
pressure + thresholds
```

Cuatro niveles:
```text
T0 NORMAL
T1 ALERTA
T2 ADAPTADA
T3 PRESIONADA
```

## Decisión explícita: sin hysteresis/cooldown en v0.1

Se rechazó introducir `lastTierChangeAt` en v0.1 porque haría que el tier dejara de ser una función pura de pressure + config.

Se acepta como limitación experimental que una población cerca de un threshold pueda oscilar.

Hysteresis queda como deuda v0.2.

## Adaptaciones

No se persisten.

Modelo acumulativo y reversible:

```text
T0 → ninguna
T1 → tier1
T2 → tier1 + tier2
T3 → tier1 + tier2 + tier3
```

Si tier baja, adaptaciones superiores se desactivan.

## EffectiveKit

```text
baseKit + activeAdaptations
```

Obligatorio:
- sin duplicados;
- orden canónico;
- reorder invariant;
- determinista;
- no mutación.

## No stat scaling

Prohibido producir:
- hpModifier;
- damageModifier;
- defenseModifier;
- resistanceModifier;
- accuracyModifier.

Pressure nunca modifica `cognitiveProfile`.

## No Monster AI

El módulo termina en `effectiveKit`.

```text
Adaptive Ecology
→ effectiveKit
→ Monster Decision Kernel
```

## Pureza

Inputs inmutables. `recentEventIds` entra y sale como estado explícito; no existe estado global oculto.

## Locality

`event.populationId` debe coincidir exactamente con `populationState.populationId`.

Nunca resolver por speciesId solamente.

## Fixture inicial

Una sola especie sintética `wolf_fixture`:

```text
T0 mordida
T1 + acechar
T2 + tres_flancos
T3 + falsa_apertura
```

No es canon.

## Goldens mínimos

- locality;
- determinismo;
- deep-freeze/no mutation;
- pressure bounds;
- kill exacto;
- eventId duplicado;
- poda determinista de dedup;
- populationId incorrecto;
- tier correcto;
- no transición prematura;
- decay lineal;
- elapsed=0 idempotente;
- tiempo extremo sin overflow;
- event=null = sólo catch-up;
- effectiveKit acumulativo;
- sin duplicados;
- reorder invariance;
- tier != cognitiveProfile;
- cero stat modifiers;
- catálogo vacío → baseKit;
- recalibrar config recalcula tier;
- independencia de poblaciones;
- output canónico;
- sin Math.random();
- cero ejecución de combate.

## Stress

100+ poblaciones sintéticas × miles de secuencias de kill/catch-up.

Críticos esperados en cero:

```text
invalidEffectiveKits
inputMutations
statModifiersProduced
crossPopulationLeaks
nondeterministicMismatches
```

## Deudas v0.2+

- observations semánticas;
- adaptación por patrón;
- observation decay/window;
- hysteresis;
- aprendizaje irreversible;
- eventos adicionales;
- encuentros no letales;
- Area Runtime/Dormancy;
- save productivo;
- telegraph ecológico;
- migración/spawn/reproducción;
- multiplayer.

## Criterio para implementar

Sólo si una segunda revisión confirma:
1. source of truth coherente;
2. dedup explícita y acotada;
3. no doble conteo entre familias;
4. decay O(1);
5. locality cerrada;
6. effectiveKit determinista/reorder invariant;
7. cero stat scaling;
8. cero Monster Utility;
9. cero dependencias productivas;
10. implementación íntegra bajo `experimentos/`.

Veredictos permitidos:

```text
ADAPTIVE_ECOLOGY_V01_REV2_APTA_PARA_IMPLEMENTAR
ADAPTIVE_ECOLOGY_V01_REV2_REQUIERE_CAMBIOS
ADAPTIVE_ECOLOGY_V01_REV2_FALLO_CONCEPTUAL
```

Principio final:

> Una población local puede acumular y perder presión de caza de forma persistente, determinista y auditable, y esa presión puede alterar reversiblemente su repertorio sin tocar estadísticas ni inteligencia base.
