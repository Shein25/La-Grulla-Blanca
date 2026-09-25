# Experimentos — GOAP

Familia experimental dedicada a planificación GOAP para NPC.

## Línea actual

`motor-npc-vivo-v0.2-goap/`

v0.2.2 quedó **cerrada y mergeada** como snapshot experimental.

- PR: #2
- HEAD experimental cerrado: `552117cc3f01530d43e4523de8c7d41ec986373e`
- merge commit: `5812deb59cd1c133383b9af973486a702a26daf4`
- veredicto final: `V022_GOAP_APTO_PARA_ITERAR`

## Dependencia experimental

Esta familia reutiliza fixtures ficticios de:

`../utility-ai/motor-npc-vivo-v0.1.1/`

No utiliza NPC, salas, gates ni misiones canónicas de producción.

## Regla

GOAP planifica objetivos lógicos. No debe convertirse en pathfinding físico de rooms.
