# Hotfix — LI Equipment Refinement V01 — Focus pair ID

Fecha: 2026-10-07

## Error

La fase `3/4 Focused niches` falló con:

`KeyError: 'lanza_parte_nubes'`

## Causa

El runner del microgate usó en `FOCUS_PAIRS` el identificador humano/abreviado:

`lanza_parte_nubes`

pero el catálogo canónico `techniques_arc1_catalog.json` define la técnica como:

`lanza_nubes`

Los demás IDs del bloque son canónicos.

## Corrección

Reemplazar exclusivamente:

`("lanza_parte_nubes","destello_plata")`

por:

`("lanza_nubes","destello_plata")`

No cambiar:
- candidatos de equipo;
- raíces;
- Concordancias;
- monstruos;
- repeticiones;
- semillas;
- orden de jobs;
- workers;
- checkpoints;
- criterios de decisión.

## Resume

Los checkpoints de:
- `cp_01_item_duel`
- `cp_02_canonical`
- chunks ya completados de `cp_03_niche`

son válidos y reutilizables.

La corrección conserva la posición del par en `FOCUS_PAIRS`, por lo que los chunks previos a la falla mantienen el mismo significado.

El hotfix debe reutilizar el mismo work dir:

`/content/LI_EQUIPMENT_REFINEMENT_V01/results`

No borrar esa carpeta.

## QA requerido

Antes de entregar:
- todos los IDs de `FOCUS_PAIRS` deben existir en el catálogo canónico;
- syntax/py_compile;
- entrypoint;
- 2 workers;
- checkpoint create/resume;
- barra persistente;
- review output name;
- no cambio de cardinalidades salvo el trabajo ya reanudable.
