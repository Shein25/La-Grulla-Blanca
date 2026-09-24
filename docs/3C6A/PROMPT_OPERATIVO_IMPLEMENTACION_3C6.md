# Prompt operativo — implementación 3C.6 P–M07

Trabajá exclusivamente en `Shein25/La-Grulla-Blanca`, rama `implement/3c6-prologo-m01-m07`, creada desde `contract/3c6-prologo-m01-m07` HEAD `b0d90ea70ab17b3d6a7e85951e19f00c7935c8f2`. No trabajes en main, audit, experiment ni ramas anteriores; no hagas merge.

Antes de editar, comprobá la rama, HEAD base, `grulla-blanca_ver74.html` SHA-256 `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566` y `docs/3C6A/Matriz_Implementacion_3C6A_Prologo_M01_M07_REV3_1.json` SHA-256 `96d6a73383fdd5636005460bd3483f3e6b7f8f358a5354fdaa1f76cab0e3d881`.

Leé y seguí, en este orden, `docs/3C6A/CIERRE_3C6A_REV3_1.md`, `docs/3C6A/Contrato_Implementacion_3C6_Prologo_M01_M07.md`, la reconciliación y la matriz REV3.1, y la auditoría final. La implementación debe ser `grulla-blanca_ver75.html` sin sobrescribir ver74. Entregá `Informe_Implementacion_3C6_Prologo_M01_M07.md` con archivos, hashes, tests y desviaciones explícitas.

Implementá íntegramente P–M07, migración exacta de saves ver74, estado `flags.arc1` y reconciliación fail-closed, dos transiciones de etapa, economía de Contribución/Mérito separada, anclajes con owner, wrapper local de rata M02, muñeco M03, protección/reemisión de píldora, ocho fuentes M06 y conocimiento M07. La primera incorporación de cada tipo de evidencia territorial debe invocar `reconciliarProgresionArc1()` en esa misma acción.

Conservá `SAVE_SCHEMA_VERSION=2`, las 329 salas, 17 áreas, 787 salidas, `ROOMS.exits`, `GATES_329`, el catálogo global de errantes y los subsistemas 3C.4. No incorpores M08–M18, GOAP, Utility AI, scheduler NPC, tiempo diegético ni modularización. No uses `visitadas` históricas para checkpoints M04/M05. No abras M12 ni los atajos con la transición LIII.

Probá Node y navegador real cuando esté disponible, incluidos saves a mitad de cada misión, migraciones legacy por etapa, corrupción fail-closed, recompensas one-shot, soft-locks y la suite completa. No declares PASS de navegador sin ejecutarlo ni declares 3C.6 cerrada: requiere auditoría externa y autorización posterior para merge.
