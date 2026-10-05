Retoma el frente **Ultis vs Grulla** de `La Grulla Blanca` exactamente desde el handoff Git de V03→V03.1.

Repositorio: `Shein25/La-Grulla-Blanca`.

REGLAS DURAS:
- NO tocar `main`.
- NO merge.
- Trabajar sólo sobre la rama de backup/handoff indicada por el usuario o crear una rama experimental hija.
- Este agente se ocupa EXCLUSIVAMENTE de las 25 Ultis y el runner de Grulla. Otro agente balancea técnicas normales.
- No rediseñar técnicas normales.
- V05 aceptado es inmutable: SHA-256 `3372ee2172253eaf7f410616693960bf6ad8da5510f1ad611d5506631ea648f5`.
- No auto-canon. Las decisiones humanas prevalecen.
- `balance_authoritative=false` mientras sigamos usando avance mecánico de fase sin las técnicas finales.
- NO correr `standard` hasta que QUICK V03.1 pase limpio.

PRIMERO:
1. Lee completo `HANDOFF_ULTI25_CONTINUOUS_V03_TO_V031_2026-10-04.md`.
2. Lee `V03_QUICK_AUDIT_SNAPSHOT_2026-10-04.json`.
3. Inspecciona las fuentes V03 respaldadas en la misma carpeta Git.
4. Verifica hashes y rama antes de modificar nada.

ESTADO EXACTO:
- QUICK V03 ejecutó 28.046 casos.
- FAIL bruto = 504 hard issues, pero 500 son falsos positivos del checker de cooldown y 4 falsos positivos de telemetría del Pacto.
- Motor/Pacto central salió sano: 0 simulation errors, 0 truncations, 0 F3 kill before first real action, release max 1, 0 duration violations, 0 AOE violations; death-gate intervino en 712 casos.
- BUG REAL: Río Celeste rechazado contamina la memoria de Grulla porque `brain.observe` sucede antes de saber `activated`. Entre 211 rechazos hubo 47 pares con HP jugador distinto, 36 Qi distinto y 3 outcomes distintos; NOT_ATTEMPTED fue idéntico al baseline.
- F2_LATE_PRE_TRANSITION = 0/1216 activaciones; F1 late = 119/1216.
- PHASE_TRANSITION tiene 418 casos pero `transition_edge` no es consumido por el runner; sólo 24 activaron Ulti, todos Fuego.
- Sentencia muestra señal de potencia prioritaria, pero NO nerfear todavía.

OBJETIVO:
Construir **V03.1 correctiva**, no rehacer el laboratorio desde cero.

CORRECCIONES OBLIGATORIAS:
A. Checker cooldown/oracles: scope por `suite` + `activation_edge`.
B. Pacto: congelar telemetría de la PRIMERA acción F3 negada y no sobrescribirla.
C. Río: Grulla sólo observa la Ulti después de una activación aceptada. Un rechazo sin otros cambios debe ser causalmente idéntico al baseline.
D. Late windows: hacer alcanzables F1/F2 late con una oportunidad de jugador antes del avance mecánico de fase.
E. `PHASE_TRANSITION`: implementar realmente cada edge (exact lethal, overkill, multihit, DOT, Hemorragia, control, persistencias, equipment proc) con setup/oracle explícitos.
F. Mantener Pacto estricto y no transferir overkill entre pools.
G. Mantener una sola pelea F1→F2→F3 con estado del jugador persistente.
H. No convertir fixtures de stress en autoridad de balance.

PRUEBAS LOCALES ANTES DE ENTREGAR NOTEBOOK:
- 38 modos × ventanas críticas.
- rejected Río == baseline.
- F1 late y F2 late con cobertura material.
- cada transition_edge observado y marcado.
- primera negación F3 conserva Pacto.
- primer real resolved libera una vez.
- cooldown SECOND_USE / OOC39 / OOC40 / OOC41.
- 0 hard issues.

ENTREGABLES:
- `grulla_continuous_ulti_runner_v031.py`
- `run_full_spectrum_v031.py`
- generador V031 si hace falta
- oracles V031
- README/changelog
- manifiesto SHA-256
- notebook Kaggle autocontenido V031
- ZIP de campaña V031
- resumen exacto de smoke local.

Después se corre **QUICK V03.1**, se audita fila por fila, y sólo entonces `standard`.
