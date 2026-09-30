# ETAPA 15A — Screen conjunto final de defensivas BASE

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO DIAGNÓSTICO CONJUNTO / SIN CAMBIOS NUMÉRICOS**

## Objetivo

Comparar las cinco defensivas base ya recalibradas bajo un único marco de
simulación.

Este bloque NO busca igualar porcentajes de victoria entre raíces.

Cada raíz conserva:

- su rasgo CANON;
- su ofensiva inicial PROVISIONAL;
- sus costes efectivos;
- su identidad mecánica propia.

Por eso la lectura principal es:

```text
defensiva de una raíz
vs
jugar sólo ofensiva con esa misma raíz
```

Runner:

`experimentos/balance_nuevo/etapa15a_screen_conjunto_defensivas_base.py`

Repetición principal:

- 4 semillas;
- 10.000 combates por celda y semilla;
- 40.000 combates agregados por configuración.

---

# 1. Bases incluidas

## Fuego — Cuerpo-Horno

```text
25% HP Absorción
2 turnos
7 Qi
```

## Metal — Armadura de Plata

```text
3 Placas
+3 DEF/Placa
4 turnos
7 Qi
```

## Agua — Espejo de Luna

```text
24% HP Absorción
Reflujo25%
3 turnos
7 Qi nominal / 6 efectivo
```

## Tierra — Piel de Cobre

Usa DEF_CAP2:

```text
DEF total benchmark:
4 → 5 → 5
```

más Tenacidad y extensión a Arraigo máximo.

## Viento — Paso de Nube Ligera

```text
+35 EVA
4 turnos
7 Qi
```

---

# 2. COMMON

| Raíz | Ofensiva sola | Con defensiva | Delta win | Delta HP |
|---|---:|---:|---:|---:|
| Fuego | 95.66% | 95.85% | +0.19 pp | +5.80 pp |
| Metal | 90.66% | 93.05% | +2.40 pp | +9.75 pp |
| Agua | 86.79% | 88.76% | +1.96 pp | +5.32 pp |
| Tierra | 91.66% | 95.72% | +4.06 pp | +15.46 pp |
| Viento | 87.76% | 89.19% | +1.44 pp | +7.20 pp |

Lectura:

- ninguna defensiva base es una trampa en COMMON;
- Fuego cambia poco el win pero conserva mucha más Vida;
- Tierra produce el mayor lift defensivo relativo;
- el win absoluto de Tierra no supera materialmente a Fuego porque la ofensiva
  base de Fuego parte de una posición mucho más fuerte.

---

# 3. PRECISE

| Raíz | Ofensiva sola | Con defensiva | Delta win |
|---|---:|---:|---:|
| Fuego | 93.82% | 94.00% | +0.18 pp |
| Metal | 86.78% | 88.84% | +2.06 pp |
| Agua | 82.24% | 84.63% | +2.38 pp |
| Tierra | 88.44% | 93.91% | +5.46 pp |
| Viento | 82.24% | 82.41% | +0.17 pp |

Paso no colapsa frente a PREC100, pero tampoco obtiene ventaja artificial:
queda aproximadamente en paridad de win con su ofensiva y mejora el HP
restante ~4.94 pp.

---

# 4. HEAVY

| Raíz | Ofensiva sola | Con defensiva | Delta win |
|---|---:|---:|---:|
| Fuego | 93.65% | 93.60% | -0.05 pp |
| Metal | 86.04% | 87.90% | +1.86 pp |
| Agua | 82.16% | 83.72% | +1.56 pp |
| Tierra | 87.95% | 92.96% | +5.01 pp |
| Viento | 82.99% | 84.63% | +1.64 pp |

Cuerpo-Horno queda en paridad de victoria pero conserva ~4.81 pp adicionales
de HP. No se considera elección-trampa por una oscilación de win cercana a cero.

---

# 5. DANGEROUS

| Raíz | Ofensiva sola | Con defensiva | Delta win | Delta HP |
|---|---:|---:|---:|---:|
| Fuego | 91.34% | 90.76% | -0.58 pp | +4.06 pp |
| Metal | 81.55% | 82.42% | +0.87 pp | +6.91 pp |
| Agua | 76.62% | 77.28% | +0.66 pp | +3.65 pp |
| Tierra | 83.52% | 90.21% | +6.69 pp | +16.96 pp |
| Viento | 75.24% | 76.64% | +1.41 pp | +5.87 pp |

Fuego muestra el coste táctico de sacrificar una acción ofensiva frente a un
enemigo simultáneamente preciso y pesado.

No se modifica por este dato aislado porque:

