# STAGE1_INTEGRAL_T0_OPTUNA

Laboratorio NEW ENGINE ONLY para el balance integral T0 de los cinco monstruos
LianQi I.

## Estado

`RATA_SMOKE_IMPLEMENTED_NOT_EXECUTED`

La arquitectura, el runner LAB, la telemetría, la policy `VETERAN`, la
propuesta de candidatos y el estudio Optuna real de la Rata están implementados.

**Todavía no se ha ejecutado el smoke del repositorio ni se ha promovido ningún
número a CANON.**

## Autoridad

- rama: `experiment/combat-stat-contract-v0.1`;
- contrato: `NEW_COMBAT_STATS_V0_1`;
- catálogo canónico: `../monster_arc1_registry.json`;
- resolver integral reutilizado: `../etapa19b_combat_engine.py`.

No existe un segundo resolver. `telemetry.py` y `runner.py` envuelven el
resolver existente y restauran sus funciones al terminar cada corrida.

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

La Rata T0 no posee técnica. Las habilidades adaptativas permanecen fuera del
runtime T0.

## Fuentes numéricas prohibidas

El paquete no puede importar:

- `config_lianqi1_naked.py`;
- `phase_a_enemy_profiles_lab.py`;
- `sim_core.py`;
- `etapa19c_li_screen.py`.

Esos artefactos conservan sólo valor histórico/metodológico.

## Search spaces

`search_space.py` declara bandas LAB de exploración, no valores finales.
`dice_space.py` genera notaciones explícitas de dados dentro de las bandas de
media y `proposal.py` las entrega a Optuna mediante `suggest_categorical()`.

`qi_max` de monstruos permanece deliberadamente sin resolver. No participa
del search space. Durante el runtime LAB se usa un sentinel `NaN`, de modo
que una futura ruta que intente usar ese recurso no pueda recibir
silenciosamente un número inventado.

## VETERAN

`player_policy_veteran.py` usa únicamente:

- HP/Qi actuales del jugador;
- HP actual visible del enemigo;
- resultados ya observados en la pelea;
- DOT/defensa actualmente visibles;
- propiedades del propio kit del jugador.

No lee RNG futuro ni DEF, Evasión, Precisión o Tenacidad ocultas del monstruo.
Puede elegir voluntariamente ataque básico para conservar Qi.

## Contextos principales

Por candidato:

- 5 raíces;
- `MANDATORY_ENTRY + NONE + VETERAN`;
- `EXPECTED_STAGE + NONE + VETERAN`.

Total: 10 contextos primarios.

`HIGH_ROLL_STRESS` y `UNITARGET_FIRST` quedan como brazos de stress/control.
`BLOOD_1` está declarado pero bloqueado hasta tener contrato autoritativo
compatible con el motor nuevo.

## Métricas

`telemetry.py` añade sin cambiar fórmulas:

- HP mínimo;
- daño básico/técnica/DOT por bando;
- activaciones defensivas;
- usos BASIC/TECHNIQUE/SKIPPED del monstruo;
- causa y ronda de muerte;
- uso forzado de básico por Qi;
- uso por acción/técnica.

`aggregate.py` produce distribuciones y breakdown por raíz/loadout.

## Optuna

`optuna_study.py` usa explícitamente:

- `optuna.create_study(...)`;
- `trial.suggest_int(...)`;
- `trial.suggest_categorical(...)`;
- `study.optimize(..., n_jobs=1)`;
- `NSGAIISampler(seed=...)`;
- SQLite persistente.

No existe objetivo `abs(win_rate-target)`.

### Rata — smoke

`rata_smoke.py` es el primer estudio ejecutable:

- 32 trials por defecto;
- 20 peleas por contexto;
- 10 contextos primarios;
- 6.400 peleas totales por corrida limpia.

El Pareto de Rata usa:

1. maximizar presión observada sobre HP;
2. minimizar presupuesto normalizado del candidato.

El presupuesto se normaliza contra sus propias bandas LAB y evita que el
estudio convierta “más stats” en una solución dominante.

## Reproducibilidad

- master seed explícita;
- seed estable por especie/trial/contexto/raíz/pelea;
- SQLite por estudio;
- `n_jobs=1` para el orden de trials;
- candidate ID = especie + trial number + SHA-256 de parámetros;
- export CSV + JSONL;
- `manifest.py` registra hashes de motor, registro, técnicas y equipo.

## Próximo paso operativo

Ejecutar primero:

`selfcheck.py`

`test_contracts.py`

`test_veteran_policy.py`

y sólo si los tres pasan, ejecutar `rata_smoke.py`. El resultado será LAB y
no modificará `monster_arc1_registry.json`.
