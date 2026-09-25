# Experimentos de IA y autonomía de NPCs

Esta carpeta agrupa los experimentos cuyo dominio principal son los NPCs.

## Familias actuales

- `utility-ai/` — Utility AI y selección de objetivos.
- `goap/` — planificación GOAP.
- `memoria/` — memoria, relaciones y capas de decisión.
- `scheduler/` — lifecycle y planificación temporal.
- `execution/` — ejecución, verificación y replanning.
- `integraciones/` — integración experimental entre módulos, incluido Autonomous NPC Loop.
- `reactive-routine-fsm-v0.1/` — candidata experimental para NPC sencillos con rutina + reacción, sin planificación profunda.

## Regla

Esta agrupación es organizativa. No significa que todos los NPC deban utilizar la misma IA ni que deban cargar todas estas capas.

Cada NPC deberá asignarse posteriormente al motor más simple que cubra correctamente su comportamiento.
