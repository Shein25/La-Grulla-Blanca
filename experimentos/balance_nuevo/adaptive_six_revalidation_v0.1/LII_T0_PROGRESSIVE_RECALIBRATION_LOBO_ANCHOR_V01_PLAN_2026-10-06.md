# LII T0 Progressive Recalibration — Lobo Anchor V01

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Objetivo

Recalibrar T0 de los repetibles LianQi II:

- Sapo Ceniza
- Escarabajo de Hierro

usando como ancla inferior al **Lobo Espiritual T0 final de LianQi I**.

No se ejecuta T1/T2/T3/T4.

## Regla humana

- la nueva zona debe sentirse superior ya en T0;
- HP base de un repetible normal de la nueva etapa debe quedar ligeramente por encima del referente fuerte anterior salvo excepción de identidad explícita;
- el upper envelope debe extender esa progresión;
- no existe multiplicador universal;
- cada especie mejora sobre ejes compatibles con su identidad;
- no usar adaptación para compensar un T0 débil.

## Ancla LI

Lobo Espiritual final:
- HP 53
- PREC 100
- EVA 12
- DEF 1
- TEN 20
- BASIC `2d4+2`
- Emboscada `2d6+1`
- cadence 4

Upper envelope LI:
- HP 57
- DEF 5
- EVA 12
- PREC 100
- TEN 20
- BASIC ladder hasta `2d6` / `1d6+4` / `1d2+6`
- técnica hasta `1d4+6`

Se ejecutan dos referencias:
- `LOBO_FLOOR`
- `LOBO_HIGH`

## Equipo LII

Todos los monstruos se enfrentan contra el mismo jugador LII en:

1. `CARRY_OVER_FLOOR`
   - usa exactamente `HIGH_ROLL_STRESS[LianQi_I]`;
   - player stage sigue siendo LianQi II.

2. `EXPECTED_STAGE`
   - `EXPECTED_STAGE[LianQi_II]`.

3. `HIGH_ROLL_STRESS`
   - `HIGH_ROLL_STRESS[LianQi_II]`.

No se usa `MANDATORY_ENTRY[LianQi_II]` como piso.

## Familias Sapo

`S0_CURRENT`
- conserva perfil actual para medir el gap.

`S1_ZONE_HP`
- arregla primero progresión de vida, con cambios mínimos restantes.

`S2_BALANCED`
- mejora moderadamente supervivencia, precisión y daño básico.

`S3_PRESSURE`
- prioriza identidad de presión sostenida: precisión + ataque + Nube de Hollín.

`S4_DURABLE_PRESSURE`
- mayor HP/DEF/TEN con presión ofensiva moderada.

`S5_BURN_IDENTITY`
- conserva cuerpo moderado y concentra diferencia de zona en Nube de Hollín/quemadura.

Cada familia declara explícitamente FLOOR y HIGH envelope.

## Familias Escarabajo

`E0_CURRENT`
- referencia actual.

`E1_TANK`
- refuerza HP/DEF/TEN con ofensiva casi intacta.

`E2_BALANCED`
- tanque sostenido con precisión y basic moderadamente mejores.

`E3_PRESSURE`
- sacrifica parte del aumento defensivo para elevar precisión/basic/Carga.

`E4_HEAVY_TANK`
- máxima identidad de tanque del screen; no busca daño explosivo.

Cada familia declara FLOOR y HIGH envelope.

## Matriz

- 2 perfiles de ancla Lobo.
- 6 familias Sapo × FLOOR/HIGH.
- 5 familias Escarabajo × FLOOR/HIGH.
- 24 brazos totales.
- 3 perfiles de equipo.
- 5 raíces.
- 4 policies.
- 256 peleas/contexto.
- CRN pareado por equipo/root/policy/fight index.

Total previsto:
**368.640 combates**.

## Métricas

- win-rate diagnóstica;
- rounds;
- HP final jugador;
- Qi final/spent;
- daño directo monstruo;
- DOT monstruo;
- hit-rate monstruo;
- BASIC uses;
- technique uses;
- death pressure;
- delta pareado contra `LOBO_FLOOR` y `LOBO_HIGH`;
- carry-over floor por separado;
- root/policy spread;
- timeout/NaN/Inf.

## Lectura de progresión

No hay target universal de win-rate.

Para cada candidato se generan votos diagnósticos frente al ancla en el mismo contexto:

- menor win-rate del jugador;
- mayor presión sobre HP;
- mayor duración;
- mayor daño total del monstruo.

El notebook reporta:
- fracción de contextos con al menos 2/4 señales superiores;
- fracción con al menos 3/4;
- carry-over floor separado.

Eso NO ratifica automáticamente un ganador.

## Hard guards

- no main;
- no merge;
- no CANON write;
- no T1-T4;
- no unique;
- no Definitivas;
- no T5;
- mismo player/loadout para ancla y candidato;
- player stage siempre LII;
- CARRY_OVER_FLOOR = HIGH_ROLL_STRESS LI exacto;
- G04 Tierra: HP estructural x1.10 + HP plano de equipo;
- no target de win-rate;
- no scaling universal.

## Salida

`LII_T0_PROGRESSIVE_RECALIBRATION_LOBO_ANCHOR_V01_REVIEW.zip`

El resultado seleccionará finalistas para un gate T0 LII posterior.
No freeze automático.


## Notebook FIX1

El primer paquete omitió la dependencia local:

`experimentos/balance_nuevo/monster_new_engine_guard.py`

requerida por:

`etapa19b_combat_engine.py`.

Esto producía `ModuleNotFoundError: monster_new_engine_guard` antes de ejecutar el benchmark.

FIX1:
- incluye el guard fijado por blob SHA `0dd32a940ff1ba18501f957a95ae4b8cd115b4b9`;
- compila guard + motor;
- inserta `SOURCE_DIR` en `sys.path`;
- ejecuta import preflight real de ambos módulos antes de multiprocessing;
- no altera candidatos, matriz ni número de combates.
