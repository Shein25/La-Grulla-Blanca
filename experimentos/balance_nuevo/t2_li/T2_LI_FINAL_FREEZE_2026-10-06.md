# LI — T2 final freeze

**Fecha:** 2026-10-06  
**Estado:** `T2_LI_FINAL_FREEZE_2026-10-06`

## Autoridad

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- Variabilidad: `monster-individual-variance-v0.4`
- Mutantes/sufijos: `MUTANT_SUFFIX_CONTRACT_V1`
- T2: `T2_LI_FINAL_CONTRACT_V1.json`
- Gate: `LI_MONSTER_T2_FINAL_ALL_FIVE_GATE_V03`
- Review SHA-256: `d140b9e3fafe744df2b512df3ba15bf80184deea1d97eb54fa92161ae2ab0e72`
- Combates representados: **147.200**
- `issues=[]`
- manifest 7/7 verificado.

## T2 congelado

`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

Semántica:

1. memoria de 2 acciones;
2. requiere 2 acciones **EFECTIVA** consecutivas de la misma categoría observable;
3. categorías observables:
   - PLAYER_BASIC;
   - PLAYER_UNITARGET_TECHNIQUE;
   - PLAYER_AOE_TECHNIQUE;
   - PLAYER_DEFENSIVE_TECHNIQUE;
4. reconocimiento puede anticipar la supervivencia T1 si:
   - HP del monstruo <=40%; **o**
   - golpe actual recibido >=15% de HP máximo;
5. una anticipación por reconocimiento **no reemplaza una técnica canónica due por cadencia**;
6. los triggers naturales T1 HP<=30% / golpe>=20% conservan prioridad;
7. magnitud, cooldown y cargas de T1 permanecen exactamente congelados por especie.

## Lectura del gate

NATURAL agregado, T2 vs T1:
- Rata: -0,84 pp win jugador; +0,122 rondas; +0,364 anticipaciones/pelea.
- Serpiente: -1,19 pp; -0,013 rondas; +0,175 anticipaciones/pelea; DOT preservado/aumentado.
- Avispa: -1,03 pp; +0,012 rondas; +0,128 anticipaciones/pelea; DOT preservado/aumentado.
- Mono: -0,27 pp; +0,113 rondas; +0,185 anticipaciones/pelea; QI_DRAIN preservado.
- Lobo: -0,31 pp; +0,216 rondas; +0,313 anticipaciones/pelea.

No se usa win-rate como target universal; estos valores son diagnóstico de no-regresión e identidad.

## Resultado

T2 queda **cerrado y congelado** para las cinco especies LI.

Siguiente estado permitido:
- abrir T3 como laboratorio secuencial;
- T2 no se recalibra desde T3;
- no tocar T0/T1/Mutantes/sufijos;
- no activar runtime canónico automáticamente.

No main. No merge.
