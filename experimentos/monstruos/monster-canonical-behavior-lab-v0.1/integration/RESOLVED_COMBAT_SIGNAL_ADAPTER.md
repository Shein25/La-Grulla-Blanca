# Resolved Combat Signal Adapter v0.1

## Objetivo

Conectar **resultados ya resueltos** por el combate productivo con el contrato del Semantic Memory Recorder sin parsear texto ni inferir desde HP futuro.

## Absorción — integración disponible

En ver74, `respuestaEnemigos()` llama:

```js
const r = this.absorberGolpe(gu, dmg);
```

y `absorberGolpe()` devuelve explícitamente:

```text
{ absorbido, rota, extra }
```

Por tanto el hook mínimo puede pasar únicamente:

```text
round
r.absorbido
```

a:

`absorptionOutcomeFromResolvedHit()`.

Regla:

```text
absorbido > 0 → PLAYER_ABSORPTION_RESOLVED / effective=true
absorbido = 0 → PLAYER_ABSORPTION_RESOLVED / effective=false
```

No se inspeccionan HP ni logs.

## Recuperación — contrato preparado, hook productivo pendiente

`beber()` en ver74 retorna:

```text
[msgs, bebido]
```

y actualmente expresa la cantidad recuperada dentro de texto o mediante mutación del player.

Eso **no es suficiente** para el recorder bajo su contrato estricto: no debemos parsear mensajes ni reconstruir el resultado comparando estados posteriores.

El adapter define el contrato futuro:

```text
round
vidaRecuperada
qiRecuperado
```

pero la producción todavía tendría que exponer esos deltas explícitamente en el punto donde ya fueron resueltos.

## Seguridad

El adapter:

- exige objetos planos y shape exacto;
- rechaza Symbols/accessors/campos extra;
- rechaza valores negativos o no finitos;
- devuelve outcomes congelados;
- no muta combate;
- no decide tácticas.

## Estado

`RESOLVED_COMBAT_SIGNAL_ADAPTER_V01: 13_PASS_0_FAIL_CONFIRMED`


## Verificación

```text
PASS: 13
FAIL: 0
```

Absorción queda lista para un hook productivo mínimo en el call-site de `absorberGolpe()`.

Recuperación queda **contract-ready**, pero no product-ready hasta que `beber()` exponga deltas estructurados de vida/qi recuperados.
