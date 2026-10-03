# HANDOFF — Grulla 25/25 · Ultis + equipo LIV · Smoke inicial

Fecha: 2026-10-02

## Objetivo inmediato

Preparar y ejecutar el **primer benchmark de las 25 Ultis contra la Grulla completa F1→F2→F3 usando equipo LIV aprobado**, sin técnicas normales y sin consumibles en el resultado principal.

Este frente busca observar cómo se comportan las Ultis dentro de una pelea larga y realista, no recalibrarlas automáticamente.

## Repositorio y guardias

Repositorio oficial:

`Shein25/La-Grulla-Blanca`

Rama de trabajo obligatoria:

`experiment/grulla-f3-pacto-ulti-bench-v0.1`

HEAD al emitir este handoff:

`2795988d649d19804909b9315a6591f1cc1da8a0`

Guardias:

- NO tocar `main`.
- NO merge.
- NO push a ramas distintas sin autorización.
- NO modificar motor global para hacer encajar una Ulti.
- NO reabrir balance de monstruos/NPC/comercio/A07.
- NO inventar técnicas, equipo, stats, fases ni hooks.
- Decisiones humanas prevalecen.
- Resultado de benchmark = LAB, nunca canon automático.

## Autoridad de Ultis

Usar la autoridad cerrada del frente ULTI25 ya validado.

Rama:

`experiment/ulti25-retest-v0.1`

La implementación debe conservar:

- 25 Ultis;
- una activación por combate;
- CD 40 sólo fuera de combate;
- AOE Ulti a magnitud completa;
- daño DIRECT_DAMAGE de Ulti puede crit por defecto;
- secundarios/DOT/Hemorragia no crit salvo regla explícita;
- duraciones expresas;
- correcciones del retest focal ya auditadas;
- corrección de signo de TEN de Trono.

No reutilizar una versión previa al retest si contradice esta autoridad.

## Autoridad de Grulla

En la rama del bench ya están restaurados los contratos históricos cerrados:

- `grulla-boss-brain-v0.1.mjs`
- `grulla-boss-ability-contract-v0.1.mjs`
- `grulla-player-action-adapter-v0.1.mjs`
- `grulla-technique-gate-v0.1.mjs`
- `grulla-encounter-runtime-contract-v0.1.mjs`
- `grulla-encounter-session-v0.1.mjs`
- `grulla-ver74-special-combat-adapter-v0.1.mjs`

Fuente histórica:

`4237f126a66193607f7857e5a9883b3070cc7c78`

El wrapper nuevo del bench es:

`experimentos/boss-bench/grulla-ulti25-bench-adapter-v0.1.mjs`

El Pacto F3 es:

`experimentos/boss-bench/grulla-f3-pacto-ultimo-vuelo-v0.1.mjs`

## Pacto del Último Vuelo — regla obligatoria F3

Al entrar en F3:

- el Pacto queda activo;
- cualquier daño letal deja a la Grulla en 1 HP;
- golpes posteriores de la misma acción tampoco pueden matarla;
- debe conservarse el daño/overkill prevenido como telemetría;
- un intento de acción F3 impedido por Control NO libera el Pacto;
- sólo se libera tras la primera intención real F3 efectivamente resuelta;
- luego puede morir normalmente.

Invariante duro:

`F3_KILL_BEFORE_FIRST_REAL_ACTION == 0`

Registrar:

- `f3_skip_attempted`
- `f3_lethal_preventions`
- `f3_prevented_lethal_damage`
- `f3_max_single_overkill_prevented`
- `f3_skip_source`
- `f3_first_real_action_resolved`
- `player_actions_after_gate_release_to_kill`

## Equipo — sí entra en este benchmark

Etapa del encuentro:

`LianQi_IV`

Fuente:

`experimentos/balance_nuevo/equipment_arc1_catalog.json`

Blob esperado:

`f3ba217b834eb0c2bb4156b12d4f7e8b9990263f`

Overlay de aprobación:

`experimentos/boss-bench/EQUIPMENT_BENCH_AUTHORITY_OVERLAY_2026-10-02.json`

Adapter:

`experimentos/boss-bench/equipment_bench_adapter_v01.py`

Perfiles principales:

1. `MANDATORY_ENTRY`
2. `EXPECTED_STAGE` — perfil principal por defecto
3. `HIGH_ROLL_STRESS`

Control diagnóstico:

`NAKED`

Baseline y rama con Ulti deben llevar exactamente el mismo perfil y piezas.

## Técnicas — fuera de este primer frente

Para este Smoke:

`NORMAL_TECHNIQUES_ENABLED = false`

No usar técnicas normales, ramas, buffs/debuffs ni preparación construida mediante técnicas todavía no cerradas.

## Consumibles — fuera del resultado principal

Los contratos actualizados ya están recuperados:

- `ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json`
- `ALCHEMY_QI_RECOVERY_CONTRACT_V0_2.json`

Ambos tienen números ratificados, pero **no usar pociones en el headline del primer Smoke**.

Usar:

`CONSUMABLE_ARM = NONE`

## Diseño

Ventanas:
- `F1_EARLY`
- `F2_ENTRY`
- `F3_ENTRY`
- `PREPARED_OPPORTUNITY`

Estados:
- `FULL`
- `BALANCED`
- `DISADVANTAGE`
- `NEAR_DEATH`

Equipo:
- `MANDATORY_ENTRY`
- `EXPECTED_STAGE`
- `HIGH_ROLL_STRESS`

Smoke:
`25 × 4 × 4 × 3 × 20 = 24.000` peleas con Ulti + 240 baselines.

## Pairing

Cada rama con Ulti debe compartir con su baseline:
- seed;
- estado inicial;
- equipo;
- piezas;
- stats derivados;
- IA;
- RNG previo a divergencia;
- política neutral.

La única diferencia causal debe ser la Ulti.

## Self-checks duros

1. F1→F2→F3.
2. Pacto se activa F3.
3. letal F3 queda en 1 HP.
4. multi-hit no salta Pacto.
5. acción impedida no libera.
6. primera intención real libera.
7. muerte post-release funciona.
8. 25 Ultis correctas.
9. 3 perfiles LIV sin piezas faltantes.
10. técnicas OFF.
11. consumibles NONE.
12. pairing seed/equipo válido.
13. cero fallback sintético silencioso.

## Entregable pedido al agente

Primero devolver:

`KAGGLE_GRULLA_ULTI25_EQUIPMENT_SMOKE.ipynb`

Debe descargar desde Git/commits explícitos, verificar autoridad, correr self-check y ejecutar sólo el Smoke.

ZIP esperado:

`GRULLA_ULTI25_EQUIPMENT_SMOKE_RESULTS_FOR_CHATGPT.zip`

Contenido mínimo:
- run_manifest.json
- self_check.json
- scenario_manifest.json
- baseline_summary.csv
- ulti_summary.csv
- paired_delta_summary.csv
- phase_metrics.csv
- f3_skip_pressure.csv
- equipment_profile_comparison.csv
- issues.json
- hashes/copia de adapters y runners usados

No hacer Pilot ni Mass todavía.

## Authority sync de Grulla

Antes de ejecutar, si la autoridad numérica actual del jefe no puede fijarse sin mezclar versiones, abortar con:

`GRULLA_NUMERIC_AUTHORITY_SYNC_REQUIRED`

y devolver exactamente los campos en conflicto. No inventar DEF/Abs/mitigación.
