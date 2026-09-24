# Area Catch-up Resolver v0.1

Laboratorio sintético e independiente para resolver el estado temporal de un área después de un período de dormancia. **Area Activation calcula cuánto tiempo pasó** y entrega `{areaId, fromTurn, toTurn, elapsedTurns}`. **Catch-up Resolver aplica ese tiempo** al snapshot. Esta versión no importa Area Activation ni ejecuta lógica de eventos.

```text
Dormancy: 500 → 2500 (elapsed = 2000)
Catch-up: timer 80 → 0; energy 30 → 100; hunger 80 → 0; event dueTurn 900 → due
```

Todo ocurre en una llamada sin iterar los 2000 turns.

## API

```js
import { resolveAreaCatchUp } from './catchup-resolver.mjs';

const result = resolveAreaCatchUp(state, catchUp);
// { status: 'CATCH_UP_APPLIED', state: nuevoEstado, summary: { ... } }
```

`state` contiene exactamente `version: 1`, `areaId`, `syncedTurn`, `entities` y `scheduledEvents`. Cada entidad contiene `id`, `timers` y `meters`. Cada timer contiene `id` y `remainingTurns`. Cada meter contiene `id`, `value`, `ratePerTurn`, `min` y `max`. Cada evento contiene `id`, `targetId` (`null` o ID de entidad), `kind` y `dueTurn`. Los eventos de entrada deben tener `dueTurn > syncedTurn`.

`catchUp` contiene exactamente `areaId`, `fromTurn`, `toTurn` y `elapsedTurns`. Se exige `areaId === state.areaId`, `fromTurn === state.syncedTurn`, `toTurn > fromTurn`, `elapsedTurns === toTurn - fromTurn` y `elapsedTurns >= 1`. Los turnos y duraciones son enteros seguros no negativos. Un elapsed cero se rechaza.

El resultado avanza `syncedTurn` a `toTurn`. Los timers se reducen hasta cero; los que llegan a cero por primera vez aparecen en `summary.completedTimers`. Los meters evolucionan linealmente y se limitan a `[min,max]`; sólo los cambios aparecen en `summary.meterChanges`. Los eventos con `dueTurn <= toTurn` salen de `state.scheduledEvents` y aparecen en `summary.dueEvents`. No se ejecuta `kind` ni se modifica ningún NPC por un evento.

Las entidades, los timers y los meters se ordenan por ID según comparación lexicográfica de JavaScript (sin locale). Los eventos vencidos y pendientes se ordenan por `dueTurn` y luego por ID. Los resúmenes de timers y meters siguen el orden canónico de entidades y registros. La salida y sus arrays son nuevos y están desacoplados de entradas y de otras ejecuciones.

## Validación y aritmética

La entrada se captura mediante descriptores de propiedades propias antes de ejecutar la lógica. Se rechazan accessors, campos extra, Symbols, herencia no plana, arrays con huecos o índices accessor y proxies que impiden la inspección estructural. La captura no invoca getters. Se exige unicidad de IDs en el ámbito correspondiente y enteros seguros para cada valor numérico. Un proxy que se presenta de forma indistinguible a un objeto ordinario no puede identificarse sólo por su forma; el contrato valida lo observable y no ejecuta getters.

La producción usa `BigInt` para la suma y multiplicación de meters. Esto evita desbordamientos intermedios incluso si `min` y `max` están en extremos opuestos del rango seguro. El resultado se limita primero a los bounds validados y sólo entonces se convierte a `Number`. El código no crea arrays por turn ni contiene loops cuyo límite sea `elapsedTurns`.

## Complejidad

El recorrido y las fórmulas requieren **O(entidades + timers + meters + scheduledEvents)** respecto de los registros del estado. Cada registro tiene **O(1) respecto del número de turns transcurridos**: un catch-up de 10 y uno de 1.000.000.000 recorren la misma estructura. Para producir orden canónico desde inputs desordenados, `sort` agrega `O(E log E + Σ Tᵢ log Tᵢ + Σ Mᵢ log Mᵢ + S log S)` en el peor caso (`E`: entidades; `Tᵢ`/`Mᵢ`: timers/meters de cada entidad; `S`: eventos). El tamaño máximo de `BigInt` está acotado por las entradas de tipo safe integer, no por la cantidad de turns iterados. El espacio adicional crece con la cantidad de registros y resultados, no con `elapsedTurns`.

## Ejecutar

```bash
npm test
npm run stress -- 1337
npm run stress -- 1
npm run stress -- 42
npm run stress -- 999
npm run stress -- 20260924
npm run stress -- 1337
```

El stress corre 2000 escenarios por seed, con 128 entidades, 0–5 timers y meters por entidad, y 500–2000 eventos. Usa un oracle BigInt independiente, verifica invariantes, entradas intactas y determinismo, y emite métricas con digest SHA-256. `totalElapsedTurns` se acumula como BigInt y se serializa en decimal.

## Límite de esta versión

Este laboratorio sólo resuelve timers, meters lineales y vencimiento informativo de eventos. Agenda, movimiento, decisiones, simulación narrativa e integración con otros módulos quedan para futuras fases.
