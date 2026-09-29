# ETAPA 11 — Respiración del Cuerpo-Horno completa

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO BENCHMARK COMPLETO / PROPUESTA PROVISIONAL**

## Alcance

Se rebenchmarcó la técnica completa:

- base;
- Tramo I;
- Tramo II;
- Tramo III;
- las 27 combinaciones mixables de ramas;
- 1v1 común;
- enemigo preciso;
- enemigo pesado;
- enemigo peligroso;
- 2 enemigos;
- 3 enemigos;
- sensibilidad de economía de Qi.

No se modifica runtime/HTML.

Runner:

`experimentos/balance_nuevo/etapa11_cuerpo_horno_completo.py`

---

# 1. Base

Diseño anterior:

```text
15% HP Absorción
2 turnos
7 Qi
```

Candidato previo LAB:

```text
25% HP Absorción
2 turnos
7 Qi
```

## Repetición 4×25k

Delta 25% vs 15%.

### COMMON

- win: +1.816 / +1.708 / +1.960 / +2.024 pp;
- HP restante: +7.41 / +7.33 / +7.34 / +7.42 pp.

### 2 enemigos

- win: +8.16 / +9.12 / +8.63 / +8.82 pp;
- HP restante: +5.93 / +6.71 / +6.40 / +6.41 pp.

### 3 enemigos

- win: +6.59 / +5.59 / +7.02 / +6.42 pp;
- HP restante: +2.58 / +2.21 / +2.90 / +2.52 pp.

El 15% queda claramente por debajo.

## Decisión de base

**25% HP / 2 turnos / 7 Qi → PROVISIONAL.**

No añade Calor base.

---

# 2. Barrera

La subida de base 15%→25% no obliga a eliminar los incrementos de +5 pp.

Se mantuvo:

### Tramo I — Cámara Sellada

```text
+5 pp Absorción
25% → 30%
```

### Tramo II — Crisol de Nueve Sellos

```text
+5 pp Absorción
si existe Cámara:
+5 pp adicionales de sinergia
```

Ruta BB:

```text
25 +5 +5 +5 = 40% HP
```

### Tramo III — Muro de Calor

```text
+5 pp Absorción
```

Ruta BBB:

```text
45% HP Absorción
2 turnos
7 Qi
```

## Resultado ruta BBB

Promedio de cuatro semillas de 25k:

### COMMON

- win ≈ 97.12%;
- HP restante ≈ 64.69%.

### 3 enemigos

- win ≈ 41.06%;
- HP restante ≈ 14.41%.

En el stress de 3 enemigos la reserva se consume casi por completo.

No aparece una reserva infinita ni una escalada por impacto: el pool es finito.

**Barrera conserva sus magnitudes y pasa a PROVISIONAL bajo base25.**

---

# 3. Conversión — problema detectado

Los valores históricos no funcionan bien con el contrato real de daño.

Tramo I anterior:

```text
25% del daño absorbido → Calor
tope 5% HP
```

Con HP30:

```text
tope = 1.5
```

El paquete de Calor:

- no critica;
- no vuelve a recibir pools ofensivos;
- no usa Penetración;
- sí usa DEF.

Contra DEF2, un Calor con tope1.5 no puede producir daño efectivo.

Repetición 4×25k del Tramo I antiguo:

```text
COMMON:
daño medio de Calor = 0

3 enemigos:
daño medio de Calor = 0
```

Por tanto el nodo era mecánicamente casi nulo contra el enemigo ordinario.

---

# 4. Conversión recalibrada

Se buscó el mínimo que permita a Calor existir contra DEF2 sin convertir la
defensiva en una técnica ofensiva dominante.

## Tramo I — Horno Latente — candidato PROVISIONAL

```text
40% del daño absorbido → Calor
tope Calor = 10% HP máximo
```

Con HP30:

```text
tope = 3
```

Repetición 4×25k:

- COMMON: daño medio de Calor ≈ 0.17;
- 3 enemigos: ≈ 0.42.

Es pequeño, pero deja de ser cero.

## Tramo II — Corazón Reavivado — candidato PROVISIONAL

