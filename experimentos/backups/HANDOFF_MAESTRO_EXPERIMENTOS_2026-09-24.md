# HANDOFF MAESTRO — LABORATORIO DE EXPERIMENTOS

Fecha: 2026-09-24

Este documento existe para continuar todo el trabajo experimental de La Grulla Blanca en otro chat sin mezclarlo con la conversación de producción/3C.6.

## 0. Regla de uso

Al abrir un chat nuevo para experimentos:

1. leer este archivo completo;
2. verificar el HEAD real de la rama experimental antes de modificar nada;
3. no asumir que un informe externo implica merge;
4. mantener producción y laboratorio separados;
5. no usar este handoff para redefinir canon de NPC, misiones o mundo.

---

# 1. Repositorio y ramas

Repositorio:

`https://github.com/Shein25/La-Grulla-Blanca`

Producción:

`main`

HEAD de main al crear este backup:

`a7c1c0a4fc15051b2313f19efdf20ac1e6855229`

Producción actual tiene 3C.5 cerrado y baseline ver74. Este handoff NO autoriza cambios de producción.

Rama experimental GOAP activa:

`experiment/motor-npc-v0.2-goap`

HEAD actual al crear este backup:

`d88fe4e2ddbba517412c3e943ad5241ffe15d78c`

PR activo:

`#2 — experiment: Motor NPC Vivo v0.2.2 — GOAP REV3`

`https://github.com/Shein25/La-Grulla-Blanca/pull/2`

Estado del PR al crear este backup:

- OPEN
- DRAFT
- MERGEABLE
- NO MERGED

No mergear automáticamente aunque una auditoría externa diga PASS.

---

# 2. Organización actual de experimentos

La carpeta fue reorganizada por familia de motor:

```text
experimentos/
├── README.md
├── backups/
├── utility-ai/
│   ├── README.md
│   ├── motor-npc-vivo-v0.1/
│   └── motor-npc-vivo-v0.1.1/
└── goap/
    ├── README.md
    └── motor-npc-vivo-v0.2-goap/
```

No crear carpetas futuras vacías.

Cuando exista una prueba real podrán aparecer, por ejemplo:

```text
experimentos/
├── utility-ai/
├── goap/
├── behavior-tree/
├── htn/
├── redes-neuronales/
├── reinforcement-learning/
└── integraciones/
```

La carpeta `integraciones/` sólo tendría sentido cuando comparemos combinaciones como Utility+GOAP, Neural+GOAP, Utility+HTN, etc.

---

# 3. Principio arquitectónico

Utility AI y GOAP son técnicas distintas.

Arquitectura experimental actual:

```text
Utility AI
   ↓
elige QUÉ objetivo perseguir
   ↓
GOAP
   ↓
decide CÓMO alcanzar el objetivo
   ↓
Executor
   ↓
ejecuta y verifica
```

GOAP NO es pathfinding físico.

El GOAP actual trabaja con hechos abstractos y no conoce las 329 rooms canónicas.

Separación deseada:

- Utility AI = selección/prioridad de objetivos.
- GOAP = planificación lógica.
- Executor = aplicación/verificación de acciones.
- pathfinding físico = sistema aparte si alguna vez se integra.

---

# 4. Reglas permanentes del laboratorio

Nada de `experimentos/` es producción por existir en el repositorio.

Para que un resultado experimental llegue al juego debe pasar por:

1. versión congelada;
2. tests propios;
3. stress/reproducciones adversariales;
4. auditoría externa;
5. auditoría independiente adicional;
6. contrato de integración;
7. revisión antes de merge.

Nunca usar fixtures experimentales como canon.

Nunca convertir nombres/rangos/estados sintéticos del laboratorio en canon automáticamente.

No mezclar la rama experimental con ramas de implementación de producción.

---

# 5. Convención para auditorías externas

A partir de ahora todo informe de agente externo DEBE identificar al auditor.

Nombre:

```text
Informe_Test_<SISTEMA>_<VERSION>_<REV>_<AGENTE>.md
```

Ejemplos:

```text
Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_CLAUDE.md
Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_GEMINI.md
```

