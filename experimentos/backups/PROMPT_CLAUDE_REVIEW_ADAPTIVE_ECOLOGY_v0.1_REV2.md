# Revisión independiente — Adaptive Ecology v0.1 REV2

Revisá:
`experimentos/backups/ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_REV2.md`

**No implementes código.**

La REV2 decidió:
1. sólo `SPECIES_KILLED`;
2. observations fuera;
3. pressure entero 0..100;
4. decay lineal en tiempo lógico;
5. tier derivado/no persistido;
6. activeAdaptations derivadas/no persistidas;
7. adaptaciones reversibles y acumulativas;
8. recentEventIds explícito/acotado;
9. sin RNG;
10. sin stat scaling;
11. sin Monster Utility;
12. sin hysteresis ni cooldown de tier en v0.1.

Punto especial: la revisión anterior sugirió cooldown de tier. REV2 lo rechaza porque agregaría estado y rompería la pureza `tier = f(pressure, config)`. Auditá críticamente esta decisión.

Intentá romper:
- ventana de dedup;
- replay de IDs fuera de ventana;
- decay→event;
- overflow;
- canonical ordering;
- reorder invariance;
- cambios de config;
- reversibilidad;
- locality;
- now/occurredAt;
- source of truth;
- idempotencia;
- crecimiento de save;
- frontera con v0.2.

Formato obligatorio:

1. Veredicto exacto:
   - `ADAPTIVE_ECOLOGY_V01_REV2_APTA_PARA_IMPLEMENTAR`
   - `ADAPTIVE_ECOLOGY_V01_REV2_REQUIERE_CAMBIOS`
   - `ADAPTIVE_ECOLOGY_V01_REV2_FALLO_CONCEPTUAL`
2. Bloqueantes
3. No bloqueantes
4. Exploits/adversariales
5. Contradicciones internas
6. Evaluación sin hysteresis/cooldown
7. Evaluación recentEventIds
8. Evaluación decay→event
9. Goldens adicionales
10. Contrato mínimo final recomendado
11. Conclusión

No crees ramas.
No modifiques repositorio.
No implementes.
