# HANDOFF — LII Monster Balance T0 → T2 Recognition

Fecha: 2026-10-07
Frente: seis monstruos repetibles / progresión adaptativa
Alcance actual: LianQi II — Sapo Ceniza + Escarabajo de Hierro
Estado: T0 CLOSED / T1 CLOSED / T2 GATE READY, RESULT PENDING

## Repositorio y rama

Repositorio:
`https://github.com/Shein25/La-Grulla-Blanca`

Rama autorizada:
`experiment/monster-adaptive-six-revalidation-v0.1`

Functional HEAD inmediatamente antes de los documentos de handoff:
`460c9d089e6d499fead76ad9b989412e8feb33b0`

Ese commit contiene:
`LII_T2_RECOGNITION_GATE_V01_PLAN_2026-10-07.md`.

Los commits de handoff son descendientes de ese HEAD.

## Guardias duras

- NO trabajar sobre `main`.
- NO merge.
- NO modificar `ROOMS.exits`.
- NO inventar NPCs, vendedores, rooms, gates, misiones o estados.
- Monster balance lab only; no runtime integration.
- Definitivas fuera de T0–T4.
- No T5.
- No root-specific monster stats/buffs.
- No nuevo reloj/timer.
- AI decide / motor resuelve.
- La decisión humana prevalece.
- No reabrir T0/T1 de LII salvo bug demostrado.
- No tocar LI: su cadena está cerrada.
- T3/T4 permanecen bloqueados hasta cerrar T2.
- Unique monsters siguen excluidos del T1–T4 persistente.

## Metodología global vigente

La etapa del jugador es una banda esperada, NO un gate duro:
`ALLOWED_NATURAL_LIMIT_BY_COMBAT_AND_DECAY`.

Pressure:
- T0 0–19
- T1 20–44
- T2 45–69
- T3 70–89
- T4 90–100

Decay floors:
- maxT0 → T0
- maxT1 → T1
- maxT2 → T1
- maxT3 → T2
- maxT4 → T3

La etapa por sí sola nunca concede tier adaptativo.

## T0 LianQi II — CONGELADO

Autoridad:
`experimentos/balance_nuevo/t0_lii/T0_LII_FREEZE_MANIFEST_2026-10-07.json`

### Sapo Ceniza

Stats:
- HP 55
- PREC 98
- EVA 11
- DEF 0
- TEN 6
- BASIC `1d2+5`

Nube de Hollín:
- cadence 3
- direct `1d2+4`
- burn `1d2+2 ×3`

HRS LII aproximado del floor aceptado:
~73.3% player-win.

Decisión humana:
el ~70% era aproximado; NO seguir microajustando.

### Escarabajo de Hierro

Stats:
- HP 75
- PREC 90
- EVA 14
- DEF 2
- TEN 24
- BASIC `1d2+3`

Carga de Caparazón:
- cadence 3
- direct `1d2+8`

HRS LII:
~70% player-win.

### Variación individual T0

Para recalibración adaptativa LII:
`ORDINARY_VARIANCE_COLLAPSED_TO_FLOOR_FOR_T1_RECALIBRATION`.

Los envelopes históricos más fuertes NO se borraron:
quedan como evidencia futura para excepcionales/mutantes.

Autoridad:
`experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/SIX_REPEATABLE_T0_VARIANCE_AUTHORITY_V01.json`

## T1 LianQi II — CONGELADO

Autoridad:
`experimentos/balance_nuevo/t1_lii/T1_LII_REACTIVE_FREEZE_2026-10-07.json`

Review final:
SHA-256
`cbf0c0e4994ed9a6cbe7a58a84981e73ae4f578d0ff073e5afd998b6c45c4867`

Represented fights:
186,880.

### Cambio semántico importante

Los primeros V01/V02 demostraron que hacer que T1 consumiera el turno del monstruo neutralizaba casi toda la ganancia defensiva.

Decisión humana:
**T1 de LII es REACTIVO y NO consume el turno del monstruo.**

