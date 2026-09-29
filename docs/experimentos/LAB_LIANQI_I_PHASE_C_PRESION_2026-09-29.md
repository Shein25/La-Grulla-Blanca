# LAB — LianQi I NAKED · PHASE C presión enemiga

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / PRIMER DUELO BIDIRECCIONAL / NO CANON**

## Objetivo

Introducir por primera vez daño de respuesta enemigo para decidir qué zona de
HP/DEF/Evasión del jugador y qué presión enemiga merecen seguir a PHASE C.

Este test todavía **NO** valora:

- Arrastre de Agua;
- Peso de Tierra;
- defensivas;
- equipo;
- Concordancias;
- injerto;
- Tramos;
- consumibles.

Por ello, especialmente Agua y Tierra están subvaloradas respecto de su kit
completo.

## Política del duelo

```text
Jugador actúa primero.
↓
Mientras tenga Qi suficiente:
  usa su técnica inicial.
↓
Cuando ya no alcanza:
  usa ataque básico.
↓
Si el enemigo sigue vivo:
  responde con un ataque directo simple.
```

No existe regeneración pasiva de Qi.

## Baselines ofensivos heredados de PHASE A/B

PROVISIONAL:

- enemigo: Evasión 20 / DEF 2;
- ataque básico: `1d4+4`;
- técnicas iniciales: dados narrow.

LAB:

- COMPACTA = enemigo 20 HP / jugador 24 Qi;
- EXTENDIDA = enemigo 28 HP / jugador 30 Qi.

## Barrido de presión enemiga

Precisión enemiga evaluada en el cribado inicial:

- 90;
- 100.

Modelos de daño enemigo LAB:

| ID | Dados | Media | Rango |
|---|---:|---:|---:|
| LOW_STABLE | 1d4+3 | 5.5 | 4–7 |
| MID_BELL | 2d4+1 | 6.0 | 3–9 |
| HIGH_MEDIUM | 1d6+3 | 6.5 | 4–9 |

El modelo `2d4+1` quedó como punto central más informativo: no es el de menor
presión ni el más agresivo, y conserva distribución centrada.

Precisión 100 se conserva como candidato central porque coincide con la
Precisión normal de referencia del contrato, pero **todavía no se promueve** a
perfil enemigo PROVISIONAL.

## Barrido de jugador

Se probaron combinaciones nuevas de:

- HP base: 24 / 28 / 30 / 32;
- DEF base: 0 / 1 / 2;
- Evasión base: 0 / 5 / 10.

Las raíces modifican después esos valores:

- Tierra: +10% Vida máxima;
- Viento: +10 Evasión.

## Hallazgo 1 — COMPACTA es muy indulgente

Con:

```text
COMPACTA
enemigo 20 HP
jugador 24 Qi

jugador:
24 HP
DEF 1
Evasión 0

enemigo:
Precisión 100
daño 2d4+1
```

confirmación de **100.000 duelos por raíz**:

| Raíz | Win rate | Turnos medios | HP restante medio | Usa básico |
|---|---:|---:|---:|---:|
| Fuego | 94.28% | 3.21 | 51.68% | 9.88% |
| Metal | 89.74% | 3.68 | 41.02% | 16.20% |
| Agua | 73.66% | 4.23 | 27.02% | 36.82% |
| Tierra | 87.67% | 3.91 | 40.83% | 25.45% |
| Viento | 86.44% | 4.09 | 38.79% | 29.43% |

Promedio entre raíces:

- win rate: **86.36%**;
- duración: **3.83 turnos**;
- HP restante: **39.87%**;
- fallback: **23.56%**.

Lectura:

La configuración Compacta ya es bastante segura **antes** de introducir
Control, Peso o defensivas. Si luego se añaden esas capas sin aumentar la
presión, corre riesgo de convertirse en un encuentro demasiado permisivo.

## Hallazgo 2 — EXTENDIDA genera presión real

Se refinó un punto medio:

```text
EXTENDIDA
enemigo 28 HP
jugador 30 Qi

jugador LAB:
30 HP
DEF 1
Evasión 5

enemigo LAB:
Precisión 100
daño 2d4+1
```

