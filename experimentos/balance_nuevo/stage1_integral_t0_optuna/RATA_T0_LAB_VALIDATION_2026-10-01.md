# RATA DE QI — VALIDACIÓN INTEGRAL T0 LAB

Fecha: 2026-10-01

Estado:

`LAB_VALIDATED_AWAITING_HUMAN_SELECTION`

Este documento **no selecciona CANON**, no modifica `monster_arc1_registry.json`,
no marca `stats_status=READY` y no habilita T1-T4.

## Contrato

- Motor: `NEW_COMBAT_STATS_V0_1`
- Especie: `rata_qi`
- Tier: `T0`
- Técnica T0: ninguna
- Crítico fijo: 5%
- Multiplicador crítico fijo: 1.50
- Control T0: 0
- `qi_max`: semántica pendiente; fuera de la búsqueda
- Definitivas: prohibidas
- Adaptación T1-T4: bloqueada

## Pipeline ejecutado

Todos los pasos pasaron en GitHub Actions sobre la rama
`experiment/combat-stat-contract-v0.1`.

1. selfcheck
2. guards adversariales
3. pruebas de VETERAN
4. preflight runtime real
5. smoke 32 × 20
6. búsqueda NSGA-II 256 × 40
7. revalidación Pareto 500 con common random numbers
8. revalidación Pareto 1000 con common random numbers
9. selección geométrica neutral de cinco representantes
10. stress/control 1000
11. alta precisión de tres representantes internos × 3000

No se usó target de win rate.

## Search 256 × 40

- trials COMPLETE: 256/256
- peleas por trial: 400
- peleas: 102.400
- timeouts: 0
- frente Pareto inicial: 24
- win rate observado: 99,5%–100%

Objetivos:

1. maximizar presión observada sobre HP;
2. minimizar presupuesto normalizado del candidato.

El win rate se conserva como diagnóstico, no como target.

## Revalidación 500

- candidatos recibidos: 24
- peleas por candidato: 5.000
- peleas: 120.000
- supervivientes Pareto: 20

Cuatro puntos dejaron de ser Pareto al reducir el ruido Monte Carlo:
trials 38, 128, 140 y 221.

## Revalidación 1000

- candidatos recibidos: 20
- peleas por candidato: 10.000
- peleas: 200.000
- supervivientes Pareto: 20/20

La presión fue muy estable respecto de la etapa 500: el cambio medio fue
aproximadamente +0,005 puntos porcentuales y la desviación aproximada fue
0,146 puntos porcentuales.

Esto justifica dejar de aumentar precisión sobre los veinte puntos completos
y pasar a cobertura neutral + stress.

## Cinco representantes geométricos

Los representantes se tomaron por longitud de arco normalizada del frente, en
fracciones 0%, 25%, 50%, 75% y 100%. Esto **no es un ranking**.

| Fracción | Trial | HP | DEF | EVA | PREC | TEN | Básico | Presión primaria 1000 |
|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 0% | 190 | 8 | 0 | 14 | 82 | 2 | 1d3+2 | 1,52% |
| 25% | 245 | 22 | 0 | 4 | 84 | 0 | 1d4+2 | 10,72% |
| 50% | 251 | 21 | 0 | 8 | 88 | 1 | 2d4+1 | 17,83% |
| 75% | 192 | 22 | 0 | 4 | 104 | 0 | 2d3+3 | 27,30% |
| 100% | 240 | 18 | 1 | 19 | 104 | 0 | 2d4+2 | 31,08% |

## Stress/control 1000

Cada representante se probó con:

- `HIGH_ROLL_STRESS + NONE + VETERAN`;
- `MANDATORY_ENTRY + NONE + UNITARGET_FIRST`;
- `EXPECTED_STAGE + NONE + UNITARGET_FIRST`;

en las cinco raíces y con common random numbers.

Total: 75.000 peleas.

La presión de stress permaneció muy próxima a la presión primaria. No apareció
un colapso por equipamiento alto ni una dependencia fuerte de VETERAN.

El extremo de mayor presión (trial 240) fue el único de estos cinco en mostrar
una mortalidad pequeña pero medible:

- EXPECTED + UNITARGET_FIRST: win jugador 99,62%
- HIGH_ROLL + VETERAN: win jugador 99,72%
- MANDATORY + UNITARGET_FIRST: win jugador 99,62%

Los cuatro restantes mantuvieron win jugador = 100% en esos brazos.

## Alta precisión 3000

Se eligieron **tres representantes internos**, no extremos, por posición
geométrica 25% / 50% / 75%.

Cada uno recibió:

- 3.000 peleas por contexto;
- 10 contextos primarios;
- 30.000 peleas por candidato;
- common random numbers.

Total: 90.000 peleas.

### Trial 245 — posición 25%

```text
HP        22
DEF        0
EVA        4
PREC      84
TEN        0
BASIC   1d4+2
```

Resultado 3000:

- presión HP: 10,6384%
- HP final jugador medio: 89,3616%
- win jugador: 100%
- rondas medias: 2,9041
- EXPECTED HP final: 89,4878%
- MANDATORY HP final: 89,2354%

Por raíz, HP final jugador:

- Agua: 92,1758%
- Fuego: 90,6522%
- Metal: 87,4425%
- Tierra: 88,4091%
- Viento: 88,1285%

### Trial 251 — posición 50%

```text
HP        21
DEF        0
EVA        8
PREC      88
TEN        1
BASIC   2d4+1
```

Resultado 3000:

- presión HP: 17,8155%
- HP final jugador medio: 82,1845%
- win jugador: 100%
- rondas medias: 2,9243
- EXPECTED HP final: 82,3792%
- MANDATORY HP final: 81,9898%

Por raíz, HP final jugador:

- Agua: 86,0634%
- Fuego: 84,8978%
- Metal: 79,1425%
- Tierra: 80,6026%
- Viento: 80,2161%

### Trial 192 — posición 75%

```text
HP        22
DEF        0
EVA        4
PREC     104
TEN        0
BASIC   2d3+3
```

Resultado 3000:

- presión HP: 27,0844%
- HP final jugador medio: 72,9156%
- win jugador: 99,9967%
- rondas medias: 3,0014
- EXPECTED HP final: 73,1593%
- MANDATORY HP final: 72,6720%

Por raíz, HP final jugador:

- Agua: 80,1728%
- Fuego: 77,0071%
- Metal: 67,9527%
- Tierra: 70,9848%
- Viento: 68,4608%

En 30.000 peleas se registró una única derrota del jugador.

## Lectura del sistema

La búsqueda no produjo un único “número correcto”; produjo una frontera estable
entre dos magnitudes legítimas:

- amenaza/desgaste que consigue la Rata;
- presupuesto estadístico necesario para conseguirlo.

Los tres representantes internos siguen siendo Pareto después de 30.000 peleas
cada uno. Por lo tanto, la simulación no proporciona una razón matemática para
declarar uno superior a los otros.

La decisión pendiente es de **identidad/diseño**: qué nivel de desgaste debe
representar la amenaza sobrenatural más baja de Arco 1.

## Estado canónico

Sin cambios.

`rata_qi.stats_status = PENDING_INTEGRAL_REBALANCE`

`rata_qi.technique = null`

`adaptive.status = BLOCKED_UNTIL_T0_READY`

No se seleccionó candidato.
No se promovió candidato.
No se inició T1-T4.
