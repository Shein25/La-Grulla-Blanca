# Checkpoint — Grulla Fase I · G345_D1 + Resonancia y adaptación bilateral v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / CANDIDATO RESONANCIA x1,75 PENDIENTE DE CIERRE  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Objetivo

Validar que el rebalance de Piel no dependa únicamente de reducir sus números.

Hipótesis:

```text
G345_D1
+
Pata Inmóvil telegraphía Resonancia
+
el Golpe inmediatamente posterior castiga Piel activa
```

La intención es bilateral:

- la Grulla tiene una respuesta concreta contra absorciones persistentes;
- el jugador debe reconocer que Piel no es una solución universal;
- reaccionar mecánicamente a todo tampoco debe ser óptimo.

No se toca Fase II ni Fase III.

## 2. Piel G345_D1

```text
Base:
Guardia 3
multiplicador 1
reserva 3

Cobre endurecido:
Guardia 4

Cobre grueso:
Guardia 5

Cobre flexible + Cobre grueso:
Guardia 5
multiplicador 2
reserva 10
coste 5
```

Piel conserva:

- burbuja persistente;
- reserva que sólo baja al absorber;
- sin caducidad por rondas;
- mismos costes;
- misma identidad.

## 3. Primer modelo — Resonancia x1,50

Secuencia:

```text
Pata Inmóvil
-> +3 DEF provisional
-> prepara el siguiente Golpe de Ala

Golpe de Ala resonante
-> si conecta con Piel activa:
   daño bruto x1,50
   luego Piel absorbe normalmente

-> si falla:
   no hay daño
   Resonancia se consume
```

Aislado confirmado:

```text
Piel G345_D1 óptima
DEF13 80,96%
DEF14 76,01%
```

## 4. Piel + Filamento con Resonancia x1,50

Grid:

```text
67 legales
-> 42 deduplicadas

42 × 27 × 2 × 5.000
=
11.340.000 duelos
```

Top del grid:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **C22_F00** | **58,49%** | **46,49%** |
| C03_F03 | 52,68% | 40,92% |
| C03_F20 | 49,82% | 38,11% |
| C02_F03 | 49,69% | 38,63% |

Confirmación de cuatro candidatos:

```text
4 × 27 × 2 × 20.000
=
4.320.000 duelos
```

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **C22_F00** | **58,44%** | **46,44%** |
| C03_F03 | 52,64% | 40,78% |
| C02_F03 | 49,68% | 38,52% |
| C03_F20 | 49,57% | 38,03% |

Conclusión:

> La antigua sinergia Piel + Filamento deja de ser dominante.

## 5. Paso + Piel — política rígida

Política antigua:

- Piel se precarga;
- Paso se usa antes de Campanada;
- el jugador no reserva Paso para Resonancia.

Grid:

```text
37 × 27 × 2 × 5.000
=
9.990.000 duelos
```

Confirmación:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C22** | **53,91%** | **44,25%** |
| P02_C03 | 48,84% | 39,52% |
| P02_C02 | 46,33% | 37,39% |

## 6. Paso + Piel — adaptación explícita

Nueva política:

```text
Pata detectada
+
Piel activa
+
Paso disponible
->
reservar/castear Paso para el Golpe Resonante
```

No hay lectura del RNG futuro.

Grid:

```text
37 × 27 × 2 × 5.000
=
9.990.000 duelos
```

Confirmación:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C22** | **62,34%** | **52,53%** |
| P03_C03 | 53,18% | 44,07% |
| P03_C02 | 52,57% | 43,46% |

La adaptación mejora respecto de la política rígida, pero usar Paso en **todas** las Resonancias todavía sacrifica demasiado daño.

## 7. Triple — política adaptativa

Política:

- Piel cubre daño ordinario;
- Filamento intenta resolver Campanada;
- Paso se reserva para Resonancia;
- Pata sigue telegráfica;
- no existe RNG futuro.

Grid:

```text
154 legales
-> 88 deduplicadas

88 × 27 × 2 × 5.000
=
23.760.000 duelos
```

Top:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C02_F03** | **27,85%** | **18,74%** |
| P00_C02_F20 | 25,26% | 16,92% |
| P00_C00_F23 | 25,03% | 16,66% |

Confirmación:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **P00_C02_F03** | **28,01%** | **18,79%** |
| P00_C02_F20 | 25,29% | 16,91% |
| P00_C00_F23 | 25,15% | 16,75% |

Conclusión:

> Tener todas las herramientas y tratar de utilizarlas sistemáticamente no sustituye la economía de acciones.

## 8. Adaptaciones del jugador probadas

### DEFENDER automático después de Pata

Resultado:

```text
mejor grid aprox.
DEF13 31,99%
DEF14 25,51%
```

Fracasa porque DEFENDER reemplaza Piel y consume demasiadas ventanas ofensivas.

### Paso automático en toda Resonancia

