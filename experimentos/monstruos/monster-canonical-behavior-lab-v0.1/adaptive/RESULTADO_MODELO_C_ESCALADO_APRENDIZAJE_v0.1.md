# Resultado — Modelo C · escalado estadístico por aprendizaje adaptativo v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / NO CANÓNICO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Pregunta

Se probó un tercer enfoque:

```text
C — FINAL_E1_ADAPTIVE_LEARNING_STATS
```

La diferencia fundamental frente a B es la fuente del crecimiento.

### Modelo B

```text
etapa nativa de la especie
→ crecimiento físico fijo de banda
```

### Modelo C

```text
presión/aprendizaje real de una población local
→ Tier adaptativo realmente ganado
→ crecimiento estadístico asociado al aprendizaje
```

Por tanto, C **no** significa:

```text
el jugador mata dos criaturas
→ población T4
```

Este benchmark NO modela todavía cuántas muertes, cuánto tiempo o cuánta presión hacen falta para subir de Tier.

Fuerza directamente T1/T2/T3/T4 para responder únicamente:

> si una población llega legítimamente a ese Tier después de explotación sostenida, ¿qué pasa con el combate?

La velocidad de aprendizaje queda separada del balance del efecto.

---

## 2. Estadísticas estudiadas

C prueba cinco ejes:

```text
HP
daño
HIT / precisión
esquiva
crítico
```

No se escala DEF plana.

### Por qué HIT, esquiva y crítico no usan porcentajes ciegos

ver74 resuelve impacto con d20.

- `ataque +1` cruza aproximadamente un breakpoint de 5 puntos porcentuales;
- `esquiva +5` cruza aproximadamente otro breakpoint equivalente;
- bajar `critMin` en 1 añade 5 puntos porcentuales de crítico.

Por eso aplicar “+5% a todo” no es matemáticamente suave.

HP y daño sí admiten crecimiento continuo.

---

## 3. Barrido inicial de sensibilidad

Se compararon cuatro curvas.

### A_FIXED — control

```text
E1
+
stats canónicos
```

### C_GENTLE

```text
HP/daño  +2,5% por Tier
HIT      +1 desde T3
EVA      +5 sólo T4
CRIT     +5 pp sólo T4
```

### C_MEDIUM

```text
HP/daño  +3% por Tier
HIT      +floor(Tier/2)
EVA      +5 × floor(Tier/2)
CRIT     +5 pp × floor(Tier/2)
```

### C_AGGRESSIVE — stress

```text
HP/daño  +5% por Tier
HIT      +1 por Tier
EVA      +5 por Tier
CRIT     +5 pp por Tier
```

El stress agresivo confirmó el riesgo esperado: entregar HIT + EVA + CRIT ya en T1 apila tres breakpoints d20 simultáneos.

Ejemplo contra jugador preparado LianQi IV, T1:

```text
Mantis de Nube
A_FIXED       ~73,8% victoria jugador
C_AGGRESSIVE  ~54,0%

Centinela
A_FIXED       ~82,7%
C_AGGRESSIVE  ~64,2%
```

Ese comportamiento se considera demasiado brusco para la primera adaptación.

---

## 4. Candidato C escalonado

La variante que mejor preservó progresión fue:

```text
C_STAGGERED

T0
stats canónicos
sin adaptación

T1
E1
HP    ×1,025
daño  ×1,025

T2
E1
HP    ×1,05
daño  ×1,05
HIT   +1

T3
E1
HP    ×1,075
daño  ×1,075
HIT   +1
EVA   +5

T4
E1
HP    ×1,10
daño  ×1,10
HIT   +1
EVA   +5
CRIT  5% → 10%
```

La lógica es acumulativa.

No se entregan los tres breakpoints de precisión en el mismo Tier.

---

## 5. Comprobación crítica — T1 en su propia banda

Esta prueba usa al jugador preparado de la **misma etapa nativa** del monstruo.

Así se comprueba que la primera adaptación no rompa el balance recién al aparecer.

400 duelos por build.

Promedio de victoria del jugador:

| Banda | A_FIXED | C_STAGGERED T1 | Cambio |
|---|---:|---:|---:|
| Etapa I | 94,9% | 94,4% | −0,5 pp |
| Etapa II | 71,6% | 70,2% | −1,3 pp |
| Etapa III | 78,8% | 78,1% | −0,7 pp |
| Etapa IV | 87,6% | 86,9% | −0,7 pp |

Casos sensibles:

```text
Sapo Caldera
43,6% → 41,9%

Rey Escarabajo
33,6% → 31,4%

Guardián Coral
35,6% → 34,4%

Mantis de Nube
73,7% → 72,2%

Centinela
82,3% → 81,7%
```

Lectura:

> T1 sigue siendo principalmente “aprendió a sobrevivir”; el +2,5% físico es pequeño y no convierte inmediatamente a la población en otra categoría de enemigo.

---

## 6. Escenario de explotación sostenida a LianQi IV

Se probó el techo legal ya definido:

```text
población nativa Etapa I   → máximo T4
población nativa Etapa II  → máximo T3
población nativa Etapa III → máximo T2
población nativa Etapa IV  → máximo T1
```

