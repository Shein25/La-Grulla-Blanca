# Handoff — Monstruos bajo motor nuevo

**Fecha:** 2026-10-01  
**Rama de adaptación:** `experiment/monster-adaptive-survival-lab-v0.1`  
**Rama de estadísticas:** `experiment/combat-stat-contract-v0.1`

## Autoridad

Todos los monstruos se adaptan a:

`NEW_COMBAT_STATS_V0_1`

Fuente de balance:

`experimentos/balance_nuevo/monster_arc1_registry.json`

Catálogo del laboratorio adaptativo:

`monster-canonical-behavior-lab-v0.1/canonical/monsters.json`

Ambos usan el mismo esquema nuevo.

## Estado

- 18/18 monstruos del Arco 1 presentes.
- 18/18 T0 en `PENDING_INTEGRAL_REBALANCE`.
- ningún perfil pendiente puede combatir ni entrar a benchmark numérico;
- parámetros de técnicas pendientes bloquean resolución;
- T1–T4 conservan arquitectura/identidad, pero sus magnitudes de combate se recalibran después de T0;
- Definitivas del jugador: prohibidas en balance de monstruos.

## Arquitectura activa


- identidad de especies;
- roles y bandas ecológicas;
- familias mecánicas de técnicas;
- perfiles cognitivos/sociales;
- Tactical Overlay;
- Semantic Memory;
- Adaptive Ecology;
- thresholds/decay/learning ceiling;
- cerebro y counterplay cualitativo de la Grulla;
- pipeline de señales resueltas;
- validación estricta del esquema `NEW_COMBAT_STATS_V0_1`.

## Orden de trabajo

1. Balance integral T0 LianQi I: Rata, Avispa, Serpiente, Macaco, Lobo.
2. Congelar esos perfiles en unidades del motor nuevo.
3. Recalibrar sus técnicas y T1–T4 sobre esos T0.
4. Repetir T0 por LianQi II, III y IV.
5. Recalibrar adaptación por especie.
6. Reconstruir la resolución numérica de la Grulla sobre el motor nuevo cuando corresponda.

## Regla operativa

Si una integración futura no entiende `NEW_COMBAT_STATS_V0_1`, **debe fallar**. Se corrige esa integración para consumir el contrato activo.
