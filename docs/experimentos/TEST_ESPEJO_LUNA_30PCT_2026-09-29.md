> ⚠️ **HISTÓRICO / NO USAR CIFRAS PARA BALANCE DEL SISTEMA NUEVO.**  
> Este informe fue producido antes de declarar obsoleto el sistema numérico legacy. Puede conservar hallazgos de arquitectura, interacción o metodología, pero cualquier resultado que dependa de HP/Qi/perfiles enemigos/DEF/Evasión/daño derivados o inspirados en `ver74` debe repetirse con el marco `experimentos/balance_nuevo/`. No convertir estadísticas legacy al contrato nuevo.

# Test de Espejo de Luna — base 30% HP

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **TEST DE BALANCE / NO CANÓNICO**

## Objetivo

Comprobar si una técnica defensiva activa justifica el turno gastado en activarla.

Criterio de diseño:

> La defensa base debe comprar aproximadamente una acción enemiga relevante; sus especializaciones deben mejorar reserva, recuperación o economía, no reparar una base inútil.

## Propuesta probada

~~~text
Espejo base: 30% HP máximo
Reserva T1: 35%
Reserva T2: 45%
Reserva T3: 55%
Reflujo base: 25%
Duración base: 3 turnos
~~~

HP de referencia sin equipo: 28.

Reservas discretas aproximadas:

| Estado | Absorción |
|---|---:|
| Actual 12% | 3 |
| Nueva base 30% | 8 |
| Reserva T1 35% | 10 |
| Reserva T2 45% | 13 |
| Reserva T3 55% | 15 |

## Daño absorbido durante tres turnos

| Paquete enemigo | Actual base 12% | Nueva base 30% | Reserva 35% | Reserva 45% | Reserva 55% |
|---:|---:|---:|---:|---:|---:|
| 5 | 3 | **10** | 15 | 15 | 15 |
| 8 | 3 | **8** | 13 | 16 | **23** |
| 12 | 3 | **8** | 10 | 16 | **19** |

Lectura:

- paquete 5: la nueva base absorbe dos acciones comunes gracias a Reflujo;
- paquete 8: la nueva base compra exactamente una acción enemiga completa;
- paquete 12: compra aproximadamente dos tercios de una acción de stress;
- Reserva completa contra paquete 8 absorbe 23 de 24 posibles en tres ataques.

## Comparación con Armadura de Plata

Armadura de Plata, ruta Resistencia completa:

~~~text
3 Placas × ~8 DEF
≈24 mitigación máxima en tres impactos suficientemente grandes
~~~

Espejo Reserva 55% contra tres paquetes 8:

~~~text
≈23 mitigación total
~~~

Esto coloca ambas defensas máximas en una escala semejante pero con identidades distintas:

- Metal: mitigación segmentada y garantizada por impacto;
- Agua: reserva única que puede regenerarse mientras permanezca viva.

## Regeneración con nueva base

Se mantuvo la idea de Reflujo completo 50% y reconstrucción única al 50%.

| Paquete | Nueva base | Regeneración completa |
|---:|---:|---:|
| 5 | 10 | **15** |
| 8 | 8 | **12** |
| 12 | 8 | **12** |

Con reserva máxima 8:

~~~text
Reflujo 50% = ~4 por turno
reconstrucción 50% = ~4 una vez
~~~

Regeneración ahora funciona; ya no intenta regenerar una reserva de sólo 3.

## Eficiencia con nueva base

Ruta eficiencia completa conserva reserva 30% y duración hasta 5 turnos.

Contra paquete 5:

~~~text
absorbe ≈10 total
~~~

Contra paquete 8 o 12:

~~~text
absorbe ≈8 y se rompe en el primer impacto
~~~

### Hallazgo

Subir la base a 30% arregla el valor de la activación, pero **no arregla por sí solo la identidad de la ruta Eficiencia** contra golpes fuertes: duración extra no sirve si la reserva desaparece de inmediato.

Esto no exige más Absorción para Eficiencia. Puede necesitar una ventaja propia posterior, por ejemplo economía de Qi o una regla ligera de continuidad, pero debe decidirse aparte.

## Resultado

**30% HP base pasa la prueba funcional inicial.**

Razones:

1. el turno defensivo absorbe aproximadamente una acción enemiga completa contra ELITE;
2. Reflujo empieza a operar realmente contra COMMON;
3. no necesita un valor fijo permanente;
4. escala de forma natural con HP futuro;
5. Reserva completa queda cerca del valor total de Armadura de Plata completa sin copiar su mecánica.

Valores 35/45/55 siguen siendo provisionales; el 55% no se congela hasta probarlo en kits completos y bosses.