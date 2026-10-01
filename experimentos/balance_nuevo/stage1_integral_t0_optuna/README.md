# STAGE1_INTEGRAL_T0_OPTUNA

Infraestructura de laboratorio para el balance integral T0 de los cinco monstruos
LianQi I.

## Estado

`ARCHITECTURE_IMPLEMENTED_NOT_SEARCHING`

Este directorio **todavía no ejecuta Optuna**. Su función en este primer bloque
es cerrar las fronteras del experimento antes de lanzar cualquier búsqueda.

## Autoridad

- rama: `experiment/combat-stat-contract-v0.1`;
- contrato: `NEW_COMBAT_STATS_V0_1`;
- catálogo canónico: `../monster_arc1_registry.json`;
- resolver integral reutilizable: `../etapa19b_combat_engine.py`.

No se crea un segundo resolver.

## Regla de candidatos

Los perfiles canónicos permanecen:

`PENDING_INTEGRAL_REBALANCE`

Un trial se representa como `T0LabCandidate`. Un candidato LAB:

- no modifica el registro;
- no usa `stats_status=READY`;
- no usa `params_status=READY`;
- no habilita T1-T4;
- no habilita Definitivas;
- conserva identidad, mecánicas y perfil cognitivo/social de la especie.

Sólo después de selección humana, validación high-fidelity y cierre explícito
podrá escribirse un perfil canónico READY.

## Cinco especies

1. `rata_qi`
2. `avispa_jade`
3. `serpiente_qi`
4. `mono_pildoras`
5. `lobo_espiritual`

La Rata T0 no posee técnica. `Mordisco Frenético` y cualquier otra habilidad
adaptativa permanecen fuera de este laboratorio T0.

## Fuentes numéricas prohibidas

El paquete no puede importar:

- `config_lianqi1_naked.py`;
- `phase_a_enemy_profiles_lab.py`;
- `sim_core.py`;
- `etapa19c_li_screen.py`.

Esos artefactos pueden conservar valor histórico/metodológico, pero sus números
no son baseline de monstruos para este experimento.

## Search spaces

`search_space.py` declara **bandas LAB de exploración**, no valores finales.
La identidad fija no se entrega a Optuna.

`qi_max` de monstruos permanece deliberadamente sin resolver mientras no exista
una semántica T0 autoritativa de gasto/uso de Qi para estas técnicas. El campo
no forma parte del espacio de búsqueda y bloquea la promoción canónica; no se
rellena con 0 ni con un valor histórico.

## Métricas

`metrics_contract.py` fija el contrato mínimo de observabilidad para el nuevo
runner: supervivencia, HP/Qi, daño por fuente, Control, defensivas, acciones de
monstruo, causa/ronda de muerte, uso de consumibles y distribuciones.

## Siguiente bloque

1. instrumentar ETAPA19B sin cambiar fórmulas;
2. implementar `VETERAN`;
3. crear el runner LAB que resuelve `T0LabCandidate` sin falsear READY;
4. smoke de Rata;
5. recién entonces integrar Optuna real.
