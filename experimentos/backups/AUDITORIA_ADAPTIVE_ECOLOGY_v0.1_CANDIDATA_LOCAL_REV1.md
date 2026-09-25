# Auditoría independiente — Adaptive Ecology v0.1
## Candidata local REV1 — 2026-09-25

Veredicto:

`ADAPTIVE_ECOLOGY_V01_REQUIERE_CORRECCIONES`

La arquitectura y la lógica normal son correctas, pero la frontera de validación necesita una REV2 local antes de materializar la rama experimental.

## Evidencia reproducida

```text
node tests.mjs
PASS: 62
FAIL: 0

node stress.mjs
TRANSITIONS: 100000
DIGEST run1:
632f61b2468b89e4b280a48b62ea2d31c44e01ba4c02b1bdcb2722a41a3ae821
DIGEST run2:
632f61b2468b89e4b280a48b62ea2d31c44e01ba4c02b1bdcb2722a41a3ae821
MATCH: true
```

Oráculo independiente:

```text
REFERENCE_FUZZ_CASES: 20000
REFERENCE_FUZZ_MISMATCHES: 0
```

Git verificado:

```text
main = 5812deb59cd1c133383b9af973486a702a26daf4
experiment/monster-ecology-adaptation-v0.1 = NO EXISTE
```

## Bloqueantes

### B1 — knownAbilityIds opcional

La implementación permite omitir `knownAbilityIds`, activando un modo sin filtrado. Se reprodujo:

```text
knownAbilityIds omitido
adaptation tier contiene "hack_skill"
→ effectiveKit incluye "hack_skill"
→ debug.unknownAbilityIds vacío
```

La especificación FINAL exige filtrar abilities desconocidas.

REV2 debe hacer `knownAbilityIds` obligatorio y emitir ContractError si falta/null/tipo incorrecto.

### B2 — recentEventIds puede exceder dedupWindowSize

Se reprodujo:

```text
dedupWindowSize = 2
recentEventIds = ["a","b","c","d"]
event = null
→ nextState mantiene length 4
```

REV2 debe validar de forma cruzada:
`recentEventIds.length <= dedupWindowSize`.

## Hardening

### H1 — Proxy/TOCTOU

Un Proxy sobre `recentEventIds` puede pasar validación y luego mentir en `.includes()`, permitiendo reaplicar un ID ya presente.

REV2 debe aplicar:

```text
input externo
→ captura única
→ snapshot interno plano
→ validación
→ cálculo sólo sobre snapshot
```

al menos para arrays de state/config.

### H2 — propiedades heredadas

Un `populationState = Object.create(validState)` sin propiedades propias es aceptado.

REV2 debe exigir own properties para campos requeridos y evitar satisfacer contratos mediante prototype.

## No bloqueantes a corregir

- El test cuyo nombre dice “recentEventIds with duplicates -> ContractError” en realidad espera `STATUS.OK`.
- `nondeterministicMismatches` se inicializa en 0 pero no se mide; el digest sí mide determinismo, pero esa métrica debe dejar de ser decorativa.

## Próximo paso

No crear aún la rama real.

Hacer REV2 local pequeña, rerun tests/stress/digest y repetir adversariales independientes. Sólo después materializar:

`experiment/monster-ecology-adaptation-v0.1`
