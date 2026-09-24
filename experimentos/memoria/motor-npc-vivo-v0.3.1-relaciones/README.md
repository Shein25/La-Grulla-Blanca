# Motor NPC Vivo v0.3.1 — relaciones derivadas

Laboratorio aislado en `experiment/motor-npc-v0.3-memory`. Esta capa reutiliza, sin modificarla, la memoria semántica congelada v0.3.0:

```text
Memory v0.3.0 — recallMemory(memory, currentTurn)
                     ↓ recuerdos activos validados
Relation Deriver v0.3.1 — deriveRelations(baseRelations, memory, currentTurn)
                     ↓
Snapshot derivado de relaciones + explicación de contribuciones e ignorados
```

No se conecta todavía con Utility AI ni con GOAP. No cambia objetivos, planes ni acciones. Los NPC del stress son ficticios y no son canon.

## API y contrato

```js
import { deriveRelations } from './relation-deriver.mjs';

const result = deriveRelations(baseRelations, memory, currentTurn);
// result = { relations, rawDeltas, contributions, ignoredMemories }
```

`baseRelations` debe ser un objeto plano con **exactamente** seis propiedades de datos propias: `afinidad`, `confianza`, `respeto`, `deuda`, `temor`, `rivalidad`. Cada valor debe ser un `number` finito en `0..100`. Se rechazan extras, faltantes, herencia en vez de propiedad propia y accessors, incluidos los no enumerables. La captura se hace mediante descriptores; los getters no se ejecutan. Se calcula sólo a partir de ese snapshot. `memory` y `currentTurn` conservan la validación, reloj monotónico, expiración y copia segura de `recallMemory()`.

| Recuerdo activo | Condición | Deltas base |
|---|---|---|
| `PLAYER_HELPED_ME` | `value === true` | afinidad +12, confianza +10, deuda +8 |
| `PLAYER_LIED` | `value === true` | confianza −18, respeto −6, rivalidad +12 |

Cada delta se multiplica por `(importance / 100) * (confidence / 100)`. `count`, `firstTurn` y `lastTurn` no multiplican el efecto. No hay decay ni aleatoriedad. Los resultados conservan decimales finitos, sin redondeo artificial. Los recuerdos activos sin regla social y los dos kinds anteriores con `value !== true` figuran en `ignoredMemories` con `NO_SOCIAL_RULE` o `VALUE_NOT_TRUE`. Los expirados no llegan a la capa: `recallMemory()` los excluye, por lo que no aparecen en ninguna de las dos listas.

Las contribuciones se ordenan por `memoryKey` para que invertir las entradas no cambie siquiera el orden de las sumas de coma flotante. Se suman todos los `rawDeltas` y **sólo al final** se aplica el clamp `0..100`. `relations` contiene el snapshot final; `rawDeltas`, los totales previos al clamp; `contributions`, el factor y seis deltas de cada recuerdo aplicado; `ignoredMemories`, las razones de descarte de recuerdos activos.

Las relaciones base y la memoria no se modifican. Llamar repetidamente con las mismas entradas da el mismo resultado. **Las relaciones derivadas no se escriben como nueva base automáticamente** y no existe acumulación por tick. Si una integración futura reutilizase deliberadamente `result.relations` como `baseRelations`, estaría creando otro comportamiento fuera de este contrato.

## Comandos

Desde esta carpeta:

```bash
node tests.mjs
node stress.mjs 1000 1337
node stress.mjs 1000 1
node stress.mjs 1000 42
node stress.mjs 1000 999
node stress.mjs 1000 20260924
```

El stress usa 32 NPC ficticios por 1.000 rondas. Para cada seed repite toda la simulación y compara el resultado completo mediante un digest reproducible. Comprueba relaciones finitas y acotadas, inputs intactos y ausencia de excepciones.

## Observaciones heredadas de REV1 v0.3.0

1. Un recuerdo recién registrado puede ser expulsado inmediatamente si es el más débil según la política de retención; es comportamiento esperado.
2. `recordMemory()` purga recuerdos expirados de **cualquier** `key` al avanzar el clock, antes de insertar el evento nuevo; también es comportamiento esperado.

No hay memoria NPC↔NPC, rumores, scheduler, persistencia final ni pathfinding en esta capa.
