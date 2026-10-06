# LI — T2 final all-five gate V03

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / FINAL T2 CANDIDATE GATE

## Candidato

`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

- memory_window = 2;
- repeated_same_category_required = 2;
- count_results = EFECTIVA;
- threat anticipation = HP<=40% OR current received hit>=15% monster HPmax;
- recognition-only survival cannot replace a canonical technique due by cadence;
- frozen T1 natural trigger HP<=30% OR hit>=20% keeps priority;
- T1 magnitude/cooldown/charges remain species-specific and frozen.

## Rationale

This candidate is derived from:
- Rata historical R2_SHORT recognition identity;
- LI T2 V01 all-five micro-screen;
- Rata+Serpiente V02 focal causal test.

It does not introduce universal stat scaling or new active abilities.

## Final matrix

- five LI species;
- five roots;
- EXPECTED_STAGE + HIGH_ROLL_STRESS;
- UNITARGET_FIRST / AOE_FIRST / DEFENSE_OPEN / ROTATION;
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO;
- 64/16/8/4 individual pools;
- 4 combat replicas per individual/cell;
- T1_FROZEN vs selected T2 candidate;
- CRN paired;
- 147.200 represented fights.

## Hard guards

- T0 untouched;
- T1 exact;
- no canonical-technique replacement from recognition when due;
- no root/build inspection;
- no new clocks/timers;
- no T3/T4;
- suffix contract V1 unchanged;
- no win-rate target;
- fail only on mechanical invalidity, identity break, timeout/NaN/Inf, CRN/contract drift.

## Colab UI

Compact progress standard:
- fixed width ~88 columns;
- 20-character bar;
- short label;
- abbreviated CPU/RAM/rate;
- no terminal-width expansion;
- no Kaggle paths.

No automatic ratification.
