# Resultado — LII T0 Progressive Recalibration vs Lobo V01

Fecha: 2026-10-06
Estado: **MECHANICALLY_VALID / HUMAN REVIEW COMPLETED**

Review ZIP SHA-256:
`7bedd18b472950c7ae27a82441d70cd923d0062b77b7ea9cefc6fd3e56611552`

## Integridad

- 368.640 combates representados.
- 24 brazos.
- jugador siempre LianQi II.
- 3 contextos de equipo:
  - CARRY_OVER_FLOOR = HIGH_ROLL_STRESS LI exacto;
  - EXPECTED_STAGE LII;
  - HIGH_ROLL_STRESS LII.
- 5 raíces.
- 4 policies.
- 256 peleas/contexto.
- T0 only.
- no T1–T4.
- no T5.
- 0 timeouts.
- manifest 7/7 verificado.

## Issue del verdict

El paquete reportó:

`S0_CONTROL_DID_NOT_EXPOSE_HP_GAP`

Esto es un **bug del audit harness**, no una falla mecánica.

La lógica de ranking permitía a los perfiles `CURRENT` devolver `hp_rule_pass=True` como controles,
mientras el audit esperaba que `S0_CURRENT` devolviera false para demostrar el gap.

Los datos de combate son válidos.

## Ancla

Lobo Espiritual T0 final LI.

### FLOOR

CARRY_OVER_FLOOR:
- player win ~60,5%
- HP pressure ~79,0%
- rounds ~8,13
- monster damage ~29,86

EXPECTED_STAGE:
- player win ~87,7%

HIGH_ROLL_STRESS:
- player win ~83,0%

## Sapo Ceniza

### S0_CURRENT

CARRY_OVER_FLOOR:
- player win ~61,3%
- delta vs Lobo: **+0,8 pp** para el jugador;
- HP pressure -1,9 pp;
- daño -0,72.

Conclusión:
el Sapo actual **no produce progresión clara de zona** frente al Lobo.

### S1_ZONE_HP

CARRY_OVER_FLOOR:
- player win ~50,4%
- delta vs Lobo: **-10,1 pp**;
- HP pressure +5,2 pp;
- daño +1,97.

EXPECTED_STAGE:
- delta win ~-14,8 pp.

HIGH_ROLL_STRESS:
- delta win ~-9,3 pp.

Conclusión:
S1 produce el salto moderado más cercano al criterio humano de
"un poco más de vida + mejores intervalos", sin el salto brusco de S2/S3/S4.

### S2 / S3 / S4

Todos producen un salto mucho más agresivo:
- S2: ~-37 a -46 pp de win según equipo;
- S3: ~-24 a -32 pp;
- S4: ~-33 a -41 pp.

Son válidos mecánicamente, pero excesivos como primer escalón LII bajo el criterio actual.

### S5_BURN_IDENTITY

Intermedio:
- ~-18 a -25 pp de win.
Mantiene identidad burn, pero sigue siendo un salto bastante mayor que S1.

## Escarabajo de Hierro

### E0_CURRENT

Ya supera claramente al Lobo:

CARRY_OVER_FLOOR:
- player win ~35,8%
- delta vs Lobo: **-24,7 pp**;
- HP pressure +12,6 pp;
- rounds +4,02;
- daño +4,77.

EXPECTED_STAGE:
- player win ~86,4% vs Lobo ~87,7%, pero con mayor presión y duración.

HIGH_ROLL_STRESS:
- player win ~69,8% vs Lobo ~83,0%.

Conclusión:
**no necesita buff basal adicional para justificar LII**.
Su identidad de tanque ya crea progresión mediante HP/duración.

### E1–E4

Añadir buffs extra reduce demasiado la tasa de victoria bajo carry-over:
- E1 ~14,9%
- E2 ~4,4%
- E3 ~6,0%
- E4 ~1,2%

No son necesarios para establecer el salto LI→LII.

## Corrección metodológica adicional

El indicador V01 `threat_votes` trataba "más rounds" como amenaza siempre positiva.

Eso es incorrecto cuando un candidato mata al jugador más rápido:
un combate más corto puede significar **mayor**, no menor, amenaza.

Por eso la selección humana no usa el ranking 2/4–3/4 como regla final.

Prioridad de lectura:
1. win-rate diagnóstica;
2. HP pressure;
3. daño;
4. rounds interpretados según identidad y resultado.

## Finalistas V02

### Sapo
`S1R_STAGE_CONTINUITY`

Floor propuesto:
- HP 55
- PREC 98
- EVA 11
- DEF 0
- TEN 6
- BASIC 1d2+5
- Nube de Hollín canónica.

Upper envelope:
- HP 61
- PREC 102
- EVA **33** — preserva máximo medido previo;
- DEF **3** — preserva máximo medido previo;
- TEN **19** — preserva máximo medido previo;
- offensive ladders previos preservados;
- burn canónico preservado.

Esto corrige un defecto de S1 V01: no se debe reducir un upper envelope ya medido sólo para construir el candidato.

### Escarabajo
`E0_CURRENT_RETAINED`

Se conserva:
- floor actual 75/90/14/2/24;
- upper actual 82/98/22/5/34;
- ladders ofensivos actuales.

No se agrega buff artificial.

## Próximo paso

Gate focal T0 LII:
- Lobo como ancla;
- S1R_STAGE_CONTINUITY;
- E0_CURRENT_RETAINED;
- floor + variación real;
- CARRY_OVER_FLOOR / EXPECTED_STAGE / HIGH_ROLL_STRESS;
- no adaptación;
- freeze humano posterior.
