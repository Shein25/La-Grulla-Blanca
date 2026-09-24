# La Grulla Blanca

**La Grulla Blanca** es un MUD/RPG xianxia narrativo desarrollado actualmente como una aplicación HTML monolítica.

## Estado del proyecto

El proyecto se encuentra en el cierre técnico y narrativo del **Arco 1**.

La prioridad actual es terminar y estabilizar el monolito antes de migrarlo a una arquitectura modular.

### Roadmap activo

- 3C.3 — Atlas: **CERRADO**
- 3C.4 — Ecología / errantes / herbalismo: **CERRADO**
- 3C.5 — NPC canónicos y movilidad: **CERRADO**
- 3C.6 — Prólogo + M01–M07
- 3C.7 — M08–M15
- 3C.8 — M16
- 3C.9 — M17 + M18 + epílogo
- 3C.10 — Limpieza y regresión global

Después de aprobar 3C.10 se congelará una versión final del Arco 1 y comenzará la modularización.

## Baseline técnico actual

Baseline canónico aprobado:

`grulla-blanca_ver74.html`

SHA-256:

`8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

`SAVE_SCHEMA_VERSION = 2`

La promoción a baseline se realizó después del cierre auditado de 3C.5 del 2026-09-23. La regresión completa de ver74 terminó en 398/398 PASS.

## Filosofía de desarrollo

Durante el cierre del Arco 1:

- el juego continúa siendo monolítico;
- las etapas se implementan y auditan por separado;
- no se modifican sistemas congelados sin una causa documentada;
- los cambios nuevos deben superar regresión antes de convertirse en baseline;
- no se inicia el Arco 2 antes de finalizar la modularización.

## Arquitectura futura

Después de 3C.10, el proyecto migrará progresivamente hacia una estructura modular con separación de motor/estado, mundo/topología, Atlas, NPC, combate, profesiones, misiones, persistencia, UI, datos, tests y assets.

El objetivo es desarrollar y probar sobre módulos, y poder generar una versión web jugable y, si conviene, una distribución HTML autocontenida.

## Web

Este repositorio podrá utilizarse más adelante para publicar una versión jugable mediante GitHub Pages.

La publicación web se configurará una vez que exista un baseline apropiado para distribución pública.
