# ETAPA 12 — Espejo de Luna completo

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **CERRADA COMO BENCHMARK COMPLETO / PROPUESTA PROVISIONAL**

## Alcance

Se rebenchmarcó la técnica completa:

- base;
- Tramo I;
- Tramo II;
- Tramo III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 enemigos;
- 3 enemigos;
- economía de Qi;
- Reflujo;
- reconstrucción;
- interacción con Arrastre y su anti-lock.

No se modifica runtime/HTML.

Runner:

experimentos/balance_nuevo/etapa12_espejo_luna_completo.py

## Guardia metodológica

Este benchmark aplica el anti-lock de Arrastre según el contrato actual:

> después de sufrir Arrastre, ese objetivo debe completar una acción normal antes
> de volver a ser elegible.

La elegibilidad se lleva por objetivo en escenarios multi-enemigo.

---

# 1. Base

Diseño anterior:

~~~text
12% HP Absorción
Reflujo 25%
3 turnos
coste base 7
coste efectivo Agua = 6
~~~

Candidato previo LAB:

~~~text
24% HP Absorción
Reflujo 25%
3 turnos
coste base 7
coste efectivo Agua = 6
~~~

## Repetición 4×25k — 24% vs 12%

### COMMON

- win: +8.24 / +7.64 / +7.58 / +7.61 pp;
- HP restante: +12.51 / +11.94 / +12.22 / +12.32 pp.

### PRECISE

- win: +9.88 / +10.30 / +10.07 / +10.14 pp;
- HP restante: +12.77 / +13.30 / +13.15 / +12.82 pp.

### HEAVY

- win: +9.30 / +8.82 / +8.71 / +9.20 pp;
- HP restante: +11.93 / +11.44 / +11.47 / +11.64 pp.

### DANGEROUS

- win: +11.19 / +11.60 / +11.30 / +11.86 pp.

### 2 enemigos

- win: +11.58 / +10.32 / +11.03 / +11.01 pp.

### 3 enemigos

- win: +2.60 / +2.58 / +2.52 / +2.30 pp.

El 12% queda descartado como magnitud principal.

## Base24 frente a ofensiva pura

Promedios de semillas independientes:

| Perfil | Ofensiva pura | Espejo24 |
|---|---:|---:|
| COMMON | 86.82% | 89.14% |
| PRECISE | 82.04% | 84.22% |
| HEAVY | 81.79% | 83.31% |
| DANGEROUS | 76.46% | 77.21% |
| 2 enemigos | 47.60% | 39.53% |
| 3 enemigos | 11.79% | 4.68% |

Lectura:

- en 1v1 deja de ser una elección-trampa;
- frente a múltiples enemigos conserva una debilidad real a burst;
- eso es coherente con una barrera regenerativa: si el pool llega a cero antes
  del siguiente TURN_START, Reflujo deja de funcionar.

No se fuerza a la técnica base a ser una defensa universal contra grupos.

## Decisión base

**24% HP / Reflujo25% / duración3 / coste base7 → PROVISIONAL.**

---

# 2. Ruta Reserva

Se conservan las magnitudes relativas de reserva sobre la nueva base24.

## Tramo I — Marea Profunda

~~~text
+5 pp Absorción
24% → 29%
~~~

## Tramo II — Marea Alta

~~~text
+5 pp Absorción
con Marea Profunda:
+3 pp adicionales de sinergia
~~~

Ruta RR:

~~~text
24 +5 +5 +3 = 37% HP
~~~

## Tramo III — Mar Interior

~~~text
+5 pp Absorción
~~~

Ruta RRR:

~~~text
42% HP de reserva
Reflujo25%
3 turnos
coste efectivo6
~~~

## RRR — repetición 4×15k

Promedios:

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 92.62% | 54.82% |
| PRECISE | 89.58% | 49.99% |
| HEAVY | 89.09% | 50.60% |
| DANGEROUS | 85.17% | 45.50% |
| 2 enemigos | 59.60% | 25.31% |
| 3 enemigos | 12.38% | 2.95% |

La ruta Reserva es la que mejor transforma Espejo en defensa contra presión
simultánea.

**Reserva I–III → PROVISIONAL.**

---

# 3. Ruta Reflujo / regeneración

La subida de reserva base no obliga a inflar Reflujo.

Se mantiene la progresión con retorno decreciente final.

## Tramo I — Agua Renovada

