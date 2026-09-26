# NPC Behavior Benchmark v0.1

Benchmark escalable sobre los tres NPC usados para calibrar el laboratorio.

## Objetivo

No busca elegir automáticamente una IA "ganadora". Busca producir evidencia reproducible sobre:

- decisiones e intents;
- acuerdos y desacuerdos entre motores;
- preempciones;
- acciones inválidas;
- superficies donde Utility cambia por magnitud/contexto;
- reproducibilidad por seed.

## Cargas

Cada tier indica **ejecuciones por NPC**:

| Tier | Ejecuciones/NPC |
| --- | ---: |
| smoke | 10.000 |
| standard | 100.000 |
| deep | 500.000 |
| million | 1.000.000 |

También se puede usar `--runs N`.

Millones de ejecuciones son opcionales. Se usan sólo cuando el barrido necesita más resolución o cuando queramos stress prolongado.

## Modos actuales

### Gao Shun / Pei Luo — replay

Muestrea repetidamente sus escenarios calibrados y comprueba:

- intents dentro del whitelist;
- secuencia FSM/BT;
- preempciones;
- divergencias reproducibles.

### Jiang Rui — decision surface

Genera contextos Monte Carlo con:

- peligro 0..100;
- urgencia 0..100;
- anomalía sí/no;
- superior alcanzable sí/no;
- fuera de puesto sí/no.

Para FSM/BT se deriva una categoría `highRisk` con umbrales **experimentales del benchmark**:

- `danger >= 60`, o
- `missionUrgency >= 70`.

Utility recibe las magnitudes completas.

Esto permite encontrar zonas donde FSM/BT y Utility convergen o divergen.

## Ejecutar

```bash
node benchmark/test-benchmark.mjs
node benchmark/run-benchmark.mjs --tier smoke --seed 1337
node benchmark/run-benchmark.mjs --tier standard --seed 1337 --npc jiang_rui
node benchmark/run-benchmark.mjs --tier million --seed 20260925 --out benchmark.json
```

## Interpretación

Un desacuerdo no es automáticamente un error.

Ejemplo esperado:

```text
anomalía leve
FSM/BT  -> investigar
Utility -> puede seguir patrullando
```

El benchmark registra el contexto exacto para revisión posterior.

## Frontera

- no modifica producción;
- no decide canon;
- no modifica los motores vendorizados;
- no inventa traits canónicos;
- no ejecuta pathfinding ni combate real.

## Próxima expansión

Cuando el método quede estable:

1. incorporar más NPC canónicos;
2. añadir perfiles/motores candidatos según corresponda;
3. ejecutar barridos amplios en Colab;
4. congelar matriz NPC × arquitectura;
5. pasar al bloque de monstruos.
