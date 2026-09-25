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

---

# 22. ACTUALIZACIÓN 2026-09-25 — REGLA DE BACKUP

A partir de esta fecha queda fijada como regla operativa permanente:

> Toda decisión arquitectónica importante, frente experimental nuevo, versión candidata, corrección relevante, auditoría que cambie el estado de un módulo o implementación próxima debe quedar reflejada en este backup maestro o en un documento enlazado desde `experimentos/backups/`.

Objetivo: que ningún avance importante dependa exclusivamente del contexto de un chat.

Esta actualización se realizó en rama de documentación aislada:

`docs/experimentos-backup-2026-09-25`

Base exacta usada para crearla:

`5812deb59cd1c133383b9af973486a702a26daf4`

No modifica producción ni autoriza merge.

---

# 23. MONSTER COMBAT AI v0.1 — ESTADO

Frente experimental nuevo.

Nombre de la primera versión:

`Monster Combat AI v0.1 — Deterministic Decision Kernel`

Rama futura prevista:

`experiment/monster-combat-ai-v0.1`

Al verificar GitHub el 2026-09-25, esa rama todavía NO existía.

Baseline de diseño:

`5812deb59cd1c133383b9af973486a702a26daf4`

Responsabilidad congelada:

```text
snapshot observable
+ effectiveKit
+ perfil cognitivo
+ preferencias
+ memoria semántica ya resuelta
+ contexto social
+ RNG determinista
        ↓
chooseMonsterIntent()
        ↓
INTENT_SELECTED
o
NO_ELIGIBLE_INTENT
```

Regla superior:

> La IA decide. El motor resuelve.

Fuera de alcance de v0.1:

- ejecutar combate;
- daño;
- HP;
- aplicar estados;
- consumir cooldowns;
- integrar con ver74;
- Adaptive Ecology;
- planes tácticos;
- Grulla;
- integración con `Combate`;
- modificar Utility AI NPC;
- GOAP;
- merge.

Perfiles del laboratorio:

```text
INSTINTIVO
REACTIVO_1
CAZADOR_2
TACTICO_3
MASTER_4
```

Fixtures sintéticos:

```text
Rata
Serpiente
Lobo
Devorador
Mantis
```

No son datos canónicos productivos.

## 23.1 Candidata local Claude — auditoría independiente

Claude construyó una candidata local porque su entorno no tenía egress/GitHub.

Resultados reportados y reproducidos independientemente:

```text
tests: 35/35 PASS
stress: 50.000 decisiones
invalidSelections = 0
inputMutations = 0
executionSideEffects = 0
nondeterministicMismatches = 0
```

Seed 1337 repetida:

`89c8a34cd1517e3b0a5a32c5fe82613895df63bef590c525cc6b57af9b31f1c8`

La candidata NO se considera todavía materializada en Git porque:

- la rama real no existe;
- no hay HEAD real;
- no hay parent/tree auditables;
- no hay PR draft.

## 23.2 Hallazgo bloqueante independiente

Se detectó un bug real de `reorder invariance` con jitter.

Causa:

- `effectiveKit` se recorría en el orden recibido;
- cada habilidad consumía RNG para jitter durante ese recorrido;
- al reordenar el array, los mismos valores RNG podían asignarse a habilidades distintas.

Prueba adversarial independiente:

```text
casos: 5000
mismatches por reorder: 354
≈ 7,08 %
```

Esto viola el Golden de invariancia al reordenamiento.

Corrección requerida:

> Canonicalizar el conjunto/orden de habilidades antes de consumir RNG, de modo que misma seed + mismo estado produzcan los mismos scores por ability independientemente del orden de entrada.

## 23.3 Segundo hardening requerido

El contrato de cooldowns era booleano, pero valores truthy como:

```text
"false"
1
-1
[]
{}
```

podían interpretarse como cooldown activo.

Corrección requerida:

> `cooldowns[cooldownKey]` debe aceptar sólo booleanos estrictos `true` / `false`; otros tipos deben producir `ContractError`.

## 23.4 Métricas de stress a corregir

- `memoryInfluencedCases` no debe contar solamente memoria activa; debe medir influencia real o renombrarse.
- `executionSideEffects` no debe ser un contador decorativo permanentemente en cero; debe medirse si se conserva.

Estado:

`MONSTER_COMBAT_AI_V01_REQUIERE_CORRECCIONES`

REV2 pendiente.

No rehacer arquitectura; corrección localizada.

---

# 24. ADAPTIVE ECOLOGY v0.1 — ESTADO

Frente de diseño abierto en paralelo.

Nombre:

