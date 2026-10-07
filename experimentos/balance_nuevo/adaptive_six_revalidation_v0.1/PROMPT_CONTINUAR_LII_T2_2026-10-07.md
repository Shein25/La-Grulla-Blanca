# PROMPT PARA CONTINUAR — LII T2 Recognition

Quiero continuar exactamente el frente de balance adaptativo de monstruos repetibles de LianQi II del proyecto **La Grulla Blanca**.

Repositorio:
https://github.com/Shein25/La-Grulla-Blanca

Rama obligatoria:
`experiment/monster-adaptive-six-revalidation-v0.1`

NO trabajar sobre main.
NO merge.
NO modificar ROOMS.exits.
NO inventar NPCs/rooms/gates/misiones/estados.
No T5.
No Definitivas en este frente.
No root-specific monster stats.
No nuevo reloj/timer.
No tocar LI.
No reabrir T0/T1 de LII salvo bug demostrado.
T3/T4 bloqueados hasta cerrar T2.

Antes de analizar nada, leer en Git, en este orden:

1. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/HANDOFF_LII_T0_T1_TO_T2_2026-10-07.md`
2. `experimentos/balance_nuevo/t0_lii/T0_LII_FREEZE_MANIFEST_2026-10-07.json`
3. `experimentos/balance_nuevo/t1_lii/T1_LII_REACTIVE_FREEZE_2026-10-07.json`
4. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/LII_T2_RECOGNITION_GATE_V01_PLAN_2026-10-07.md`
5. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/SIX_REPEATABLE_T0_VARIANCE_AUTHORITY_V01.json`
6. `experimentos/balance_nuevo/monster_arc1_registry.json`

Estado congelado:

T0 Sapo:
HP55 / PRE98 / EVA11 / DEF0 / TEN6
BASIC 1d2+5
Nube de Hollín: CD3, direct 1d2+4, burn 1d2+2 x3.

T0 Escarabajo:
HP75 / PRE90 / EVA14 / DEF2 / TEN24
BASIC 1d2+3
Carga de Caparazón: CD3, direct 1d2+8.

T1 Sapo:
`MITIGATE_NEXT 60% / CD3`
REACTIVE.
NO consume turno.
Trigger natural: HP<=30% OR hit recibido>=20% maxHP.
Mitiga sólo el siguiente paquete DIRECTO conectado; persiste por miss; no afecta DoT.

T1 Escarabajo:
`DEFENSE_UP +4 / CD3`
REACTIVE.
NO consume turno.
Mismo trigger natural 30/20.
Protege siguiente acción ofensiva del jugador por pipeline normal DEF/penetración.

Estos T1 fueron ratificados por humano después de V03 reactivo:
- Sapo HRS: T0 73.28125% → T1 63.0078125%.
- Escarabajo HRS: T0 69.140625% → T1 59.609375%.

La semántica anterior donde T1 consumía turno está descartada para LII.
No volver a V01/V02 salvo auditoría histórica.

Nos quedamos exactamente en T2.

El gate ya está preparado:
`COLAB_LII_T2_RECOGNITION_GATE_V01.zip`

SHA-256:
`0a982fbf34a6235849729069e86a127aa27b6004a38f12c3a8574b7de2e3586d`

Esperado:
61.440 combates.

Yo te voy a adjuntar en esta nueva conversación:
`LII_T2_RECOGNITION_GATE_V01_REVIEW.zip`

NO regeneres el notebook ni repitas la corrida si el resultado está íntegro.

T2 candidate:
`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

Reglas T2:
- memory_window 2;
- necesita 2 acciones EFECTIVA consecutivas de misma categoría;
- categorías visibles:
  PLAYER_BASIC,
  PLAYER_UNITARGET_TECHNIQUE,
  PLAYER_AOE_TECHNIQUE,
  PLAYER_DEFENSIVE_TECHNIQUE;
- no inspecciona root/build;
- no inspecciona RNG futuro;
- puede anticipar T1 si recognition confirmado Y además HP<=40% OR hit actual>=15% maxHP;
- trigger natural T1 30/20 tiene prioridad;
- T1 sigue siendo reactivo y NO consume turno;
- T2 NO modifica magnitud ni cooldown T1;
- no reemplazar técnica canónica due por cadencia.

Cuando te pase el ZIP de resultados:
1. inspeccionarlo completo;
2. validar manifest;
3. verificar 61.440 fights, 0 timeout, 0 NaN/Inf;
4. verificar zero T2 leakage en arm T1_FROZEN;
5. verificar magnitudes/cooldowns T1 intactos;
6. verificar recognition y anticipation >0;
7. verificar canonical technique due/turn preservation;
8. comparar T2 vs T1 pareado por gear/root/policy;
9. calcular root spread después de promediar policies;
10. recordar: T2 >2 pp más fácil que T1 es problema; caída HRS >8 pp es flag de cliff para revisar, no fallo automático.

No uses un target universal de win-rate.

Si el T2 sale limpio:
- dame primero la interpretación simple;
- propone freeze;
- NO lo congeles hasta que yo lo apruebe.

Sólo después de mi aprobación:
- crear T2 freeze manifest;
- actualizar authority;
- pasar Sapo y Escarabajo a `READY_FOR_T3_RECALIBRATION`;
- diseñar T3 causal usando los anchors históricos del handoff.

No perder tiempo repitiendo benchmarks ya cerrados.
