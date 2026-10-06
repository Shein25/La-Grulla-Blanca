# LI — T2 Recognition Micro-screen V01

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Autoridad

- T0: T0_LI_EXHAUSTIVE_PASS_2026-10-06.
- T1: T1_LI_FINAL_FREEZE_2026-10-06.
- Variabilidad + Mutantes + sufijos: MUTANT_SUFFIX_SYSTEM_FROZEN_FOR_T2_LAB.
- Modelo adaptativo: T2 = RECONOCIMIENTO / memoria persistente / anticipación elegible.
- No existe escalado universal de HP/daño/DEF/EVA/PREC por tier.

## Rebase de la Rata

La Rata histórica cerró R2_SHORT:
- memory_window = 2;
- repeat = 2;
- count_results = EFECTIVA.

Se conserva esa arquitectura como prior estructural.

NO se transplanta su viejo +8 sobre el T1 +40/CD5 porque ese T1 quedó obsoleto.
El T1 actual de Rata es +70/CD6.

## Hipótesis T2 V01

Para las cinco especies:

1. observar únicamente la categoría real ejecutada por el jugador:
   - PLAYER_BASIC;
   - PLAYER_UNITARGET_TECHNIQUE;
   - PLAYER_AOE_TECHNIQUE;
   - PLAYER_DEFENSIVE_TECHNIQUE;
2. contar sólo acciones EFECTIVAS;
3. reconocer dos acciones consecutivas de la misma categoría;
4. si hay reconocimiento y la supervivencia T1 está disponible, hacer elegible anticipatoriamente la MISMA habilidad T1;
5. la acción T1 mantiene magnitud, cargas y cooldown congelados y consume el turno igual que en T1;
6. no crear habilidad ofensiva T2, stat boost, cooldown nuevo, reloj nuevo ni inspección de root/build.

Este modo se denomina:
T2_R2_SHORT_PREEMPTIVE_V01

Es una hipótesis LAB para Serpiente/Avispa/Mono/Lobo y un rebase mecánico para Rata.

## Matriz

- 5 especies LI.
- 5 raíces.
- 4 policies engine-native:
  UNITARGET_FIRST / AOE_FIRST / DEFENSE_OPEN / ROTATION.
- EXPECTED_STAGE + HIGH_ROLL_STRESS.
- arms pareados:
  T1_FROZEN / T2_R2_SHORT_PREEMPTIVE_V01.
- poblaciones por especie:
  64 NATURAL;
  16 SPECIALIZED_MUTANT;
  8 EXCEPCIONAL;
  4 ASCENDIDO.
- CRN pareado T1/T2.
- Mutantes/sufijos se resuelven desde q_axis antes del tier.

Aproximación: 36.800 combates.

## Métricas

- recognition_trigger_rate;
- prediction_accuracy / false_positive_rate;
- survival_procs;
- preemptive_survival_procs;
- rounds / win-rate diagnóstico;
- HP final / Qi gastado;
- daño directo / DOT / Qi drain;
- evades / DEF prevented / absorption;
- split NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO;
- root/policy/profile spread;
- timeouts / NaN/Inf.

## Criterio

No hay target universal de win-rate.

El micro-screen pregunta:
- ¿la memoria se expresa?
- ¿la anticipación cambia combate de forma perceptible?
- ¿se mantiene identidad?
- ¿hay sobre-reacción con ciertas policies?
- ¿Mutantes/Excepcionales/Ascendidos siguen siendo mecánicamente estables?
- ¿alguna especie necesita focal propio?

Rata no se reabre numéricamente salvo evidencia de incompatibilidad con el T1 actual.

## Backend

Google Colab únicamente para V01:
- rutas relativas o /content/...;
- 2 workers automáticos en el backend actual;
- barra de progreso por especie;
- CPU/RAM/ETA visibles;
- checkpoint por especie;
- reanudación;
- prohibidas rutas /kaggle/....

No main. No merge. No runtime canónico. Definitivas prohibidas.


## Paquete Colab preparado

Artefacto:
`COLAB_LI_MONSTER_T2_RECOGNITION_MICROSCREEN_V01.zip`

- ZIP SHA-256: `c0a0bb566f71ba8cfd5cde169f88ac9531cf49c830ba8207371928d25858df5d`
- Notebook SHA-256: `b4b5e518ba3120499a7e1910a2ee948b18f30e7fff9e736568aac6aff2cee7e5`
- Runner SHA-256: `35517815d6ff9e2fa70b5424ba72e4ffc535d78fd4867bf59bd44b5a6e85df30`
- Notebook válido: nbformat 4.
- 0 rutas Kaggle en el notebook.
- backend: Google Colab;
- workers: detección automática de todos los CPU lógicos disponibles;
- checkpoints parciales + completos por especie;
- barra de progreso con CPU/RAM/peleas por segundo;
- matriz representada: 36.800 combates.

El paquete es un micro-screen diagnóstico y no ratifica T2 automáticamente.


## Colab V01R1 — hotfix de infraestructura

Durante la primera ejecución V01 en Google Colab, `ProcessPoolExecutor` falló al inicializar workers con:

```text
ModuleNotFoundError: No module named 'monster_new_engine_guard'
BrokenProcessPool
```

Causa:
- `etapa19b_combat_engine.py` importa directamente `monster_new_engine_guard`;
- el notebook V01 descargaba el motor pero omitía ese archivo de `SOURCE_SPECS`;
- `worker_init()` sí añadía `sources/` a `sys.path`, por lo que el fallo no era de path sino de dependencia ausente.

R1 corrige exclusivamente infraestructura:
- añade `monster_new_engine_guard.py` fijado al blob `0dd32a940ff1ba18501f957a95ae4b8cd115b4b9`;
- compila e importa guard + motor en el proceso principal;
- cada worker valida la existencia de ambos archivos e invalida caché de imports;
- añade preflight real de `ProcessPoolExecutor` antes de generar los pools de individuos;
- mantiene exactamente las mismas seeds, CRN, tamaños de pool, T1, hipótesis T2, roots, policies y perfiles.

Artefacto:
`COLAB_LI_MONSTER_T2_RECOGNITION_MICROSCREEN_V01R1.zip`

SHA-256:
- notebook: `c5be2d7b044f888dfce97b3daa49b2a0a2adb170bc810d1732cdab4a2212f0dd`;
- runner: `b59005e2981916f0062c6aecf30637fbb5c0cdbaeebc1b01b7ef89d1e2d12ec7`;
- ZIP: `23510d7e406ec42fc41583e92afdd6a832d4f9a5f6cddd0fa0ece3d972658001`.

Backend guard:
- nbformat 4 válido;
- 0 rutas `/kaggle/`;
- Colab usa `/content/...`.
