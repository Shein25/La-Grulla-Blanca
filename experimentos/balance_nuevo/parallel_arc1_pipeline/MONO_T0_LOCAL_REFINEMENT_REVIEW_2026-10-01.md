# Mono ladrón de píldoras — revisión T0 local refinement

Fecha: 2026-10-01

## Integridad

Archivo:

`RESULTADOS_MONO_T0_LOCAL_REFINEMENT.zip`

SHA-256:

`5d1b0106f2420ba009c4c34ea9631a2beb00fa8e250751c2ad168c9b84644947`

Contrato:

- experimento `MONO_T0_LOCAL_REFINEMENT_V01`;
- 48 configuraciones HP/DEF/EVA;
- identidad fija del trial 1068;
- paired common random numbers;
- WITH_DRAIN5 vs NO_DRAIN0;
- 500 peleas/contexto/arm en búsqueda;
- 5000 peleas/contexto/arm en final;
- 10 contextos;
- 7 finalistas;
- 100000 peleas por finalista (ambos arms);
- 1180000 peleas totales aproximadas entre búsqueda y final;
- sin selección automática;
- sin canonical write;
- sin T1–T4;
- sin target win rate.

Identidad fija:

```text
PREC 91
TEN  12
basic 1d2+3
Manotazo 1d2+3
QI_DRAIN 5
cadencia 2
```

## Frontera final

| grid | HP | DEF | EVA | forced basic causal Δ | QI drenado | presión NO_DRAIN | presión WITH_DRAIN | victoria WITH_DRAIN |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1  | 22 | 0 | 24 | 0.1920 | 4.2293 | 16.61% | 16.83% | 100.000% |
| 16 | 26 | 1 | 24 | 0.5517 | 5.9941 | 22.92% | 23.79% | 99.986% |
| 17 | 26 | 1 | 34 | 0.9003 | 7.1349 | 27.84% | 29.52% | 99.810% |
| **43** | **34** | **2** | **24** | **1.6698** | **9.3066** | **36.93%** | **41.20%** | **99.474%** |
| 46 | 34 | 3 | 24 | 2.1437 | 10.1246 | 44.81% | 51.23% | 96.972% |
| 47 | 34 | 3 | 34 | 2.3570 | 10.6550 | 54.78% | 61.73% | 88.984% |
| 48 | 34 | 3 | 44 | 2.4077 | 11.0501 | 66.61% | 73.13% | 72.820% |

## Candidato recomendado — grid 43

```text
HP   34
DEF   2
EVA  24
PREC 91
TEN  12

Básico: 1d2+3

Manotazo al Dantian
direct damage: 1d2+3
QI_DRAIN: 5
cadencia: 2
```

### Con drenaje

- victoria jugador: 99.474%;
- presión HP: 41.199%;
- rondas: 7.309;
- básicos forzados por Qi: 2.91984;
- Qi drenado: 9.30658;
- daño del monstruo: 13.03187;
- HP final p10: 32.551%.

### Sin drenaje

- victoria jugador: 99.744%;
- presión HP: 36.930%;
- rondas: 7.041;
- básicos forzados naturales: 1.25004;
- daño del monstruo: 11.67810.

### Efecto causal del QI_DRAIN

- +1.66980 básicos forzados por pelea;
- +133.58% respecto de los básicos forzados naturales NO_DRAIN;
- 57.19% de los básicos forzados observados WITH_DRAIN son atribuibles al drenaje;
- 9.30658 Qi drenado medio;
- -1.87076 Qi final;
- +4.269 pp presión HP;
- -0.270 pp victoria jugador;
- +1.35377 daño monstruo;
- +0.26844 rondas.

La diferencia entre Qi drenado (9.31) y Qi final (-1.87) confirma de nuevo que
`player_qi_final` no representa por sí solo la identidad: el jugador deja de
pagar técnicas y pasa a básicos.

## Robustez grid 43

WITH_DRAIN por raíz:

| raíz | victoria | HP final |
|---|---:|---:|
| Agua | 98.88% | 57.08% |
| Fuego | 99.80% | 66.80% |
| Metal | 99.60% | 56.47% |
| Tierra | 99.68% | 58.05% |
| Viento | 99.41% | 55.61% |

- spread HP entre raíces: 11.18 pp;
- spread victoria entre raíces: 0.92 pp.

Por equipo:

- EXPECTED_STAGE: victoria 99.492%, HP final 59.37%;
- MANDATORY_ENTRY: victoria 99.456%, HP final 58.23%;
- spread HP loadout: 1.14 pp;
- spread victoria loadout: 0.036 pp.

No depende de una sola raíz ni del loadout.

## Por qué no grid 17

Grid 17 reduce más la presión basal (27.84%), pero la identidad se expresa menos:

- +0.9003 básicos causales;
- 7.13 Qi drenado;
- sólo +1.68 pp de presión por drenaje.

Es válido como criatura más ligera, pero desaprovecha parte de la identidad
`QI_DRAIN / SKIRMISHER`.

## Por qué no grid 46

Grid 46 obtiene más señal causal (+2.1437 básicos), pero:

- presión NO_DRAIN ya sube a 44.81%;
- presión WITH_DRAIN a 51.23%;
- spread HP entre raíces sube a 17.43 pp;
- la victoria Agua cae a 93.85%.

Es un candidato fuerte útil para variabilidad, pero peor centro T0.

## Por qué no grid 47/48

La supervivencia vuelve a dominar el encuentro.

Grid 48 prácticamente reproduce el problema del viejo trial 1068:

- NO_DRAIN presión 66.61%;
- WITH_DRAIN presión 73.13%;
- victoria WITH_DRAIN 72.82%;
- spread de victoria entre raíces 25.25 pp.

El QI_DRAIN sigue siendo real, pero deja de ser la explicación principal de la
dificultad.

## Contraste contra trial 1068 original

Trial 1068:

- HP34 / DEF3 / EVA44;
- NO_DRAIN presión ≈66.56%;
- WITH_DRAIN presión ≈73.16%;
- causal forced basics ≈+2.418.

Grid 43 conserva la misma identidad ofensiva pero cambia sólo supervivencia:

- HP34 / DEF2 / EVA24;
- NO_DRAIN presión 36.93%;
- WITH_DRAIN presión 41.20%;
- causal forced basics +1.6698.

Se reduce drásticamente la dificultad independiente del drenaje sin volver el
drenaje invisible.

## Decisión recomendada

`mono_pildoras grid 43`

Estado:

`T0_NUMERIC_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION`

No modificar todavía el registro canónico ni habilitar T1.

## Variabilidad intraespecie

Si grid 43 es ratificado como piso T0, los datos ya contienen una banda de
supervivencia fuerte hasta grid 48.

Para la futura capa de variabilidad/Mutante:

- piso provisional: grid 43;
- grid 46/47: referencias intermedias fuertes;
- grid 48 / trial 1068: referencia superior de supervivencia con identidad fija;
- trial 1274 del search amplio sigue siendo evidencia de una envolvente ofensiva
  extrema, pero mezcla daño, precisión, técnica y drenaje distintos y no debe
  combinarse automáticamente con grid 48 sin un test de variabilidad.

