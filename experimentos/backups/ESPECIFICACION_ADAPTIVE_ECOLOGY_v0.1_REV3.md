# LA GRULLA BLANCA
# Adaptive Ecology v0.1 — REV3
## Population Pressure & Adaptation Resolver
### Especificación contractual candidata a implementación — 2026-09-25

## 0. Estado

**REV3 DE DISEÑO. TODAVÍA NO IMPLEMENTAR HASTA CERRAR ESTA TERCERA REVISIÓN.**

Esta revisión incorpora los hallazgos de las dos revisiones conceptuales externas anteriores.

Baseline Git de referencia:

`5812deb59cd1c133383b9af973486a702a26daf4`

Rama futura propuesta:

`experiment/monster-ecology-adaptation-v0.1`

Toda futura implementación debe vivir únicamente en `experimentos/`.

---

# 1. Objetivo v0.1

Probar una cadena mínima y auditable:

```text
caza repetida de una población local
→ pressure
→ tier derivado
→ adaptaciones reversibles por tier
→ effectiveKit
```

v0.1 NO intenta todavía adaptar la respuesta según el tipo de táctica usada por el jugador.

---

# 2. Fuera de alcance v0.1

Quedan fuera:

- observations semánticas;
- selección de adaptación por patrón;
- observation poisoning;
- SPECIES_DEFEATED;
- POPULATION_CLEAR;
- REPEATED_HUNT;
- hysteresis;
- cooldown entre cambios de tier;
- aprendizaje irreversible;
- multiplayer;
- cambios de loot;
- cambios de stats;
- cambios de cognitiveProfile;
- Monster Utility;
- ejecución de combate;
- integración con save productivo;
- Area Runtime;
- Dormancy real;
- migración/reproducción/spawns.

Estas capacidades pueden evaluarse en v0.2+.

---

# 3. Unidad de estado

La unidad es una población local explícita:

```js
{
  populationId: "bosque_norte:lobo_tres_colas",
  speciesId: "lobo_tres_colas",
  territoryId: "bosque_norte"
}
```

Adaptive Ecology no calcula territorios.

Una capa superior es responsable de entregar un `populationId` ecológicamente coherente.

Dos poblaciones de la misma especie son independientes.

---

# 4. Estado persistente — fuente de verdad

v0.1 persiste solamente:

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

## 4.1 `pressure`

- entero;
- rango `0..100`;
- fuente principal del tier;
- clamp obligatorio.

## 4.2 `lastUpdate`

Tiempo lógico de la última evolución del estado.

Debe ser entero seguro no negativo.

## 4.3 `recentEventIds`

Ventana acotada usada únicamente para deduplicación defensiva.

No puede crecer indefinidamente.

Su tamaño máximo se declara en config.

No es memoria ecológica ni narrativa.

---

# 5. Configuración de especie

No se duplica dentro del estado de cada población.

Shape conceptual:

```js
{
  baseKit,

  thresholds: {
    tier1,
    tier2,
    tier3
  },

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

Todos los valores numéricos usados por el resolver deben ser enteros seguros dentro de rangos contractuales explícitos.

Los números de balance todavía NO son canon.

---

# 6. Evento único de v0.1

La única fuente positiva de pressure es:

```text
SPECIES_KILLED
```

Shape:

```js
{
  eventId,
  type: "SPECIES_KILLED",
  populationId
}
```

`occurredAt` se elimina deliberadamente de v0.1.

El resolver sólo tiene un reloj lógico autoritativo: `now`.

No existe en v0.1 un segundo timestamp de evento con semántica ambigua.

No existe `SPECIES_DEFEATED`, `POPULATION_CLEAR` ni `REPEATED_HUNT` en v0.1.

Esto elimina el doble conteo entre familias de eventos por construcción.

---

# 7. Deduplicación

Cada evento debe traer `eventId`.

Si `eventId` ya está en `recentEventIds`:

```text
no cambia pressure
no cambia lastUpdate por causa del evento
no duplica el ID
resultado informa DUPLICATE_EVENT
```

Después de aplicar un evento válido:

```text
eventId se agrega a recentEventIds
```

Si excede `dedupWindowSize`, se descartan los IDs más antiguos mediante FIFO por **orden de aplicación exitoso**.

No se ordena por timestamp ni por valor lexicográfico del `eventId`.

La ventana es acotada para evitar crecimiento infinito del save.

## 7.1 Garantía exacta de deduplicación

La deduplicación de v0.1 protege únicamente contra reintentos cercanos que todavía estén dentro de `recentEventIds`.

Cuando un `eventId` sale de la ventana FIFO, un reenvío posterior del mismo ID **puede volver a aplicarse** como evento nuevo.

Esto es una limitación conocida y aceptada de v0.1, no una garantía de exactly-once global.

Responsabilidad de integración futura:

- el emisor debe evitar replays fuera de la ventana;
- `dedupWindowSize` debe dimensionarse para el horizonte real de reintentos;
- si Dormancy/Catch-up necesita garantías más fuertes, v0.2 deberá introducir secuencia monotónica, event store u otra estrategia explícita.

La ventana no es memoria ecológica ni narrativa.

---

# 8. Tiempo lógico

El módulo recibe `now` como tiempo lógico entero seguro.

No conoce:

- reloj real;
- world tick concreto;
- Scheduler;
- Area Runtime.

Requisito:

```text
now >= state.lastUpdate
```

Un `now` menor es error contractual.

---

# 9. Decay lineal

Antes de aplicar un evento nuevo, el estado se lleva desde `lastUpdate` hasta `now`.

Fórmula conceptual:

```text
elapsed = now - lastUpdate
decay = elapsed * decayPerTimeUnit
pressureAfterDecay = max(0, pressure - decay)
```

Toda aritmética debe proteger:

- overflow;
- NaN;
- Infinity.

No se simula turno por turno.

`elapsed = 0` debe ser idempotente.

---

# 10. Orden transaccional

Para una evolución con evento:

```text
1. validar input estructural y config
2. si hay evento, validar locality:
   event.populationId === populationState.populationId
   si falla → error duro INVALID_POPULATION, sin modificar estado
