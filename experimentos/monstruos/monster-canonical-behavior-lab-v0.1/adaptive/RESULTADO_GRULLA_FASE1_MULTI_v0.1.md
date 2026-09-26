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


## 5. Sub-barrido 2 — Paso + Filamento

Configuraciones:

```text
67 legales brutas
-> 42 efectivamente distintas
```

Volumen:

```text
42 configuraciones
× 27 formas raíz
× 2 DEF
× 5.000
=
11.340.000 duelos
```

### Top DEF 13

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **P02_F03** | 2 | **45,09%** |
| P00_F23 | 2 | 44,16% |
| P02_F20 | 2 | 42,60% |
| P20_F03 | 2 | 39,94% |
| P00_F33 | 2 | 38,74% |

### Top DEF 14

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **P02_F03** | 2 | **35,82%** |
| P00_F23 | 2 | 34,34% |
| P02_F20 | 2 | 33,62% |
| P00_F33 | 2 | 31,21% |
| P20_F03 | 2 | 31,00% |

Mejor forma:

```text
P02 = Paso velado
+25% Esquiva
duración 2
1 PT

F03 = Lazo medido
Filamento base de control
+ 1d4 al atar
1 PT
```

Resultado:

```text
DEF 13 = 45,09%
DEF 14 = 35,82%
```

Frente al READER universal:

```text
DEF13: 60,9 -> 45,09 = -15,81 pp
DEF14: 54,7 -> 35,82 = -18,88 pp
```

### Lectura provisional

La combinación no es rota; bajo `MULTI_READER` es directamente ineficiente.

El patrón explica el resultado:

```text
Golpe 1 -> raíz
Golpe 2 -> Paso
Campanada -> Filamento
Pata -> básico
```

En cada ciclo sólo queda una de las dos ventanas de Golpe para la técnica raíz. Paso consume qi y una acción para respaldar un Filamento que ya intenta cancelar Campanada. La defensa redundante mejora seguridad, pero reduce demasiado el daño sostenido y agota recursos antes de terminar 150 HP.

Esto demuestra por qué Fase I-C no puede juzgar una build sólo por cantidad de herramientas: la política de uso importa tanto como la build.


## 6. Sub-barrido 3 — Piel + Filamento

Configuraciones:

```text
67 legales brutas
-> 42 efectivamente distintas
```

Volumen:

```text
42 configuraciones
× 27 formas raíz
× 2 DEF
× 5.000
=
11.340.000 duelos
```

### Top DEF 13

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **C02_F03** | 2 | **93,08%** |
| C02_F20 | 2 | 92,12% |
| C22_F00 | 2 | 91,30% |
| C10_F03 | 2 | 90,30% |
| C10_F20 | 2 | 89,29% |

### Top DEF 14

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **C02_F03** | 2 | **86,60%** |
| C02_F20 | 2 | 85,24% |
| C22_F00 | 2 | 83,94% |
| C10_F03 | 2 | 82,54% |
| C02_F02 | 2 | 81,27% |

Mejor forma:

```text
C02 = Cobre grueso
Guardia 7
reserva 14
1 PT

F03 = Lazo medido
Filamento base de control
+ 1d4 al atar
1 PT
```

Resultado:

```text
DEF 13 = 93,08%
DEF 14 = 86,60%
```

Frente al READER universal:

```text
DEF13: 60,9 -> 93,08 = +32,18 pp
DEF14: 54,7 -> 86,60 = +31,90 pp
```

### Lectura provisional

La combinación sigue siendo excesivamente fuerte en Fase I, aunque queda por debajo de Piel aislada óptima.

`MULTI_READER` usa:

```text
Golpe 1 -> precarga Piel
Golpe 2 -> raíz
Campanada -> Filamento
Pata -> básico
```

Si Filamento acierta, la Campanada desaparece y la reserva de Piel queda disponible para golpes posteriores. Si falla, Piel amortigua la ventana peligrosa.

La sinergia es real y robusta, pero paga una acción ofensiva adicional por ciclo.


## 7. Sub-barrido 4 — Paso + Piel + Filamento

Configuraciones:

```text
154 legales brutas
-> 88 efectivamente distintas
```

Volumen:

```text
88 configuraciones
× 27 formas raíz
× 2 DEF
× 5.000
=
23.760.000 duelos
```

### Top DEF 13

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **P00_C02_F03** | 2 | **53,00%** |
| P00_C02_F20 | 2 | 49,60% |
| P00_C10_F03 | 2 | 45,69% |
| P00_C22_F00 | 2 | 43,94% |
| P00_C10_F20 | 2 | 42,91% |

### Top DEF 14

| Configuración | PT opcionales | Win |
|---|---:|---:|
| **P00_C02_F03** | 2 | **39,28%** |
| P00_C02_F20 | 2 | 36,19% |
| P00_C10_F03 | 2 | 32,99% |
| P00_C22_F00 | 2 | 30,80% |
| P00_C10_F20 | 2 | 30,33% |

