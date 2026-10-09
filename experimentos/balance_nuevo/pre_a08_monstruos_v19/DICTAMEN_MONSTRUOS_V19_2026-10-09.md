# La Grulla Blanca · V19 — Microbalance de Cangrejo/Jabalí con Concordancias V17

**Fecha:** 2026-10-09 · **Estado:** PASS EXPERIMENTAL / NO CANON / NO CAMBIOS AL JUEGO  
**Autoridad de habilidad:** perfil V17, Tramo I de LianQi II, dos puntos.  
**Fuente de monstruos:** V18; cuatro otras especies permanecen inalteradas.

## Objetivo y método
Contrastar dos cambios focales de reacción T1 mediante cuatro brazos **pareados por semilla**: `ORIGINAL_OFF / ORIGINAL_ON / CANDIDATE_OFF / CANDIDATE_ON`.

- `cangrejo_cauce`: defensa reactiva `DEFENSE_UP.defense_bonus` **3→2** (sin alterar DEF básica, HP, Pinza o T0).
- `jabali_pizarra`: `MITIGATE_NEXT.damage_reduction_pct` **40→35 %** (sin alterar ataque, HP, T0).
- Habilidades V17 fijas; ninguna otra técnica, estatística ni pieza de equipo fue modificada.
- Concordancia defensiva V17 **BASE**: 17 pares numéricos, un negativo sin receptor, y **por separado** Placa Fundacional Tierra→Metal / Embalse Tierra→Agua físicos sobre el motor experimental V04B. No hubo resolución física de hooks condicionales de Tramo I.
- Dos estrategias de combate `EARLY`/`DELAYED_TRIGGER`; tiers T1/T2; cinco raíces; 16 builds monorraíz por raíz; tres kits de laboratorio `PRE_M03`/`POST_M03`/`EXPECTED_STAGE`.
- Técnica ofensiva ajena asumida conocida para producir el Eco; su acceso/coste oficial aún NO se ha verificado.

## Cardinalidad y QA
| Bloque | Peleas | Contextos pareados de 4 brazos | Semillas |
|---|---:|---:|---|
| Escalares discovery | 55.296 | 13.824 | 81000–81001 |
| Escalares holdout | 55.296 | 13.824 | 82000–82001 |
| Estructurales discovery | 6.144 | 1.536 | 83000–83001 |
| Estructurales holdout | 6.144 | 1.536 | 84000–84001 |
| **Total** | **122.880** | **30.720** | disjuntas |

**QA PASS:** 0 timeouts; 0 ataques programados omitidos; 1.536 contextos negativos sin diferencias entre ON/OFF; 48.832 resoluciones escalares ON, 0 OFF; 5.748 resoluciones estructurales ON, 0 OFF; la reacción T1 se restaura a sus valores originales tras cada ronda; el manifiesto ZIP pasó CRC y SHA-256. Las 30.720 peleas de preflight se excluyen de esta estadística.

**Reproducción desde extracción limpia:** 27.648 peleas escalares con 28 columnas y 3.072 estructurales con 21 columnas: **30.720 filas coincidentes exactamente**, salvo el campo descriptivo `cohort` del runner de reproducción.

## T2, POST_M03 — resultados agregados con Concordancias BASE V17
Matriz escalar, **N=2.304 contextos por monstruo**, con raíces y builds igualmente ponderadas:

| Monstruo | ORIGINAL_OFF | CANDIDATE_OFF | ORIGINAL_ON | CANDIDATE_ON | Δ cambio ON |
|---|---:|---:|---:|---:|---:|
| Cangrejo | 59,90 % | 67,10 % | **62,15 %** | **68,84 %** | **+6,68 pp** |
| Jabalí | 68,53 % | 71,83 % | **71,53 %** | **74,74 %** | **+3,21 pp** |

