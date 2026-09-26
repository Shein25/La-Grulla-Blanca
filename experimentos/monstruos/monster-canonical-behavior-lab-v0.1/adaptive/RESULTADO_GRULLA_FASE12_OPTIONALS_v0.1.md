# Resultado — Grulla Fase I → II · opcionales en cadena v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / VALIDACIÓN DE OPCIONALES CERRADA  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Objetivo

Cerrar el único pendiente explícito del checkpoint de recalibración:

```text
PASO / PIEL / FILAMENTO PENDIENTES EN CADENA
```

Se mantiene congelada Fase I y se prueba Fase II con:

```text
HP FII = 100
DEF = 13
CHAIN_A
Golpe de Ala = 1d4
Tormenta = 1d6+1
ATQ bonus = +0
Cerrar Alas = absorción 3 / reserva 6
Recordar Filo = +10 EVA siguiente ofensiva
Eco = drain condicional 3
Tormenta drain = 1
```

No se modifica cerebro, memoria, anti-spam ni Utility.

## 2. Técnicas opcionales y counters

Contrato recuperado del laboratorio:

```text
Paso de Nube
role = esquiva
counter = PULSO FIJADO

Piel de Cobre
role = guardia
counter = RESONANCIA INTERNA

Filamento de Agua
role = control
counter = ANCLA DEL VOTO

técnica raíz
role = ofensiva
counter = TRAZO VACÍO
```

La regla de aprendizaje se conserva:

```text
3 usos consecutivos de la misma técnica
-> técnica comprendida
-> siguiente repetición queda totalmente suprimida
-> BASIC u otra técnica rompe el lock
-> DEFENDER / curarse no lo rompen
```

## 3. Política tool-aware

Cada ruta usa en Fase I la política ya cerrada para su técnica.

En Fase II:

- READER mantiene BASIC/raíz como política principal;
- Eco se responde sin gasto de qi;
- Recordar se responde con BASIC;
- Cerrar no fuerza gasto adicional;
- la opcional sólo sustituye la defensa de emergencia ante Tormenta cuando HP <= 14;
- si la técnica opcional queda comprendida, su efecto se suprime pero el qi se consume;
- Filamento conserva Tenacidad/cooldown de jefe único.

Esta política evita inflar artificialmente el valor de las opcionales.

## 4. Control 5.000 — reutilizar opcional vs no reutilizarla

Se compararon las mismas entradas a Fase II con la opcional desactivada o activada dentro de Fase II.

### Paso

```text
sin reutilizar:  FII condicional 19,65%
tool-aware:      FII condicional 19,43%
```

### Piel

```text
sin reutilizar:  FII condicional 28,38%
tool-aware:      FII condicional 28,15%
```

### Filamento

```text
sin reutilizar:  FII condicional 22,83%
tool-aware:      FII condicional 23,13%
```

Conclusión:

> La técnica opcional usada dentro de Fase II casi no altera la tasa global. El factor dominante es el estado con el que el jugador llega desde Fase I.

No aparece una llave obligatoria.

## 5. Confirmación 20.000

Volumen:

```text
3 herramientas
× 27 builds raíz
× 20.000
=
1.620.000 cadenas I→II
```

### Global

| Herramienta | Llega FII | FII condicional | Victoria I+II | HP entrada | qi entrada | Poción entrada |
|---|---:|---:|---:|---:|---:|---:|
| Paso | **66,15%** | **19,35%** | **13,49%** | 13,75 | 8,52 | 27,15% |
| Piel | **75,15%** | **28,12%** | **21,86%** | 14,29 | 17,28 | 29,53% |
| Filamento | **75,73%** | **22,86%** | **17,95%** | 13,81 | 13,60 | 26,85% |

### Por raíz

#### Paso

| Raíz | Llega FII | FII condicional | I+II |
|---|---:|---:|---:|
| Fuego | 64,24% | 16,02% | 10,79% |
| Metal | 65,63% | 20,56% | 14,21% |
| Agua | 68,58% | 21,48% | 15,47% |

#### Piel

| Raíz | Llega FII | FII condicional | I+II |
|---|---:|---:|---:|
| Fuego | 75,27% | 26,28% | 20,31% |
| Metal | 76,14% | 32,36% | 25,44% |
| Agua | 74,05% | 25,71% | 19,84% |

#### Filamento

| Raíz | Llega FII | FII condicional | I+II |
|---|---:|---:|---:|
| Fuego | 75,32% | 20,62% | 16,01% |
| Metal | 79,84% | 26,31% | 21,61% |
| Agua | 72,02% | 21,64% | 16,24% |

Rango condicional entre builds:

```text
Paso       7,09% .. 43,79%
Piel      11,88% .. 58,23%
Filamento  9,39% .. 51,90%
```

## 6. Lectura

1. Ninguna opcional trivializa Fase II.
2. Ninguna opcional se vuelve obligatoria dentro de Fase II.
3. Reutilizar la técnica opcional dentro de Fase II produce cambios pequeños frente a conservar la política universal.
4. La mayor diferencia entre rutas proviene del desgaste y consumo de qi de Fase I.
5. Las tres raíces conservan rutas de victoria.
6. El contrato de tres repeticiones sigue evitando automatizar una técnica concreta.
7. Piel llega con mejores recursos, pero no convierte Fase II en una fase fácil.
8. Paso paga mucho qi en Fase I y llega especialmente agotado; esto explica su peor cadena sin necesidad de nerfear la técnica o endurecer la Grulla.

## 7. Decisión sobre CHAIN_A

La validación de opcionales no invalida la recalibración anterior.

Por tanto:

```text
CHAIN_A
Golpe de Ala     1d4
Tormenta         1d6+1
bonus ATQ        +0

Cerrar Alas      3 / reserva 6
Recordar Filo    +10 EVA
Eco              drain 3 condicional
Tormenta drain   1
```

queda **SELECCIONADO para continuar el cierre de Fase II**.

TACT_C / TACT_D quedan como sensibilidad histórica y no deben volver a usarse como baseline de cadena.

## 8. Estado

```text
FASE I                         CERRADA / NO TOCAR

FASE II HP 100                 MANTENER
CEREBRO / MEMORIA              MANTENER
ANTI-SPAM                      MANTENER
CHAIN_A                        SELECCIONADO

PASO EN CADENA                 VALIDADO
PIEL EN CADENA                 VALIDADA
FILAMENTO EN CADENA            VALIDADO

FASE II                        TODAVÍA NO CERRADA
FASE III                       NO TOCAR
```

El siguiente bloque ya no es recalibrar daño ni volver a probar opcionales aisladas.

Lo pendiente para cerrar Fase II es validar el **aprendizaje adaptativo como experiencia de combate**:

- que repetir una técnica tres veces siga siendo castigado;
- que variar de verdad rompa el conocimiento;
- que el jugador que lee Recordar/Eco/Tormenta supere al jugador rígido;
- que la memoria heredada de Fase I no produzca estados imposibles;
- que ninguna respuesta adaptive cree un soft-lock de recursos.

Script reproducible:

`benchmark/colab/grulla-phase12-chain-optionals-v0.1.py`
