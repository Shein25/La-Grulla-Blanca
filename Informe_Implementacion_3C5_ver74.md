# Implementación 3C.5 — ver74 (candidata)

Rama de trabajo: `implement/3c5-npc-ver74`. Baseline: `00_grulla-blanca_ver73.html` del paquete `LA_GRULLA_BLANCA_3C5_IMPLEMENTACION_PARA_CODEX.zip`. Se respetó `docs/GUARDIA_RAMA_3C5_IMPLEMENTACION.md`; no se trabajó sobre `main` ni sobre las ramas experimentales y no se hizo merge.

## Integridad

- SHA-256 de entrada ver73 verificado: `a66310f06fbf8c76e054df89f9d8cdf6959ac64c79400694474351c0936bc6dc`.
- SHA-256 de salida ver74: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`.
- Comparación mecánica de `ROOMS.exits` y `GATES_329` entre ambos HTML: idénticos; **0 cambios**.
- Auditores integrados: mundo **PASS** (329 salas, 17 áreas, 787 salidas dirigidas, 786 internas y una externa); cartografía **PASS** (355 cardinales intra hoja, 349 rectas, seis rutas, dos cruces).
- `SAVE_SCHEMA_VERSION = 2`; no se añadieron dependencias externas en runtime.

## Bloques modificados en `grulla-blanca_ver74.html`

1. Catálogo estático `NPC_DEF` generado de las 32 entradas de `Matriz_Implementacion_3C5_NPC_REV3.json`, conservando los 17 campos exigidos sin reinterpretar datos. `NOMBRES_NPC`, `NPC_ALIASES` e índice normalizado derivan de esa tabla. `DESCS_NPC` permanece vacío.
2. `Juego.constructor` y `nuevaPartida`: inicializan `posicionNPC` y `conocimientoNPC` con 32 IDs cada uno. Los laboratorios de prueba que instancian `Juego` directamente también reciben defaults válidos.
3. `npcsEnSala`, `npcPresente`, `puedeMoverNPC`, `aplicarMovimientoNPC`: posición runtime única, un paso físico explícito, territorio y gates validados; sin cadencia automática ni actualización de Atlas al mover.
4. `mostrarSala`, `recordarAtlas`, `cmd_examinar`, `cmd_hablar`, `cmd_entregar` y chips de sala: consultan posición runtime y resuelven nombre o alias por igualdad exacta. `EXAMINAR` muestra únicamente nombre y rol si no hay descripción física cerrada.
5. `validarSave329`, `serializar`, `deserializar`: forma LEGACY exacta y forma NPC v1 exacta; el save nuevo guarda snapshots profundos; la carga LEGACY prepara defaults internos sin mutar el payload; cualquier forma intermedia o corrupta se rechaza antes de importar estado.
6. Pruebas previas que presuponían catálogos NPC vacíos o claves de save sin NPC: actualizadas para el estado de 3C.5. Se añadieron cuatro casos nuevos de matriz, alias/presencia/Atlas, movimiento/gates/anclaje y save/legacy/corrupción.

## Cobertura y pruebas

- **32/32** definiciones, posiciones y conocimientos R1–R10. Categorías: 7 autoridad, 7 intermedio, 12 funcional y 6 companero. Salas iniciales: 14 `CANÓNICO`, 18 `ELECCION_TECNICA_3C5`; 0 `LIBRE`.
- **4/4** pruebas nuevas de 3C.5: PASS, incluyendo los 12 tokens ambiguos, tránsito técnico por NPC, gates cerrados y abiertos, último avistamiento independiente y rechazo atómico de 14 corrupciones de save.
- `node --check` del script embebido: PASS.
- Suite histórica completa: se ejecutaron **398 casos** en un entorno Node con DOM simulado: **309 pasan y 89 no se pueden validar allí**. Los errores restantes corresponden a métodos y comportamiento de interfaz que el simulador no implementa (`replaceChildren`, clics, render y estilos). Esos resultados no equivalen a una regresión en navegador. En ejecuciones filtradas: 3C.2, 107/113; 3C.1, 15/16; 3C.4, 10/11; 3C.5, 4/4. Los fallos de las tres primeras selecciones son de la interfaz simulada.
- Pruebas negativas del save NPC v1: faltan versión, posición, conocimiento o ID; ID extra; room inexistente o fuera de territorio; anclaje incoherente o room inexistente; R1 ausente, R11 extra, valor inválido y clave top-level extra: todos rechazados sin importar estado parcial. El legacy puro valida y se carga sin modificación del objeto fuente.

## Límite pendiente

El navegador de pruebas no está disponible para abrir el HTML local en este entorno. Se requiere correr `GB.PRUEBAS.correr()` en un navegador real y revisar la interfaz antes de presentar ver74 a auditoría independiente. La presente implementación **no** declara cerrado 3C.5.

No se implementaron misiones M01–M18, M16, diálogos narrativos, descripciones físicas, Utility AI, GOAP, propagación de conocimiento ni scheduler de NPC.

`3C5_IMPLEMENTACION_REQUIERE_CORRECCIONES`
