# ETAPA 13 — Paso de Nube Ligera completo

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **CERRADA COMO BENCHMARK COMPLETO / PROPUESTA PROVISIONAL**

## Alcance

Se rebenchmarcó la técnica completa:

- base antigua vs base nueva;
- Tramo I;
- Tramo II;
- Tramo III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 enemigos;
- 3 enemigos;
- CORRIENTE_CLARA;
- economía de Qi;
- duración.

No se modifica runtime/HTML.

Runner:

experimentos/balance_nuevo/etapa13_paso_nube_completo.py

## Guardia conceptual

Paso sigue siendo una defensa de Evasión.

No introduce:

- movimiento;
- Velocidad;
- reposicionamiento;
- segunda tirada de esquiva;
- inmunidad.

La raíz Viento conserva +10 EVA y +5 pp de daño crítico.

---

# 1. Base

Diseño anterior:

~~~text
+15 EVA
2 turnos
7 Qi
~~~

Candidato previo LAB:

~~~text
+35 EVA
4 turnos
7 Qi
~~~

Con jugador base EVA5 + raíz Viento EVA10:

~~~text
sin Paso: EVA15

Paso nuevo:
EVA total50
~~~

Frente a PREC90:

~~~text
P(hit) = 90 - 50 = 40%
~~~

Frente a PREC100:

~~~text
P(hit) = 100 - 50 = 50%
~~~

Todavía existe una probabilidad sustancial de impacto.

## Repetición 4×25k — base nueva vs antigua

### COMMON

- mejora de win: +11.13 / +11.96 / +11.52 / +11.61 pp;
- promedio: +11.55 pp;
- mejora de HP restante: ~+16.0 pp.

### PRECISE

- mejora de win: +14.45 / +14.56 / +14.87 / +14.84 pp;
- promedio: +14.68 pp.

### HEAVY

- mejora de win: +15.24 / +14.30 / +15.07 / +14.51 pp;
- promedio: +14.78 pp.

### DANGEROUS

- mejora de win: +17.84 / +16.83 / +17.29 / +17.52 pp;
- promedio: +17.37 pp.

### 2 enemigos

- mejora: +28.79 / +28.38 / +29.00 / +29.25 pp;
- promedio: +28.86 pp.

### 3 enemigos

- mejora: +23.55 / +23.73 / +23.82 / +23.51 pp;
- promedio: +23.65 pp.

El antiguo +15/2 queda descartado.

## Base nueva frente a ofensiva pura

Promedio 4×25k:

| Perfil | Ofensiva pura | Paso +35/4 | Delta |
|---|---:|---:|---:|
| COMMON | 87.84% | 89.37% | +1.53 pp |
| PRECISE | 82.18% | 82.31% | +0.12 pp |
| HEAVY | 82.49% | 84.74% | +2.25 pp |
| DANGEROUS | 75.33% | 76.11% | +0.77 pp |
| 2 enemigos | 53.26% | 62.92% | +9.66 pp |
| 3 enemigos | 17.02% | 30.24% | +13.22 pp |

Lectura:

- ya no es una elección-trampa en 1v1;
- contra PREC100 no obtiene una ventaja artificial enorme;
- escala naturalmente con cantidad de ataques porque cada ataque es otra
  oportunidad de evitar un impacto completo.

## Decisión base

**+35 EVA / 4 turnos / coste7 → PROVISIONAL.**

---

# 2. Ruta Evasión

Los antiguos +5 EVA por nodo siguen siendo utilizables sobre la nueva base.

## Tramo I — Nube Velada

~~~text
+5 EVA
Paso: +35 → +40
~~~

## Tramo II — Cuerpo de Nube

~~~text
+5 EVA
~~~

Con T1:

~~~text
+45 EVA otorgada
~~~

## Tramo III — Nube Inalcanzable

~~~text
+5 EVA
~~~

Ruta VVV completa:

~~~text
+50 EVA otorgada por Paso
duración4
coste7
~~~

Con EVA base5 + raíz10:

~~~text
EVA total durante Paso = 65
~~~

Frente a PREC90:

~~~text
P(hit) = 25%
~~~

Frente a PREC100:

~~~text
P(hit) = 35%
~~~

No alcanza el clamp mínimo de impacto y no produce inmunidad.

