# Resultado — Resolved Combat Signal Adapter v0.1

## Verificación

```text
PASS: 13
FAIL: 0
```

Confirmado:

- absorción positiva → `PLAYER_ABSORPTION_RESOLVED / effective=true`;
- absorción cero → `effective=false`;
- salida congelada;
- valores negativos/no finitos rechazados;
- campos de HP/log/mensaje rechazados;
- ronda inválida rechazada;
- recuperación de vida estructurada → `PLAYER_RECOVERY_RESOLVED`;
- recuperación de qi estructurada → `PLAYER_RECOVERY_RESOLVED`;
- recuperación cero → `effective=false`;
- deltas negativos/campos extra rechazados;
- salida alimenta directamente al Semantic Memory Recorder;
- múltiples señales en la misma ronda preservan orden de inserción.

## Compatibilidad con ver74

### Absorción

Compatible con el punto real:

```js
const r = this.absorberGolpe(gu, dmg);
```

El resultado ya contiene `r.absorbido`.

### Recuperación

`beber()` todavía retorna `[msgs, bebido]`; no expone deltas estructurados.

Por tanto:

- absorción: hook listo;
- recuperación: contrato listo, hook productivo pendiente;
- no se parsean mensajes;
- no se infiere desde HP posterior.

## Estado

`RESOLVED_COMBAT_SIGNAL_ADAPTER_V01: 13_PASS_0_FAIL_CONFIRMED`
