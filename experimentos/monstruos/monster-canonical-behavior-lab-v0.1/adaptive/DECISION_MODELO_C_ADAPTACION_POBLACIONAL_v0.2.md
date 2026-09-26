# Decisión maestra — Modelo C de adaptación poblacional v0.2

**Fecha:** 2026-09-26  
**Estado de diseño:** SELECCIONADO  
**Estado de implementación:** EXPERIMENTAL / NO INTEGRADO A PRODUCCIÓN  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Modelo elegido

Se selecciona como dirección de diseño para la adaptación de monstruos:

```text
C — FINAL_E1_ADAPTIVE_LEARNING_STATS
variante: C_STAGGERED
```

La adaptación depende de la **población local y de lo que realmente ha aprendido bajo presión**.

No depende automáticamente:

- de la etapa nativa del monstruo;
- del nivel del jugador;
- de haber matado dos o tres ejemplares;
- de un multiplicador global de dificultad.

A queda como control histórico.

B queda como comparación descartada para la dirección adaptativa porque escala por etapa nativa, no por aprendizaje real.

---

## 2. Unidad de adaptación

La unidad es:

```text
populationId
= territoryId + speciesId
```

Dos poblaciones de la misma especie pueden evolucionar de manera distinta.

No existe aprendizaje telepático global de especie.

---

## 3. Progresión adaptativa seleccionada

### T0 — NATURAL

```text
stats canónicos
comportamiento natural
sin adaptación aprendida
```

### T1 — SUPERVIVENCIA

Capacidad aprendida:

```text
E1 defensiva propia de la especie
```

Stats:

```text
HP    ×1,025
daño  ×1,025
```

T1 representa la primera respuesta estable a la presión.

### T2 — RECONOCIMIENTO

Capacidades:

```text
E1
+
memoria persistente de patrones
+
defensa anticipatoria elegible
```

Stats:

```text
HP    ×1,05
daño  ×1,05
HIT   +1
```

### T3 — CONTRAADAPTACIÓN

Capacidades:

```text
todo T2
+
counter específico permitido por especie
```

Stats:

```text
HP    ×1,075
daño  ×1,075
HIT   +1
EVA   +5
```

### T4 — ADAPTACIÓN MADURA

Capacidades:

```text
todo T3
+
segunda adaptación compatible
```

Stats:

```text
HP    ×1,10
daño  ×1,10
HIT   +1
EVA   +5
CRIT  5% → 10%
```

Las mejoras son acumulativas.

---

## 4. Velocidad de adaptación

La referencia inicial de calibración queda:

```text
T1 ≈ 10 muertes efectivas
T2 ≈ 25 muertes efectivas acumuladas
T3 ≈ 50 muertes efectivas acumuladas
T4 ≈ 90 muertes efectivas acumuladas
```

No son obligatoriamente un contador bruto de kills.

La fuente real debe ser presión/aprendizaje poblacional.

Thresholds de presión de trabajo:

```text
T0 = 0–19
T1 = 20–44
T2 = 45–69
T3 = 70–89
T4 = 90–100
```

La conversión entre eventos de caza y presión se calibrará después.

---

## 5. Techo por progresión del jugador

El jugador limita hasta dónde **puede** aprender una población, pero no concede el Tier.

```text
playerStage < nativeStage      → máximo T0
playerStage == nativeStage     → máximo T1
playerStage == nativeStage + 1 → máximo T2
playerStage == nativeStage + 2 → máximo T3
playerStage == nativeStage + 3 → máximo T4
```

Por tanto:

```text
effectiveAdaptiveTier
=
min(
  tier ganado por población,
  adaptiveCapabilityCeiling
)
```

---

## 6. Decay con consolidación histórica

La presión actual puede bajar.

El aprendizaje histórico no se borra completamente.

Se persiste:

```text
maxTierReached
```

Pisos irreversibles:

```text
máximo histórico T0 → piso T0
máximo histórico T1 → piso T1
máximo histórico T2 → piso T1
máximo histórico T3 → piso T2
máximo histórico T4 → piso T3
```

Ejemplos:

```text
alcanzó T1
→ jamás vuelve a T0

alcanzó T2
→ puede bajar a T1
→ jamás T0

alcanzó T3
→ puede bajar a T2
→ jamás T1

alcanzó T4
→ puede bajar a T3
→ jamás T2
```

Fórmula:

```text
floorTier = consolidación(maxTierReached)

effectiveEarnedTier =
max(
  pressureTier,
  floorTier
)
```

Luego se aplica el techo del jugador:

```text
effectiveAdaptiveTier =
min(
  effectiveEarnedTier,
  adaptiveCapabilityCeiling
)
```

---

## 7. Qué escala y qué no

Modelo C sí puede modificar por aprendizaje:

- HP;
- daño;
- HIT;
- esquiva;
- crítico;
- repertorio de habilidades;
- memoria;
- capacidades anticipatorias;
- counters específicos.

No se añade por defecto:

- DEF plana escalada proporcionalmente;
- inmunidad global elemental;
- resistencia universal;
- nivel artificial por jugador.

Especialmente HIT / EVA / CRIT permanecen escalonados porque cada breakpoint del d20 es fuerte.

---

## 8. Principio de identidad

Una población adaptada debe sentirse como:

> la misma especie que aprendió a sobrevivir mejor.

No como:

> un monstruo de una zona superior con la skin de una rata.

Por eso incluso T4 conserva estadísticas base e identidad de especie.

---

## 9. Estado de A y B

### A — FINAL_E1_FIXED_STATS

```text
CONSERVADO COMO BASELINE / CONTROL
```

Sirve para medir cuánto aporta C.

Ya no es la dirección seleccionada.

### B — FINAL_E1_STAGE_SCALING

```text
CONSERVADO COMO COMPARACIÓN
```

No se continúa como modelo de adaptación porque su crecimiento depende de la etapa nativa, no del aprendizaje real de la población.

---

## 10. Fuente de verdad prevista

Persistencia mínima poblacional:

```text
populationId
speciesId
territoryId
pressure
maxTierReached
lastUpdate
recentEventIds
```

Derivados, no persistidos:

```text
pressureTier
floorTier
earnedTier
capabilityCeiling
effectiveAdaptiveTier
activeAdaptations
effectiveKit
adaptiveStats
```

No se crea un `survivalXp` productivo paralelo.

---

## 11. Bridge futuro

La integración prevista queda:

```text
Population State
        ↓
pressure + maxTierReached
        ↓
earned adaptive tier
        ↓
clamp por player/native stage
        ↓
effective adaptive tier
        ↓
C_STAGGERED stats
        +
adaptive abilities
        ↓
effectiveKit
        ↓
Monster Combat AI
        ↓
Combat Ability Executor
```

`CADENCE_COMPAT` sigue siendo autoridad hasta que exista una decisión explícita que lo sustituya.

---

## 12. Decisión cerrada

Para continuar el desarrollo de adaptación poblacional:

```text
MODELO SELECCIONADO = C_STAGGERED
```

No se vuelve a abrir A vs B vs C salvo que futuros tests de integración demuestren un problema concreto que invalide esta decisión.
