# Auditoría externa — Monster Combat AI v0.1 — REV2

Fecha: 2026-09-25

Agente auditor: Claude (auditor externo offline)
Modelo/versión declarada: Claude Sonnet 5

Snapshot auditado:

```text
branch = experiment/monster-combat-ai-v0.1
HEAD   = aecbbcac1f2243dad16e2f881fdc6b683debe616
base   = 5812deb59cd1c133383b9af973486a702a26daf4
tree   = d1e4bb82c90032c8bae37361867ab6c1190a0a8c
PR     = #13 (Draft)
```

El auditor no tuvo acceso de red a GitHub. Verificó localmente:

- SHA-256 del paquete;
- Git blob SHA-1 de los 9 archivos;
- 38/38 tests;
- 50.000 decisiones de stress;
- seed 1337 repetida con digest byte-idéntico:
  `4cee9933469e7d8545741b067f57ef023e49eb9a2ac4a3a104650cd84abe5c18`;
- arnés propio con 17 verificaciones;
- 5.200 casos propios de fuzz coherente;
- 0 invalidSelections;
- 0 inputMutations;
- 0 executionSideEffects;
- 0 nondeterministicMismatches.

REV2 confirmada:

1. reorder invariance con jitter;
2. cooldowns estrictamente booleanos;
3. memoryInfluencedCases mide contribución real;
4. executionSideEffects se mide mediante replay determinista.

Hallazgos bloqueantes:

`Ninguno`

Deudas no bloqueantes aceptadas:

- D-MON-15 — orden diagnóstico de debug.considered;
- D-MON-16 — límite conceptual de executionSideEffects.

Veredicto externo:

`MONSTER_COMBAT_AI_V01_APTO_PARA_ITERAR`

Verificación posterior desde GitHub realizada fuera del entorno del auditor:

```text
main = 5812deb59cd1c133383b9af973486a702a26daf4
PR #13 = OPEN / DRAFT / NOT MERGED
PR base SHA = 5812deb59cd1c133383b9af973486a702a26daf4
PR head SHA = aecbbcac1f2243dad16e2f881fdc6b683debe616
ahead_by = 1
behind_by = 0
changed files = 9
```

Todos los archivos modificados siguen únicamente bajo:

`experimentos/monster-ai/monster-combat-ai-v0.1/`

No mergear automáticamente.
