# HUMAN DECISION — LII T2 Recognition Freeze

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: **T2 HUMAN-RATIFIED / FROZEN**

## Decisión

El usuario aprueba congelar LianQi II T2 tal como fue validado en `LII_T2_RECOGNITION_GATE_V01_REVIEW.zip`.

ID canónico congelado:
`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

Alias observado en la evidencia:
`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE_REACTIVE`

El alias no representa una variante nueva.

## Semántica congelada

- memory_window = 2
- repeated_same_category_required = 2
- sólo resultados `EFECTIVA`
- categorías: BASIC / UNITARGET / AOE / DEFENSIVE
- anticipación: HP <=40% OR golpe recibido >=15% maxHP
- prioridad: T1 natural 30/20 antes que anticipación T2 40/15
- T2 no consume turno
- T2 no modifica magnitud ni cooldown de T1
- T2 no crea una habilidad activa nueva
- T2 preserva la técnica canónica cuando está due

T1 permanece congelado:
- Sapo: MITIGATE_NEXT 60% / CD3 / REACTIVE
- Escarabajo: DEFENSE_UP +4 / CD3 / REACTIVE

## Evidencia

- gate input SHA-256: `0a982fbf34a6235849729069e86a127aa27b6004a38f12c3a8574b7de2e3586d`
- notebook SHA-256: `7237acb37be3a80be628c567311301d2bcbe62c54c3791f307877d784441dc02`
- runner SHA-256: `6dc81b2a1c1ff4dfc0eba4029f8136e0999a96b9bb5e91d302fd0685c1949457`
- REVIEW SHA-256: `aec7c2c40dd8c29b2d22d3ae70c62e2966ae067803bd673bcb841036b0227fd0`
- combates: 61.440
- timeout: 0
- NaN/Inf: 0
- leakage T2 en brazo T1: 0
- canonical due perdida con activación T2: 0
- contextos HRS con caída >8 pp: 0
- contextos donde T2 fue >2 pp más fácil: 0

Win-rate global pareado:
- T1: 53,5905%
- T2: 51,3770%
- delta: -2,2135 pp

## Interpretación

T2 introduce reconocimiento y anticipación reales con un impacto global moderado. No se retunea: su función es añadir memoria/predicción y dejar espacio de progresión para T3 causal y T4.

## Siguiente estado

- sapo_ceniza -> READY_FOR_T3_RECALIBRATION
- escarabajo_hierro -> READY_FOR_T3_RECALIBRATION
- T4 continúa bloqueado hasta cerrar T3

No se diseña ni ejecuta T3 en este cierre.
No main. No merge. No T5. No cambios a LI/T0/T1.
