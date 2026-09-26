# Cierre experimental — Grulla Blanca · Fase I v0.1

**Fecha:** 2026-09-26  
**Estado:** FASE I CERRADA EXPERIMENTALMENTE  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`  
**Producción:** `ver74` sin cambios

## 1. Alcance cerrado

```text
FASE I-A / raíz                 CERRADA
FASE I-B / Paso                 CERRADA
FASE I-B / Piel                 CERRADA
FASE I-B / Filamento            CERRADA
FASE I-C / combinaciones        CERRADA
rebalance Piel                  CERRADO
anti-absorción / Resonancia     CERRADO
sensibilidad DEF / Pata         CERRADA
```

No reabrir estos benchmarks salvo invalidación concreta de las reglas simuladas o cambio productivo relevante.

## 2. Contrato final de Fase I

```text
FASE I — EL VOTO INMÓVIL

HP                150
ATQ               4
DEF               13

Golpe de Ala      1d6+2
Campanada         2d6+2

Ciclo:
Golpe
Golpe
Campanada
Pata Inmóvil
```

### Pata Inmóvil

`+3 DEF` contra la siguiente acción ofensiva del jugador y telegraphía **Resonancia** para el siguiente Golpe de Ala.

### Resonancia

```text
Pata Inmóvil
-> prepara el siguiente Golpe de Ala

si conecta con Piel de Cobre activa:
    daño bruto x1,75
    después Piel absorbe normalmente

si falla:
    0 daño
    Resonancia se consume igualmente
```

No ignora toda absorción, no rompe Piel por definición, no persigue hasta acertar y no consulta RNG futuro.

## 3. Piel seleccionada — G345_D1

```text
Piel base
coste 5
Guardia 3
multiplicador 1
reserva 3

Tramo 1
Cobre endurecido  -> Guardia 4
Cobre flexible    -> +1 multiplicador
Cobre sobrio      -> coste -1

Tramo 2
Aliento económico -> coste -1
Cobre grueso      -> Guardia 5
Placas continuas  -> +1 multiplicador
```

Forma especializada de referencia:

```text
Cobre flexible + Cobre grueso
coste 5
Guardia 5
multiplicador 2
reserva 10
```

Se conserva la identidad de Guardia: burbuja persistente, reserva que sólo baja al absorber, sin caducidad por rondas y sin consumo por fallos enemigos.

## 4. Balance final — Pata +3 / DEF13

Confirmación a 20.000 duelos por escenario:

| Ruta | Victoria |
|---|---:|
| READER universal | **60,87%** |
| Paso óptimo | **66,29%** |
| Filamento óptimo | **75,60%** |
| Piel G345_D1 + Resonancia x1,75 | **75,29%** |

La Piel original rondaba 97%; la final queda cerca de Filamento, eliminando el outlier sin hacer obligatoria ninguna opcional.

## 5. Validación de combinaciones x1,75

| Familia | Configuración | DEF13 | DEF14 |
|---|---|---:|---:|
| Piel + Filamento | C22_F00 | **49,08%** | 38,00% |
| Paso + Piel | P00_C22 | **55,40%** | 45,85% |
| Triple | P00_C02_F03 | **22,00%** | 14,45% |

`Paso + Filamento` no contiene Piel y Resonancia no altera su contrato cerrado.

Conclusión: apilar opcionales no crea una ruta dominante; la economía de acciones limita las combinaciones defensivas.

## 6. Adaptación bilateral

La Grulla castiga persistencia excesiva de absorción y uso automático de Piel. El jugador puede aceptar Resonancia cuando el riesgo es bajo, usar Paso, abandonar Piel y cambiar de defensa, administrar qi, priorizar daño o usar Filamento en su ventana adecuada.

Los tests también muestran que reaccionar siempre es subóptimo: la respuesta correcta depende de HP, qi y coste de acción.

No existe una llave obligatoria: Paso, Piel y Filamento siguen siendo opcionales y el READER universal permanece viable.

## 7. Sensibilidad final de Pata

### DEF13

| Pata | READER | Paso | Filamento | Piel |
|---:|---:|---:|---:|---:|
| +2 | 63,08% | 68,50% | 77,60% | 76,79% |
| **+3** | **60,87%** | **66,29%** | **75,60%** | **75,29%** |
| +4 | 58,51% | 63,66% | 73,59% | 73,62% |

Se mantiene **Pata +3**: reproduce el baseline histórico y queda en el centro de sensibilidad.

## 8. Sensibilidad final de DEF

Con Pata +3:

| Ruta | DEF13 | DEF14 |
|---|---:|---:|
| READER | **60,87%** | 54,56% |
| Paso | **66,29%** | 59,46% |
| Filamento | **75,60%** | 67,30% |
| Piel | **75,29%** | 69,90% |

Se selecciona **DEF13**. Fase I es la primera etapa de un encuentro de tres fases; DEF14 reduce demasiado la viabilidad de la cola de builds antes de que comiencen los sistemas adaptativos de Fase II y III.

## 9. Contrato congelado

```text
BOSS DEF                         13
PATA INMÓVIL                    +3
PIEL                            G345_D1
RESONANCIA                      x1,75
RESONANCIA                      posterior a Pata
RESONANCIA FALLA                se consume
ABSORCIÓN                       después del x1,75

FASE I HP                       150
ATQ                             4
GOLPE                           1d6+2
CAMPANADA                       2d6+2
```

## 10. Último volumen de validación

```text
validación directa x1,75          3.240.000
sensibilidad final               12.960.000
-------------------------------------------
último bloque                    16.200.000 duelos
```

## 11. Scripts finales

- `benchmark/colab/grulla-phase1-multi-g345d1-resonance-v0.1.py`
- `benchmark/colab/grulla-phase1-final-sensitivity-g345d1-res175-v0.1.py`
- `benchmark/colab/grulla-phase1-pata-anti-absorption-v0.1.py`

Los scripts de raíz, Paso, Piel, Filamento, multi-optionals y rebalance anteriores permanecen como trazabilidad histórica.

## 12. Estado final

```text
FASE I                         CERRADA
FASE I-A                       CERRADA
FASE I-B                       CERRADA
FASE I-C                       CERRADA

G345_D1                        CONGELADA PARA FASE I
RESONANCIA x1,75               CONGELADA PARA FASE I
DEF13                          CONGELADA PARA FASE I
PATA +3                        CONGELADA PARA FASE I

G234_D1                        FALLBACK / NO ACTIVO
PIEL ORIGINAL                  DESCARTADA COMO BALANCE FINAL

VER74                          SIN CAMBIOS
INTEGRACIÓN PRODUCTIVA         NO REALIZADA

FASE II                        PENDIENTE
FASE III                       PENDIENTE
```

La siguiente etapa del laboratorio, cuando sea autorizada, es Fase II — **LAS ALAS RECUERDAN**.