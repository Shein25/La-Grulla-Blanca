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