Cabecera mínima:

```text
Agente auditor:
Modelo o versión:
Fecha:
Rama auditada:
HEAD auditado:
Tipo de revisión:
```

Si un informe antiguo no identifica agente, NO inferirlo. Referirse a él como Agente A/B o "agente no identificado".

---

# 6. Utility AI — v0.1

Ruta actual:

`experimentos/utility-ai/motor-npc-vivo-v0.1/`

Fue el primer laboratorio del Motor NPC Vivo.

Objetivo:

- probar decisión determinista basada en Utility AI;
- fixtures ficticios/no canónicos;
- personalidad;
- conocimiento;
- diálogo restringido;
- selección de acciones.

Acciones iniciales del laboratorio:

- vigilar
- trabajar
- patrullar
- hablar_jugador
- ayudar_jugador
- investigar
- informar_superior
- regresar_puesto
- esperar

Los rangos sintéticos usados en laboratorio nunca fueron canon.

La v0.1 sirvió como prueba de concepto, no como base definitiva.

---

# 7. Utility AI — v0.1.1

Ruta actual:

`experimentos/utility-ai/motor-npc-vivo-v0.1.1/`

Rama histórica:

`experiment/motor-npc-v0.1.1`

PR histórico:

`#1`

`https://github.com/Shein25/La-Grulla-Blanca/pull/1`

Head auditado final:

`8249378a0c572799a051d8d024f8567f8fec63eb`

Resultado externo final:

`V011_APTO_PARA_GOAP`

PR #1 fue mergeado.

Merge commit:

`404411f09c0e110f02c92689ffeb1a3c69a213ab`

## 7.1 Cadena de hardening v0.1.1

Durante los retests se encontraron sucesivamente:

- propiedades heredadas;
- accessors propios;
- campos obligatorios con `undefined`;
- TOCTOU con JavaScript Proxy;
- rereads externos después de validar.

La solución final fue cambiar la frontera del motor:

```text
input externo
   ↓
captura única desde descriptores propios
   ↓
snapshot interno plano
   ↓
validación del snapshot
   ↓
cálculo sólo sobre snapshot
```

El motor no debe volver a leer datos de negocio desde el input externo después de capturarlos.

Retest final:

- 44 PASS / 0 FAIL;
- cinco stress de 10.000 casos PASS;
- Proxy/getters/accessors/herencia endurecidos;
- finitud verificada;
- determinismo verificado;
- pesos sin cambios.

Deuda menor documentada:

- determinados valores hostiles usados sólo para formatear errores pueden causar TypeError durante el mensaje de validación;
- no permite que una entrada inválida llegue al cálculo;
- no bloqueó GOAP.

---

# 8. GOAP — v0.2 inicial

Rama:

`experiment/motor-npc-v0.2-goap`

PR:

`#2`

Arquitectura objetivo:

```text
Utility AI → OBJECTIVE
GOAP       → PLAN
Executor   → apply / verify / replan
```

Primera candidata relevante auditada:

`a64b708b781ad273100c04845dcba116f8400209`

REV1 externa:

`V02_GOAP_REQUIERE_CORRECCIONES`

## 8.1 Hallazgos principales REV1

1. Inconsistencia `-0` vs `0`:
   - `factsMatch(Object.is)` distinguía;
   - la key JSON los colapsaba.

2. Costes:
   - acumulación podía llegar a Infinity;
   - costes diminutos podían no incrementar el total por redondeo.

3. Explosión por estados equivalentes:
   - caminos de igual coste al mismo estado se reencolaban;
   - crecimiento combinatorio.

4. Límites:
   - `maxExpansions` negativo;
   - semántica one-over;
   - SEARCH_LIMIT tratado como NO_PLAN por controller.

5. Executor:
   - podía continuar hacia un objetivo que había dejado de ser relevante.

6. Rendimiento:
   - frontier por sort completo;
   - facts irrelevantes agrandaban el estado.

REV1 validó la separación arquitectónica, pero la candidata necesitaba correcciones.

---

# 9. GOAP — v0.2.1

La misma PR #2 evolucionó a v0.2.1.

