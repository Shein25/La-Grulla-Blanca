# ETAPA 14 — Armadura de Plata completa

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **CERRADA COMO BENCHMARK COMPLETO / PROPUESTA PROVISIONAL**

## Alcance

Se rebenchmarcó:

- base;
- Tramos I–III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 enemigos;
- 3 enemigos;
- consumo/no-consumo de Placas;
- Adaptación con stress de Control separado.

No se modifica runtime/HTML.

Runner:

experimentos/balance_nuevo/etapa14_armadura_plata_completa.py

## Guardia metodológica

Los perfiles COMMON/PRECISE/HEAVY/DANGEROUS no usan Control.

Por eso Adaptación no se juzga sólo por win rate de daño puro. Se añade un
stress LAB separado con Control efectivo65 para comprobar su identidad.

Los benchmarks de Tramos I–III siguen usando estadísticas LianQi I como marco
mecánico; no sustituyen la futura validación contra enemigos LianQi II–IV.

---

# 1. Base

La base actual se conserva:

~~~text
coste: 7 Qi
duración máxima: 4 turnos
3 Placas

cada Placa activa:
+3 DEF contra un impacto directo

impacto conectado válido:
consume 1 Placa

evasión:
no consume

DOT:
no consume
~~~

Las Placas son secuenciales. Tres Placas NO significan +9 DEF.

## Base frente a ofensiva pura

Promedio de cuatro semillas de 25.000 combates:

| Perfil | Ofensiva pura | Armadura base | Delta |
|---|---:|---:|---:|
| COMMON | 90.71% | 92.90% | +2.19 pp |
| PRECISE | 86.60% | 88.85% | +2.26 pp |
| HEAVY | 86.04% | 88.24% | +2.19 pp |
| DANGEROUS | 80.84% | 82.65% | +1.82 pp |
| 2 enemigos | 58.32% | 52.17% | -6.15 pp |
| 3 enemigos | 14.33% | 7.50% | -6.83 pp |

Lectura:

- en 1v1 la activación justifica el turno;
- con varios enemigos las tres Placas se consumen demasiado rápido;
- esto no invalida la base: la especialización de Cantidad existe precisamente
  para aumentar cobertura multiimpacto.

La base permanece **PROVISIONAL**.

---

# 2. Recalibración de ramas por cantidad de nodos

El texto histórico dependía demasiado de haber tomado nodos concretos
anteriores de la misma familia.

Para respetar las 27 rutas mixables, las tres familias pasan a resolverse por
**cantidad de nodos de esa familia**.

Esto no cambia su identidad; vuelve determinista cualquier combinación.

---

# 3. Resistencia

La intención histórica era aproximadamente:

~~~text
base      +3 DEF/Placa
1 nodo    +4
2 nodos   ~+6
3 nodos   ~+8
~~~

El benchmark confirma que esta curva puede conservarse.

## Un nodo de Resistencia

Cualquiera de:

- Placas Gruesas;
- Núcleo Reforzado;
- Acero Cerrado.

Resultado:

~~~text
+4 DEF por Placa
~~~

## Dos nodos

Cualquier combinación de dos:

~~~text
+6 DEF por Placa
~~~

## Tres nodos — RRR

~~~text
+8 DEF por Placa
3 Placas
duración4
coste7
~~~

La Placa sigue consumiéndose tras un impacto conectado aunque el daño resultante
sea 0, salvo que Adaptación de 2+ nodos habilite explícitamente lo contrario.

Esto impide convertir Resistencia pura en DEF permanente.

## RRR — promedio 4×15k

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 97.76% | 69.50% |
| PRECISE | 96.08% | 62.38% |
| HEAVY | 96.63% | 66.39% |
| DANGEROUS | 93.96% | 58.71% |
| 2 enemigos | 70.26% | 30.07% |
| 3 enemigos | 16.78% | 4.16% |

Lectura:

- excelente contra pocos impactos importantes;
- sigue cayendo con muchos enemigos porque sólo hay 3 Placas;
- +8 DEF no equivale a DEF permanente: como máximo protege las cargas
  disponibles y la instancia expira en 4 turnos.

**Resistencia I–III → PROVISIONAL.**

---

# 4. Cantidad

La intención histórica ya definía una curva muy clara.

Se formaliza también por conteo:

~~~text
0 nodos Q → 3 Placas
1 nodo Q  → 4
2 nodos Q → 6
3 nodos Q → 8
~~~

Esto hace válidas combinaciones como Q en Tramo I + Q en Tramo III aunque el
jugador no haya elegido Q en Tramo II.

## Ruta QQQ

~~~text
8 Placas
+3 DEF/Placa
duración4
coste7
~~~

La duración4 actúa como segundo límite.

En 1v1 no siempre es posible consumir las 8 Placas antes de expirar.

Contra varios enemigos, en cambio, sí aparecen suficientes impactos para que
la cantidad extra importe.

## QQQ — promedio 4×15k

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 94.81% | 54.29% |
| PRECISE | 92.24% | 49.21% |
| HEAVY | 90.94% | 47.72% |
| DANGEROUS | 87.39% | 42.42% |
| 2 enemigos | 76.36% | 31.45% |
| 3 enemigos | 33.09% | 9.02% |

La identidad queda invertida respecto de Resistencia:

~~~text
Resistencia:
pocas Placas muy fuertes

Cantidad:
muchas Placas moderadas
~~~

**Cantidad I–III → PROVISIONAL.**

---

# 5. Adaptación

La familia queda formalizada también por cantidad de nodos.

## Un nodo A

Tras romperse una Placa:

~~~text
+5 Tenacidad
hasta el comienzo del próximo turno del usuario
~~~

## Dos nodos A

~~~text
+10 Tenacidad reactiva
~~~

Además:

> si un impacto directo conectado queda en 0 **por DEF**, la Placa no se consume.

La comprobación se realiza sobre el paquete post-DEF, antes de cualquier
Absorción externa. Que otro pool absorba el daño no cuenta como "detenido por
DEF".

## Tres nodos — AAA

~~~text
+15 Tenacidad reactiva

si DEF deja el impacto en0:
no consume Placa

primer Control fallido:
recupera 1 Placa rota
una vez/activación
~~~

La recuperación exige que exista una Placa previamente rota.

---

# 6. Adaptación contra daño puro

Sin Control enemigo, Adaptación no pretende ganar a Resistencia.

Promedio 4×15k de AAA:

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 93.59% | 51.93% |
| PRECISE | 90.02% | 45.44% |
| HEAVY | 88.89% | 45.09% |
| DANGEROUS | 83.99% | 38.59% |
| 2 enemigos | 57.01% | 20.65% |
| 3 enemigos | 10.97% | 2.63% |

La pequeña mejora sobre base proviene del no-consumo de Placa cuando DEF
detiene totalmente algunos impactos.

No se buffea Adaptación por quedar por debajo de R/Q en enemigos sin Control.

---

# 7. Stress LAB de Control

Este bloque NO define un enemigo canónico.

Se usa únicamente:

~~~text
Control efectivo enemigo = 65
~~~

y se intenta Control después de impactos directos conectados.

Como referencia matemática, inmediatamente después de romper una Placa:

~~~text
sin Adaptación → P(Control) 65%
1 nodo A       → 60%
2 nodos A      → 55%
3 nodos A      → 50%
~~~

La probabilidad agregada de todo el combate es mayor porque el buff sólo existe
tras romper una Placa y expira al comenzar el siguiente turno.

Promedio 4×20k, 1 enemigo:

| Nodos A | Control agregado | Win stress | Recuperación |
|---:|---:|---:|---:|
| 0 | 65.01% | 31.74% | — |
| 1 | 62.95% | 33.99% | — |
| 2 | 61.39% | 37.01% | — |
| 3 | 59.11% | 41.12% | 96.98% |

La tasa de recuperación alta de AAA es esperable en este stress deliberadamente
cargado de intentos de Control.