3. calcular decay hasta now
4. actualizar lastUpdate = now
5. si hay evento, comprobar deduplicación
6. si no es duplicado, aplicar pressurePerKill
7. clamp 0..100
8. si no es duplicado, actualizar recentEventIds y podar FIFO
9. derivar tier
10. derivar activeAdaptations
11. derivar effectiveKit
12. devolver nextState + view + transition
```

La locality se valida antes que dedup para que un error de enrutamiento nunca quede enmascarado como `DUPLICATE_EVENT`.

El decay ocurre antes del efecto del kill porque el tiempo transcurrido es real aunque el evento resulte duplicado.

Por tanto, un `DUPLICATE_EVENT` puede devolver un `nextState` con `pressure` reducido por decay y `lastUpdate = now`, pero nunca agrega pressure ni reordena/reinserta el `eventId`.

---

# 11. API v0.1

API principal propuesta:

```js
advancePopulation({
  populationState,
  now,
  event = null,
  speciesConfig
})
```

`event = null` permite sólo aplicar catch-up/decay.

Salida:

```js
{
  status,

  nextState: {
    populationId,
    speciesId,
    territoryId,
    pressure,
    lastUpdate,
    recentEventIds
  },

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

`debug` sólo existe en laboratorio.

Estados de dominio mínimos:

```text
OK
DUPLICATE_EVENT
```

Errores contractuales/locality deben distinguirse de estados normales. Como mínimo:

```text
INVALID_POPULATION
INVALID_INPUT
INVALID_CONFIG
```

`INVALID_POPULATION` nunca puede degradarse a `DUPLICATE_EVENT`.

---

# 12. Tier

`tier` NO se persiste.

Se deriva exclusivamente del `pressure` actual + thresholds de config.

Cuatro niveles:

```text
T0 NORMAL
T1 ALERTAJ
T2 ADPTADA
T3 PRESIONADA
```

Los nombres pueden cambiar antes de producción.

Los thresholds deben ser estrictamente crecientes.

---

# 13. Decisión explícita sobre hysteresis

v0.1 NO implementa:

- hysteresis;
- cooldown de tier;
- `lastTierChangeAt`.

Motivo:

> v0.1 todavía no tiene ningún consumidor real de las transiciones de tier: no hay telegraph productivo, no hay ejecución de combate y Monster Combat AI no consume este `effectiveKit` dentro de un encuentro real. La oscilación cerca de un threshold es, por ahora, observable sólo en el laboratorio.

Por tanto, en v0.1 se acepta como limitación conocida que una población cerca de un threshold pueda alternar tiers al subir/bajar pressure.

Ese problema queda como deuda explícita para v0.2.

Cuando exista un consumidor real, v0.2 deberá decidir además si `effectiveKit` se congela al inicio de cada encuentro para impedir cambios a mitad de combate.

---

# 14. Active adaptations

`activeAdaptations` NO se persiste.

Se deriva de:

```text
tier + adaptationCatalog
```

Modelo v0.1: acumulativo.

Ejemplo:

```text
T0 → ninguna
T1 → tier1
T2 → tier1 + tier2
T3 → tier1 + tier2 + tier3
```

Si el tier baja, las adaptaciones superiores dejan de estar activas.

Reversibilidad total en v0.1.

---

# 15. Effective Kit

Se deriva:

```text
baseKit
+
activeAdaptations
=
effectiveKit
```

Reglas:

- sin duplicados;
- orden canónico estable;
- determinista;
- no depende del orden de entrada;
- no muta config;
- no muta state.

## 15.1 Orden canónico

Los IDs de ability usados por este laboratorio deben ser strings ASCII normalizados:

```text
^[a-z0-9][a-z0-9_.:-]*$
```

`effectiveKit` se ordena ascendentemente por ID usando comparación ordinal simple, nunca `localeCompare()` ni el orden de aparición en arrays de config.

Dos configs semánticamente idénticas con arrays reordenados deben producir byte a byte el mismo `effectiveKit`.

## 15.2 Existencia semántica de ability

Adaptive Ecology v0.1 no recibe el catélogo autoritativo de habilidades de combate.

Por tanto:

- valida que los IDs tengan shape válido;
- NO inventa habilidades;
- NO intenta decidir si un ID existe en el futuro catálogo de combate;
- NO filtra silenciosamente IDs por una autoridad que no posee.

La validación cruzada contra `H"AB���q�^