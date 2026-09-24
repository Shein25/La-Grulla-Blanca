# NPC Scheduler / ciclo de reevaluación v0.1

El Scheduler sólo responde **qué NPC necesita reevaluarse ahora**. No decide
acciones, no planifica, no navega y no ejecuta. Emite solicitudes de dispatch
que una integración futura podrá entregar a Utility AI. Este laboratorio no
importa Utility AI, GOAP, Memory, Relations, Pathfinder ni Executor; todos sus
NPC son sintéticos.

```text
eventos + cadencia periódica + cooldown + presupuesto
                         ↓
             dispatch de reevaluación
```

## API y tiempo

`createSchedulerState(configs)` crea `{ version:1, clock:null, npcs }` en orden
canónico por `id`. Cada config contiene `id`, `interval >= 1`, `minGap >= 0`
y `firstPeriodicTurn >= 0`; los tres números son enteros seguros.

`tickScheduler(state, currentTurn, events = [], options = {})` devuelve
`{ status, state, dispatches, eligibleCount, deferredCount }`. `currentTurn` es
un entero seguro no negativo. Tras el primer tick debe ser **estrictamente
mayor** que `state.clock`. Se entregan todos los eventos de un turno juntos:
cada evento contiene sólo `{ npcId, kind }`, y recibe `currentTurn` como fecha.
No se usa reloj real ni timers JS.

`eligibleCount` cuenta NPC con razones pendientes que pueden despacharse en
ese turno, antes del presupuesto. `deferredCount` cuenta todos los NPC que
siguen con razones pendientes después del tick, tanto por cooldown como por
presupuesto. `BUDGET_EXHAUSTED` significa que quedaron NPC **elegibles** sin
despachar por `maxDispatches`; un NPC retenido sólo por cooldown mantiene el
estado `DISPATCH_COMPLETE`.

## Razones y cadencia

Los eventos externos admitidos son `PLAN_INVALIDATED`, `ACTION_FINISHED`,
`MEMORY_CHANGED` y `WORLD_CHANGED`. `PERIODIC` sólo lo genera el scheduler.
Las prioridades respectivas son `100`, `80`, `60`, `50`, `10`. Cada razón
pendiente conserva `firstTurn`, `lastTurn` y `count`. Repeticiones de un mismo
kind se acumulan; varias razones del mismo NPC producen como máximo un
dispatch por tick.

Al saltar turns, los vencimientos periódicos se representan con una sola
razón. Por ejemplo, `nextPeriodicTurn=10`, `interval=5`, tick `27` produce
`PERIODIC { firstTurn:10, lastTurn:25, count:4 }` y deja el siguiente
vencimiento en `30`. No se generan cuatro dispatches ni una tormenta de
backlog.

Después de un dispatch normal en `T`, otro normal requiere
`currentTurn >= T + minGap`. `PLAN_INVALIDATED` es la única razón que puede
saltar este cooldown; se incluyen además todas las razones que ya estaban
pendientes. El scheduler no ejecuta IA aunque el evento sea urgente.

## Budget y orden

`options.maxDispatches` es un entero seguro `>= 1` (default `64`). El orden
para elegir NPC es:

1. quienes tienen `PLAN_INVALIDATED`;
2. mayor prioridad de razón dominante;
3. `firstTurn` más antiguo entre todas sus razones pendientes;
4. `npcId` ascendente mediante comparación JS.

Dentro de cada dispatch, las razones siguen prioridad descendente y después
el orden fijo `REASON_ORDER`. Los NPC no elegidos conservan sus razones, fechas
y counts. Con carga finita y ticks posteriores suficientes terminan por
despacharse; no se promete ausencia de starvation frente a una secuencia
infinita de urgencias o presupuesto insuficiente.

## Frontera y pureza

Configs, state, arrays, eventos y opciones se capturan mediante descriptores
de propiedades propias. Se rechazan accessors sin ejecutar getters, campos
heredados, prototipos no planos, holes, símbolos y números inválidos. Los
turns, intervalos y counts deben ser enteros seguros; el overflow de count o
`nextPeriodicTurn` lanza `RangeError` explícito. Ni los inputs ni los
resultados anteriores se modifican.

## Verificación

```bash
node tests.mjs
node stress.mjs 1337 5000
node stress.mjs 1 5000
node stress.mjs 42 5000
node stress.mjs 999 5000
node stress.mjs 20260924 5000
```

El stress usa 64 NPC inventados, saltos de clock, bursts, los cuatro eventos,
períodos, cooldowns y budgets variables. `coalescedEvents` cuenta eventos
externos adicionales absorbidos dentro del mismo dispatch o pendiente de un
NPC. `coalescingRatio = dispatches / (events + periodicOccurrences)` mide la
fracción de reevaluaciones emitidas frente a las ocurrencias que pudieron
haberlas provocado. El workload deliberadamente satura el presupuesto para
probar la conservación de pendientes.

La denominación «ciclo de vida» significa aquí `quiet → pending → eligible →
dispatched → cooldown`. No implementa horarios, rutinas diarias, save/load,
threads ni integración de producción.
