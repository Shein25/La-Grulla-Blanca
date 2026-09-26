# Resultado — Grulla Fase I-B · Piel de Cobre aislada v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / BLOQUE PIEL CERRADO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance

Este bloque estudia solamente:

```text
FASE I — EL VOTO INMÓVIL
+
Piel de Cobre
```

No incluye Paso, Filamento, combinaciones de opcionales, Fase II ni Fase III.

No se repite Fase I-A.

Baseline:

```text
Grulla HP 150
ATQ 4
daño 1d6+2
Campanada 2d6+2
DEF 13 / 14
Pata Inmóvil +3 DEF siguiente ofensiva
```

Jugador de referencia: LianQi IV, 4 PT totales. La técnica raíz conserva 2 PT; Piel usa 0, 1 o 2 PT.

## 2. Semántica de Guardia ver74

Se verificó directamente `grulla-blanca_ver74.html` en `implement/3c5-npc-ver74`.

Piel NO funciona como reducción porcentual ni como buff que caduque por turnos.

La semántica real es:

```text
reserva inicial = Guardia × duración
absorción por golpe = min(daño conectado, Guardia, reserva restante)
la reserva sólo disminuye por daño realmente absorbido
un fallo no consume reserva
la burbuja no decae por rondas
se rompe cuando la reserva llega a 0
```

`duración` en estas técnicas es un multiplicador de capacidad inicial, no un contador temporal.

`DEFENDER` conserva su semántica distinta: reducción porcentual para los dos próximos impactos reales.

## 3. Configuraciones legales

Base:

```text
coste 5
Guardia 3
duración 2
reserva 6
```

Tramo 1:

```text
Cobre endurecido -> Guardia 6
Cobre flexible   -> +1 duración
Cobre sobrio     -> coste -1
```

Tramo 2:

```text
Aliento económico -> coste -1
Cobre grueso       -> Guardia 7
Placas continuas   -> +1 duración
```

Grid legal:

```text
base                1
sólo tramo 1        3
sólo tramo 2        3
tramo 1 + tramo 2   9
---------------------
total              16
```

Las reducciones de coste respetan el piso del 70% de ver74. Piel no recibe una afinidad Tierra adicional en este benchmark.

## 4. Política PIEL_READER

La política usada evita tanto el spam mecánico de Piel como la inteligencia perfecta:

```text
Golpe de Ala
-> técnica raíz

Golpe de Ala
-> técnica raíz

Campanada
-> si NO queda burbuja de Piel: lanzar Piel
-> si la burbuja sigue activa: usar técnica raíz
-> si no alcanza qi para Piel: DEFENDER

Pata Inmóvil
-> ATACAR básico
```

La poción conserva prioridad en vida crítica, igual que el READER universal de Fase I-A.

La política puede leer la reserva restante porque ver74 la muestra explícitamente en el estado activo.

## 5. Barrido de selección

Se ejecutó:

```text
27 formas raíz
× 16 configuraciones Piel
× 2 DEF
× 5.000 duelos
=
4.320.000 duelos
```

Resultado del grid:

| Configuración Piel | Coste | Guardia | Multiplicador | Reserva | DEF 13 | DEF 14 |
|---|---:|---:|---:|---:|---:|---:|
| **Cobre flexible + Cobre grueso** | 5 | 7 | 3 | 21 | **97,13%** | **95,57%** |
| Cobre endurecido + Placas continuas | 5 | 6 | 3 | 18 | 95,26% | 93,05% |
| Cobre sobrio + Cobre grueso | 4 | 7 | 2 | 14 | 94,95% | 92,83% |
| Cobre endurecido + Cobre grueso | 5 | 7 | 2 | 14 | 94,62% | 91,98% |
| Cobre grueso | 5 | 7 | 2 | 14 | 94,52% | 92,11% |
| Cobre endurecido + Aliento económico | 4 | 6 | 2 | 12 | 92,59% | 89,79% |
| Cobre endurecido | 5 | 6 | 2 | 12 | 92,14% | 89,06% |
| Cobre flexible + Placas continuas | 5 | 3 | 4 | 12 | 82,81% | 78,30% |
| Cobre sobrio + Placas continuas | 4 | 3 | 3 | 9 | 80,27% | 75,35% |
| Cobre flexible + Aliento económico | 4 | 3 | 3 | 9 | 80,23% | 75,39% |
| Cobre flexible | 5 | 3 | 3 | 9 | 80,17% | 74,95% |
| Placas continuas | 5 | 3 | 3 | 9 | 79,80% | 74,75% |
| Aliento económico | 4 | 3 | 2 | 6 | 74,90% | 69,49% |
| Cobre sobrio + Aliento económico | 4 | 3 | 2 | 6 | 74,84% | 69,43% |
| Cobre sobrio | 4 | 3 | 2 | 6 | 74,68% | 69,59% |
| Piel base | 5 | 3 | 2 | 6 | 74,38% | 69,03% |

