# Resultado — Grulla Fase I-B · Filamento de Agua aislado v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / BLOQUE FILAMENTO CERRADO  
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

Prueba de control:

```text
1 natural -> falla
20 natural -> acierta
resto -> d20 + ATQ efectivo + controlBono >= DEF jefe + 2
```

Filamento es Agua:

- raíz Agua recibe -1 qi por afinidad;
- Fuego y Metal no;
- se respeta el piso de coste del 70%.

## 3. Ramas probadas

Tramo 1:

```text
Nudo ligero   -> coste -1
Hilo cortante -> daño al atar 1d3
Nudo firme    -> control +3
```

Tramo 2:

```text
Lazo doble       -> atadura 2
Nudo perseguidor -> control +4
Lazo medido      -> daño al atar 1d4
```

Configuraciones legales:

```text
base                1
sólo tramo 1        3
sólo tramo 2        3
tramo 1 + tramo 2   9
---------------------
total              16
```

`Lazo doble` eleva la atadura nominal a 2, pero contra la Grulla sigue limitada a una sola acción por el contrato de jefe único.

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

La poción conserva prioridad en vida crítica.

No se usa Filamento sobre Golpes normales ni sobre Pata. La política tampoco conoce de antemano el resultado de la tirada de control.

## 5. Barrido de selección

```text
27 formas raíz
× 16 configuraciones Filamento
× 2 DEF
× 5.000 duelos
=
4.320.000 duelos
```

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

## 6. Finalistas confirmados

Se confirmaron:

```text
T1-2 + T2-3
Hilo cortante + Lazo medido
daño al atar 1d3+1d4
controlBono +4

T1-3 + T2-3
Nudo firme + Lazo medido
daño al atar 1d4
controlBono +7

T1-2 + T2-2
Hilo cortante + Nudo perseguidor
daño al atar 1d3
controlBono +8
```

Coste de las tres:

```text
Fuego = 6 qi
Metal = 6 qi
Agua = 5 qi por afinidad
```

Confirmación:

```text
27 formas raíz
× 3 finalistas
× 2 DEF
× 20.000 duelos
=
3.240.000 duelos
```

Resultado global:

| Configuración | DEF 13 | DEF 14 |
|---|---:|---:|
| **Hilo cortante + Lazo medido** | **75,69%** | 66,76% |
| **Nudo firme + Lazo medido** | 75,02% | **67,25%** |
| Hilo cortante + Nudo perseguidor | 72,97% | 65,89% |

El orden del grid se mantiene. La sensibilidad DEF cambia cuál de las dos primeras formas queda arriba.

## 7. Ganador por sensibilidad

### DEF 13

Mejor:

```text
Hilo cortante + Lazo medido
controlBono +4
daño al atar 1d3+1d4
```

Por raíz:

| Raíz | Win jugador |
|---|---:|
| Fuego | 75,44% |
| Metal | 79,72% |
| Agua | 71,91% |
| **Global** | **75,69%** |

Rango entre builds:

```text
57,76% – 88,10%
```

La tasa media de éxito del control en esta configuración fue aproximadamente:

```text
Agua 80,04%
Fuego 84,96%
Metal 90,03%
```

### DEF 14

Mejor:

```text
Nudo firme + Lazo medido
controlBono +7
daño al atar 1d4
```

Por raíz:

| Raíz | Win jugador |
|---|---:|
| Fuego | 68,02% |
| Metal | 70,97% |
| Agua | 62,77% |
| **Global** | **67,25%** |

Rango entre builds:

```text
44,62% – 86,81%
```

Éxito medio del control:

```text
Agua 90,02%
Fuego 94,96%
Metal 94,97%
```

No aparece una única configuración universal dominante:

- DEF13 favorece acumular daño al cerrar el lazo;
- DEF14 aumenta el valor de mejorar la precisión de control.

## 8. Comparación con READER universal

READER universal:

```text
DEF 13 = 60,9%
DEF 14 = 54,7%
```

Mejor Filamento para cada sensibilidad:

```text
DEF 13:
60,9 -> 75,69
+14,79 puntos porcentuales

DEF 14:
54,7 -> 67,25
+12,55 puntos porcentuales
```

Filamento base:

```text
DEF 13 = 59,52% -> -1,38 pp
DEF 14 = 49,14% -> -5,56 pp
```

Por tanto el manual por sí solo no es una mejora automática. La ventaja aparece al especializar correctamente la técnica.

## 9. Comparación cualitativa con Paso y Piel

Resultados ya cerrados:

```text
Paso óptimo:
DEF13 +5,35 pp
DEF14 +4,69 pp

Piel óptima:
DEF13 +36,23 pp
DEF14 +40,84 pp
```

Filamento óptimo:

```text
DEF13 +14,79 pp
DEF14 +12,55 pp
```

Filamento aporta más que Paso, pero muchísimo menos que Piel.

## 10. Lectura de diseño

Filamento ayuda **de forma fuerte pero razonable**.

No trivializa Fase I:

- su mejor resultado global queda alrededor de 76% / 67%;
- sigue existiendo una diferencia importante entre builds;
- la prueba de control puede fallar;
- el jefe limita la atadura a una acción;
- Tenacidad impide encadenar controles;
- la técnica consume la acción del jugador;
- la versión base es peor que simplemente usar el READER universal.

El resultado encaja con el papel de una herramienta opcional especializada: puede neutralizar Campanadas con frecuencia, pero no convierte la fase en victoria casi automática.

No se propone nerfear Filamento ni modificar stats de la Grulla a partir de este bloque.

## 11. Volumen útil

```text
4.320.000 duelos — grid de selección
3.240.000 duelos — confirmación de 3 finalistas
------------------------------------------------
7.560.000 duelos útiles
```

## 12. Estado

```text
FASE I-A              CERRADA
FASE I-B / PASO       CERRADO
FASE I-B / PIEL       CERRADO
FASE I-B / FILAMENTO  CERRADO
FASE I-C              PENDIENTE — NO INICIAR EN ESTE BLOQUE
FASE II               NO TOCAR
FASE III              NO TOCAR
```

Script reproducible:

`benchmark/colab/grulla-phase1-filamento-v0.1.py`