- el win sigue ~91%;
- conserva más Vida;
- la rama Barrera/Conversión existe para especialización posterior.

---

# 6. Dos enemigos

Stress unitarget con HP total28 dividido 14+14.

| Raíz | Ofensiva sola | Con defensiva | Delta win |
|---|---:|---:|---:|
| Fuego | 75.41% | 68.98% | -6.43 pp |
| Metal | 58.08% | 51.92% | -6.16 pp |
| Agua | 47.79% | 39.80% | -7.99 pp |
| Tierra | 61.44% | 84.98% | +23.55 pp |
| Viento | 53.32% | 63.29% | +9.97 pp |

Aquí aparecen las identidades sistémicas:

- pools/cargas finitas de Fuego/Metal/Agua se agotan mientras se perdió una
  acción ofensiva;
- Viento gana oportunidades de evasión;
- Tierra genera Arraigo más rápido y aplica DEF plana a impactos posteriores.

---

# 7. Tres enemigos

Stress unitarget con HP total28 dividido 10+9+9.

| Raíz | Ofensiva sola | Con defensiva | Delta win |
|---|---:|---:|---:|
| Fuego | 42.32% | 28.01% | -14.31 pp |
| Metal | 14.42% | 7.78% | -6.64 pp |
| Agua | 11.85% | 4.77% | -7.09 pp |
| Tierra | 17.31% | 57.97% | +40.66 pp |
| Viento | 17.21% | 30.46% | +13.26 pp |

Éste es un **stress mecánico**, no un objetivo de dificultad grupal.

---

# 8. Hallazgo global

No hay una única defensiva dominante en todos los ejes.

## Fuego

- muy alta potencia total de raíz en 1v1;
- Cuerpo-Horno aumenta supervivencia, pero el turno sacrificado pesa contra
  presión múltiple.

## Metal

- Placas base justifican 1v1;
- tres cargas son insuficientes para enjambres;
- Cantidad existe como especialización posterior.

## Agua

- Espejo funciona bien si tiene ventanas de TURN_START;
- burst multiimpacto rompe su condición de Reflujo;
- Reserva es la especialización anti-burst.

## Viento

- escalado natural contra múltiples intentos de impacto;
- PREC alta limita su ventaja sin invalidarla.

## Tierra

- sigue siendo la base con mayor lift defensivo;
- especialmente fuerte frente a muchas acciones enemigas.

---

# 9. Vigilancia específica de Piel

DEF_CAP2 corrigió una parte importante del exceso anterior, pero el screen
global confirma que Piel continúa siendo un **outlier multiimpacto**.

Eso NO revoca su estado PROVISIONAL.

Razones para no tocarla en esta etapa:

1. el stress fuerza únicamente ofensivas unitarget;
2. no incluye AOE del jugador;
3. no representa composición real de encuentros;
4. la identidad de Tierra está diseñada precisamente para asentarse bajo
   presión;
5. ya existe evidencia de que DEF_CAP2 redujo materialmente el exceso de la
   curva anterior.

Por tanto:

```text
Piel
→ PROVISIONAL
→ WATCH multiimpacto global
→ sin nerf automático
```

El watch deberá reabrirse sólo cuando existan encuentros reales o perfiles de
etapa que demuestren que invalida alternativas.

---

# 10. Bloqueador para llamar “cerradas completas” a las cinco

El screen detectó una cuestión documental/experimental importante:

Piel tiene cerrados:

- base;
- Corteza Endurecida;
- Estratos Compactos;
- Cuerpo de Roca.

Es decir, la familia **Fortificación** completa.

Pero todavía NO han pasado el mismo benchmark integral:

## Estabilidad

- Centro Firme;
- Raíz Profunda;
- Inamovible.

## Aguante

- Tierra Persistente;
- Suelo que Sostiene;
- Montaña Persistente.

Sus valores actuales siguen siendo diseño previo/orientativo.

Por tanto no es correcto declarar todavía:

```text
5 defensivas × 27 rutas
todas cerradas
```

El estado correcto es:

```text
Fuego   completo
Metal   completo
Agua    completo
Viento  completo

Tierra:
base + Fortificación completa
Estabilidad/Aguante pendientes de benchmark integral
```

---

# 11. Decisión de Etapa 15A

**PASS como screen conjunto de bases.**

No se modifica ningún número.

No se modifica runtime/HTML.

## Próximo bloque correcto

**ETAPA 15B — Piel de Cobre completa: Estabilidad + Aguante + 27 rutas.**

Sólo después de cerrar ese hueco se puede ejecutar honestamente el
**screen conjunto final de las cinco técnicas completas**.
