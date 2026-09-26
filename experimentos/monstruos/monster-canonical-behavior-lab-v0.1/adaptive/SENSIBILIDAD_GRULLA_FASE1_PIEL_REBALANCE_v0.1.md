# Sensibilidad — rebalance de Piel de Cobre v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / SENSIBILIDAD COMPLETA / CANDIDATO PENDIENTE DE GRID COMPLETO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Objetivo

Reducir el outlier de Piel detectado al cerrar Fase I-C sin cambiar su identidad mecánica.

Se conserva:

```text
burbuja persistente
reserva = Guardia × duración
absorción por golpe = min(daño, Guardia, reserva)
la reserva sólo baja al absorber
no caduca por rondas
fallos enemigos no consumen reserva
misma política PIEL_READER
mismos costes
mismas ramas de coste
mismas ramas +1 duración
```

En este bloque sólo varían:

- Guardia base;
- duración/multiplicador base;
- valor de `Cobre endurecido`;
- valor de `Cobre grueso`.

No se modifica ver74 productivo.

## 2. Modelos de sensibilidad

| Modelo | Guardia base | Duración base | Endurecido | Grueso |
|---|---:|---:|---:|---:|
| CURRENT | 3 | 2 | 6 | 7 |
| G345_D2 | 3 | 2 | 4 | 5 |
| G234_D2 | 2 | 2 | 3 | 4 |
| G345_D1 | 3 | 1 | 4 | 5 |
| G234_D1 | 2 | 1 | 3 | 4 |
| G344_D1 | 3 | 1 | 4 | 4 |

Cada modelo conserva las 16 configuraciones legales de Piel y raíz = 2 PT.

## 3. Volumen

```text
6 modelos
× 27 formas raíz
× 16 configuraciones Piel
× 2 DEF
× 2.000 duelos
=
10.368.000 duelos
```

## 4. Mejor configuración de cada modelo

| Modelo | Mejor capacidad | DEF 13 | DEF 14 |
|---|---:|---:|---:|
| CURRENT | Guardia 7 × 3 = 21 | 97,16% | 95,62% |
| G345_D2 | Guardia 5 × 3 = 15 | 92,36% | 89,41% |
| G234_D2 | Guardia 4 × 3 = 12 | 87,53% | 82,99% |
| G345_D1 | Guardia 5 × 2 = 10 | 88,69% | 84,44% |
| **G234_D1** | **Guardia 4 × 2 = 8** | **82,47%** | **77,79%** |
| G344_D1 | Guardia 4 × 2 = 8 | 82,58% | 77,96% |

El control CURRENT reproduce la magnitud del benchmark cerrado (≈97,13% / 95,54%), por lo que el barrido es consistente con el modelo anterior.

## 5. Piel base

| Modelo | Piel base | DEF 13 | DEF 14 |
|---|---|---:|---:|
| CURRENT | G3 × 2 = 6 | 74,05% | 68,80% |
| G345_D2 | G3 × 2 = 6 | 74,60% | 68,95% |
| G234_D2 | G2 × 2 = 4 | 63,30% | 57,53% |
| G345_D1 | G3 × 1 = 3 | 58,87% | 52,53% |
| **G234_D1** | **G2 × 1 = 2** | **50,11%** | **43,86%** |
| G344_D1 | G3 × 1 = 3 | 59,04% | 52,72% |

Que la forma base sea débil no invalida el modelo: Paso base también quedó por debajo del READER universal en su aislamiento. El manual no necesita ser una mejora automática sin inversión de PT.

## 6. Candidato seleccionado para grid completo

Se selecciona provisionalmente:

```text
G234_D1

Piel base:
Guardia 2
duración/multiplicador 1
reserva 2

Cobre endurecido:
Guardia 3

Cobre flexible:
+1 duración

Cobre sobrio:
coste -1

Aliento económico:
coste -1

Cobre grueso:
Guardia 4

Placas continuas:
+1 duración
```

Razones:

1. reduce la forma especializada desde ≈97/96 a ≈82/78;
2. mantiene diferencias reales entre Guardia 2, 3 y 4;
3. mantiene intactas las identidades de duración y economía;
4. no introduce reglas nuevas;
5. no duplica `Cobre endurecido` y `Cobre grueso`, como ocurriría en G344_D1;
6. conserva la burbuja persistente exacta de ver74.

## 7. Estado

```text
FASE I-C                    CERRADA
PIEL / SENSIBILIDAD         CERRADA
PIEL / G234_D1 GRID 5.000   PENDIENTE
PIEL / CONFIRMACIÓN 20.000  PENDIENTE
DEF13 / DEF14               NO SELECCIONAR AÚN
FASE II                     NO TOCAR
```

Script:

`benchmark/colab/grulla-phase1-piel-rebalance-v0.1.py`
