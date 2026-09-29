> ⚠️ **HISTÓRICO / NO USAR CIFRAS PARA BALANCE DEL SISTEMA NUEVO.**  
> Este informe fue producido antes de declarar obsoleto el sistema numérico legacy. Puede conservar hallazgos de arquitectura, interacción o metodología, pero cualquier resultado que dependa de HP/Qi/perfiles enemigos/DEF/Evasión/daño derivados o inspirados en `ver74` debe repetirse con el marco `experimentos/balance_nuevo/`. No convertir estadísticas legacy al contrato nuevo.

# Espejo de Luna — combate completo con base 30% HP

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **TEST DE BALANCE / NO CANÓNICO**

## 0. Pregunta

¿El turno gastado en activar Espejo de Luna se siente justificado dentro de un combate real?

Se compara:

- sin Espejo;
- Espejo actual 12%;
- nueva base 30%;
- Reserva completa 55%;
- Regeneración completa con base 30%;
- Eficiencia completa con base 30%.

Después de activar Espejo, el jugador usa Latigazo de Marea por la ruta de daño.

Se excluyen equipo, injerto, Concordancias, consumibles y buffs externos.

## 1. Daño enemigo variable

El Pass anterior con paquetes fijos produjo escalones artificiales. Para esta prueba se usan distribuciones de daño inspiradas en la escala real de criaturas de `ver74`:

```text
COMMON: 1d6+1  · media 4.5
ELITE:  2d6+1  · media 8
BOSS:   2d8+3  · media 12
```

Perfiles de objetivo:

```text
COMMON: HP18 · DEF3
ELITE:  HP34 · DEF6
BOSS:   HP52 · DEF9
```

HP del jugador sin equipo: 28.

## 2. Resultado COMMON

| Configuración | Kill | TTK | HP final | Absorción media | Qi |
|---|---:|---:|---:|---:|---:|
| Sin Espejo | 100% | 2.00 | ~23.50 | 0 | 12 |
| Actual 12% | 100% | 3.00 | ~22.17 | ~3.17 | 18 |
| Base 30% | 100% | 3.00 | **~27.44** | **~8.44** | 18 |
| Reserva 55% | 100% | 3.00 | 28.00 | ~9.00 | 18 |
| Regeneración 30% | 100% | 3.00 | ~27.89 | ~8.89 | 18 |
| Eficiencia 30% | 100% | 3.00 | ~27.44 | ~8.44 | **16** |

### Lectura

El Espejo actual es peor que atacar inmediatamente: cuesta un turno y termina con menos Vida.

Con 30%:

- el turno defensivo ya deja una ganancia visible;
- el jugador termina casi a Vida completa;
- Reflujo puede operar;
- la técnica compra suficiente margen para justificar su activación.

## 3. Resultado ELITE — sin Arrastre

| Configuración | Kill/supervivencia ≤6 | TTK si mata | HP final medio | Absorción media |
|---|---:|---:|---:|---:|
| Sin Espejo | ~39.5% | ~4.23 | ~2.06 | 0 |
| Actual 12% | ~17.1% | ~4.99 | ~0.72 | 3.0 |
| **Base 30%** | **~45.3%** | ~5.33 | ~2.80 | ~8.89 |
| Reserva 55% | **~94.7%** | ~5.61 | ~11.92 | ~20.82 |
| Regeneración 30% | **~69.7%** | ~5.49 | ~5.84 | ~13.66 |
| Eficiencia 30% | ~45.3% | ~5.33 | ~2.81 | ~8.89 |

### Hallazgo E-30

30% ya supera el umbral funcional:

```text
sin Espejo ~39.5%
con base 30% ~45.3%
```

Por tanto ya no sólo cancela el ataque extra provocado por gastar la acción defensiva: genera una mejora real en supervivencia.

## 4. Sensibilidad de la base

Se probaron bases 25/28/30/32/35% con Reflujo 25%.

Contra ELITE variable:

