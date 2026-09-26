# Cierre experimental — Grulla Blanca · Fase II v0.1

**Fecha:** 2026-09-26  
**Estado:** FASE II CERRADA EXPERIMENTALMENTE  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`  
**Producción:** `ver74` sin cambios

## 1. Alcance cerrado

Queda cerrada:

```text
FASE II — LAS ALAS RECUERDAN
```

Fase I permanece congelada y no se reabre.

No se toca Fase III en este bloque.

## 2. Contrato final de Fase II

```text
HP                     100
DEF                    13
ATQ base               4

Golpe de Ala           1d4
Tormenta Mil Plumas    1d6+1
bonus ATQ Tormenta     +0
drain Tormenta         1 qi si hace daño

Cerrar Alas            absorción 3 / reserva 6
Recordar el Filo       +10 EVA siguiente ofensiva
Eco del Meridiano      drain 3 condicional a gasto de qi
```

El cerebro permanece sin cambios:

- Golpe base score 30;
- Tormenta base 28 y responde a qi alto / HP bajo;
- Cerrar Alas responde a racha ofensiva, daño fuerte y HP propio bajo;
- Recordar el Filo responde a repetición;
- Eco responde a gasto consecutivo de qi;
- anti-spam interno de intenciones;
- sin lectura de acción futura.

## 3. Memoria y aprendizaje

Fase II recibe de Fase I sólo un resumen semántico.

Reglas congeladas:

```text
2+ usos exclusivos en Fase I
+ ninguna BASIC/alternativa real
-> Fase II puede entrar recordando esa técnica

3 usos consecutivos de una misma técnica dentro de Fase II
-> técnica comprendida

la tercera repetición se resuelve
la siguiente repetición queda completamente suprimida

BASIC u otra técnica
-> rompe el lock

DEFENDER / RECOVER
-> NO borran el conocimiento
```

Counters por rol:

```text
ofensiva       -> TRAZO VACÍO
esquiva        -> PULSO FIJADO
guardia        -> RESONANCIA INTERNA
control        -> ANCLA DEL VOTO
fortificación  -> CAMPANA INVERSA
```

## 4. Anti-spam

Los benchmarks mínimos confirmaron:

```text
SPAM                0%
SPAM + DEFENDER     0%
```

El contrato duro sigue funcionando con 100 HP.

La Grulla no necesita subir estadísticas para castigar una única técnica repetida.

## 5. Lectura vs rigidez

En cadena real Fase I -> Fase II con CHAIN_A:

```text
READER
FII condicional     31,70%
I+II                20,30%

ALTERNATE
FII condicional     26,86%
I+II                10,98%
```

El jugador que interpreta Recordar, Eco y Tormenta supera al que sólo alterna mecánicamente.

Por tanto la adaptación del jugador tiene valor real.

## 6. Opcionales en cadena

Confirmación:

```text
3 herramientas
× 27 builds raíz
× 20.000
=
1.620.000 cadenas I→II
```

| Herramienta | Llega FII | FII condicional | I+II |
|---|---:|---:|---:|
| Paso | 66,15% | **19,35%** | 13,49% |
| Piel | 75,15% | **28,12%** | 21,86% |
| Filamento | 75,73% | **22,86%** | 17,95% |

Conclusiones:

- ninguna opcional trivializa Fase II;
- ninguna es obligatoria;
- reutilizarlas dentro de Fase II cambia poco el resultado;
- la mayor diferencia viene del desgaste heredado desde Fase I;
- las tres raíces conservan rutas de victoria.

## 7. Counterplay universal

La matriz sigue garantizando respuesta universal para toda intención de Fase II:

```text
Golpe de Ala       BASIC / DEFEND
Tormenta           DEFEND
Cerrar Alas        BASIC
Recordar el Filo   BASIC
Eco Meridiano      BASIC / DEFEND
```

Paso, Piel y Filamento siguen siendo mejoras opcionales, no llaves.

## 8. Stress de recursos — cero qi

Se forzó una entrada extrema:

```text
HP       28
qi        0
poción    0
opcionales 0
```

10.000 duelos por build:

| Raíz | Victoria media | Mín | Máx |
|---|---:|---:|---:|
| Fuego | 17,45% | 15,33% | 19,60% |
| Metal | 23,32% | 20,92% | 26,84% |
| Agua | 33,56% | 30,61% | 38,57% |
| **Global** | **24,78%** | **15,33%** | **38,57%** |

Conclusión:

> Eco/Tormenta no generan soft-lock de recursos.

Incluso con qi cero, BASIC mantiene una ruta real de victoria.

## 9. CHAIN_A congelado

Los modelos anteriores quedan supersedidos como baseline:

```text
TACT_C     histórico / superseded
TACT_D     histórico / superseded

