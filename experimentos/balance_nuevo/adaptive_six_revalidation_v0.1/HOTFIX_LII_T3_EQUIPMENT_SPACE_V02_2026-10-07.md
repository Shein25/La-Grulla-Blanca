# HOTFIX — LII T3 Equipment-Space Gate V02

Fecha: 2026-10-07
Estado: HOTFIX2 / POST-SIMULATION AGGREGATION ONLY

## Incidente

Después de completar la campaña V02, `aggregate_species_gear()` fallaba con:

`TypeError: unsupported operand type(s) for -: 'float' and 'NoneType'`

## Causa

`T2_REFERENCE` contiene referencias históricas sólo para los tres loadouts canónicos:

- CARRY_OVER_FLOOR
- EXPECTED_STAGE
- HIGH_ROLL_STRESS

V02 incorpora además loadouts derivados del censo exhaustivo del espacio de equipo. Para esos contextos no existe una referencia histórica T2 externa y `dict.get()` devuelve `None`. El agregador intentaba calcular un drift contra ese `None`.

## Corrección

El drift histórico T2 se calcula únicamente cuando existe una referencia:

```python
ref = T2_REFERENCE.get((mid, gear)) if arm == "T2_FROZEN" else None
row["t2_reference_win_rate"] = ref
row["t2_reference_drift_pp"] = (100.0 * (row["win_rate"] - ref)) if ref is not None else None
```

Los contextos no canónicos conservan `t2_reference_win_rate = null` y `t2_reference_drift_pp = null`.

## Impacto

- No cambia T0, T1, T2 ni T3.
- No cambia semillas.
- No cambia CRN.
- No cambia el cohort de 64 equipos.
- No cambia los 1.310.720 combates.
- No requiere repetir combates si el checkpoint y chunks ya están completos.
- La corrección afecta únicamente la agregación/postproceso y empaquetado final.

Runner HOTFIX2 SHA-256:
`e67688e96f5a1a05965a7c7e4d683c1de09781f49cf27c6562d3e08a0d515072`

No main. No merge. No freeze automático.
