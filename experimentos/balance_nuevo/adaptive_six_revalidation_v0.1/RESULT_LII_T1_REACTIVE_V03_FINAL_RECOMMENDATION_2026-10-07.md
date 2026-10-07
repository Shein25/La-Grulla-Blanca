# Review LII T1 Reactive V03 — final recommendation

Fecha: 2026-10-07
Estado: MECHANICALLY_PASS / FINAL_RECOMMENDATION_AWAITING_HUMAN_FREEZE

ZIP SHA-256:
`cbf0c0e4994ed9a6cbe7a58a84981e73ae4f578d0ff073e5afd998b6c45c4867`

## Integridad

- 186.880 combates.
- issues=[].
- 0 timeouts.
- manifest 9/9 íntegro.
- 4 policies.
- 3 gear contexts en confirmación.
- comparación directa T0 vs OLD_ACTION_COST vs REACTIVE.
- root spread calculado después de promediar policies.

## Resultado del cambio semántico

La nueva semántica reactiva sí crea separación real entre T0 y T1.

### Sapo

T0 HRS:
- 73,2813% player-win.

OLD_ACTION_COST 90% / CD3:
- 72,7734%.
- prácticamente igual a T0.

REACTIVE 60% / CD3:
- 63,0078%.
- delta vs T0: **-10,2734 pp**.

Por gear:
- CARRY: 52,2266% -> 32,8516% (-19,375 pp).
- EXPECTED: 73,2422% -> 59,5703% (-13,6719 pp).
- HRS: 73,2813% -> 63,0078% (-10,2734 pp).

Root spread HRS:
- T0: 13,0859 pp.
- T1 60/CD3: 12,8906 pp.
- delta: -0,1953 pp.

Adaptation procs:
- ~1,41 por combate agregado.

### Por qué no elegir 70% / CD3

70/CD3 da 60,0391% HRS y fue el ganador algorítmico por cercanía matemática a 60%.

Sin embargo:
- 60/CD3 ya está dentro de la banda diagnóstica;
- usa menor magnitud;
- deja más espacio para T2;
- no aumenta el root spread;
- evita sobreajustar una diferencia de pocos puntos a un target no canónico.

Recomendación humana: **MITIGATE_NEXT 60%, CD3**.

## Escarabajo

T0 HRS:
- 69,1406%.

OLD_ACTION_COST +12/CD3:
- 69,4531%.
- nuevamente casi igual a T0.

REACTIVE +4 DEF / CD3:
- 59,6094%.
- delta vs T0: **-9,5312 pp**.

Por gear:
- CARRY: 36,8359% -> 25,6641% (-11,1719 pp).
- EXPECTED: 86,2500% -> 79,6875% (-6,5625 pp).
- HRS: 69,1406% -> 59,6094% (-9,5312 pp).

Root spread HRS:
- T0: 13,4766 pp.
- T1 +4/CD3: 18,1641 pp.
- delta: +4,6875 pp.
Still below the historical 75 pp hard-polarization guard and no catastrophic new cliff.

Adaptation procs:
- ~1,66 per combat on the confirmed matrix.

### Why not +10/CD5

+10/CD5 gives 60,0781% HRS, only ~0,47 pp away from +4/CD3.
At R128/context this small difference is not meaningful enough to justify +10 flat DEF.

+4/CD3:
- achieves the same practical T1 separation;
- uses a much smaller magnitude;
- is easier to reason about;
- preserves more room for T2.

Recommendation: **DEFENSE_UP +4, CD3**.

## Proposed T1 LII freeze

### Sapo Ceniza
- kind: MITIGATE_NEXT
- magnitude: 60%
- cooldown: 3
- trigger: HP<=30% OR hit>=20% maxHP
- reactive: yes
- consumes monster turn: no
- affects DIRECT packet only
- persists through miss

### Escarabajo de Hierro
- kind: DEFENSE_UP
- magnitude: +4 DEF
- cooldown: 3
- trigger: HP<=30% OR hit>=20% maxHP
- reactive: yes
- consumes monster turn: no
- consumed after next player offensive action

## Status

No automatic freeze.
Awaiting human ratification.
