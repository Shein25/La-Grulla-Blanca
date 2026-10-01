# Contrato — estadísticas de monstruos bajo motor nuevo v0.1

**Estado:** GUARDIA EXPERIMENTAL ACTIVA  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Decisión

Los 18 monstruos del Arco 1 se rigen por el **nuevo motor universal de estadísticas**.

El snapshot `canonical/MOBS_ver74.snapshot.json` deja de ser una fuente numérica válida para balance nuevo.

Puede conservar:

- identidad;
- nombre/lore;
- región/elemento;
- nombre de técnica;
- familia mecánica cualitativa.

No puede suministrar al combate nuevo:

- HP/Qi;
- `ataque` o `defensa` legacy;
- daño básico;
- daño/ataque/cadencia numérica de técnica;
- potencia/duración de DOT;
- drenaje de Qi;
- ninguna conversión matemática desde stats legacy.

## Fuente numérica

La fuente de trabajo se construye en:

`experiment/combat-stat-contract-v0.1`

Registro:

`experimentos/balance_nuevo/monster_arc1_new_engine_registry_v0_2.json`

Un monstruo sólo puede entrar a un nuevo benchmark adaptativo cuando su T0 declare:

```text
engine_contract = NEW_COMBAT_STATS_V0_1
stats_status    = READY_NEW_ENGINE_T0
numeric_source  = NEW_ENGINE_ONLY
```

y tenga explícitos:

```text
HP
Qi max
Precisión
Evasión
DEF
Tenacidad
Control
Crítico
Daño crítico
Ataque básico
```

Las técnicas deben declarar sus propios parámetros nuevos.

## Orden obligatorio

```text
T0 NUEVO
→ adaptación poblacional T1–T4
→ abilities adaptativas
→ effectiveKit
→ Monster Combat AI
→ resolver del motor nuevo
```

No:

```text
MOBS_ver74
→ conversión de ataque/defensa
→ adaptación
```

## Consecuencia sobre trabajos anteriores

Los tests que leen `MOBS_ver74.snapshot.json` siguen siendo válidos para:

- recuperación de contenido;
- asignación de perfiles;
- smoke tests de decisión;
- arquitectura de IA;
- historia de los experimentos.

No son autoridad numérica para balance futuro.

Los benchmarks adaptativos nuevos deberán migrarse al bridge de stats nuevo antes de producir cifras de balance.

## C_STAGGERED

Se conserva como **dirección seleccionada de adaptación poblacional**, pero sus números deben revalidarse después de cerrar los T0 nuevos.

T0 define la criatura natural.  
T1–T4 modifican esa criatura; no reparan una ficha legacy.

## Rata de Qi / Mordisco Frenético

`rata_qi__mordisco_frenetico_t4` usa un escalar del **ataque básico T0 nuevo**.

Nunca debe resolver:

```text
0.75 × 1d4 legacy
```

por el solo hecho de que ver74 tuviera `daño: 1d4`.

Debe resolver:

```text
0.75 × basic_damage del perfil READY_NEW_ENGINE_T0
```

El escalar 0.75 sigue siendo LAB y será recalibrado en la simulación T1–T4.

## Guardia ejecutable

`adaptive/monster-stat-source-contract-v0.1.mjs`

expone `assertNewEngineMonsterBase()`, que rechaza:

- perfiles pendientes;
- fuentes numéricas que no sean `NEW_ENGINE_ONLY`;
- campos legacy `ataque/defensa/daño`;
- perfiles incompletos.

La regla cubre los 18 monstruos.