## VVV — repetición 4×15k

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 93.77% | 55.18% |
| PRECISE | 88.48% | 45.74% |
| HEAVY | 90.67% | 51.46% |
| DANGEROUS | 83.45% | 41.56% |
| 2 enemigos | 78.18% | 36.08% |
| 3 enemigos | 51.38% | 18.23% |

Es la especialización más fuerte frente a muchos impactos.

No domina todos los perfiles: contra enemigos de PREC100 la ruta de Eficiencia
queda muy cerca o ligeramente por encima.

**Evasión I–III → PROVISIONAL.**

---

# 3. Ruta Respuesta — CORRIENTE_CLARA

La estructura antigua dependía demasiado de haber elegido exactamente los
nodos anteriores de la misma familia.

Para respetar 27 rutas mixables se formaliza por cantidad de nodos de Respuesta.

## Trigger universal de la familia

~~~text
primera Evasión válida
mientras Paso esté activo
→ crea CORRIENTE_CLARA
→ una vez por activación
~~~

La siguiente técnica pura de Viento consume CORRIENTE_CLARA.

El ataque básico no la consume.

No concede acción adicional ni contraataque.

## Un nodo de Respuesta

Puede ser cualquiera de:

- Estela Vacía;
- Huella del Cielo;
- Paso sin Sombra.

Efecto:

~~~text
siguiente técnica pura de Viento:
+5 Precisión
~~~

## Dos nodos de Respuesta

Cualquier combinación de dos:

~~~text
+10 Precisión
~~~

## Tres nodos — RRR

~~~text
+15 Precisión
+5 pp crítico
~~~

Esto conserva la magnitud histórica de la ruta completa y hace que las mezclas
T1/T3, T2/T3, etc. sean deterministas.

Con Lanza que Parte Nubes:

~~~text
Precisión normal:
100 actor +5 técnica =105

vs EVA20:
85% hit

CORRIENTE con 1 R:
90%

con 2 R:
95%

con 3 R:
100%
~~~

La rama no desperdicia Precisión más allá del clamp.

## Frecuencia del trigger

Con la nueva base +35/4, en los benchmarks:

- COMMON: CORRIENTE se crea en ~97% de combates;
- PRECISE: ~94%;
- 2 enemigos: ~99%;
- 3 enemigos: ~100%.

La respuesta es fiable, pero sólo una vez por activación.

## RRR — repetición 4×15k

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 91.72% | 49.05% |
| PRECISE | 85.69% | 40.22% |
| HEAVY | 87.67% | 44.99% |
| DANGEROUS | 80.04% | 35.78% |
| 2 enemigos | 68.03% | 26.84% |
| 3 enemigos | 34.72% | 10.07% |

Respuesta queda por debajo de Evasión pura en supervivencia, como corresponde:
parte de su valor se desplaza a mejorar la siguiente acción ofensiva.

**Respuesta I–III → PROVISIONAL con sinergia por cantidad de nodos.**

---

# 4. Ruta Eficiencia

La base ahora ya dura4 turnos, por lo que la antigua ruta completa “hasta4”
había quedado absorbida por la nueva base.

Se recalibra la progresión de duración sin cambiar la lógica principal de
coste.

## Tramo I — Respiración Ligera

~~~text
coste7 → 6 Qi
~~~

## Tramo II — Circulación del Vendaval

Se conserva:

~~~text
−10% coste
~~~

Si existe un nodo previo de Eficiencia:

~~~text
+1 turno de duración
~~~

Por tanto con Respiración Ligera:

~~~text
duración4 →5
~~~

## Tramo III — Aliento de las Nubes

Se conserva:

~~~text
−10% coste
~~~

Si existe al menos un nodo previo de Eficiencia:

~~~text
+1 turno de duración
~~~

Esto hace útil también la combinación E de Tramo II + E de Tramo III aunque
no se haya elegido E en Tramo I.

### Ejemplos

~~~text
un nodo E aislado:
coste efectivo6
duración4

T1 E + T2 E:
coste5
duración5

T1 E + T3 E:
coste5
duración5

T2 E + T3 E:
coste6
duración5

EEE:
coste5
duración6
~~~

La ruta completa conserva aproximadamente el techo de coste histórico:

~~~text
6 × 0.90 × 0.90 = 4.86
→ ROUND_HALF_UP = 5
~~~

No se fuerza un coste4.

## Qi31

~~~text
def7 + 4 ofensivas6 =31
def6 + 4 ofensivas6 =30
def5 + 4 ofensivas6 =29
~~~