Incluso sin invertir PT en Piel, la burbuja base supera con amplitud al READER universal.

## 6. Finalistas

El grid dejó tres finalistas consistentes para ambos valores de DEF:

```text
T1-2 + T2-2
Cobre flexible + Cobre grueso
coste 5
Guardia 7
multiplicador 3
reserva 21

T1-1 + T2-3
Cobre endurecido + Placas continuas
coste 5
Guardia 6
multiplicador 3
reserva 18

T1-3 + T2-2
Cobre sobrio + Cobre grueso
coste 4
Guardia 7
multiplicador 2
reserva 14
```

## 7. Confirmación a 20.000

Se confirmó solamente a los tres finalistas:

```text
27 formas raíz
× 3 finalistas
× 2 DEF
× 20.000 duelos
=
3.240.000 duelos
```

Resultado global confirmado:

| Configuración Piel | DEF 13 | DEF 14 |
|---|---:|---:|
| **Cobre flexible + Cobre grueso** | **97,13%** | **95,54%** |
| Cobre endurecido + Placas continuas | 95,35% | 93,14% |
| Cobre sobrio + Cobre grueso | 94,91% | 92,78% |

La confirmación reproduce prácticamente el orden y magnitud del grid de selección.

## 8. Mejor forma — detalle por raíz

Mejor forma confirmada:

```text
Cobre flexible + Cobre grueso
coste 5
Guardia 7
multiplicador 3
reserva 21
```

### DEF 13

| Raíz | Win jugador |
|---|---:|
| Fuego | 97,55% |
| Metal | 97,70% |
| Agua | 96,13% |
| **Global** | **97,13%** |

Rango entre las 27 formas raíz:

```text
91,02% – 99,12%
```

### DEF 14

| Raíz | Win jugador |
|---|---:|
| Fuego | 96,21% |
| Metal | 96,78% |
| Agua | 93,64% |
| **Global** | **95,54%** |

Rango entre las 27 formas raíz:

```text
84,77% – 98,82%
```

## 9. Comparación con READER universal

READER universal sin opcionales:

```text
DEF 13 = 60,9%
DEF 14 = 54,7%
```

Mejor Piel confirmada:

```text
DEF 13:
60,9 -> 97,13
+36,23 puntos porcentuales

DEF 14:
54,7 -> 95,54
+40,84 puntos porcentuales
```

Piel base, ya en el grid de 5.000, había dado:

```text
DEF 13 = 74,38%  -> +13,48 pp
DEF 14 = 69,03%  -> +14,33 pp
```

Por contraste, el mejor Paso confirmado aportaba aproximadamente:

```text
DEF 13 +5,35 pp
DEF 14 +4,69 pp
```

Piel tiene por tanto un impacto de otra magnitud.

## 10. Lectura de diseño

Con la semántica real de ver74, Piel ayuda **demasiado** en Fase I.

No es una mejora pequeña ni sólo una recompensa moderada por preparación:

```text
READER universal
~61% / ~55%

Piel base
~74% / ~69%

Piel especializada óptima
~97% / ~96%
```

La causa observable es la combinación de:

- absorción plana alta por golpe;
- reserva persistente que no decae por rondas;
- duración convertida en capacidad adicional;
- posibilidad de conservar una burbuja entre ventanas de Campanada;
- cuando la burbuja sigue viva, el jugador puede usar la acción de Campanada para atacar en vez de volver a defender.

Bajo esta política razonable de lectura, la mejor Piel **trivializa Fase I**. Subir de DEF13 a DEF14 no corrige el problema: la tasa global sólo baja de 97,13% a 95,54%.

Este bloque no modifica Piel ni los stats de la Grulla; sólo mide el comportamiento actual. Cualquier ajuste de balance debe decidirse aparte.

## 11. Volumen útil

```text
4.320.000 duelos — grid de selección
3.240.000 duelos — confirmación de 3 finalistas
------------------------------------------------
7.560.000 duelos útiles
```

No se cuentan Fase I-A ni Paso porque son bloques ya cerrados.

## 12. Estado

```text
FASE I-A              CERRADA
FASE I-B / PASO       CERRADO
FASE I-B / PIEL       CERRADO
FASE I-B / FILAMENTO  PENDIENTE — NO INICIAR EN ESTE BLOQUE
FASE I-C              NO INICIAR
FASE II               NO TOCAR
FASE III              NO TOCAR
```

Script reproducible:

`benchmark/colab/grulla-phase1-piel-v0.1.py`
