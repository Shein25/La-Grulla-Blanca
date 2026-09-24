# Auditoría externa — Motor NPC Vivo v0.3.2

Auditar sólo la rama `experiment/motor-npc-v0.3-memory` del repositorio
`Shein25/La-Grulla-Blanca`. El commit base congelado debe ser exactamente
`460ffdf57b9a20ab837f406787207eccc83944ac`; verificar rama, HEAD y
ancestría antes de evaluar. Verificar que el diff desde ese commit contiene
únicamente archivos nuevos bajo
`experimentos/memoria/motor-npc-vivo-v0.3.2-decision/`.

Comprobar byte por byte las dependencias congeladas v0.3.0, v0.3.1, Utility
v0.1.1 y GOAP v0.2.2. Como mínimo, comparar los blobs `memory.mjs`
`9108779974baebc3ef81502392f9823c59a49c53`, `relation-deriver.mjs`
`aa0e450604efd0f0cf21488fe66f5d1746a5dd25`, `engine.mjs`
`8d567625be09a4272c33b939b9b1bd94b68f18e7`, `goal-selector.mjs`
`b4552439494395358fa8bd763e513448fcce9f13`, `goap.mjs`
`d2862199d5bbbddcca06d22c612362366eacbc60` y `actions.mjs`
`4ede8db5aa28797a0bc9162cd356494f3510cf56`.

Ejecutar `node tests.mjs` en v0.3.2 y `node stress.mjs 500 SEED` para las
cinco seeds `1337`, `1`, `42`, `999`, `20260924`. Repetir al menos una seed y
comparar resultado completo y digest. Auditar Golden A (investigar →
INVESTIGATE_ANOMALY → investigar_anomalia), Golden B (`PLAYER_HELPED_ME` →
ayudar_jugador → HELP_PLAYER → ir_jugador, ayudar_jugador) y Golden C
(`PLAYER_LIED` con `subject: 'superior'` → investigar). Revisar no fallback,
acción unmapped, `SEARCH_LIMIT`/`FRONTIER_LIMIT`, inputs hostiles y getters
sin ejecutar, coherencia context/world, inmutabilidad y determinismo.
Verificar que no se llama `rankGoals`, `selectGoal`, `decideAndPlan` ni Executor.

Regresiones obligatorias:

```text
v0.3.0: node tests.mjs; node stress.mjs 10000 1337
v0.3.1: node tests.mjs; node stress.mjs 1000 1337/1/42/999/20260924
Utility v0.1.1: node tests.mjs; node stress.mjs 10000 1337
GOAP v0.2.2: node tests.mjs; node stress.mjs 10000 1337;
             node dynamic-stress.mjs 5000 1337
```

Reportar conteos reales de PASS, exit codes, stress por seed, hallazgos y
deudas. Terminar el informe exactamente con una de estas líneas:

```text
V032_PIPELINE_APTO_PARA_ITERAR
V032_PIPELINE_REQUIERE_CORRECCIONES
V032_PIPELINE_FALLO_CONCEPTUAL
```
