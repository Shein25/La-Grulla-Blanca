# Auditoría externa REV2 — Reactive Routine FSM v0.1

Audita exclusivamente la cabeza actual de `experiment/npc-reactive-routine-fsm-v0.1` como experimento independiente.

La auditoría REV1 de Claude terminó en:

`REACTIVE_ROUTINE_FSM_V01_REQUIERE_CORRECCIONES`

REV2 pretende cerrar únicamente H1–H6 sin ampliar arquitectura.

NO modifiques producción.
NO integres NPC canónicos.
NO añadas Utility AI, GOAP, Behavior Trees, HTN o pathfinding.
NO hagas merge.

## 1. Integridad y revisión

- reporta HEAD exacto;
- lee `README.md`;
- lee `CAMBIOS_v0.1_REV2.md`;
- confirma que los tres fixtures no cambiaron semánticamente.

## 2. Suite histórica

```bash
node tests.mjs
```

Debe permanecer:

`30 PASS / 0 FAIL`.

## 3. Regresiones REV2

```bash
node tests-rev2.mjs
```

Debe producir:

`17 PASS / 0 FAIL`.

No te limites a confiar en esos tests: reproduce independientemente cada H1–H6.

## 4. Stress determinista

```bash
node stress.mjs 100000 1337
node stress.mjs 100000 1
node stress.mjs 100000 42
node stress.mjs 100000 999
node stress.mjs 100000 20260925
```

Los digests del camino normal deben seguir siendo exactamente los de REV1:

- 1337: `b98864d75ad4851d4be47d80ca24cb4d2deda75c83605fd81e5bed1738c87534`
- 1: `3d4e13bbbdbdd20820ae42e9bcdb2dc224b2ee34d6c38ae7d9ebd2a133dabccf`
- 42: `54643d4bc1d686724b051a1b6ac6da0f1a3890ea15cf78511c3b2a2ed419c35d`
- 999: `a17f931a309466c100c76795b6105ee4e26d9f14696595a0db3d11821ab76195`
- 20260925: `f1c9ed91ac3b6913d935e503071cd1eb84b083d5cab15e881ffc91191d9a26c8`

Exige además:

- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidStates = 0`.

## 5. Retest obligatorio H1–H6

### H1
- `stateAge = Number.MAX_SAFE_INTEGER` + evento no manejado;
- `step = Number.MAX_SAFE_INTEGER`;
- la salida debe permanecer válida y reinyectable;
- la política esperada es saturación, no wrap ni BigInt.

### H2
Intenta guards runtime con `constructor`, `hasOwnProperty`, `__proto__`, `toString`.
Deben rechazarse. Sólo `machineId`, `state`, `stateAge`, `step` son válidas.

### H3
Prueba Proxy revocado, `getPrototypeOf`, `ownKeys` y `getOwnPropertyDescriptor` que lancen, sobre machine/event/runtime cuando corresponda.
La entrada hostil debe cerrar con `ContractError`.

### H4
- nesting exactamente en `MAX_GUARD_DEPTH` debe validarse;
- `MAX_GUARD_DEPTH + 1` debe rechazarse con `ContractError`;
- profundidad extrema no debe producir `RangeError`.

### H5
- `GT/GTE/LT/LTE` con expected no numérico deben rechazarse;
- esos operadores sobre `runtime.machineId` o `runtime.state` deben rechazarse;
- sobre `runtime.stateAge` y `runtime.step` deben funcionar;
- confirma la semántica documentada: fact ausente + `NEQ` es verdadero;
- `EQ/NEQ` continúan usando `Object.is`.

### H6
Prueba propiedades extra, Symbols, huecos y accessors en arrays de transición, `emit`, `all/any` e `IN.value`.
Deben rechazarse sin ejecutar getters.

## 6. Busca regresiones nuevas

Intenta romper determinismo, pureza, prioridad independiente del orden físico, una transición máxima por evento, validez del `nextRuntime`, aliasing, límites de arrays/guards y valores límite de enteros seguros.

## 7. Entregable

Devuelve un informe Markdown con entorno, HEAD, comandos, resultados, reproducción de H1–H6 y cualquier hallazgo nuevo.

Termina exactamente con uno:

```text
REACTIVE_ROUTINE_FSM_V01_REV2_APTO_PARA_ITERAR
REACTIVE_ROUTINE_FSM_V01_REV2_REQUIERE_CORRECCIONES
REACTIVE_ROUTINE_FSM_V01_REV2_FALLO_CONCEPTUAL
```
