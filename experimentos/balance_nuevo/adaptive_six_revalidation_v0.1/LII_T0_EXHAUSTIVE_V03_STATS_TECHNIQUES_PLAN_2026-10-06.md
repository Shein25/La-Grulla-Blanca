# LII T0 Exhaustive V03 — Stats + Technique Variance

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / T0 ONLY / EXHAUSTIVE

## Objetivo

Cerrar los upper envelopes de variación ordinaria de:
- Sapo Ceniza;
- Escarabajo de Hierro;

sin tocar sus floors ya seleccionados y explorando también variación T0 de sus técnicas.

No se ejecuta T1–T4.
No se introducen familias mecánicas nuevas.

## Floors congelados para este screen

### Sapo
- HP 55
- PREC 98
- EVA 11
- DEF 0
- TEN 6
- BASIC 1d2+5
- Nube de Hollín:
  - cadence 3
  - direct 1d2+4
  - burn 1d2+2 ×3

### Escarabajo
- HP 75
- PREC 90
- EVA 14
- DEF 2
- TEN 24
- BASIC 1d2+3
- Carga de Caparazón:
  - cadence 3
  - direct 1d2+8

## Ancla

Lobo Espiritual T0 final LI con su variación congelada.

## Stat-envelope tiers

### Sapo

S_NARROW:
- HP 58
- PREC 100
- EVA 18
- DEF 1
- TEN 10
- BASIC upper 1d3+5

S_MEDIUM:
- HP 60
- PREC 101
- EVA 24
- DEF 2
- TEN 14
- BASIC upper 1d3+6

S_FULL_MEASURED:
- HP 61
- PREC 102
- EVA 33
- DEF 3
- TEN 19
- BASIC upper 1d2+7

### Escarabajo

E_NARROW:
- HP 78
- PREC 94
- EVA 18
- DEF 3
- TEN 28
- BASIC upper 1d2+4

E_MEDIUM:
- HP 80
- PREC 96
- EVA 20
- DEF 4
- TEN 31
- BASIC upper 1d2+4

E_FULL_MEASURED:
- HP 82
- PREC 98
- EVA 22
- DEF 5
- TEN 34
- BASIC upper 1d2+6

## Variaciones de habilidad — Sapo

Todas son LAB-only. No constituyen autoridad numérica hasta revisión humana.

1. A0_FIXED
   - direct fijo 1d2+4
   - burn fijo 1d2+2 ×3
   - cadence 3

2. A1_DIRECT_MILD
   - direct ladder 1d2+4 → 1d2+5
   - burn fijo
   - cadence 3

3. A2_DIRECT_FULL
   - direct ladder 1d2+4 → 1d2+5 → 1d2+8
   - burn fijo
   - cadence 3

4. A3_BURN_DIE
   - direct mild
   - burn damage ladder 1d2+2 → 1d3+2
   - ticks 3
   - cadence 3

5. A4_BURN_FLAT
   - direct mild
   - burn damage ladder 1d2+2 → 1d2+3
   - ticks 3
   - cadence 3

6. A5_EXTRA_TICK
   - direct fijo
   - burn 1d2+2
   - ticks 3; q alto puede promover a 4
   - cadence 3

7. A6_FAST_CADENCE
   - direct fijo
   - burn fijo
   - cadence 3; q alto puede promover a 2

8. A7_COMBINED_MILD
   - direct mild
   - burn die mild
   - ticks 3
   - cadence 3

9. A8_DIRECT_FAST
   - direct mild
   - burn fijo
   - cadence 3; q alto puede promover a 2

Para cadence/ticks discretos, la mejora excepcional del eje sólo se activa con q >= 0.85.
Ese q sigue participando del score Mutante.

## Variaciones de habilidad — Escarabajo

1. B0_FIXED
   - Carga 1d2+8
   - cadence 3

2. B1_DIRECT_MILD
   - Carga ladder 1d2+8 → 1d2+9
   - cadence 3

