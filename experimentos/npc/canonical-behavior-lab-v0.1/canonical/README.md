# Snapshot canónico NPC_DEF — ver74

Fuente exacta:

```text
grulla-blanca_ver74.html
blob d34f7ea3f9de9344130aa072fac34d14a7a474d6
objeto const NPC_DEF
```

El archivo `NPC_DEF_ver74.snapshot.json` fue extraído mediante parseo directo del objeto JSON válido contenido en `const NPC_DEF`.

No contiene interpretación ni perfiles experimentales.

Se usa para evitar reescribir manualmente el canon de los 32 NPC en cada test.

La suite `tests/all-npc-canon.test.mjs` comprueba transversalmente:

- 32 NPC;
- ids;
- sala inicial;
- territorio y tránsito;
- rutas;
- movilidad ANCLADO/RUTA;
- conocimiento R1–R10;
- aliases;
- totales por categoría y movilidad.
