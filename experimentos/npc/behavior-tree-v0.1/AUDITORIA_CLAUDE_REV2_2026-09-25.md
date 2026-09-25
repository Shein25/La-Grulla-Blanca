# Auditoría externa REV2 — Behavior Tree v0.1

## Identificación

- Auditor: Claude, retest adversarial independiente.
- Fecha: 2026-09-25.
- Rama: `experiment/npc-behavior-tree-v0.1`.
- HEAD auditado: `0d44c5289f189e21c85584706da37af4ffafd103`.
- PR: #16, OPEN / DRAFT / NO MERGED.
- Base: `chore/organizar-experimentos-npc-monstruos`.
- Snapshot inmutable posterior: `snapshot/npc-behavior-tree-v0.1-rev2-audited`.

## Integridad

- 17/17 archivos del paquete: OK por SHA-256.
- 9/9 archivos fuente: git blob hashes coincidentes con el manifiesto del paquete.
- `tests.mjs` histórico: byte-idéntico respecto a REV1.

## Suites

- histórica: 34/34 PASS;
- REV2: 6/6 PASS;
- batería independiente de preempción: 27/27 PASS;
- batería adversarial general heredada de REV1: 52/52 PASS;
- hallazgos nuevos: 0.

## Verificación masiva de preempción

Sobre 500.000 ticks generados independientemente:

- 116.055 finalizaciones terminales;
- 163.554 abandonos sin resultado;
- 60.091 abandonos con RUNNING;
- 0 violaciones de la semántica REV2.

Semántica confirmada:

- SUCCESS/FAILURE terminal => `preemptedAction = null`;
- desplazamiento sin resultado => preempción real;
- RUNNING + desplazamiento => preempción real.

## Stress multiseed

Cinco seeds × 100.000 ticks:

- 1337 → `b8b316221567ea86d2335e346caa244b8c16a18cce911a1a121888da7f16e286`
- 1 → `786a551d20fefffc1d1f5884e5980e661d7cc012c52e07ea1e3ef743d0f22766`
- 42 → `49e43f63a04846de21d39bebf655c6c03f3d314b60f787778d3a487dfa87c7bd`
- 999 → `e8c7bb4817ea0b57879739eb49b0d50524a507dee716d7d08220e71acbf6b6f9`
- 20260925 → `8985e74923d85e10bdd43d861bcc944c16aa391e4ba1510959e58267ca52827a`

En todas:

- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidRuntime = 0`;
- `multiEmit = 0`.

## Hallazgo residual aceptado

La identidad del runtime frente a cambios de topología/intents queda definida por contrato y no forzada por hash/versionado:

> Un runtime pertenece a una definición estructuralmente estable del árbol; cambiar topología, IDs o intents exige crear un runtime nuevo.

La auditoría lo considera observación residual documentada, no bug de REV2.

## Frontera arquitectónica

El motor:

```text
reevalúa prioridades
→ selecciona como máximo una acción
→ emite intención
→ executor externo resuelve
```

No ejecuta movimiento, combate ni efectos del mundo.

## Veredicto

```text
BEHAVIOR_TREE_V01_REV2_APTO_PARA_ITERAR
```
