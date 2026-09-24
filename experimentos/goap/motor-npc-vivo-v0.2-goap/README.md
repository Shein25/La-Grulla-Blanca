# Motor NPC Vivo v0.2.2 — Laboratorio GOAP

Iteración correctiva posterior a la auditoría externa REV2.

## Estado

**CERRADA Y MERGEADA COMO SNAPSHOT EXPERIMENTAL.**

PR #2 fue mergeada el 2026-09-24.

Merge commit:

`5812deb59cd1c133383b9af973486a702a26daf4`

Esto no implica integración de GOAP en producción.

La arquitectura sigue separada:

```text
Utility AI → OBJETIVO
GOAP       → PLAN lógico
Executor   → ejecución / verificación
```

La REV2 confirmó que las correcciones principales de v0.2.1 funcionan, pero encontró dos defectos localizados:

1. la relevancia del objetivo podía omitirse al llamar al Executor;
2. el tercer desempate usaba la serialización JSON del plan y no la secuencia real de IDs.

v0.2.2 corrige ambos puntos sin tocar producción.

## Aislamiento

- laboratorio experimental independiente;
- no usa los 32 NPC canónicos;
- no usa topología canónica;
- no implementa misiones;
- no modifica el baseline de producción;
- GOAP no hace pathfinding de las 329 salas.

## Correcciones v0.2.2

### Relevancia vinculada al plan ejecutable

Cuando `controller.mjs` obtiene `PLAN_FOUND`, el plan que expone incorpora:

```js
{
  ...plan,
  goal,
  relevance,
  goalId
}
```

El Executor usa primero ese contrato vinculado.

Por tanto, esta llamada es segura:

```js
executeNext(decision.plan, world, decision.selectedGoal.goal, GOAP_ACTIONS)
```

aunque no se pase un quinto argumento de relevancia.

Si un plan construido fuera del controller no contiene relevancia vinculada, el Executor exige que se suministre explícitamente y rechaza la ejecución antes de aplicar efectos si falta.

Si se suministra un goal o una relevancia explícitos que contradicen el contrato vinculado, también se rechaza.

### Desempate lexicográfico real

El criterio del planner queda definido como:

```text
1. menor coste total
2. menor cantidad de pasos
3. secuencia lexicográficamente menor de IDs
```

La tercera comparación ya no usa `JSON.stringify(plan)`.

Ahora compara cada ID de la secuencia directamente, con orden de cadenas por unidades UTF-16 de JavaScript y prefijo corto antes que su extensión.

Caso de regresión obligatorio:

```text
a
a!
```

Con igual coste y un paso debe ganar:

```text
a
```

## Lo que v0.2.1 ya había corregido y debe conservarse

- identidad coherente `-0` / `0`;
- costes enteros seguros > 0;
- `COST_OVERFLOW`;
- poda canónica por estado;
- facts causalmente relevantes;
- heap binaria;
- `maxExpansions` estricto;
- `maxFrontier`;
- `SEARCH_LIMIT` / `FRONTIER_LIMIT` distintos de `NO_PLAN`;
- `PLANNING_DEFERRED`;
- vigencia de objetivos;
- stress dinámico.

## Suite

La candidata v0.2.2 contiene **47 tests declarados**.

El stress dinámico ahora llama al Executor **sin pasar relevancia por separado**, de modo que prueba realmente que la relevancia viaje vinculada al plan.

La aprobación efectiva corresponde a la auditoría externa REV3.

## Límites deliberados

Siguen fuera de esta etapa:

- topología física real;
- pathfinding de rooms;
- gates canónicos;
- memoria episódica;
- relaciones NPC↔NPC;
- propagación de conocimiento;
- scheduler real de 32 NPC;
- save/load de GOAP;
- efectos probabilísticos.

## Cierre

REV3 Agente A, REV3 Gemini y auditoría independiente concluyeron que v0.2.2 es apta para iterar.

Resultado de cierre:

`V022_GOAP_APTO_PARA_ITERAR`

La línea GOAP v0.2.2 queda congelada. El siguiente laboratorio se desarrolla en una rama separada.
