# HANDOFF — ULTIS / GRULLA CONTINUOUS FULL SPECTRUM V03 → V03.1

**Fecha local:** 2026-10-04  
**Proyecto:** La Grulla Blanca  
**Repo:** `Shein25/La-Grulla-Blanca`  
**Frente exclusivo:** 25 Ultis vs Grulla. Las técnicas normales las trabaja otro agente.  
**Reglas:** NO `main`, NO merge, NO rediseñar técnicas, NO auto-canon. AI decide sólo dentro del LAB; motor resuelve.  
**Estado:** `PATCH_REQUIRED_BEFORE_STANDARD`.

## 1. Artefactos sellados

- V05 completo aceptado: SHA-256 `3372ee2172253eaf7f410616693960bf6ad8da5510f1ad611d5506631ea648f5`.
- V03 paquete runner: `GRULLA_ULTI25_CONTINUOUS_FULL_SPECTRUM_V03.zip`
  - SHA-256 `df3b3077b75f0b9f78a2b4b4e709dcc8a3b7c91e3d3018230f1f8a29f2d6efbb`.
- V03 notebook Kaggle:
  - SHA-256 `14f36c3ef2835d6c4f4ba42044aa995476c7d5418221f5ae0a824450ecd8a225`.
- QUICK Kaggle recibido: `CONTINUOUS_FULL_SPECTRUM_V03.zip`
  - SHA-256 `3f0e125e5c92563da0ad08971e53581310f0a30f22985553285bd753288053f5`.
- Runner V03:
  - SHA-256 `07a23faa70b804b8b4be9789ca6c74af199a7907b23758cd68d702b66dc1afa0`.
- Autoridad numérica de bench:
  - SHA-256 `0264794e6f2eca67dff23a3d04e5339bbe23df06c90558d294073a0f8727af3a`.
  - Estado: `HUMAN_BENCH_AUTHORITY_NOT_GLOBAL_CANON`.

No modificar V05. V03 se conserva como evidencia histórica; las correcciones deben salir como **V03.1**.

## 2. Qué ejecutó QUICK

- Casos: **28.046**.
- Parejas CORE Ulti/baseline: **12.160**.
- `hard_issue_count` bruto: **504**.
- El `FAIL` bruto NO significa 504 bugs de Ultis.

Conteo bruto:
- `ooc_not_ready_at_40`: **200**.
- `reactivation_probe_missing`: **200**.
- `second_activation_not_blocked`: **100**.
- `pact_released_by_denied_intent`: **4**.

## 3. Auditoría del FAIL bruto

### 3.1 Checker de cooldown — 500 falsos positivos

Las reglas genéricas del checker V03 se aplican a casos `ACTIVATION_COOLDOWN` que no tienen por qué emitir todas las sondas.

El contrato específico sí mostró:
- segunda activación en el mismo combate: bloqueada;
- OOC 39: todavía no ready;
- OOC 40: ready.

**Parche V03.1:** en `run_full_spectrum_v03.py`, evaluar por `suite` + `activation_edge`.

- `FIRST_USE`: verificar primera activación legal; NO exigir reactivation probe ni OOC40.
- `SECOND_USE_SAME_COMBAT`: exigir segundo intento bloqueado.
- `OOC_39`: exigir `cooldown_ready == false`.
- `OOC_40` y `OOC_41`: exigir `cooldown_ready == true`.
- En CORE continuo sólo exigir reactivación/OOC si el runner realmente ejecutó esa sonda de contrato.

### 3.2 Pacto — 4 falsos positivos de telemetría

Casos:
- 2 × `EARTH_TRONO_VOLCAN_SEPULTADO`.
- 2 × `WIND_DESIERTO_MIL_DUNAS`.

La primera acción F3 negada sí dejó el Pacto activo. El campo `pact_active_after_denied` se sobrescribe si después ocurre otra negación cuando el Pacto ya fue liberado legítimamente.

