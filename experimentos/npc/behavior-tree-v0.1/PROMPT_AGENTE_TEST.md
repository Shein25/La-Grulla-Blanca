# Auditoría externa REV2 — Behavior Tree v0.1

Audita exclusivamente la cabeza actual de `experiment/npc-behavior-tree-v0.1`.

La auditoría REV1 terminó en:

`BEHAVIOR_TREE_V01_REQUIERE_CORRECCIONES`

por un bug sistemático en `preemptedAction`. REV2 corrige ese bug sin cambiar arquitectura.

NO modifiques producción.
NO integres NPC canónicos.
NO añadas Utility AI, GOAP, HTN o pathfinding.
NO hagas merge.

## 1. Suite histórica

```bash
node tests.mjs
```

Debe conservar 34 PASS / 0 FAIL.

## 2. Regresiones REV2

```bash
node tests-rev2.mjs
```

Debe producir 6 PASS / 0 FAIL.

No aceptes esa suite como prueba suficiente: reproduce independientemente los casos.

## 3. Retest obligatorio del bug principal

Partiendo de una acción `RUNNING`:

1. si recibe `SUCCESS`, `preemptedAction` debe ser `null`;
2. si recibe `FAILURE`, `preemptedAction` debe ser `null`;
3. si no recibe resultado y una prioridad superior desplaza la acción, debe aparecer en `preemptedAction`;
4. si recibe `RUNNING` pero una prioridad superior la desplaza, debe aparecer en `preemptedAction`;
5. si recibe un resultado terminal y simultáneamente empieza una prioridad superior, la acción anterior terminó normalmente y NO debe marcarse preemptada.

Busca variantes en los tres fixtures y en árboles sintéticos propios.

## 4. Estabilidad tree/runtime

REV2 fija explícitamente este contrato:

> Un runtime pertenece a una definición estructuralmente estable del árbol. Cambiar topología, IDs o intents durante la vida de ese runtime está fuera de contrato y exige crear un runtime nuevo.

Comprueba que la documentación sea inequívoca. No trates hot-reload de topología sobre un runtime vivo como uso soportado de v0.1.

## 5. Stress

Repite:

```bash
node stress.mjs 100000 1337
node stress.mjs 100000 1
node stress.mjs 100000 42
node stress.mjs 100000 999
node stress.mjs 100000 20260925
```

No presupongas que los digests REV1 deben permanecer iguales: `preemptedAction` era parte del trace y su semántica fue corregida.

Exige:

- digest repetible por seed;
- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidRuntime = 0`;
- `multiEmit = 0`.

## 6. Regresión adversarial general

Vuelve a atacar:

- selector/sequence;
- RUNNING;
- preempción;
- actionResults;
- multi-intent;
- límites de profundidad/nodos/hijos;
- ciclos;
- arrays hostiles;
- Proxies;
- overflow de tick;
- pureza;
- determinismo;
- aliasing;
- contaminación de prototipo;
- facts ausentes;
- `-0` vs `0`.

## 7. Frontera arquitectónica

Debe seguir cumpliéndose:

```text
reevalúa prioridades
→ selecciona como máximo una acción
→ emite intención
→ executor externo resuelve
```

No debe ejecutar movimiento, combate ni efectos del mundo.

## 8. Entregable

Informe Markdown con HEAD exacto, integridad, resultados, reproducciones independientes, cualquier hallazgo nuevo y un único veredicto:

```text
BEHAVIOR_TREE_V01_REV2_APTO_PARA_ITERAR
BEHAVIOR_TREE_V01_REV2_REQUIERE_CORRECCIONES
BEHAVIOR_TREE_V01_REV2_FALLO_CONCEPTUAL
```
