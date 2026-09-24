# Cambios v0.2 → v0.2.1

Fuente: auditoría externa `Informe_Test_Motor_NPC_Vivo_v0.2_GOAP_REV1.md`.

Veredicto REV1:

`V02_GOAP_REQUIERE_CORRECCIONES`

## C1 — identidad de estado

Problema:

`factsMatch()` distinguía `-0` de `0`, pero la clave JSON los colapsaba.

Corrección:

- codificación explícita de facts;
- `-0` y `0` tienen claves distintas;
- ausencia de fact también queda diferenciada.

## C2 — costes

Problemas:

- suma acumulada podía producir `Infinity`;
- costes positivos diminutos podían no aumentar el acumulado por redondeo.

Corrección:

- action.cost debe ser entero seguro positivo;
- suma acumulada debe seguir siendo entero seguro y estrictamente creciente;
- overflow no produce plan: se registra y puede terminar en `COST_OVERFLOW`.

## C3 — caminos equivalentes

Problema:

cada camino de igual coste al mismo estado se reencolaba.

Corrección:

por estado se conserva un solo representante canónico:

1. menor coste;
2. menos pasos;
3. menor plan lexicográfico.

La frontera usa heap binaria.

## C4 — facts irrelevantes

Problema:

todos los facts participaban en la clave del estado.

Corrección:

se calcula cierre de relevancia desde el goal hacia atrás por efectos/precondiciones.
La identidad de búsqueda usa sólo esos facts.

## C5 — presupuesto

Problemas:

- maxExpansions negativo aceptado;
- se podía informar una expansión más que el límite;
- SEARCH_LIMIT se confundía con NO_PLAN.

Corrección:

- maxExpansions entero >= 0;
- límite estricto;
- maxFrontier entero >= 1;
- SEARCH_LIMIT / FRONTIER_LIMIT / COST_OVERFLOW son resultados inconclusos;
- controller devuelve `PLANNING_DEFERRED` y no hace fallback.

## C6 — objetivo obsoleto

Problema:

una acción podía seguir siendo legal aunque el objetivo ya no tuviera sentido.

Corrección:

cada objetivo incorpora `relevance`.
Executor revalida goal y relevancia antes de la próxima acción.

Ejemplo:

si `HELP_PLAYER` sigue sin alcanzarse pero `playerNeedsHelp` pasa a false,
`ir_jugador` ya no se ejecuta: devuelve `REPLAN_REQUIRED`.

## C7 — stress dinámico

Se añadió `dynamic-stress.mjs` para inyectar cambios entre pasos y medir replanning.

## Fuera de alcance

No se implementan aún:

- memoria episódica;
- pathfinding de rooms;
- topología canónica;
- comunicación NPC↔NPC;
- scheduler de 32 NPC;
- save/load GOAP;
- política definitiva de starvation/cooldown narrativo.

Esos puntos pertenecen a etapas posteriores si REV2 valida el núcleo.
