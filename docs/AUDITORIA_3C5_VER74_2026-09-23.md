# Auditoría independiente 3C.5 — ver74

Fecha: 2026-09-23

## Veredicto

`3C5_IMPLEMENTACION_AUDITADA_PASS`

La candidata `grulla-blanca_ver74.html` de la rama `implement/3c5-npc-ver74` supera la auditoría independiente técnica y la regresión completa disponible.

## Integridad

- SHA-256 ver73 de entrada:
  `a66310f06fbf8c76e054df89f9d8cdf6959ac64c79400694474351c0936bc6dc`
- SHA-256 ver74 auditada:
  `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`
- `SAVE_SCHEMA_VERSION = 2`
- `ROOMS.exits`: 0 cambios
- `GATES_329`: 0 cambios
- sin dependencias runtime externas nuevas

## Regresión

La candidata se ejecutó en Chromium real headless con un shim exclusivo de almacenamiento para el banco de pruebas, necesario porque el entorno de prueba bloqueaba `localStorage` al cargar contenido local. El HTML auditado no fue modificado.

Resultado:

```text
GB.PRUEBAS.correr()
398 / 398 PASS
0 FAIL
```

Subconjuntos:

```text
3C.5          4 / 4 PASS
3C.4         11 / 11 PASS
3C.2        113 / 113 PASS
3C.1         16 / 16 PASS
Atlas        33 / 33 PASS
Cartografía   2 / 2 PASS
```

`node --check` del script embebido: PASS.

## NPC

- 32/32 IDs exactos
- categorías: 7 autoridad / 7 intermedio / 12 funcional / 6 companero
- 14 `CANÓNICO`
- 18 `ELECCION_TECNICA_3C5`
- 0 `LIBRE`
- 32/32 con R1–R10 exactos
- 0 aliases aceptados en colisión
- 12 tokens ambiguos rechazados
- 5 NPC sin alias corto: qiao_ren, chen_bo, wen_tao, ren_bo, mei_lian
- han_qiao acepta `han`
- mei_shufen acepta `shufen`

## Posición y movilidad

`posicionNPC` es la única fuente de posición runtime.

Se verificó:

- 85/85 tramos de rutas físicamente adyacentes;
- 0 rutas imposibles;
- por NPC: `transito_tecnico ∩ territorio_normal = ∅`;
- por NPC: sala inicial fuera de tránsito técnico;
- todos los nodos de tránsito técnico son internos a rutas del NPC;
- los únicos cruces de gate publicados siguen siendo Qiao Ren y Wei Jian por `SECTA_INTERIOR`;
- movimiento bloqueado con gate cerrado;
- movimiento permitido con gate abierto cuando el paso físico existe;
- no existe scheduler/cadencia automática.

## Atlas

Separación preservada:

```text
posicionNPC[id].sala   = posición real
atlas.personas[id].sala = último avistamiento
atlas.salas[rid].npcs   = memoria acumulada
```

Mover un NPC sin observación no actualiza Atlas.

## Save/load

Se verificaron las dos únicas formas válidas:

- LEGACY exacto;
- NPC v1 exacto.

NPC v1 requiere:

- `npc_version === 1`;
- 32 IDs exactos de posición;
- 32 IDs exactos de conocimiento;
- room real y permitida;
- anclaje coherente;
- R1–R10 exactos;
- enum DESCONOCIDO/SOSPECHA/SABE/CONFIRMADO.

Las formas intermedias/corruptas se rechazan antes de importar estado. Legacy carga defaults NPC sin mutar el payload fuente.

## Alcance

No se implementaron:

- M01–M18;
- M16;
- diálogos narrativos;
- descripciones físicas inventadas;
- Utility AI;
- GOAP;
- memoria social;
- propagación de conocimiento;
- scheduler de NPC;
- pathfinding nuevo.

## Cierre

La limitación declarada por Codex era únicamente la falta de navegador real en su entorno. Esa validación se completó en auditoría independiente y no se detectaron defectos bloqueantes.

Por tanto, 3C.5 queda apta para merge y cierre.
