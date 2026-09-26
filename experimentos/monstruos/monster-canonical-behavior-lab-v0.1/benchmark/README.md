# Monster Behavior Benchmark v0.1

Benchmark escalable de las 18 criaturas combatientes canónicas.

## Tiers

Cada tier es **por monstruo seleccionado**:

| Tier | decisiones por mob |
| --- | ---: |
| smoke | 1.000 |
| standard | 10.000 |
| deep | 100.000 |
| million | 1.000.000 |

Con `--mob all`, `million` implica 18 millones de decisiones primarias, más las comparaciones internas. Úsalo sólo cuando haga falta.

## Qué varía

En rondas donde la técnica está disponible experimentalmente:

- PLAYER_LOW_HP;
- aliados;
- superioridad numérica;
- 0–4 recuerdos;
- resultado EFECTIVA/FALLIDA;
- 0–4 repeticiones recientes de la técnica;
- seed de jitter determinista.

## Comparaciones por escenario

Se ejecuta la misma decisión con la misma seed en cuatro variantes:

1. full;
2. sin memoria;
3. sin social;
4. neutral (sin memoria ni social).

Así se mide:

- `memoryChangedDecision`;
- `socialChangedDecision`;
- `combinedChangedVsNeutral`.

Cada 10 escenarios también se verifica `CADENCE_COMPAT`. Una violación de cadencia es siempre error.

## Ejecutar

```bash
node benchmark/test-benchmark.mjs
node benchmark/run-benchmark.mjs --tier smoke
node benchmark/run-benchmark.mjs --tier standard --mob guardian_coral
node benchmark/run-benchmark.mjs --tier million --mob lobo_espiritual --out lobo.json
```

## Interpretación

Una tasa alta de cambio no significa automáticamente mejor IA. Sirve para localizar qué monstruos son sensibles a memoria/social y revisar si ese comportamiento encaja con su diseño.
