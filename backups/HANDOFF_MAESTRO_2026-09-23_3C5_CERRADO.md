# Handoff Maestro — 3C.5 cerrado / ver74 baseline

Fecha: 2026-09-23

## Estado

3C.5 — NPC canónicos y movilidad técnica: **CERRADO**.

Baseline canónico actual:

`grulla-blanca_ver74.html`

SHA-256:

`8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

`SAVE_SCHEMA_VERSION = 2`

## Git

Rama de implementación:

`implement/3c5-npc-ver74`

PR:

`#3 — 3C.5: NPC canónicos y movilidad técnica — ver74`

Merge commit:

`eb97b0aeec4725228757d11ffcaff5c3234394ad`

Head de main al crear este handoff:

`9312be155909086ab2358a46ea81b1fe1fe2862d`

## Auditoría

Resultado:

`3C5_IMPLEMENTACION_AUDITADA_PASS`

Regresión completa:

`398 / 398 PASS`

Subconjuntos:

- 3C.5: 4/4
- 3C.4: 11/11
- 3C.2: 113/113
- 3C.1: 16/16
- Atlas: 33/33
- Cartografía: 2/2

`node --check`: PASS.

Informe:

`docs/AUDITORIA_3C5_VER74_2026-09-23.md`

## NPC congelados en este hito

- 32/32 NPC
- 7 autoridad
- 7 intermedio
- 12 funcional
- 6 companero
- 14 CANÓNICO
- 18 ELECCION_TECNICA_3C5
- 0 LIBRE
- R1–R10 exactos
- aliases sin colisiones
- 12 tokens ambiguos rechazados

## Movilidad

- posición runtime: `posicionNPC`
- 85/85 tramos de rutas adyacentes
- tránsito técnico validado por NPC
- Qiao Ren y Wei Jian son los únicos cruces publicados de `SECTA_INTERIOR`
- no existe scheduler/cadencia automática
- no se modificaron `ROOMS.exits`
- no se modificó `GATES_329`

## Atlas

Se mantiene:

```text
posicionNPC[id].sala    = posición real
atlas.personas[id].sala = último avistamiento
atlas.salas[rid].npcs   = memoria acumulada
```

## Persistencia

Dos formas válidas:

- LEGACY exacto
- NPC v1 exacto

NPC v1 añade:

- `npc_version = 1`
- `posicionNPC`
- `conocimientoNPC`

Legacy válido carga defaults NPC sin mutar el payload.

## Fuera de alcance de 3C.5

No se implementaron:

- M01–M18
- M16
- diálogos narrativos
- descripciones físicas inventadas
- Utility AI
- GOAP
- memoria social
- propagación de conocimiento
- scheduler NPC
- pathfinding nuevo

## Roadmap inmediato

Cerrados:

- 3C.3
- 3C.4
- 3C.5

Siguiente bloque activo:

- 3C.6 — Prólogo + M01–M07

Después:

- 3C.7 — M08–M15
- 3C.8 — M16
- 3C.9 — M17 + M18 + epílogo
- 3C.10 — cleanup + regresión global