Con x1,50:

```text
P00_C22
DEF13 62,34%
DEF14 52,53%
```

Mejora respecto de una política combinada rígida, pero sigue pagando demasiadas acciones.

### Paso sólo en riesgo

Screening de `P00_C22` a 5.000:

#### Resonancia x1,50

| Umbral para usar Paso | DEF13 | DEF14 |
|---|---:|---:|
| HP <= 10 | 81,89% | 75,73% |
| HP <= 14 | 78,74% | 71,96% |
| HP <= 18 | 74,90% | 67,70% |
| HP <= 22 | 70,75% | 62,39% |
| siempre | 62,37% | 52,62% |

#### Resonancia x1,75

| Umbral para usar Paso | DEF13 | DEF14 |
|---|---:|---:|
| HP <= 10 | 74,98% | 68,39% |
| HP <= 14 | 72,10% | 64,76% |
| HP <= 18 | 68,40% | 60,71% |
| HP <= 22 | 63,84% | 55,72% |
| siempre | 55,68% | 46,17% |

#### Resonancia x2,00

| Umbral para usar Paso | DEF13 | DEF14 |
|---|---:|---:|
| HP <= 10 | 69,31% | 62,89% |
| HP <= 14 | 66,76% | 59,49% |
| HP <= 18 | 62,91% | 55,45% |
| siempre | 50,93% | 41,73% |

Lectura:

> La adaptación correcta no es reaccionar siempre. El jugador debe valorar HP, qi y coste de acción.

## 9. Sensibilidad de fuerza de Resonancia

Piel G345_D1 óptima, jugador que no altera su política:

| Resonancia | DEF13 | DEF14 |
|---|---:|---:|
| x1,50 | 80,96% | 76,01% |
| **x1,75** | **75,27%** | **69,83%** |
| x2,00 | 70,14% | 64,69% |

Comparación con rutas cerradas:

| Ruta | DEF13 | DEF14 |
|---|---:|---:|
| READER universal | 60,90% | 54,70% |
| Paso óptimo aislado | 66,25% | 59,39% |
| Filamento óptimo aislado | 75,69% | 67,25% |
| **Piel G345_D1 + Resonancia x1,75** | **75,27%** | **69,83%** |

Esta es la razón principal para promover **x1,75 como candidato provisional**:

- Piel deja de dominar claramente el espacio opcional;
- Filamento queda prácticamente empatado;
- Paso sigue siendo útil pero no obligatorio;
- no se vuelve a nerfear Piel globalmente.

## 10. Variantes descartadas por ahora

### CRACK

Resonancia permite que Piel absorba el golpe pero destruye la reserva restante.

Resultado rígido:

```text
86,73% / 82,11%
```

Insuficiente.

### SHATTER

Resonancia ignora y destruye Piel si conecta.

La respuesta automática con Paso:

```text
~49,74% / 40,32%
```

Demasiado punitiva bajo esa política. No seleccionar todavía.

## 11. Lectura de diseño

Los tests sostienen cuatro principios:

1. **La Grulla debe adaptarse al abuso de defensas.**
2. **El jugador también debe leer al jefe, pero reaccionar automáticamente no debe ser óptimo.**
3. **Piel debe seguir siendo poderosa fuera de su counter natural.**
4. **La respuesta correcta puede ser estratégica —elección de herramienta y economía de acciones— además de reactiva.**

Esto encaja con Fase I como enseñanza del lenguaje del jefe y deja a Fase II/III espacio para adaptación más agresiva.

## 12. Estado

```text
G234_D1                         FALLBACK VALIDADO
G345_D1                         CANDIDATO PRINCIPAL

RESONANCIA x1,50                TESTEADA / PIEL AÚN MUY DOMINANTE
RESONANCIA x1,75                CANDIDATO PROVISIONAL
RESONANCIA x2,00                TESTEADA / MÁS PUNITIVA

PIEL+FILAMENTO x1,50            CERRADO EN GRID+CONFIRMACIÓN
PASO+PIEL rígido x1,50          CERRADO EN GRID+CONFIRMACIÓN
PASO+PIEL adaptativo x1,50      CERRADO EN GRID+CONFIRMACIÓN
TRIPLE adaptativo x1,50         CERRADO EN GRID+CONFIRMACIÓN

x1,75 combinaciones             PENDIENTE DE SPOT-CHECK / CONFIRMACIÓN
DEF13 / DEF14                   NO SELECCIONAR TODAVÍA
PATA +3                         SIGUE PROVISIONAL
FASE II                         NO TOCAR
FASE III                        NO TOCAR
```

## 13. Scripts

- `benchmark/colab/grulla-phase1-pata-anti-absorption-v0.1.py`
- `benchmark/colab/grulla-phase1-piel-g345d1-pata-filamento-v0.1.py`
- `benchmark/colab/grulla-phase1-multi-g345d1-resonance-v0.1.py`
