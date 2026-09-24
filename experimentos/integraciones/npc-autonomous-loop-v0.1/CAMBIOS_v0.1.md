# Cambios v0.1

- Se restauraron exclusivamente cinco archivos runtime congelados: Memory, Relations, Decision Pipeline, Scheduler y Execution + Replanning; se verifican sus blobs exactos antes de publicar.
- Se agregó `autonomous-loop.mjs`: creación de estado global, captura defensiva, aplicación de observations y memory events, generación de razones para Scheduler y una transición cerebral por dispatch.
- El loop conserva la relación base y la inercia Utility, sincroniza context después de effects GOAP, respeta el presupuesto Scheduler y no crea eventos internos con significados falsos.
- Se agregaron fixtures sintéticos, 101 pruebas (Golden A–R incluidos), stress determinista de cinco seeds y prompt de auditoría externa.
- Se limita a NPC activos y facts GOAP simbólicos. No conecta producción, pathfinder, agenda, dormancy ni duración de acciones.
