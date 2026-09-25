# Area Catch-up v0.3: overrides de agenda

Laboratorio sintético e independiente. **Agenda v0.2** determina la rutina base; **Overrides v0.3** puede reemplazarla temporalmente. Si no hay override activo, gana la agenda. Si hay varios activos, gana `priority` mayor; en empate, `startTurn` más reciente; en otro empate, `id` lexicográficamente menor. `kind` es sólo metadata y no activa comportamiento especial. Esta rama no importa v0.2 ni otros laboratorios.

```text
turn 100: agenda → room_library / STUDY
turn 120: empieza medical → room_infirmary / RECOVER
turn 500: termina medical
jugador vuelve en 300 → room_infirmary / RECOVER
jugador vuelve en 700 → agenda correspondiente al turn 700
```

No se simulan los 600 turns intermedios. `logicalRoomId` sigue siendo una **posición lógica resumida** al reactivar el área, no movimiento físico ni una ruta.

## API y contrato

```js
import { resolveOverrideCatchUp } from './override-resolver.mjs';
const result = resolveOverrideCatchUp(state, catchUp);
// status: 'OVERRIDE_CATCH_UP_APPLIED'
```

El estado contiene exactamente `version: 1`, `areaId`, `syncedTurn` y `entities`. Cada entidad contiene `id`, `logicalRoomId`, `currentActivity`, `currentSourceType`, `currentSourceId`, `agenda` y `overrides`. La agenda mantiene `cycleLength`, `offset` y slots `[start,end)` que cubren exactamente el ciclo. Cada override contiene `id`, `kind`, `priority`, `startTurn`, `endTurn`, `roomId` y `activity`. `endTurn: null` significa duración indefinida. Los strings obligatorios no pueden estar vacíos ni contener sólo espacios.

`currentSourceType` es `AGENDA` o `OVERRIDE`. `currentSourceId` identifica el slot o override ganador en `syncedTurn`. Antes de resolver, se comprueba que source, room y actividad del snapshot coincidan con la agenda y las prioridades en ese turn. Un override finito con `endTurn <= syncedTurn` es stale y se rechaza.

El request contiene exactamente `{areaId, fromTurn, toTurn, elapsedTurns}`. Debe satisfacer `areaId === state.areaId`, `fromTurn === syncedTurn`, `toTurn > fromTurn` y `elapsedTurns === toTurn - fromTurn >= 1`; los turns son enteros seguros no negativos.

Un override está activo en `[startTurn,endTurn)`, con `endTurn: null` sin límite. En el turn final se elige el ganador directamente. Los finitos con `endTurn <= toTurn` se eliminan y aparecen en `summary.expiredOverrides`, incluso si estuvieron sombreados por otro. Los futuros y los activos al final permanecen. No se construye historial de ganadores, boundaries o actividades.

`summary.entityUpdates` contiene entidades cuyo room, actividad o source cambió; incluye `visibleChanged` y `sourceChanged` por separado. Por eso un override que muestra la misma room y actividad que la agenda sigue registrando el cambio de source. `summary.entitySummaries` contiene un registro por entidad, aunque no cambie, con slot base, ganador, source final, overrides restantes y `fullCyclesElapsed = floor(elapsedTurns / cycleLength)` calculado con BigInt. Los expirados se ordenan por `endTurn`, `entityId`, `overrideId`. Entidades y slots se canonicalizan por ID y `start`; los overrides persistentes por `startTurn`, `priority` descendente e ID. No se usa locale.

## Seguridad y complejidad

La entrada se captura por descriptores propios antes de resolver. Se rechazan accessors sin ejecutar getters, herencia, Symbols, campos extra, arrays con huecos o índices accessor y proxies que bloquean inspección estructural. Un proxy cuyo único trap es `get` puede pasar porque el resolver no usa `get` para leer la entrada; ese trap no se ejecuta. Todos los objetos y arrays de salida están desacoplados de las entradas y de otras ejecuciones.

La validación y selección recorren **O(entidades + slots + overrides)** registros. Canonicalizar añade `O(E log E + Σ Sᵢ log Sᵢ + Σ Oᵢ log Oᵢ + X log X)` por ordenar entidades, slots, overrides persistentes y expirados (`X`). La fase `(turn + offset) % cycleLength` y `fullCyclesElapsed` usan BigInt para evitar overflow y cuestan **O(1) respecto de turns o ciclos transcurridos por entidad**, con tamaño de operandos acotado por los safe integers de entrada. No hay loops ni arrays proporcionales a `elapsedTurns` o `fullCyclesElapsed`.

## Verificación

```bash
npm test
npm run stress -- 1337
npm run stress -- 1
npm run stress -- 42
npm run stress -- 999
npm run stress -- 20260924
npm run stress -- 1337
```

El stress genera 128 NPC, 1–12 slots y 0–12 overrides por NPC, con activos, futuros, finitos, indefinidos, solapamientos, prioridades y empates. Ejecuta 10.000 escenarios por seed y compara con un oracle BigInt independiente. `totalElapsedTurns` y `fullCyclesCollapsed` usan acumuladores BigInt serializados en decimal.

## Fuera de alcance

No se ejecutan actividades ni efectos de overrides; no hay salud, quests, alarmas, muerte, Pathfinder, Scheduler, integración con Area Activation ni creación dinámica de overrides. `kind` no codifica semántica de juego en esta versión.