`Adaptive Ecology v0.1 — Population Pressure & Adaptation Resolver`

Rama futura propuesta:

`experiment/monster-ecology-adaptation-v0.1`

Al verificar GitHub el 2026-09-25 esa rama NO existía.

Estado actual:

```text
ESPECIFICACIÓN EN REVISIÓN
NO IMPLEMENTAR TODAVÍA
```

Arquitectura:

```text
Population State
→ Pressure Resolver
→ Adaptation Resolver
→ activeAdaptations
→ effectiveKit
→ FIN v0.1
```

Relación futura:

```text
Adaptive Ecology
→ effectiveKit
→ Monster Decision Kernel
```

Adaptive Ecology NO decide qué acción usar.

Monster Combat AI NO conoce:

```text
kills
pressure
adaptationTier
decay
population history
```

## 24.1 Principio

No level scaling.

No:

```text
jugador fuerte
→ +HP
→ +daño
→ +defensa
```

Sí:

```text
caza repetida de población local
→ pressure
→ adaptation tier
→ respuestas conductuales disponibles
```

La adaptación debe sentirse como:

> el ecosistema aprendió a sobrevivirme

y no:

> el juego hizo scaling porque estoy jugando demasiado.

## 24.2 Unidad de adaptación

La adaptación es local por población.

Ejemplo:

```text
bosque_norte:lobo_tres_colas
valle_oeste:lobo_tres_colas
```

son poblaciones independientes.

No hay telepatía global de especie.

## 24.3 Modelo preliminar

Preferencia actual para una futura v0.1:

```text
pressure 0..100
4 tiers
adaptaciones reversibles
sin RNG
sin stat scaling
sin loot
populationId explícita
eventos declarativos
observations agregadas
decay por elapsedTime
effectiveKit determinista
```

Los thresholds y pesos todavía NO son canon.

## 24.4 Observations semánticas

Vocabulario preliminar:

```text
OFENSIVA_DIRECTA
OFENSIVA_MULTIIMPACTO
DEFENSA_ABSORCION
DEFENSA_PORCENTUAL
EVASION
CONTROL
RECUPERACION
PREPARACION
```

Pueden ayudar a escoger una respuesta conductual permitida.

Nunca deben crear:

- HP extra;
- daño extra;
- defensa oculta;
- inmunidad;
- resistencia secreta.

## 24.5 Riesgos que la revisión debe cerrar

- doble conteo entre eventos;
- observation poisoning;
- adaptación global accidental;
- oscilación alrededor de thresholds;
- source of truth de tier/adaptations;
- decay;
- reversibilidad;
- frontera territorial explotable;
- dependence de orden;
- effectiveKit con duplicados;
- crecimiento histórico infinito;
- O(elapsedTime);
- acoplamiento indebido con Monster AI.

## 24.6 Preguntas abiertas clave

- pressure 0..100 o interno no acotado;
- hysteresis desde v0.1;
- decay de observations;
- recent vs lifetime observations;
- cómo evitar poisoning;
- necesidad real de SPECIES_DEFEATED;
- deduplicación de eventos;
- tier persistido vs derivado;
- activeAdaptations persistidas vs derivadas;
- adaptación por pattern en v0.1 o v0.2;
- decay lineal/escalonado/exponencial;
- unidad de tiempo;
- reversibilidad total;
- futuro multiplayer;
- eventId desde v0.1.

Documento local de especificación preparado:

`ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_REVISION.md`

SHA-256 del documento local:

`862ca8b27e58482c648b3e80b33265305eef4295bc13c65c2dde45c094efae87`

Prompt local de revisión Claude:

`PROMPT_CLAUDE_REVISION_ADAPTIVE_ECOLOGY_v0.1.md`

SHA-256:

`b8801ded7731e2d1a3d186135ab1c8f2ce473dab387af2f84577d36ce9d1a189`

Claude debe REVISAR, no implementar.

Veredictos conceptuales permitidos:

```text
ADAPTIVE_ECOLOGY_V01_SPEC_APTA_PARA_IMPLEMENTAR
ADAPTIVE_ECOLOGY_V01_SPEC_REQUIERE_CAMBIOS
ADAPTIVE_ECOLOGY_V01_SPEC_FALLO_CONCEPTUAL
```

---

# 25. REGLA DE AISLAMIENTO MONSTER/ADAPTIVE

A partir de estos frentes:

1. todo nace en `experimentos/`;
2. producción no se toca;
3. `ver74` no se toca;
4. fixtures no son canon;
5. cada módulo se audita separado;
6. no merge automático;
7. integración futura requiere adapter explícito;
8. decisiones importantes se vuelcan al backup maestro antes de avanzar demasiado.