En Qi31 ninguno agrega una quinta ofensiva.

Umbrales futuros:

~~~text
Qi29:
coste5 → 4 ofensivas
coste6/7 → 3

Qi30:
coste6 → 4
coste7 → 3

Qi31:
coste7 → 4

Qi35:
coste5 → 5

Qi36:
coste6 → 5

Qi37:
coste7 → 5
~~~

Por eso el valor futuro debe revalidarse contra Qi de LianQi II–IV.

## EEE — repetición 4×15k

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 93.42% | 53.40% |
| PRECISE | 88.22% | 43.99% |
| HEAVY | 90.38% | 49.75% |
| DANGEROUS | 83.61% | 40.05% |
| 2 enemigos | 72.80% | 30.65% |
| 3 enemigos | 41.88% | 12.98% |

Contra DANGEROUS, EEE queda ligeramente por encima de VVV en win rate.

Esto confirma que +50 EVA no es una respuesta universal: contra mayor Precisión,
mantener +35 EVA durante más tiempo puede competir con aumentar su magnitud.

**Eficiencia I–III → PROVISIONAL condicionada a Qi futuro.**

---

# 5. Screen 27/27

8.000 combates por celda.

Códigos:

~~~text
V = Evasión
R = Respuesta
E = Eficiencia
~~~

## COMMON

~~~text
win: 90.31% – 93.45%
HP restante: 47.16% – 54.90%
~~~

## PRECISE

~~~text
win: 83.73% – 88.60%
HP restante: 38.47% – 45.32%
~~~

## HEAVY

~~~text
win: 86.61% – 91.34%
HP restante: 43.29% – 51.74%
~~~

## DANGEROUS

~~~text
win: 77.86% – 83.81%
HP restante: 34.15% – 41.57%
~~~

## 2 enemigos

~~~text
win: 65.35% – 78.30%
HP restante: 25.13% – 36.56%
~~~

## 3 enemigos

~~~text
win: 31.24% – 50.33%
HP restante: 8.78% – 18.07%
~~~

No aparece ninguna ruta fuera de escala.

La ruta óptima cambia por perfil y presión.

---

# 6. Identidad de las tres familias

## Evasión

~~~text
más EVA
→ menor probabilidad de cada impacto
→ máximo valor cuando existen muchos intentos enemigos
~~~

Especialización anti-multiimpacto.

## Respuesta

~~~text
evasión exitosa
→ CORRIENTE_CLARA
→ mejora ofensiva futura una vez/activación
~~~

Especialización de transición defensa → ofensiva.

## Eficiencia

~~~text
menor coste
+ mayor duración
→ mantiene la ventana defensiva durante más rondas
~~~

Especialización de continuidad/economía.

---

# 7. Estado final de Paso de Nube Ligera

~~~text
BASE                 PROVISIONAL
EVASIÓN I–III        PROVISIONAL
RESPUESTA I–III      PROVISIONAL recalibrada por conteo de nodos
EFICIENCIA I–III     PROVISIONAL recalibrada en duración
27/27 paths          SCREEN PASS
runtime              SIN CAMBIOS
~~~

## Base

~~~text
+35 EVA
4 turnos
7 Qi
~~~

## Ruta Evasión completa

~~~text
+50 EVA
4 turnos
7 Qi
~~~

## Ruta Respuesta completa

~~~text
+35 EVA
4 turnos
7 Qi

primera Evasión válida:
CORRIENTE_CLARA

siguiente técnica pura Viento:
+15 Precisión
+5 pp crítico
~~~

## Ruta Eficiencia completa

~~~text
+35 EVA
6 turnos
coste5
~~~

---

# 8. Guardias futuras

1. revalidar economía cuando se fije Qi máximo LianQi II–IV;
2. revalidar magnitudes con perfiles enemigos II–IV autoritativos;
3. no interpretar stress 2/3 enemigos como balance final de grupos;
4. CORRIENTE_CLARA sigue siendo una sola respuesta por activación;
5. CORRIENTE_CLARA modifica la siguiente técnica pura de Viento, no el ataque
   básico;
6. no introducir movimiento/Velocidad/segunda esquiva;
7. conservar clamp global 5–100% de impacto.

Paso queda apto como base reutilizable para futuras defensivas de:

- stat evasion buff;
- reactive-on-evade response;
- next-action modifier;
- duration scaling;
- cost-efficiency defensive stance.
