# ver74 structured hooks v0.1 — absorción

## Alcance

Rama experimental derivada exactamente de:

`289a090b83f2e0f3652c93c870f88ec2c4256bc4`

No toca `main`, no mergea PR #18 y no modifica los motores congelados.

## Cambio mínimo

En la copia de ver74 de esta rama se agregó un hook opcional:

`juego.onPlayerAbsorptionResolved`

El hook se invoca únicamente después de que `absorberGolpe()` ya resolvió el golpe y recibe un objeto congelado con shape exacto:

```js
{ round, absorbido }
```

Ese shape entra directamente en `absorptionOutcomeFromResolvedHit()` del laboratorio sin parsear logs, sin leer HP y sin inferir resultados.

Si no existe consumidor, el hook es no-op y el combate conserva su flujo anterior.

## Prueba integrada añadida

Se registró en el banco `PRUEBAS`:

`integración monstruos: absorción expone señal estructurada`

Comprueba:

- una absorción real desde `respuestaEnemigos()`;
- una única señal;
- `round` preservado;
- `absorbido` resuelto;
- shape sin campos extra;
- payload congelado.

## No realizado en este commit

- no se tocó `beber()`;
- no se instrumentó recuperación;
- no se conectó todavía Monster AI al monolito;
- no se alteró `CADENCE_COMPAT`;
- no se tocó CANON ni perfiles experimentales;
- no se integró NPC↔monstruos.

Siguiente paso, después de verificar este hook: instrumentar `beber()` para exponer deltas estructurados `vidaRecuperada` / `qiRecuperado`, manteniendo los dos valores de retorno existentes para compatibilidad.
