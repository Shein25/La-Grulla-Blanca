# LII T3 Equipment-Space Gate V02

Fecha: 2026-10-07
Estado: DESIGN_READY / LAB ONLY
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`

## Motivo

V01 usaba tres loadouts canónicos como contextos de equipo. Eso es suficiente para un gate focal, pero no para llamar a la prueba "exhaustiva" respecto del equipo disponible en LianQi II.

El catálogo autorizado contiene 35 piezas utilizables hasta LianQi II:
- 14 LianQi I;
- 21 LianQi II.

Para los slots completos ARMA, TOCADO, VESTIDURA, BRAZALES, FAJIN, PIERNAS, CALZADO, AMULETO, PULSERA y dos ANILLOS existen 349.920 combinaciones completas legales.

## Estrategia

### Fase A — censo exhaustivo de equipo

Enumerar las 349.920 combinaciones completas legales LII.

Para cada combinación:
- sumar el vector mecánico de stats;
- registrar equivalencias;
- calcular mínimos/máximos;
- conservar un representante por vector;
- producir `EQUIPMENT_SPACE_CENSUS.json`.

La autoridad de catálogo actual no introduce efectos especiales en las piezas disponibles hasta LII; el vector considerado incluye:
- basic_attack_flat;
- control;
- defense;
- evasion;
- hp_max;
- percent_penetration_pp;
- precision;
- qi_max;
- technique_direct_damage_percent;
- tenacity.

### Fase B — cohort mecánico

Seleccionar determinísticamente 64 contextos de equipo:
- los tres loadouts canónicos:
  - CARRY_OVER_FLOOR;
  - EXPECTED_STAGE;
  - HIGH_ROLL_STRESS;
- extremos por cada eje mecánico;
- puntos de soporte multidimensionales;
- relleno por máxima distancia normalizada para cubrir huecos del espacio.

La selección se deriva exclusivamente del catálogo y queda serializada en el REVIEW.

No se pretende simular literalmente las 349.920 combinaciones × toda la matriz adaptativa, porque eso produciría miles de millones de combates. La exhaustividad corresponde al censo del espacio; la simulación usa un cohort determinista de cobertura mecánica.

## Matriz de combate V02

- 2 especies;
- 64 gear contexts;
- 5 roots;
- 4 policies;
- 2 arms:
  - T2_FROZEN;
  - T3_CAUSAL_COUNTER;
- R256;
- CRN pareado.

Total previsto:
**1.310.720 combates**.

## Autoridad T0–T3

Igual a `LII_T3_CAUSAL_COUNTER_GATE_V01_PLAN_2026-10-07.md`.

T3:
- Sapo: counter `INSTANCE_T0_BASIC 1d2+5` sólo tras predicción T2 confirmada y MITIGATE_NEXT causal;
- Escarabajo: counter `INSTANCE_T0_BASIC 1d2+3` sólo tras predicción T2 confirmada y DEFENSE_UP +4 causal.

No cambia T0/T1/T2.
No T4.
No T5.
No main.
No merge.

## Salidas obligatorias

- `EQUIPMENT_SPACE_CENSUS.json`
- `LII_T3_EQUIPMENT_SPACE_COHORT_V02.csv`
- `RUN_MANIFEST.json`
- fight-level comprimido
- contexts
- paired T2/T3
- aggregate species × gear
- root spread tras promediar policies
- verdict
- runner usado
- SOURCE_LOCK
- PACKAGE_MANIFEST

Resultado esperado:
`LII_T3_EQUIPMENT_SPACE_GATE_V02_REVIEW.zip`

No freeze automático.
