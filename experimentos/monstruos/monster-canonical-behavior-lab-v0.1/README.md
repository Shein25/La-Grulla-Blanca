# Monster Behavior Lab v1 — New Engine Only

Laboratorio aislado de comportamiento, adaptación e IA de los 18 monstruos del Arco 1.

## Fuente de monstruos

Existe un único catálogo:

`canonical/monsters.json`

Contrato:

`NEW_COMBAT_STATS_V0_1`

Los perfiles T0 todavía no calibrados permanecen en:

`PENDING_INTEGRAL_REBALANCE`

y no pueden entrar a un benchmark de combate.

## Flujo

```text
monster T0 READY
→ adaptive tier T0–T4
→ effectiveKit
→ Monster Combat AI
→ intent
→ new-engine intent bridge
→ new combat resolver
→ resolved signals
→ semantic memory
```

La IA decide; el resolver de combate ejecuta.

## Estadísticas

El laboratorio usa las estadísticas universales:

- HP / Qi;
- Precisión;
- Evasión;
- DEF;
- Tenacidad;
- Control;
- Crítico;
- Daño crítico;
- ataque básico;
- parámetros explícitos de técnicas.

No existe tabla paralela de escalado de estadísticas por etapa.

## Etapas

Las bandas nativas permanecen:

- LianQi I: 5 monstruos;
- LianQi II: 5 monstruos;
- LianQi III: 4 monstruos;
- LianQi IV: 4 monstruos.

La etapa define ecología, rol y techo de aprendizaje; no inventa estadísticas.

## Adaptación

Se conservan como arquitectura experimental:

- perfiles cognitivos;
- perfiles sociales;
- Tactical Overlay;
- Semantic Memory;
- señales resueltas;
- Adaptive Ecology;
- `C_STAGGERED` como dirección de trabajo;
- tiers T0–T4;
- thresholds/decay/`maxTierReached`;
- learning ceiling;
- Survival Evolution;
- arsenal adaptativo por especie.

Los valores numéricos que afecten combate se revalidan después de cerrar cada T0.

## Cadencia

La cadencia pertenece a los parámetros de la técnica del perfil nuevo:

`technique.params.cadence`

Mientras `params_status != READY`, no se permite resolver ni simular esa técnica.

## Estado actual

- 18/18 monstruos presentes en el esquema nuevo.
- 18/18 T0 pendientes de balance integral.
- Benchmarks numéricos antiguos retirados.
- Tests estructurales pueden ejecutarse.
- Benchmarks de combate quedan bloqueados hasta disponer de perfiles T0 `READY`.

## Guardia

`adaptive/monster-stat-source-contract-v0.1.mjs`

Todo perfil incompleto debe fallar de forma explícita. No hay fallback.
