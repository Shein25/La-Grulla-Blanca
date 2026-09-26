# Decisión — Decay con hitos evolutivos irreversibles v0.2

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / ENMIENDA DE DISEÑO  
**Rama:** \`experiment/monster-adaptive-survival-lab-v0.1\`

## Objetivo

Conservar el decay de presión sin permitir que una población olvide por completo adaptaciones históricas importantes.

El decay reduce la **adaptación activa**.

Los hitos alcanzados dejan un **piso evolutivo permanente**.

## Regla aprobada

\`\`\`text
máximo histórico T0 → piso T0
máximo histórico T1 → piso T1
máximo histórico T2 → piso T1
máximo histórico T3 → piso T2
máximo histórico T4 → piso T3
\`\`\`

Equivale a:

\`\`\`text
T0 nunca adaptada
→ puede permanecer T0

alcanza T1
→ T1 queda consolidado para siempre

alcanza T2
→ puede decaer a T1
→ nunca vuelve a T0

alcanza T3
→ T2 queda consolidado
→ puede decaer a T2
→ nunca vuelve a T1

alcanza T4
→ T3 queda consolidado
→ puede decaer a T3
→ nunca vuelve a T2
\`\`\`

## Fórmula

\`\`\`text
pressureTier = tier derivado de la presión actual

floorTier =
  maxTierReached == 0 ? 0
  maxTierReached == 1 ? 1
  maxTierReached - 1

effectiveTier =
  max(pressureTier, floorTier)
\`\`\`

## Persistencia

Adaptive Ecology v0.1 estaba congelado con:

\`\`\`text
populationId
speciesId
territoryId
pressure
lastUpdate
recentEventIds
\`\`\`

Esta regla necesita recordar el máximo histórico.

Por tanto v0.2 añade **un único campo persistente**:

\`\`\`text
maxTierReached
\`\`\`

No se persisten:

\`\`\`text
floorTier
pressureTier
effectiveTier
\`\`\`

Los tres se derivan.

Esto evita crear varias fuentes de verdad.

## Thresholds experimentales mantenidos

La calibración propuesta sigue siendo:

\`\`\`text
T0 = presión 0–19
T1 = 20–44    ~10 muertes efectivas
T2 = 45–69    ~25 muertes efectivas
T3 = 70–89    ~50 muertes efectivas
T4 = 90–100   ~90 muertes efectivas
\`\`\`

“Muertes efectivas” es una equivalencia de calibración, no un contador bruto obligatorio.

La presión puede seguir dependiendo de eventos, tiempo y decay.

## Ejemplos

### Población que sólo alcanzó T1

\`\`\`text
peak T1
pressure cae hasta zona T0
floor T1
effective T1
\`\`\`

No pierde su primera adaptación.

### Población que alcanzó T2

\`\`\`text
peak T2
pressure cae
effective T1 mínimo
\`\`\`

Puede relajarse bastante, pero no volver a estado virgen.

### Población que alcanzó T3

\`\`\`text
peak T3
pressure cae de 78 → 40 → 10
pressureTier T3 → T1 → T0
floor T2
effective T3 → T2 → T2
\`\`\`

### Población que alcanzó T4

\`\`\`text
peak T4
pressure 94
→ effective T4

pasa tiempo
pressure 81
→ pressureTier T3
→ effective T3

pasa mucho más tiempo
pressure 12
→ pressureTier T0
→ floor T3
→ effective T3
\`\`\`

T4 es una adaptación extrema reversible.

T3 queda como legado consolidado.

## Semántica

El sistema diferencia:

\`\`\`text
presión actual
≠
aprendizaje histórico
\`\`\`

La presión puede desaparecer.

La población no pierde completamente la historia de haber sido explotada.

## Implementación experimental

Archivo:

\`\`\`text
adaptive/adaptive-ecology-milestone-floor-v0.2.mjs
\`\`\`

Funciones:

- \`consolidatedFloorFromMaxReached()\`
- \`registerReachedTier()\`
- \`effectiveTierAfterDecay()\`
- \`reconcilePopulationAdaptation()\`

Test dirigido:

\`\`\`text
tests/adaptive-ecology-milestone-floor.test.mjs
\`\`\`

El test fija explícitamente la secuencia de pisos:

\`\`\`text
[0, 1, 1, 2, 3]
\`\`\`

para máximos históricos:

\`\`\`text
[T0, T1, T2, T3, T4]
\`\`\`

## Estado

Esto es una **enmienda v0.2** y no modifica silenciosamente Adaptive Ecology v0.1 congelado.
