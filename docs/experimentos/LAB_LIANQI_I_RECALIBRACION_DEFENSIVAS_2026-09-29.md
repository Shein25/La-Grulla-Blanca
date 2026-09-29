# LAB — Recalibración de defensivas débiles · LianQi I PHASE C

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO PROVISIONAL / NO CANON**

## Objetivo

Recalibrar únicamente las tres defensivas que fallaron el screen conjunto:

- Fuego · Respiración del Cuerpo-Horno;
- Agua · Espejo de Luna;
- Viento · Paso de Nube Ligera.

Metal y Tierra quedan como controles y no reciben buffs en este bloque.

Baseline:

- Qi máximo LAB = 31;
- jugador base HP30 / DEF1 / EVA5;
- enemigo ordinario LAB HP28 / PREC90 / EVA20 / DEF2;
- daño enemigo `2d4+1`;
- Arrastre PROVISIONAL = 50% de referencia;
- Peso PROVISIONAL = STACK_REFRESH;
- jugador actúa primero;
- defensiva como apertura.

Runner reproducible:

`experimentos/balance_nuevo/phase_c_defensive_recalibration_lab.py`

---

## 1. Fuego — Respiración del Cuerpo-Horno

### Situación anterior

`15% HP / 2 turnos` no justificaba el turno:

- ofensiva pura: ~95.7% win;
- Cuerpo-Horno 15%: ~94.1%.

### Barrido fino

Se probaron 22 / 23 / 24 / 25% de HP máximo como reserva inicial,
manteniendo duración2 y coste7.

Confirmación de 120.000 duelos por punto:

| Absorción | Win rate aprox. | HP restante aprox. |
|---:|---:|---:|
| 22% | 95.5% | 56.2% |
| 23% | 95.4% | 56.7% |
| 24% | 96.0% | 57.4% |
| 25% | 95.9% | 58.1% |

La pequeña oscilación de win entre 22–25% está dentro de la sensibilidad
Monte Carlo; la tendencia estable aparece en HP conservado.

### Candidato LAB

```text
Cuerpo-Horno
Absorción base ≈ 25% HP
duración 2
coste 7
```

Motivo:

- deja de ser una elección-trampa;
- mantiene la identidad de barrera corta;
- conserva aproximadamente el mismo win que la ofensiva fuerte de Fuego;
- aumenta ~5–6 pp el HP restante;
- no necesita añadir Calor a la técnica base.

El objetivo no es que Cuerpo-Horno supere siempre a Palma, sino que cambiar una
acción ofensiva por defensa produzca una ganancia defensiva tangible.

---

## 2. Agua — Espejo de Luna

### Situación anterior

`12% HP / Reflujo25%` falla claramente porque la reserva suele romperse antes
de que Reflujo pueda expresarse.

Baseline ofensivo con Arrastre50:

- win ~86.8%;
- HP restante ~42.8%.

### Barrido fino

| Absorción | Win rate aprox. | HP restante aprox. |
|---:|---:|---:|
| 21% | 87.5% | 45.7% |
| 22% | 88.3% | 46.6% |
| 23% | 88.4% | 47.2% |
| 24% | 89.0% | 48.4% |
| 25% | 89.8% | 49.1% |

### Candidato LAB

```text
Espejo de Luna
Absorción base ≈ 24% HP
Reflujo = 25%
duración 3
coste base 7
coste efectivo Agua principal = 6
```

24% es un centro útil porque:

- la reserva sobrevive con suficiente frecuencia para que Reflujo exista;
- mejora el win aproximadamente +2 pp respecto de ofensiva pura;
- mejora ~5–6 pp el HP restante;
- sigue claramente por debajo de Piel de Cobre en fortificación bruta;
- conserva su identidad de reserva que vuelve a fluir.

No se modifica Reflujo en este bloque.

---

## 3. Viento — Paso de Nube Ligera

### Problema estructural detectado

El valor actual:

```text
+15 EVA
2 turnos
```

no puede compensar una acción sacrificada.

Una mejora pequeña tampoco alcanza:

- +20 EVA / 3t sigue muy por debajo;
- +25 EVA / 3t sigue por debajo;
- +30 EVA / 3t todavía no iguala la ofensiva pura.

Esto concuerda con la matemática del duelo: una bonificación pequeña de
Evasión durante pocas respuestas sólo evita una fracción de un impacto, mientras
la activación sustituye una acción ofensiva completa.

### Barrido de Evasión/duración

Valores relevantes:

| Paso LAB | Win rate aprox. |
|---|---:|
| +25 EVA / 3t | ~83% |
| +30 EVA / 3t | ~85% |
| +30 EVA / 4t | ~88% |
| +32 EVA / 4t | ~88.6% |
| +33 EVA / 4t | ~88.7% |
| +34 EVA / 4t | ~89.0% |
| +35 EVA / 4t | ~89.4% |

Ofensiva pura de Viento: ~88.1%.

### Candidato LAB

```text
Paso de Nube Ligera
+35 EVA
duración 4
coste 7
sin nueva mecánica base
```

Éste es deliberadamente un candidato **LAB**, no una promoción.

Ventajas:

- convierte Paso en una defensiva real;
- mantiene el diseño simple de Evasión + duración;
- no mueve a la base `CORRIENTE_CLARA`, que actualmente pertenece a una rama;
- no añade movimiento, velocidad ni una segunda tirada de esquiva;
- mejora el HP restante de ~39% a ~46%.

### Consecuencia importante

`+35 EVA / 4t` supera numéricamente la actual ruta completa provisional
(+30 / 4t).

Eso **no invalida el candidato**, porque las magnitudes de los Tramos son
provisionales, pero sí significa:

> si Paso base se mueve a esta escala, su progresión I–III debe recalibrarse
> después. No se puede conservar la vieja escalera +15→+30 como si nada hubiera
> cambiado.

Se prefirió probar primero una solución puramente numérica porque preserva los
hooks base actuales:

- EVASION_GRANTED;
- DEFENSIVE_DURATION.

Mover `REACTIVE_RESPONSE` a la técnica base funcionaba en variantes de LAB,
pero canibalizaba la identidad de Estela Vacía y obligaba a rediseñar ramas
antes de demostrar que fuera necesario.

---

## 4. Stress check de candidatos

Se probaron los candidatos:

- Fuego: 25%;
- Agua: 24%;
- Viento: +35 EVA / 4t;

contra:

- COMMON: PREC90 / `2d4+1`;
- PRECISE: PREC100 / `2d4+1`;
- HEAVY: PREC90 / `1d6+3`;
- DANGEROUS: PREC100 / `1d6+3`.

### Lectura

**Cuerpo-Horno 25%**

- queda aproximadamente en paridad de win con ofensiva pura;
- conserva ~5 pp adicionales de HP incluso bajo presión;
- deja de empeorar fuertemente al personaje.

**Espejo 24%**

- mejora win aproximadamente 1–2 pp según perfil;
- mantiene mejora consistente de HP;
- Reflujo empieza a participar de forma real.

**Paso +35/4**

- mejora claramente contra COMMON y HEAVY;
- queda aproximadamente en paridad contra PRECISE;
- mantiene mejora contra DANGEROUS;
- no depende de que el enemigo tenga exactamente PREC90.

Esto elimina la hipótesis de que los nuevos candidatos sólo funcionen contra un
único perfil artificial.

---

## 5. Screen conjunto con candidatos recalibrados

Usando los valores LAB anteriores junto a Metal/Tierra sin cambios:

| Raíz | Defensiva | Win aproximado |
|---|---|---:|
| Fuego | Cuerpo-Horno 25% | ~96% |
| Metal | Armadura de Plata actual | ~93% |
| Agua | Espejo 24% | ~89% |
| Tierra | Piel de Cobre actual | ~96% |
| Viento | Paso +35 EVA / 4t | ~89% |

No se busca igualdad exacta de win rate:

- Fuego ya posee una raíz fuertemente ofensiva;
- Agua tiene Arrastre;
- Tierra posee +10% HP y Piel escala con impactos;
- Viento posee +10 EVA de raíz;
- Metal posee penetración/precisión.

El criterio en este bloque es que ninguna defensiva base sea una elección
obviamente peor que ignorarla.

---

## Resultado

Candidatos LAB principales para la próxima validación:

```text
Cuerpo-Horno
25% HP Absorción
2 turnos

Espejo de Luna
24% HP Absorción
Reflujo25%
3 turnos

Paso de Nube Ligera
+35 EVA
4 turnos
```

**NO modificar todavía el documento autoritativo de técnicas.**

Antes de promoverlos a PROVISIONAL:

1. validar el perfil de jugador/enemigo que sostiene PHASE C;
2. confirmar Qi31 frente a las cinco raíces;
3. revisar que Piel de Cobre no escale excesivamente con impactos múltiples;
4. volver a proyectar las ramas I–III de las tres técnicas recalibradas.

