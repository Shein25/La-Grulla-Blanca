# Auditoría externa: NPC Execution + Replanning Coordinator v0.1

Auditá sólo `experiment/npc-executor-replanning-v0.1` contra `main@5812deb59cd1c133383b9af973486a702a26daf4`. No hagas merge ni modifiques otros PR.

1. Informá HEAD, padre, base y ancestry. Comprobá `git hash-object` de `executor.mjs` = `287b5b48c30c8b7dbaa0aae34cd1433f889695f2` y `goap.mjs` = `d2862199d5bbbddcca06d22c612362366eacbc60`. Verificá diff aislado de ocho archivos nuevos y status limpio.
2. Ejecutá `npm test`; auditá Golden A–L, cambio externo del world entre llamadas, plan vacío, acción desaparecida, precondition invalidada, goal satisfecho externamente y relevance obsoleta.
3. Ejecutá stress con seeds `1337`, `1`, `42`, `999`, `20260924`; repetí `1337` y exigí digest idéntico. Informá todas las métricas, sobre todo `actionsExecutedDuringReplan = 0` y `obsoleteGoalActionsExecuted = 0`.
4. Confirmá máximo una acción por llamada, cero acciones en `REPLAN_READY`, replan del **mismo goal**, ausencia de imports Utility/controller/`decideAndPlan`, y que `REPLAN_PENDING` nunca llama Executor.
5. Diferenciá `NO_PLAN_FOR_GOAL` de `PLANNING_DEFERRED` para `SEARCH_LIMIT`, `FRONTIER_LIMIT` y `COST_OVERFLOW`. Revisá retry pendiente, contadores y overflow.
6. Revisá oracle BFS independiente, perturbaciones externas, acciones stale descartadas, inputs hostiles (getters, proxies, holes, Symbols, herencia), determinismo e inmutabilidad. Inspeccioná ausencia de `executeWholePlan` y de loops autónomos en el coordinador.

Emití evidencia concreta y **un solo veredicto exacto**:

```text
NPC_EXEC_REPLAN_V01_APTO_PARA_ITERAR
NPC_EXEC_REPLAN_V01_REQUIERE_CORRECCIONES
NPC_EXEC_REPLAN_V01_FALLO_CONCEPTUAL
```
