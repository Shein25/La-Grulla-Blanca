# Auditoría externa adversarial — NPC Scheduler v0.1

Auditar exclusivamente `Shein25/La-Grulla-Blanca` en
`experiment/npc-scheduler-v0.1`. Verificar HEAD exacto del candidato, su
ancestría desde `main@5812deb59cd1c133383b9af973486a702a26daf4` y que
el diff contiene sólo archivos nuevos en
`experimentos/scheduler/npc-lifecycle-v0.1/`. Confirmar que las ramas Memory
y Pathfinder, PR #4 y PR #5 no fueron modificadas. La PR del Scheduler debe
seguir open/draft/no merged.

Ejecutar la suite real `node tests.mjs` y cinco stress runs
`node stress.mjs SEED 5000` para `1337`, `1`, `42`, `999`, `20260924`. Repetir
una seed y comparar todas las métricas y el digest.

Auditar mediante casos independientes y fuzzing: coalescing de eventos y
períodos, saltos de clock, cooldown, único bypass urgente, budget y pendientes
conservados, orden entre NPC, fairness con carga finita, clock estrictamente
monotónico, overflow de count y nextPeriodicTurn, determinismo del orden de
eventos/configs, inmutabilidad y reducción real de dispatches frente a
eventos + períodos.

Atacar configs, state, events y options con getters, setter-only, Proxies con
traps `get`, `getPrototypeOf`, `ownKeys` y `getOwnPropertyDescriptor`,
propiedades heredadas, símbolos, holes, índices accessor, enteros inválidos,
`NaN`, `Infinity`, duplicados, clocks futuros e IDs inexistentes. Comprobar
que ningún getter se ejecuta y que no se llama Utility AI, GOAP, Memory,
Relations, Pathfinder, Executor ni timers de tiempo real.

Reportar conteos y exit codes reales, digests, hallazgos y deudas. Terminar
el informe exactamente con una de estas líneas:

```text
SCHEDULER_V01_APTO_PARA_ITERAR
SCHEDULER_V01_REQUIERE_CORRECCIONES
SCHEDULER_V01_FALLO_CONCEPTUAL
```
