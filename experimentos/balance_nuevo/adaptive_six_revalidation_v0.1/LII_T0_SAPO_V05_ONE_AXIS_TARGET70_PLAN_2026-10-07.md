# LII T0 Sapo V05 — One-Axis Target70 Search

Fecha: 2026-10-07
Estado: READY_FOR_COLAB / SAPO-ONLY FINAL MICROSEARCH

## Contexto

V04 confirmó:
- Sapo floor HRS LII: 73,34% player-win;
- micro-envelope simultáneo de cinco stats: ~66%;
- por lo tanto el ajuste requerido es pequeño y debe aislarse por eje.

Escarabajo queda fuera de esta búsqueda:
- floor HRS = 69,98%;
- su cierre se hará luego con una variación de Carga leve si se desea.

## Objetivo

Encontrar la **mínima variación ordinaria** del Sapo que deje:
- HIGH_ROLL_STRESS LII agregado: 67–73%;
- centro deseado: ~70%;
- con espacio real para T1.

## Floor fijo

Sapo:
- HP55
- PRE98
- EVA11
- DEF0
- TEN6
- BASIC 1d2+5
- Nube direct 1d2+4
- burn 1d2+2 ×3
- cadence 3

## Screen HRS — candidatos

### Control
- S00_FLOOR_FIXED

### Variación sólo de Nube
- S01_SKILL_Q75: 1d2+5 si q>=.75
- S02_SKILL_Q50: 1d2+5 si q>=.50
- S03_SKILL_Q25: 1d2+5 si q>=.25
- S04_SKILL_Q10: 1d2+5 si q>=.10
- S05_SKILL_FIXED_HIGH: direct fijo 1d2+5 (control, no candidato final preferido)

### Un solo eje de stat
- S06_HP56
- S07_PRE99
- S08_EVA12
- S09_DEF1
- S10_TEN7

### Un eje + variación de Nube q>=.50
- S11_HP56_SKILL_Q50
- S12_PRE99_SKILL_Q50
- S13_EVA12_SKILL_Q50
- S14_DEF1_SKILL_Q50
- S15_TEN7_SKILL_Q50

### Pares mínimos de stats
- S16_HP56_PRE99
- S17_HP56_EVA12
- S18_HP56_DEF1
- S19_HP56_TEN7
- S20_EVA12_TEN7

Total screen: 21 arms.

## Población

- q independiente por cada eje variable;
- stat +1 se obtiene cuando interpolación round-half-up cruza q>=.5;
- Nube alta según threshold específico del arm;
- individuos que crucen Mutant threshold se excluyen de NORMAL;
- no suffix abilities.

## Fase A — screen HRS

21 arms
× 5 roots
× 4 policies
× 128 individuos
× 2 reps
= **107.520 peleas**.

Ranking:
1. dentro de 67–73%;
2. menor distancia a 70%;
3. excluir S00 y S05 de la selección automática salvo que ningún candidato variable pase;
4. preferir menor número de ejes variables.

Se seleccionan TOP 6.

## Fase B — confirmación

TOP 6 variables:
- CARRY_OVER_FLOOR
- EXPECTED_STAGE
- HIGH_ROLL_STRESS
- 5 roots
- 4 policies
- 256 fights/context

= **92.160 peleas**.

Controles:
- Sapo floor
- Lobo frozen normal
en 3 gears × 5 roots × 4 policies ×128
= **15.360 peleas**.

Total previsto:
**215.040 peleas**.

## Métricas

- player win-rate;
- HP pressure;
- rounds;
- monster direct/DOT/total damage;
- hit-rate;
- technique/basic uses;
- skill proc-rate;
- root/policy spread;
- distancia al 70%.

## Hard guards

- T0 only;
- no T1–T4;
- no T5;
- no new mechanics;
- burn/ticks/cadence fijos;
- no main / merge / canonical write;
- G04 Tierra;
- exact schema;
- deep preflight;
- smoke arms;
- multiprocessing sin lambdas;
- 0 timeout/NaN/Inf.

## Resultado esperado

`LII_T0_SAPO_V05_ONE_AXIS_TARGET70_REVIEW.zip`

Si V05 identifica candidato estable:
- congelar Sapo T0;
- cerrar Escarabajo T0;
- luego abrir T1.
