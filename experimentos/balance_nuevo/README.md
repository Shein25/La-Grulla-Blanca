# Balance nuevo — marco reproducible

Este directorio contiene el laboratorio de balance del contrato nuevo.

## Regla cero

**No importar estadísticas numéricas de ver74.**

Toda magnitud usada por una simulación debe aparecer explícitamente en un archivo/configuración de escenario y tener una de estas procedencias:

- `CANON`: cerrada por contrato nuevo.
- `PROVISIONAL`: valor actual de una técnica del rediseño.
- `LAB`: hipótesis deliberada para sensibilidad.

Nunca se permiten valores implícitos.

## Flujo de trabajo

```text
CONFIG
  ├─ actor/player
  ├─ enemy profile
  ├─ technique
  ├─ branches
  └─ scenario
        ↓
SIM CORE
        ↓
MONTE CARLO
        ↓
METRICS
        ↓
CSV / tablas / gráficos
```

Cambiar un test significa modificar CONFIG/SCENARIO, no reescribir el motor.

## Métricas estándar

- hit rate;
- crit rate;
- daño directo medio/mediana/p10/p90;
- daño a HP;
- daño absorbido;
- TTK;
- supervivencia;
- HP final;
- Qi gastado;
- acciones realizadas;
- daño por Qi;
- mitigación por acción defensiva;
- Control aplicado;
- uptime de estados;
- frecuencia de branches/hook.

## Perfiles por etapa

No hay valores heredados.

Cada etapa deberá declarar explícitamente:

```python
StageProfile(
    hp=...,
    qi=...,
    precision=100, # CANON: referencia normal
    evasion=...,
    defense=...,
    control=...,
    tenacity=...,
)
```

Sólo HP/Qi/acceso pueden crecer automáticamente por cultivo según contrato.

## Colab

El notebook `COLAB_BALANCE_NUEVO.ipynb` está pensado para:

1. clonar esta rama;
2. importar `sim_core.py`;
3. declarar perfiles;
4. correr decenas/cientos de miles de iteraciones;
5. exportar resultados.

La semilla queda fija por escenario para reproducibilidad.

## Guardia de monstruos — migración v0.2 (2026-09-30)

La Regla cero se aplica también a **todos los monstruos**.

Fuente de entrada obligatoria para nuevo balance:

`monster_arc1_new_engine_registry_v0_2.json`

El archivo `monster_arc1_new_contract_lab.json` queda **DEPRECATED / LEGACY_CONTAMINATED / DIAGNOSTIC_ONLY**.

Prohibido para los 18 monstruos:

- heredar HP, daño o magnitudes de técnicas desde ver74;
- convertir `legacy_attack` en Precisión;
- convertir `legacy_defense` en Evasión o DEF;
- usar una cifra legacy porque "se parece" a la escala nueva;
- aplicar T1–T4 sobre un T0 todavía pendiente de migración.

Todo runner nuevo de balance debe abortar si `stats_status` sigue en
`PENDING_INTEGRAL_REBALANCE_NEW_ENGINE`.

Orden:

```text
identidad del monstruo
→ stats T0 expresadas directamente en unidades del motor nuevo
→ validación integral
→ adaptación T1–T4
→ IA
→ resolver nuevo
```

Auditoría completa:

`docs/experimentos/AUDITORIA_MIGRACION_ESTADISTICAS_18_MONSTRUOS_NUEVO_MOTOR_2026-09-30.md`

