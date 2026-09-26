# Resultado — Grulla Fase I-C · combinaciones múltiples v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / FASE I-C EN PROGRESO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance

Fase I-C cruza técnicas opcionales múltiples después de cerrar sus aislamientos.

Reglas:

```text
raíz = 2 PT fijos
opcionales = máximo 2 PT adicionales
total LianQi IV = 4 PT
```

Familias:

```text
Paso + Piel
Paso + Filamento
Piel + Filamento
Paso + Piel + Filamento
```

No se toca Fase II ni Fase III.

## 2. Deduplicación

El cruce bruto contiene:

```text
3 familias de dos técnicas × 67 = 201
triple = 154
total bruto = 355
```

Se deduplican configuraciones con efecto real idéntico contra la Grulla, conservando el representante de menor gasto de PT.

Total efectivo previo al Monte Carlo:

```text
Paso + Piel       37
Paso + Filamento  42
Piel + Filamento  42
Triple             88
---------------------
Total             209
```

La equivalencia de Filamento considera el contrato de jefe único: aumentar atadura nominal por encima de 1 no aumenta acciones perdidas ni cooldown real contra la Grulla.

## 3. Política MULTI_READER

Política fija de stress-test táctico, sin lectura de RNG futuro:

```text
Golpe 1
-> si Piel está preparada y no queda burbuja: precargar Piel
-> si no: técnica raíz

Golpe 2
-> si Paso está preparado y no cubriría Campanada: precargar Paso
-> si no: técnica raíz

Campanada
-> Filamento si está legal
-> si ya existe protección Piel/Paso: técnica raíz
-> si no existe protección: Piel
-> después Paso
-> finalmente DEFENDER

Pata Inmóvil
-> ATACAR básico
```

La poción crítica conserva prioridad.

La política no conoce:

- próximo d20;
- resultado del control;
- próximo daño;
- próximo crítico;
- si Paso evitará el ataque.

## 4. Sub-barrido 1 — Paso + Piel

Configuraciones:

```text
67 legales brutas
-> 37 efectivamente distintas
```

Volumen:

```text
37 configuraciones
× 27 formas raíz
× 2 DEF
× 5.000
=
9.990.000 duelos
```

### Top DEF 13

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **P02_C02** | 2 | **89,22%** |
| P00_C22 | 2 | 88,41% |
| P20_C02 | 2 | 86,35% |
| P02_C10 | 2 | 86,07% |
| P00_C13 | 2 | 84,07% |

### Top DEF 14

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **P02_C02** | 2 | **82,70%** |
| P00_C22 | 2 | 81,58% |
| P20_C02 | 2 | 78,85% |
| P02_C10 | 2 | 78,35% |
| P00_C13 | 2 | 76,26% |

Código de la mejor forma:

```text
P02
Paso: T1 sin mejora + T2 Paso velado
coste 5
Esquiva +25%
duración 2
1 PT

C02
Piel: T1 sin mejora + T2 Cobre grueso
coste 5
Guardia 7
duración/multiplicador 2
reserva 14
1 PT
```

Resultado:

```text
DEF 13 = 89,22%
DEF 14 = 82,70%
```

Comparación con READER universal:

```text
DEF13: 60,9 -> 89,22 = +28,32 pp
DEF14: 54,7 -> 82,70 = +28,00 pp
```

### Lectura provisional

La combinación es muy fuerte, pero queda por debajo de Piel aislada óptima (~97% / ~96%).

No es una contradicción: `MULTI_READER` precarga Piel y Paso en acciones distintas para estudiar sinergia defensiva, sacrificando parte del ritmo ofensivo. Sobrevivir más no equivale automáticamente a matar antes de agotar qi/ventanas.

El mejor reparto usa 1 PT en cada técnica, no 2 PT en una sola.

## 5. Estado

```text
Paso + Piel       CERRADO EN SELECCIÓN
Paso + Filamento  PENDIENTE
Piel + Filamento  PENDIENTE
Triple             PENDIENTE
Confirmación       PENDIENTE
FASE II            NO TOCAR
```

Script:

`benchmark/colab/grulla-phase1-multi-optionals-v0.1.py`
