# Guardia de rama — Implementación 3C.5 NPC

Rama dedicada:

`implement/3c5-npc-ver74`

Base:

`main`

Objetivo exclusivo:

Implementar 3C.5 — NPC canónicos y movilidad técnica sobre el baseline `grulla-blanca_ver73.html`, produciendo `grulla-blanca_ver74.html`.

## Reglas

- No trabajar directamente sobre `main`.
- No hacer merge automático.
- No modificar ramas `experiment/motor-npc-*`.
- No integrar Utility AI ni GOAP.
- No implementar misiones M01–M18.
- No inventar scheduler/cadencia de movimiento.
- No modificar `ROOMS.exits`.
- No modificar `GATES_329`.
- Mantener `SAVE_SCHEMA_VERSION = 2`.
- El baseline HTML de entrada debe verificarse por SHA-256:
  `a66310f06fbf8c76e054df89f9d8cdf6959ac64c79400694474351c0936bc6dc`.
- La implementación final debe quedar en esta rama para auditoría independiente antes de cualquier merge.

## Fuente de entrada

Hasta que el baseline y documentos se incorporen explícitamente a Git, usar el paquete local:

`LA_GRULLA_BLANCA_3C5_IMPLEMENTACION_PARA_CODEX.zip`

y su archivo:

`00_grulla-blanca_ver73.html`

No reconstruir el baseline desde documentos históricos.
