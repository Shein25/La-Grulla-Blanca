# Experimentos de IA y sistemas de monstruos

Esta carpeta agrupa experimentos cuyo dominio principal son los monstruos.

## Familias actuales

- `monster-ai/` — kernel de decisión de Monster Combat AI.
- `monster-canonical-behavior-lab-v0.1/` — catálogo, adaptación, memoria, señales e integración de los 18 monstruos.

## Regla

La IA de combate de monstruos permanece separada de la autonomía general de NPCs y de la resolución real del Combat Engine.

Las futuras familias específicas de monstruos se añadirán aquí sólo cuando exista un experimento real. No crear carpetas vacías por adelantado.

## Contrato vigente de estadísticas

Todo el subsistema de monstruos usa exclusivamente `NEW_COMBAT_STATS_V0_1`.

Handoff actual:

`HANDOFF_MONSTRUOS_NUEVO_MOTOR_2026-10-01.md`

Todo consumidor debe usar ese contrato directamente y validar su esquema exacto.