Esto NO significa que lleguen automáticamente a ese Tier.

Significa:

> si la población acumuló suficiente aprendizaje real y el techo del jugador lo permite, ése es su máximo posible.

400 duelos por build para confirmar `C_STAGGERED`.

Promedio contra jugador preparado LianQi IV:

| Banda nativa | A_FIXED | C_STAGGERED | Cambio |
|---|---:|---:|---:|
| Etapa I / T4 | 100,0% | 100,0% | ~0 pp |
| Etapa II / T3 | 96,3% | 91,6% | −4,7 pp |
| Etapa III / T2 | 89,5% | 84,0% | −5,5 pp |
| Etapa IV / T1 | 87,4% | 86,6% | −0,8 pp |

Esto es importante:

- volver a Exterior con LianQi IV sigue sintiéndose como haber superado esa zona;
- la adaptación no convierte ratas o avispas en enemigos equivalentes a Alturas;
- poblaciones antiguas más fuertes sí conservan algo de peligro si fueron explotadas durante mucho tiempo.

### Casos representativos

```text
Sapo Caldera — T3
92,4% → 83,0%

Rey Escarabajo — T3
89,4% → 76,4%

Guardián Coral — T2
63,3% → 46,6%

Mantis de Nube — T1
73,2% → 71,9%

Centinela — T1
82,4% → 80,6%
```

El Guardián Coral es el caso más sensible y debe seguir vigilándose.

---

## 7. Comparación de curvas en el techo legal de Arco I

Barrido inicial, 250 duelos por build:

| Curva | Banda I | Banda II | Banda III | Banda IV |
|---|---:|---:|---:|---:|
| A_FIXED | 100,0% | 96,5% | 89,4% | 87,6% |
| C_GENTLE | 100,0% | 92,7% | 86,5% | 87,2% |
| C_STAGGERED* | ~100,0% | 91,6% | 84,0% | 86,6% |
| C_MEDIUM | 100,0% | 90,0% | 79,5% | 86,8% |
| C_AGGRESSIVE | 99,5% | 74,7% | 69,9% | 74,5% |

`C_STAGGERED` se confirmó posteriormente con 400 duelos por build; por eso su fila usa el barrido de confirmación.

Lectura:

- `C_AGGRESSIVE` es demasiado fuerte;
- `C_MEDIUM` empieza a castigar demasiado T2/T3 por acumulación de breakpoints;
- `C_GENTLE` es segura pero concentra demasiadas mejoras discretas al final;
- `C_STAGGERED` distribuye mejor los saltos.

---

## 8. Qué significa “aprender” en C

El crecimiento NO debe depender directamente de:

```text
killCount bruto
```

como único contador.

Debe seguir la arquitectura poblacional:

```text
populationId
→ presión/aprendizaje persistente
→ decay
→ Tier realmente ganado
→ clamp por adaptiveCapabilityCeiling
→ stats/kit correspondientes al Tier efectivo
```

Por tanto:

- matar unos pocos ejemplares no debe llevar a T4;
- la presión puede necesitar repetición sostenida;
- el decay puede hacer perder adaptación si cesa la explotación;
- dos poblaciones de la misma especie pueden estar en Tiers distintos;
- el Tier máximo sigue limitado por la relación entre etapa nativa y etapa del jugador.

Los thresholds concretos de presión para T1–T4 **no se fijan en este benchmark**.

Primero se calibra qué efecto tiene cada Tier; después se decide cuánto esfuerzo debe costar alcanzarlo.

---

## 9. Estado del Modelo C

Se añade como tercer candidato experimental:

```text
A — FINAL_E1_FIXED_STATS
    stats canónicos
    + adaptación conductual

B — FINAL_E1_STAGE_SCALING
    stats físicos por etapa nativa
    + adaptación conductual

C — FINAL_E1_ADAPTIVE_LEARNING_STATS
    stats canónicos de base
    + adaptación conductual
    + crecimiento escalonado sólo si la población realmente aprende
```

Dentro de C, la configuración actualmente más prometedora es:

```text
C_STAGGERED
```

No se declara todavía canónica ni reemplaza automáticamente la preferencia A.

---

## 10. Volumen nuevo de simulación

Para este estudio C se ejecutaron aproximadamente:

```text
486.000   — A / Gentle / Medium / Aggressive · techo legal LianQi IV
1.166.400 — sensibilidad Tier 1–4
388.800   — confirmación A vs C_STAGGERED · techo legal
220.800   — confirmación T1 en etapa nativa
----------------------------------------------
≈2.262.000 duelos nuevos
```

Las cifras Monte Carlo sirven para comparar configuraciones, no prometen tasas exactas de una partida concreta.

---

## 11. Tests cerrados

No se repitieron:

- 107/107 Monster Canonical Behavior;
- 336/336 NPC;
- 15/15 transversal NPC;
- validaciones E1 cerradas.

No se modificaron:

- E1;
- cooldown;
- `CADENCE_COMPAT`;
- Monster Combat AI;
- MOBS canónicos;
- distribución de etapas.

El trabajo fue un benchmark nuevo y documentación experimental.
