# Resolved Combat Signal Adapter — New Engine

## Objetivo

Conectar resultados **ya resueltos por el motor nuevo** con Semantic Memory sin parsear texto, inferir estados ni recalcular combate.

El adapter no conoce fórmulas de impacto, DEF, Evasión, Absorción, curación ni Qi. Sólo recibe del resolver un resultado estructurado.

## Absorción

Entrada mínima:

```text
round
absorbido
```

Salida:

```text
absorbido > 0 → PLAYER_ABSORPTION_RESOLVED / effective=true
absorbido = 0 → PLAYER_ABSORPTION_RESOLVED / effective=false
```

## Recuperación

Entrada mínima:

```text
round
vidaRecuperada
qiRecuperado
```

Los deltas deben venir ya cerrados por el motor. Está prohibido reconstruirlos desde logs o comparando estados posteriores.

## Seguridad

- objetos planos y shape exacto;
- sin Symbols/accessors/campos extra;
- valores no negativos y finitos;
- outcomes congelados;
- sin mutación del combate;
- sin decisiones tácticas;
- sin compatibilidad con resolvers anteriores.

## Regla

```text
NEW COMBAT RESOLVER
→ resolved structured signal
→ adapter
→ semantic memory
```

El adapter nunca ejecuta el camino inverso ni contiene fallback.
