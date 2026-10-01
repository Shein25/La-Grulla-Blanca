# Rata T3 — revisión de daño del counter

Fecha: 2026-10-01

## Contrato congelado durante esta fase

```text
T1:
Reflejo de Madriguera
+40 EVA / CD5 / REACTIVO_1 / BASE

T2:
R2_SHORT
memory 2 / repeat 2 / EFECTIVA / +8

Trigger T3 provisional:
CONFIRMED_PATTERN_REFLEJO_MISS
```

El trigger sólo arma T3 cuando:

1. T2 reconoció un patrón;
2. la acción real coincide con la predicción;
3. Reflejo estaba activo;
4. el mismo roll habría impactado contra la EVA natural;
5. ese roll falla después del +40 EVA de Reflejo.

## Candidatos de daño

Sólo se usaron expresiones de Rata ya medidas:

1. `FIXED_CANONICAL_2D4`;
2. `INSTANCE_BASIC`;
3. `FIXED_MEASURED_HIGH_2D4_PLUS_2`.

`INSTANCE_BASIC` usa el `basic_damage` ya resuelto para ese individuo, cuya
envolvente ratificada contiene:

```text
2d4
2d4+1
2d3+3
2d4+2
```

Fuentes medidas: trials 4254 / 251 / 192 / 240.

## Estudio

- 5 player policies;
- normales + Mutantes condicionados;
- 50.000 combates;
- pipeline normal de daño directo;
- sin QI_DRAIN, DOT ni Control;
- T4 bloqueado;
- 0 loops degenerados en todos los brazos.

## Resultados principales

### VETERAN — normal

| daño | daño/counter | daño/pelea | presión HP extra |
|---|---:|---:|---:|
| 2d4 fijo | 2,63 | 0,72 | +2,41 pp |
| INSTANCE_BASIC | 3,70 | 1,01 | +3,45 pp |
| 2d4+2 fijo | 4,34 | 1,18 | +3,97 pp |

Mutante:

| daño | daño/counter | daño/pelea | presión HP extra |
|---|---:|---:|---:|
| 2d4 fijo | 2,88 | 0,70 | +2,68 pp |
| INSTANCE_BASIC | 4,79 | 1,16 | +4,12 pp |
| 2d4+2 fijo | 4,78 | 1,16 | +4,11 pp |

### UNITARGET_FIRST — normal

`INSTANCE_BASIC`:

- ~0,274 counters/pelea;
- 3,70 daño/counter;
- 1,01 daño/pelea;
- +3,24 pp de presión HP;
- delta de victoria ≈ -0,05 pp.

### AOE_FIRST — normal

`INSTANCE_BASIC`:

- ~0,169 counters/pelea;
- 3,64 daño/counter;
- 0,61 daño/pelea;
- +2,07 pp de presión HP;
- delta de victoria ≈ -0,35 pp.

Mutante:

- 5,55 daño/counter;
- 0,52 daño/pelea;
- +1,39 pp de presión HP;
- delta de victoria ≈ -1,2 pp.

### DEFENSE_OPEN — normal

`INSTANCE_BASIC`:

- ~0,290 counters/pelea;
- 2,48 daño/counter;
- 0,72 daño/pelea;
- +2,68 pp de presión HP.

La defensa real del jugador reduce naturalmente el packet T3; no existe bypass.

### ROTATION

Todos los candidatos son prácticamente irrelevantes porque T2 casi nunca
confirma el patrón.

Esto preserva el contrajuego.

## Lectura

`FIXED_CANONICAL_2D4` funciona, pero desacopla T3 de la variabilidad ofensiva
que ya fue ratificada para individuos de la misma especie.

`FIXED_MEASURED_HIGH_2D4_PLUS_2` vuelve a todos los counters equivalentes al
extremo ofensivo medido, incluso en Ratas ordinarias.

`INSTANCE_BASIC` queda en medio de forma emergente:

- Rata normal → counter medio;
- Rata ofensivamente fuerte → counter fuerte;
- Mutante → tiende naturalmente hacia el extremo;
- no se inventa una segunda escala ofensiva;
- conserva exactamente el mismo `species_id` y perfil individual.

## Candidato provisional T3 completo

```text
Trigger:
CONFIRMED_PATTERN_REFLEJO_MISS

Daño:
INSTANCE_BASIC

Resolución:
normal direct-damage pipeline

No:
QI_DRAIN
DOT
Control
root/build inspection
once-per-fight artificial
```

Estado:

`T3_FULL_CANDIDATE_SELECTED_FINAL_VALIDATION_PENDING`

T4 permanece bloqueado.
