# Cambios v0.2.1 → v0.2.2

Fuente: auditoría externa `Informe_Test_Motor_NPC_Vivo_v0.2.1_GOAP_REV2.md`.

Veredicto REV2:

`V021_GOAP_REQUIERE_CORRECCIONES`

## Hallazgo 1 — relevancia opcional

Problema:

`executeNext(..., relevance={})` y `executeWholePlan(..., relevance={})` permitían omitir relevancia. Un plan HELP_PLAYER podía ejecutar `ir_jugador` aunque `playerNeedsHelp` ya fuera false.

Corrección:

- el controller vincula `goal`, `relevance` y `goalId` al plan ejecutable;
- Executor usa el contrato vinculado;
- si un plan no vinculado no trae relevancia y tampoco se pasa explícitamente, se rechaza antes de efectos;
- goal/relevance explícitos contradictorios con el plan vinculado se rechazan;
- el stress dinámico omite deliberadamente el argumento de relevancia para validar la vinculación real.

## Hallazgo 2 — tercer desempate

Problema:

`JSON.stringify(plan).localeCompare(...)` no representa el orden lexicográfico de la secuencia de IDs. Con `a` y `a!`, el planner podía elegir `a!`.

Corrección:

- comparación directa ID por ID;
- orden de cadenas por comparación relacional de JavaScript;
- si todos los IDs comparados son iguales, el prefijo más corto precede;
- el criterio queda: coste → pasos → secuencia de IDs.

## Regresiones añadidas

- caso directo `a` vs `a!`;
- caso multistep con puntuación/longitudes distintas;
- plan del controller contiene goal/relevance;
- omitir relevancia en executeNext sigue detectando obsolescencia;
- omitir relevancia en executeWholePlan sigue detectando obsolescencia antes del primer efecto;
- plan no vinculado sin relevancia se rechaza;
- contrato vinculado rechaza relevancia explícita contradictoria.

La suite pasa de 40 a **47 tests declarados**.

## Fuera de alcance

Sin cambios en:

- pesos;
- costes del dominio experimental;
- NPC canónicos;
- topología real;
- producción;
- memoria;
- scheduler;
- NPC↔NPC;
- pathfinding.
