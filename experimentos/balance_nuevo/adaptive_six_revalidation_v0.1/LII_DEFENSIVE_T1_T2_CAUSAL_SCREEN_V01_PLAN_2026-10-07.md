# LianQi II — Defensivas × T1/T2 — Causal Screen V01

Fecha: 2026-10-07.
Estado: PLAN / NO BALANCE FREEZE.
Rama: experiment/monster-adaptive-six-revalidation-v0.1.

## Autoridad previa
- PRE-FLIGHT LI I: `LII_STAGE_REAL_PREFLIGHT_V01_REVIEW_2026-10-07.md`.
- BRIDGE: `LII_T1_T2_ADAPTIVE_BRIDGE_CONTRACT_GATE_V01_REVIEW_2026-10-07.md` (PASS_BRIDGE_ONLY; 30.720 fights, 10 tests de evento).
- T0, T1, T2 LII human-ratified. No recalibrarlos.
- Cinco BASE ofensivas y cinco defensivas de la etapa real; Tramo I con dos puntos.

## Objetivo

Distinguir tres efectos:
1. Decisión de **usar defensiva** o no (consume turno + Qi).
2. Elección de **momento**: apertura fija versus antes de amenaza.
3. Efecto incremental de **una especialización de Tramo I** en ofensiva o defensiva.

Los brazos comparten equipamiento, monstruo, estado inicial y semilla: CRN (common random numbers). La elección de política altera la secuencia de acciones y, potencialmente, el flujo aleatorio posterior; las diferencias de win/HP son **efectos netos de política**, no el efecto mecánico instantáneo de una defensa. No afirmar paridad de acción/RNG después de una decisión diferente.

## Matriz

- 5 raíces × 16 builds monorraíz legales de 0–2 puntos = 80.
- 4 equipos: MANDATORY_ENTRY, CARRY_OVER_LI_HIGH, EXPECTED_STAGE, HIGH_ROLL_STRESS.
- 2 monstruos nativos READY: sapo_ceniza (NORMAL), escarabajo_hierro (TANK).
- 2 tiers de adaptación: T1 y T2 (T0 ya fue validado como control en Bridge).
- 4 políticas:
  - OFFENSE_ONLY (sin defensiva);
  - DEFENSE_OPEN (una defensiva en la primera ronda);
  - DEFENSE_DUE (defensiva antes de siguiente técnica canónica, si hay Qi y queda recorrido de combate);
  - DEFENSE_GUARD (defensiva cuando ronda due o HP bajo, máximo 2 activaciones, con reserva mínima de Qi para ofensiva).

- R32 por contexto/política; semillas pareadas entre los cuatro brazos y las builds comparables.
- 1.280 contextos base × 4 políticas × 32 = **163.840 combates**.

## Métricas y salidas

- Victoria, HP% restante, Qi restante y gastado, rondas, defensa usada/procs, daño prevenido, control, daño recibido, triggers T1/T2, due y due_missed.
- Exportar RAW_SEED_RESULTS.csv.gz (permite reprocesar causalidad por semilla sin reejecutar).
- POLICY_PAIR_CONTEXTS.csv.gz: OFFENSE_ONLY vs cada estrategia defensiva, contrastes pareados R32.
- TRAMO_I_PAIRED_COMPARISONS.csv.gz: branch defensivo comparado con BUILD base de igual ofensiva; branch ofensivo comparado con base correspondiente.
- POLICY_SUMMARY.csv y FOCUS_WARNINGS.csv con contextos potenciales (sin juicio definitivo).
- SOURCE_LOCK, EVENT_PARITY_TESTS, MANIFEST/QA, hash de checkpoints y REVIEW ZIP.

## Screening y escalación

Pantalla R32 sólo detecta hipótesis. No implica nerf/buff, ni automatic freeze.

Priorizar escalación a R256 en V02 para:
- pérdidas defensivas de Fuego/Viento persistentes;
- regresiones fuertes de Tramo I defensivo frente a su mismo contexto/base;
- signos inversos por gear y monster;
- gasto desproporcionado de Qi sin beneficio de supervivencia;
- cualquier no-paridad funcional (bloqueo duro inmediato).

Agrupación jerárquica (raíz, monstruo, gear, política y T1/T2) antes de escalar, para evitar miles de contextos a R256.

## Guardrails
- Sólo laboratorio, fuente fijada a commit y SHA-256.
- No `main`, no merge/push; no runtime HTML, Astra recibirá cierre.
- No modificar LI ni T0/T1/T2 LII.
- 2 workers, checkpoints reanudables con firma de corrida, IntProgress persistente, RUN/CP/DONE/ERR.
- Este espacio es sólo monorraíz, NO cierre multielemental ni Concordancias LII.
