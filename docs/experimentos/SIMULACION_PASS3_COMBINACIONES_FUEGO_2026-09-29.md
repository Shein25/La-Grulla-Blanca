> ⚠️ **HISTÓRICO / NO USAR CIFRAS PARA BALANCE DEL SISTEMA NUEVO.**  
> Este informe fue producido antes de declarar obsoleto el sistema numérico legacy. Puede conservar hallazgos de arquitectura, interacción o metodología, pero cualquier resultado que dependa de HP/Qi/perfiles enemigos/DEF/Evasión/daño derivados o inspirados en `ver74` debe repetirse con el marco `experimentos/balance_nuevo/`. No convertir estadísticas legacy al contrato nuevo.

# Pass 3 — 27 combinaciones de ramas · Fuego

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **SIMULACIÓN / SIN CAMBIOS CANÓNICOS**

## 0. Protocolo

Se evalúan las 27 combinaciones posibles de Tramo I × Tramo II × Tramo III para cada técnica de Fuego.

Fuera: equipo, injertos, Concordancias, consumibles y buffs externos.

Dentro: raíz Fuego (+10% daño directo y +5 pp crítico), ramas propias, crítico, DOT, Absorción y Calor.

Perfiles principales:

~~~text
COMMON: HP 18 · DEF 3 · paquete entrante 5
ELITE:  HP 34 · DEF 6 · paquete entrante 8
~~~

Horizonte principal: 6 turnos.

---

# 1. Palma Ardiente — 27/27 simulables

Claves: DOT = Quemadura · DIR = daño directo · EFF = eficiencia.

## 1.1 COMMON

| build | TTK | HP final | Qi |
|---|---:|---:|---:|
| DIR-DIR-DIR | ~1.85 | ~23.74 | ~12.96 |
| DOT-DIR-DIR | ~1.90 | ~23.52 | ~13.28 |
| DIR-DIR-EFF | ~1.90 | ~23.52 | ~11.38 |
| DOT-EFF-DIR | ~1.90 | ~23.51 | ~9.49 |

La ruta Directa pura conserva la mejor presión contra enemigos frágiles, pero varias mezclas llegan casi al mismo TTK gastando menos Qi.

## 1.2 ELITE

| build | kill | TTK | HP final | Qi |
|---|---:|---:|---:|---:|
| DOT-DIR-DIR | 100% | **~2.99** | **~12.08** | ~20.93 |
| DIR-DIR-DOT | 100% | ~2.99 | ~12.07 | ~20.93 |
| DOT-DIR-EFF | 100% | ~3.00 | ~12.00 | **18.00** |
| DOT-DIR-DOT | 100% | ~3.00 | ~12.00 | 21.00 |
| DIR-DIR-DIR | 100% | ~3.59 | ~7.26 | ~25.15 |
| DIR-DIR-EFF | 100% | ~3.71 | ~6.29 | ~22.28 |

### F3-PALMA-01

La ruta Directa pura no domina. DOT-DIR-DIR conserva Quemadura de Tramo I y suma las ramas directas posteriores. Contra ELITE mejora TTK, Vida final y Qi respecto de DIR-DIR-DIR, aunque la ruta pura sigue siendo mejor contra COMMON.

### F3-PALMA-02

DOT-DIR-EFF es una build mixta muy eficiente contra ELITE: ~3 turnos, 18 Qi y ~12 HP final. Se mantiene en observación, sin nerf.

---

# 2. Círculo de las Cien Ascuas — 27/27 simulables

Stress: 3 COMMON simultáneos, HP18, DEF3, paquete5.

| build | clear | TTK | HP final | Qi |
|---|---:|---:|---:|---:|
| DIR-DIR-DIR | **~61.9%** | ~2.97 | ~2.89 | ~31.19 |
| EFF-DIR-DIR | ~48.2% | ~2.99 | ~1.94 | ~27.22 |
| DOT-EFF-DIR | ~47.7% | ~2.99 | ~1.95 | ~22.24 |
| DOT-DIR-DIR | ~47.4% | ~2.99 | ~1.92 | ~29.61 |
| DIR-DOT-DIR | ~47.4% | ~2.98 | ~1.95 | ~24.66 |
| DOT-DOT-DOT | ~47.2% | ~2.98 | ~1.93 | ~22.17 |
| DIR-EFF-DOT | ~46.7% | ~2.99 | ~1.88 | ~19.69 |

### F3-CIRCULO-01

Directa pura mantiene ventaja clara de supervivencia grupal: más daño frontal mata enemigos antes y reduce cuántos ataques llegan a ocurrir.

### F3-CIRCULO-02

Muchas mezclas se concentran alrededor de 47% de clear con costes muy distintos. La técnica es muy sensible al umbral de matar antes de la siguiente ronda; conviene probar HP16–22 y paquete4 además de este punto.

---

# 3. Respiración del Cuerpo-Horno

Prueba: turno 1 Horno, luego Palma Directa completa contra ELITE.

Claves: BAR = barrera · CONV = conversión · EFF = eficiencia.

## 3.1 Hueco detectado

Calor Acumulado de Tramo III sólo declara su efecto para la ruta completa: 60% del daño absorbido a Calor y tope 15% HP.

De las 9 combinaciones que eligen CONV en Tramo III, sólo CONV-CONV-CONV tiene semántica completa. Ocho combinaciones mixtas quedan **NO SIMULABLES** sin inventar una regla standalone.

## 3.2 19 combinaciones con semántica suficiente

| build | TTK | HP final | Qi | Calor usado |
|---|---:|---:|---:|---:|
| CONV-CONV-EFF | **~3.72** | ~10.24 | **~25.04** | ~1.8 |
| CONV-CONV-CONV | ~3.72 | ~10.20 | ~26.07 | ~2.4 |
| CONV-CONV-BAR | ~3.73 | **~12.19** | ~26.08 | ~2.7 |
| CONV-BAR-EFF | ~3.85 | ~11.21 | ~25.94 | ~1.4 |
| BAR-CONV-BAR | ~3.85 | **~12.20** | ~26.95 | ~1.4 |
| BAR-BAR-BAR | ~4.59 | ~9.24 | ~32.16 | 0 |
| EFF-EFF-EFF | ~4.59 | ~5.29 | ~30.12 | 0 |

### F3-HORNO-01

Conversión pura no es automáticamente la mejor. CONV-CONV-EFF conserva casi el mismo TTK gastando menos Qi; CONV-CONV-BAR conserva casi el mismo TTK con más Vida final.

### F3-HORNO-02

Barrera pura y Eficiencia pura quedan detrás en este escenario ELITE, pero no se buffean todavía: pueden ganar con paquetes más grandes o combates más largos.

---

# 4. Cierre provisional de Fuego

No modificar todavía Palma DOT, Palma Directa, Círculo Directo ni Conversión de Horno.

Builds mixtas relevantes:

~~~text
Palma:  DOT-DIR-DIR · DOT-DIR-EFF
Círculo: EFF-DIR-DIR · DOT-EFF-DIR · DIR-EFF-DOT
Horno: CONV-CONV-EFF · CONV-CONV-BAR · CONV-BAR-EFF
~~~

El Pass 3 confirma que mezclar rutas puede superar una especialización pura en ciertos perfiles sin dominar todos los escenarios.