Cambios principales:

## 9.1 Identidad de estado

- encoding tipado de facts;
- `-0` distinguido de `0`;
- missing distinguido de present.

## 9.2 Cierre causal de facts

Se añadió cálculo de `relevantFactKeys(goal, actions)`.

La key de estado ignora facts que no participan causalmente del objetivo.

## 9.3 Poda canónica

Firma por nodo:

```text
cost
steps
planKey
```

Sólo queda el mejor representante por estado.

## 9.4 Frontier

Se sustituyó sort completo por binary MinHeap.

## 9.5 Costes

Los costes de acción pasaron a ser:

`Number.isSafeInteger(cost) && cost > 0`

La suma acumulada se protege contra overflow.

Nuevo estado:

`COST_OVERFLOW`

## 9.6 Límites

- `maxExpansions` estricto;
- `maxFrontier`;
- `SEARCH_LIMIT`;
- `FRONTIER_LIMIT`.

## 9.7 Controller

Estados inconclusos:

- SEARCH_LIMIT
- FRONTIER_LIMIT
- COST_OVERFLOW

producen:

`PLANNING_DEFERRED`

No se hace fallback a objetivos inferiores ante búsqueda inconclusa.

Sólo `NO_PLAN` permite fallback legítimo.

## 9.8 Goal relevance

El selector devuelve para cada objetivo:

- goal
- relevance

Ejemplos:

HELP_PLAYER:
```js
{
  playerPresent:true,
  playerNeedsHelp:true,
  playerHelped:false
}
```

La idea: antes de ejecutar un paso, comprobar si el objetivo todavía tiene sentido.

## 9.9 Suite

v0.2.1 llegó a 40 tests declarados.

---

# 10. Auditoría externa REV2 de v0.2.1

Resultado:

`V021_GOAP_REQUIERE_CORRECCIONES`

La auditoría confirmó que funcionaban:

- 40/40 tests;
- cinco stress estáticos;
- tres stress dinámicos;
- `-0` / `0`;
- costes seguros;
- COST_OVERFLOW;
- poda de estados;
- facts irrelevantes;
- límites;
- NO_PLAN vs estados inconclusos;
- personalidades;
- arquitectura.

Encontró DOS defectos reales y localizados.

## 10.1 Defecto A — relevance opcional

La API pública del Executor permitía:

```js
executeNext(..., relevance={})
```

Si el caller olvidaba pasar relevance, un plan HELP_PLAYER podía ejecutar `ir_jugador` aunque `playerNeedsHelp` ya fuera false.

## 10.2 Defecto B — desempate lexicográfico

El tercer criterio usaba:

```js
JSON.stringify(plan).localeCompare(...)
```

Eso no equivale a comparar la secuencia real de IDs.

Contraejemplo:

```text
a
a!
```

La implementación podía elegir incorrectamente `a!`.

---

# 11. GOAP — v0.2.2 actual

Versión actual del laboratorio:

`0.2.2`

Ruta:

`experimentos/goap/motor-npc-vivo-v0.2-goap/`

Candidata lógica antes de reorganizar carpetas:

`c5b1c0bf4c6e84cc7268c62daf8a31f633704501`

HEAD actual tras reorganización:

`d88fe4e2ddbba517412c3e943ad5241ffe15d78c`

Los archivos centrales de motor no cambiaron entre ambos HEAD; la reorganización movió carpetas y ajustó imports/documentación.

## 11.1 Corrección de relevance

Cuando controller obtiene PLAN_FOUND, el plan ejecutable incorpora:

```js
{
  ...plan,
  goal,
  relevance,
  goalId
}
```

Executor consume ese contrato vinculado.

Por eso esta llamada debe ser segura:

```js
executeNext(
  decision.plan,
  changedWorld,
  decision.selectedGoal.goal,
  GOAP_ACTIONS
)
```

aunque no exista un quinto argumento de relevance.

Si el objetivo dejó de ser relevante:

```text
REPLAN_REQUIRED
goalObsolete = true
executed = null
```

antes de aplicar efectos.

Plan manual no vinculado sin relevance:

- se rechaza antes de efectos.

