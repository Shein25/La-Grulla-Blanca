# Pathfinder de Rooms v0.1

Laboratorio **independiente** de navegación física entre rooms sintéticas.

```text
Utility AI: decide QUÉ quiere hacer el NPC
GOAP: decide QUÉ pasos lógicos necesita (por ejemplo, "ir_jugador")
Pathfinder: decide POR QUÉ ROOMS desplazarse para ese paso
Executor: en una futura iteración ejecutará acciones
```

Este módulo no importa Utility AI ni GOAP, no elige metas o comportamientos y
no ejecuta movimientos. Tampoco usa las 329 rooms reales, NPC canónicos,
topología, gates ni misiones de producción.

## API

`findRoute(graph, startRoomId, goalRoomId, options = {})` devuelve:

```js
{
  status, startRoomId, goalRoomId,
  rooms, // IDs ordenados desde start hasta goal si hay ruta
  steps, // { from, direction, to } por movimiento
  distance, // cantidad de steps, o null si no hay ruta concluida
  visitedCount // rooms extraídas de la cola, incluida la de inicio
}
```

`validateGraph(graph)` valida el contrato y retorna `true` o lanza
`TypeError`. `DIRECTION_ORDER` exporta el orden fijo `norte`, `este`, `sur`,
`oeste`, `arriba`, `abajo`.

El grafo es `{ version: 1, rooms: [{ id, exits }] }`. Cada room contiene
exactamente `id` y `exits`; cada `exits` contiene las seis direcciones, con
valor `null` o ID de una room existente. Las conexiones son **dirigidas**:
una salida `A/norte → B` no implica `B/sur → A`. `arriba` y `abajo` son
direcciones normales del grafo; no se infiere ningún piso ni coordenada.

## Búsqueda

BFS garantiza el mínimo número de movimientos porque todos cuestan uno.
Explora vecinos en `DIRECTION_ORDER`, por lo que ese orden resuelve empates
entre rutas mínimas sin depender del orden de propiedades o de la lista de
rooms. No hay A*, Dijkstra, heurísticas ni costes variables.

| Estado | Interpretación |
| --- | --- |
| `ROUTE_FOUND` | Ruta no vacía; `distance === steps.length`. |
| `ALREADY_THERE` | Inicio y destino coinciden; una room, cero pasos. |
| `NO_ROUTE` | Se agotó todo el componente alcanzable permitido. |
| `SEARCH_LIMIT` | Quedaban rooms por explorar al llegar a `maxVisited`. |

`options.maxVisited` es un entero seguro `>= 1` (default `10000`). Cuenta
rooms extraídas de la cola. Si se agota la cola justo al alcanzar el límite,
el resultado es `NO_ROUTE`; si quedan rooms pendientes, es `SEARCH_LIMIT`.

`options.blockedExits` admite entradas `{ from, direction }` para una sola
búsqueda. Bloquear una salida impide recorrerla, sin modificar el grafo.
No modela llaves, puertas, permisos, facciones o quests.

## Captura segura

Grafo, rooms, exits, opciones y bloqueos se inspeccionan mediante descriptores
de propiedades propias y se copian a snapshots internos. Se rechazan
accessors, holes, símbolos, propiedades heredadas usadas como campos,
prototipos no planos, IDs duplicados o targets inexistentes. Los getters no
se ejecutan. Los resultados no comparten estructuras mutables con los inputs.

## Verificación

```bash
node tests.mjs
node stress.mjs 1337 600
node stress.mjs 1 600
node stress.mjs 42 600
node stress.mjs 999 600
node stress.mjs 20260924 600
```

`fixtures.mjs` contiene trece rooms de laboratorio. El stress crea 160 rooms
sintéticas por seed. Los tests incluyen un oracle independiente por relajación
de distancias para verificar rutas mínimas en todos los pares de dos grafos.
