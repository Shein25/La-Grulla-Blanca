# LianQi II — T1/T2 Adaptive Bridge Contract Gate V01

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: PLAN, NO SIMULATION FREEZE

## Justificación

El preflight `LII_STAGE_REAL_PREFLIGHT_V01` pasa los 23.040 combates T0, las cinco defensivas y Tramo I.

Pero `etapa19b_combat_engine.py` **rechaza explícitamente todo tier diferente de T0**. Por tanto, no se puede arrancar la campaña T1/T2 simplemente cambiando `tier`.

Sapo de Ceniza y Escarabajo de Hierro tienen T1/T2 human-ratified en el registro, pero la descripción de un perfil no equivale a una implementación ejecutable validada.

## Entradas autoritativas

- `monster_arc1_registry.json` (LII T0/T1/T2 ratified statuses)
- Contratos freeze y runners originales de `T0_LII_HUMAN_RATIFIED_2026-10-07`, `T1_LII_REACTIVE_HUMAN_RATIFIED_2026-10-07`, `T2_LII_RECOGNITION_HUMAN_RATIFIED_2026-10-07` (recuperar rutas y hashes antes de construir el adapter)
- `etapa19b_combat_engine.py` (jugador/Tramo I/equipo LII)
- `LII_STAGE_REAL_PREFLIGHT_V01_REVIEW_2026-10-07.md`

No reemplazar contratos con aproximaciones inventadas.

## Gate A — Discovery / Source lock

1. Encontrar y leer contratos nativos exactos de las dos especies READY.
2. Encontrar implementación nativa de T1/T2, o construir lab-only adapter únicamente después de leer esos contratos.
3. Fijar SHA-256 de fuentes, commit, motor y adapter.
4. Conservar T0 del preflight como baseline; no modificar stats ni IA congela­dos.

## Gate B — Event-level parity

Sapo:
- T1 MITIGATE_NEXT 60%, cooldown 3.
Escarabajo:
- T1 DEFENSE_UP +4, cooldown 3.

T1 natural (ambos):
- HP <= 30% OR current received hit >=20% maxHP.

T2:
- memoria 2;
- dos acciones EFECTIVAS consecutivas de la misma categoría;
- anticipación HP<=40% OR current hit>=15% maxHP;
- triggers naturales T1 conservan prioridad;
- anticipación no reemplaza acción debida por cadencia;
- duración/cargas/cooldown de T1 preservados.

No confundir la adaptación T2 del monstruo con LianQi II del jugador. Verificar casos de borde por eventos: ataque que activa natural vs anticipación, ataques fallados, defensivas efectivas, categoría cambiante, cadencia due y expiración/cooldown.

## Gate C — Tactical defensive policies

El preflight prueba solamente:
- `UNITARGET_FIRST`
- `DEFENSE_OPEN`

Las pruebas causales deben añadir:
- apertura ofensiva;
- apertura defensiva;
- defensiva según condición razonable (HP/peligro/beneficio real, sin conocer RNG futuro);
- reserva de Qi para mantener ofensiva;
- no resucitar ni autoconsumir defensivas sin costes.

Evaluar contra Sapo normal y Escarabajo TANK, T1/T2; pruebas de sensibilidad del comportamiento y no sólo WR.

## Gate D — Build/gear sampling

- 80 builds monorraíz sólo como primer subespacio, no como cierre.
- ENTRY / EXPECTED / HIGH_ROLL.
- observar transición real de adquisición M04/M05/M06 y carry-over LI; no tratar los tres perfiles como probabilidades históricas.
- Primero R32/64 para screening, R256 condicionado a riesgo; common random numbers.
- Añadir configuraciones multielementales legalmente aprendidas en una fase posterior antes de freeze global.

## Bloqueantes duros

- Falta de fuente canónica exacta para T1/T2.
- Divergencias de eventos adaptativos con el laboratorio nativo.
- Monitor de cadencia o due no preservado.
- Bug de defensa o Qi inducido por el adapter.
- Cualquier AOE o Tramo II/III en LII.

## No hacer

- No main; no merge; no push salvo autorización;
- no editar HTML/runtime; Astra integra después;
- no reabrir LI;
- no inflar estadísticas de monstruos por T0 smoke de altas tasas de victoria;
- no simular tier T2 con el motor T0 sin adapter;
- no congelar LII con una campaña inicial de R24.

## Salidas

Primero `LII_T1_T2_ADAPTIVE_BRIDGE_CONTRACT_GATE_V01_REVIEW.zip`.

Sólo con ese gate PASS se autoriza la campaña `LII_DEFENSIVE_T1_T2_CAUSAL_GATE_V01`.
