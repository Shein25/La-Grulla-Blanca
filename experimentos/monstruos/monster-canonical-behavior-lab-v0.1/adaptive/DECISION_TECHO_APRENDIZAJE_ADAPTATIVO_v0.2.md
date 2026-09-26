# Decisión — El techo limita aprendizaje real v0.2

**Fecha:** 2026-09-26  
**Estado:** SELECCIONADO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Problema

La auditoría detectó una ambigüedad válida:

`adaptiveCapabilityCeiling` podía interpretarse como:

1. techo de **manifestación**: la población aprende tiers ocultos y los revela más tarde;
2. techo de **aprendizaje**: la población no puede almacenar aprendizaje por encima de lo que el jugador actual puede enseñarle.

Se selecciona la segunda interpretación.

## Regla

```text
adaptiveCapabilityCeiling
=
máximo Tier que la población puede APRENDER Y CONSOLIDAR
en el estado actual de progresión del jugador
```

No sólo limita lo que se muestra en combate.

## Consecuencia

Ejemplo:

```text
Rata de Qi
jugador LianQi I
ceiling T1
```

Aunque el jugador la mate de forma obsesiva:

```text
pressure máxima almacenable = 44
pressureTier máximo = T1
maxTierReached máximo = T1
```

No puede precargar T2/T3/T4.

Cuando el jugador llega a LianQi II:

```text
ceiling sube a T2

pressure sigue en 44
effective tier sigue T1
```

La población necesita **nueva presión válida** para:

```text
44 → 45+
→ aprender T2
```

## Caps de presión

Con thresholds seleccionados:

```text
T0 = 0–19
T1 = 20–44
T2 = 45–69
T3 = 70–89
T4 = 90–100
```

el máximo de presión almacenable por ceiling es:

```text
ceiling T0 → 19
ceiling T1 → 44
ceiling T2 → 69
ceiling T3 → 89
ceiling T4 → 100
```

## Motivo

Esto evita:

```text
farmear 90 muertes en una etapa temprana
→ almacenar T4 oculto
→ subir de etapa
→ revelar varios tiers sin nuevos encuentros
```

El jugador debe provocar cada nuevo salto adaptativo **después de haber alcanzado una progresión capaz de enseñarlo**.

## Relación con decay

El ceiling regula aprendizaje nuevo.

El ratchet histórico regula lo que ya fue consolidado.

Por tanto:

```text
pressure actual
→ cap por ceiling
→ pressureTier
→ maxTierReached
→ floor histórico
→ earnedTier
→ effectiveAdaptiveTier
```

Los pisos siguen siendo:

```text
max T0 → floor T0
max T1 → floor T1
max T2 → floor T1
max T3 → floor T2
max T4 → floor T3
```

## Implementación experimental

Archivo:

`adaptive/adaptive-learning-ceiling-v0.2.mjs`

Funciones:

- `pressureTierFromPressure()`
- `pressureCapForAdaptiveCeiling()`
- `clampPressureToAdaptiveCeiling()`
- `reconcileLearningWithCeiling()`

## Invariante

Subir de etapa por sí solo **nunca aumenta el Tier adaptativo efectivo**.

Hace falta un nuevo evento que aumente presión dentro del nuevo ceiling.

## Fuente de verdad

No se añade un segundo XP.

Persistencia prevista:

```text
pressure
maxTierReached
```

El ceiling es derivado de:

```text
playerStage
nativeStage
```

y no se persiste.

## Estado

Esta decisión cierra la ambigüedad detectada por la auditoría antes de implementar el bridge poblacional.