Goal/relevance explícitos contradictorios con el contrato vinculado:

- se rechazan.

## 11.2 Corrección del desempate

El criterio actual es:

```text
1. menor coste
2. menor número de pasos
3. secuencia lexicográficamente menor de IDs
```

Ya no se usa `JSON.stringify(plan)`.

La comparación es ID por ID.

Caso obligatorio:

`a` debe preceder a `a!`.

## 11.3 Suite actual

47 tests declarados.

El stress dinámico fue modificado deliberadamente para NO pasar relevance por separado al Executor.

Así se comprueba que la protección realmente viaje dentro del plan.

---

# 12. Reorganización de carpetas

Antes:

```text
experimentos/motor-npc-vivo-v0.1/
experimentos/motor-npc-vivo-v0.1.1/
experimentos/motor-npc-vivo-v0.2-goap/
```

Ahora:

```text
experimentos/utility-ai/motor-npc-vivo-v0.1/
experimentos/utility-ai/motor-npc-vivo-v0.1.1/
experimentos/goap/motor-npc-vivo-v0.2-goap/
```

Imports GOAP hacia fixtures Utility AI fueron ajustados a:

```js
../../utility-ai/motor-npc-vivo-v0.1.1/npc-fixtures.mjs
```

La reorganización NO pretende cambiar la lógica del motor.

---

# 13. Estado de REV3 — dos agentes

El usuario decidió pedir REV3 a DOS agentes distintos para comparar evidencia.

Regla:

- no promediar opiniones;
- un bug reproducible pesa más que un PASS declarativo;
- comparar cobertura;
- reproducir contradicciones antes de decidir.

## 13.1 REV3 Agente A — RECIBIDA

El archivo recibido originalmente se llamó:

`Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3.md`

No identificó al agente en la cabecera porque fue generado antes de fijar la nueva convención.

NO inferir quién fue.

Referirse a él como:

`REV3 AGENTE A — agente no identificado en el archivo`

HEAD auditado:

`c5b1c0bf4c6e84cc7268c62daf8a31f633704501`

Ese HEAD es anterior únicamente a la reorganización de carpetas.

Resultado:

`V022_GOAP_APTO_PARA_ITERAR`

### Resultados principales del Agente A

Suite:

```text
47 / 47 PASS
0 FAIL
exit code 0
```

Stress estático:

```text
10000 × seeds:
1337
1
42
999
20260923

todos PASS
```

Stress dinámico:

```text
seed 1337
goalReached 4932
replanRequired 426
successfulReplans 426
repeatedStates 68
stepLimit 0
uselessMoveAfterObsoleteGoal 0

seed 42
goalReached 4927
replanRequired 398
successfulReplans 398
repeatedStates 73
stepLimit 0
uselessMoveAfterObsoleteGoal 0

seed 20260923
goalReached 4927
replanRequired 421
successfulReplans 421
repeatedStates 73
stepLimit 0
uselessMoveAfterObsoleteGoal 0
```

Confirmó por lectura de código que dynamic-stress llama `executeNext` con 4 argumentos y NO pasa relevance por separado.

Reprodujo HELP_PLAYER con `playerNeedsHelp=false`:

- REPLAN_REQUIRED;
- goalObsolete=true;
- executed=null;
- sin movimiento.

Reprodujo también `executeWholePlan` sin relevance separada:

- REPLAN_REQUIRED antes del primer movimiento.

Contrato:

- plan.goal presente;
- plan.relevance presente;
- plan.goalId presente;
- plan manual sin relevance rechazado;
- contradicciones explícitas de goal/relevance rechazadas.

Desempate:

- `a` vs `a!` PASS;
- array invertido PASS;
- oráculo independiente;
- 8 casos dirigidos;
- fuzz 300 casos;
- 0 discrepancias.

Rendimiento aproximado informado:

- tests 47: ~47 ms;
- stress 10000: ~570 ms/seed;
- dynamic stress 5000: ~420 ms/seed.

### Observaciones no bloqueantes del Agente A

