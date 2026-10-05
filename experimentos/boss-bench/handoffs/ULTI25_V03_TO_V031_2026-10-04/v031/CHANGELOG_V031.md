# Changelog V03 → V03.1

## Fixed

1. Falsos positivos del checker de cooldown: contrato evaluado por `suite + activation_edge`.
2. Telemetría del Pacto: primera negación F3 inmutable.
3. Contaminación de Río Celeste rechazado:
   - `brain.observe` ocurre sólo tras `activated=true`;
   - un rechazo no consume el estado de “próxima ofensiva”;
   - oracle pareado fuerte exige equivalencia causal con baseline.
4. F1/F2 late: una oportunidad exacta de jugador antes del avance mecánico.
5. `transition_edge`: ejecución real en F1→F2 y F2→F3 para exact lethal, overkill, multi-hit, DOT, Hemorragia, Control, buff, debuff, Absorción y dos estados de proc de equipo.
6. Multi-hit directo: no derrama al pool/ward fresco dentro de la misma macro Ulti.
7. OOC41 agregado al contrato local.
8. Perfil de equipo propagado al hook V05 durante la corrida para probar su efecto real.

## Not changed

- V05 y sus dependencias aceptadas: hashes intactos.
- HP/DEF/Abs/Pacto de la autoridad de bench.
- Técnicas normales y consumibles.
- Diseño de las 25 Ultis.
- `main` y política de merge.

## Balance

`METAL_SENTENCIA_FILO_CELESTIAL` queda marcado únicamente `BALANCE_PRIORITY`. V03.1 no realiza nerf, buff ni canon automático.

## Validation

- Self-check V03.1: PASS.
- Local acceptance: 301 casos, 0 hard issues.
- 38/38 modos presentes en cuatro ventanas críticas.
- 22/22 celdas transición edge×fase PASS.
- 125/125 cooldown edge cases sin issues.
- Río rechazado == baseline: PASS.
- QUICK V03.1: generado únicamente; no ejecutado.
- STANDARD: no ejecutado.
