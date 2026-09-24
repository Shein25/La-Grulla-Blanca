# Cambios v0.1

- Se restauraron exclusivamente cinco archivos runtime congelados: Memory, Relations, Decision Pipeline, Scheduler y Execution + Replanning; se verifican sus blobs exactos antes de publicar.
- Se agregó `autonomous-loop.mjs`: creación de estado global, captura defensiva, aplicación de observations y memory events, generación de razones para Scheduler y una transición cerebral por dispatch.
- El loop conserva la relación base y la inercia Utility, sincroniza context después de effects GOAP, respeta el presupuesto Scheduler y no crea eventos internos con significados falsos.
- Se agregaron fixtures sintéticos, 101 pruebas (Golden A–R incluidos), stress determinista de cinco seeds y prompt de auditoría externa.
- Se limita a NPC activos y facts GOAP simbólicos. No conecta producción, pathfinder, agenda, dormancy ni duración de acciones.

## REV2

- El loop distingue `PLAN_READY` con plan vacío: comprueba que el goal ya esté satisfecho, devuelve `DECISION_GOAL_ALREADY_SATISFIED` y evita crear la session vacía que producía churn. Toda session recién creada tiene al menos un paso.
- El stress rearma facts transitorios de HELP_PLAYER, INVESTIGATE_ANOMALY, FULFILL_DUTY y REPORT_SUPERIOR; programa invalidaciones reales, obsolescencia y goals alcanzados externamente.
- Se fuerzan replans listos, planificación diferida en ejecución y recuperaciones desde `REPLAN_PENDING`. El oracle comprueba que el paso invalidado no se ejecute y que el primer paso del nuevo plan espere otro dispatch.
- Se agregaron métricas de goals satisfechos al decidir, sesiones vacías, goals externos, planes stale forzados y prevenidos, recuperaciones pendientes y acciones posteriores a replans. La suite suma seis regresiones y conserva los Golden A–R.