1. Caller malicioso/consciente podría pasar explícitamente `relevance:{}` a un plan no vinculado.
   - distinto del bug REV2 de omisión silenciosa;
   - clasificado no bloqueante.

2. El orden lexicográfico actual es por comparación de strings JS / unidades UTF-16.
   - comportamiento documentado;
   - no es orden numérico ni locale-aware.

## 13.2 Relación Agente A ↔ HEAD actual

Agente A auditó:

`c5b1c0bf...`

HEAD actual:

`d88fe4e2...`

Después de la auditoría se reorganizaron carpetas.

Los blobs centrales del motor permanecieron iguales:

- goap.mjs
- controller.mjs
- executor.mjs
- actions.mjs
- goal-selector.mjs
- world-fixtures.mjs

Los cambios posteriores relevantes fueron:

- mover rutas;
- ajustar imports en tests/stress/dynamic-stress;
- documentación;
- convención de nombres de auditoría.

Por eso REV3 A sigue siendo evidencia válida para la lógica v0.2.2, pero no sustituye una corrida sobre la estructura reorganizada.

## 13.3 REV3 Agente B — PENDIENTE

El segundo agente debe auditar EXACTAMENTE el HEAD actual:

`d88fe4e2ddbba517412c3e943ad5241ffe15d78c`

Ruta:

`experimentos/goap/motor-npc-vivo-v0.2-goap/`

Debe usar:

`PROMPT_AGENTE_TEST.md`

y entregar:

`Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_<AGENTE>.md`

con identidad de agente/modelo/HEAD.

Además de dar una segunda opinión, esta auditoría debe confirmar que la reorganización y los imports funcionan.

---

# 14. Decisión pendiente inmediata

NO MERGEAR PR #2 todavía.

Siguiente secuencia:

```text
REV3 Agente A
        +
REV3 Agente B
        ↓
comparación de cobertura
        ↓
reproducción de contradicciones
        ↓
auditoría independiente final
        ↓
¿v0.2.2 apta?
   /            \
 NO              SÍ
 ↓                ↓
v0.2.3        considerar cierre/merge
```

Incluso si ambos dicen PASS, revisar el HEAD real antes de merge.

---

# 15. Preguntas abiertas / deuda no bloqueante

- decidir si `relevance:{}` explícita en plan no vinculado merece hardening futuro;
- documentar de forma permanente la semántica UTF-16 de IDs o imponer una convención restringida de IDs;
- decidir si v0.2.2 será la base estable para el siguiente experimento;
- no integrar todavía topología real;
- no integrar todavía scheduler;
- no integrar todavía memoria;
- no integrar todavía comunicación NPC↔NPC.

---

# 16. Próximas líneas experimentales discutidas

No están implementadas.

## 16.1 Memoria dinámica

Posible futuro:

```text
NPC_RUNTIME
├── posicion
├── conocimiento
├── estado_narrativo
├── memoria
├── relaciones
│   ├── jugador
│   └── otros_NPC
└── percepcion_jugador
```

La memoria debería ser semántica/selectiva, no un log infinito de turnos.

Ejemplos:

- jugador_me_ayudo;
- jugador_mintio;
- orden_recibida;
- avistamiento_relevante;
- conocimiento transmitido;
- deuda social.

## 16.2 NPC↔NPC / social AI

Posibles futuras pruebas:

- confianza;
- credibilidad;
- rumores;
- secretos;
- jerarquía;
- órdenes;
- propagación de conocimiento;
- conflictos de objetivos.

Una cadena futura podría ser:

```text
NPC A sabe R6
→ informa a B
→ B actualiza conocimiento
→ cambia Utility
→ cambia objetivo
→ GOAP genera otro plan
```

## 16.3 Behavior Trees

Candidato para ejecución reactiva o comportamientos inmediatos.

No decidido como reemplazo de GOAP.

## 16.4 HTN

Candidato para planificación jerárquica.

Podría compararse contra GOAP para objetivos estructurados.

## 16.5 Redes neuronales

Se discutió usarlas principalmente para:

- selección de objetivos;
- comportamiento social;
- relaciones;
- reacción emocional;
- evaluación de credibilidad.

NO para definir verdad canónica del mundo.