**Parche V03.1:** registrar una observación inmutable de la **primera** negación:
- `f3_first_denied_observed`;
- `pact_active_after_first_denied`;
- no sobrescribirla después.
Mantener contador separado si se desean negaciones posteriores.

## 4. Invariantes mecánicos que salieron bien

En toda la corrida QUICK:

- **0** errores de simulación.
- **0** truncamientos.
- **0** muertes de la Grulla antes de la primera intención real F3.
- máximo de liberaciones del Pacto: **1**.
- **0** casos con Pacto activo después de primera intención real F3 resuelta.
- **712** casos donde el death-gate intervino.
- **730** prevenciones letales acumuladas.
- máximo daño letal evitado en una simulación: **253**.
- **0** `duration_violation`.
- **0** `aoe_scalar_violation`.

No apareció un bug mecánico generalizado de las 25 Ultis.

## 5. BUG REAL DEL RUNNER — Río Celeste sin Orillas

En `grulla_continuous_ulti_runner_v01.py` V03, el intento de Ulti se envía a `brain.observe(...)` **antes** de conocer `activated`.

Eso contamina la memoria de la Grulla aunque Río sea rechazado.

Diagnóstico CORE de Río:
- 320 casos.
- 0 activaciones.
- 211 `IMPLEMENTATION_REJECTED`.
- 109 `NOT_ATTEMPTED`.

Entre los 211 rechazados:
- **47** pares con HP final del jugador distinto al baseline.
- **36** con Qi distinto.
- **3** con outcome distinto.
- **3** con HP final de Grulla distinto.
- **12** con rondas distintas.

Entre los 109 `NOT_ATTEMPTED`:
- **0 diferencias** en outcome/HP/Qi/boss HP/rondas.

**Parche V03.1 obligatorio:**
1. resolver intento de Río;
2. sólo si `activated == true`, registrar la acción de Ulti en la memoria de la Grulla;
3. si el intento es rechazado, no mutar brain/history/phase memory/RNG causal del tratamiento;
4. añadir oracle fuerte: para una activación rechazada sin otro cambio, tratamiento y baseline deben ser bit-equivalentes en outcome, HP/Qi, boss HP, rondas y traza pre-divergencia.

Río no debe usarse para conclusiones generales de potencia hasta definir correctamente el concepto de “técnica normal actualmente utilizable” mientras las técnicas normales están OFF.

## 6. Huecos de cobertura reales

Activaciones CORE por ventana:

- `F1_EARLY`: 1080/1216.
- `F1_LATE_PRE_TRANSITION`: **119/1216**.
- `F2_ENTRY`: 1029/1216.
- `F2_ADAPTIVE_MID`: 842/1216.
- `F2_LATE_PRE_TRANSITION`: **0/1216**.
- `F3_ENTRY_PACT_ACTIVE`: 673/1216.
- `F3_PRE_RELEASE`: 674/1216.
- `F3_CONTROL_DENIED_FIRST_INTENT`: 940/1216.
- `F3_POST_RELEASE`: 876/1216.
- `PREPARED_OPPORTUNITY`: 953/1216.

Causa: el fixture fuerza transición después de cuatro acciones de Grulla. `F2_LATE_PRE_TRANSITION` espera `boss_actions >= 4`, pero tras la cuarta acción ya se cambia de fase y nunca existe la oportunidad de jugador.

**Parche V03.1:**
- introducir estado `phase_transition_pending`;
- después de alcanzar el umbral de avance mecánico, ofrecer exactamente **una acción de jugador de late-window** antes de cambiar de fase;
- luego resolver transición si la fase sigue viva;
- no transferir overkill ni inventar daño;
- misma política baseline/Ulti.
- F1 late debe quedar también materialmente cubierto, no 9.8%.

## 7. Suite PHASE_TRANSITION todavía nominal

- Casos declarados: **418**.
- Activaron Ulti: **24**, todos Fuego.
- `transition_edge` se genera pero el runner V03 **no lo consume**.

