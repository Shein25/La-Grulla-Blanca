# Resultado — Grulla Fase I · 150 HP · grid raíz v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / CALIBRACIÓN  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance

Este documento cubre **solamente Fase I — El Voto Inmóvil**.

No incluye Fase II ni Fase III.

Baseline restaurado:

```text
HP = 150
ATQ = 4
daño básico = 1d6+2
Campanada = 2d6+2
ciclo = Golpe → Golpe → Campanada → Pata Inmóvil
```

Se comparan:

```text
DEF 13
DEF 14
```

Pata Inmóvil conserva provisionalmente el efecto actual de laboratorio:

```text
+3 DEF contra la siguiente acción ofensiva
```

Este último valor todavía no está cerrado históricamente.

## 2. Builds

Se probaron las 27 combinaciones raíz legales de maestría 2:

```text
3 raíces
× 3 opciones de tramo 1
× 3 opciones de tramo 2
= 27 builds
```

Raíces:

- Fuego / Palma Ardiente;
- Metal / Filo de Qi Metálico;
- Agua / Látigo de Agua.

Jugador preparado de referencia:

```text
LianQi IV
28 HP
110 qi
+3 ATQ por consagraciones
gear de sensibilidad: +2 ATQ / +7 DEF / básico 1d8
1 poción de sangre
```

## 3. Estrategias

### SPAM

Usa la técnica raíz siempre que tenga qi.

Si se queda sin qi, usa ataque básico.

No lee la Campanada.

### ALTERNATE

Alterna:

```text
técnica raíz
→ ATACAR básico
→ técnica raíz
→ ATACAR básico
```

y usa una poción en vida baja.

No interpreta el ciclo de la Grulla.

### READER

Lee Fase I:

- técnica durante Golpe de Ala;
- DEFENDER frente a Campanada;
- ATACAR básico durante Pata Inmóvil;
- una poción si cae a vida crítica.

No usa Paso, Piel ni Filamento.

## 4. Volumen

```text
27 builds
× 2 valores de DEF
× 3 estrategias
× 20.000 duelos
=
3.240.000 duelos
```

Monte Carlo reproducible:

`benchmark/colab/grulla-phase1-root-grid-v0.1.py`

El script es compatible con Google Colab.

Con 20.000 duelos por escenario, una tasa cercana al 50% tiene un error Monte Carlo aproximado de ±0,7 puntos porcentuales al 95%.

## 5. Resultados — DEF 13

| Estrategia | Fuego | Metal | Agua | Promedio global |
|---|---:|---:|---:|---:|
| SPAM | 38,3% | 39,1% | 35,1% | **37,5%** |
| ALTERNATE | 38,0% | 37,2% | 39,6% | **38,3%** |
| READER | 61,5% | 59,5% | 61,8% | **60,9%** |

Rango entre builds para READER:

```text
mínimo global ≈ 39,3%
máximo global ≈ 80,5%
```

## 6. Resultados — DEF 14

| Estrategia | Fuego | Metal | Agua | Promedio global |
|---|---:|---:|---:|---:|
| SPAM | 33,6% | 35,3% | 29,1% | **32,7%** |
| ALTERNATE | 32,6% | 32,4% | 34,0% | **33,0%** |
| READER | 55,2% | 53,9% | 55,0% | **54,7%** |

Rango entre builds para READER:

```text
mínimo global ≈ 32,3%
máximo global ≈ 75,8%
```

## 7. Valor de leer la Fase I

La mejora del lector respecto de alternar sin leer es:

```text
DEF 13:
38,3% → 60,9%
+22,6 puntos porcentuales

DEF 14:
33,0% → 54,7%
+21,7 puntos porcentuales
```

La Fase I ya recompensa fuertemente reconocer Campanada y no malgastar la ofensiva durante Pata Inmóvil.

## 8. Builds extremas — READER

### DEF 13

#### Fuego

Peor:

```text
Chispa perseguidora
+ Respiración frugal
≈ 51,5%
```

Mejor:

```text
Ascua persistente
+ Pulso certero
≈ 78,3%
```

#### Metal

Peor:

```text
Filo oportunista
+ Corte del vacío
≈ 39,3%
```

Mejor:

```text
Filo pesado
+ Corte dirigido
≈ 75,3%
```

#### Agua

Peor:

```text
Onda desgarradora
+ Cauce continuo
≈ 45,3%
```

Mejor:

```text
Azote profundo
+ Curva imprevisible
≈ 80,5%
```

### DEF 14

#### Fuego

Peor:

```text
Chispa perseguidora
+ Respiración frugal
≈ 44,2%
```

Mejor:

```text
Ascua persistente
+ Pulso certero
≈ 74,3%
```

#### Metal

Peor:

```text
Filo oportunista
+ Corte del vacío
≈ 32,3%
```

Mejor:

```text
Filo pesado
+ Corte dirigido
≈ 72,6%
```

#### Agua

Peor:

```text
Onda desgarradora
+ Cauce continuo
≈ 37,0%
```

Mejor:

```text
Azote profundo
+ Curva imprevisible
≈ 75,8%
```

## 9. Lectura provisional

### DEF 13

Produce una Fase I exigente pero con una recompensa clara por leer el patrón:

```text
lector medio ≈ 61%
```

### DEF 14

Endurece todas las formas y lleva al lector medio a:

```text
≈ 55%
```

pero algunas ramas legítimas bajan a aproximadamente un tercio de victoria antes de incorporar técnicas opcionales.

Por eso **todavía no se selecciona DEF 13 ni DEF 14**.

Primero hay que medir cuánto aportan:

- Paso de Nube;
- Piel de Cobre;
- Filamento.

## 10. Relación con la regla anti-spam

SPAM puede ganar Fase I aislada.

Eso es deliberadamente compatible con el diseño:

```text
Fase I
→ PROGRAMADA
→ observa

transición a Fase II
→ recuerda la técnica dominante
→ counter aprendido
```

La regla:

> 100% la misma skill = 0% victoria

se aplica al **encuentro completo de tres fases**, no a la obligación de morir durante Fase I.

## 11. Próximo bloque permitido

Fase I-B:

```text
Paso / Piel / Filamento
de forma aislada
+
ramas legales
+
presupuesto máximo de 4 PT
```

No avanzar a Fase II hasta cerrar Fase I-C y documentarla.