NO aplicar este cambio retroactivamente a LI.

### Trigger natural T1

Activa si:
- HP <=30%, OR
- golpe recibido >=20% maxHP.

Debe además:
- cooldown <=0;
- no existir survival T1 activo.

El cooldown usa `monster_survival_cd` existente y `end_round()`.
No crear reloj nuevo.

### Sapo — T1 final

Candidate:
`3f30ec963d6b5614`

`MITIGATE_NEXT 60% / CD3`

Semántica:
- REACTIVE;
- no consume turno;
- reduce el siguiente paquete DIRECTO conectado;
- ocurre antes de DEF plana;
- persiste si el jugador falla;
- NO afecta DoT;
- se consume al conectar.

HRS:
- T0 73.28125%
- T1 63.0078125%
- delta -10.2734375 pp.

### Escarabajo — T1 final

Candidate:
`37ac83cfdd4c6973`

`DEFENSE_UP +4 / CD3`

Semántica:
- REACTIVE;
- no consume turno;
- añade DEF a la próxima acción ofensiva del jugador;
- usa pipeline normal penetración/DEF;
- se consume después de esa acción.

HRS:
- T0 69.140625%
- T1 59.609375%
- delta -9.53125 pp.

### Resultados T1 que NO son autoridad

V01:
`LII_T1_SURVIVAL_RECALIBRATION_V01_REVIEW.zip`
Quedó invalidado para freeze por usar sólo UNITARGET_FIRST + DEFENSE_OPEN.

V02:
`LII_T1_SURVIVAL_RECALIBRATION_V02_FOUR_POLICY_REVIEW.zip`
Demostró que la semántica OLD_ACTION_COST seguía neutralizando T1.

V03 reactive:
es la autoridad de evidencia usada para el freeze.

## Estado registry después de T1

`sapo_ceniza.adaptive.status = READY_FOR_T2_RECALIBRATION`

`escarabajo_hierro.adaptive.status = READY_FOR_T2_RECALIBRATION`

Registry:
`experimentos/balance_nuevo/monster_arc1_registry.json`

El registry incluye Sapo y Escarabajo en `ready_profiles`.

## T2 — PUNTO EXACTO DONDE CONTINUAR

Plan:
`experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/LII_T2_RECOGNITION_GATE_V01_PLAN_2026-10-07.md`

Artefacto preparado:
`COLAB_LII_T2_RECOGNITION_GATE_V01.zip`

SHA-256:
`0a982fbf34a6235849729069e86a127aa27b6004a38f12c3a8574b7de2e3586d`

Notebook SHA-256:
`7237acb37be3a80be628c567311301d2bcbe62c54c3791f307877d784441dc02`

Runner SHA-256:
`6dc81b2a1c1ff4dfc0eba4029f8136e0999a96b9bb5e91d302fd0685c1949457`

El usuario lo ejecutará y en la próxima conversación entregará:
`LII_T2_RECOGNITION_GATE_V01_REVIEW.zip`

NO regenerar el gate si el ZIP de resultados está íntegro.

## T2 candidate exacto

