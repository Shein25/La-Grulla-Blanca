# NPC Execution + Replanning Coordinator v0.1

Laboratorio sintético para coordinar la ejecución simbólica de un objetivo **ya elegido**. Reutiliza [Executor GOAP v0.2.2](../../goap/motor-npc-vivo-v0.2-goap/executor.mjs) y `planGOAP` del `main` congelado. Executor verifica y ejecuta **un paso**; el coordinador decide si continúa, replantea **el mismo goal**, queda pendiente o devuelve `INTENT_REEVALUATION_REQUIRED` para que una capa superior elija una nueva intención. No importa Utility ni `decideAndPlan`.

```js
import { createExecutionSession, advanceExecutionSession } from './execution-session.mjs';

let session = createExecutionSession({
  goalId: 'HELP_PLAYER', goal: { playerHelped: true },
  relevance: { playerPresent: true, playerNeedsHelp: true },
  plan: ['ir_a', 'usar_a']
});

const result = advanceExecutionSession(session, currentWorld, actions, plannerOptions);
session = result.session; // null cuando termina el goal o debe reevaluarse intención
```

Cada llamada recibe el **world actual** y hace como máximo una acción o un intento de replanning, nunca ambos. Si una precondition falla o una acción desaparece, el Executor pide replan. Si `relevance` todavía coincide, `planGOAP` busca un plan para el mismo goal y devuelve `REPLAN_READY`; el primer paso nuevo espera a la próxima llamada. Si relevance murió, se devuelve `INTENT_REEVALUATION_REQUIRED` sin llamar Planner. Si el goal ya fue satisfecho por un cambio externo, se devuelve `GOAL_REACHED` sin acción.

`NO_PLAN_FOR_GOAL` indica que el mismo goal sigue vigente pero no existe ruta conocida. `PLANNING_DEFERRED` conserva por separado `SEARCH_LIMIT`, `FRONTIER_LIMIT` o `COST_OVERFLOW`. Ambos dejan la session en `REPLAN_PENDING` con `plan: null`; una llamada posterior reevalúa primero goal y relevance y luego puede reintentar Planner. El plan viejo nunca queda activo tras fallar. No hay fallback a otro objetivo.

Los resultados incluyen `session`, `world`, `executed`, `reason`, `goalObsolete`, `replan` y `counters`. `stepCount` cuenta acciones realmente aplicadas, incluso la que alcanza el goal; `replanCount` cuenta intentos reales. `counters` conserva ambos números cuando `session` pasa a `null`. Los incrementos que excederían `Number.MAX_SAFE_INTEGER` arrojan `RangeError` sin modificar entradas.

## Frontera de confianza

`session`, goal, relevance, plan, world y plannerOptions se capturan desde descriptores propios. Se rechazan accessors sin ejecutar getters, herencia, Symbols, campos extra donde el esquema es cerrado, arrays con huecos o índices accessor y proxies que bloquean la inspección estructural. Los facts GOAP admiten valores `null`, boolean, string o número finito; `{}` es válido. Las salidas están desacopladas de las entradas y de otras llamadas.

`actions` es un **catálogo interno trusted del motor**, no input de jugador. El coordinador no replica toda la validación de acciones: Executor usa el catálogo para el paso actual y Planner lo valida cuando replanifica. Ninguna función del coordinador modifica el catálogo. El Planner ordena acciones internamente para que su resultado no dependa del orden recibido.

`plannerOptions` sólo admite `maxExpansions` entero >= 0 y `maxFrontier` entero >= 1; ambos son opcionales. Esta validación sigue el contrato del GOAP existente.

## Ejecutar

```bash
npm test
npm run stress -- 1337
npm run stress -- 1
npm run stress -- 42
npm run stress -- 999
npm run stress -- 20260924
npm run stress -- 1337
```

El stress ejecuta 10.000 episodios por seed. El **harness** llama al coordinador en ticks sucesivos y altera el mundo **entre** llamadas: cierra rutas, abre alternativas, satisface el goal o invalida relevance. Un oracle BFS independiente comprueba rutas alternativas en el catálogo pequeño. El coordinador no contiene un loop autónomo de ejecución.

## Alcance futuro

Esta v0.1 usa acciones GOAP simbólicas e instantáneas (`preconditions`/`effects`). Un Executor de producción deberá distinguir inicio, ejecución en curso, finalización y fallo de acciones con duración. Scheduler, Utility, Memory, Pathfinder físico, múltiples NPC, rollback y persistencia quedan fuera de este laboratorio.
