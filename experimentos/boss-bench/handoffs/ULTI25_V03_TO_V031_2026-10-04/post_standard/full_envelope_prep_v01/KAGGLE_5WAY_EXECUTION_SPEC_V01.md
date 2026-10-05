# ESPECIFICACIÓN DE EJECUCIÓN KAGGLE EN 5 VÍAS — FULL ENVELOPE V01

## Objetivo

Preparar la campaña final de técnicas + repertorio de Ultis + Grulla para ejecutarse en **5 notebooks en paralelo**, uno por elemento principal:

1. FIRE
2. METAL
3. WATER
4. EARTH
5. WIND

Cada notebook comparte exactamente las mismas autoridades, semántica de seeds/CRN, contratos y formato de salida.

## Unidad real de comparación

La unidad no es una Ulti aislada. Es:

`primary_element + grafted_element + normal_technique_profile + primary_ultimate + grafted_ultimate + combat_context + choice_policy`

El repertorio tiene máximo 2 Ultis y sólo 1 activación válida total por combate.

## Sharding determinístico

No usar un índice secuencial dependiente del orden del notebook para generar RNG.

Definir un `comparison_group_id` canónico a partir de:

`campaign_id | stage | primary_element | grafted_element | policy | loadout | targets | route | replica`

La seed CRN se deriva del `comparison_group_id`, **sin incluir qué Ulti alternativa fue elegida**, para que las elecciones comparadas reciban el mismo mundo aleatorio.

El `case_id` sí incluye la alternativa/candidato para que cada fila sea única.

## Cinco notebooks

Cada notebook fija `primary_element` y procesa todos los grafts autorizados para esa raíz. Si la autoridad futura prohíbe primary==grafted, esos casos no se generan. Hasta entonces la legalidad de esa combinación permanece `AUTHORITY_REQUIRED`.

La división en cinco vías no debe cambiar ninguna seed ni métrica frente a una ejecución serial equivalente.

## Checkpoint

Cada shard guarda, como mínimo:

- `campaign_id`
- `notebook_root`
- `shard_id`
- hashes de todas las autoridades
- `cases_committed`
- `last_committed_case_id`
- lista/rangos de réplicas finalizadas
- profundidad alcanzada (`HIGH_R64`, `DEEP_R256`, `DEEP_R1000`, etc.)
- suites/celdas completas
- suites/celdas parciales
- timestamp
- SHA-256 de archivos parciales

La escritura debe ser atómica: escribir temporal, flush/fsync y rename/commit.

## Resume

Al reiniciar:

1. validar hashes de autoridad;
2. validar `campaign_id`;
3. rechazar checkpoints incompatibles;
4. reconstruir el conjunto de `case_id` ya comprometidos;
5. continuar sólo con casos faltantes;
6. no repetir R64/R256 si ya forman parte del rango incremental completado.

## Progressive depth

Mostrar progreso por evidencia, no sólo porcentaje global:

- `HIGH R64`
- `DEEP R256`
- `DEEP R1000`

Ejemplo: `HIGH R64 ✅ | DEEP R256 ✅ | DEEP R1000 43%`.

R64/R256/R1000 son incrementales; una campaña que ya tiene `0..255` debe ejecutar sólo `256..999` para completar R1000.

## Barra de progreso

Cada notebook debe mostrar periódicamente:

- casos completados / total
- porcentaje
- casos/s
- tiempo transcurrido
- ETA
- shard actual
- profundidad actual
- último checkpoint
- tiempo restante estimado de sesión

## Watchdog de sesión

`session_budget_minutes` y `watchdog_reserve_minutes` son parámetros de campaña, no constantes enterradas en el código.

Cuando se entra en la reserva:

1. no aceptar un nuevo shard grande;
2. terminar la unidad atómica actual;
3. escribir checkpoint;
4. cerrar resultados parciales;
5. producir ZIP recuperable;
6. salir limpiamente con estado `PAUSED_BY_WATCHDOG`, no `FAIL`.

## Salida comprimida

Evitar un único JSON bruto gigantesco. Preferir chunks comprimidos por shard y tablas agregadas compactas. El ZIP de cada notebook debe incluir manifiesto, hashes y checkpoint final.

## Consolidación

El consolidator final debe exigir:

- los 5 roots esperados;
- hashes de autoridad idénticos;
- 0 `case_id` duplicados;
- 0 huecos esperados;
- 0 solapamientos de replica ranges no autorizados;
- misma versión de esquema;
- CRN reproducible;
- todos los shards `COMPLETE` o una lista explícita de faltantes.

Sólo después se calculan métricas cross-root.

## Métricas específicas de elección de Ulti

- `ULTIMATE_CHOICE_SHARE`
- `ULTIMATE_OPPORTUNITY_REGRET`
- `ULTIMATE_UNUSED_RATE`
- `PRIMARY_ULTIMATE_USE_RATE`
- `GRAFTED_ULTIMATE_USE_RATE`
- distribución de fase de uso
- Pacto F3 / first-real-action interaction
- supervivencia post-Ulti
- estado de Grulla post-Ulti

Una Ulti que sea elegida casi siempre sobre su alternativa debe marcarse para revisión humana, no auto-nerf.
