# Autonomous NPC Loop v0.1

Laboratorio sintético de NPC dentro de un área activa. Integra cinco módulos runtime congelados con Utility AI y GOAP ya presentes en `main`. No conecta personajes, rooms, producción, dormancy ni agenda.

```text
                 GLOBAL TURN
                      │
                      ▼
                  Scheduler
                      │
             NPC despachado?
                 /        \
               NO          SÍ
               │            │
          sin cerebro   ¿session?
                         /     \
                       NO       SÍ
                       │         │
                    Memory    Executor
                       ↓         +
                   Relations   Replan
                       ↓
                    Utility
                       ↓
                     GOAP
                       ↓
                  crear session
```

**Scheduler** decide cuándo piensa o avanza cada NPC. **Decision Pipeline** deriva relaciones temporales desde Memory, selecciona la intención con Utility y crea un plan GOAP. **Execution Session** avanza o replantea ese plan frente a cambios. **Autonomous Loop** orquesta esas responsabilidades sin fusionarlas: cada dispatch atraviesa exactamente uno de los caminos `DECISION` o `EXECUTION`.

## API

```js
import { createAutonomousLoopState, tickAutonomousLoop } from './autonomous-loop.mjs';

const state = createAutonomousLoopState({ schedulerConfigs, npcs });
const result = tickAutonomousLoop(state, currentTurn, {
  observations: [{ npcId, world, utilityContext, memoryEvents }],
  schedulerEvents: [{ npcId, kind: 'PLAN_INVALIDATED' }],
}, {
  scheduler: { maxDispatches: 5 },
  planner: { maxExpansions: 1000, maxFrontier: 1000 },
});
```

`npcs` contiene `{ npc, world, utilityContext }` por NPC; los IDs deben coincidir exactamente con `schedulerConfigs`. La creación inicia Memory vacío y `executionSession: null`. `state.clock` y `scheduler.clock` arrancan en `null` y luego coinciden en cada tick. El turno debe ser entero seguro, no negativo y estrictamente creciente.

Las observations reemplazan world/context completos para los NPC indicados. El loop compara los facts con `Object.is`, conserva `-0`, aplica memory events del turno en orden de key y genera `WORLD_CHANGED` y `MEMORY_CHANGED` sólo cuando corresponde. Los eventos externos se entregan intactos al Scheduler para su coalescencia. Los NPC no despachados conservan su session y behaviorState aun si recibieron una observation.

En `DECISION`, `PLAN_READY` crea una session, sin ejecutar el primer paso. `UTILITY_ACTION_UNMAPPED`, `NO_PLAN` y `PLANNING_DEFERRED` no crean session. `behaviorState` registra sólo decisiones Utility; `relationPlayer` base nunca se reemplaza por relaciones derivadas. En `EXECUTION`, GOAP puede aplicar hasta una acción, alcanzar la meta, replanificar o pedir reevaluación. La nueva decisión, si procede, espera otro dispatch. Los effects GOAP actualizan el world simbólico autoritativo y se sincronizan los campos espejo de context para conservar coherencia.

La captura defensiva rechaza accessors, Symbols, herencia, huecos, propiedades extra en esquemas exactos y proxies que impiden inspección. Los motores congelados siguen validando sus propios contratos. El tick es puro respecto de state, input y options; la salida es desacoplada.

## Ejecutar

Desde este directorio:

```bash
npm test
npm run stress
```

También funcionan `node tests.mjs` y `node stress.mjs`. El test runner nativo de Node se usa dentro de `tests.mjs`; invocar el archivo directamente evita la necesidad de crear un subproceso por archivo en entornos restringidos. La suite cubre los Golden A–R, validación, entradas hostiles, pureza y determinismo. El stress ejecuta 3.000 turnos globales con 16 NPC para cada seed `1337`, `1`, `42`, `999` y `20260924`, repite `1337` y exige un digest idéntico.

## Alcance y límites

Los facts GOAP son simbólicos y las acciones instantáneas. La continuidad depende de dispatches futuros del Scheduler, normalmente `PERIODIC` con `interval: 1` en fixtures que necesitan avanzar cada turno. El loop no inventa eventos por plan creado, replan listo o acción aplicada. No modela duración, navegación por rooms, activación de áreas, rutinas, HTN ni Behavior Trees. Las planner options son globales por tick.
