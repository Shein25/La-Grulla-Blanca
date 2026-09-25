# Reactive Routine FSM v0.1 — Cambios REV2

Fuente: auditoría externa adversarial de Claude (Sonnet 4.6), 2026-09-25, sobre `experiment/npc-reactive-routine-fsm-v0.1@34f53cd541e098a8a943b1b500575643899e1d42`.

Veredicto recibido:

`REACTIVE_ROUTINE_FSM_V01_REQUIERE_CORRECCIONES`

La auditoría reprodujo 30/30 tests, los cinco stress de 100.000 eventos y los digests documentados. No cuestionó la hipótesis arquitectónica; detectó defectos de hardening dentro del contrato.

## H1 — BLOCKER: contadores fuera de contrato
REV2 satura `stateAge` y `step` en `Number.MAX_SAFE_INTEGER`, preservando la reinyectabilidad del runtime.

## H2 — HIGH: lectura heredada desde runtime
REV2 limita `source:'runtime'` a `machineId`, `state`, `stateAge`, `step`.

## H3 — MEDIUM: excepciones nativas desde Proxy hostil
REV2 envuelve inspecciones reflectivas y normaliza fallos de entrada hostil a `ContractError`.

## H4 — MEDIUM: profundidad ilimitada de guards
REV2 fija `MAX_GUARD_DEPTH = 32`; una profundidad superior se rechaza antes de evaluación.

## H5 — LOW: comparadores semánticamente inválidos
REV2 exige `value` numérico para `GT/GTE/LT/LTE`; sobre runtime esos operadores sólo aceptan `stateAge` o `step`. Se documenta fact ausente + `NEQ` y se conserva `Object.is`.

## H6 — LOW: arrays contractuales con propiedades extra
REV2 rechaza huecos, accessors, Symbols y propiedades extra en arrays contractuales.

## Regresión local
- suite histórica: 30/30 PASS;
- regresiones REV2: 17/17 PASS;
- total lógico: 47 PASS / 0 FAIL;
- cinco stress de 100.000 eventos mantienen exactamente los digests REV1;
- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidStates = 0`.

## Alcance preservado
No se añaden Utility AI, GOAP, Behavior Trees, HTN, pathfinding, NPC canónicos ni integración con producción.
