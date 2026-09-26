# Resultado — Grulla Fase I → II · recalibración de cadena v0.2

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / CHAIN_A PROVISIONAL  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Punto de partida

Fase I permanece congelada:

```text
HP 150
ATQ 4
DEF 13
Pata +3
Piel G345_D1
Resonancia x1,75
```

Fase II mantiene:

```text
HP 100
DEF 13
cerebro LAS ALAS RECUERDAN
memoria / counters / Utility sin cambios
```

No existe recuperación gratuita documentada entre fases.

## 2. Corrección del benchmark encadenado

Se detectó que `grulla-phase12-chain-v0.1.py` transportaba `def_next` de Pata Inmóvil a la función de ataque, pero la tirada no lo sumaba a la DEF de la Grulla.

Antes:

```text
hit_roll(..., bdef, ...)
```

Corregido:

```text
hit_roll(..., bdef + def_next, ...)
```

Commit:

`bf934cb82c69b45c1f6fa477193d497565397e10`

Tras la corrección, READER llega a Fase II en ~60,84%, reproduciendo el ~60,87% del cierre de Fase I.

Los resultados de cadena anteriores a esta corrección no se usan para balance.

## 3. TACT_C / TACT_D con recursos heredados

A 5.000 duelos por escenario:

| FX | Estrategia | Llega FII | Victoria FII condicional | Victoria I+II |
|---|---|---:|---:|---:|
| TACT_C | ALTERNATE | 38,27% | 7,74% | 3,33% |
| TACT_C | READER | 60,85% | 10,75% | 7,12% |
| TACT_D | ALTERNATE | 38,00% | 7,48% | 3,19% |
| TACT_D | READER | 60,70% | 10,55% | 6,98% |

Entrada media READER a Fase II:

```text
HP      ~11,8 / 28
qi      ~51 / 110
poción  ~10%
```

Conclusión:

> TACT_C/D eran razonables con jugador fresco, pero demasiado punitivos cuando Fase II recibe el desgaste real de Fase I.

## 4. Sensibilidad de causa

Se probó la misma Fase II sin daño directo de la Grulla, conservando 100 HP, memoria, locks, Cerrar/Recordar/Eco y recursos heredados.

Resultado READER:

```text
victoria condicional Fase II ~99,7%
```

Por tanto el cuello de botella no es:

- HP 100;
- memoria;
- anti-spam;
- qi del jugador;
- capacidad ofensiva para terminar la fase.

El factor dominante es el daño directo de Fase II sobre un jugador que ya entra herido.

## 5. Recalibración de daño directo

Se mantuvieron intactos:

```text
HP FII = 100
DEF = 13
ATQ base = 4
Cerrar Alas = 3 / reserva 6
Recordar Filo = +10 EVA siguiente ofensiva
Eco = drain condicional 3
Tormenta drain = 1
cerebro / scores / memoria
```

Se compararon tres puntos vecinos:

### CHAIN_A

```text
Golpe de Ala     1d4
Tormenta         1d6+1
bonus ATQ        +0
```

### CHAIN_B

```text
Golpe de Ala     1d3+1
Tormenta         1d6+1
bonus ATQ        +0
```

### CHAIN_C

```text
Golpe de Ala     1d4+1
Tormenta         1d6+1
bonus ATQ        +0
```

## 6. Selección 5.000 — por raíz

### CHAIN_A · READER

| Raíz | Llega FII | FII condicional | I+II |
|---|---:|---:|---:|
| Fuego | 61,14% | 33,97% | 21,69% |
| Metal | 59,46% | 33,31% | 20,70% |
| Agua | 61,95% | 28,57% | 18,94% |
| **Global** | **60,85%** | **31,95%** | **20,44%** |

### CHAIN_B · READER

```text
FII condicional global 27,35%
I+II global            17,62%
```

### CHAIN_C · READER

```text
FII condicional global 23,64%
I+II global            15,32%
```

CHAIN_A preserva mejor una ruta mínima para las tres raíces.

## 7. Confirmación CHAIN_A

READER:

```text
27 builds
× 20.000
=
540.000 cadenas I→II
```

| Raíz | Llega FII | FII condicional | I+II |
|---|---:|---:|---:|
| Fuego | 61,15% | 33,62% | 21,45% |
| Metal | 59,54% | 33,17% | 20,66% |
| Agua | 61,83% | 28,32% | 18,79% |
| **Global** | **60,84%** | **31,70%** | **20,30%** |

Rango condicional entre las 27 builds:

```text
11,94% .. 57,94%
```

ALTERNATE, 10.000 por escenario:

```text
FII condicional global 26,86%
I+II global            10,98%
```

La lectura de la Grulla mejora el resultado frente a alternar sin interpretar intenciones.

## 8. Estado

```text
FASE I                         CERRADA / NO TOCAR
FASE II HP 100                 MANTENER
CEREBRO / MEMORIA              MANTENER
ANTI-SPAM                      MANTENER

TACT_C                         SUPERSeded EN CADENA
TACT_D                         SUPERSeded EN CADENA

CHAIN_A                        CANDIDATO PRINCIPAL PROVISIONAL
CHAIN_B                        SENSIBILIDAD
CHAIN_C                        SENSIBILIDAD

PASO / PIEL / FILAMENTO        PENDIENTES EN CADENA
FASE III                       NO TOCAR
```

No congelar CHAIN_A hasta validar las tres herramientas opcionales.

Script reproducible:

`benchmark/colab/grulla-phase12-chain-recalibration-v0.2.py`