Mejor forma:

```text
P00 = Paso base
0 PT

C02 = Cobre grueso
Guardia 7
reserva 14
1 PT

F03 = Lazo medido
+1d4 al atar
1 PT
```

Resultado:

```text
DEF 13 = 53,00%
DEF 14 = 39,28%
```

Frente al READER universal:

```text
DEF13: 60,9 -> 53,00 = -7,90 pp
DEF14: 54,7 -> 39,28 = -15,42 pp
```

### Lectura provisional

El triple no trivializa la fase bajo esta política: la sobredefiende y pierde demasiada economía de acciones.

Cuando las tres herramientas están preparadas, el patrón de apertura tiende a ser:

```text
Golpe 1 -> Piel
Golpe 2 -> Paso
Campanada -> Filamento
Pata -> básico
```

Mientras haya qi, puede transcurrir un ciclo completo sin una técnica raíz ofensiva.

Por tanto:

> Más herramientas disponibles no implican más DPS ni mayor probabilidad de victoria si se usan todas por automatismo.

Ésta es precisamente una propiedad deseable para el diseño general de la Grulla: el jugador debe elegir qué respuesta merece una acción, no pulsar todas las defensas porque las posee.

## 8. Confirmación — Paso + Piel

Se confirmaron únicamente los tres finalistas estables del grid:

```text
3 configuraciones
× 27 formas raíz
× 2 DEF
× 20.000
=
3.240.000 duelos
```

Resultado:

| Configuración | DEF 13 | DEF 14 |
|---|---:|---:|
| **P02_C02** | **89,26%** | **82,58%** |
| P00_C22 | 88,37% | 81,58% |
| P20_C02 | 86,27% | 78,94% |

La confirmación conserva el mismo orden del barrido de 5.000.

Mejor forma confirmada:

```text
P02 = Paso velado
+25% Esquiva
duración 2
1 PT

C02 = Cobre grueso
Guardia 7
reserva 14
1 PT
```

Frente al READER universal:

```text
DEF13: 60,9 -> 89,26 = +28,36 pp
DEF14: 54,7 -> 82,58 = +27,88 pp
```

## 9. Confirmación — Paso + Filamento

Se confirmaron los tres finalistas del grid:

```text
3 configuraciones
× 27 formas raíz
× 2 DEF
× 20.000
=
3.240.000 duelos
```

Resultado:

| Configuración | DEF 13 | DEF 14 |
|---|---:|---:|
| **P02_F03** | **45,20%** | **35,74%** |
| P00_F23 | 44,01% | 34,69% |
| P02_F20 | 42,64% | 33,73% |

La confirmación conserva el orden del grid.

Mejor forma confirmada:

```text
P02 = Paso velado
+25% Esquiva
duración 2
1 PT

F03 = Lazo medido
Filamento base
+1d4 al atar
1 PT
```

Frente al READER universal:

```text
DEF13: 60,9 -> 45,20 = -15,70 pp
DEF14: 54,7 -> 35,74 = -18,96 pp
```

La lectura de selección queda confirmada: Paso y Filamento se solapan demasiado frente a Campanada bajo MULTI_READER. La seguridad extra no compensa la pérdida de ofensiva.

## 10. Confirmación — Piel + Filamento

Se confirmaron los tres finalistas estables:

```text
3 configuraciones
× 27 formas raíz
× 2 DEF
× 20.000
=
3.240.000 duelos
```

Resultado:

| Configuración | DEF 13 | DEF 14 |
|---|---:|---:|
| **C02_F03** | **93,09%** | **86,68%** |
| C02_F20 | 92,11% | 85,23% |
| C22_F00 | 91,28% | 83,90% |

Mejor forma confirmada:

```text
C02 = Cobre grueso
Guardia 7
reserva 14
1 PT

F03 = Lazo medido
Filamento base
+1d4 al atar
1 PT
```

Frente al READER universal:

```text
DEF13: 60,9 -> 93,09 = +32,19 pp
DEF14: 54,7 -> 86,68 = +31,98 pp
```

La confirmación sostiene la lectura provisional: Piel cubre el fallo de Filamento y Filamento conserva la reserva cuando cancela Campanada. La combinación es robusta y demasiado fuerte para Fase I en su estado actual.

## 11. Estado

```text
Paso + Piel       CERRADO EN SELECCIÓN
Paso + Filamento  CERRADO EN SELECCIÓN
Piel + Filamento  CERRADO EN SELECCIÓN
Triple             CERRADO EN SELECCIÓN
Confirmación       PENDIENTE
FASE II            NO TOCAR
```

Script:

`benchmark/colab/grulla-phase1-multi-optionals-v0.1.py`
