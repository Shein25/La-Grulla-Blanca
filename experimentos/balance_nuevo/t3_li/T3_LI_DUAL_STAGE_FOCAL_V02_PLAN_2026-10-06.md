# LI — T3 focal dual-stage V02

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Fuente

Deriva de:
- T3 species-counter micro-screen V01;
- T0/T1/T2 congelados;
- variabilidad + Mutantes/sufijos congelados.

## Objetivo

Resolver únicamente los finalistas T3 antes del gate final.

## Contextos de etapa

1. `LI_OVERREACH`
   - player stage = LianQi_I;
   - representa sobreextensión extrema permitida por la política adaptativa.

2. `LIV_STRUCTURAL`
   - player stage = LianQi_IV;
   - usa equipo EXPECTED_STAGE/HIGH_ROLL_STRESS propio de LIV;
   - mantiene las técnicas base sin especializaciones para aislar etapa/equipo;
   - NO pretende reemplazar el futuro cruce con técnicas finales del otro frente.

## Finalistas

### Rata
- T2_FROZEN
- R1_INSTANCE_BASIC
- R1_INSTANCE_BASIC_ONCE
  - mismo packet INSTANCE_BASIC;
  - máximo 1 counter T3 por pelea.

### Serpiente
- T2_FROZEN
- S1_INSTANCE_POISON_TICK

### Avispa
- T2_FROZEN
- A2_INSTANCE_POISON_TICK

### Mono
- T2_FROZEN
- M2_INSTANCE_MANOTAZO_PACKET

### Lobo
- T2_FROZEN
- L1_INSTANCE_BASIC
- L2_INSTANCE_EMBOSCADA_DAMAGE

## Matriz

- 2 etapas;
- 5 especies;
- EXPECTED_STAGE + HIGH_ROLL_STRESS;
- 5 raíces;
- 4 policies;
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO;
- pools 64/16/8/4;
- 2 réplicas;
- CRN pareado.

Total previsto: **176.640 combates**.

## Métricas clave

- activaciones T3;
- false counter;
- counter packet mean/p90;
- direct/DOT/Qi decomposition;
- multi-counter;
- max counters;
- delta vs T2 por stage/policy/población;
- win-rate sólo diagnóstico;
- presión HP/Qi;
- duración;
- loops/timeouts/NaN.

## Criterios

- Serpiente/Avispa/Mono: confirmar estabilidad cross-stage.
- Rata: decidir si ONCE_PER_FIGHT es necesario con el T1/T2 final.
- Lobo: elegir el packet más coherente y estable entre básico y Emboscada.

No ratificación automática.
No T4.
No main.
No merge.

## UI

Google Colab:
- panel único con display_id;
- 0 tqdm;
- 0 rutas Kaggle;
- checkpoints por especie y etapa;
- workers automáticos.


## Paquete Colab preparado

Artefacto:
`COLAB_LI_MONSTER_T3_DUAL_STAGE_FOCAL_V02.zip`

- ZIP SHA-256: `0b8acb190bd1dce8c9778d5d84bec5bfd6db594ef06f8cdbcbecaa38f7f72aa8`
- Notebook SHA-256: `1d9d7438e138565cc2473de305a3e909ec632f5e3bca54f17660e4a0f21a40a1`
- Runner SHA-256: `a956a33ef7bd6105469b11062e8c06ccd619d4ef99add27e167f85cc3c405a6b`
- combates previstos: 176.640;
- panel único;
- 0 imports tqdm;
- 0 rutas Kaggle;
- notebook nbformat 4 válido;
- runner compila.