| Base | supervivencia |
|---:|---:|
| 25% | ~34–40% según redondeo/rolls |
| 28% | ~40–45% |
| **30%** | **~45%** |
| 32% | ~53% |
| 35% | ~64.5% |

El salto 30→35 es grande. 35% como base empieza a acercarse demasiado al poder de una especialización defensiva.

Conclusión provisional:

> **30% es un punto base más prudente que 35%.**

## 5. Rutas puras con base 30%

### Reserva

Propuesta probada:

```text
30% base
35% T1
45% T2
55% T3
```

Contra ELITE:

```text
supervivencia ≈94.7%
absorción media ≈20.8
HP final ≈11.9
```

Es una especialización fuerte, pero no invulnerable.

### Regeneración

Con:

```text
30% reserva base
50% Reflujo
reconstrucción única 50%
```

Contra ELITE:

```text
supervivencia ≈69.7%
absorción media ≈13.7
HP final ≈5.8
```

Ahora sí tiene identidad propia: menos pico que Reserva, pero mejor continuidad.

### Eficiencia

Con base 30%, duración 5 y coste reducido:

```text
supervivencia ≈45.3%
absorción ≈8.9
```

Es prácticamente igual a Espejo base en supervivencia, pero gasta menos Qi.

Esto indica que su ganancia actual es **económica**, no defensiva.

## 6. Latigazo/Arrastre — sensibilidad

No existe todavía `base_control` canónico, así que Arrastre sólo se usa como sensibilidad.

Contra ELITE:

### Si Arrastre efectivo ≈30%

| Espejo | supervivencia |
|---|---:|
| Base 30% | ~78.7% |
| Reserva 55% | ~98.7% |
| Regeneración 30% | ~90.9% |
| Eficiencia 30% | ~78.7% |

### Si Arrastre efectivo ≈50%

| Espejo | supervivencia |
|---|---:|
| Base 30% | ~90.0% |
| Reserva 55% | ~99.7% |
| Regeneración 30% | ~96.8% |
| Eficiencia 30% | ~90.0% |

Esto confirma que Agua no necesita daño adicional para volverse competitivo: Control + defensa transforman el resultado.

## 7. BOSS-STRESS

Sin equipo y usando sólo Espejo + Latigazo de daño, ninguna configuración mata de forma consistente al perfil BOSS.

Eso es deseable: este stress no debería resolverse con una sola defensiva desnuda.

Promedio de acciones enemigas soportadas sin Arrastre:

| Configuración | acciones enemigas | Absorción media |
|---|---:|---:|
| Sin Espejo | ~2.84 | 0 |
| Base 30% | ~3.50 | ~8.2 |
| Regeneración 30% | ~3.86 | ~12.4 |
| Reserva 55% | **~4.37** | **~18.5** |

Reserva aumenta claramente la ventana de supervivencia sin volver suficiente por sí sola para ganar.

## 8. Comparación conceptual

Con 30% base:

```text
Espejo base
→ compra aproximadamente una acción relevante

Reserva
→ maximiza cuánto daño puede atravesar antes de romperse

Regeneración
→ maximiza cuánto valor obtiene si consigue volver a fluir

Eficiencia
→ conserva el comportamiento base gastando menos Qi y permaneciendo disponible más tiempo
```

## 9. Veredicto de test

**30% HP base PASA la prueba de combate completo.**

No se recomienda subir la base a 35% por ahora.

Valores provisionales que merecen continuar al siguiente Pass:

```text
BASE          30% HP
RESERVA T1    35%
RESERVA T2    45%
RESERVA T3    55%
REFLUJO BASE  25%
REGEN FULL    50% + reconstrucción 50%
```

Pendiente:

- comprobar las 27 mezclas de Espejo con esta nueva base;
- decidir si Eficiencia necesita una pequeña ventaja defensiva propia o si el ahorro de Qi es suficiente;
- cerrar `base_control` y Tenacidad antes del balance final de Agua;
- no convertir todavía estos valores en canon hasta esa reauditoría.