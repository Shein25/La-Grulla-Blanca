# Sensibilidad y cierre — rebalance de Piel de Cobre G234_D1 v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / REBALANCE G234_D1 VALIDADO EN FASE I  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Objetivo

Corregir el outlier de Piel de Cobre detectado en Fase I-B/Fase I-C sin destruir su identidad.

Se conserva exactamente:

```text
burbuja persistente
reserva = Guardia × duración
absorción por golpe = min(daño, Guardia, reserva restante)
la reserva sólo baja al absorber
no caduca por rondas
fallos enemigos no consumen reserva
mismos costes
mismas ramas de coste
mismas ramas +1 duración
misma política PIEL_READER / MULTI_READER
```

No se modifica ver74 productivo en este bloque.

## 2. Sensibilidad inicial

Se compararon seis escalas numéricas:

| Modelo | Guardia base | Duración base | Endurecido | Grueso | Mejor DEF13 | Mejor DEF14 |
|---|---:|---:|---:|---:|---:|---:|
| CURRENT | 3 | 2 | 6 | 7 | 97,16% | 95,62% |
| G345_D2 | 3 | 2 | 4 | 5 | 92,36% | 89,41% |
| G234_D2 | 2 | 2 | 3 | 4 | 87,53% | 82,99% |
| G345_D1 | 3 | 1 | 4 | 5 | 88,69% | 84,44% |
| **G234_D1** | **2** | **1** | **3** | **4** | **82,47%** | **77,79%** |
| G344_D1 | 3 | 1 | 4 | 4 | 82,58% | 77,96% |

Volumen:

```text
6 × 27 × 16 × 2 × 2.000
=
10.368.000 duelos
```

CURRENT reproduce la magnitud del benchmark cerrado (~97,13% / 95,54%).

Se seleccionó G234_D1 porque reduce el outlier sin crear ramas equivalentes.

## 3. G234_D1

```text
Piel base
Guardia 2
duración/multiplicador 1
reserva 2

Tramo 1
Cobre endurecido -> Guardia 3
Cobre flexible   -> +1 duración
Cobre sobrio     -> coste -1

Tramo 2
Aliento económico -> coste -1
Cobre grueso       -> Guardia 4
Placas continuas   -> +1 duración
```

No se altera ninguna otra regla.

## 4. Grid aislado — 5.000

```text
27 × 16 × 2 × 5.000
=
4.320.000 duelos
```

Top:

| Configuración | Guardia | Mult. | Reserva | DEF13 | DEF14 |
|---|---:|---:|---:|---:|---:|
| **Cobre flexible + Cobre grueso** | **4** | **2** | **8** | **82,56%** | **77,92%** |
| Cobre endurecido + Placas continuas | 3 | 2 | 6 | 74,54% | 68,88% |
| Cobre flexible + Placas continuas | 2 | 3 | 6 | 68,65% | 63,05% |
| Cobre sobrio + Cobre grueso | 4 | 1 | 4 | 67,96% | 61,96% |
| Cobre grueso | 4 | 1 | 4 | 67,32% | 60,64% |

Piel base:

```text
DEF13 50,03%
DEF14 43,85%
```

## 5. Confirmación aislada — 20.000

```text
27 × 3 × 2 × 20.000
=
3.240.000 duelos
```

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **Cobre flexible + Cobre grueso** | **82,61%** | **77,91%** |
| Cobre endurecido + Placas continuas | 74,53% | 68,84% |
| Cobre flexible + Placas continuas | 68,95% | 63,24% |

Mejor forma G234_D1:

```text
coste 5
Guardia 4
multiplicador 2
reserva 8
```

Frente al READER universal:

```text
DEF13: 60,9 -> 82,61 = +21,71 pp
DEF14: 54,7 -> 77,91 = +23,21 pp
```

Frente a Piel actual óptima:

```text
DEF13: 97,13 -> 82,61 = -14,52 pp
DEF14: 95,54 -> 77,91 = -17,63 pp
```

La Piel especializada sigue siendo fuerte, pero deja de ser una victoria casi automática.

## 6. Piel + Filamento con G234_D1

Selección:

```text
67 legales -> 42 deduplicadas
42 × 27 × 2 × 5.000
=
11.340.000 duelos
```

Top del grid:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **C22_F00** | **76,79%** | **67,32%** |
| C13_F00 | 65,50% | 54,72% |
| C03_F03 | 64,08% | 53,05% |
| C02_F03 | 63,89% | 52,85% |

La combinación que antes era problemática:

```text
C02_F03
antes:       93,09% / 86,68%
G234_D1:     63,89% / 52,85%
```

