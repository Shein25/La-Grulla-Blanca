# Sensibilidad — rebalance de Piel de Cobre v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / G234_D1 CONFIRMADO EN AISLAMIENTO / RETEST MULTI EN PROGRESO  
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

Sólo se estudian Guardia base, duración base y los valores de Cobre endurecido / Cobre grueso.

No se modifica ver74 productivo.

## 2. Sensibilidad inicial

Modelos:

| Modelo | Guardia base | Duración base | Endurecido | Grueso |
|---|---:|---:|---:|---:|
| CURRENT | 3 | 2 | 6 | 7 |
| G345_D2 | 3 | 2 | 4 | 5 |
| G234_D2 | 2 | 2 | 3 | 4 |
| G345_D1 | 3 | 1 | 4 | 5 |
| G234_D1 | 2 | 1 | 3 | 4 |
| G344_D1 | 3 | 1 | 4 | 4 |

Volumen:

```text
6 modelos
× 27 formas raíz
× 16 configuraciones Piel
× 2 DEF
× 2.000
=
10.368.000 duelos
```

Mejor configuración de cada modelo:

| Modelo | Mejor capacidad | DEF13 | DEF14 |
|---|---:|---:|---:|
| CURRENT | G7 × 3 = 21 | 97,16% | 95,62% |
| G345_D2 | G5 × 3 = 15 | 92,36% | 89,41% |
| G234_D2 | G4 × 3 = 12 | 87,53% | 82,99% |
| G345_D1 | G5 × 2 = 10 | 88,69% | 84,44% |
| **G234_D1** | **G4 × 2 = 8** | **82,47%** | **77,79%** |
| G344_D1 | G4 × 2 = 8 | 82,58% | 77,96% |

El control CURRENT reproduce el benchmark cerrado (~97,13% / 95,54%).

Piel base por modelo:

| Modelo | Piel base | DEF13 | DEF14 |
|---|---|---:|---:|
| CURRENT | G3 × 2 = 6 | 74,05% | 68,80% |
| G345_D2 | G3 × 2 = 6 | 74,60% | 68,95% |
| G234_D2 | G2 × 2 = 4 | 63,30% | 57,53% |
| G345_D1 | G3 × 1 = 3 | 58,87% | 52,53% |
| **G234_D1** | **G2 × 1 = 2** | **50,11%** | **43,86%** |
| G344_D1 | G3 × 1 = 3 | 59,04% | 52,72% |

## 3. Candidato G234_D1

```text
Piel base:
Guardia 2
duración/multiplicador 1
reserva 2

Cobre endurecido -> Guardia 3
Cobre flexible   -> +1 duración
Cobre sobrio     -> coste -1

Aliento económico -> coste -1
Cobre grueso       -> Guardia 4
Placas continuas   -> +1 duración
```

Razones:

1. elimina el rango 90–97% del aislamiento;
2. mantiene escalones reales Guardia 2/3/4;
3. conserva intacta la semántica de burbuja;
4. conserva ramas de duración y economía;
5. no crea ramas equivalentes como G344_D1;
6. no introduce reglas nuevas.

## 4. Grid completo G234_D1 — 5.000

Volumen:

```text
27 formas raíz
× 16 configuraciones Piel
× 2 DEF
× 5.000
=
4.320.000 duelos
```

| Configuración | Guardia | Mult. | Reserva | Coste | DEF13 | DEF14 |
|---|---:|---:|---:|---:|---:|---:|
| **Cobre flexible + Cobre grueso** | **4** | **2** | **8** | 5 | **82,56%** | **77,92%** |
| Cobre endurecido + Placas continuas | 3 | 2 | 6 | 5 | 74,54% | 68,88% |
| Cobre flexible + Placas continuas | 2 | 3 | 6 | 5 | 68,65% | 63,05% |
| Cobre sobrio + Cobre grueso | 4 | 1 | 4 | 4 | 67,96% | 61,96% |
| Cobre grueso | 4 | 1 | 4 | 5 | 67,32% | 60,64% |
| Cobre endurecido + Cobre grueso | 4 | 1 | 4 | 5 | 67,10% | 60,94% |
| Cobre sobrio + Placas continuas | 2 | 2 | 4 | 4 | 63,76% | 58,02% |
| Cobre flexible + Aliento económico | 2 | 2 | 4 | 4 | 63,75% | 57,87% |
| Cobre flexible | 2 | 2 | 4 | 5 | 63,27% | 57,60% |
| Placas continuas | 2 | 2 | 4 | 5 | 63,26% | 57,40% |
| Cobre endurecido + Aliento económico | 3 | 1 | 3 | 4 | 59,33% | 53,33% |
| Cobre endurecido | 3 | 1 | 3 | 5 | 58,85% | 52,64% |
| Aliento económico | 2 | 1 | 2 | 4 | 50,29% | 44,34% |
| Cobre sobrio + Aliento económico | 2 | 1 | 2 | 4 | 50,27% | 44,33% |
| Cobre sobrio | 2 | 1 | 2 | 4 | 50,26% | 44,36% |
| Piel base | 2 | 1 | 2 | 5 | 50,03% | 43,85% |

