# HANDOFF MAESTRO — NPC + MONSTRUOS — 2026-09-25

## Regla de seguridad

- NO tocar `main` sin orden explícita.
- NO mergear PR #17 ni PR #18 por iniciativa propia.
- NO repetir baselines NPC ya cerrados.
- NO repetir Monster Combat AI ni reconstruir el laboratorio canónico de monstruos.
- Antes de escribir, inspeccionar HEAD/PR/README/matriz/resultados de la rama correspondiente.
- Mantener CANON separado de políticas, traits y perfiles experimentales.

## Repo

`Shein25/La-Grulla-Blanca`

Main verificado en esta etapa:

`de3a7593dc59120f5940b3589bc42ed6e500ba9b`

---

# NPC — ESTADO CERRADO DE BASELINES

## Rama de trabajo

`experiment/npc-canonical-behavior-lab-v0.1`

HEAD al handoff:

`adc086ba5aca8d2a98c63f2df742ac019a498fea`

PR:

`#17 — experiment: canonical NPC behavior lab v0.1 — 32/32 baselines complete`

Estado:

- OPEN
- DRAFT
- NO MERGED
- 108 archivos cambiados
- 154 commits

Snapshot de handoff:

`snapshot/handoff-2026-09-25-npc-complete`

Snapshot previo de cobertura completa:

`snapshot/npc-canonical-behavior-lab-v0.1-32-baselines`

## Resultado NPC

Los 32 NPC canónicos de `NPC_DEF` ver74 tienen baseline reproducible.

```text
Autoridades    88/88
Intermedios    74/74
Funcionales    89/89
Compañeros     85/85
TOTAL         336/336 PASS
```

Suite canónica transversal:

```text
15/15 PASS
32/32 NPC cubiertos
```

Archivo clave:

`experimentos/npc/canonical-behavior-lab-v0.1/MATRIZ_NPC_ARQUITECTURAS_v0.1.md`

## Matriz de baselines ya probados

- Ji Xueying — FSM mínima/eventos.
- Qiao Ren — Autonomous Loop (Utility+GOAP+Execution).
- Wei Jian — Behavior Tree.
- Song Rui — Utility+GOAP+diálogo.
- Lan Meihua — Utility+GOAP.
- Duan Shibo — Utility+GOAP.
- He Zhen — Utility+GOAP+diálogo.
- Shen Baojun — FSM mínima/eventos.
- Madre Wen — FSM mínima/eventos.
- Tao Ming — FSM.
- Jiang Rui — FSM + BT + Utility.
- Su Lian — Behavior Tree.
- Chen Bo — Behavior Tree.
- Yao Fen — Behavior Tree.
- Gao Shun — FSM + Behavior Tree.
- Feng Zhi — FSM mínima/eventos.
- Ma Qiren — Behavior Tree.
- Pei Luo — FSM + Behavior Tree.
- Lu Cheng — FSM anclada.
- Ning Cai — FSM anclada.
- Wen Tao — Behavior Tree.
- Yu Shun — FSM mínima/eventos.
- Ma Gu — FSM.
- Ren Bo — Behavior Tree.
- Xu An — Behavior Tree.
- Mei Shufen — FSM con guardia narrativa.
- Lin Yue — Memory→Relations→Utility→GOAP.
- Han Qiao — Utility+GOAP.
- Zhao Wen — diálogo Utility.
- Mei Lian — Utility+GOAP.
- Guo Chen — Utility+GOAP + guardia irreversible.
- Luo Yan — diálogo Utility.

## Gaps NPC antes de producción

1. `KNOWLEDGE_SCHEMA_R1_TO_R10`.
2. Navegación física real por rooms/rutas/gates.
3. Executor de combate/seguridad para intents marciales.
4. `RESOURCE_ALLOCATION_AND_LOGISTICS`.
5. `ARCHIVE_PROTECTION_AND_CATALOG_STATE`.
6. `MEDICAL_TRIAGE_AND_TREATMENT_STATE`.
7. `FORMATION_NETWORK_STATE_AND_REPAIR`.
8. Asignación de frentes M16 y responsables.
9. Permisos institucionales (`ARCHIVO_RESTRINGIDO_PERMISSION`, `NUCLEO_PROFUNDO`).
10. Guardias de decisiones irreversibles para que `FULFILL_DUTY` no absorba decisiones narrativas.
11. Acciones sociales Utility no mapeadas a GOAP, p.ej. `hablar_jugador`.
12. Estado de mundo de dominio para consecuencias reales.

## Motores auditados/congelados relevantes

- Reactive Routine FSM REV2:
  `snapshot/npc-reactive-routine-fsm-v0.1-rev2-audited`
- Behavior Tree REV2:
  `snapshot/npc-behavior-tree-v0.1-rev2-audited`
- Utility AI v0.1.1 auditada.
- GOAP v0.2.2 auditado.
- Memory / Relations / Decision.
- Scheduler.
- Execution/Replanning.
- Autonomous NPC Loop v0.1 REV2.

No crear más motores antes de una necesidad concreta.

---

# MONSTRUOS — ESTADO ACTUAL

## Monster Combat AI

Experimento base ya auditado/cerrado.

Rama histórica:

