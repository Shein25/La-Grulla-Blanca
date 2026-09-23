# Estado técnico del proyecto

Este documento resume el estado de trabajo y sirve como referencia rápida del repositorio.

## Regla de autoridad

Las fuentes canónicas del proyecto y las decisiones humanas posteriores tienen prioridad sobre propuestas históricas o borradores.

No se deben inventar conexiones, estados, NPC, room IDs, gates ni resultados ausentes de las fuentes.

## Mundo congelado

Invariantes actuales:

- 329 salas
- 17 áreas
- 787 salidas dirigidas
- 786 salidas internas
- 1 salida externa
- 0 reciprocidades rotas
- 0 salas aisladas
- 1 componente físico
- 329 salas alcanzables ignorando gates
- 185 salas inicialmente alcanzables
- 144 salas inicialmente bloqueadas
- 63 articulation rooms
- 70 bridges
- 13 alojamientos
- 6 atajos de Primera Ala

## Baseline

Baseline canónico actual previo a las integraciones en curso:

`grulla-blanca_ver72a.html`

SHA-256:

`5fa5306940dba5c9c829b67b4e59bd03d1a9e0153aa8bd7ec1dd707c56f70820`

`SAVE_SCHEMA_VERSION = 2`

## Etapas

### Cerradas

- PRE-3C
- 3C.1 — ROOMS / topología / gates
- 3C.1R — cleanup
- 3C.1B — narrativa 329
- 3C.2 — Save/Load
- 3C.3A — Cartografía 329
- 3C.4 — Ecología / errantes / herbalismo

### En curso o pendientes

- 3C.3B — Integración Atlas en producción
- 3C.5 — NPC canónicos
- 3C.6 — Prólogo + M01–M07
- 3C.7 — M08–M15
- 3C.8 — M16
- 3C.9 — M17 + M18 + epílogo
- 3C.10 — Cleanup + regresión completa

## Regla para modularización

No modularizar el juego durante las etapas 3C activas.

La modularización comienza después de:

1. completar 3C.10;
2. congelar el HTML final del Arco 1;
3. ejecutar una regresión global satisfactoria;
4. conservar ese HTML como referencia dorada.

La migración deberá ser progresiva y cada extracción de módulo tendrá que conservar el comportamiento del baseline.
