# LI — T3 final freeze

**Fecha:** 2026-10-06  
**Estado:** `T3_LI_FINAL_FREEZE_2026-10-06`

## Autoridad

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- T2: `T2_LI_FINAL_FREEZE_2026-10-06`
- T3: `T3_LI_FINAL_CONTRACT_V1.json`
- Variabilidad: `monster-individual-variance-v0.4`
- Mutantes/sufijos: `MUTANT_SUFFIX_CONTRACT_V1`
- Gate final: `LI_MONSTER_T3_FINAL_DUAL_STAGE_GATE_V03`
- Review SHA-256: `ba9c8ef20c5155af0064f337b7eda7ff6cafcc79da8900e303a432849a0461d2`
- 294.400 combates.
- manifest 7/7.
- `issues=[]`.

## Trigger común congelado

T3 sólo responde a un patrón realmente aprendido y confirmado:

1. T2 reconoce una categoría repetida;
2. la siguiente acción real coincide con esa predicción;
3. T1 estaba activo;
4. T1 cambia causalmente el resultado defensivo.

Para EVADE:
- mismo roll habría acertado contra EVA natural;
- bono T1 lo convierte en miss.

Para DEFENSE_UP:
- mismo packet conecta;
- +DEF T1 previene >0 daño.

Un miss natural nunca activa T3.

## Counters congelados

- Rata Qi: `R1_INSTANCE_BASIC`.
- Serpiente Qi: `S1_INSTANCE_POISON_TICK`.
- Avispa Jade: `A2_INSTANCE_POISON_TICK`.
- Mono Píldoras: `M2_INSTANCE_MANOTAZO_PACKET`.
- Lobo Espiritual: `L2_INSTANCE_EMBOSCADA_DAMAGE`.

No existe límite artificial ONCE_PER_FIGHT para Rata.

## Frontera

T3 queda cerrado para las cinco especies LI.

Siguiente frente permitido: **T4 / ADAPTACIÓN MADURA**.

T4 no puede recalibrar T0–T3.

No main. No merge. No runtime canónico automático.
