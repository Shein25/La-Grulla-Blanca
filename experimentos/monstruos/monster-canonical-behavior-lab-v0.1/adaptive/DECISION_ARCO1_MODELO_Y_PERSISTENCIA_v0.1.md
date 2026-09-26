# Decisión experimental — Modelo Arco I y fuente de verdad adaptativa v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / NO CANÓNICO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Modelo preferido para Arco I

Se fija como **preferencia experimental de trabajo**:

```text
A — FINAL_E1_FIXED_STATS
```

Es decir:

```text
estadísticas canónicas ver74
+
defensas E1 definitivas
+
adaptación conductual
```

El modelo B:

```text
B — FINAL_E1_STAGE_SCALING
HP/daño 100/105/110/115%
```

permanece conservado como **modelo de sensibilidad / comparación**, no se elimina ni se invalida.

### Motivos

1. La dificultad física por banda ya existe en las fichas canónicas y en los roles NORMAL / SKIRMISHER / TANK / ELITE / BOSS.
2. E1 fue diseñada para añadir supervivencia y aprendizaje, no para convertir la adaptación en crecimiento estadístico oculto.
3. El modelo A mantiene mayor peso de:
   - técnicas;
   - equipo;
   - preparación;
   - Monster Combat AI;
   - aprendizaje adaptativo.
4. Preserva mejor la sensación de superar zonas antiguas.
5. Evita apilar simultáneamente:
   - estadísticas canónicas crecientes;
   - rol regional;
   - defensas E1;
   - escalado adicional de HP/daño.
6. Es coherente con el principio de Adaptive Ecology:
   la población cambia su repertorio por presión, no sus estadísticas porque el jugador sea más fuerte.

Esta preferencia sigue siendo experimental hasta una decisión canónica explícita.

## 2. Hallazgo de arquitectura: no persistir dos sistemas adaptativos

Actualmente `survival-evolution-v0.1.mjs` recibe:

```text
survivalXp
→ survivalEvolutionStage
```

pero esos valores todavía no tienen almacenamiento real.

En paralelo, la especificación congelada de Adaptive Ecology define como fuente persistente de verdad una **población local**:

```text
populationId
speciesId
territoryId
pressure
lastUpdate
recentEventIds
```

y deriva el tier/adaptaciones desde ese estado.

Por tanto, NO se debe añadir a producción otra fuente persistente independiente como:

```text
population.survivalXp
population.evolutionStage
```

sin reconciliar antes ambos modelos.

Eso produciría dos autoridades capaces de responder por separado a la misma pregunta:

> ¿qué adaptación ha aprendido esta población?

## 3. Unidad de adaptación

La unidad acordada para criaturas comunes es la **población local**, no la especie global.

Ejemplo conceptual:

```text
bosque_norte:rata_qi
bosque_sur:rata_qi
```

pueden evolucionar de manera distinta.

Los únicos pueden conservar semántica individual cuando corresponda, pero no se introduce aquí un segundo motor.

## 4. Separación de responsabilidades

Se mantienen dos ejes distintos:

### A. Techo adaptativo por progresión del jugador

`adaptiveCapabilityCeiling(mobId, playerStage)` responde:

```text
¿hasta qué Tier PODRÍA llegar esta población?
```

Regla ya fijada:

```text
playerStage < nativeStage      → Tier 0
playerStage == nativeStage     → techo Tier 1
playerStage == nativeStage + 1 → techo Tier 2
playerStage == nativeStage + 2 → techo Tier 3
playerStage == nativeStage + 3 → techo Tier 4
```

### B. Adaptación realmente ganada por la población

Adaptive Ecology / estado poblacional responde:

```text
¿cuánto aprendizaje/presión ganó realmente esta población?
```

El techo de etapa NO concede adaptación por sí solo.

## 5. Regla de composición futura

La composición debe respetar conceptualmente:

```text
tier efectivo
=
mínimo(
  techo permitido por relación playerStage/nativeStage,
  tier realmente ganado por la población
)
```

pero **no se implementa todavía esta fórmula** porque existe una incompatibilidad contractual pendiente:

- Stage Progression define Tier 0..4.
- Adaptive Ecology v0.1 define T0..T3.
- Tier 4 (segunda adaptación compatible) todavía no tiene un umbral poblacional aprobado.

Inventar ahora un cuarto threshold, reciclar T3 o persistir un contador paralelo rompería la regla de no crear nuevas arquitecturas sin necesidad.

## 6. Papel actual de survivalXp

Hasta reconciliar la progresión poblacional:

`survivalXp` queda clasificado como **parámetro de laboratorio para calibrar el desbloqueo E1**, no como campo de save productivo.

Se conservan sus valores experimentales actuales:

```text
común  → unlock E1 en 6 XP
único  → unlock E1 en 4 XP
encuentro válido → +1
HP bajo o golpe fuerte observado → +1 adicional
máximo → 2 por encuentro
```

No se cambian ni se vuelven a balancear en este cierre.

## 7. Próximo trabajo válido

Antes de escribir persistencia productiva:

1. reconciliar T0..T3 de Adaptive Ecology con Tier 0..4 de Stage Progression;
2. definir cómo se gana específicamente Tier 4;
3. decidir si los thresholds de presión sustituyen por completo los thresholds 4/6 XP de E1 o si esos valores sólo sirven como calibración de equivalencia;
4. después crear un bridge fino:
   ```text
   Population State
   → tier ganado
   → clamp por adaptiveCapabilityCeiling
   → effective adaptive tier
   → effectiveKit
   → Monster Combat AI
   ```
5. mantener `CADENCE_COMPAT` como autoridad;
6. no tocar todavía el executor defensivo hasta que la fuente de verdad adaptativa quede única.

## 8. Tests

No se repitió ningún test cerrado.

Este cambio es exclusivamente documental y no modifica:

- valores E1;
- cooldown;
- distribución de etapas;
- Monster Combat AI;
- `CADENCE_COMPAT`;
- stats canónicos;
- Modelo B de comparación.

Por tanto, no invalida los baselines cerrados ni requiere reejecutarlos.
