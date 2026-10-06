# LI — T4 final freeze

**Fecha:** 2026-10-06  
**Estado:** `T4_LI_FINAL_FREEZE_2026-10-06`

## Autoridad

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- T2: `T2_LI_FINAL_FREEZE_2026-10-06`
- T3: `T3_LI_FINAL_FREEZE_2026-10-06`
- T4: `T4_LI_FINAL_CONTRACT_V1.json`
- Variabilidad: `monster-individual-variance-v0.4`
- Mutantes/sufijos: `MUTANT_SUFFIX_CONTRACT_V1`
- Gate final: `LI_MONSTER_T4_FINAL_DUAL_STAGE_GATE_V03`
- Review SHA-256: `b5ca5163b3c099820c7d85b1ba039994956b4e30e5650aaf0d3e697a87b88eee`
- 294.400 combates.
- manifest 7/7.
- `issues=[]`.

## T4 congelado

### Rata Qi
`Mordisco Frenético`

`INSTANCE_BASIC ×1.0 + 2d4 canónico ×0.50`

- precisión independiente por packet;
- crítico independiente por packet;
- CD7.

### Serpiente Qi
`S4A_BASIC_POISON_ON_OPEN_HIT`

- BASIC de instancia;
- si impacta: un tick inmediato del veneno de la instancia;
- no añade duración;
- CD7.

### Avispa Jade
`A4A_BASIC_POISON_ON_OPEN_HIT`

- BASIC de instancia;
- si impacta: un tick inmediato del veneno de la instancia;
- no añade duración;
- CD7.

### Mono Píldoras
`M4B_MANOTAZO_REPLACE`

- packet directo de Manotazo de instancia;
- si impacta: Qi drain 6;
- no consume la cadencia del Manotazo canónico;
- CD7.

### Lobo Espiritual
`L4A_EMBOSCADA_REPLACE`

- packet directo de Emboscada de instancia;
- no consume la cadencia de Emboscada canónica;
- CD7.

## Orden de prioridad

```text
T1 survival
→ técnica canónica due
→ T4 si lista
→ BASIC
```

T4 sólo reemplaza BASIC.

## Guardias

- T0–T3 no se reabren.
- no universal stat scaling.
- no root/build inspection.
- no future RNG.
- no Definitivas.
- Acechante +20 PREC sólo siguiente ataque.
- T3 counter sigue requiriendo causalidad real.
- no T5.

## Estado

T4 queda cerrado para las cinco especies LI.

La cadena adaptativa completa queda:
`T0 NATURAL → T1 SUPERVIVENCIA → T2 RECONOCIMIENTO → T3 CONTRAADAPTACIÓN → T4 ADAPTACIÓN MADURA`.

No agregar T5 sin reapertura humana explícita.
