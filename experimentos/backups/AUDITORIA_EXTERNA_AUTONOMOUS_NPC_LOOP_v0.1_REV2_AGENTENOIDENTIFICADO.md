# Auditoría externa independiente — Autonomous NPC Loop v0.1 REV2

Fecha recibida: 2026-09-25.

Agente auditor: no identificado en el archivo.
Tipo: auditoría externa independiente offline.

Snapshot auditado según evidencia del paquete y verificación posterior:

```text
branch = experiment/npc-autonomous-loop-v0.1
HEAD   = ddff6e7b386b401ae1e471cbfe05f0bd113bb866
TREE   = a6f78d4a162650fc755e5fbe599084a5fef38237
PR     = #12 (Draft)
```

Observación de provenance del auditor:

- el paquete no contenía `.git`;
- faltaban `CLAUDE_AUDIT_REV2/00_LEER_PRIMERO.md`,
  `AUDIT_MANIFEST_REV2.json` y `EVIDENCIA_REPORTADA_NO_CONFIAR.md`;
- el auditor reconstruyó el tree con `git write-tree` y obtuvo exactamente
  `a6f78d4a162650fc755e5fbe599084a5fef38237`;
- recalculó blobs de los motores congelados y coincidieron con los esperados.

Evidencia principal:

```text
npm test       = 107/107 PASS
npm run stress = 5 seeds + repeat(1337), PASS
fuzz propio    = 14.400 ticks / ~44.000 dispatches
mutation test  = 15 mutantes reportados, 12 muertos por stress oficial
bugs bloqueantes = 0
```

Arquitectura confirmada:

- Scheduler es la única puerta;
- DECISION XOR EXECUTION;
- session activa bloquea Utility;
- crear plan no ejecuta;
- REPLAN_READY no ejecuta en el mismo dispatch;
- GOAL_REACHED / INTENT_REEVALUATION_REQUIRED no llaman Utility en el mismo dispatch;
- relationPlayer base no se reemplaza;
- behaviorState sólo cambia en nueva decisión Utility;
- world de Execution es autoritativo;
- no Pathfinder/Area/Agenda/Overrides/HTN/BT/duración dentro de este loop.

Corrección REV2 confirmada:

- plan vacío sólo cuando goal ya está satisfecho;
- si se fuerza plan vacío con goal insatisfecho mediante stub, el loop lanza error
  sin corromper estado;
- ningún motor real congelado produjo la combinación inválida en fuzz extensivo.

Deudas no bloqueantes:

1. churn `PERIODIC + DECISION_GOAL_ALREADY_SATISFIED` (~44% de dispatches en seed 1337);
2. riesgo de starvation semántica con `dutyMode` fijo y goal ya satisfecho;
3. falta test oficial con Decision Pipeline stub para el guard defensivo de plan vacío;
4. Memory congelado acepta claves extra / `__proto__` como dato sin romper ni rechazar.

El auditor considera especialmente significativo el punto 2 para una futura conexión a producción, aunque no invalida el contrato del Autonomous Loop.

Veredicto:

`NPC_AUTONOMOUS_LOOP_V01_APTO_PARA_ITERAR`

Verificación posterior desde GitHub:

```text
main current = df439ad789e668c526666fa3955deb5b2fe3e8d4
branch HEAD  = ddff6e7b386b401ae1e471cbfe05f0bd113bb866
tree         = a6f78d4a162650fc755e5fbe599084a5fef38237
PR #12       = OPEN / DRAFT / MERGEABLE / CLEAN
original base SHA = 5812deb59cd1c133383b9af973486a702a26daf4
compare vs current main = diverged (ahead 2 / behind 2), but mergeable clean
```

No se hizo merge.