---

# 26. ADAPTIVE ECOLOGY v0.1 — RESULTADO PRIMERA REVISIÓN Y REV2

Primera revisión conceptual externa recibida.

Veredicto:

`ADAPTIVE_ECOLOGY_V01_SPEC_REQUIERE_CAMBIOS`

Hallazgos bloqueantes de la revisión:
- doble conteo de eventos no cerrado;
- deduplicación sin responsabilidad/estado definido;
- hysteresis con impacto contractual;
- tier/activeAdaptations persistidos vs derivados sin cerrar;
- decay/unidad temporal sin cerrar.

La revisión recomendó simplificar v0.1 y sacar observations, SPECIES_DEFEATED y REPEATED_HUNT. También recomendó tier/activeAdaptations derivados, pressure 0..100 y decay lineal.

Decisión independiente adoptada para REV2:

```text
v0.1
- sólo SPECIES_KILLED
- observations fuera
- pressure entero 0..100
- decay lineal O(1)
- tiempo lógico
- tier derivado
- activeAdaptations derivadas
- adaptaciones acumulativas/reversibles
- recentEventIds acotado para dedup defensiva
- sin RNG
- sin stat scaling
- sin Monster Utility
```

Diferencia deliberada respecto de la revisión externa:

> NO se adopta cooldown/hysteresis de tier en v0.1.

Razón: un cooldown obligaría a agregar estado temporal y haría que `tier` dejara de ser una función pura de `pressure + config`. Para este laboratorio se acepta la posible oscilación alrededor de thresholds como limitación conocida y se difiere hysteresis a v0.2.

Source of truth REV2:

Persistido:
```text
populationId
speciesId
territoryId
pressure
lastUpdate
recentEventIds
```

Derivado:
```text
tier
activeAdaptations
effectiveKit
```

Config:
```text
baseKit
thresholds
adaptationCatalog
pressurePerKill
decayPerTimeUnit
dedupWindowSize
```

Orden transaccional REV2:

```text
validate
→ decay hasta now
→ update lastUpdate
→ dedup
→ check populationId
→ apply kill pressure
→ clamp
→ update recentEventIds
→ derive tier
→ derive adaptations
→ derive effectiveKit
```

Documentos preservados en esta rama de backup:

`experimentos/backups/ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_REV2.md`

`experimentos/backups/PROMPT_CLAUDE_REVIEW_ADAPTIVE_ECOLOGY_v0.1_REV2.md`

Estado actual:

```text
REV2 LISTA PARA SEGUNDA REVISIÓN CONCEPTUAL
NO IMPLEMENTAR TODAVÍA
```

---

# 27. ADAPTIVE ECOLOGY v0.1 — SEGUNDA REVISIÓN Y REV3

Segunda revisión conceptual externa recibida sobre REV2.

Veredicto:

`ADAPTIVE_ECOLOGY_V01_REV2_REQUIERE_CAMBIOS`

La revisión confirmó que REV2 resolvió casi todos los bloqueantes de la primera pasada y encontró tres defectos puntuales de especificación:

1. locality debía validarse antes que dedup;
2. `occurredAt` estaba presente sin semántica funcional;
3. la garantía limitada de `recentEventIds` no estaba documentada con suficiente precisión.

También señaló como no bloqueantes:
- orden canónico de `effectiveKit` subespecificado;
- poda FIFO de dedup no descrita de forma operativa;
- política de ability desconocida ambigua;
- justificación de “sin hysteresis” mal formulada aunque la decisión fuera correcta.

## 27.1 Decisiones adoptadas en REV3

REV3 corrige:

```text
locality antes de dedup
occurredAt eliminado
dedup FIFO por orden de aplicación
replay después de poda documentado como limitación conocida
effectiveKit con orden canónico por ID ASCII
INVALID_POPULATION distinto de DUPLICATE_EVENT
duplicate + elapsedTime aplica decay pero no kill
```

No se adopta filtrado silencioso de abilities desconocidas.

Razón:

> Adaptive Ecology v0.1 no recibe el catálogo autoritativo de habilidades de combate. Sólo valida el shape del ID; la existencia semántica se validará en el futuro adapter contra HABILIDADES_MOB.

La ausencia de hysteresis se mantiene, pero cambia la justificación:

> se difiere porque v0.1 todavía no tiene un consumidor real de tier/effectiveKit. La oscilación es hoy un fenómeno sólo de laboratorio. Cuando exista integración real, v0.2 deberá decidir hysteresis y/o congelación de effectiveKit durante cada encuentro.

