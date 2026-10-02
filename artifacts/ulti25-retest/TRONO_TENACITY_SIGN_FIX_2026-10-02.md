# ULTI25 — Trono del Volcán Sepultado · corrección de signo TEN

Fecha: 2026-10-02

Estado: LAB / NO RUNTIME / NO CANON / NO MERGE / NO PUSH

## Hallazgo

La auditoría manual del retest masivo detectó que `EARTH_TRONO_VOLCAN_SEPULTADO` aplicaba correctamente:

- Fractura 1: -1 DEF
- Fractura 2: -2 DEF total

pero el `-15 TEN` de Fractura 2 se almacenaba como `+15` en `temp_stats['tenacity_penalty']`.

El motor calcula Control así:

`base_control + source.control + source.temp_control - target.tenacity - target.temp_stats['tenacity_penalty']`

Por lo tanto `+15` reducía la probabilidad de Control en vez de aumentar la vulnerabilidad del objetivo.

## Corrección exacta del LAB

Antes:

```python
new_def, new_ten = -min(2.0, current_real), 15.0
target.temp_stats['tenacity_penalty'] = new_ten
m['debuff_tenacity'] = max(m.get('debuff_tenacity', 0), new_ten)
```

Después:

```python
new_def, new_ten = -min(2.0, current_real), -15.0
target.temp_stats['tenacity_penalty'] = new_ten
m['debuff_tenacity'] = max(m.get('debuff_tenacity', 0), abs(new_ten))
```

## Retest focal local

Se repitieron los 273 escenarios heredados de Trono con:

- 2.000 réplicas por escenario
- 546.000 simulaciones
- misma seed base: 2026100256
- mismos ordinales de escenario / streams RNG
- mismo motor y runner base

Resultado:

- SELF_CHECK: PASS
- daño: sin cambios
- kills: sin cambios
- DEF shred: sin cambios
- Control F2: corregido

Promedio FULL:
- control_successes / turns_denied: 0.0810 -> 0.2662

BALANCED + FULL:
- control_successes / turns_denied: 0.0540 aprox. -> 0.2035

## SHA-256

- runner corregido: `9cb10f2166fedaf6bc90745e12b1200612706e91a98d7e1d651ffbf9cf0442d1`
- summary.csv: `b0030c85c1e6d2c8b08144e3b3069b1cb1540d985fd352de4f14549365172b06`
- ZIP compacto: `b7d6cd3864ebed4ed7e918dde210df04455637975296695ad77cb6fef6ddf184`

Esta corrección no modifica ninguna decisión humana ni reabre el diseño de la Ulti.
