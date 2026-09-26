# Resultado — Grulla Fase I-B · Paso de Nube aislado v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / BLOQUE PASO CERRADO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance

Este bloque estudia solamente:

```text
FASE I — EL VOTO INMÓVIL
+
Paso de Nube
```

No incluye:

- Piel de Cobre;
- Filamento;
- combinaciones entre opcionales;
- Fase II;
- Fase III.

No se repite Fase I-A.

Baseline:

```text
Grulla HP 150
ATQ 4
daño 1d6+2
Campanada 2d6+2
DEF 13 / 14
Pata Inmóvil +3 DEF siguiente acción
```

## 2. Presupuesto legal

LianQi IV dispone de 4 PT.

Fase I-A mantiene:

```text
2 PT en técnica raíz
```

Por tanto Paso puede usar:

```text
0, 1 o 2 PT
```

Configuraciones probadas:

```text
base                1
sólo tramo 1        3
sólo tramo 2        3
tramo 1 + tramo 2   9
---------------------
total               16
```

Cada una se cruza contra las 27 formas raíz.

## 3. Uso táctico probado

Estrategia `PASO_READER`:

```text
Golpe de Ala
→ técnica raíz

Golpe de Ala
→ técnica raíz

Campanada
→ Paso de Nube
→ si falta qi: DEFENDER

Pata Inmóvil
→ ATACAR básico
```

Una poción conserva prioridad en vida crítica, igual que el READER de Fase I-A.

Paso usa exactamente la semántica de ver74:

- base +15% Esquiva;
- duración base 2 turnos;
- coste base 5 qi;
- se activa antes de la respuesta enemiga;
- su duración decae por turnos.

## 4. Barrido de selección

Se ejecutó:

```text
27 formas raíz
× 16 configuraciones de Paso
× 2 DEF
× 5.000 duelos
=
4.320.000 duelos
```

El barrido separó tres finalistas:

```text
T1-1 + T2-2
Paso prolongado + Paso velado
coste 5
Esquiva +25%
duración 3

T1-1 + T2-3
Paso prolongado + Aliento sostenido
coste 5
Esquiva +15%
duración 4

T1-2 + T2-3
Paso corto + Aliento sostenido
coste 5
Esquiva +22%
duración 3
```

## 5. Confirmación finalistas

Se ejecutó:

```text
27 formas raíz
× 3 finalistas
× 2 DEF
× 20.000 duelos
=
3.240.000 duelos
```

Resultado global:

| Configuración Paso | DEF 13 | DEF 14 |
|---|---:|---:|
| **Prolongado + Velado** | **66,25%** | **59,39%** |
| Prolongado + Aliento | 57,79% | 51,23% |
| Corto + Aliento | 57,83% | 51,07% |

La diferencia de la mejor forma es suficientemente amplia para no atribuirse a ruido Monte Carlo.

## 6. Mejor forma — por raíz

### DEF 13

| Raíz | Win jugador |
|---|---:|
| Fuego | 64,59% |
| Metal | 65,62% |
| Agua | 68,54% |
| **Global** | **66,25%** |

Rango de builds:

```text
46,11% – 86,26%
```

### DEF 14

| Raíz | Win jugador |
|---|---:|
| Fuego | 57,31% |
| Metal | 59,76% |
| Agua | 61,11% |
| **Global** | **59,39%** |

Rango de builds:

```text
38,03% – 81,69%
```

## 7. Comparación con READER universal de Fase I-A

READER sin opcionales:

```text
DEF 13 = 60,9%
DEF 14 = 54,7%
```

Mejor Paso:

```text
DEF 13 = 66,25%
→ +5,35 puntos porcentuales

DEF 14 = 59,39%
→ +4,69 puntos porcentuales
```

Paso bien construido da una ventaja real, pero no trivializa la fase.

## 8. Paso base no es automáticamente mejor que DEFENDER

Se confirmó también la forma sin PT:

```text
Paso base
coste 5
Esquiva +15%
duración 2
```

Resultados:

```text
DEF 13 = 39,60%
DEF 14 = 33,40%
```

Es notablemente peor que el READER universal.

Esto es coherente con la mecánica:

- DEFENDER reduce de forma fiable los próximos impactos;
- Paso base sólo aumenta la probabilidad de evitar por completo la Campanada;
- la segunda ronda de duración cae sobre Pata Inmóvil, que no ataca.

Por tanto encontrar el manual no equivale automáticamente a obtener una respuesta superior.

## 9. Por qué gana Prolongado + Velado

```text
+25% Esquiva
+
3 turnos
```

La tercera ronda de duración permite:

```text
Campanada
→ Pata Inmóvil
→ siguiente Golpe de Ala
```

Así la inversión protege dos ataques reales:

- la Campanada;
- el primer Golpe del siguiente ciclo.

Esto explica por qué supera tanto a:

```text
+25% / 2 turnos
```

como a:

```text
+15% / 4 turnos
```

## 10. Lectura de diseño

Paso cumple el objetivo buscado:

```text
sin Paso
→ el jugador competente puede ganar

Paso base
→ no es botón de victoria

Paso bien especializado
→ recompensa preparación
→ +~5 pp frente al lector universal
→ no trivializa Fase I
```

No se recomienda nerfear Paso ni subir stats de la Grulla por este resultado.

## 11. Volumen útil

Trabajo nuevo de selección y confirmación:

```text
4.320.000 duelos — grid completo de 16 configuraciones
3.240.000 duelos — confirmación de 3 finalistas
---------------------------------------------------
7.560.000 duelos útiles
```

No se cuentan reruns de extracción del mismo escenario como evidencia nueva.

## 12. Estado

```text
FASE I-A  → CERRADA
FASE I-B / PASO → CERRADO
FASE I-B / PIEL → PENDIENTE
FASE I-B / FILAMENTO → PENDIENTE
FASE I-C → NO INICIAR TODAVÍA
```

Script reproducible:

`benchmark/colab/grulla-phase1-paso-v0.1.py`
