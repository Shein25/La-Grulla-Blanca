# Review LII T1 V01 — methodological correction required

Fecha: 2026-10-07
Estado: MECHANICALLY_PASS / TARGET_GATE_INVALID_BY_POLICY_SUBSET / DO_NOT_FREEZE

## Integridad

- 99.840 combates.
- issues=[].
- 0 timeout.
- manifest íntegro.
- semántica T1 ejecutada correctamente:
  - HP <=30% OR heavy hit >=20% max HP;
  - survival action consume turno;
  - Sapo MITIGATE_NEXT;
  - Escarabajo DEFENSE_UP.

## Problema metodológico

V01 usó sólo:
- UNITARGET_FIRST
- DEFENSE_OPEN

Pero el cierre T0 V04 que fundamentó el objetivo ~70% usó cuatro policies:
- UNITARGET_FIRST
- AOE_FIRST
- DEFENSE_OPEN
- ROTATION

Por eso el T0 HRS medido en V01 quedó:
- Sapo ~99,14%;
- Escarabajo ~94,38%;

mientras que el agregado comparable de V04 era:
- Sapo ~73,34%;
- Escarabajo ~69,98%.

La discrepancia no es un cambio del T0; es un cambio del conjunto de policies.

## Lo que V01 sí demuestra

### Sapo
Incluso MITIGATE_NEXT 40% / CD5–6 fue más fácil que T0 en el subconjunto probado:
- 40% CD6: delta agregado +1,93 pp;
- 40% CD5: +2,45 pp.

El histórico 10% / CD5:
- delta agregado +3,78 pp.

Lectura:
la pérdida del turno del monstruo pesa más que una mitigación débil. V02 debe ampliar magnitud.

### Escarabajo
DEFENSE_UP fuerte sí compensa el turno perdido:
- +10 DEF / CD3: delta agregado -1,12 pp;
- +8 DEF / CD3: -0,65 pp.

Histórico +2 / CD5:
- delta +4,79 pp;
- demasiado débil bajo el T0 nuevo.

## Decisión

- NO freeze T1 desde V01.
- Repetir con las cuatro policies de T0 V04.
- Mantener tres gear contexts.
- Ampliar búsqueda:
  - Sapo MITIGATE_NEXT hasta 90%;
  - Escarabajo DEFENSE_UP hasta +20.
- conservar candidato histórico como control.
- comparar siempre contra T0 pareado con la misma matriz.

V01 queda como evidencia diagnóstica, no autoridad numérica.