Holdout aislado conserva la dirección: Cangrejo +5,30 pp ON; Jabalí +3,99 pp ON; discovery +8,07 pp y +2,43 pp, respectivamente. Interacciones candidato × Concordancia son limitadas en esta matriz: Cangrejo −0,52 pp; Jabalí −0,09 pp.

**Por kit con Concordancia BASE ON**:
- Cangrejo T2: PRE_M03 64,89→70,53 %; POST_M03 62,15→68,84 %; EXPECTED_STAGE 99,31→99,35 %.
- Jabalí T2: PRE_M03 72,35→74,91 %; POST_M03 71,53→74,74 %; EXPECTED_STAGE 98,13→98,39 %.

La equipación fuerte produce *techo de victorias*; NO aumentar dificultad de criaturas para compensar acceso que no está garantizado.

## Resultados estructurales V17, calculados APARTE
En T2 POST_M03, **128 contextos por especie y receptor**, a menor resolución que la muestra numérica:
- Cangrejo con Eco Tierra→Agua / Embalse: **+7,81 pp** al aplicar el cambio de monstruo; receptor Metal / Placa: **+5,47 pp**.
- Jabalí con Embalse: **+1,56 pp**; con Placa: **+3,13 pp**.

Placa conserva/refuerza impactos y Embalse almacena/devuelve absorción, sin superar almacenamiento. Son efectos del **puente V04B adaptado**, no pruebas de paridad con HTML. No se suman estos resultados a los escalares.

## Acceso al equipo: dependencia para el freeze, NO bloqueo del microbalance
`docs/experimentos/AUDITORIA_EQUIPO_Y_PROGRESION_ARCO1_2026-09-29.md` diferencia piezas jugables del catálogo Etapa18 **provisional** (58 piezas, 19 atribuidas a LianQi II) y documenta que en esa revisión no existe una capa de equipo LII garantizada.

Las configuraciones de nuestro puente:
- `PRE_M03`: espada_madera_entrenamiento + uniforme_gris_aspirante;
- `POST_M03`: las anteriores + fajin_discipulo_externo;
- `EXPECTED_STAGE`: espada_hierro_equilibrada, bandana_cuero_reforzada, sobretunica_patrulla, fajin_patrulla, sandalias_corriente_ligera, pulsera_cauce_trenzado, anillo_hierro_oxidado.

**No afirmar que los kits correspondan a inventarios obtenibles en el motor actual.** El frente de equipamiento debe verificar acceso por misión y reglas comerciales antes del freeze de la fauna.

## Decisión
**Propuesta técnica V19: retener como baseline experimental los dos ajustes Cangrejo 3→2 y Jabalí 40→35 %.** La robustez frente a Concordancias V17 BASE justifica llevarlos al cruce posterior con equipo realmente obtainable; no significa que hayan sido aplicados ni ratificados.

Preservar sin cambios Búho, Zorro, Murciélago y Araña. Esta última necesita medir veneno, antídotos y aflicción persistente antes de decidir cambios.

**No se ejecutaron** mutantes, élites, T3/T4, AOE, consumibles, hooking condicional de Tramo I, adquisición real de técnica ajena ni paridad de HTML. Los resultados no incluyen ninguno de esos mecanismos.

## Reproducción
Archivo **`GRULLA_MONSTRUOS_LII_V19_CONCORDANCIAS_Y_EQUIPO_2026-10-09.zip`**, SHA256 `4919a8c494e5a25db747a12c8ab6154ab9ea610ff0ded9f41bf674204c42f6db`, **49 ficheros**, manifiesto e integridad verificados. Incluye runners `run_v19_numeric.py`, `run_v19_structural.py`, scripts de análisis, fuentes originales V07/V10/V11/V12/V17, datos crudos pareados, QA y documentación. El ZIP está disponible en la conversación, no en Git.

**Guardias**: no main, no merge, no cambios en motor HTML, equipo ni registry, todos los cambios in-memory restaurados.
