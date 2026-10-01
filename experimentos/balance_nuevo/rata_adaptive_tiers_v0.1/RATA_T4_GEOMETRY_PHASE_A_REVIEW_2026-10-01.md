# Rata T4 — Mordisco Frenético — Phase A geometry review

Fecha: 2026-10-01

## Objetivo

Probar una primera interpretación literal:

```text
T2 decide BASIC
→ T4 listo
→ reemplazar BASIC por Mordisco Frenético
→ todos los packets derivados del 2d4 canónico
```

Ejes fijos:

- precisión independiente por hit;
- crítico independiente por hit;
- CD5;
- DEF plana y absorción por hit;
- T1–T3 congelados.

## Control técnico

El harness `HARNESS_INSTANCE_BASIC_1X100` reproduce el BASIC individual y se
usa sólo para verificar que el arnés no altera T3.

Tras corregir el respeto a `skip_next_action`, el control reproduce el
baseline T3 exactamente.

Esto también confirma que T4 no puede ignorar Control del jugador.

## Estudio dirigido

30.000 combates VETERAN:

- T3 baseline;
- 4 geometrías T4;
- normales + Mutantes.

Baseline T3:

```text
normal:
monster damage 6,635
HP jugador     79,03%

Mutante:
monster damage 10,835
HP jugador      65,78%
```

### CONTROL_1X100 — 1 × 2d4 canónico

Normal:

- ~0,971 usos/pelea;
- 2,62 daño/uso;
- daño total monstruo -1,15/pelea vs T3;
- presión HP -3,63 pp.

Mutante:

- ~1,055 usos/pelea;
- 2,75 daño/uso;
- daño total -1,83/pelea;
- presión HP -5,80 pp.

Interpretación: reemplazar el BASIC individual por 2d4 canónico borra parte de
la variabilidad ofensiva ya ratificada.

### FRENZY_2X050

Normal:

- 2 packets/uso;
- 1,44 daño/uso;
- daño total -2,11/pelea.

Mutante:

- 1,50 daño/uso;
- daño total -3,46/pelea.

Es el peor candidato. Igualar la expectativa bruta de 2d4 no iguala daño real,
porque DEF plana/absorción actúan por packet.

**Descartado.**

### FRENZY_2X075

Normal:

- 3,28 daño/uso;
- daño total -0,275/pelea;
- presión HP -0,88 pp.

Mutante:

- 3,40 daño/uso;
- daño total -1,33/pelea;
- presión HP -4,19 pp.

Es el mejor de la interpretación replacement, pero sigue siendo un downgrade,
especialmente para individuos ofensivamente altos.

**No seleccionar.**

### FRENZY_3X050

Normal:

- 2,14 daño/uso;
- daño total -1,35/pelea.

Mutante:

- 2,23 daño/uso;
- daño total -2,96/pelea.

El tercer packet aumenta exposición a DEF plana sin recuperar suficiente daño.

**Descartado.**

## Hallazgo

La interpretación:

```text
REPLACE BASIC WITH CANONICAL MULTI-HIT
```

es incompatible con dos contratos ya ratificados:

1. la variabilidad individual también afecta ofensiva;
2. T4 no debe convertirse en una mejora de tier que reduzca amenaza.

No se debe compensar esto elevando scalars sin entender el origen del problema.

## Siguiente hipótesis

Preservar el BASIC individual como packet de apertura y añadir follow-ups
frenéticos derivados del 2d4 canónico:

```text
BASIC individual
+
N × (2d4 canónico × scalar)
```

Esto mantiene:

- la identidad ofensiva individual;
- el vínculo de Mordisco Frenético con el 2d4 canónico;
- multi-hit;
- DEF/absorción por packet;
- T1–T3 intactos.

Siguiente fase: `A2_FOLLOWUP_GEOMETRY`.

T4 continúa sin selección canónica.
