# Mutant / T1 Compatibility Gate v0.4 — resultado final

**Fecha:** 2026-10-06  
**Rama:** `experiment/li-monster-t0-final-t1-lab-v0.1`  
**Status:** `MUTANT_T1_COMPAT_PASS_READY_FOR_HUMAN_ACTIVATION`

## Autoridades

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- Variance: `monster-individual-variance-v0.4`

## Fidelidad previa

Antes del gate, el harness local reprodujo exactamente celdas de las autoridades previas para los cinco monstruos:

- Rata +70: `RATA_T1_PLUS70_FOCAL_V02`
- Serpiente / Avispa / Mono / Lobo: `T1_FINAL_EXHAUSTIVE_GATE_V02`

Coincidieron win-rate, rondas, HP, DoT/QI drain, procs y métricas defensivas relevantes.

## Cobertura

- 1.000.000 spawns totales, 200.000 por especie.
- 102.400 combates T1.
- 5 especies × 4 perfiles × 5 raíces × 2 policies × 4 arms × R128.
- Arms: BASE / NORMAL / MUTANT / UPPER.
- 0 timeouts.
- 0 NaN/Inf.
- Issues: ninguno.

Review SHA-256:

`c4e3c73f8ff907fa3b8e698bbc6ae991b9dfde1015a5eb2b439b154630b4bf34`

## Incidencia Mutante

| Especie | Incidencia |
|---|---:|
| Rata Qi | 0,7745% |
| Serpiente Qi | 0,7465% |
| Avispa Jade | 0,7395% |
| Mono Píldoras | 0,7245% |
| Lobo Espiritual | 0,7300% |

Todas permanecen por debajo del 1%, con floors y envelopes válidos.

## Combate agregado

| Especie | BASE | NORMAL | MUTANT | UPPER |
|---|---:|---:|---:|---:|
| Rata Qi | 72,01% | 45,88% | 22,42% | 18,81% |
| Serpiente Qi | 61,19% | 6,64% | 0,31% | 0,08% |
| Avispa Jade | 63,67% | 15,37% | 2,38% | 1,11% |
| Mono Píldoras | 43,22% | 2,87% | 0,00% | 0,00% |
| Lobo Espiritual | 40,51% | 7,21% | 0,08% | 0,02% |

La caída de win-rate Mutante/UPPER es esperada y no bloqueante por decisión humana. En ninguna especie el agregado MUTANT o UPPER fue más fácil que NORMAL. Tampoco aparecieron celdas con inversión >3 pp.

## Resultado

La capa de variabilidad v0.4 queda compatible con T0/T1 congelados y habilitada para **integración experimental**.

Esto no implica activación automática en runtime canónico ni merge a `main`.

## Nota de infraestructura

El ZIP V04 original tenía un bug en el validador de `candidate_id`: serializaba las magnitudes de Serpiente/Avispa como enteros, aunque sus IDs congelados pertenecen al esquema `FLOAT_MAGNITUDE_V04`. La ejecución local corrigió únicamente ese validador. No se alteraron candidatos, magnitudes, cooldowns, seeds ni comportamiento de combate.
