# Behavior Tree v0.1 — Cambios REV2

Fuente: auditoría adversarial independiente sobre HEAD `ec73c31a12b4e5de593536253725ead0f813f2dc`.

Veredicto REV1:

`BEHAVIOR_TREE_V01_REQUIERE_CORRECCIONES`

## Hallazgo 1 — preemptedAction

REV1 marcaba como preemptada cualquier acción anterior cuyo ID dejara de ser `runningAction`, incluso si el executor acababa de informar `SUCCESS` o `FAILURE`.

REV2 distingue:

- resultado terminal `SUCCESS/FAILURE` → finalización normal, `preemptedAction = null`;
- sin resultado terminal + acción desplazada → preempción real;
- resultado `RUNNING` + acción desplazada → preempción real.

La corrección es local a la semántica de `preemptedAction`; no altera selector, sequence, condition, action ni la frontera con el executor.

## Hallazgo 2 — cambio de árbol con runtime vivo

La auditoría lo clasificó como borde contractual, no como violación explícita. REV2 adopta la solución documental:

> Un runtime pertenece a una definición estructuralmente estable del árbol. Cambiar topología, IDs o intents durante su vida está fuera de contrato y exige crear un runtime nuevo.

No se añade hashing ni versionado estructural en v0.1 para mantener pequeño el contrato.

## Nota -0

Se documenta que `EQ/NEQ/IN` usan `Object.is` y distinguen `-0` de `0`; `GT/GTE/LT/LTE` usan comparación numérica normal.

## Tests REV2

Se añade `tests-rev2.mjs` con 6 regresiones dirigidas al bug de preempción.

## Alcance

No se añaden NPC canónicos, Utility AI, GOAP, HTN, pathfinding ni integración con producción.
