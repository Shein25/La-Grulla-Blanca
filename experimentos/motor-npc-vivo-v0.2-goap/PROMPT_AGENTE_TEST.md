# Encargo para agente externo — Auditoría Motor NPC Vivo v0.2 GOAP

Audita exclusivamente la cabeza actual de:

`experiment/motor-npc-v0.2-goap`

Directorio:

`experimentos/motor-npc-vivo-v0.2-goap/`

La v0.1.1 ya está congelada y sólo se usa aquí para fixtures ficticios.

NO modifiques el juego principal.
NO toques `grulla-blanca_ver73.html`.
NO conviertas estos datos en canon.
NO ajustes pesos o costes durante la auditoría.
NO hagas merge.

## 1. Regresión oficial

Ejecuta:

```bash
node tests.mjs
```

La candidata inicial espera **25 PASS**.

## 2. Stress

Ejecuta al menos:

```bash
node stress.mjs 10000 1337
node stress.mjs 10000 1
node stress.mjs 10000 42
node stress.mjs 10000 999
node stress.mjs 10000 20260923
```

Reporta distribución de objetivos, NO_PLANNABLE_GOAL, errores y determinismo.

## 3. Separación arquitectónica

Verifica que:

- Utility AI selecciona un OBJETIVO, no un plan;
- GOAP no recalcula personalidad;
- GOAP recibe hechos, objetivo y acciones;
- Executor no selecciona objetivos;
- Executor sólo ejecuta/verifica;
- replanning se solicita cuando una precondición deja de cumplirse.

Marca cualquier mezcla de responsabilidades.

## 4. Optimalidad del planner

Construye grafos pequeños donde:

- la primera acción que alcanza el objetivo sea más cara que una ruta posterior;
- haya dos rutas con distinto número de pasos y distinto coste;
- haya dos planes con mismo coste;
- haya ciclos;
- haya una acción que no cambie el estado;
- haya acciones que vuelvan a estados ya visitados.

Comprueba que el plan devuelto tenga coste mínimo.

Para grafos pequeños, compara contra una búsqueda exhaustiva/brute force independiente.

## 5. Determinismo

Repite exactamente los mismos inputs muchas veces.

El mismo estado + goal + actions debe producir:

- mismo status;
- mismo plan;
- mismo coste;
- mismo desempate.

Prueba especialmente planes con coste idéntico.

## 6. Replanning

Prueba planes que queden obsoletos entre pasos:

- se cierra un paso;
- desaparece el superior;
- el jugador deja de necesitar ayuda;
- cambia la posición;
- desaparece una precondición cualquiera.

El Executor debe:

- no ejecutar una acción cuyas precondiciones ya no se cumplen;
- devolver REPLAN_REQUIRED cuando corresponda;
- conservar el mundo sin aplicar los efectos de la acción fallida.

Después llama de nuevo al controller y verifica que:

- encuentre una alternativa si existe;
- pruebe el siguiente objetivo si el objetivo prioritario ya no es planificable.

## 7. Fallback de objetivos

Construye situaciones donde el objetivo Utility #1 sea imposible.

El controller debe probar objetivos disponibles posteriores, sin alterar sus scores para forzar un resultado.

Revisa si este comportamiento puede producir decisiones absurdas o starvation.

## 8. Executor

Audita:

- plan vacío;
- objetivo ya satisfecho;
- acción inexistente;
- stale plan;
- maxSteps;
- no mutación del mundo de entrada;
- efectos aplicados exactamente una vez;
- goal alcanzado sólo si los hechos realmente lo satisfacen.

## 9. Robustez del planner

Prueba entradas inválidas:

- cost 0;
- cost negativo;
- NaN / Infinity;
- action IDs duplicados;
- facts no primitivos;
- arrays donde se espera objeto;
- acciones vacías;
- maxExpansions pequeño.

Busca estados que causen explosión de búsqueda o cola excesiva.

Reporta número de expansiones en escenarios relevantes.

## 10. Personalidades

En el mismo mundo base confirma:

- Disciplinado → FULFILL_DUTY
- Leal → HELP_PLAYER
- Curioso → INVESTIGATE_ANOMALY

Después barre urgency, danger y dutyImportance 0..100 y comprueba si las transiciones de objetivos son razonables y deterministas.

No exijas distribución uniforme.

## 11. Costes

Verifica:

- paso abierto: REPORT_SUPERIOR debe preferir ir_superior + informar_superior (coste 2);
- paso cerrado con mensajero: enviar_mensajero (coste 4);
- cambios de coste alteran el plan por coste total, no por orden del array.

Busca dependencia accidental del orden original de GOAP_ACTIONS.

## 12. Stress con cambios durante ejecución

El stress incluido genera mundos estáticos durante cada plan.

Crea un stress adicional que, entre pasos y con seed reproducible, cambie ocasionalmente una precondición.

Mide:

- GOAL_REACHED;
- REPLAN_REQUIRED;
- replans exitosos;
- objetivos abandonados;
- loops;
- STEP_LIMIT.

## 13. Escalabilidad conceptual

Evalúa si el diseño puede crecer a 32 NPC sin compartir planner state accidentalmente.

Revisa especialmente:

- estados independientes por NPC;
- planner sin mutaciones globales;
- actions declarativas reutilizables;
- riesgo de coste CPU si muchos NPC planifican en el mismo turno;
- necesidad futura de presupuestos de planning / scheduling.

## 14. Riesgos de diseño

Busca específicamente:

- state explosion;
- objetivos imposibles que consuman demasiadas expansiones;
- planes válidos pero semánticamente absurdos;
- hechos irrelevantes que multipliquen estados;
- efectos contradictorios;
- acciones dominantes;
- loops de replanning;
- starvation de objetivos de baja utilidad;
- planner usado como sustituto de pathfinding físico.

GOAP no debe reemplazar el pathfinding de las 329 salas; en una integración futura una acción de movimiento debería delegar la ruta física al sistema de movilidad.

## Entregable

Devuelve únicamente:

`Informe_Test_Motor_NPC_Vivo_v0.2_GOAP_REV1.md`

Incluye:

- entorno;
- commit auditado;
- comandos;
- resultados;
- bugs reproducibles;
- optimalidad;
- determinismo;
- replanning;
- stress dinámico;
- escalabilidad;
- riesgos;
- recomendaciones v0.2.1 si correspondiera.

Termina exactamente con uno:

`V02_GOAP_APTO_PARA_ITERAR`

`V02_GOAP_REQUIERE_CORRECCIONES`

`V02_GOAP_FALLO_CONCEPTUAL`