`experiment/monster-combat-ai-v0.1`

PR #13 ya fue mergeado previamente.

NO repetir este experimento.

## Laboratorio canónico actual

Rama:

`experiment/monster-canonical-behavior-lab-v0.1`

HEAD al handoff:

`289a090b83f2e0f3652c93c870f88ec2c4256bc4`

PR:

`#18 — experiment: monster canonical behavior lab v0.1 — closed feedback loop`

Estado:

- OPEN
- DRAFT
- NO MERGED

Snapshot de handoff:

`snapshot/handoff-2026-09-25-monsters-complete`

## Canon monstruos

Fuente:

- `grulla-blanca_ver74.html`
- blob `d34f7ea3f9de9344130aa072fac34d14a7a474d6`

Snapshot:

`experimentos/monstruos/monster-canonical-behavior-lab-v0.1/canonical/MOBS_ver74.snapshot.json`

Catálogo:

- 19 MOBS totales.
- 18 criaturas combatientes.
- `muneco_practica` fuera de IA.

## Cadencia canónica

Debe preservarse:

```js
round % tecnica.cada === 0
```

`CADENCE_COMPAT` es autoritativo para compatibilidad productiva.

`DECISION_EXPERIMENTAL` es sólo laboratorio.

## Cobertura monstruos ya hecha

```text
canon transversal         13/13
baseline representativo   18/18
18 combatientes           15/15
tactical overlay          14/14
intent bridge             11/11
semantic memory           12/12
resolved signal adapter   13/13
feedback loop             11/11
TOTAL                    107/107 PASS
```

## Arquitecturas/perfiles experimentales ya explorados

Matriz candidata de 18 combatientes:

```text
INSTINTIVO  4
REACTIVO_1  5
CAZADOR_2   5
TACTICO_3   3
MASTER_4    1
TOTAL      18
```

Estas asignaciones NO son canon.

## Benchmark monstruos ya hecho

- 18 combatientes × 1.000 escenarios = 18.000 decisiones primarias.
- 0 violaciones de cadencia.
- 0 selecciones inválidas.
- guardian_coral: memoria cambia ~11,29% en 10.000.
- lobo_espiritual: social cambia ~11,50% en 10.000.
- mono_pildoras: combinado cambia ~20,47% en 10.000.

## Integración ya construida

### Canonical Intent Bridge v0.1

Traduce la decisión a:

```text
BASIC_ATTACK
TECHNIQUE
```

preservando payload canónico y bloqueando técnica fuera de cadencia.

### Semantic Memory Recorder v0.1

```text
resolved outcome
→ memoria semántica
→ Monster Combat AI
```

### Resolved Combat Signal Adapter v0.1

Compatibilidad confirmada:

```text
ver74 absorberGolpe()
→ r.absorbido
→ PLAYER_ABSORPTION_RESOLVED
→ Semantic Memory Recorder
```

Recuperación:

- contrato preparado;
- `beber()` todavía no expone deltas estructurados;
- NO parsear logs;
- NO inferir desde HP.

### Combat Feedback Loop v0.1

Cadena cerrada:

```text
AI
→ intent bridge
→ resolved signal
→ semantic memory
→ AI
```

Caso guardian_coral:

```text
sin memoria → technique
3 absorciones efectivas
→ DEFENSA_ABSORCION
→ technique recibe -24
→ basic
```

En `CADENCE_COMPAT`, la técnica canónica sigue siendo obligatoria en su ronda.

## Próximos huecos reales de monstruos

NO volver a inspeccionar/reconstruir lo anterior salvo verificación rápida.

Continuar desde:

1. hook productivo mínimo para absorción, primero sobre copia/branch de integración, no main;
2. instrumentación estructurada de recuperación en `beber()`;
3. pruebas de integración sobre una COPIA de ver74;
4. luego decidir integración NPC↔monstruo fuera de producción:
   - NPC puede entrar a room con combate ya iniciado;
   - monstruo y NPC pueden estar enfrentándose;
   - NPC puede pedir ayuda al jugador;
   - jugador puede incorporarse al combate;
   - mantener Monster AI separado del cerebro general NPC.

---

# IDEA ARCO 2 YA REGISTRADA

Situaciones emergentes deseadas:

```text
jugador entra en room
→ NPC ya combate con monstruo
→ NPC pide ayuda
→ jugador puede incorporarse
```

Astra podrá eventualmente integrar NPC/monstruos con Arco 1 auditado y crear situaciones una vez determinada la IA de cada NPC.

No implementar esto en producción todavía.

---

# ORDEN RECOMENDADO AL RETOMAR

1. Inspeccionar PR #17 y PR #18; no asumir estado desde memoria.
2. Confirmar que los snapshots de handoff siguen apuntando al estado esperado.
3. NO repetir pruebas NPC: 32/32 ya cubiertos.
4. NO repetir Monster Combat AI ni canonical monster lab: feedback loop 107/107 ya cerrado.
5. Continuar desde el siguiente gap real de monstruos:
   - hooks estructurados sobre copia de ver74,
   - especialmente absorción y recuperación.
6. Mantener PRs draft y main intacto.
7. Tras cerrar monstruos, diseñar laboratorio NPC↔monstruos/combate conjunto, todavía aislado.

