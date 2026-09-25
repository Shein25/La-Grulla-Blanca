# Behavior Tree v0.1 — Laboratorio NPC

Experimento aislado para NPC que necesitan **reevaluar prioridades cada tick** sin llegar a la planificación profunda de Utility AI + GOAP.

## Hipótesis

Un Behavior Tree pequeño debería cubrir NPC que tienen varias prioridades reactivas ordenadas, por ejemplo:

- guardia que patrulla, advierte y combate según contexto;
- trabajador cuya rutina puede ser interrumpida por una alarma;
- supervisor que prioriza crisis sobre solicitudes normales.

Los fixtures son sintéticos. No modifican NPC canónicos.

## Nodo mínimo

```text
selector
sequence
condition
action
```

Los nodos `action` no ejecutan efectos del mundo: emiten un `intent` y quedan `RUNNING` hasta que una capa externa devuelve `SUCCESS`, `FAILURE` o `RUNNING`.

## Diferencia respecto de Reactive Routine FSM

La FSM representa estados/transiciones explícitos. El Behavior Tree vuelve a recorrer prioridades en cada tick:

```text
¿crisis?
  sí -> responder
  no
    ¿solicitud?
      sí -> atender
      no -> rutina
```

Esto permite preempción natural: una acción de rutina puede ser desplazada por una prioridad superior sin modelar una transición explícita desde cada estado posible.

## API

```js
validateTree(tree)
createRuntime(tree)
tickBehaviorTree(tree, runtime, tick)
```

## Contrato v0.1 REV2

- determinista;
- sin callbacks del dominio;
- sin efectos del mundo;
- un máximo de un intent emitido por tick;
- IDs de nodo únicos;
- composites no vacíos;
- `MAX_TREE_DEPTH = 32`;
- `MAX_TREE_NODES = 512`;
- `MAX_CHILDREN = 64`;
- facts limitados a primitivos JSON finitos;
- comparadores `EQ/NEQ/GT/GTE/LT/LTE/IN`;
- `GT/GTE/LT/LTE` exigen valores numéricos;
- arrays contractuales estrictos;
- Proxies/estructuras hostiles deben cerrar con `ContractError`;
- `runtime.tick` satura en `Number.MAX_SAFE_INTEGER`;
- un `actionResult` sólo puede corresponder a la acción que estaba `RUNNING`;
- cada tick reevalúa el árbol desde la raíz y puede preemptar la acción anterior;
- `preemptedAction` sólo identifica una interrupción real: si la acción anterior recibió `SUCCESS` o `FAILURE` en ese tick, su finalización es normal y no se marca como preemptada;
- un runtime pertenece a una definición estructuralmente estable del árbol: cambiar topología, IDs o `intent` durante su vida está fuera de contrato y exige crear un runtime nuevo;
- `EQ/NEQ/IN` usan `Object.is` y por tanto distinguen `-0` de `0`; los comparadores ordenados usan semántica numérica normal.

## Fixtures

- `fixture_bt_guard` — prioridad hostil > sospechoso > patrulla.
- `fixture_bt_worker` — alarma > servicio > preparación.
- `fixture_bt_supervisor` — crisis > solicitud del jugador > inspección.

## Ejecutar

```bash
node tests.mjs
node tests-rev2.mjs
node stress.mjs 100000 1337
```

Suite histórica: 34 pruebas contractuales. REV2 añade 6 regresiones específicas de semántica de preempción.

Stress local verificado con seeds 1337, 1, 42, 999 y 20260925, 100.000 ticks por seed.

## Fuera de alcance

- NPC canónicos;
- pathfinding;
- combate resuelto;
- diálogos;
- memoria social;
- Utility AI;
- GOAP;
- HTN;
- integración con producción.

## Estado

`CANDIDATE_STATUS: REV2_EXTERNALLY_AUDITED_APTO_PARA_ITERAR`


## Auditoría externa REV2

HEAD exacto auditado:

`0d44c5289f189e21c85584706da37af4ffafd103`

Resultado:

- 34/34 suite histórica;
- 6/6 regresiones REV2;
- 27/27 casos independientes de preempción;
- 52/52 re-ataques adversariales generales;
- 500.000 ticks de verificación por propiedades;
- 0 regresiones nuevas.

Veredicto:

`BEHAVIOR_TREE_V01_REV2_APTO_PARA_ITERAR`

Snapshot inmutable:

`snapshot/npc-behavior-tree-v0.1-rev2-audited`