~~~text
Reflujo 25% → 35%
~~~

## Tramo II — Corriente de Retorno

~~~text
+10 pp Reflujo

con Agua Renovada:
si el pool se rompe,
una vez por activación se reconstruye
al siguiente TURN_START con 40% de reserva máxima
~~~

Con G1+G2:

~~~text
Reflujo45%
reconstrucción40%
~~~

## Tramo III — Marea Eterna

~~~text
+10 pp Reflujo
tope de ruta = 50%

si existe reconstrucción:
40% → 50%
~~~

Ruta GGG:

~~~text
reserva24%
Reflujo50%
reconstrucción50% una vez/activación
duración3
coste efectivo6
~~~

El tope50 resuelve la inconsistencia aritmética del texto anterior
(25+10+10+10 habría dado55 aunque la intención histórica declaraba50).

## GGG — repetición 4×15k

| Perfil | Win | HP restante | Reconstrucción |
|---|---:|---:|---:|
| COMMON | 91.76% | 52.69% | 24.17% |
| PRECISE | 88.41% | 47.60% | 28.85% |
| HEAVY | 87.34% | 47.45% | 36.11% |
| DANGEROUS | 82.72% | 41.97% | 41.28% |
| 2 enemigos | 49.92% | 18.19% | 87.74% |
| 3 enemigos | 8.19% | 1.70% | 99.10% |

Lectura:

- Reflujo funciona mejor cuando el pool puede sobrevivir entre TURN_START;
- contra burst múltiple la reconstrucción sí ocurre, pero no convierte el
  Espejo en una barrera de masa;
- ésa es una diferencia de identidad frente a Reserva, no un fallo.

**Reflujo I–III → PROVISIONAL.**

---

# 4. Eficiencia — problema estructural detectado

Diseño anterior:

~~~text
T1: 7 → 6 Qi
T2: −10% coste
T3: −10% coste
~~~

Con raíz Agua:

~~~text
coste base7
× 0.90 raíz
= 6.3
→ ROUND_HALF_UP = 6
~~~

Un nodo aislado de −10% adicional:

~~~text
7 × 0.90 × 0.90
= 5.67
→ ROUND_HALF_UP = 6
~~~

Por tanto:

> Flujo Ligero o Corriente Ininterrumpida podían ser mecánicamente nulos si se
> elegían sin Circulación Serena.

Esto viola la regla de rutas mixables: una elección de Tramo II/III debe tener
valor aunque no se haya seguido la misma familia antes.

---

# 5. Eficiencia recalibrada

## Tramo I — Circulación Serena

Se conserva:

~~~text
coste nominal Espejo 7 → 6
con raíz Agua:
coste efectivo = 5
~~~

## Tramo II — Flujo Ligero

Se recalibra:

~~~text
−15% coste
~~~

Motivo:

- 15% cruza el umbral de redondeo;
- elegido sin T1 lleva coste efectivo6 →5;
- con Circulación Serena conserva sinergia:
  duración3 →4.

## Tramo III — Corriente Ininterrumpida

Se recalibra:

~~~text
−15% coste
~~~

Además:

- si Espejo termina naturalmente conservando Absorción: recupera 1 Qi;
- esta recuperación es explícita, no regeneración pasiva;
- la recuperación funciona aunque no se hayan elegido E1/E2;
- con la ruta EEE completa: duración5.

### Costes resultantes

~~~text
sin E: coste efectivo6

1 nodo E:
coste efectivo5

2 nodos E:
coste efectivo5
+ las sinergias de duración/reembolso que correspondan

EEE completa:
coste efectivo4
duración5
reembolso1 Qi al expirar con reserva
~~~

Esto conserva el techo anterior de la ruta completa, pero elimina nodos muertos.

## Umbrales discretos

Con ofensiva Agua de coste efectivo6:

~~~text
Qi28:
def6 → 3 ofensivas
def5 → 3
def4 → 4

Qi29:
def6 → 3
def5 → 4
def4 → 4

Qi34:
def6 → 4
def5 → 4
def4 → 5

Qi35:
def6 → 4
def5 → 5
def4 → 5

Qi40:
def6 → 5
def5 → 5
def4 → 6

Qi41:
def6 → 5
def5 → 6
def4 → 6
~~~

Qi31 no cruza ninguno:

~~~text
def6 / def5 / def4
→ todos permiten 4 ofensivas de coste6
~~~

