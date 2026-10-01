# Rata T4 — Mordisco Frenético — Phase A2 follow-up review

Fecha: 2026-10-01

## Modelo

Se abandonó el reemplazo completo por packets canónicos porque reducía la
amenaza de individuos cuyo BASIC ya estaba por encima de 2d4.

A2 usa:

```text
BASIC individual
+
follow-up(s) derivados del 2d4 canónico
```

Fijos:

- precisión independiente por packet;
- crítico independiente por packet;
- CD5;
- DEF plana y absorción por packet;
- T1–T3 congelados.

## Estudio dirigido

30.000 combates VETERAN.

Baseline T3:

```text
normal:
damage 6,768
HP jugador 78,63%

Mutante:
damage 10,157
HP jugador 67,92%
```

### FOLLOWUP_1X025

Normal:

- daño total -0,046/pelea vs baseline;
- presión HP -0,14 pp.

Mutante:

- daño total +0,085;
- presión HP +0,28 pp.

Demasiado pequeño; rounding + DEF absorben casi toda la identidad T4.

### FOLLOWUP_2X025

Misma expectativa bruta extra que 1×0,50, pero dos packets pequeños.

Normal:

- daño total -0,052;
- presión HP -0,15 pp.

Mutante:

- daño total +0,230;
- presión HP +0,71 pp.

La DEF plana por hit elimina demasiado del follow-up.

**Descartado.**

### FOLLOWUP_1X050

Normal:

- ~0,971 usos/pelea;
- ~4,40 daño total por uso de Mordisco incluyendo apertura;
- +0,653 daño monstruo/pelea;
- +2,07 pp presión HP;
- win jugador -0,06 pp.

Mutante:

- ~1,051 usos/pelea;
- ~5,22 daño/uso;
- +0,890 daño/pelea;
- +2,83 pp presión HP;
- win jugador -0,60 pp.

Es perceptible sin dominar T1–T3.

### FOLLOWUP_1X075

Normal:

- +1,571 daño/pelea;
- +4,97 pp presión HP.

Mutante:

- +1,916 daño/pelea;
- +6,07 pp presión HP.

Funciona, pero es una subida mucho más agresiva antes de haber calibrado
precision/critical/cooldown.

## Candidato provisional para Phase B

```text
opening:
INSTANCE_BASIC ×1.0

follow-up:
1 × (2d4 canónico ×0.50)

cooldown:
5

activation:
replace BASIC when ready
```

No es todavía T4 seleccionado.

## Siguiente fase

Phase B congela geometría 1×0,50 y compara:

- precisión independiente vs follow-up condicionado al hit de apertura;
- crítico independiente vs crítico sólo en apertura.

Después se calibrará cooldown.

T4 sigue experimental.
