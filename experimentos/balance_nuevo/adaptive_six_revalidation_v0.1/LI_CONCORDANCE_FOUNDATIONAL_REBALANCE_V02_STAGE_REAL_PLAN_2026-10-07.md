# LianQi I — Concordance Foundational Rebalance V02 · Stage Real

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: PLAN LAB / SUPERSEDE V01 / NO FREEZE / NO RUNTIME

## Autoridad humana incorporada

Ver:
`HUMAN_DECISION_TECHNIQUE_ACQUISITION_BY_LIANQI_STAGE_2026-10-07.md`

La V01 queda superada porque utilizaba las 15 técnicas como envolvente mecánica. La etapa real LI no dispone todavía de defensivas ni AOE.

## LianQi I real

Técnicas disponibles para este gate:

- `palma_ardiente` — Fuego — unitarget
- `destello_plata` — Metal — unitarget
- `latigazo_marea` — Agua — unitarget/control
- `golpe_montana` — Tierra — unitarget
- `lanza_nubes` — Viento — unitarget

Reglas:

- 0 técnicas defensivas;
- 0 técnicas AOE;
- 0 puntos de Tramo;
- 0 Tramo I/II/III;
- técnicas ajenas pueden existir por adquisición, sin convertirlas en raíz principal o injerto.

## Concordancias LI

Con una técnica unitarget por elemento:

```
5 × 4 = 20 pares dirigidos entre elementos distintos
```

Según el mapeo canónico BASE:

- 16 pares resuelven una Concordancia;
- 4 pares son controles negativos BASE NONE:
  - Metal → Fuego sobre Palma;
  - Agua → Metal sobre Destello;
  - Agua → Viento sobre Lanza;
  - Tierra → Viento sobre Lanza.

Los cuatro deben permanecer con:
- 0 resolución;
- 0 consumo por Concordancia;
- 0 fallback.

## Banda adaptativa

- T0/T1 = balance principal LI.
- T2 = stress transitorio.
- T3/T4 = excluidos de la calibración LI.

## Equipo

Conservar censo exhaustivo LI:
- 14 piezas;
- 6.144 loadouts legales;
- 4.864 firmas mecánicas.

## Comparación

Pareado Common Random Numbers:

- CONCORDANCE_OFF;
- CONCORDANCE_ON;

mismas técnicas, raíz principal, equipo, monstruo, tier y seed.

## Progresión posterior que este gate NO debe simular

### LII
- agrega defensivas;
- habilita Tramo I;
- +2 puntos.

### LIII
- agrega AOE;
- habilita Tramo II;
- 4 puntos acumulados.

### LIV
- habilita Tramo III;
- 6 puntos acumulados;
- builds maduras y equipo avanzado.

T3/T4 adaptativos deben revalidarse más adelante contra jugadores avanzados, incluyendo LIII/LIV y stress LIV con equipo EXPECTED/HIGH_ROLL_STRESS y Tramo III disponible.

## Resultado esperado

`LI_CONCORDANCE_FOUNDATIONAL_REBALANCE_V02_STAGE_REAL_REVIEW.zip`

No main. No merge. No runtime. No auto-freeze.