## 27.2 Contrato REV3

Fuente persistente:

```text
populationId
speciesId
territoryId
pressure
lastUpdate
recentEventIds
```

Derivado:

```text
tier
activeAdaptations
effectiveKit
```

Evento positivo único:

`SPECIES_KILLED`

Orden transaccional:

```text
validate
→ locality
→ decay hasta now
→ update lastUpdate
→ dedup
→ apply kill si no duplicado
→ clamp
→ update/prune recentEventIds FIFO
→ derive tier
→ derive adaptations
→ derive effectiveKit
```

Documentos preservados:

`experimentos/backups/ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_REV3.md`

`experimentos/backups/PROMPT_CLAUDE_REVIEW_ADAPTIVE_ECOLOGY_v0.1_REV3.md`

Estado:

```text
REV3 LISTA PARA TERCERA REVISIÓN CONCEPTUAL
NO IMPLEMENTAR TODAVÍA
```

---

# 26. ADAPTIVE ECOLOGY v0.1 — REV3

Segunda revisión conceptual recibida:

`ADAPTIVE_ECOLOGY_V01_REV2_REQUIERE_CAMBIOS`

La revisión confirmó que REV2 resolvió la arquitectura principal y dejó tres correcciones puntuales de especificación:

1. validar `locality` antes de `dedup`;
2. definir `occurredAt` como metadata opaca sin efecto lógico en v0.1;
3. documentar que `recentEventIds` sólo protege reintentos cercanos y que un ID expulsado por la ventana puede volver a aplicarse.

También se aceptaron estas precisiones:

- poda FIFO por orden de aplicación;
- effectiveKit con orden canónico por abilityId;
- ability desconocida filtrada del kit y reportada sólo en debug;
- estados distinguibles `OK | DUPLICATE_EVENT | INVALID_POPULATION`;
- hysteresis sigue fuera de v0.1, pero la justificación correcta es que todavía no existe un consumidor real de transiciones de tier;
- cuando Monster AI consuma effectiveKit en combate, habrá que impedir cambios inesperados de kit a mitad de encuentro.

Documentos preservados en esta rama:

`experimentos/backups/ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_REV3.md`

`experimentos/backups/PROMPT_CLAUDE_REVIEW_ADAPTIVE_ECOLOGY_v0.1_REV3.md`

Estado:

```text
REV3 CANDIDATA FINAL DE DISEÑO
PENDIENTE REVISIÓN CONCEPTUAL FINAL
NO IMPLEMENTAR TODAVÍA
```

Si la revisión final devuelve:

`ADAPTIVE_ECOLOGY_V01_REV3_APTA_PARA_IMPLEMENTAR`

el siguiente paso será preparar el prompt de implementación experimental, manteniendo producción intacta y sin merge automático.


Fin del handoff.


---

# 26. ADAPTIVE ECOLOGY v0.1 — DISEÑO CONGELADO

La tercera revisión conceptual externa concluyó:

`ADAPTIVE_ECOLOGY_V01_REV3_APTA_PARA_IMPLEMENTAR`

No quedaron bloqueantes contractuales.

La REV3 confirmó:

- locality antes de dedup;
- `occurredAt` como metadata opaca;
- límite explícito de `recentEventIds`;
- FIFO por orden de aplicación;
- effectiveKit canónico/reorder-invariant;
- source of truth limpio;
- ausencia de contradicciones estructurales.

Se incorporaron además cuatro aclaraciones no bloqueantes antes de congelar la versión FINAL:

1. thresholds con límite inferior inclusivo;
2. validación explícita `now >= lastUpdate`;
3. errores contractuales mediante `ContractError`;
4. corrección de referencia REV2 → FINAL.

Estado:

```text
ADAPTIVE ECOLOGY v0.1
DESIGN_STATUS: FROZEN_FOR_EXPERIMENTAL_IMPLEMENTATION
```

Archivos de respaldo:

`experimentos/backups/ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_FINAL.md`

`experimentos/backups/PROMPT_IMPLEMENTACION_ADAPTIVE_ECOLOGY_v0.1.md`

Rama de implementación prevista:

`experiment/monster-ecology-adaptation-v0.1`

Base obligatoria:

`5812deb59cd1c133383b9af973486a702a26daf4`

Cadena v0.1 congelada:

```text
SPECIES_KILLED
→ pressure
→ decay
→ tier derivado
→ activeAdaptations derivadas
→ effectiveKit
```

Fuera de v0.1:

- observations;
- adaptación por patrón;
- hysteresis;
- otros event types;
- stat scaling;
- Monster Utility;
- combate real;
- producción.

No merge automático.
