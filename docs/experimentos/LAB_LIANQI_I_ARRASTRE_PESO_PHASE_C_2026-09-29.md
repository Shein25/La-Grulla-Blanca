# LAB — LianQi I PHASE C · Arrastre y Peso

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / UTILIDAD BASE / NO CANON**

## Objetivo

Valorar las utilidades base de Agua y Tierra antes de corregir daño por
diferencias de win rate.

Duelo central LAB:

```text
Jugador
HP base 30
Qi 30
DEF 1
EVA base 5

Enemigo
HP 28
PREC 90
EVA 20
DEF 2
ataque 2d4+1

Jugador actúa primero.
```

Se mantienen:

- ataque básico `1d4+4` PROVISIONAL;
- técnicas narrow PROVISIONAL;
- cap de impacto 100;
- sin equipo;
- sin Concordancias;
- sin injerto;
- sin Tramos;
- sin defensivas.

## Reglas recuperadas

### Arrastre — Latigazo de Marea

Base aprobada:

- al impactar intenta aplicar Arrastre mediante Control vs Tenacidad;
- Arrastre hace perder la próxima acción;
- puede cortar una acción anunciada aún no ejecutada;
- anti-bloqueo: después de sufrir Arrastre, el objetivo debe completar una
  acción normal antes de poder sufrirlo otra vez.

La potencia base de Arrastre y la Tenacidad del enemigo siguen PENDIENTES.

Por eso el laboratorio **NO inventa `base_control` ni Tenacidad**.

Se barre directamente la probabilidad efectiva post-fórmula:

```text
25 / 35 / 45 / 50 / 55 / 65 / 75 %
```

### Peso — Golpe de Montaña

Base provisional:

- −3 Evasión por carga;
- duración 2 turnos;
- máximo 2 cargas;
- no es Control.

El contrato del State Engine admite:

- `STACK_REFRESH`;
- `INDEPENDENT`.

La técnica todavía no declara cuál de ambas usa, por lo que se testean ambas
semánticas en vez de asumir una.

Runner reproducible:

`experimentos/balance_nuevo/phase_c_water_earth_utility_lab.py`

---

## Agua sin Arrastre

Confirmación de 200.000 duelos:

| Métrica | Agua sin Arrastre |
|---|---:|
| Win rate | 74.11% |
| Turnos medios | 5.92 |
| HP restante medio | 26.03% |
| Combates con básico | 59.08% |
| Acciones enemigas completas | 5.18 |

Esto confirma que valorar Latigazo sólo por daño directo deja a Agua
claramente por debajo.

---

## Barrido de Arrastre

Confirmación de 100.000–200.000 duelos por candidato:

| Prob. efectiva | Win rate | HP restante | Acciones enemigas omitidas | Acciones enemigas completas |
|---:|---:|---:|---:|---:|
| 25% | ~81.8% | ~35.4% | ~0.77 | ~4.51 |
| 35% | ~84.3% | ~38.6% | ~1.03 | ~4.26 |
| 45% | ~86.0% | ~41.5% | ~1.26 | ~4.07 |
| 50% | ~86.7–86.8% | ~42.8% | ~1.36 | ~3.97 |
| 55% | ~87.6–87.7% | ~44.1% | ~1.46 | ~3.88 |
| 65% | ~88.9% | ~46.5% | ~1.65 | ~3.71 |
| 75% | ~90.0% | ~48.7% | ~1.82 | ~3.55 |

### Lectura

La zona **45–55%** es la más interesante:

- compensa gran parte de la desventaja de daño;
- evita aproximadamente 1.25–1.45 acciones enemigas por duelo;
- no convierte Arrastre en un bloqueo continuo;
- mantiene diferencia frente a Fuego/Metal/Tierra;
- hace visible la identidad de control de Agua.

Como centro de sensibilidad:

```text
P(Arrastre efectivo contra enemigo ordinario)
≈ 50%
```

Esto NO fija todavía `base_control`.

Con Agua principal:

```text
P(Control)
= base_control + 5 Control - Tenacidad
≈ 50
```

por tanto la relación que interesa cerrar después es:

```text
base_control - Tenacidad_referencia
≈ 45
```

No hace falta escoger todavía valores absolutos.

---

## Importancia del anti-bloqueo

Con Arrastre ~50% y la regla aprobada de anti-bloqueo:

- win rate Agua ≈ 86.8%;
- ~1.36 acciones enemigas omitidas.

En una comprobación sin anti-bloqueo:

- win rate sube a ~88.2%;
- acciones omitidas suben a ~1.78;
- HP restante aumenta de forma apreciable.