Frente a Piel actual óptima:

```text
DEF13: 97,13 -> 82,56 = -14,57 pp
DEF14: 95,54 -> 77,92 = -17,62 pp
```

## 5. Confirmación G234_D1 — 20.000

Finalistas:

```text
Cobre flexible + Cobre grueso
Cobre endurecido + Placas continuas
Cobre flexible + Placas continuas
```

Volumen:

```text
27 × 3 × 2 × 20.000
=
3.240.000 duelos
```

Resultado:

| Configuración | Guardia | Mult. | Reserva | DEF13 | DEF14 |
|---|---:|---:|---:|---:|---:|
| **Cobre flexible + Cobre grueso** | **4** | **2** | **8** | **82,61%** | **77,91%** |
| Cobre endurecido + Placas continuas | 3 | 2 | 6 | 74,53% | 68,84% |
| Cobre flexible + Placas continuas | 2 | 3 | 6 | 68,95% | 63,24% |

Mejor forma confirmada:

```text
coste 5
Guardia 4
multiplicador 2
reserva 8
```

Comparada con READER universal:

```text
DEF13: 60,9 -> 82,61 = +21,71 pp
DEF14: 54,7 -> 77,91 = +23,21 pp
```

Comparada con Piel actual:

```text
DEF13: 97,13 -> 82,61 = -14,52 pp
DEF14: 95,54 -> 77,91 = -17,63 pp
```

El aislamiento deja de ser victoria casi automática.

## 6. Retest Piel + Filamento — selección 5.000

Se reutiliza exactamente `MULTI_READER` de Fase I-C. Sólo cambia Piel a G234_D1.

Deduplicación:

```text
67 configuraciones legales brutas
-> 42 efectivamente distintas
```

Volumen:

```text
42 × 27 × 2 × 5.000
=
11.340.000 duelos
```

Top:

| Configuración | PT | DEF13 | DEF14 |
|---|---:|---:|---:|
| **C22_F00** | 2 | **76,79%** | **67,32%** |
| C13_F00 | 2 | 65,50% | 54,72% |
| C03_F03 | 2 | 64,08% | 53,05% |
| C02_F03 | 2 | 63,89% | 52,85% |
| C03_F20 | 2 | 61,96% | 50,57% |
| C02_F20 | 2 | 61,63% | 50,58% |

La antigua combinación problemática:

```text
C02_F03
antes:
DEF13 93,09%
DEF14 86,68%

con G234_D1:
DEF13 63,89%
DEF14 52,85%
```

La amplificación excesiva desaparece.

El nuevo líder `C22_F00` invierte los 2 PT en Piel y lleva Filamento base preparado:

```text
C22
Cobre flexible + Cobre grueso
Guardia 4
reserva 8
2 PT

F00
Filamento base
0 PT
```

Bajo MULTI_READER, intentar Filamento base en Campanada reduce el rendimiento frente a Piel aislada (82,61/77,91 -> 76,79/67,32) porque consume una ventana ofensiva y puede fallar.

## 7. Finalistas del retest

```text
C22_F00
C13_F00
C03_F03
```

Confirmación a 20.000 pendiente.

## 8. Volumen acumulado del rebalance

```text
sensibilidad             10.368.000
grid G234_D1              4.320.000
confirmación aislamiento  3.240.000
retest Piel+Filamento    11.340.000
-----------------------------------
subtotal                  29.268.000 duelos
```

## 9. Estado

```text
FASE I-C                         CERRADA
PIEL / SENSIBILIDAD              CERRADA
PIEL / G234_D1 GRID              CERRADO
PIEL / G234_D1 CONFIRMACIÓN      CERRADA
PIEL + FILAMENTO RETEST GRID     CERRADO
PIEL + FILAMENTO CONFIRMACIÓN    PENDIENTE
DEF13 / DEF14                    NO SELECCIONAR AÚN
VER74 PRODUCTIVO                 SIN CAMBIOS
FASE II                          NO TOCAR
```

Scripts:

- `benchmark/colab/grulla-phase1-piel-rebalance-v0.1.py`
- `benchmark/colab/grulla-phase1-piel-g234d1-filamento-v0.1.py`
