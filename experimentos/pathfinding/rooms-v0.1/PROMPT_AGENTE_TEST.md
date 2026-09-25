# Auditoría externa adversarial — Pathfinder de Rooms v0.1

Auditar `Shein25/La-Grulla-Blanca` en la rama
`experiment/pathfinding-rooms-v0.1`. Verificar HEAD exacto del commit candidato,
padre/ancestría desde `main@5812deb59cd1c133383b9af973486a702a26daf4`
y que el diff desde esa base incluya **sólo archivos nuevos** bajo
`experimentos/pathfinding/rooms-v0.1/`. Confirmar que no se modificó la rama
`experiment/motor-npc-v0.3-memory` ni la PR #4, y que la PR de este experimento
permanece open/draft/no merged.

Ejecutar `node tests.mjs` y `node stress.mjs SEED 600` con seeds `1337`, `1`,
`42`, `999`, `20260924`. Repetir una seed y comparar métricas y digest.
Comprobar independently shortest path, el desempate exacto por dirección,
ciclos, conexiones unidireccionales, `arriba`/`abajo`, blockedExits,
`SEARCH_LIMIT` distinto de `NO_ROUTE`, `ALREADY_THERE`, inmutabilidad y que
ningún resultado ejecute movimientos ni seleccione objetivos.

Hacer fuzzing independiente sobre grafos sintéticos de topologías y tamaños
distintos. Comparar distancias con un oracle que no comparta BFS, cola ni
helpers del código de producción. Validar cada step contra el grafo y los
bloqueos, y verificar que nunca aparezcan rooms repetidas en una ruta.

Atacar la frontera con getters, setter-only, Proxy (`get`, `getPrototypeOf`,
`ownKeys`, `getOwnPropertyDescriptor`), índices accessor de arrays, holes,
campos heredados, símbolos, targets inválidos, duplicados, `NaN`, `Infinity`,
`undefined` y límites extremos. Verificar que los getters nunca se ejecutan y
que inputs y ejecuciones posteriores permanecen intactos tras mutar outputs.

Reportar número real de tests, exits, stress y digests, hallazgos y deudas.
Terminar el informe exactamente con una de estas líneas:

```text
PATHFINDING_V01_APTO_PARA_ITERAR
PATHFINDING_V01_REQUIERE_CORRECCIONES
PATHFINDING_V01_FALLO_CONCEPTUAL
```
