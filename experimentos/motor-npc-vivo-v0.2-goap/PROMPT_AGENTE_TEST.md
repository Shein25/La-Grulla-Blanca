# Encargo para agente externo — Auditoría REV2 Motor NPC Vivo v0.2.1 GOAP

Audita exclusivamente la **cabeza actual** de:

`experiment/motor-npc-v0.2-goap`

Directorio:

`experimentos/motor-npc-vivo-v0.2-goap/`

La REV1 terminó en:

`V02_GOAP_REQUIERE_CORRECCIONES`

Esta revisión debe comprobar específicamente las correcciones v0.2.1.

NO modifiques el juego principal.
NO toques `grulla-blanca_ver73.html`.
NO uses los 32 NPC canónicos.
NO uses la topología canónica.
NO ajustes pesos ni costes.
NO hagas merge.
NO implementes funciones durante la auditoría.

## 1. Regresión oficial

Ejecuta:

```bash
node tests.mjs
```

La candidata actual contiene **40 tests declarados**.

Reporta número real PASS/FAIL y exit code. No asumas que 40 debe pasar: compruébalo.

## 2. Stress estático

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Reporta:

- objetivos elegidos;
- NO_PLANNABLE_GOAL;
- PLANNING_DEFERRED;
- errores;
- determinismo.

## 3. Stress dinámico incluido

Ejecuta al menos:

```bash
node dynamic-stress.mjs 5000 1337
node dynamic-stress.mjs 5000 42
node dynamic-stress.mjs 5000 20260923
```

Verifica:

- GOAL_REACHED;
- REPLAN_REQUIRED;
- replans exitosos;
- cambios de objetivo;
- PLANNING_DEFERRED;
- NO_PLANNABLE_GOAL;
- estados repetidos;
- STEP_LIMIT;
- movimientos inútiles después de objetivo obsoleto.

Debe haber **0 movimientos ejecutados después de que la relevancia del objetivo ya sea falsa**.

## 4. Regresión exacta de -0 / 0

Reproduce:

```js
planGOAP(
  { x: -0 },
  { x: 0 },
  [{ id:'set_zero', cost:1, preconditions:{}, effects:{x:0} }]
)
```

Debe devolver:

- PLAN_FOUND;
- plan `['set_zero']`;
- coste 1.

Prueba también que la identidad siga siendo determinista para:

- null;
- false/true;
- strings;
- números finitos normales;
- facts ausentes vs presentes.

La equivalencia de `factsMatch()` y la de la clave de estado no deben contradecirse.

## 5. Costes

Comprueba que `action.cost` sólo acepta **enteros seguros > 0**.

Deben rechazarse:

- 0;
- negativos;
- fracciones;
- Number.MIN_VALUE;
- NaN;
- Infinity;
- -Infinity;
- 1e308.

Prueba acumulación con:

```text
stage1 cost = Number.MAX_SAFE_INTEGER
stage2 cost = 1
```

No debe salir `Infinity`.

Resultado esperado si no existe otra ruta:

`COST_OVERFLOW`

Busca cualquier caso que consiga producir coste no finito o coste acumulado que no aumente.

## 6. Optimalidad contra oráculo independiente

Vuelve a comparar contra búsqueda exhaustiva/brute force en grafos pequeños reproducibles.

Incluye:

- 2–6 nodos;
- ciclos;
- no-ops;
- rutas de mismo coste;
- distinto número de pasos;
- reordenamiento de acciones;
- retornos a estados anteriores.

Comprueba:

1. existencia de plan;
2. coste mínimo;
3. número de pasos usado como segundo desempate;
4. plan lexicográfico como tercer desempate;
5. determinismo.

Reporta discrepancias exactas si existen.

## 7. Poda de caminos equivalentes

Reproduce un grafo de **12 etapas** con dos acciones equivalentes por etapa.

La REV1 producía explosión exponencial.

Ahora debe:

- encontrar plan de coste 12;
- no necesitar cientos/miles de expansiones;
- no devolver SEARCH_LIMIT con presupuesto 100.

Reporta:

- expansions;
- generated;
- maxFrontier.

Prueba además objetivo imposible con varias rutas equivalentes.

## 8. Facts irrelevantes

Construye estados con muchos flags que ninguna cadena causal hacia el goal utiliza.

Confirma que:

- no multiplican la identidad de búsqueda;
- `relevantFacts` no los incluye;
- el plan y coste no cambian al añadir/quitar esos flags;
- el número de expansiones permanece esencialmente ligado a los facts relevantes.