CHAIN_A    SELECCIONADO
```

CHAIN_A:

```text
Golpe de Ala     1d4
Tormenta         1d6+1
bonus ATQ        +0

Cerrar Alas      3 / reserva 6
Recordar Filo    +10 EVA
Eco              drain 3 condicional
Tormenta drain   1
```

## 10. Qué hace desafiante a Fase II

La dificultad no proviene de inflar daño.

Proviene de:

1. memoria heredada;
2. reconocimiento de repetición;
3. counters específicos por técnica;
4. presión de qi;
5. defensas que responden al patrón ofensivo;
6. necesidad de variar de verdad;
7. coste de reaccionar demasiado;
8. recursos heredados desde Fase I.

Esto preserva la filosofía bilateral:

> La Grulla aprende al jugador y el jugador debe aprender a la Grulla.

## 11. Evidencia lógica ya cubierta por tests

`grulla-boss-brain.test.mjs` valida entre otros:

- Fase II prioriza Recordar ante repetición;
- distingue qi-heavy play;
- hereda sólo resumen de Fase I;
- pure single-skill entra hard-countered;
- tres repeticiones bloquean una técnica;
- variar con otra técnica rompe el lock;
- DEFENDER/RECOVER no borran memoria;
- BASIC sí rompe el conocimiento;
- Trazo Vacío / Pulso Fijado / Resonancia Interna / Ancla del Voto / Campana Inversa;
- anuncio inmediato del counter;
- toolkit mínimo raíz + BASIC evita hard-lock.

`grulla-counterplay-matrix.test.mjs` valida que ninguna intención dependa de opcionales.

## 12. Archivos de cierre

- `adaptive/RESULTADO_GRULLA_FASE2_MINIMAL_CONTROL_v0.1.md`
- `adaptive/RESULTADO_GRULLA_FASE2_FX_SENSIBILIDAD_v0.1.md`
- `adaptive/RESULTADO_GRULLA_FASE12_CHAIN_RECALIBRATION_v0.2.md`
- `adaptive/RESULTADO_GRULLA_FASE12_OPTIONALS_v0.1.md`
- `benchmark/colab/grulla-phase12-chain-recalibration-v0.2.py`
- `benchmark/colab/grulla-phase12-chain-optionals-v0.1.py`

## 13. Estado final

```text
FASE I                         CERRADA / CONGELADA
FASE II                        CERRADA / CONGELADA

FASE II HP                     100
FASE II DEF                    13
CHAIN_A                        CONGELADO
CEREBRO                        CONGELADO
MEMORIA                        CONGELADA
ANTI-SPAM                      CONGELADO
COUNTERPLAY                    CONGELADO

PASO                           VALIDADO
PIEL                           VALIDADA
FILAMENTO                      VALIDADO
ZERO-QI                        SIN SOFT-LOCK

VER74                          SIN CAMBIOS
INTEGRACIÓN PRODUCTIVA         NO REALIZADA

FASE III                       PENDIENTE
```

La siguiente etapa del laboratorio, cuando se continúe, es:

```text
FASE III — LA CAMPANA SIN DUEÑO
```