Sin Horno Latente:

```text
50% absorbido → Calor
tope 10% HP
```

Con Horno Latente:

```text
60% absorbido → Calor
tope 15% HP
```

## Tramo III — Calor Acumulado — candidato PROVISIONAL

Sin ninguna Conversión previa:

```text
50% absorbido → Calor
tope 10% HP
```

Con exactamente un nodo previo de Conversión:

```text
70% absorbido → Calor
tope 15% HP
```

Con Horno Latente + Corazón Reavivado:

```text
80% absorbido → Calor
tope 20% HP
```

Ruta CCC completa:

```text
Absorción base: 25% HP
Conversión: 80%
tope Calor: 20% HP
duración: 2
coste: 7
```

## Resultado ruta CCC

Promedio 4×25k:

### COMMON

- win ≈ 96.67%;
- HP restante ≈ 62.31%.

### 3 enemigos

- win ≈ 49.59%;
- HP restante ≈ 14.60%.

La ruta gana valor contra múltiples enemigos porque el Calor ayuda a retirar
enemigos y reducir acciones futuras.

No supera a Barrera en todos los contextos:

- BBB domina claramente en 2 enemigos;
- Barrera conserva más protección bruta;
- Conversión compra tempo ofensivo a cambio de no aumentar el pool base.

---

# 5. Semántica de Calor usada en el benchmark

El Motor §38.20 ya fija:

```text
DIRECT
FIRE
STORED_RESOURCE
no crit
sí DEF
no Penetración
sí Absorción
sin Life Steal
sin nuevo escalado ofensivo
```

Para poder simular la técnica completa, el LAB asumió:

```text
Calor se consume con la siguiente técnica ofensiva de Fuego;
comparte el resultado hit/miss de la técnica portadora;
no tira Precisión propia.
```

Este detalle de consumo/acierto **no se eleva automáticamente a CANON** por el
benchmark. Debe sincronizarse con el contrato de ejecución al implementar.

Las magnitudes de Conversión sí quedan justificadas como PROVISIONAL bajo esa
semántica de prueba.

---

# 6. Eficiencia

Se conservó conceptualmente:

### Tramo I — Respiración Mesurada

```text
7 → 6 Qi
```

### Tramo II — Circuito del Horno

```text
−10% coste
con Respiración Mesurada:
duración 2 → 3
```

### Tramo III — Horno Continuo

```text
−10% coste
ruta completa:
duración 4
+5 pp Absorción
```

Con el redondeo actual del LAB:

```text
ruta E:   coste6
ruta EE:  coste5 + duración3
ruta EEE: coste5 + duración4 + Absorción30%
```

## Por qué Qi31 oculta parte del valor

Con Palma de coste6:

```text
Qi31:
def7 + 4 Palmas = 31
def6 + 4 Palmas = 30
def5 + 4 Palmas = 29
```

Los tres costes permiten cuatro ofensivas.

Por eso reducir 7→6 no aumenta acciones en Qi31.

Pero la mejora sí aparece en otros umbrales:

```text
Qi30:
coste7 → 3 ofensivas
coste6 → 4

Qi35:
coste6 → 4
coste5 → 5

Qi36:
coste7 → 4
coste6 → 5

Qi41:
coste6 → 5
coste5 → 6

Qi42:
coste7 → 5
coste6 → 6
```

Por tanto la rama no está rota: su valor depende del presupuesto de Qi de la
etapa.

## Resultado ruta EEE con Qi31

Promedio 4×25k:

### COMMON

- win ≈ 96.90%;
- HP restante ≈ 65.18%.

### 3 enemigos

- win ≈ 30.37%;
- HP restante ≈ 9.15%.

No hay sobreescalado.

**Eficiencia puede permanecer PROVISIONAL**, pero requiere obligatoriamente
revalidación cuando se fijen Qi máximos de LianQi II–IV.

---

# 7. Las 27 combinaciones

Se ejecutó un screen completo de las 27 rutas mixables.

Código:

```text
B = Barrera
C = Conversión
E = Eficiencia
```

Ejemplos:

