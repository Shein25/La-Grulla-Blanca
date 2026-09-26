# Zhao Wen — baseline de conocimiento/diálogo / LAB v0.1

## Objetivo

Cubrir una dimensión distinta del comportamiento NPC: **no revelar conocimiento inexistente**.

## Canon relevante

- aspirante — piezas documentales / análisis;
- progresión territorial hacia Archivo;
- LIII: no accede a Restringido antes que el jugador;
- M09: `ARCHIVO_RESTRINGIDO` concedido por Qiao Ren;
- R1–R10 iniciales: todos `DESCONOCIDO`.

## Invariante principal

Para un topic `DESCONOCIDO`:

```text
mode       = NO_SABE
disclosure = 0
```

La relación con el jugador, su rango o una restricción formal favorable no pueden convertir desconocimiento en información.

El test fuerza incluso relaciones sociales máximas para comprobar este punto.

## Gap M09

El stack GOAP actual no contiene una capacidad de permiso equivalente a:

`ARCHIVO_RESTRINGIDO_PERMISSION`

Por tanto, el acceso canónico de M09 queda registrado como gap de capacidad del stack avanzado. No se simula como si Zhao pudiera atravesar el acceso por decisión propia.

## Estado

`ZHAO_WEN_DIALOGUE_BASELINE: PENDING_RUNTIME_CONFIRMATION`
