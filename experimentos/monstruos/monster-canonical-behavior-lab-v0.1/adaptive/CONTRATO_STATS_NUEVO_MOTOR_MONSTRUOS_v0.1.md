# Contrato — estadísticas de monstruos bajo motor nuevo v1

**Estado:** ACTIVO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Autoridad única

Los 18 monstruos del Arco 1 usan exclusivamente:

`NEW_COMBAT_STATS_V0_1`

Catálogo del laboratorio:

`canonical/monsters.json`

Fuente de balance:

`experiment/combat-stat-contract-v0.1/experimentos/balance_nuevo/monster_arc1_registry.json`

No existe una segunda fuente de estadísticas ni una capa de compatibilidad.

## Perfil T0

Un monstruo sólo puede entrar a combate o benchmark cuando declare:

```text
engine_contract = NEW_COMBAT_STATS_V0_1
stats_status    = READY
```

y tenga resueltos:

```text
hp
qi_max
precision
evasion
defense
tenacity
control
crit_chance
crit_damage
basic_damage
```

Si posee técnica, ésta debe declarar:

```text
params_status = READY
params.cadence
+ todos los parámetros numéricos que exijan sus mechanics
```

Un perfil pendiente provoca error. No se rellena automáticamente.

## Orden obligatorio

```text
T0 READY
→ adaptación T1–T4
→ abilities adaptativas
→ effectiveKit
→ Monster Combat AI
→ resolver del motor nuevo
```

La adaptación no sintetiza el T0.

## Etapas

La etapa nativa define banda ecológica, rol y techo de aprendizaje. No genera estadísticas mediante una tabla global.

Cada criatura recibe sus estadísticas T0 directamente durante su balance integral.

## T1–T4

Las capas adaptativas se recalibran sobre el T0 final de cada especie.

La estructura de aprendizaje puede conservarse, pero ningún multiplicador o habilidad adaptativa se considera numéricamente validado hasta probarse con el perfil T0 `READY`.

## Rata de Qi

`rata_qi__mordisco_frenetico_t4` escala sobre `stats.basic_damage` del perfil T0 `READY`.

Su escalar actual continúa siendo LAB hasta la calibración T1–T4.

## Guardia ejecutable

`adaptive/monster-stat-source-contract-v0.1.mjs`

expone `assertMonsterProfile()`.

Los perfiles incompletos quedan fuera de combate por diseño.