Identidad:
`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

Recognition:
- memory_window = 2;
- repeated_same_category_required = 2;
- sólo resultados `EFECTIVA`;
- categorías observables:
  - PLAYER_BASIC
  - PLAYER_UNITARGET_TECHNIQUE
  - PLAYER_AOE_TECHNIQUE
  - PLAYER_DEFENSIVE_TECHNIQUE
- no inspecciona root/build;
- no inspecciona RNG futuro.

Anticipación:
si hay reconocimiento confirmado, puede anticipar T1 si:
- HP <=40%, OR
- golpe recibido actual >=15% maxHP.

Prioridad:
1. trigger natural T1 30/20;
2. anticipación T2 40/15;
3. si cooldown/survival activo bloquea, no rearma.

Con T1 reactivo:
- anticipar T1 NO consume turno;
- no cambia 60% / +4 DEF;
- no cambia CD3;
- no crea habilidad activa nueva;
- el monstruo realiza su acción ordinaria;
- no reemplaza técnica canónica due por cadencia.

## Matriz T2 V01

2 especies
× 3 gear contexts
× 5 roots
× 4 policies
× 2 arms:
- T1_FROZEN
- T2_RECOGNITION
× R256

Total:
**61,440 combates**.

Gear:
- CARRY_OVER_FLOOR = HRS LI
- EXPECTED_STAGE = expected LII
- HIGH_ROLL_STRESS = HRS LII

## Qué revisar cuando llegue el resultado T2

Primero validar:
- manifest íntegro;
- expected 61,440 fights;
- 0 timeout;
- 0 NaN/Inf;
- `issues=[]` o explicar cualquier issue;
- arm T1_FROZEN tiene ZERO recognition/T2 leakage;
- T2 NO modifica T1 magnitude/cooldown;
- no root/build/future RNG inspection;
- no T3/T4 leakage;
- canonical technique due/turn preserved.

Luego comparar T2 vs T1 pareado:
- win-rate;
- rounds;
- HP pressure;
- monster damage direct/DOT/total;
- T1 natural activations;
- T2 anticipatory activations;
- recognition checks/triggers;
- prediction accuracy/false predictions;
- blocked recognition due cooldown/active survival;
- root spread AFTER averaging policies.

Guard diagnóstico:
- T2 no debe ser >2 pp más fácil que T1;
- HRS drop >8 pp vs T1 = revisar cliff, NO fallo automático;
- recognition/anticipation debe aparecer >0;
- no target universal de win-rate.

Si sale limpio:
1. presentar resultado y recomendación;
2. esperar ratificación humana;
3. sólo entonces congelar T2;
4. avanzar registry a `READY_FOR_T3_RECALIBRATION`;
5. preparar T3 causal.

## T3 — sólo después de congelar T2

Usar como ancla histórica, NO como autoridad numérica automática:

### Sapo
Trigger causal histórico:
`PLAYER_ATTACK_CONNECTED_WITH_T1_MITIGATION_ACTIVE`

Requiere:
- T2 recognition active;
- prediction confirmed;
- T1 active;
- offensive player action;
- interacción causal real con la mitigación.

Daño histórico:
- `INSTANCE_T0_BASIC`;
- direct damage pipeline;
- no QI drain;
- no DoT;
- no control.

### Escarabajo
Trigger causal histórico:
`PLAYER_ATTACK_CONNECTED_AND_T1_DEFENSE_PREVENTED_DAMAGE`

Mismos guards:
- T2 confirmed;
- T1 active;
- interacción causal real;
- INSTANCE_T0_BASIC;
- no QI drain / DoT / control.

No diseñar ni ejecutar T3 antes del freeze humano T2.

## T4 — sólo referencia histórica

No reabrir aún.

Sapo:
- reuse Nube de Hollín;
- historical CD12.

Escarabajo:
- reuse Carga de Caparazón;
- historical CD8.

Son anchors históricos y deben revalidarse después de T3.

## Archivos Git a leer primero en la próxima conversación

1. Este handoff.
2. `t0_lii/T0_LII_FREEZE_MANIFEST_2026-10-07.json`
3. `t1_lii/T1_LII_REACTIVE_FREEZE_2026-10-07.json`
4. `adaptive_six_revalidation_v0.1/LII_T2_RECOGNITION_GATE_V01_PLAN_2026-10-07.md`
5. `adaptive_six_revalidation_v0.1/SIX_REPEATABLE_T0_VARIANCE_AUTHORITY_V01.json`
6. `monster_arc1_registry.json`
7. El ZIP de resultados T2 que entregue el usuario.

## Regla final de continuidad

No repetir T0 ni T1.
No volver a perseguir un 70% exacto.
No reabrir OLD_ACTION_COST.
El siguiente trabajo real es **auditar el resultado T2 V01**.
