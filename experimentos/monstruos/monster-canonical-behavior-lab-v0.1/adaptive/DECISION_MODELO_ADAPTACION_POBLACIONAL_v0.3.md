# Decisión — Adaptación poblacional v0.3

**Estado:** ACTIVO / NEW ENGINE ONLY

## Unidad

La adaptación pertenece a una población local:

```text
populationId = territoryId + speciesId
```

Dos poblaciones de una misma especie pueden aprender de forma distinta.

## Tiers

```text
T0 NATURAL
T1 SUPERVIVENCIA
T2 RECONOCIMIENTO
T3 CONTRAADAPTACIÓN
T4 ADAPTACIÓN MADURA
```

T0 es la criatura natural completa. T1–T4 son una presión adaptativa que el jugador provoca voluntariamente al insistir sobre la misma población.

### Capacidades

- T0: arsenal e inteligencia naturales.
- T1: primera respuesta de supervivencia propia de la especie.
- T2: memoria persistente y anticipación elegible.
- T3: counter específico compatible con la especie.
- T4: adaptación madura y segunda respuesta compatible.

La estructura de capacidades no fija números de combate.

## Presión y aprendizaje

Se mantiene el estado poblacional:

```text
pressure
maxTierReached
lastUpdate
recentEventIds
```

Los thresholds de aprendizaje y el decay pertenecen al subsistema Adaptive Ecology. No son estadísticas de combate.

El techo por progresión limita qué puede aprender la población; no concede tiers automáticamente.

## Decay

`maxTierReached` conserva hitos de aprendizaje. La presión actual puede bajar y el piso consolidado se calcula por Adaptive Ecology.

La semántica concreta permanece en:

- `DECISION_DECAY_HITOS_ADAPTATIVOS_v0.2.md`
- `DECISION_TECHO_APRENDIZAJE_ADAPTATIVO_v0.2.md`

## Regla numérica

**No existe escalado universal T1–T4 de HP, daño, Precisión, Evasión, DEF, crítico ni ninguna otra estadística.**

Cada magnitud adaptativa se calibra después de que el T0 de esa especie esté `READY` bajo `NEW_COMBAT_STATS_V0_1`.

Por tanto están prohibidas las tablas globales del tipo:

```text
Tier → +X% HP
Tier → +X% daño
Tier → +X Precisión/Evasión/DEF
Tier → +X crítico
```

La adaptación puede modificar esas propiedades únicamente cuando una habilidad/especie concreta lo declare y haya sido validada con el resolver nuevo.

## Identidad

Una población adaptada debe seguir siendo la misma especie. La dificultad T1–T4 debe surgir de cómo aprende y explota su arsenal, no de convertirla en un saco de estadísticas.

## Pipeline

```text
T0 READY — NEW_COMBAT_STATS_V0_1
→ Population State
→ effectiveAdaptiveTier
→ habilidades/adaptaciones de especie con parámetros READY
→ effectiveKit
→ Monster Combat AI
→ NEW COMBAT RESOLVER
→ resolved signals
→ aprendizaje posterior
```

Si T0 o una adaptación numérica está pendiente, el benchmark de combate debe abortar.
