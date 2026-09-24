# Auditoría externa — Autonomous NPC Loop v0.1

Auditá el PR draft contra `main@5812deb59cd1c133383b9af973486a702a26daf4`, sin modificar código ni hacer merge. Reportá HEAD, base, parent y commits. Confirmá que el diff contiene exactamente 13 archivos agregados (los cinco runtime congelados y los ocho del laboratorio), cero archivos existentes modificados y ningún cambio en `experimentos/README.md`.

Verificá blobs exactos de los diez módulos runtime: Memory `9108779974baebc3ef81502392f9823c59a49c53`, Relations `aa0e450604efd0f0cf21488fe66f5d1746a5dd25`, Decision Pipeline `b17fbb90c5e95de603abb25ce996c9187a45383a`, Scheduler `71907d437008804cb0d289bfdc4412e6c7059cc1`, Execution Session `5caa006c0f2c20b177a077c71ad7f5484e254225`; y los cinco presentes en main: Utility engine `8d567625be09a4272c33b939b9b1bd94b68f18e7`, GOAP goal-selector `b4552439494395358fa8bd763e513448fcce9f13`, GOAP actions `4ede8db5aa28797a0bc9162cd356494f3510cf56`, GOAP executor `287b5b48c30c8b7dbaa0aae34cd1433f889695f2`, GOAP planner `d2862199d5bbbddcca06d22c612362366eacbc60`.

Ejecutá 101+ tests y confirmá Golden A–R. Ejecutá stress con seeds `1337`, `1`, `42`, `999` y `20260924`, 3.000 turnos y 16 NPC por seed; repetí `1337` y compará digest exacto. Auditá Scheduler como única puerta cerebral, Decision/Execution mutuamente excluyentes, cero Utility durante session activa, cero acciones al crear plan, máximo una acción por dispatch, base relations nunca persistidas, behaviorState sólo en nuevas decisiones, cadena Memory → Relations → Utility, world changes, presupuesto Scheduler, entradas hostiles, determinismo e inmutabilidad. Revisá métricas críticas y limitaciones conocidas.

Emití un único veredicto exacto, con evidencia:

```text
NPC_AUTONOMOUS_LOOP_V01_APTO_PARA_ITERAR
NPC_AUTONOMOUS_LOOP_V01_REQUIERE_CORRECCIONES
NPC_AUTONOMOUS_LOOP_V01_FALLO_CONCEPTUAL
```