La diferencia confirma que la guardia:

> sufrir Arrastre → completar una acción normal → volver a ser elegible

cumple una función real de balance y debe conservarse.

---

## Peso — resultados

### Sin Peso

Confirmación 200.000 duelos:

| Métrica | Tierra sin Peso |
|---|---:|
| Win rate | 89.57% |
| Turnos | 5.42 |
| HP restante | 40.56% |
| Usa básico | 39.70% |

### STACK_REFRESH / duración compartida refrescada

```text
cada impacto:
+1 carga, máximo 2
refresca duración del estado a 2 turnos
```

Resultado:

| Métrica | Tierra + Peso |
|---|---:|
| Win rate | 91.91% |
| Turnos | 5.23 |
| HP restante | 43.16% |
| Usa básico | 33.25% |

### INDEPENDENT / duración por carga

Resultado:

| Métrica | Tierra + Peso |
|---|---:|
| Win rate | 91.09% |
| Turnos | 5.31 |
| HP restante | 42.12% |
| Usa básico | 35.97% |

### Lectura

Peso aporta una mejora moderada y sana:

- aproximadamente +1.5 a +2.3 pp de win rate;
- reduce turnos;
- reduce necesidad de fallback;
- no domina el duelo;
- expresa su función: cada golpe hace más probable que el siguiente conecte.

La diferencia entre `STACK_REFRESH` e `INDEPENDENT` es pequeña pero real.

El State Engine ya soporta ambos. Falta una decisión de contenido para Golpe de
Montaña.

---

## Comparación entre raíces con utilidades

Usando como sensibilidad:

- Arrastre efectivo = 50%;
- Peso = STACK_REFRESH;
- PREC enemiga = 90;

confirmación de 200.000 duelos:

| Raíz | Win rate | Turnos | HP restante | Usa básico |
|---|---:|---:|---:|---:|
| Fuego | 95.70% | 4.24 | 52.28% | 13.36% |
| Tierra + Peso | 91.91% | 5.24 | 43.12% | 33.39% |
| Metal | 90.57% | 5.06 | 40.02% | 28.43% |
| Viento | 87.95% | 5.68 | 38.87% | 47.95% |
| Agua + Arrastre 50% | 86.85% | 6.20 | 42.77% | 63.76% |

La dispersión todavía existe, pero cambia completamente respecto del test de
daño puro.

Agua deja de parecer una técnica simplemente subpotente: sacrifica daño y
duración ofensiva a cambio de negar acciones.

Tierra mejora de forma menor porque Peso es una utilidad ofensiva gradual; su
raíz ya estaba obteniendo +10% HP.

---

## Sensibilidad a Precisión enemiga

Con las utilidades activas:

| PREC enemiga | Agua + Arrastre 50% | Tierra + Peso |
|---:|---:|---:|
| 85 | ~88.85% | ~93.16% |
| 90 | ~86.84% | ~91.86% |
| 95 | ~84.56% | ~90.28% |

La utilidad no depende de que PREC90 sea exacta para funcionar. El patrón se
mantiene en 85–95.

---

## Conclusiones

### Arrastre

No aumentar el daño de Latigazo por ahora.

La banda objetivo más prometedora es:

```text
Arrastre efectivo vs enemigo ordinario
≈ 45–55%
centro LAB ≈ 50%
```

Eso deberá convertirse después en una combinación explícita de:

- `base_control` de Arrastre;
- Tenacidad de referencia de LianQi I.

### Peso

El valor base `−3 EVA / carga, máximo 2` supera este primer test sin indicar
sobrepotencia.

La magnitud no necesita corregirse todavía.

Falta decidir:

```text
STACK_REFRESH
vs
INDEPENDENT
```

antes de implementar el estado real.

### Precisión enemiga

PREC90 sigue siendo un centro LAB útil para enemigo ordinario, pero no se eleva
a estadística universal.

---

## Estado de PHASE C

```text
PHASE A
PASS PROVISIONAL

PHASE B
PARCIAL

PHASE C
Precisión/Evasión A/B completado
Arrastre/Peso screening completado
NO PASS todavía
```

## Próximo paso recomendado

1. fijar una **Tenacidad de referencia LAB** del enemigo ordinario;
2. convertir el objetivo de ~50% de Arrastre en candidatos de
   `base_control`;
3. decidir semántica de stacking de Peso;
4. después probar las primeras técnicas defensivas, empezando por
   **Piel de Cobre** y **Espejo de Luna**, porque consumen un turno y deben
   demostrar que ese turno defensivo vale la pena.

