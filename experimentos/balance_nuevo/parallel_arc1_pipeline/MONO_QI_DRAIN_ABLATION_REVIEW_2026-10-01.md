# Mono Ladrón de Píldoras — revisión causal QI_DRAIN

Fecha: 2026-10-01

## Integridad

Archivo analizado:

`RESULTADOS_MONO_QI_DRAIN_ABLATION.zip`

SHA-256:

`dd8fe1e839e1469045814565bd12fc30f42bf43ff45f40cb6487b0369d927c2e`

Configuración:

- 5 candidatos;
- 2 brazos por candidato;
- 10 contextos;
- 10000 peleas/contexto/brazo;
- 1000000 peleas totales;
- common random numbers;
- única diferencia A/B: `qi_drain -> 0`;
- sin escritura CANON;
- sin selección automática;
- sin T1–T4.

## Hallazgo metodológico

La métrica `forced_basic_due_to_qi` original mezcla:

1. agotamiento natural de Qi por gasto del jugador;
2. agotamiento adicional provocado por `QI_DRAIN`.

La ablación permite aislar causalmente el punto 2.

El efecto de drenaje **no debe medirse sólo por Qi final**: cuando el Mono
drena Qi, el jugador deja antes de pagar técnicas y usa más ataques básicos,
conservando parte del Qi que de otra manera habría gastado.

Por eso el efecto causal aparece principalmente en:

- `forced_basic_delta`;
- cambio de presión HP;
- cambio de victoria;
- gasto de Qi evitado/reemplazado;
- no sólo en `qi_final_delta`.

## Resultados

| Trial | drain | cadence | forced basic A | forced basic B | delta causal | QI drenado | delta victoria | presión extra |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1211 | 1 | 4 | 0.00688 | 0.00475 | +0.00213 | 0.0298 | 0.000 pp | +0.0027 pp |
| 1179 | 8 | 2 | 5.57435 | 4.58991 | +0.98444 | 14.45289 | -16.526 pp | +7.428 pp |
| 1068 | 5 | 2 | 7.35876 | 4.94045 | **+2.41831** | 11.06776 | -7.813 pp | +6.600 pp |
| 1331 | 2 | 4 | 0.00910 | 0.00513 | +0.00397 | 0.05285 | 0.000 pp | +0.0049 pp |
| 1274 | 4 | 2 | 2.77403 | 1.75917 | +1.01486 | 8.98574 | -5.657 pp | +1.393 pp |

## Lectura por identidad

### 1211 / 1331

El Mono casi nunca llega a ejecutar la técnica:

- skill uses ≈ 0.03 por pelea;
- drenaje medio ≈ 0.03–0.05 Qi.

La identidad `QI_DRAIN` es prácticamente invisible. No son buenos anclajes
para el Mono aunque el combate global sea ligero.

### 1179

El drenaje tiene efecto real, pero el candidato ya es muy dominante sin
drenaje:

- win jugador sin drain: 48.857%;
- presión HP sin drain: 83.658%.

La identidad deja de estar aislada: buena parte de la dificultad proviene de
la supervivencia/daño base del perfil.

### 1274

También expresa drenaje, pero es todavía más extremo sin drenaje:

- win jugador sin drain: 12.926%;
- presión HP sin drain: 96.898%.

Su daño directo domina la identidad. No es un buen ancla para diseñar un
`SKIRMISHER` de presión sobre Qi.

### 1068 — ancla recomendada para refinación

Parámetros:

```text
HP 34
DEF 3
EVA 44
PREC 91
TEN 12
basic 1d2+3
tech direct 1d2+3
QI_DRAIN 5
cadence 2
```

Ablación:

```text
forced basic con drain   7.35876
forced basic sin drain   4.94045
delta causal            +2.41831

incremento vs baseline natural ≈ +48.95%
fracción de básicos forzados atribuible al drain ≈ 32.86%

QI drenado medio        11.06776
delta Qi final          -1.70218

win jugador con drain    72.843%
win jugador sin drain    80.656%
delta causal             -7.813 pp

presión HP con drain     73.158%
presión HP sin drain     66.559%
delta causal             +6.600 pp
```

El hecho de que drene 11.07 Qi pero el Qi final sólo baje 1.70 confirma que el
jugador **adapta su gasto involuntariamente** al quedarse sin recurso.

## Robustez de 1068 por raíz

Delta de victoria causado por drain:

- Agua: -6.315 pp
- Fuego: -5.115 pp
- Metal: -11.610 pp
- Tierra: -9.820 pp
- Viento: -6.205 pp

No depende de una única raíz.

Por equipo:

- EXPECTED_STAGE: -7.628 pp
- MANDATORY_ENTRY: -7.998 pp

Tampoco depende materialmente de un solo loadout.

## Decisión de laboratorio

`trial 1068` queda como:

`MONO_QI_DRAIN_IDENTITY_ANCHOR_FOR_LOCAL_REFINEMENT`

No se promueve a READY.

Motivo: su `QI_DRAIN=5 / cadence=2` y daños directos bajos expresan la
identidad correctamente, pero HP/DEF/EVA hacen que la presión sin drenaje siga
siendo demasiado protagonista para aislar una criatura cuyo concepto es
presionar Qi/Dantian y jugar oportunistamente.

## Próximo bloque

Conservar del 1068:

- PREC 91;
- TEN 12;
- basic `1d2+3`;
- tech direct `1d2+3`;
- QI_DRAIN 5;
- cadence 2;
- cognition CAZADOR_2;
- social OPORTUNISTA.

Refinar únicamente supervivencia:

- HP: 22 / 26 / 30 / 34
- DEF: 0 / 1 / 2 / 3
- EVA: 24 / 34 / 44

48 configuraciones exhaustivas.

Objetivos del frente:

1. maximizar `forced_basic_delta` causal;
2. minimizar presión HP del brazo `NO_DRAIN`.

`QI drained`, duración, win rate, raíces y loadout se reportan como
descriptivos. No existe target de win rate.

No se debe reabrir daño, precision, tenacity, drain o cadence en este bloque.
