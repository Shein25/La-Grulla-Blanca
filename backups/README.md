# Backups del proyecto

Esta carpeta contiene snapshots de continuidad de **La Grulla Blanca**.

## Regla

Los backups fechados no se sobrescriben.

Después de un progreso importante se crea un nuevo `HANDOFF_MAESTRO_YYYY-MM-DD*.md` con:

- baseline y SHA-256;
- fuentes canónicas vigentes;
- decisiones humanas nuevas;
- etapas cerradas y pendientes;
- invariantes congelados;
- entregables nuevos;
- problemas abiertos;
- próxima acción exacta.

Los commits normales de Git conservan el historial del código; estos handoffs conservan además el contexto de diseño y auditoría necesario para retomar el proyecto desde otra conversación.