Por eso el benchmark actual subestima deliberadamente la economía futura.

## EEE — repetición 4×15k con Qi31

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 90.65% | 54.21% |
| PRECISE | 85.73% | 47.07% |
| HEAVY | 84.76% | 46.66% |
| DANGEROUS | 78.34% | 39.18% |
| 2 enemigos | 39.72% | 12.38% |
| 3 enemigos | 4.72% | 0.80% |

El reembolso de 1 Qi ocurre aproximadamente:

- 21% de duelos COMMON;
- 13–14% en PRECISE/HEAVY;
- <1% en 2 enemigos;
- ~0% en 3 enemigos.

Eso es coherente con la condición “expira conservando Absorción”.

**Eficiencia I–III → PROVISIONAL condicionada a rebenchmark de Qi II–IV.**

---

# 6. Screen de las 27 combinaciones

Se ejecutaron 8.000 combates por celda.

Códigos:

~~~text
R = Reserva
G = Reflujo / Regeneración
E = Eficiencia
~~~

## COMMON

~~~text
win: 89.74% – 92.84%
HP restante: 49.35% – 57.14%
~~~

## PRECISE

~~~text
win: 85.09% – 89.70%
HP restante: 44.13% – 51.21%
~~~

## HEAVY

~~~text
win: 84.43% – 89.31%
HP restante: 43.70% – 51.42%
~~~

## DANGEROUS

~~~text
win: 78.86% – 85.15%
HP restante: 37.85% – 45.72%
~~~

## 2 enemigos

~~~text
win: 40.33% – 59.28%
HP restante: 12.64% – 25.02%
~~~

## 3 enemigos

~~~text
win: 4.60% – 12.44%
HP restante: 0.80% – 2.94%
~~~

No se detectó una combinación fuera de escala.

La mejor ruta cambia con el contexto:

- Reserva domina burst multiimpacto;
- Reflujo gana valor cuando existen ventanas entre impactos;
- Eficiencia gana valor por coste/uptime y depende del presupuesto de Qi;
- mezclas R/G son especialmente robustas contra presión alta.

---

# 7. Lectura de identidad

## Reserva

~~~text
pool mayor
→ más difícil romper Espejo
→ Reflujo tiene más oportunidades de operar
~~~

Es la especialización anti-burst.

## Reflujo

~~~text
pool sobrevive
→ TURN_START
→ restaura reserva
→ reconstrucción única si la ruta lo habilita
~~~

Es la especialización de presión sostenida.

## Eficiencia

~~~text
menor coste
+ mayor uptime mediante sinergias
+ posible reembolso final
~~~

Es la especialización económica.

No pretende superar Reserva frente a tres atacantes.

---

# 8. Estado final de Espejo de Luna

~~~text
BASE                 PROVISIONAL
RESERVA I–III        PROVISIONAL
REFLUJO I–III        PROVISIONAL
EFICIENCIA I–III     PROVISIONAL recalibrada
27/27 paths          SCREEN PASS
runtime              SIN CAMBIOS
~~~

## Base

~~~text
24% HP Absorción
Reflujo25%
duración3
coste base7
coste efectivo Agua6
~~~

## Ruta Reserva completa

~~~text
42% HP reserva
Reflujo25%
duración3
coste6 efectivo
~~~

## Ruta Reflujo completa

~~~text
24% HP reserva
Reflujo50%
reconstrucción50% una vez
duración3
coste6 efectivo
~~~

## Ruta Eficiencia completa

~~~text
24% HP reserva
Reflujo25%
duración5
coste efectivo4
+1 Qi si expira naturalmente conservando reserva
~~~

---

# 9. Guardias futuras

1. revalidar Eficiencia cuando se fije Qi máximo LianQi II–IV;
2. revalidar todas las magnitudes con perfiles enemigos II–IV autoritativos;
3. no interpretar el stress 2/3 enemigos como balance final de encuentros;
4. conservar orden canónico TURN_START: Reflujo antes de DOT;
5. reconstrucción crea una nueva instancia lógica del pool según el contrato de
   Absorción múltiple;
6. no añadir regeneración universal de Qi: el +1 de Corriente Ininterrumpida es
   una fuente explícita de la rama.

La técnica completa queda apta como base reutilizable para:

- regenerating absorption pool;
- break/reconstruction;
- defensive restore at TURN_START;
- cost-efficiency branches;
- conditional Qi refund.
