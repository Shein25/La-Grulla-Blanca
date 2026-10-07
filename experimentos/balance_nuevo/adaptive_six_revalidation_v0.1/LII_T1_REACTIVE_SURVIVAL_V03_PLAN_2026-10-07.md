# LII T1 Reactive Survival V03 — paired recalibration

Fecha: 2026-10-07
Estado: READY_FOR_COLAB

## Objetivo

Recalibrar T1 de:
- Sapo Ceniza;
- Escarabajo de Hierro;

bajo la nueva semántica reactiva aprobada:
- activa defensa al cumplirse trigger;
- NO consume turno;
- el monstruo ejecuta luego su acción ordinaria.

## Comparadores

Se incluyen:
1. T0 puro.
2. T1 OLD_ACTION_COST:
   - Sapo 90% / CD3;
   - Escarabajo +12 DEF / CD3.
3. T1 REACTIVE candidatos.

La comparación usa misma raíz/policy/gear/seed.

## Trigger

- HP <=30% maxHP OR
- golpe recién recibido >=20% maxHP.

## Sapo — MITIGATE_NEXT REACTIVE

Magnitudes:
- 10, 20, 30, 40, 50, 60, 70%.

Cooldown:
- 3, 4, 5, 6.

28 candidatos.

Semántica:
- protege contra siguiente paquete DIRECTO conectado;
- antes de DEF plana;
- persiste si el ataque falla;
- no afecta DoT;
- no consume turno.

## Escarabajo — DEFENSE_UP REACTIVE

Bonos:
- +2, +4, +6, +8, +10, +12.

Cooldown:
- 3, 4, 5, 6.

24 candidatos.

Semántica:
- DEF extra contra próxima acción ofensiva;
- se consume tras esa acción;
- no consume turno.

## Matriz

### Fase A — screen HRS

52 candidatos reactivos
× 5 roots
× 4 policies
× R32
= **33.280 peleas**.

### Fase B — confirmación TOP8

16 finalistas
× 3 gear contexts
× 5 roots
× 4 policies
× R128
= **122.880 peleas**.

### Controles T0

2 especies
× 3 gears
× 5 roots
× 4 policies
× R128
= **15.360 peleas**.

### Comparador OLD_ACTION_COST

2 especies
× 3 gears
× 5 roots
× 4 policies
× R128
= **15.360 peleas**.

TOTAL:
**186.880 combates**.

## Selección

Primary:
- 0 timeout;
- T1 reactivo no puede ser >2 pp más fácil que T0 pareado;
- proc >0;
- root spread se calcula DESPUÉS de promediar policies;
- no introducir un nuevo cliff material frente a T0.

Diagnostic:
- HRS player-win 55–65% es zona deseable;
- centro ~60%;
- no es regla universal ni obligación matemática.

Desempate:
1. dentro de banda;
2. más cerca de 60%;
3. menor magnitud;
4. cooldown más largo si resultado equivalente.

## Gear contexts

- CARRY_OVER_FLOOR = HRS LI;
- EXPECTED_STAGE = expected LII;
- HIGH_ROLL_STRESS = HRS LII.

## Hard guards

- T0 LII frozen;
- no LI changes;
- no T2–T4;
- no T5;
- no new mechanic family;
- no new clock/timer;
- no main;
- no merge;
- G04 Tierra;
- exact registry schema;
- multiprocessing without lambdas.

## Output

`LII_T1_REACTIVE_SURVIVAL_V03_REVIEW.zip`

No freeze automático.
