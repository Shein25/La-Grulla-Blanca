# GRULLA ULTI25 — Recuperación y creación del adapter V0.1

Fecha: 2026-10-02

Estado: **LAB / NO CANON / NO MAIN / NO MERGE / NO PUSH**

## 1. Hallazgo

Sí existía un adapter de la Grulla.

La fuente cerrada del 26/09 está en:

- rama histórica: `experiment/monster-adaptive-survival-lab-v0.1`
- commit: `4237f126a66193607f7857e5a9883b3070cc7c78`
- handoff: `HANDOFF_FINAL_GRULLA_BOSS_2026-09-26.md`

El handoff declara preparados:

- `grulla-boss-brain-v0.1.mjs`
- `grulla-boss-ability-contract-v0.1.mjs`
- `grulla-player-action-adapter-v0.1.mjs`
- `grulla-technique-gate-v0.1.mjs`
- `grulla-encounter-runtime-contract-v0.1.mjs`
- `grulla-encounter-session-v0.1.mjs`
- `grulla-ver74-special-combat-adapter-v0.1.mjs`

No se vuelve a diseñar esa capa.

## 2. Fuentes restauradas

Las siete fuentes históricas anteriores fueron copiadas **sin modificaciones** a:

`experiment/grulla-f3-pacto-ulti-bench-v0.1`

SHA de blobs históricos:

- brain: `8aaa18c2c98fd6926b5a87d717c6104cbe9657ef`
- ability contract: `44b81744d96d0b342fdb6d24a4b138d2c1529ad4`
- player action adapter: `38da41b57625016015b95d815048112a68a21542`
- technique gate: `09973493c2a10b3b39e6599d365230fb465b2a61`
- runtime contract: `34b0f879330cae48f6207b3df5b72ac206840ec4`
- encounter session: `dc2930566411fdae7d3c3c02ff184a229b7a7661`
- special combat adapter: `6d8ace4fbf61d2314376c007bae867f2d0f29286`

## 3. Adapter nuevo del benchmark

Se creó:

`experimentos/boss-bench/grulla-ulti25-bench-adapter-v0.1.mjs`

Responsabilidades nuevas y solamente nuevas:

1. componer el special-combat adapter histórico;
2. activar el Pacto del Último Vuelo al entrar en F3;
3. interceptar **daño a Vida ya resuelto** antes de comprometer el pool de fase;
4. impedir muerte F3 antes de una intención real resuelta;
5. registrar skip/overkill prevenido;
6. liberar el Pacto sólo después de una acción F3 real resuelta;
7. exponer snapshot estable para el bench.

El adapter NO:

- selecciona técnicas del jugador;
- resuelve DEF/Abs/crit;
- decide si una Ulti acierta;
- reimplementa IA;
- reimplementa memoria;
- cambia F1/F2;
- cambia el catálogo de Ultis.

## 4. Pacto importable

Se creó:

`experimentos/boss-bench/grulla-f3-pacto-ultimo-vuelo-v0.1.mjs`

API:

- `initialGrullaF3Pact`
- `activateGrullaF3Pact`
- `applyGrullaF3PactToLifeDamage`
- `releaseGrullaF3PactAfterRealAction`
- `grullaF3PactTelemetry`

## 5. Self-check

Se creó:

`experimentos/boss-bench/grulla-ulti25-bench-adapter.test.mjs`

Comprueba:

- F1 -> F2 -> F3;
- activación automática del Pacto;
- letal F3 queda en 1 HP;
- segundo packet no salta el gate;
- acción enemiga impedida no libera;
- acción real F3 sí libera;
- muerte posterior a release es legal.

Los tres archivos nuevos pasaron `node --check` localmente.

La suite ejecutable completa queda pendiente de correr en un entorno que materialice las dependencias históricas restauradas. No se declara PASS de runtime sin ejecutar esa suite.

## 6. Referencias posteriores recuperadas

También se preservaron como **referencia, no autoridad automática**:

`experimentos/boss-bench/reference-grulla-v2-final-boss-lab/`

- `grulla_v2_final_boss_lab.py`
- `grulla_v2_lab_config.json`
- `README_GRULLA_V2_FINAL_BOSS_LAB.md`
- `fire_ultimates_integral_colab_v2.py`

El benchmark integral de Fuego demuestra que ya se había conectado directamente el loop de Grulla usando:

- `choose_boss_intent`
- `pre_player_intent`
- `post_player_intent`
- `enter_phase`

## 7. Authority sync pendiente

Hay tres capas históricas que no deben mezclarse silenciosamente:

### A. Contrato cerrado 26/09
- HP 150 / 100 / 50
- DEF 13 / 13 / 13
- F1 programada
- F2 CHAIN_A
- F3 M_A

### B. Grulla v2 LAB 30/09
Estado explícito: LAB / PROVISIONAL.

- HP 150 / 100 / 50
- DEF 12 / 16 / 20
- F3 Abs 36, cap 12
- bonus crítico recibido reducido 50%
- otras capas de mitigación/evasión/reflejo

### C. B20 UI posterior
El prototipo UI recuperado contiene:

- F1/F2 DEF 13
- F3 DEF 15
- F3 ward/Abs 25
- bonus crítico F3 reducido al 50%

Por seguridad, el adapter V0.1 exporta:

`GRULLA_ULTI25_NUMERIC_AUTHORITY_STATUS='AUTHORITY_SYNC_REQUIRED_BEFORE_MASS_BENCH'`

El cableado/IA puede seguir avanzando, pero el mass benchmark no debe ejecutarse hasta fijar cuál de estas capas numéricas representa la Grulla actual.

## 8. Próximo paso técnico

1. ejecutar el self-check completo del adapter;
2. crear un `profile overlay` separado para la autoridad numérica actual;
3. conectar el adapter al runner pareado del bench;
4. conectar el adapter de Ultis ya validado;
5. smoke 25x4x4x20 antes de Pilot.