Arquitectura segura propuesta:

```text
estado real del mundo
    ↓
reglas duras/canon/gates
    ↓
red neuronal propone intención
    ↓
validación simbólica
    ↓
GOAP/HTN
    ↓
Executor
```

La red nunca decide por sí sola:

- si una puerta está abierta;
- si una misión ocurrió;
- qué sabe realmente un NPC;
- qué room existe;
- qué hecho es canon.

## 16.6 Reinforcement Learning

Sólo como laboratorio.

Recompensas podrían representar:

- cumplir deber;
- ayudar;
- proteger puesto;
- no revelar secreto;
- evitar loops;
- completar objetivo.

No hay implementación todavía.

---

# 17. Torneo de arquitecturas en Google Colab

El usuario quiere ejecutar el cómputo pesado en Colab para no gastar créditos de agentes/código.

Idea:

```text
GitHub
  ↓
Colab
  ↓
mismos escenarios / mismas seeds
  ↓
Utility
GOAP
HTN
Behavior Tree
Neural
Hybrid
  ↓
métricas
```

Primero métricas deterministas, no evaluación LLM por episodio.

Posibles métricas:

- cumplimiento de objetivo;
- loops;
- replans;
- decisiones inválidas;
- coste CPU;
- memoria;
- estabilidad;
- respeto de invariantes.

Entrenamiento neural/RL separado de evaluación.

Conjunto de test congelado, no visto durante entrenamiento.

Posible futura estructura:

```text
experimentos/npc-ai-tournament/
├── environments/
├── agents/
├── scenarios/
├── metrics/
├── training/
├── benchmarks/
└── colab/
    └── NPC_AI_Tournament.ipynb
```

No crear todavía hasta que exista una prueba real.

---

# 18. Filosofía del torneo

No decidir por moda que GOAP sea "el ganador".

Comparar arquitecturas con:

- mismos escenarios;
- mismas seeds;
- mismos invariantes;
- mismo presupuesto de cálculo.

Posibles combinaciones:

- Utility AI;
- Utility + GOAP;
- Utility + HTN;
- Neural;
- Neural + GOAP;
- Neural + HTN;
- híbridos.

El objetivo no es un ranking absoluto sino encontrar qué componente sirve mejor para cada responsabilidad.

---

# 19. Separación producción / experimento

Producción actual tiene un sistema NPC canónico 3C.5, pero el laboratorio NO lo reemplaza.

El laboratorio usa fixtures ficticios.

No integrar:

- 32 NPC canónicos;
- gates reales;
- rooms reales;
- quests reales;
- save/load real;

hasta que exista un contrato explícito de integración.

El hecho de que Utility AI v0.1.1 haya sido mergeada significa que el laboratorio/versionado quedó preservado, no que el juego de producción esté usando ese cerebro.

---

# 20. Prompt mínimo para continuar en otro chat

Usar el archivo:

`experimentos/backups/PROMPT_NUEVO_CHAT_EXPERIMENTOS_2026-09-24.md`

como mensaje inicial del nuevo chat.

La tarea inmediata allí será:

1. recuperar este handoff;
2. verificar HEAD actual de `experiment/motor-npc-v0.2-goap`;
3. recibir REV3 del segundo agente;
4. comparar REV3 A vs REV3 B;
5. reproducir cualquier discrepancia;
6. emitir auditoría independiente final;
7. NO mergear sin decisión explícita del usuario.

---

# 21. Estado resumido

```text
Utility AI v0.1
→ histórico / prueba inicial

Utility AI v0.1.1
→ auditada
→ V011_APTO_PARA_GOAP
→ PR #1 MERGED
→ base experimental estable

GOAP v0.2
→ REV1 encontró problemas reales

GOAP v0.2.1
→ corrigió núcleo
→ REV2 encontró 2 bugs localizados

GOAP v0.2.2
→ corrigió relevance inseparable
→ corrigió desempate secuencial
→ 47 tests
→ REV3 Agente A = PASS
→ REV3 Agente B = PENDIENTE
→ PR #2 DRAFT
→ NO MERGED
```

Fin del handoff.
