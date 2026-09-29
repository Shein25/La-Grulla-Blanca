# LAB — Stress multi-enemigo de defensivas · LianQi I

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **LAB / STRESS / NO BALANCE FINAL DE GRUPOS**

## Objetivo

Comprobar cómo escalan las defensivas cuando existen varias acciones enemigas reales por ronda.

A diferencia del stress exploratorio anterior, aquí cada atacante posee HP propio, acción propia, posibilidad de morir y orden de objetivo unitarget.

Para aislar la cantidad de acciones entrantes, el HP enemigo total se mantiene aproximadamente constante:

- 1 enemigo: 28 HP;
- 2 enemigos: 14 + 14 HP;
- 3 enemigos: 10 + 9 + 9 HP.

El jugador usa sólo su técnica inicial unitarget sobre el primer enemigo vivo. No se incluyen AOE.

Runner: experimentos/balance_nuevo/phase_c_multi_enemy_defensive_stress_lab.py

## Configuración

- Qi31 LAB;
- enemigo PREC90 / EVA20 / DEF2 / ataque 2d4+1;
- Fuego Horno25% LAB;
- Metal Armadura actual;
- Agua Espejo24% LAB;
- Tierra Piel actual;
- Viento Paso +35 EVA / 4t LAB.

## Resultado cualitativo fuerte

### Dos enemigos

| Raíz | Sólo ofensiva | Con defensiva | Delta |
|---|---:|---:|---:|
| Fuego | ~75% | ~69% | −6 pp |
| Metal | ~59% | ~52% | −6 pp |
| Agua | ~50% | ~41% | −9 pp |
| Tierra | ~61% | **~89%** | **+28 pp** |
| Viento | ~53% | ~63% | +10 pp |

### Tres enemigos

| Raíz | Sólo ofensiva | Con defensiva | Delta |
|---|---:|---:|---:|
| Fuego | ~41% | ~28% | −13 pp |
| Metal | ~15% | ~7% | −7 pp |
| Agua | ~13% | ~5% | −8 pp |
| Tierra | ~18% | **~68%** | **+50 pp** |
| Viento | ~16% | ~30% | +14 pp |

Los valores son de stress y no deben interpretarse como win rates objetivo de combate grupal.

## Hallazgo principal — Piel de Cobre

Piel escala de forma extremadamente fuerte con varias acciones enemigas.

La razón está en su propio contrato:

~~~text
cada acción enemiga de daño directo que quite Vida
→ +1 Arraigo
→ máximo una vez por acción
~~~

Con varios enemigos:

1. alcanza 3 Arraigos casi inmediatamente;
2. activa su extensión de duración pronto;
3. la DEF plana alta se aplica después contra cada impacto posterior;
4. en la escala de daño LianQi I, DEF5–6 puede reducir una gran fracción de ataques comunes a daño muy bajo o 0.

Esto produce una realimentación:

~~~text
más atacantes
→ más Arraigo
→ más DEF
→ cada atacante futuro hace mucho menos daño
~~~

La identidad de Tierra debe ser buena bajo presión, pero el salto observado es lo bastante grande para impedir promover Piel sin otro benchmark.

**Piel vuelve a estado de vigilancia de balance.**

No se revoca su diseño; se marca el escalado multi-impacto como problema a resolver.

## Armadura de Plata

Placas muestra el comportamiento opuesto:

- más enemigos consumen las 3 Placas muy rápido;
- el turno de activación pesa más;
- deja de justificar la apertura en este stress.

Esto puede ser identidad válida: Metal puede ser excelente contra pocos impactos importantes sin ser la defensa ideal contra enjambres.

No se buffea Armadura a partir de este stress.

## Viento

Paso gana valor de manera natural al crecer la cantidad de ataques:

- cada ataque adicional es una nueva oportunidad de que Evasión evite un impacto completo;
- con +35 EVA / 4t el beneficio aumenta en 2–3 enemigos.

Esto confirma que el diseño de Paso como defensa de continuidad/evasión tiene una identidad sistémica real.

También obliga a no sobrerreaccionar al duelo 1v1: un valor que parece sólo moderado en duelo puede escalar bastante en encuentros múltiples.

## Fuego y Agua

Absorción usa una reserva compartida.

Más atacantes vacían la reserva rápidamente, aumentan el coste de haber sacrificado una acción ofensiva y Reflujo de Espejo puede no sobrevivir hasta el siguiente turno.

No se concluye que Horno/Espejo estén mal para grupos; el test unitarget deliberadamente no usa sus futuras ramas, Concordancias ni AOE.

## Consecuencia

Antes de promover Piel, hace falta comparar al menos estas hipótesis LAB:

1. Arraigo máximo una vez por acción, regla actual;
2. ganancia normal de Arraigo limitada a una vez por ronda/turno del usuario, conservando el trigger de impacto fuerte;
3. mantener la frecuencia actual pero reducir la DEF marginal por Arraigo;
4. mantener Piel fuerte contra enjambres pero introducir una curva de rendimientos decrecientes explícita.

No elegir una todavía.

Primero hay que medir cuál conserva identidad de Tierra bajo presión, utilidad en duelo y utilidad contra varios enemigos sin convertir una defensiva base de LianQi I en respuesta universal a todo encuentro multiobjetivo.

## Guardia

Este stress no se usa para balancear AOE ni dificultad final de grupos.

No se cambia runtime, Piel, Placas, Paso, HP de monstruos ni cantidad real de monstruos por encuentro.

Sólo identifica un riesgo de escalado.
