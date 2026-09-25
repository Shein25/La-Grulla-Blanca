# IMPLEMENTACIÓN — Adaptive Ecology v0.1

Usar como contrato:
`experimentos/backups/ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_FINAL.md`

Repositorio:
`Shein25/La-Grulla-Blanca`

Base exacta:
`5812deb59cd1c133383b9af973486a702a26daf4`

Rama:
`experiment/monster-ecology-adaptation-v0.1`

Ruta:
`experimentos/monster-ai/adaptive-ecology-v0.1/`

Implementar exclusivamente el laboratorio v0.1.

API principal:
```js
advancePopulation({
  populationState,
  now,
  event = null,
  speciesConfig
})
```

Obligatorio:
- función pura;
- SPECIES_KILLED único evento positivo;
- pressure 0..100;
- decay lineal O(1);
- recentEventIds FIFO acotado;
- tier derivado;
- activeAdaptations derivadas;
- effectiveKit canónico por abilityId;
- ContractError para errores contractuales;
- status OK / DUPLICATE_EVENT / INVALID_POPULATION;
- sin observations;
- sin RNG;
- sin stat scaling;
- sin Monster AI;
- sin producción.

Tests:
- implementar todos los Goldens A–AG de la FINAL;
- agregar AH threshold boundary;
- agregar AI now rewind;
- adversariales de overflow, locality, dedup, reorder, frozen inputs, unknown abilities.

Stress:
```text
100+ poblaciones
x
1000+ transiciones coherentes
>= 100.000 transiciones
```

Críticos en cero:
```text
invalidEffectiveKits
inputMutations
statModifiersProduced
crossPopulationLeaks
nondeterministicMismatches
```

Repetir dataset y exigir digest idéntico.

No tocar:
- main;
- ver74;
- Monster Combat AI;
- Utility AI;
- GOAP;
- ramas implement/*.

No mergear.

Si GitHub está disponible, abrir PR DRAFT. Si no está disponible, reportarlo honestamente y entregar candidata local empaquetada.

El reporte final debe incluir base/branch/HEAD/parent/tree cuando existan, archivos, tests, stress, digests, métricas críticas y:
```text
PRODUCTION FILES TOUCHED: NO
EXISTING EXPERIMENTS TOUCHED: NO
MAIN MODIFIED: NO
MERGE PERFORMED: NO
```
