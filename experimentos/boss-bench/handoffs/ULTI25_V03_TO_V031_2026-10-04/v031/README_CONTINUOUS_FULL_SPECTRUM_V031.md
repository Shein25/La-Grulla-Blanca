# Grulla · 25 Ultis · Continuous Full Spectrum V03.1

Estado: **PATCHED / LOCAL ACCEPTANCE PASS / QUICK V03.1 PENDIENTE**.

Este paquete corrige V03 sin reabrir V05 ni tocar técnicas normales. Mantiene una pelea continua F1→F2→F3, Pacto estricto, técnicas normales OFF y `balance_authoritative=false` mientras el progreso F1/F2 siga usando fixture mecánico.

## Correcciones V03.1

- Cooldown: checker por `suite + activation_edge`; FIRST_USE, SECOND_USE_SAME_COMBAT, OOC39, OOC40 y OOC41 ya no comparten exigencias incompatibles.
- Pacto: `f3_first_denied_observed` y `pact_active_after_first_denied` se congelan en la primera negación F3 y nunca se sobrescriben.
- Río Celeste: una activación rechazada no entra en `brain.observe`, no consume la defensa/guardia de la próxima ofensiva y debe ser causalmente idéntica al baseline pareado.
- Late windows: al llegar al umbral mecánico de F1/F2 se arma exactamente una oportunidad de acción del jugador antes del cambio de fase.
- Transiciones: los 11 `transition_edge` ahora ejecutan un fixture mecánico explícito, etiquetado y no autoritativo para balance, en F1→F2 y F2→F3.
- Multi-hit: los paquetes directos posteriores de la misma macro Ulti no pueden consumir HP/ward del pool fresco después de cruzar fase, salvo futura autorización contractual explícita.
- Persistencias: DOT, Hemorragia, Control pendiente, buff/debuff persistente, Absorción permitida y estado de proc de equipo se verifican explícitamente; efectos `GRULLA_PHASE_LOCAL_*` expiran al cambiar fase.
- Equipo: el perfil elegido se propaga al hook V05 durante la corrida para que el proc de HIGH_ROLL_STRESS pueda comprobarse en su edge dedicado.
- Sentencia del Filo Celestial: sólo `BALANCE_PRIORITY`; no se aplica nerf/buff automático.

## Aceptación local obligatoria

`local_acceptance` ejecutó 301 casos y pasó con 0 hard issues:

- 38 modos × 4 ventanas críticas = 152 casos.
- Cooldown: 25 Ultis × 5 edges = 125 casos.
- Transición: 11 edges × 2 fronteras = 22 casos.
- Río rechazado + baseline pareado = 2 casos.

Activaciones observadas en las ventanas críticas del smoke local: F1 late 27/38, F2 late 28/38, F3 primera negación 37/38 y F3 post-release 37/38. Una no activación legal no se fuerza ni se transforma en autoridad de balance.

## QUICK V03.1

Se generó, pero **NO se ejecutó**, la matriz QUICK V03.1: 28.464 casos. `PHASE_TRANSITION` sube a 836 porque cada edge se comprueba en ambas fronteras. Ejecutar QUICK sólo después de verificar hashes del paquete.

```bash
python generate_full_spectrum_cases_v031.py --preset quick --out cases_v031.jsonl
python run_full_spectrum_v031.py --cases cases_v031.jsonl --runner grulla_continuous_ulti_runner_v031.py --out CONTINUOUS_FULL_SPECTRUM_V031
```

No ejecutar `standard` hasta que QUICK V03.1 quede limpio.

## Guardias

- NO `main`.
- NO merge.
- V05 inmutable.
- Técnicas normales OFF; otro agente las trabaja.
- Consumibles OFF en headline.
- Fixtures de stress ≠ autoridad de balance.
- No auto-canon y no ajuste automático de Ultis.
