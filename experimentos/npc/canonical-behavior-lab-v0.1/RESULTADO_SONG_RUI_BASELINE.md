# Song Rui — baseline de archivos/conocimiento / LAB v0.1

## Objetivo

Probar dos dimensiones:

1. conocimiento canónico parcialmente fuera del esquema R1-R3;
2. protección documental M16 reducida hoy a deber simbólico.

## Canon relevante

- Responsable de Archivos;
- R3 = SABE;
- R4, R5, R6 y R9 = SOSPECHA;
- M16: Archivo / protección de documentación;
- epílogo: catalogación.

## Conocimiento

R3 sí entra en el esquema actual y puede evaluarse.

Los topics canónicos adicionales R4/R5/R6/R9 no caben todavía en `knowledge`.

Gap compartido:

`KNOWLEDGE_SCHEMA_R1_TO_R10`

## M16

El stack actual abstrae protección documental como:

```text
trabajar
→ FULFILL_DUTY
→ cumplir_deber
```

Eso no representa:

- inventario documental;
- prioridad/protección de piezas;
- daño/pérdida;
- traslado;
- catalogación;
- acceso por sector.

Gap de dominio:

`ARCHIVE_PROTECTION_AND_CATALOG_STATE`

## Estado

`SONG_RUI_ARCHIVE_BASELINE: 13_PASS_0_FAIL_CONFIRMED`


## Confirmación

```text
PASS: 13
FAIL: 0
```

Confirmado:

- R3 = SABE se evalúa como conocimiento real (`INSINUA` en el contexto de calibración);
- R4/R5/R6/R9 producen `knowledge: sobran ...`;
- M16 crea `trabajar → FULFILL_DUTY → cumplir_deber`;
- `cumplir_deber` no contiene semántica de archivo/documentos.
