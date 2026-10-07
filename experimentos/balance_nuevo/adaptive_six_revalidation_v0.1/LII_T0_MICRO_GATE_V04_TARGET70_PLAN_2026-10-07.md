# LII T0 Micro Gate V04 — ~70% HRS Target

Fecha: 2026-10-07
Estado: READY_FOR_COLAB / HUMAN TARGETED CONFIRMATION

## Decisión humana

Para dejar margen real a T1, el T0 ordinario de LianQi II se calibra con:

- referencia principal: `HIGH_ROLL_STRESS(LianQi_II)`;
- objetivo agregado de player win-rate: **67%–73%**;
- centro deseado: ~70%.

Este target es local a este cierre LII T0.
No se convierte en target universal para otras etapas/tier.

## Floors ya aceptados

### Sapo Ceniza
- HP55 / PRE98 / EVA11 / DEF0 / TEN6
- BASIC 1d2+5
- Nube de Hollín direct 1d2+4
- burn 1d2+2 ×3
- cadence 3

V03 floor HRS: ~73,5% player-win.

### Escarabajo de Hierro
- HP75 / PRE90 / EVA14 / DEF2 / TEN24
- BASIC 1d2+3
- Carga de Caparazón 1d2+8
- cadence 3

V03 floor HRS: ~69,7% player-win.

## Candidatos Sapo

Todos preservan burn/cadence.

- S0_FLOOR_FIXED
  - sin variación.

- S1_MICRO_Q95
  - HP 55→56
  - PRE 98→99
  - EVA 11→13
  - DEF 0→1
  - TEN 6→7
  - Nube direct 1d2+4; sube a 1d2+5 sólo si q_skill>=0.95

- S2_MICRO_Q90
  - mismo micro-envelope
  - direct sube a 1d2+5 si q_skill>=0.90

- S3_MICRO_Q85
  - mismo micro-envelope
  - direct sube a 1d2+5 si q_skill>=0.85

- S4_MICRO_STATS_ONLY
  - mismo micro-envelope
  - Nube direct siempre 1d2+4

## Candidatos Escarabajo

El floor ya está dentro de target. Se prueba únicamente variación muy rara de habilidad:

- E0_FLOOR_FIXED
  - sin variación.

- E1_CARGA_Q975
  - Carga 1d2+8; sube a 1d2+9 si q_skill>=0.975.

- E2_CARGA_Q95
  - Carga 1d2+8; sube a 1d2+9 si q_skill>=0.95.

- E3_CARGA_Q90
  - Carga 1d2+8; sube a 1d2+9 si q_skill>=0.90.

No se añade stat variance ordinaria al Escarabajo en V04.

## Ancla

Se incluye Lobo Espiritual LI frozen NORMAL como control de progresión.

## Matriz

NORMAL arms:
- Lobo frozen normal: 1
- Sapo: 5
- Escarabajo: 4
Total: 10 arms.

Por arm:
- 128 individuos
- 2 reps por individuo
- 3 gear contexts
- 5 roots
- 4 policies

Total NORMAL:
10 × 128 × 2 × 3 × 5 × 4 = **153.600 peleas**.

Se añaden floors deterministas:
- Lobo / Sapo / Escarabajo
- 128 reps/contexto
= **23.040 peleas**.

Total V04:
**176.640 combates**.

## Criterio principal de selección

En HIGH_ROLL_STRESS LII, agregado sobre roots/policies:

1. player win-rate dentro de **67–73%**;
2. preferir candidato más cercano a 70%;
3. si empatan, preferir:
   - menor complejidad;
   - menor alejamiento del floor;
   - habilidad variable antes que stat inflation;
   - identidad preservada.

## Controles

También reportar:
- CARRY_OVER_FLOOR;
- EXPECTED_STAGE;
- root/policy spread;
- HP pressure;
- daño;
- rounds;
- technique/basic uses.

No exigir 67–73% en cada root/policy individual.

## Hard guards

- no T1–T4;
- no T5;
- no Definitivas;
- no new mechanics;
- no main;
- no merge;
- no canonical write;
- G04 Tierra;
- exact schema;
- deep preflight;
- smoke todas las arms;
- ProcessPool sin lambdas;
- 0 timeout/NaN/Inf.

Si V04 confirma un candidato:
- freeze humano T0 LII;
- luego T1.
