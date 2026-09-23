# Estado técnico del proyecto

Este documento resume el estado de trabajo y sirve como referencia rápida del repositorio.

## Regla de autoridad

Las fuentes canónicas del proyecto y las decisiones humanas posteriores tienen prioridad sobre propuestas históricas o borradores.

No se deben inventar conexiones, estados, NPC, room IDs, gates ni resultados ausentes de las fuentes.

## Mundo congelado

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

Baseline canónico actual:

`grulla-blanca_ver73.html`

SHA-256:

`a66310f06fbf8c76e054df89f9d8cdf6959ac64c79400694474351c0936bc6dc`

`SAVE_SCHEMA_VERSION = 2`

Baseline anterior conservado como referencia histórica:

`grulla-blanca_ver72a.html` — `5fa5306940dba5c9c829b67b4e59bd03d1a9e0153aa8bd7ec1dd707c56f70820`

## Etapas cerradas

- PRE-3C
- 3C.1 — ROOMS / topología / gates
- 3C.1R — cleanup
- 3C.1B — narrativa 329
- 3C.2 — Save/Load
- 3C.3A — Cartografía 329
- 3C.3B — Integración Atlas en producción
- **3C.3 — CERRADO**
- 3C.4 — Ecología / errantes / herbalismo

## En curso o pendientes

- 3C.5 — NPC canónicos
- 3C.6 — Prólogo + M01–M07
- 3C.7 — M08–M15
- 3C.8 — M16
- 3C.9 — M17 + M18 + epílogo
- 3C.10 — Cleanup + regresión completa

## Auditoría 3C.3B

Fecha: 2026-09-23.

Resultado independiente: **APROBADO**.

Comprobaciones reproducidas:

- hash de ver73 correcto;
- ROOMS y GATES_329 idénticos a ver72a;
- serializar(), deserializar(), validarSave329() y salidasAtlas() sin cambios;
- las cinco tablas cartográficas coinciden exactamente con REV3;
- 329/17/787, 786 internas + 1 externa;
- 355 cardinales intra-hoja;
- 20 cardinales entre hojas;
- 18 verticales;
- 29 pares entre áreas;
- 349 rectas + 6 routes = 355 representadas;
- 2 crossovers exactos y ningún cruce adicional;
- 0 líneas sobre rooms ajenas;
- 0 autointersecciones;
- 63 articulation rooms y 70 bridges;
- 185 alcanzables inicialmente / 144 bloqueadas;
- bloque de pruebas congelado 3C.4 idéntico a ver72a;
- node --check PASS;
- sin dependencias externas nuevas;
- SAVE_SCHEMA_VERSION sigue en 2.

La suite de navegador 394/394 y la inspección visual de seis hojas constan en el informe de implementación de Codex; el entorno de auditoría independiente no permitió relanzar Chromium, por lo que esas dos comprobaciones no se reclaman como reproducidas localmente.

## Regla para modularización

No modularizar durante las etapas 3C activas.

La modularización comienza después de:

1. completar 3C.10;
2. congelar el HTML final del Arco 1;
3. ejecutar una regresión global satisfactoria;
4. conservar ese HTML como referencia dorada.

La migración deberá ser progresiva y cada extracción de módulo tendrá que conservar el comportamiento del baseline.
