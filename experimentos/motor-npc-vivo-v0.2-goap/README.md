# Motor NPC Vivo v0.2.1 — Laboratorio GOAP

Iteración correctiva de la primera candidata v0.2, basada en la auditoría externa REV1.

## Estado

**No mergear todavía.**

La REV1 validó la arquitectura general:

```text
Utility AI → OBJETIVO
GOAP       → PLAN
Executor   → ejecución / verificación
```

pero encontró problemas en identidad de estados, dominio numérico de costes, poda de caminos equivalentes, presupuesto de búsqueda y vigencia de objetivos.

v0.2.1 corrige esos puntos sin tocar producción.

## Aislamiento

- no se importa desde `grulla-blanca_ver73.html`;
- no usa los 32 NPC canónicos;
- no usa topología canónica;
- no implementa misiones;
- no modifica el baseline del Arco 1;
- no convierte GOAP en pathfinding de las 329 salas.

Los tres NPC siguen siendo fixtures ficticios heredados de v0.1.1.

## Cambios principales de v0.2.1

### 1. Identidad de estados coherente

`factsMatch()` usa `Object.is()`.

La clave interna del planner ahora conserva explícitamente la diferencia entre:

```text
-0
0
```

y distingue facts ausentes de facts presentes.

### 2. Costes discretos seguros

Los costes GOAP se restringen a:

```text
entero seguro > 0
```

Esto elimina costes diminutos que se redondean a cero y costes gigantes no representables con seguridad.

El coste acumulado también se controla. Si desborda el rango de entero seguro, el planner no devuelve `Infinity`: produce `COST_OVERFLOW`.

### 3. Poda canónica por estado

Para cada estado relevante sólo se conserva el mejor representante según:

```text
coste
  ↓ empate
número de pasos
  ↓ empate
plan lexicográfico
```

Ya no se reencolan automáticamente todas las rutas de igual coste al mismo estado.

### 4. Sólo facts relevantes para la identidad de búsqueda

El planner calcula hacia atrás qué facts pueden influir en el objetivo a través de:

```text
goal
  ← effects
  ← preconditions
  ← effects anteriores
  ...
```

Flags que no pueden afectar ese objetivo no multiplican la identidad de estados.

El estado completo se conserva para aplicar efectos; la clave de búsqueda usa sólo facts relevantes.

### 5. Frontera con heap

La frontera ya no ordena un array completo en cada expansión.

Se usa una cola de prioridad binaria y se informan:

- `expansions`;
- `generated`;
- `maxFrontier`;
- `relevantFacts`.

También existe `maxFrontier`.

### 6. Presupuesto estricto

`maxExpansions` debe ser entero >= 0.

Un presupuesto 0 realiza exactamente 0 expansiones.

El planner puede devolver:

- `PLAN_FOUND`;
- `NO_PLAN`;
- `SEARCH_LIMIT`;
- `FRONTIER_LIMIT`;
- `COST_OVERFLOW`.

### 7. Búsqueda inconclusa no significa objetivo imposible

El controller sólo hace fallback a otro objetivo cuando recibe:

`NO_PLAN`

Si recibe:

- `SEARCH_LIMIT`;
- `FRONTIER_LIMIT`;
- `COST_OVERFLOW`;

devuelve:

`PLANNING_DEFERRED`

y conserva el objetivo prioritario.

### 8. Vigencia del objetivo

Cada objetivo experimental tiene ahora condiciones de relevancia.

Ejemplo:

```text
HELP_PLAYER

goal:
playerHelped = true

relevancia:
playerPresent = true
playerNeedsHelp = true
playerHelped = false
```

Antes de cada paso, Executor comprueba:

1. si el goal ya fue alcanzado;
2. si el objetivo sigue siendo relevante;
3. si la acción siguiente sigue cumpliendo precondiciones.

Si la relevancia desapareció:

`REPLAN_REQUIRED`

sin ejecutar el movimiento anterior.

### 9. Stress dinámico incluido

Se añadió:

`dynamic-stress.mjs`

Introduce eventos entre pasos y mide:

- GOAL_REACHED;
- REPLAN_REQUIRED;
- replans;
- cambios de objetivo;
- búsquedas diferidas;
- estados repetidos;
- STEP_LIMIT;
- movimientos inútiles después de objetivo obsoleto.

## Suite

La candidata actual contiene **40 tests declarados**.

El resultado efectivo de esta revisión debe obtenerlo la auditoría externa REV2; no se considera aprobada hasta entonces.

## Límites que siguen siendo deliberados

- sin topología real;
- sin pathfinding físico;
- sin gates canónicos;
- sin memoria episódica;
- sin relaciones NPC↔NPC;
- sin comunicación de conocimiento;
- sin reservas de recursos compartidos;
- sin scheduling real de 32 NPC;
- sin save/load de GOAP;
- sin efectos probabilísticos.

## Próximo paso

Ejecutar la auditoría externa REV2 definida en `PROMPT_AGENTE_TEST.md`.

No mergear PR #2 hasta revisar ese informe.
