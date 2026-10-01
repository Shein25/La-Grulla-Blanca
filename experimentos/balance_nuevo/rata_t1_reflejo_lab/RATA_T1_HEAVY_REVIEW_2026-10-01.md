# Rata T1 — revisión de RESULTADOS_RATA_T1_REFLEJO_HEAVY

Fecha: 2026-10-01

## Integridad

- ZIP SHA-256: `11a1fd44d7e8f8f90d12ef374cb73fadb9d985f392dd922844f25509623da5f2`
- Experimento: `RATA_T1_REFLEJO_CALIBRATION_V01`
- T0 fuente: `rata_qi READY trial 4254`
- T0: HP 21 / PREC 80 / EVA 0 / DEF 0 / TEN 0 / CTRL 0 / crit 5% / x1.50 / basic 2d4
- resource_model: NONE
- search: 50 configuraciones, 1000 peleas/contexto
- high precision: 7 configuraciones, 20000 peleas/contexto
- 10 contextos por brazo
- raw fights: no persistidos
- T2-T4: no ejecutados

La estructura y el manifest son consistentes con el contrato T1 LAB.

## Baseline T0 high precision

- 200000 peleas
- win rate jugador: 1.0
- rondas medias: 2.763965
- HP final medio jugador: 0.8888204962
- daño medio total monstruo: 3.5229378
- hit rate jugador: 1.0

## Resultado numérico de magnitud

Los siete representantes high precision fueron:

| EVA bonus | CD | evades adicionales/pelea | extensión rondas | activaciones/pelea | hit rate jugador | retención daño monstruo |
|---:|---:|---:|---:|---:|---:|---:|
| +5 | 5 | 0.01749 | 0.01414 | 0.99866 | 0.99370 | 0.37867 |
| +15 | 5 | 0.11412 | 0.11122 | 0.99866 | 0.96030 | 0.43431 |
| +25 | 5 | 0.21338 | 0.21076 | 0.99866 | 0.92822 | 0.49087 |
| +40 | 5 | 0.36278 | 0.36065 | 0.99866 | 0.88381 | 0.57624 |
| +50 | 5 | 0.46333 | 0.46175 | 0.99866 | 0.85625 | 0.63393 |
| +50 | 3 | 0.46350 | 0.46192 | 0.99901 | 0.85620 | 0.63391 |
| +50 | 1 | 0.62711 | 0.62476 | 1.35269 | 0.81406 | 0.53328 |

Los brazos EARLY/BASE/LATE son extremadamente estables en estas métricas.

## Qué sí demuestra la corrida

1. `EVADE_NEXT` funciona mecánicamente.
2. La magnitud responde de forma monotónica y estable.
3. +5 es prácticamente invisible.
4. +15 produce una defensa perceptible pero todavía pequeña.
5. +25 / +40 / +50 forman un rango útil de moderado a fuerte.
6. CD1 permite más de una activación por pelea y altera claramente el patrón.
7. CD3, CD4 y CD5 son casi indistinguibles en los combates T1 actuales; la pelea suele terminar antes de que esa diferencia importe.
8. Para evitar spam adaptativo en tiers posteriores, CD5 es el valor conservador que debe pasar a revalidación.

## Hallazgo de arquitectura: NO cerrar T1 todavía

El harness Heavy no ejecuta el selector adaptativo original.

En `survival-evolution-v0.1.mjs`, T1:
- cambia `INSTINTIVO -> REACTIVO_1`;
- añade `rata_qi__survival_1` al `effectiveKit`;
- deja que Monster Combat AI puntúe BASIC vs SURVIVAL;
- la supervivencia usa utility base + señales + jitter + repetición.

El harness Heavy, en cambio, intercepta `execute_monster_turn` y activa Reflejo de forma obligatoria cuando ocurre:

`SELF_LOW_HP OR TOOK_HEAVY_HIT`

Por eso la tasa observada ronda 1 activación por pelea y los brazos de señal resultan casi idénticos.

Eso es adecuado como **stress/calibración de magnitud por activación**, pero no representa la frecuencia final de decisión de la IA.

Además, la selección forzada consume el turno del monstruo. Por eso T1 reduce el daño total del monstruo respecto de T0 incluso cuando aumenta su supervivencia. No se debe interpretar esa reducción como resultado final de la IA adaptativa.

## Contrato del selector original relevante

Para Rata T1, con `REACTIVO_1`:
- BASIC base = 40
- SURVIVAL base = 18
- SELF_LOW_HP = +22
- TOOK_HEAVY_HIT = +10
- PLAYER_LOW_HP = +3
- jitter REACTIVO_1 = ±3
- repetition penalty = 5

Consecuencia:
- heavy hit por sí solo no alcanza para vencer BASIC;
- SELF_LOW_HP vuelve Reflejo competitivo;
- SELF_LOW_HP + TOOK_HEAVY_HIT vuelve Reflejo fuertemente preferido.

La revalidación correcta debe por tanto ser **decision-aware**, no un segundo grid de 50 configuraciones.

## Input reducido para revalidación decision-aware

Conservar solamente:

- EVA +25 / CD5 — límite moderado
- EVA +40 / CD5 — candidato provisional central
- EVA +50 / CD5 — límite fuerte

Estado:

`MAGNITUDE_CALIBRATED_DECISION_FREQUENCY_PENDING`

No escribir todavía valores T1 en CANON.
No habilitar T2.
No modificar el T0 READY.
