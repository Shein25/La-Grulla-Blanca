# Plan — Mutant / T1 Compatibility Gate v0.4

**Fecha:** 2026-10-06  
**Estado:** READY_TO_RUN

## Autoridad

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- variance: `monster-individual-variance-v0.4`
- rama: `experiment/li-monster-t0-final-t1-lab-v0.1`

## Cobertura

Spawn-only:
- 200.000 instancias por especie
- 1.000.000 total

Combate:
- 5 especies
- 4 perfiles: NAKED / MANDATORY_ENTRY / EXPECTED_STAGE / HIGH_ROLL_STRESS
- 5 raíces
- 2 policies: UNITARGET_FIRST / DEFENSE_OPEN
- 4 arms:
  - BASE: T0 canónico + T1 congelado
  - NORMAL: variación natural condicionada a no-Mutante + T1
  - MUTANT: Mutante condicionado + T1
  - UPPER: extremo determinista de todos los techos + T1
- R128 por celda
- 102.400 combates representados

## Criterio humano

**No existe un piso de win-rate del jugador para Mutantes.**

La dificultad extrema es válida. No se reequilibra un Mutante simplemente porque la probabilidad de victoria sea muy baja.

## Hard failures

Sólo bloquean:
- stat/ataque por debajo de T0;
- stat por encima de envelope;
- identidad/cadencia/QI_DRAIN alterados;
- candidate ID T1 incorrecto;
- NaN/Inf;
- timeout/soft-lock;
- tier adaptativo concedido por mutación;
- mutación del registro canónico;
- incidencia Mutante >=1%.

Que MUTANT o UPPER sean mucho más difíciles que NORMAL es diagnóstico esperado y no bloqueo.

## Artefacto

`KAGGLE_LI_MUTANT_T1_COMPAT_GATE_V04.zip`

SHA-256 paquete: `8635cc1ebfce0354ec1193008d8f895f2ac5fc22bf507a15ac15f639e61433de`

Runner SHA-256: `c6b8f5e70722c0c35f300fa1cdaf1200599068eeb4c3bbacc706bd1ed25698ad`
