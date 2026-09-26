# Resultado — Grulla Fase II-A · sensibilidad de efectos v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / SELECCIÓN PRELIMINAR  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Baseline mantenido

```text
Fase II HP = 100
BOSS DEF   = 13
perfil base de control:
ATQ 4
Golpe 1d6+2
```

El cerebro adaptativo no se modifica.

## 2. Corrección semántica

La matriz de counterplay exige que ante `Eco del Meridiano` una acción sin gasto de qi sea respuesta suficiente.

Por tanto los modelos TACT_* usan:

```text
Eco sólo drena si la acción del jugador gastó qi.
BASIC / DEFENDER -> 0 drenaje de Eco
```

El modelo HIST se conserva sólo como control histórico.

## 3. Modelos

```text
HIST
Tormenta +3 ATQ, 2d6+3, drain 2
Cerrar 4/8
Recordar +20 EVA
Eco 4 incondicional

TACT_A
Tormenta +2 ATQ, 2d6+2, drain 2
Cerrar 3/6
Recordar +15 EVA
Eco condicional 4

TACT_B
Tormenta +2 ATQ, 2d6+2, drain 1
Cerrar 3/6
Recordar +15 EVA
Eco condicional 3

TACT_C
Tormenta +1 ATQ, 2d6+2, drain 1
Cerrar 3/6
Recordar +10 EVA
Eco condicional 3

TACT_D
Tormenta +2 ATQ, 1d8+3, drain 1
Cerrar 3/6
Recordar +15 EVA
Eco condicional 3
```

## 4. Hallazgo de política READER

Responder automáticamente a toda Tormenta con DEFENDER produce un bucle:

```text
DEFENDER
-> recupera qi
-> jugador permanece en qi alto
-> Tormenta gana prioridad
-> volver a DEFENDER
```

También es subóptimo intentar vaciar siempre la reserva de Cerrar Alas con BASIC.

Política corregida:

- BASIC si la técnica está comprendida;
- BASIC durante la evasión preparada por Recordar;
- BASIC durante Eco para no gastar qi;
- DEFENDER ante Tormenta sólo con HP <= 14;
- fuera de eso, alternar raíz/BASIC sin repetir raíz consecutivamente;
- no reaccionar automáticamente a la reserva de Cerrar.

La lectura de intención requiere juicio, no una tabla rígida de respuestas.

## 5. Selección 5.000

Volumen de los dos finalistas:

```text
2 FX
× 2 estrategias
× 27 builds
× 5.000
=
540.000 duelos
```

### Global

| Modelo | ALTERNATE | READER |
|---|---:|---:|
| **TACT_C** | **53,56%** | **53,39%** |
| **TACT_D** | **58,82%** | **57,31%** |

### Por raíz — TACT_C

| Estrategia | Fuego | Metal | Agua |
|---|---:|---:|---:|
| ALTERNATE | 56,86% | 51,61% | 52,21% |
| READER | 58,04% | 50,58% | 51,54% |

### Por raíz — TACT_D

| Estrategia | Fuego | Metal | Agua |
|---|---:|---:|---:|
| ALTERNATE | 63,52% | 57,83% | 55,12% |
| READER | 63,23% | 54,93% | 53,78% |

Rangos READER:

```text
TACT_C 35,08% .. 76,64%
TACT_D 38,48% .. 82,76%
```

## 6. Lectura

TACT_D es el candidato más sano en aislamiento:

- acerca el toolkit mínimo fresco a ~57–59%;
- mantiene las tres raíces con rutas de victoria;
- no debilita el anti-spam;
- Tormenta sigue siendo amenaza;
- Eco tiene counterplay real;
- Cerrar/Recordar obligan a gestionar ventanas sin anular la ofensiva.

TACT_C queda como sensibilidad más dura.

No se congela TACT_D todavía porque el jugador real entra desde Fase I con recursos gastados.

## 7. Próximo bloque

Encadenar:

```text
FASE I cerrada
->
FASE II TACT_C / TACT_D
```

y medir:

- tasa de llegada a Fase II;
- HP/qi/poción al entrar;
- victoria condicional de Fase II;
- victoria total I+II;
- diferencias por raíz/build;
- invariantes de anti-spam.

## 8. Estado

```text
FASE I               CERRADA
FASE II-A control     CERRADO
TACT_C                FINALISTA
TACT_D                FINALISTA PREFERIDO EN AISLAMIENTO
TACT_D                NO CONGELAR TODAVÍA
opcionales            NO TOCAR TODAVÍA
FASE III              NO TOCAR
```

Scripts:

- `benchmark/colab/grulla-phase2-minimal-grid-v0.1.py`
- `benchmark/colab/grulla-phase2-fx-sensitivity-v0.1.py`