- BBB = Barrera/Barrera/Barrera;
- CCC = Conversión/Conversión/Conversión;
- EEE = Eficiencia/Eficiencia/Eficiencia;
- BCC = Barrera/Conversión/Conversión;
- BBC = Barrera/Barrera/Conversión.

Screen de 8.000 combates por celda:

## COMMON

Rango entre las 27 rutas:

```text
win ≈ 95.86% – 97.23%
HP restante ≈ 58.29% – 65.86%
```

No existe una ruta fuera de escala en 1v1 ordinario.

## 2 enemigos

```text
win ≈ 68.76% – 80.05%
HP restante ≈ 24.31% – 36.81%
```

La ruta BBB es la más robusta.

## 3 enemigos

```text
win ≈ 30.03% – 50.18%
HP restante ≈ 8.80% – 16.88%
```

Las rutas con Conversión profunda ganan valor por tempo ofensivo.

No se observa crecimiento ilimitado: todas siguen usando una reserva de
Absorción finita.

---

# 8. Rutas representativas bajo stress 1v1

25.000 combates por perfil.

| Ruta | PRECISE | HEAVY | DANGEROUS |
|---|---:|---:|---:|
| Base25 | 94.00% | 93.51% | 90.88% |
| BBB | 95.68% | 95.38% | 93.86% |
| BBC | 95.90% | 95.50% | 93.78% |
| BCC | 95.44% | 95.14% | 93.14% |
| CCC | 95.04% | 94.85% | 92.55% |
| EEE | 95.14% | 94.57% | 92.14% |

Ninguna ruta depende exclusivamente de PREC90 / 2d4+1.

---

# 9. Lectura de identidad

La técnica completa queda diferenciada de forma clara.

## Barrera

```text
más reserva
→ más supervivencia bruta
→ especialmente fuerte cuando el peligro es concentrado
```

## Conversión

```text
absorber
→ almacenar Calor
→ devolver una fracción como daño secundario
→ retirar amenazas antes
```

Gana valor relativo al aumentar el número de enemigos.

## Eficiencia

```text
menos coste
+ más duración mediante sinergia
→ valor dependiente del presupuesto de Qi
```

No intenta competir con Barrera en absorción bruta ni con Conversión en daño.

---

# 10. Resultado

## Base

```text
Respiración del Cuerpo-Horno
25% HP Absorción
2 turnos
7 Qi
→ PROVISIONAL
```

## Barrera

Magnitudes actuales de +5 pp:

**PROVISIONAL bajo la nueva base25.**

Ruta BBB:

```text
45% HP Absorción
2 turnos
7 Qi
```

## Conversión

Los valores anteriores quedan reemplazados PROVISIONALMENTE por:

```text
T1 Horno Latente:
40% conversión / cap10%

T2 Corazón Reavivado:
solo: 50% / cap10%
con Horno: 60% / cap15%

T3 Calor Acumulado:
sin C previa: 50% / cap10%
con 1 C previa: 70% / cap15%
con 2 C previas: 80% / cap20%
```

## Eficiencia

Se conservan sus reglas actuales como **PROVISIONAL**, con guardia obligatoria:

> rebenchmark de economía cuando se definan Qi máximos LianQi II, III y IV.

---

# 11. Estado final de Cuerpo-Horno

```text
BASE              PROVISIONAL
BARRERA I–III     PROVISIONAL
CONVERSIÓN I–III  PROVISIONAL recalibrada
EFICIENCIA I–III  PROVISIONAL condicionada a Qi futuro
27/27 paths       SCREEN PASS
runtime            SIN CAMBIOS
```

## Pendientes futuros, no bloqueantes para este cierre

1. fijar Qi máximo por LianQi II–IV y revalidar Eficiencia;
2. fijar perfiles enemigos II–IV y revalidar magnitudes por etapa;
3. cerrar en Motor el momento exacto de consumo de Calor respecto de hit/miss.

La arquitectura completa queda apta para servir como familia reutilizable de:

- Absorption pool;
- stored defensive resource;
- secondary damage from stored resource;
- defensive cost efficiency;
- defensive duration scaling.
