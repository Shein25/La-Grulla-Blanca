# Auditoría externa REV2 — Reactive Routine FSM v0.1

## Identificación

- Auditor/modelo: Claude (Sonnet 5), vía Claude.ai.
- Fecha: 2026-09-25.
- Rol: revisor adversarial externo e independiente.
- HEAD auditado: `e001730675fdd0a780c273cbfad2e46c045d64a9`.
- Rama auditada: `experiment/npc-reactive-routine-fsm-v0.1`.
- Snapshot inmutable posterior: `snapshot/npc-reactive-routine-fsm-v0.1-rev2-audited`.

## Integridad

- 15/15 archivos del paquete coinciden con `SHA256SUMS.txt`.
- `fixtures.mjs`, `tests.mjs` y `stress.mjs` permanecieron byte-idénticos respecto de REV1.
- `engine.mjs` y la documentación REV2 cambiaron como se esperaba.

## Suites

- suite histórica: 30/30 PASS;
- suite REV2: 17/17 PASS;
- batería adversarial independiente: 77/77 PASS;
- hallazgos nuevos: 0.

## Stress

Cinco seeds × 100.000 eventos:

- 1337 → `b98864d75ad4851d4be47d80ca24cb4d2deda75c83605fd81e5bed1738c87534`
- 1 → `3d4e13bbbdbdd20820ae42e9bcdb2dc224b2ee34d6c38ae7d9ebd2a133dabccf`
- 42 → `54643d4bc1d686724b051a1b6ac6da0f1a3890ea15cf78511c3b2a2ed419c35d`
- 999 → `a17f931a309466c100c76795b6105ee4e26d9f14696595a0db3d11821ab76195`
- 20260925 → `f1c9ed91ac3b6913d935e503071cd1eb84b083d5cab15e881ffc91191d9a26c8`

En todos:

- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidStates = 0`.

Los digests son byte-idénticos a REV1.

## Retest H1–H6

- H1: RESUELTO — saturación de `stateAge` y `step` preserva round-trip del runtime.
- H2: RESUELTO — guards runtime restringidos a las cuatro claves declaradas.
- H3: RESUELTO — superficies reflectivas hostiles fallan con `ContractError`.
- H4: RESUELTO — `MAX_GUARD_DEPTH = 32`; profundidad excesiva falla con `ContractError`, no `RangeError`.
- H5: RESUELTO — comparadores numéricos estrictos; semántica de fact ausente documentada.
- H6: RESUELTO — arrays contractuales rechazan propiedades extra, huecos, Symbols y accessors.

## Deuda no bloqueante

Permanece únicamente deuda ya conocida y fuera de alcance de REV2:

- H7: Proxy transparente indistinguible de objeto plano, considerado comportamiento correcto;
- H9: revalidación completa de máquina en cada `stepFSM()`, potencial deuda de rendimiento si el alcance crece mucho.

## Alcance

No se integraron NPC canónicos ni se añadieron Utility AI, GOAP, HTN, Behavior Trees, pathfinding o lógica de producción.

## Veredicto

```text
REACTIVE_ROUTINE_FSM_V01_REV2_APTO_PARA_ITERAR
```