Por tanto todavía NO se probaron realmente como casos distintos:
- exact lethal;
- overkill;
- multi-hit cruzando fase;
- DOT cruzando fase;
- Hemorragia cruzando fase;
- Control en transición;
- persistencia de buff/debuff;
- Absorción persistente cuando contrato lo permita;
- proc de equipo antes/en borde.

**Parche V03.1:** cada `transition_edge` debe activar una ruta de setup y un oracle concretos. Si una Ulti no puede producir naturalmente ese edge, usar fixture mínimo de stress claramente etiquetado, nunca fingir que la Ulti lo produjo.

Obligatorio:
- F1/F2 exact lethal crea siguiente pool completo;
- overkill NO se transfiere;
- multi-hit no daña siguiente pool salvo que el contrato de acción lo autorice explícitamente;
- DOT/Hemorragia persistentes se prueban según contrato;
- efectos no persistentes deben expirar;
- estado del jugador sí permanece;
- Pacto aparece sólo al entrar F3.

## 8. Señales preliminares de potencia — NO CANON

Sólo sirven para priorizar.

### Sentencia del Filo Celestial
En 198 pares CORE activados:
- daño medio Ulti ≈ **38.78**;
- Δ HP final Grulla ≈ **-11.97**;
- uplift mecánico victoria ≈ **+7.58 pp**.

En `F3_POST_RELEASE`:
- n = **21**;
- uplift ≈ **+28.57 pp**;
- tratamiento 28.57% vs baseline 0% en esa muestra.

Es la segunda batería distinta donde Sentencia sobresale. Marcar `BALANCE_PRIORITY`, no nerfear todavía.

### Otras señales QUICK
- Renacer del Sol Carmesí ≈ **+6.06 pp**.
- Corazón ≈ **+1.53 pp**.
- Brasa ≈ **-6.59 pp**.
- Loto ≈ **-3.48 pp**.
- Aguja ≈ **-1.51 pp**.

Las negativas NO justifican buff: late windows/transitions siguen incompletos.

Defensivas/utilitarias deben evaluarse también por HP/Qi/acciones/control, no sólo victoria.

## 9. Estado de autoridad / metodología

- Técnicas normales: OFF, las trabaja otro agente.
- Consumibles: OFF en headline.
- V03 usa `MECHANICAL_PHASE_ADVANCE_FIXTURE`, por lo que `balance_authoritative=false`.
- V03 sirve para bugs, continuidad y señales preliminares.
- No declarar balance integral hasta reemplazar avance mecánico por build/técnicas humanas aprobadas.
- No tocar `main`.
- No merge.
- No reabrir V05.
- No ejecutar `standard` V03.

## 10. Próximo entregable exacto: V03.1

Crear:
- `grulla_continuous_ulti_runner_v031.py`
- `run_full_spectrum_v031.py`
- `generate_full_spectrum_cases_v031.py` si hace falta para edges explícitos
- `ULTI25_FULL_SPECTRUM_ORACLES_V031.json`
- notebook `KAGGLE_GRULLA_ULTI25_CONTINUOUS_FULL_SPECTRUM_V031.ipynb`
- paquete `GRULLA_ULTI25_CONTINUOUS_FULL_SPECTRUM_V031.zip`

Antes de Kaggle:
1. self-check;
2. smoke de los 38 modos × F1/F2/F3;
3. test específico rejected Río == baseline;
4. test late F1/F2 alcanzable;
5. test de cada `transition_edge`;
6. test Pacto primera negación;
7. test cooldown por edge;
8. 0 hard issues locales.

Luego correr **QUICK V03.1**. Sólo si queda limpio, pasar a `standard`.

## 11. Referencia Git previa

Rama histórica de este frente:
`experiment/grulla-f3-pacto-ulti-bench-v0.1`

HEAD observado antes del backup:
`d01413a1eb748b6efbcc07c6155e8102737c42e8`.

El backup/handoff debe vivir en una rama nueva; no tocar `main`.
