# Encargo para agente externo — Auditoría REV3 Motor NPC Vivo v0.2.2 GOAP

Audita exclusivamente la **cabeza actual** de:

`experiment/motor-npc-v0.2-goap`

Directorio:

`experimentos/goap/motor-npc-vivo-v0.2-goap/`

PR:

`#2`

La REV2 terminó en:

`V021_GOAP_REQUIERE_CORRECCIONES`

REV2 confirmó el núcleo de v0.2.1 y encontró dos defectos localizados:

1. relevancia del objetivo opcional en Executor;
2. desempate lexicográfico basado en JSON serializado.

v0.2.2 sólo pretende corregir esos dos defectos y añadir regresiones.

NO modifiques el repositorio.
NO modifiques producción.
NO uses NPC canónicos ni topología canónica.
NO ajustes pesos.
NO ajustes costes.
NO hagas merge.
NO implementes funciones durante la auditoría.

## 1. Verificación de revisión

Antes de probar:

- reporta HEAD local;
- reporta HEAD remoto;
- confirma que coinciden;
- lee `CAMBIOS_v0.2.2.md`;
- lee este prompt completo.

## 2. Suite oficial

Ejecuta:

```bash
node tests.mjs
```

La candidata declara **47 tests**.

Reporta:

- PASS reales;
- FAIL reales;
- exit code.

## 3. Stress estático

Ejecuta:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Confirma ausencia de regresiones respecto de REV2.

## 4. Stress dinámico

Ejecuta:

```bash
node dynamic-stress.mjs 5000 1337
node dynamic-stress.mjs 5000 42
node dynamic-stress.mjs 5000 20260923
```

IMPORTANTE:

`dynamic-stress.mjs` ya no debe pasar `selectedGoal.relevance` como argumento separado a `executeNext`.

Verifica que la protección contra objetivos obsoletos provenga del plan vinculado.

Debe haber:

```text
movimientos inútiles tras obsolescencia = 0
```

## 5. Hallazgo REV2 #1 — relevancia inseparable

Caso obligatorio:

```text
NPC: Leal
mundo: WORLDS.crisis_jugador
objetivo: HELP_PLAYER
plan: ir_jugador → ayudar_jugador
```

Después de planificar:

```js
const changed={...WORLDS.crisis_jugador,playerNeedsHelp:false};
```

Llama exactamente:

```js
executeNext(
  decision.plan,
  changed,
  decision.selectedGoal.goal,
  GOAP_ACTIONS
)
```

NO pases un quinto argumento.

Debe devolver:

- `REPLAN_REQUIRED`;
- `goalObsolete === true`;
- `executed === null`;
- posición sin cambio.

Repite con:

```js
executeWholePlan(
  decision.plan,
  changed,
  decision.selectedGoal.goal,
  GOAP_ACTIONS,
  30
)
```

sin sexto argumento.

El primer paso NO debe ejecutar `ir_jugador`.

## 6. Contrato del plan ejecutable

Confirma que un `PLAN_READY` producido por controller contiene:

- `plan.goal`;
- `plan.relevance`;
- `plan.goalId`.

Deben coincidir con `selectedGoal`.

Prueba también:

### Plan no vinculado

Un objeto manual:

```js
{status:'PLAN_FOUND', plan:['ir_jugador']}
```

sin relevancia explícita debe rechazarse **antes de aplicar efectos**.

### Contradicción explícita

Si el plan vinculado lleva una relevancia y el caller pasa otra distinta, debe rechazarse y no ejecutar efectos.

Haz lo mismo con un goal explícito contradictorio.

### Goal ya alcanzado

Si el goal vinculado ya está satisfecho, debe seguir devolviendo `GOAL_REACHED` sin ejecutar nada.

## 7. Hallazgo REV2 #2 — desempate `a` / `a!`

Reproduce exactamente:

```js
planGOAP(
  {x:0},
  {x:1},
  [
    {id:'a!',cost:1,preconditions:{x:0},effects:{x:1}},
    {id:'a', cost:1,preconditions:{x:0},effects:{x:1}},
  ]
)
```

Debe elegir:

```js
['a']
```

Invierte el array de acciones y debe seguir eligiendo `['a']`.

## 8. Desempate secuencial independiente

Construye casos de igual:

- coste;
- número de pasos;

con IDs de:

- distinta longitud;
- prefijos;
- puntuación;
- dígitos;
- mayúsculas/minúsculas;
- Unicode simple si lo consideras razonable dentro del dominio de strings aceptado.

Compara contra un oráculo independiente que ordene **secuencias de IDs**, no JSON serializado.

Criterio esperado:

```text
coste
→ pasos
→ secuencia lexicográfica de IDs
```

La comparación debe ser determinista al reordenar el array de acciones.

Reporta cualquier discrepancia y el par mínimo que la reproduzca.

## 9. Regresión del planner

Repite al menos una muestra sustancial de las pruebas independientes de REV2:

- `-0` vs `0`;
- costes inválidos;
- COST_OVERFLOW;
- 12 etapas con caminos equivalentes;
- facts irrelevantes;
- maxExpansions;
- maxFrontier;
- SEARCH_LIMIT;
- FRONTIER_LIMIT;
- NO_PLAN vs PLANNING_DEFERRED;
- brute force de grafos pequeños.

No hace falta aumentar alcance si no hay regresión.

## 10. Replanning

Con plan vinculado y sin pasar relevancia por separado, prueba:

- jugador deja de necesitar ayuda;
- deber desaparece;
- anomalía desaparece;
- evidencia desaparece;
- paso se cierra;
- superior desaparece;
- posición cambia.

Ningún objetivo obsoleto debe provocar un paso inútil antes del replan.

## 11. Executor

Confirma:

- no mutación del mundo de entrada;
- efectos una sola vez;
- plan vacío;
- acción inexistente;
- precondición obsoleta;
- maxSteps 0;
- maxSteps negativo;
- STEP_LIMIT;
- GOAL_REACHED sólo con goal satisfecho;
- ausencia del contrato de relevancia no puede degradarse silenciosamente a `{}`.

## 12. Personalidades y arquitectura

Sin cambios esperados:

```text
Disciplinado → FULFILL_DUTY
Leal         → HELP_PLAYER
Curioso      → INVESTIGATE_ANOMALY
```

Confirma que sigue separada:

```text
Utility AI → objetivo
GOAP       → plan lógico
Executor   → ejecución/verificación
```

GOAP no debe realizar pathfinding de rooms.

## 13. Rendimiento

Repite la prueba conceptual de 32 NPC ficticios y algunos casos adversariales.

No se busca optimización nueva; sólo detectar regresiones provocadas por v0.2.2.

## 14. Alcance

No exijas todavía:

- memoria episódica;
- scheduler real;
- NPC↔NPC;
- topología canónica;
- pathfinding real;
- save/load definitivo del motor experimental.

Distingue bugs bloqueantes de trabajo futuro.

## Identificación obligatoria del agente auditor

El informe debe identificar claramente quién realizó la auditoría.

La cabecera debe incluir:

- **Agente auditor:** Claude / Gemini / ChatGPT / Codex / otro;
- **Modelo o versión:** si se conoce;
- **Fecha**;
- **Rama auditada**;
- **HEAD exacto auditado**;
- **Tipo de revisión:** externa / independiente.

El nombre del archivo debe incluir el agente auditor, por ejemplo:

`Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_CLAUDE.md`

`Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_GEMINI.md`

Si se usa otro agente, reemplaza el sufijo por un identificador claro y estable.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_<AGENTE>.md`

Termina exactamente con uno:

`V022_GOAP_APTO_PARA_ITERAR`

`V022_GOAP_REQUIERE_CORRECCIONES`

`V022_GOAP_FALLO_CONCEPTUAL`
