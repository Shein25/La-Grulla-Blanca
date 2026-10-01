# Pociones y Alquimia — recalibración tras revisión de HP de equipo

Fecha: 2026-10-01

Estado: **CURACIÓN HP RATIFICADA / QI Y ECONOMÍA PENDIENTES / SIN CAMBIO DE RUNTIME**

## Nueva base

Se toma como base de diseño:

```text
HP desnudo
LI   30
LII  36
LIII 42
LIV  48

HP de equipo ≈ ×1,5 frente al catálogo anterior
peso interno HP ≈ 0,333
DEF sin cambios
build de resistencia LIV ≈ 70–80 HP
```

Qi estructural conservado:

```text
37 / 43 / 49 / 55
```

## Problemas del consumible legacy

En `grulla-blanca_ver74.html`:

- Poción de sangre de almacén: `3d6+6`, media 16,5, impureza +1.
- Poción de sangre refinada estable: `3d4+4`, media 11,5.
- Elixir de qi menor estable: 20.
- Elixir de tempestad excepcional: 55.

La primera relación invierte la lógica de Alquimia: la medicina barata cura más
que la estable refinada.

El valor 55 de Tempestad puede restaurar el 100% del Qi desnudo de LianQi IV.

## Referencia de HP equipado

Para diagnóstico, no como autoridad de equipo, si los antiguos bonos EXPECTED
de HP (1/3/5/7) se aproximan a ×1,5, el personaje esperado queda cerca de:

```text
LI  ≈ 32 HP
LII ≈ 41 HP
LIII≈ 50 HP
LIV ≈ 59 HP
```

Esto permite que una medicina estable ronde un tercio largo del HP esperado y
que una excepcional ronde aproximadamente dos tercios, mientras una build LIV
de 70–80 HP recibe proporcionalmente menos.

## Curación HP ratificada

La propuesta provisional anterior queda reemplazada por:

`ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json`

Formulaciones cerradas:

| Etapa | Formulación | Impura | Estable | Superior | Excepcional |
|---|---|---:|---:|---:|---:|
| LI | Básica | 2d4+4 | 2d4+7 | 3d4+7 | 4d4+7 |
| LII | Templada | 3d4+5 | 3d4+9 | 4d4+10 | 5d4+11 |
| LIII | Profunda | 4d4+6 | 4d6+8 | 5d6+10 | 6d6+12 |
| LIV | Condensada | 5d4+10 | 5d6+12 | 6d6+16 | 7d6+20 |

Poción común:

`2d4+3` (mín. 5 / media 8 / máx. 11).

Estos valores están HUMAN-RATIFIED. No recalibrarlos durante el trabajo de Qi,
ingredientes, XP o costes salvo reapertura humana explícita.

## Propuesta de recuperación de Qi pura

Se propone inicialmente la misma escalera absoluta:

| Etapa | Impura | Estable | Superior | Excepcional |
|---|---:|---:|---:|---:|
| LianQi I | 8 | 12 | 16 | 20 |
| LianQi II | 10 | 15 | 20 | 26 |
| LianQi III | 12 | 18 | 25 | 33 |
| LianQi IV | 14 | 22 | 30 | 40 |

Con costes base de 6/7/9 Qi, esto devuelve acciones útiles sin convertir una
poción en un segundo depósito de Qi completo.

Medicinas híbridas (por ejemplo Destilado Lunar con purificación) deben recuperar
menos Qi que un elixir puro equivalente.

## Estructura por etapas

No se pretende que una calidad excepcional de la receta LI sustituya una receta
LIV.

La progresión será:

```text
etapa de receta/material
×
calidad del lote
```

Por tanto:

- LI: receta inicial;
- LII: nuevo material de etapa;
- LIII: nuevo material de etapa;
- LIV: material tardío/raro.

Arco 1 mantiene rango formal máximo de Alquimia en **Novicio**, por lo que
ninguna receta del propio Arco 1 deberá exigir Aprendiz.

## Orden de cierre

1. ratificar números HP/Qi;
2. asignar recetas y materiales por etapa;
3. balancear cantidades/rareza/coste;
4. revisar XP de cada receta;
5. revisar techos de calidad/práctica;
6. probar economía de fabricación;
7. sólo entonces preparar migración de runtime.

No se modifica `ver74` durante esta fase.
