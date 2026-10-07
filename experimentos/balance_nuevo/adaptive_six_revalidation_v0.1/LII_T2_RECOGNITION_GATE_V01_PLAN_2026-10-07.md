# LII T2 Recognition Gate V01 — frozen reactive T1

Fecha: 2026-10-07
Estado: READY_FOR_COLAB

## Autoridad

T0:
`experimentos/balance_nuevo/t0_lii/T0_LII_FREEZE_MANIFEST_2026-10-07.json`

T1:
`experimentos/balance_nuevo/t1_lii/T1_LII_REACTIVE_FREEZE_2026-10-07.json`

T1 congelado:
- Sapo: MITIGATE_NEXT 60%, CD3, reactivo, no consume turno.
- Escarabajo: DEFENSE_UP +4, CD3, reactivo, no consume turno.

## T2 candidate

Se reutiliza la semántica final LI:
`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

### Reconocimiento
- memory_window: 2;
- requiere 2 acciones EFECTIVA consecutivas de la misma categoría;
- categorías visibles:
  - PLAYER_BASIC;
  - PLAYER_UNITARGET_TECHNIQUE;
  - PLAYER_AOE_TECHNIQUE;
  - PLAYER_DEFENSIVE_TECHNIQUE;
- no inspecciona root/build;
- no inspecciona RNG futuro.

### Anticipación
El reconocimiento sólo puede anticipar T1 si además:
- HP monstruo <=40%; OR
- golpe recibido actual >=15% HP máximo.

Prioridades:
1. trigger natural T1 HP<=30% / golpe>=20%;
2. anticipación T2 40/15 si hay reconocimiento;
3. si cooldown/estado bloquea, no rearma.

### Semántica con T1 reactivo

- anticipar T1 NO consume turno;
- no agrega una habilidad activa nueva;
- magnitud/cooldown T1 permanecen congelados;
- el monstruo realiza su turno ordinario;
- una técnica canónica due por cadencia no es reemplazada.

## Matriz

2 especies
× 3 gear contexts
× 5 roots
× 4 policies
× 2 arms (T1_FROZEN / T2_RECOGNITION)
× R256

= **61.440 combates**.

## Gear

- CARRY_OVER_FLOOR = HRS LI;
- EXPECTED_STAGE = expected LII;
- HIGH_ROLL_STRESS = HRS LII.

## Métricas

- player win-rate;
- rounds;
- HP pressure;
- monster damage total/direct/DOT;
- T1 natural activations;
- T2 anticipatory activations;
- recognition checks/triggers;
- prediction count/accuracy/false;
- recognitions blocked by cooldown/active survival;
- canonical technique due/turn preservation;
- root spread after averaging policies.

## Guards

Hard:
- 0 timeout/NaN/Inf;
- T1 arm must have zero T2 recognition leakage;
- T2 cannot modify T1 magnitude/cooldown;
- no root/build/future RNG inspection;
- no T3/T4;
- no new clock/timer;
- no main/merge.

Diagnostic:
- T2 must not become >2 pp easier than paired T1;
- HRS drop >8 pp vs T1 flags potential cliff for review;
- recognition/anticipation must occur at nonzero rate;
- no universal win-rate target.

## Output

`LII_T2_RECOGNITION_GATE_V01_REVIEW.zip`

No automatic freeze.