Intenta encontrar una poda incorrecta donde se elimine un fact que sí era necesario para una precondición futura.

## 9. maxExpansions y maxFrontier

Prueba:

- maxExpansions = -1 → rechazo;
- maxExpansions = 0 → SEARCH_LIMIT con expansions 0;
- maxExpansions = 1 en plan directo de un paso → debe poder encontrarlo con 1 expansión;
- maxFrontier = 0 → rechazo;
- frontera insuficiente → FRONTIER_LIMIT;
- nunca informar expansions > maxExpansions;
- nunca informar maxFrontier observado > límite configurado.

## 10. NO_PLAN vs búsqueda inconclusa

Éste es un criterio crítico.

Con Leal en `WORLDS.comun` y presupuesto insuficiente para HELP_PLAYER:

- el controller NO debe saltar a FULFILL_DUTY;
- debe conservar HELP_PLAYER como objetivo prioritario;
- debe devolver `PLANNING_DEFERRED`.

Comprueba lo mismo para:

- SEARCH_LIMIT;
- FRONTIER_LIMIT;
- COST_OVERFLOW cuando pueda construirse un caso aplicable.

En cambio, si HELP_PLAYER recibe un `NO_PLAN` demostrado, el fallback al siguiente objetivo debe seguir funcionando.

## 11. Vigencia del objetivo

Prueba específicamente:

### HELP_PLAYER

Plan inicial:

`ir_jugador → ayudar_jugador`

Antes del primer paso cambia:

`playerNeedsHelp=false`

Aunque `ir_jugador` siga siendo físicamente aplicable, Executor debe:

- NO ejecutarlo;
- devolver REPLAN_REQUIRED;
- marcar el objetivo como obsoleto;
- no modificar la posición.

Prueba equivalentes para:

- anomalyPresent=false;
- dutyPending=false;
- hasEvidence=false.

Confirma que si el goal ya está cumplido se devuelve GOAL_REACHED antes de considerar obsolescencia.

## 12. Replanning

Repite los casos REV1:

- paso cerrado;
- superior desaparece;
- cambio de posición;
- jugador deja de necesitar ayuda;
- deber retirado;
- anomalía desaparece.

Comprueba que ningún efecto se aplique cuando una acción o goal ya no sea válido.

Después vuelve a llamar al controller y verifica alternativa, cambio de objetivo o PLANNING_DEFERRED según corresponda.

## 13. Executor

Revisa:

- plan vacío;
- goal ya satisfecho;
- goal obsoleto;
- acción inexistente;
- precondición obsoleta;
- maxSteps 0;
- maxSteps negativo;
- efectos exactamente una vez;
- no mutación del input;
- STEP_LIMIT;
- GOAL_REACHED sólo con hechos realmente satisfechos.

## 14. State explosion y rendimiento

Construye casos adversariales con:

- caminos equivalentes;
- flags irrelevantes;
- objetivos imposibles;
- 32 NPC ficticios planificando repetidamente.

Compara con REV1 si es posible.

Reporta:

- expansions;
- generated;
- maxFrontier;
- tiempo aproximado;
- cualquier caso donde un grafo pequeño aún consuma presupuesto excesivo.

## 15. Personalidades — no regresión

En `WORLDS.comun` debe mantenerse:

- Disciplinado → FULFILL_DUTY
- Leal → HELP_PLAYER
- Curioso → INVESTIGATE_ANOMALY

No ajustes pesos.

Repite algún barrido de urgency/danger/dutyImportance para confirmar determinismo.

## 16. Arquitectura

Confirma que sigue separada:

```text
Utility AI → objetivo
GOAP       → plan lógico
Executor   → ejecución/verificación
```

GOAP no debe hacer pathfinding de rooms.

En producción futura una acción lógica como `ir_superior` deberá delegar movimiento a la capa física de las 329 salas y gates.

## 17. Riesgos pendientes

Distingue entre:

- bugs que bloquean v0.2.1;
- optimizaciones futuras;
- funciones deliberadamente pospuestas a memoria/scheduler/NPC↔NPC.

No exijas implementar memoria, pathfinding canónico ni scheduling completo en esta revisión.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.2.1_GOAP_REV2.md`

Termina exactamente con uno:

`V021_GOAP_APTO_PARA_ITERAR`

`V021_GOAP_REQUIERE_CORRECCIONES`

`V021_GOAP_FALLO_CONCEPTUAL`
