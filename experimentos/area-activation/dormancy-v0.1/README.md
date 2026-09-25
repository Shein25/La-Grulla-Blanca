# Area Activation / NPC Dormancy v0.1

**Sólo el área actual del jugador participa de simulación continua.** Todas
las demás áreas están dormidas. En ellas hay **0 Scheduler, 0 Utility, 0 GOAP,
0 Pathfinder y 0 Executor**. Esta capa únicamente responde qué área debe
estar activa y cuánto tiempo llevaba dormida cuando el jugador entra.

```text
GLOBAL TURN → Area Activation
                    ├─ área del jugador: ACTIVE → futuro Scheduler
                    └─ otras áreas: DORMANT → sin simulación por turno
```

No se importan otros motores ni áreas, rooms o NPC canónicos. Los fixtures
contienen sólo IDs sintéticos. Tampoco se modela qué NPC pertenece a cada área.

## API

`createAreaActivationState(configs)` recibe un array no vacío de `{ id }`,
con IDs string no vacíos y únicos. Devuelve `{ version:1, clock:null,
activeAreaId:null, areas }`, con áreas ordenadas por ID y
`lastSimulatedTurn:0`. `activeAreaId` es la **única fuente de verdad** sobre
qué área está activa; ninguna área almacena un flag `active`.

`activatePlayerArea(state, currentTurn, playerAreaId)` devuelve:

```js
{
  status, state, previousAreaId, activeAreaId,
  deactivation, activation, catchUp
}
```

Los estados son `INITIAL_ACTIVATION`, `AREA_SWITCHED` y `ALREADY_ACTIVE`.
`currentTurn` es un entero seguro no negativo; después del primer uso debe
superar estrictamente `state.clock`. Se rechazan áreas desconocidas. No se
usa reloj real ni timers.

En la activación inicial desde el estado recién creado, un tick `0` produce
`catchUp:null`; un tick `25` produce `0 → 25`, elapsed `25`. Al continuar
en la misma área se devuelve `ALREADY_ACTIVE`, sin nueva activación,
desactivación ni catch-up. Se avanza `clock` sin tocar innecesariamente
`lastSimulatedTurn` del área activa. Al salir, el área anterior se sincroniza
al turn real de salida.

Un estado con `clock !== null` y `activeAreaId === null` es válido como estado
con cero áreas activas. En cambio, si `clock === null`, se exige el estado
inicial puro: `activeAreaId === null` y todos los `lastSimulatedTurn === 0`.

## Dormancia y catch-up

Para un área dormida, `lastSimulatedTurn` indica hasta qué turn se considera
sincronizada. Al entrar en ella:

```text
elapsedTurns = currentTurn - lastSimulatedTurn
```

Si el elapsed es positivo se emite **una sola** solicitud
`{ areaId, fromTurn, toTurn, elapsedTurns }`. No se incrementa un contador
de sueño cada turno ni se recorre un rango de turns. Un millón de turns
dormidos sigue produciendo un único request. La resta y todos los turns
deben ser enteros seguros.

La transición `A → B` actualiza sólo `A` y `B`. Otras áreas conservan su
`lastSimulatedTurn`. El nuevo estado contiene exactamente un área activa,
identificada por `activeAreaId`.

**Contrato transaccional:** `result.state` es el estado candidato después de
una transición completada. Esta v0.1 no ejecuta el catch-up. La integración
futura debe obtener la transición, ejecutar el Catch-up Resolver si existe
`result.catchUp` y **sólo si tiene éxito** adoptar `result.state`. Así no se
declara sincronizada un área cuyo catch-up haya fallado.

```text
DORMANT → tiempo sin simulación → jugador entra
        → Area Activation calcula elapsed
        → futuro Catch-up Resolver
        → área sincronizada → futuro Scheduler
```

## Seguridad, límites y verificación

Configs y state se capturan por descriptores de propiedades propias. Se
rechazan accessors sin ejecutar getters, prototipos no planos, propiedades
heredadas usadas como campos, símbolos, holes, IDs duplicados y turns no
seguros. La API es pura: no modifica configs, state ni resultados anteriores.

```bash
node tests.mjs
node stress.mjs 1337 20000
node stress.mjs 1 20000
node stress.mjs 42 20000
node stress.mjs 999 20000
node stress.mjs 20260924 20000
```

El stress usa un oracle independiente con área activa y último turn
sincronizado por área. `collapsedDormantTurns` suma turns de dormancia
representados por `catchUpRequests` únicos, sin simularlos uno por uno.

Followers, companions, perseguidores, transportes, excepciones globales,
áreas vecinas warm, rutinas, recursos y catch-up real quedan para futuras
integraciones. La regla v0.1 es exclusivamente «área del jugador = ACTIVE».
