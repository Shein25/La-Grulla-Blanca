# Auditoría externa adversarial — Area Activation / NPC Dormancy v0.1

Auditar la rama `experiment/area-activation-v0.1` en
`Shein25/La-Grulla-Blanca`. Confirmar HEAD exacto, padre/ancestría desde
`main@5812deb59cd1c133383b9af973486a702a26daf4` y diff limitado a
archivos nuevos bajo `experimentos/area-activation/dormancy-v0.1/`.
Confirmar que las ramas Memory, Pathfinder y Scheduler y las PR #4, #5 y #6
no se modificaron. La PR de este laboratorio debe estar open/draft/no merged.

Ejecutar `node tests.mjs` y `node stress.mjs SEED 20000` para seeds
`1337`, `1`, `42`, `999`, `20260924`. Repetir una seed y comparar métricas y
digest. Crear un oracle independiente que conserve `activeArea`,
`lastSimulatedTurn` por área y global turn; contrastar cada catch-up y
transición. Hacer fuzzing de configs, clocks, permutaciones y secuencias de
áreas sintéticas.

Auditar initial activation, switch, reentry, only-one-active invariant,
elapsed exacto, gran salto sin simulación por turn dormido, áreas no
involucradas intactas, `ALREADY_ACTIVE` sin catch-up, determinismo,
inmutabilidad y contrato transaccional de `result.state`.

Atacar config y state con getters, setter-only, Proxies (`get`,
`getPrototypeOf`, `ownKeys`, `getOwnPropertyDescriptor`), campos heredados,
símbolos, holes, índices accessor, duplicados, clocks futuros, `NaN`,
`Infinity`, floats y enteros fuera de rango. Comprobar que ningún getter se
ejecuta y que no se importa Scheduler, Memory, Relations, Utility, GOAP,
Pathfinder ni Executor.

Reportar tests, exits, stress por seed, digests, hallazgos y deudas. Terminar
el informe exactamente con una de estas líneas:

```text
AREA_DORMANCY_V01_APTO_PARA_ITERAR
AREA_DORMANCY_V01_REQUIERE_CORRECCIONES
AREA_DORMANCY_V01_FALLO_CONCEPTUAL
```
