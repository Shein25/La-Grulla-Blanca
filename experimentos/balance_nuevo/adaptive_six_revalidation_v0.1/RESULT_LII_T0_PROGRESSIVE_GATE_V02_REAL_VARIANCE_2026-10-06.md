# Review — LII T0 Progressive Gate V02 Real Variance

Fecha: 2026-10-06
Estado: MECHANICALLY_PASS / VARIANCE_REQUIRES_ONE_MORE_REFINEMENT

Review ZIP SHA-256:
`4daa877fc6fea7456c2f83b1279237c3f0a83d6ba354e78dabb824d87d54e621`

## Integridad

- 138.240 combates.
- manifest 8/8 válido.
- issues=[].
- 0 timeouts.
- T0 only.
- no T1-T4.
- no suffix abilities.
- player siempre LianQi II.

## Conclusión de FLOOR

### Lobo LI
CARRY_OVER_FLOOR:
- player win 60.49%
- HP pressure 78.98%
- daño monstruo 29.83
- rounds 8.13

### Sapo S1R FLOOR
CARRY_OVER_FLOOR:
- player win 51.33%
- HP pressure 83.34%
- daño 31.50
- rounds 7.35

EXPECTED_STAGE:
- player win 73.36% vs Lobo 87.30%

HIGH_ROLL_STRESS:
- player win 73.03% vs Lobo 82.83%

Lectura:
el FLOOR del Sapo produce un salto moderado y correcto de zona.

### Escarabajo E0 FLOOR
CARRY_OVER_FLOOR:
- player win 35.61%
- HP pressure 91.83%
- daño 34.71
- rounds 12.20

EXPECTED_STAGE:
- player win 85.27% vs Lobo 87.30%

HIGH_ROLL_STRESS:
- player win 70.55% vs Lobo 82.83%

Lectura:
el FLOOR actual del Escarabajo ya cumple progresión LII y conserva identidad tanque.

## Problema detectado: NORMAL_POPULATION

La combinación de q independientes UNIFORM[0,1] con los upper envelopes actuales eleva demasiado al individuo ordinario.

CARRY_OVER_FLOOR:
- Lobo normal: player win 24.26%
- Sapo normal: 10.12%
- Escarabajo normal: 2.93%

EXPECTED_STAGE:
- Lobo normal: 53.52%
- Sapo normal: 22.56%
- Escarabajo normal: 18.07%

HIGH_ROLL_STRESS:
- Lobo normal: 49.06%
- Sapo normal: 27.42%
- Escarabajo normal: 14.24%

Esto no es falla mecánica, pero sí indica que los envelopes completos no deben congelarse todavía si la intención humana es un salto progresivo y no abrupto.

## Pool observado

Sapo normal medio:
- HP 58.31
- PREC 99.90
- EVA 21.53
- DEF 1.44
- TEN 12.41

Escarabajo normal medio:
- HP 78.62
- PREC 94.21
- EVA 17.87
- DEF 3.47
- TEN 28.81

La suma simultánea de supervivencia + ofensiva variable amplifica la amenaza más de lo deseado.

## Decisión recomendada

No tocar los floors seleccionados.

Mantener:
- Sapo floor: HP55 / PRE98 / EVA11 / DEF0 / TEN6.
- Escarabajo floor: HP75 / PRE90 / EVA14 / DEF2 / TEN24.

Reabrir únicamente los **upper envelopes / ladders de variación ordinaria** en un V03 focal.

Objetivo V03:
- mantener mejora sobre LI;
- preservar identidad;
- evitar que el individuo medio de LII se comporte como un high-roll excepcional;
- conservar HIGH_VECTOR como stress separado;
- no tocar T1-T4.

No freeze T0 LII completo hasta cerrar V03.
