# T0 LI — Auditoría final exhaustiva
Fecha: 2026-10-06

## Veredicto

`T0_LI_EXHAUSTIVE_PASS_READY_TO_FREEZE`

La validación exhaustiva confirma una curva T0 coherente usando una única ficha por especie para las cinco raíces. No se justifica balance por raíz.

## Evidencia

- REVIEW SHA-256: `77337e8ee77dfcd53ca1e679998d158cf5d2f8de8b6f744fc5e4c426bb3bf542`
- Manifest: 13/13 PASS.
- 4.864 firmas mecánicas / 6.144 loadouts crudos.
- 5 raíces × 2 policies.
- 6 candidatos (dos alternativas de Mono).
- R12 exhaustivo: 291.840 celdas = 3.502.080 peleas.
- R128 perfiles: 240 celdas = 30.720 peleas.
- R128 worst-tail: 300 celdas = 38.400 peleas.
- Total representado: 3.571.200 peleas.
- Timeouts máximos: 0.

## Selección final propuesta

| Monstruo | Candidate | EXPECTED R128 | NAKED | MANDATORY | HIGH | R12 universo signature mean |
|---|---|---:|---:|---:|---:|---:|
| Rata Qi | `59c6253e797f0c92` | 83,67% | 62,66% | 81,72% | 82,89% | 77,76% |
| Serpiente Qi | `9672faaa29074ab3` | 76,48% | 59,45% | 72,03% | 74,14% | 74,62% |
| Avispa Jade | `320443d1333c58a3` | 75,55% | 55,86% | 74,06% | 71,64% | 73,41% |
| Mono Píldoras | `36667a2ea37561ed` | 67,97% | 23,20% | 66,88% | 72,03% | 56,27% |
| Lobo Espiritual | `3ac540847aca982a` | 60,86% | 27,89% | 56,95% | 57,66% | 51,76% |

La jerarquía pasa: Rata > Serpiente ≈ Avispa > Mono > Lobo.

## Stats/patch final propuesto

### Rata Qi
- HP 45
- Precision 84
- DEF 2
- basic damage: baseline `2d4` + 3 → `2d4+3`

### Serpiente Qi
- HP 57
- Precision 94
- EVA 11
- DEF 0
- veneno sin aumento: cadence 2; `1d2+2` × 3 ticks.

### Avispa Jade
- HP 42
- Precision 102
- EVA 22
- DEF 2
- veneno sin aumento: cadence 2; `1d3+2` × 2 ticks.

### Mono de las Píldoras
Seleccionado `36667a2ea37561ed` frente al auto-winner.
- HP 59
- Precision 91
- EVA 28
- DEF 2
- basic/direct damage sin aumento
- cadence 2
- Qi drain 6

Motivo: EXPECTED 67,97%, más cercano al centro ~70%, preserva mejor la jerarquía y refuerza la identidad de drenaje. El auto-winner queda 73,20% EXPECTED y 60,53% raw-weighted R12 frente a 55,32% del alternativo.

### Lobo Espiritual
- HP 53
- Precision 100
- EVA 12
- DEF 1
- basic `2d4+2` sin aumento
- Emboscada `2d6+1` sin aumento
- cadence 5 → 4

## Progresión de equipo

El patrón útil queda:
- NAKED: normales ~56–63%; Mono/Lobo ~23–28%.
- MANDATORY: Rata 81,7%; Serpiente/Avispa ~72–74%; Mono 66,9%; Lobo 57,0%.
- EXPECTED: 83,7 / 76,5 / 75,5 / 68,0 / 60,9%.

`HIGH_ROLL_STRESS` no se interpreta como una banda obligatoriamente superior: sus extras LI no aportan un salto uniforme de poder de combate. Las pequeñas regresiones de Serpiente/Avispa/Lobo no bloquean el cierre.

## Matchups por raíz

El balance permanece general. No se crearán stats por raíz.

Asimetría conocida: Lobo vs Viento EXPECTED = 41,02% promedio de policies (DEFENSE_OPEN 50,78%; UNITARGET_FIRST 31,25%). Se conserva como matchup exigente del APEX_BRIDGE y se vigilará en T1/T2; no justifica buff de Viento ni nerf por raíz.

## Autoridad adaptativa

- LI ceiling T1.
- LII ceiling T2.
- LIII ceiling T2.
- LIV puede desarrollar T3 y T4 mediante nueva presión.
- T3 debe ser difícil pero sostenible para un LIV competente, porque necesita permitir el tránsito de presión 70→90.
- Si una población alcanza T3 pero no T4, el decay puede devolverla a T2.
- Una población que alcanzó T4 consolida T3 como piso histórico.
- T4 es el pico adaptativo y puede ser mucho más duro; puede decaer a T3.

Thresholds provisionales se mantienen: T1 20, T2 45, T3 70, T4 90.

## Gate

Los cinco T0 están listos para congelarse como nueva autoridad numérica, sujeto sólo a la decisión humana de aplicar el patch al registry. T1–T4 siguen sin magnitudes numéricas canon y deben recalibrarse secuencialmente sobre estos T0.