3. B2_DIRECT_MEASURED
   - Carga ladder 1d2+8 → 1d4+9
   - cadence 3

4. B3_FAST_CADENCE
   - Carga fija 1d2+8
   - cadence 3; q alto puede promover a 2

5. B4_DIRECT_MILD_FAST
   - direct mild
   - cadence variable

6. B5_DIRECT_FULL_FAST
   - direct measured
   - cadence variable

## Combinatoria exhaustiva

Sapo:
- 3 stat tiers × 9 ability variants = 27 arms.

Escarabajo:
- 3 stat tiers × 6 ability variants = 18 arms.

Más:
- 1 Lobo anchor real-variance arm.

Total de brazos NORMAL_POPULATION: 46.

## Población y q

- q independiente UNIFORM[0,1] por eje variable;
- stat axes interpolan floor→upper con round-half-up;
- ladders ofensivas seleccionan entrada por q;
- cadence/ticks excepcionales usan threshold q>=0.85;
- Mutante se detecta con el threshold congelado por cantidad de ejes variables;
- NORMAL_POPULATION rechaza threshold-crossers;
- no suffix abilities en V03.

## Matriz heavy

### NORMAL_POPULATION
- 128 individuos no-mutantes por arm;
- 2 reps por individuo;
- 3 gear contexts;
- 5 roots;
- 4 policies.

46 × 60 × 256 = 706.560 peleas.

### HIGH_VECTOR
- cada arm en vector upper;
- 64 reps/contexto.

46 × 60 × 64 = 176.640 peleas.

### FLOOR
Sólo:
- Lobo;
- Sapo;
- Escarabajo.

3 × 60 × 256 = 46.080 peleas.

### Total
**929.280 combates**.

## Equipo

Jugador siempre LianQi II.

1. CARRY_OVER_FLOOR = HIGH_ROLL_STRESS LI exacto.
2. EXPECTED_STAGE = EXPECTED_STAGE LII.
3. HIGH_ROLL_STRESS = HIGH_ROLL_STRESS LII.

## Métricas

Por arm / profile class / gear / root / policy:
- player win-rate;
- HP pressure;
- HP final;
- Qi final/spent;
- rounds;
- monster direct damage;
- monster DOT;
- monster total damage;
- hit-rate;
- technique uses;
- basic uses;
- technique direct contribution;
- DOT contribution;
- cadence realized;
- burn ticks realized;
- root/policy spread.

## Comparaciones

Cada arm se compara con:
1. Lobo del mismo profile class y contexto;
2. floor de su propia especie;
3. arm A0/B0 del mismo stat tier;
4. misma ability variant en tier inferior.

Esto permite separar:
- cuánto agrega el stat envelope;
- cuánto agrega la habilidad;
- cuánto agrega la combinación.

## Interpretación

No target universal de win-rate.

Rounds es descriptivo, no amenaza monotónica.

La selección debe favorecer:
- progresión real sobre Lobo;
- aumento moderado en población normal;
- high vector claramente excepcional;
- identidad de especie;
- ausencia de saturación o comportamiento tipo mini-jefe en promedio;
- habilidad variable que no eclipse completamente a los stats.

## Hard guards

- no main;
- no merge;
- no canonical write;
- no T1–T4;
- no T5;
- no Definitivas;
- no nuevas familias mecánicas;
- floors intactos;
- exact guard schema;
- G04 Tierra correcto;
- no `lambda` en ProcessPoolExecutor;
- deep profile preflight;
- smoke de todas las familias antes del heavy;
- checkpoints;
- 0 timeout/NaN/Inf requerido para pass mecánico.

## Resultado esperado

`LII_T0_EXHAUSTIVE_V03_STATS_TECHNIQUES_REVIEW.zip`

El review debe permitir elegir:
- upper envelope final del Sapo;
- variación permitida de Nube de Hollín;
- upper envelope final del Escarabajo;
- variación permitida de Carga de Caparazón.

Luego:
- freeze humano T0 LII;
- recién después reabrir T1.