No se interpreta como frecuencia esperada en encuentros reales.

**Adaptación I–III → PROVISIONAL**, pendiente de revalidación con enemigos que
realmente utilicen Control en etapas superiores.

---

# 8. Screen 27/27

Se ejecutaron 8.000 combates por celda.

Códigos:

~~~text
R = Resistencia
A = Adaptación
Q = Cantidad
~~~

Rangos:

| Perfil | Win mínimo | Win máximo | HP mínimo | HP máximo |
|---|---:|---:|---:|---:|
| COMMON | 93.19% | 98.55% | 51.33% | 74.68% |
| PRECISE | 90.26% | 97.76% | 45.55% | 71.66% |
| HEAVY | 88.48% | 97.14% | 44.98% | 69.60% |
| DANGEROUS | 83.84% | 95.99% | 38.45% | 66.56% |
| 2 enemigos | 56.94% | 83.20% | 20.37% | 42.23% |
| 3 enemigos | 11.38% | 34.03% | 2.66% | 10.39% |

No aparece una ruta con crecimiento ilimitado.

## Combinaciones emergentes

En 1v1, mezclar dos nodos de Resistencia con uno de Cantidad produce:

~~~text
4 Placas
+6 DEF/Placa
~~~

y es muy robusto.

En grupo, dos nodos de Cantidad + uno de Resistencia producen:

~~~text
6 Placas
+4 DEF/Placa
~~~

y compiten con QQQ o lo superan.

Esto es deseable:

> las rutas mixtas pueden encontrar puntos de equilibrio que las rutas puras no
> cubren.

No se fuerza que RRR/AAA/QQQ sean siempre las tres mejores configuraciones.

---

# 9. Identidad final

## Resistencia

~~~text
más DEF por carga
→ gran mitigación de pocos impactos
→ cargas siguen siendo finitas
~~~

## Adaptación

~~~text
romper Placa
→ Tenacidad temporal

especialización profunda
→ impacto0 no consume
→ fallo de Control puede recuperar una carga
~~~

## Cantidad

~~~text
más Placas
→ más impactos cubiertos
→ mejor contra presión múltiple
~~~

La técnica queda claramente diferenciada de:

- Piel de Cobre: DEF reactiva/Arraigo;
- Cuerpo-Horno: pool de Absorción;
- Espejo: pool regenerativo;
- Paso: Evasión.

---

# 10. Estado final

~~~text
ARMADURA DE PLATA

BASE                 PROVISIONAL
RESISTENCIA I–III    PROVISIONAL
ADAPTACIÓN I–III     PROVISIONAL
CANTIDAD I–III       PROVISIONAL
27/27 rutas          SCREEN PASS
runtime              SIN CAMBIOS
~~~

## Base

~~~text
3 Placas
+3 DEF/Placa
duración4
coste7
~~~

## Resistencia completa

~~~text
3 Placas
+8 DEF/Placa
duración4
coste7
~~~

## Adaptación completa

~~~text
3 Placas
+3 DEF/Placa

tras romper:
+15 Tenacidad hasta próximo turno

daño0 por DEF:
no consume Placa

primer Control fallido:
recupera 1 Placa rota
una vez/activación
~~~

## Cantidad completa

~~~text
8 Placas
+3 DEF/Placa
duración4
coste7
~~~

---

# 11. Guardias futuras

1. revalidar magnitudes con perfiles enemigos LianQi II–IV autoritativos;
2. revalidar Adaptación con enemigos reales de Control;
3. un multihit puede consumir varias Placas si produce impactos directos
   separados; no crear excepción ad hoc;
4. el no-consumo de Adaptación depende de daño0 **por DEF**, no por Absorción;
5. duración4 sigue limitando incluso una reserva de 8 Placas;
6. no convertir Placas en DEF permanente;
7. no hacer que varias Placas sumen su DEF simultáneamente.

La familia queda apta como patrón reutilizable para futuras defensivas de
cargas secuenciales por impacto.
