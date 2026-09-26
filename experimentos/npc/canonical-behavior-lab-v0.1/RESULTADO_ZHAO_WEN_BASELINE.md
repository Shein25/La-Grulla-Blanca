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

`ZHAO_WEN_DIALOGUE_BASELINE: 15_PASS_0_FAIL_CONFIRMED`


## Verificación confirmada

```text
PASS: 15
FAIL: 0
```

Confirmado:

- R1, R2 y R3 iniciales devuelven `NO_SABE`;
- `disclosure = 0`;
- relaciones máximas no cambian ese resultado;
- rango máximo del jugador tampoco cambia ese resultado;
- el perfil canónico y el perfil experimental permanecen inmutables;
- `ARCHIVO_RESTRINGIDO_PERMISSION` no existe en el vocabulario GOAP actual.
