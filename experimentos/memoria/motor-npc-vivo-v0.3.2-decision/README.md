# Motor NPC Vivo v0.3.2 — decisión desde memoria

Laboratorio sintético de integración:

```text
Memory v0.3.0 (recuerda)
  ↓
Relations v0.3.1 (deriva un snapshot social)
  ↓
Utility AI v0.1.1 (elige ACTION / INTENTION)
  ↓
mapping explícito Utility action → GOAP goal
  ↓
GOAP v0.2.2 (produce un plan lógico)
```

`decideFromMemory(npc, memory, currentTurn, utilityContext, world, plannerOptions = {})`
devuelve `status`, `relationDerivation`, `utilityDecision`, `mapping`, `goalId`,
`goal`, `relevance` y `plan`. Los cuatro motores se importan de sus versiones
congeladas. GOAP recibe directamente el objetivo que eligió Utility. No participa
`rankGoals()`, no se vuelve a decidir el objetivo y no hay fallback silencioso
cuando el objetivo elegido es imposible. No se llama al Executor ni se ejecuta
ninguna acción.

Los estados externos son `PLAN_READY` (`plan.status=PLAN_FOUND`),
`PLANNING_DEFERRED` (`SEARCH_LIMIT`, `FRONTIER_LIMIT` o `COST_OVERFLOW`),
`NO_PLAN` (`plan.status=NO_PLAN`) y `UTILITY_ACTION_UNMAPPED` (`goalId=null`,
`plan=null`). `hablar_jugador` carece por ahora de goal GOAP; no se inventa uno.
El plan encontrado incluye copias de `goal` y `relevance`, además de `goalId`
y `utilityAction`.

Cada llamada parte de `npc.relationPlayer` **original** y de la memoria actual.
Las relaciones derivadas sólo viven en un NPC temporal y nunca se guardan como
nueva base. Los inputs y los resultados no comparten estructuras mutables.
Memory ordena las entradas recordadas por su prioridad y Relations ordena las
contribuciones por clave, por lo que el orden de inserción de la memoria no
cambia el resultado completo.

## Semántica social

`kind` codifica la clase del evento y, en `PLAYER_*`, quién actuó. `subject`
representa la entidad, tema o referente del recuerdo; **no representa al
actor**. Un `PLAYER_LIED` con `subject: 'superior'` afecta la relación hacia el
jugador. La futura separación `actor` / `target` / `subject` para NPC↔NPC
queda fuera de alcance.

## Fronteras y coherencia

El integrador captura una vez, mediante descriptores propios de datos, los
siete campos superiores requeridos del NPC y los once del contexto. Rechaza
getters y prototipos no planos sin ejecutarlos. Relations valida la relación
base y Utility vuelve a validar el NPC temporal y el contexto completo.
El `world` se copia a un objeto plano con claves string ordenadas y valores
primitivos/null finitos; se rechazan accessors, símbolos, objetos, arrays,
funciones y números no finitos. También se capturan los límites del planner
mediante descriptores antes de llamar a GOAP.

Se exige coherencia estricta para estas equivalencias:

| Utility context | World |
| --- | --- |
| `playerPresent` | `playerPresent` |
| `playerRequestsHelp` | `playerNeedsHelp && !playerHelped` |
| `anomalyPresent` | `anomalyPresent && !anomalyInvestigated` |
| `awayFromPost` | `at !== 'puesto'` |
| `dutyImportance` | `dutyImportance` |
| `danger` | `danger` |
| `missionUrgency` | `urgency` |

No se infieren equivalencias para `playerRank`, `relevantKnowledge`,
`dutyMode` ni `superiorReachable`, porque no tienen correspondencia inequívoca.
En la traza pública, las acciones Utility indisponibles llevan `score: null`
y `raw: null` en vez de los centinelas internos `-Infinity`; `available:false`
y `reasonUnavailable` conservan la explicación y todos los números expuestos
son finitos.

## Ejecución

```bash
node tests.mjs
node stress.mjs 500 1337
node stress.mjs 500 1
node stress.mjs 500 42
node stress.mjs 500 999
node stress.mjs 500 20260924
```

El fixture `memory_flip` y los 16 NPC del stress son sintéticos, no canon.
GOAP sigue planificando hechos lógicos; `ir_jugador` no es pathfinding físico.
No hay Executor, scheduler, navegación, NPC↔NPC, propagación social, persistencia
definitiva ni integración de producción en esta capa.
