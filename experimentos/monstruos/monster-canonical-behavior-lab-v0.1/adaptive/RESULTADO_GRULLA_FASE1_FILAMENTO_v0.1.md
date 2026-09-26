# Resultado — Grulla Fase I-B · Filamento de Agua aislado v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / SELECCIÓN COMPLETA / FINALISTAS PENDIENTES DE CONFIRMACIÓN  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance

Este bloque estudia solamente:

```text
FASE I — EL VOTO INMÓVIL
+
Filamento de Agua
```

No incluye Paso, Piel, combinaciones entre opcionales, Fase II ni Fase III.

Baseline:

```text
Grulla HP 150
ATQ 4
daño 1d6+2
Campanada 2d6+2
DEF 13 / 14
Pata Inmóvil +3 DEF siguiente ofensiva
```

La técnica raíz conserva 2 PT. Filamento puede usar 0, 1 o 2 PT, siempre dentro del máximo total de 4 PT.

## 2. Semántica ver74 comprobada

Se verificó directamente `grulla-blanca_ver74.html` en `implement/3c5-npc-ver74`.

Filamento:

```text
coste base = 6
atadura base = 1
controlBono base en maestría 2 = 2 + 2 = +4
```

Contra un jefe único:

```text
DEF de la prueba de control = DEF del jefe +2
atadura máxima efectiva = 1 acción
si el control acierta -> Tenacidad 2 rondas
cooldown efectivo de Filamento = 1 ronda
dañoAtar sólo ocurre si el control acierta
```

La prueba usa exactamente el d20 de ver74:

```text
1 natural -> falla
20 natural -> acierta
resto -> d20 + ATQ efectivo + controlBono >= DEF jefe + 2
```

Filamento es Agua:

- raíz Agua recibe el -1 qi de afinidad;
- Fuego y Metal no;
- siempre se respeta el piso de coste del 70%.

## 3. Ramas probadas

Tramo 1:

```text
Nudo ligero  -> coste -1
Hilo cortante -> daño al atar 1d3
Nudo firme -> control +3
```

Tramo 2:

```text
Lazo doble -> atadura 2
Nudo perseguidor -> control +4
Lazo medido -> daño al atar 1d4
```

Se probaron las 16 configuraciones legales:

```text
base                1
sólo tramo 1        3
sólo tramo 2        3
tramo 1 + tramo 2   9
---------------------
total              16
```

Nota importante: `Lazo doble` eleva la atadura nominal a 2, pero contra la Grulla sigue limitada a una sola acción por ser jefe único.

## 4. Política FILAMENTO_READER

```text
Golpe de Ala
-> técnica raíz

Golpe de Ala
-> técnica raíz

Campanada
-> si Filamento está legal:
   sin Tenacidad
   sin cooldown
   qi suficiente
   -> usar Filamento
-> en caso contrario -> DEFENDER

Pata Inmóvil
-> ATACAR básico
```

La poción conserva prioridad en vida crítica, como en los bloques anteriores.

No se usa Filamento sobre Golpes normales ni Pata. Tampoco se conoce de antemano si la tirada de control acertará.

## 5. Barrido de selección

```text
27 formas raíz
× 16 configuraciones Filamento
× 2 DEF
× 5.000 duelos
=
4.320.000 duelos
```

Script:

`benchmark/colab/grulla-phase1-filamento-v0.1.py`

## 6. Resultados del grid

### DEF 13

| Configuración | Win global |
|---|---:|
| **Hilo cortante + Lazo medido** | **75,57%** |
| **Nudo firme + Lazo medido** | **75,03%** |
| **Hilo cortante + Nudo perseguidor** | **73,01%** |
| Nudo ligero + Lazo medido | 70,88% |
| Lazo medido | 69,48% |
| Hilo cortante + Lazo doble | 67,56% |
| Hilo cortante | 67,51% |
| Nudo ligero + Nudo perseguidor | 66,77% |
| Nudo firme + Nudo perseguidor | 64,19% |
| Nudo firme + Lazo doble | 64,13% |
| Nudo firme | 63,96% |
| Nudo perseguidor | 63,90% |
| Nudo ligero + Lazo doble | 61,83% |
| Nudo ligero | 61,69% |
| Filamento base | 59,52% |
| Lazo doble | 59,43% |

### DEF 14

| Configuración | Win global |
|---|---:|
| **Nudo firme + Lazo medido** | **67,28%** |
| **Hilo cortante + Lazo medido** | **67,00%** |
| **Hilo cortante + Nudo perseguidor** | **65,98%** |
| Nudo ligero + Lazo medido | 61,50% |
| Lazo medido | 59,42% |
| Nudo ligero + Nudo perseguidor | 58,84% |
| Hilo cortante | 57,57% |
| Hilo cortante + Lazo doble | 57,50% |
| Nudo firme + Nudo perseguidor | 55,88% |
| Nudo perseguidor | 55,68% |
| Nudo firme | 55,06% |
| Nudo firme + Lazo doble | 54,96% |
| Nudo ligero | 51,81% |
| Nudo ligero + Lazo doble | 51,79% |
| Filamento base | 49,14% |
| Lazo doble | 49,06% |

## 7. Lectura preliminar

READER universal:

```text
DEF 13 = 60,9%
DEF 14 = 54,7%
```

Filamento base:

```text
DEF 13 = 59,52%  -> -1,38 pp
DEF 14 = 49,14%  -> -5,56 pp
```

Por tanto encontrar el manual, sin especializarlo, no produce una mejora automática.

Las formas fuertes combinan una de dos ideas:

1. daño adicional al cerrar el control;
2. mayor probabilidad de impedir Campanada.

El extremo de duración `Lazo doble` no aporta contra la Grulla porque el contrato de jefe único limita la atadura real a una sola acción.

## 8. Finalistas

Se seleccionan:

```text
T1-2 + T2-3
Hilo cortante + Lazo medido
daño al atar 1d3+1d4
controlBono +4
coste: 6 Fuego/Metal, 5 Agua

T1-3 + T2-3
Nudo firme + Lazo medido
daño al atar 1d4
controlBono +7
coste: 6 Fuego/Metal, 5 Agua

T1-2 + T2-2
Hilo cortante + Nudo perseguidor
daño al atar 1d3
controlBono +8
coste: 6 Fuego/Metal, 5 Agua
```

Estos tres dominan de forma consistente el grid y representan combinaciones distintas de daño/control.

## 9. Estado

```text
FASE I-A              CERRADA
FASE I-B / PASO       CERRADO
FASE I-B / PIEL       CERRADO
FASE I-B / FILAMENTO  GRID COMPLETO / CONFIRMACIÓN PENDIENTE
FASE I-C              NO INICIAR
FASE II               NO TOCAR
FASE III              NO TOCAR
```
