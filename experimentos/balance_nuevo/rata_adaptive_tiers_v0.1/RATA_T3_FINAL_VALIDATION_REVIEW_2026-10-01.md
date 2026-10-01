# Rata T3 — revisión final del candidato completo

Fecha: 2026-10-01

## Candidato validado

```text
T3 identity:
SPECIES_COUNTER / PHYSICAL_RETALIATION

Trigger:
CONFIRMED_PATTERN_REFLEJO_MISS

Daño:
INSTANCE_BASIC

Resolución:
pipeline normal de daño directo
```

Cadena causal obligatoria:

1. T2 R2_SHORT reconoce una repetición observable;
2. la Rata elige Reflejo de Madriguera;
3. la siguiente acción real del jugador coincide con la categoría predicha;
4. el mismo roll de hit habría conectado contra la EVA natural del individuo;
5. el +40 EVA de Reflejo convierte ese roll en fallo;
6. T3 arma un contraataque físico;
7. el counter usa el `basic_damage` ya resuelto de esa instancia.

No existe counter si el fallo habría ocurrido aun sin Reflejo.

## Contratos anteriores congelados

T1:

```text
Reflejo de Madriguera
+40 EVA
CD5
REACTIVO_1
BASE
```

T2:

```text
R2_SHORT
memory_window = 2
repeat = 2
count_results = EFECTIVA
recognition bonus = +8
```

T3 no modifica ninguno de esos valores.

## Por qué INSTANCE_BASIC

La Rata ya tiene variabilidad ofensiva ratificada.

Su ladder medida es:

```text
2d4
2d4+1
2d3+3
2d4+2
```

Por tanto el counter:

- no introduce una segunda escala ofensiva;
- mantiene diferencias entre individuos;
- una Rata normal contraataca como una Rata normal;
- una Rata ofensivamente excepcional contraataca más fuerte;
- un Mutante hereda naturalmente ese extremo.

## Validación final

- 5 policies;
- 10 contextos por policy;
- 1.000 naturales/contexto;
- 250 Mutantes condicionados/contexto;
- T2 baseline + T3 candidato;
- 125.000 combates totales;
- T4 no ejecutado.

## VETERAN

Normal:

- 0,2823 counters/pelea;
- 3,64 daño/counter;
- 1,03 daño T3/pelea;
- p90 counter = 6;
- +3,38 pp de presión HP;
- delta win ≈ -0,03 pp.

Mutante:

- 0,2824 counters/pelea;
- 4,75 daño/counter;
- 1,34 daño T3/pelea;
- p90 = 7;
- +4,33 pp de presión HP;
- sin cambio material de win rate.

## UNITARGET_FIRST

Normal:

- 0,2839 counters/pelea;
- 3,64 daño/counter;
- 1,03 daño/pelea;
- +3,18 pp presión HP;
- delta win ≈ -0,05 pp.

Mutante:

- 0,2944 counters/pelea;
- 4,76 daño/counter;
- 1,40 daño/pelea;
- +4,36 pp presión HP;
- delta win ≈ -0,28 pp.

## AOE_FIRST

Es la policy más castigada, pero también la más repetitiva/subóptima en 1v1.

Normal:

- 0,1612 counters/pelea;
- 3,82 daño/counter;
- 0,62 daño/pelea;
- +1,83 pp presión HP;
- delta win ≈ -0,71 pp.

Mutante:

- 0,1008 counters/pelea;
- 4,74 daño/counter;
- 0,48 daño/pelea;
- +1,10 pp presión HP;
- delta win ≈ -1,40 pp.

El trigger sigue exigiendo predicción confirmada; no castiga el cambio de patrón.

## DEFENSE_OPEN

Normal:

- 0,2844 counters/pelea;
- 2,60 daño/counter;
- 0,74 daño/pelea;
- +2,67 pp presión HP;
- delta win ≈ -0,01 pp.

Mutante:

- 0,2872 counters/pelea;
- 3,27 daño/counter;
- 0,94 daño/pelea;
- +3,47 pp presión HP;
- delta win ≈ -0,08 pp.

La defensa del jugador reduce el counter mediante el pipeline normal. No hay
bypass.

## ROTATION

T3 prácticamente desaparece:

Normal:

- 0,00040 counters/pelea;
- ~0,0014 daño T3/pelea.

Mutante:

- 0,0008 counters/pelea;
- ~0,0036 daño T3/pelea.

Esto confirma el contrajuego central:

```text
repetir patrón
→ T2 aprende
→ Reflejo anticipa
→ insistir en el patrón
→ T3 castiga

romper patrón
→ T2 pierde certeza
→ T3 desaparece
```

## Guardias

En 125.000 peleas:

- false counter rate = 0 en todas las policies;
- degenerate counter loops = 0;
- multi-counter fight rate = 0;
- máximo counter observado por pelea = 1;
- QI_DRAIN añadido = no;
- DOT añadido = no;
- Control añadido = no;
- root/build inspection = no;
- T4 ejecutado = no.

## Estado recomendado

`T3_FULL_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION`

Candidato:

```text
CONFIRMED_PATTERN_REFLEJO_MISS
+
INSTANCE_BASIC
```

No abrir T4 hasta ratificación humana.