Confirmación:

```text
3 × 27 × 2 × 20.000
=
3.240.000 duelos
```

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **C22_F00** | **76,90%** | **67,14%** |
| C13_F00 | 65,66% | 54,60% |
| C03_F03 | 64,40% | 53,01% |

La amplificación excesiva Piel+Filamento queda eliminada.

## 7. Paso + Piel con G234_D1

Selección:

```text
67 legales -> 37 deduplicadas
37 × 27 × 2 × 5.000
=
9.990.000 duelos
```

Top:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C22** | **60,55%** | **50,70%** |
| P02_C03 | 55,93% | 46,33% |
| P02_C02 | 55,42% | 45,82% |

Antes del rebalance, la mejor forma daba 89,26% / 82,58%.

Confirmación:

```text
3 × 27 × 2 × 20.000
=
3.240.000 duelos
```

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C22** | **60,46%** | **50,89%** |
| P02_C03 | 56,09% | 46,28% |
| P02_C02 | 55,65% | 46,04% |

Paso+Piel deja de constituir una sinergia defensiva dominante.

## 8. Triple con G234_D1

Selección:

```text
154 legales -> 88 deduplicadas
88 × 27 × 2 × 5.000
=
23.760.000 duelos
```

Top:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C22_F00** | **16,08%** | **9,89%** |
| P00_C02_F03 | 14,17% | 8,67% |
| P00_C02_F20 | 12,57% | 7,56% |

Validación del simulador:

```text
mismo código + Piel antigua en P00_C02_F03:
53,05% / 39,19%

resultado histórico:
53,00% / 39,28%
```

La caída es por el rebalance, no por divergencia del simulador.

Confirmación:

```text
3 × 27 × 2 × 20.000
=
3.240.000 duelos
```

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C22_F00** | **16,17%** | **9,87%** |
| P00_C02_F03 | 14,20% | 8,75% |
| P00_C02_F20 | 12,64% | 7,55% |

El triple expone el coste real de intentar activar demasiadas respuestas en un ciclo. Sin una Piel sobredimensionada, sacrificar casi toda la ofensiva deja de ser sostenible.

## 9. Resultado global del rebalance

Comparación de rutas relevantes:

| Ruta | DEF13 | DEF14 |
|---|---:|---:|
| READER universal | 60,9% | 54,7% |
| Paso aislado óptimo | 66,25% | 59,39% |
| Filamento aislado óptimo | 75,69% | 67,25% |
| **Piel G234_D1 óptima** | **82,61%** | **77,91%** |
| Piel G234_D1 + Filamento | 76,90% | 67,14% |
| Paso + Piel G234_D1 | 60,46% | 50,89% |
| Triple G234_D1 | 16,17% | 9,87% |

Conclusiones:

1. Piel deja de trivializar Fase I.
2. Sigue siendo la opcional individual más potente cuando recibe 2 PT.
3. Filamento no se vuelve obligatorio.
4. Piel+Filamento ya no produce una sinergia superior a Piel aislada.
5. Paso+Piel deja de sobreproteger.
6. El triple demuestra que poseer más herramientas no sustituye una buena economía de acciones.
7. No fue necesario cambiar la semántica persistente de Guardia.

## 10. Volumen útil del rebalance

```text
sensibilidad                       10.368.000
grid aislado G234_D1                4.320.000
confirmación aislada                3.240.000
Piel+Filamento grid                11.340.000
Piel+Filamento confirmación         3.240.000
Paso+Piel grid                      9.990.000
Paso+Piel confirmación              3.240.000
triple grid                        23.760.000
triple confirmación                 3.240.000
---------------------------------------------
TOTAL                              72.738.000 duelos
```

## 11. Estado

```text
FASE I-A                         CERRADA
FASE I-B / PASO                  CERRADO
FASE I-B / FILAMENTO             CERRADO
FASE I-C                         CERRADA

PIEL ACTUAL                      SUPERSEDED COMO CANDIDATO DE BALANCE
PIEL G234_D1                     VALIDADA EXPERIMENTALMENTE
VER74 PRODUCTIVO                 SIN CAMBIOS

DEF13 / DEF14                    LISTOS PARA REEVALUACIÓN
PATA INMÓVIL +3                  SIGUE PROVISIONAL
FASE II                          NO TOCAR
FASE III                         NO TOCAR
```

Scripts:

- `benchmark/colab/grulla-phase1-piel-rebalance-v0.1.py`
- `benchmark/colab/grulla-phase1-piel-g234d1-filamento-v0.1.py`
- `benchmark/colab/grulla-phase1-multi-g234d1-v0.1.py`