Confirmación de **100.000 duelos por raíz**:

| Raíz | Win rate | Turnos medios | HP restante medio | Usa básico |
|---|---:|---:|---:|---:|
| Fuego | 93.85% | 4.21 | 47.04% | 12.64% |
| Metal | 86.79% | 4.98 | 33.81% | 26.57% |
| Agua | 65.22% | 5.72 | 19.74% | 55.68% |
| Tierra | 85.19% | 5.33 | 34.49% | 38.93% |
| Viento | 82.32% | 5.57 | 31.73% | 46.29% |

Promedio entre raíces:

- win rate: **82.68%**;
- duración: **5.16 turnos**;
- HP restante: **33.36%**;
- fallback: **36.02%**.

La raíz Tierra parte efectivamente de 33 HP por su +10% de Vida.
La raíz Viento alcanza 15 Evasión por su +10 propio.

## Hallazgo 3 — DEF base cambia mucho el duelo

En la configuración Extendida con HP base 30 y Evasión base 5:

```text
DEF 0
→ win rate medio ~70.9%

DEF 1
→ win rate medio ~82.7%
```

Esto confirma que una sola unidad de DEF plana es una decisión grande en esta
escala numérica.

No debe fijarse DEF 1 por comodidad: deberá justificarse como DEF corporal/base
del sistema nuevo si termina sobreviviendo a los siguientes tests.

## Hallazgo 4 — la amplitud de daño enemigo importa

En el barrido amplio, manteniendo otras variables comparables:

- `1d4+3` produce la presión más estable y baja;
- `2d4+1` ocupa una zona media;
- `1d6+3` aumenta significativamente derrotas y reduce duración efectiva.

Por ejemplo, sobre varios perfiles Extendidos del cribado:

```text
1d4+3  → win rate agregado aprox. 71–93% según defensa
2d4+1  → aprox. 62–88%
1d6+3  → aprox. 53–82%
```

No se promueve todavía ninguno a CANON.

## Hallazgo 5 — Agua expone el hueco más importante

En el candidato Extendida P30/D1/E5, Agua gana sólo **65.22%** de los duelos,
mientras Fuego alcanza **93.85%**.

No se interpreta como necesidad automática de subir daño de Agua.

En este test Agua no está recibiendo todavía:

- valor de Arrastre;
- valor completo de Control;
- posibles interrupciones/pérdidas de acciones enemigas.

La diferencia es precisamente una señal de que **no podemos cerrar PHASE C
sólo con intercambios de daño**.

## Shortlist actual

No se promueve todavía a PROVISIONAL, pero el punto más informativo para seguir
es:

```text
DUELO EXTENDIDO LAB

Jugador:
HP base 30
Qi 30
DEF base 1
Evasión base 5

Enemigo:
HP 28
Precisión 100
Evasión 20
DEF 2
Ataque 2d4+1

Turno:
jugador primero
```

Razones:

- duración media cercana a 5 turnos;
- el Qi puede agotarse;
- el ataque básico aparece sin dominar todo el combate;
- Tierra y Viento ya expresan sus rasgos defensivos;
- existe margen visible para que Control/Peso/defensivas aporten valor;
- no es tan indulgente como COMPACTA.

## Estado

```text
PHASE A
PASS PROVISIONAL

PHASE B
PARCIAL
Qi 24–30 como banda útil
piso global sigue PENDIENTE

PHASE C
PRESSURE SCREEN COMPLETADO
NO PASS TODAVÍA
```

## Próximo test necesario

Antes de promover el perfil Extendida:

1. incorporar **Peso** de Golpe de Montaña;
2. cerrar una potencia LAB de **Arrastre** para Latigazo de Marea;
3. medir cuántas acciones enemigas evita/reduce realmente cada utilidad;
4. volver a comparar raíces;
5. después incorporar técnicas defensivas.

La prioridad es comprobar si el bajo daño directo de Agua queda compensado por
su identidad real, en lugar de corregirlo artificialmente.
