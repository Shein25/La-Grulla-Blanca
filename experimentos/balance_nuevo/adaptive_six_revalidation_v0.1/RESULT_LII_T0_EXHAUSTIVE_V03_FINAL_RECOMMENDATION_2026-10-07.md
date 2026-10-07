# Review V03 — LII T0 Exhaustive Stats + Technique Variance

Fecha: 2026-10-07
Estado: MECHANICALLY_PASS / FINAL_RECOMMENDATION_AWAITING_HUMAN_RATIFICATION

## Integridad

- 929.280 combates.
- issues=[].
- 0 timeouts.
- manifest íntegro.
- 46 brazos normales:
  - 27 Sapo;
  - 18 Escarabajo;
  - 1 Lobo ancla.
- T0 only.
- no T1-T4.
- no T5.
- no nuevas familias mecánicas.

## Selección recomendada — Sapo Ceniza

### Floor
Se conserva:
- HP 55
- PREC 98
- EVA 11
- DEF 0
- TEN 6
- BASIC 1d2+5
- Nube de Hollín:
  - direct 1d2+4
  - burn 1d2+2 x3
  - cadence 3

### Upper envelope recomendado
`S_MEDIUM`:
- HP 60
- PREC 101
- EVA 24
- DEF 2
- TEN 14
- BASIC ladder:
  - 1d2+5
  - 1d3+5
  - 1d3+6

### Variación de habilidad recomendada
`A1_DIRECT_MILD`:
- Nube de Hollín direct:
  - 1d2+4
  - 1d2+5
- burn fijo:
  - 1d2+2 x3
- cadence fija:
  - 3

Razón:
- mantiene variación real de la técnica;
- no modifica ticks ni cadence;
- produce progresión consistente sobre Lobo sin usar el full measured envelope;
- el aporte aislado de la variación de habilidad es moderado (~-1,18 pp de win-rate medio respecto A0 con el mismo stat tier).

Comparación NORMAL vs Lobo NORMAL:
- carry-over: 19,61% vs 25,33% player-win
- expected LII: 40,14% vs 55,21%
- high-roll gear LII: 43,75% vs 51,00%

## Selección recomendada — Escarabajo de Hierro

### Floor
Se conserva:
- HP 75
- PREC 90
- EVA 14
- DEF 2
- TEN 24
- BASIC 1d2+3
- Carga de Caparazón:
  - direct 1d2+8
  - cadence 3

### Upper envelope recomendado
`E_NARROW`:
- HP 78
- PREC 94
- EVA 18
- DEF 3
- TEN 28
- BASIC ladder:
  - 1d2+3
  - 1d2+4

### Variación de habilidad recomendada
`B1_DIRECT_MILD`:
- Carga:
  - 1d2+8
  - 1d2+9
- cadence fija:
  - 3

Razón:
- el floor del Escarabajo ya es muy fuerte;
- E_MEDIUM y E_FULL elevan demasiado al individuo ordinario;
- B1 agrega variedad sin convertir la cadencia en un segundo multiplicador de amenaza;
- el efecto aislado de B1 es moderado dentro de E_NARROW (~-3,35 pp de win-rate medio frente B0).

Comparación NORMAL vs Lobo NORMAL:
- carry-over: 12,89% vs 25,33% player-win
- expected LII: 54,71% vs 55,21%
- high-roll gear LII: 41,95% vs 51,00%

## Variantes descartadas como default ordinario

### Sapo
- S_FULL_MEASURED: demasiado fuerte para población normal.
- A2_DIRECT_FULL: no necesario para el individuo ordinario.
- A3_BURN_DIE / A7_COMBINED_MILD: mayor presión de burn; además A3 y A7 son equivalentes en V03 por construcción.
- A4_BURN_FLAT: aumento de burn mayor de lo necesario.
- A5_EXTRA_TICK: válido mecánicamente, pero no necesario.
- A6_FAST_CADENCE / A8_DIRECT_FAST: cadence 2 añade otro multiplicador de presión innecesario para T0 normal.

### Escarabajo
- E_MEDIUM / E_FULL_MEASURED: demasiado fuertes para población ordinaria.
- B2_DIRECT_MEASURED: salto mayor del necesario.
- B3/B4/B5: cadence 2 o combinaciones aumentan demasiado la presión y no son necesarias para establecer LII.

## Nota sobre HIGH_VECTOR

Los HIGH_VECTOR son deliberadamente extremos y no representan el individuo ordinario.
Para las selecciones recomendadas:
- Sapo high es ~26,5 pp más difícil que su población normal en player-win medio.
- Escarabajo high es ~23,4 pp más difícil que su población normal.

Esto confirma separación clara entre población ordinaria y extremo de stress.

## Próximo paso

Si la selección humana es aprobada:
1. freeze T0 LII Sapo + Escarabajo;
2. actualizar authority/variance contract;
3. reabrir T1 de ambos;
4. después usar el monstruo T0 más fuerte de LII como ancla para LIII.
