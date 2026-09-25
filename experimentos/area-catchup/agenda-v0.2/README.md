# Area Catch-up v0.2: agenda y posición lógica

Laboratorio sintético e independiente. **Catch-up temporal v0.1** responde qué timers, meters y eventos cambiaron durante la dormancia. **Catch-up Agenda v0.2** responde dónde debería considerarse ubicado cada NPC y qué actividad debería estar realizando al reactivar el área. Esta rama no importa ni integra los otros laboratorios.

```js
import { resolveAgendaCatchUp } from './agenda-resolver.mjs';

const result = resolveAgendaCatchUp(state, catchUp);
// status: 'AGENDA_CATCH_UP_APPLIED'
// state.syncedTurn: catchUp.toTurn
```

El request contiene exactamente `{areaId, fromTurn, toTurn, elapsedTurns}`. Debe corresponder al snapshot: mismo `areaId`, `fromTurn === syncedTurn`, `toTurn > fromTurn` y `elapsedTurns === toTurn - fromTurn >= 1`. Todos los turns son enteros seguros no negativos.

Cada entidad contiene `id`, `logicalRoomId`, `currentActivity` y `agenda`. La agenda contiene `cycleLength`, `offset` y `slots`. Los slots `[start,end)` cubren exactamente `[0,cycleLength)` sin huecos ni solapamientos; sus IDs son únicos dentro de la agenda. El snapshot de entrada debe coincidir con el slot que determina `syncedTurn`. Cualquier contradicción se rechaza.

La fase en un turn absoluto es `(BigInt(turn) + BigInt(offset)) % BigInt(cycleLength)`. El slot que contiene la fase final determina `logicalRoomId` y `currentActivity`. **`logicalRoomId` es una posición lógica resumida de reactivación; no representa una trayectoria física simulada.** No se camina room por room, no se ejecutan actividades y no se reproducen transiciones.

`summary.entityUpdates` contiene sólo cambios visibles de room o actividad. `summary.cycleSummaries` contiene un registro para **cada** entidad, incluso sin cambio visible, con `fromSlotId`, `toSlotId`, `finalPhase` y `fullCyclesElapsed = floor(elapsedTurns / cycleLength)`. La división usa BigInt exacto antes de convertir a entero seguro. `summary.elapsedTurns` conserva la duración total. Así, volver al mismo slot tras muchos ciclos no se presenta como ausencia de tiempo transcurrido.

La salida ordena entidades por ID y slots por `start`, sin locale. Todos los objetos y arrays de salida son nuevos y desacoplados del input y de otras ejecuciones. La validación usa descriptores propios: rechaza accessors sin ejecutar getters, Symbols, campos extra, herencia, arrays con huecos o índices accessor y proxies que impiden inspección estructural.

## Complejidad

Validar y resolver cuesta **O(entidades + total de slots procesados)** respecto del estado. La canonicalización agrega `O(E log E + Σ Sᵢ log Sᵢ)` por ordenar entidades y los slots de cada agenda. Calcular la fase y los ciclos completos cuesta **O(1) respecto de la cantidad de turns o ciclos transcurridos** por entidad; los operandos BigInt tienen tamaño acotado por el rango de safe integers de entrada. No hay loops ni arrays proporcionales a `elapsedTurns` o `fullCyclesElapsed`.

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

El stress usa 128 NPC con 1–12 slots, períodos y offsets variados, 10.000 escenarios por seed, oráculo BigInt independiente, invariantes, determinismo y digest SHA-256. Los acumuladores grandes (`totalElapsedTurns`, `fullCyclesCollapsed`) se serializan como strings decimales.

## Fuera de alcance y futuras excepciones

No hay Pathfinder, Scheduler, Utility, GOAP, movimiento real, azar, combate, sueño, hambre ni efectos de actividades. Futuras versiones deberán decidir cómo interrumpir la agenda cuando haya un evento urgente, un NPC herido o muerto, un perseguidor entre áreas, un seguidor del jugador, una quest que cambie la rutina, un área bloqueada o una room inaccesible.
