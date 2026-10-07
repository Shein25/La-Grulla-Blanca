# PLAN DE PRUEBAS — FULL ENVELOPE TÉCNICAS + 2 ULTIS + GRULLA V01

## Estado

`PREPARED_WAITING_FOR_FINAL_TECHNIQUE_AUTHORITY`

V03.1 de Ultis queda congelado como evidencia mecánica. Este frente no lo modifica.

## Principio de progresión de ramas

**Afinidad y profundidad son sistemas distintos.**

Cualquier rama elemental que el jugador haya aprendido puede profundizarse hasta `APRENDIDA_AL_MAXIMO`, aunque no sea principal ni injertada.

El injerto:

- NO habilita la profundidad de la rama;
- NO es requisito para aprender una rama hasta el final;
- SÍ convierte una rama en segunda afinidad;
- SÍ es requisito para que esa segunda rama pueda conceder la Ulti injertada en LianQi IV.

Las ramas no afines se balancean por sus penalizaciones autorizadas, no por un techo artificial de aprendizaje.

## Preflight obligatorio

La campaña NO puede comenzar hasta disponer de:

- catálogo final/candidato autorizado de 15 técnicas (3 por raíz);
- SHA-256 del catálogo;
- catálogo de 25 Ultis y SHA-256;
- runner/autoridad de Grulla y SHA-256;
- perfiles de jugador/loadout autorizados;
- estado de progresión de las cinco ramas por perfil;
- elemento principal e injerto, cuando exista;
- distribuciones de puntos/builds a testear;
- autoridad de penalizaciones para ramas no afines;
- regla explícita sobre intento de Ulti rechazado y consumo del presupuesto.

Cualquier ausencia crítica debe producir `AUTHORITY_REQUIRED`, nunca un valor inventado.

## Gate de aprendizaje y gate de Ulti

Una rama puede alcanzar aprendizaje máximo sin afinidad.

Las Ultis sí están limitadas por identidad elemental:

### Principal
Disponible sólo si:
1. etapa >= **LianQi III**;
2. rama principal = **APRENDIDA_AL_MAXIMO**.

### Injertada
Disponible sólo si:
1. existe injerto elemental;
2. etapa >= **LianQi IV**;
3. rama injertada = **APRENDIDA_AL_MAXIMO**.

Una tercera rama no afín puede estar completamente dominada y aun así **no concede una tercera Ulti**.

## Builds

La distribución de puntos es una variable de build, no un gate de aprendizaje ni de Ulti.

Deben testearse:

- builds concentradas;
- builds híbridas;
- builds distribuidas como `2/2/2`;
- ramas no afines con inversión alta;
- principal/injerto con poca inversión actual pero maestría histórica máxima;
- combinaciones donde varias ramas estén aprendidas al máximo.

## Invariantes de repertorio

1. máximo 2 Ultis disponibles/equipables según la autoridad de repertorio;
2. máximo 1 del elemento principal;
3. máximo 1 del elemento injertado;
4. ramas no afines, aunque estén aprendidas al máximo, no añaden Ultis;
5. distribución de puntos nunca bloquea una Ulti ya elegible;
6. presupuesto compartido = 1 activación válida por combate;
7. tras activación válida, la otra queda bloqueada;
8. nunca ejecutar ambas en una misma simulación válida;
9. preservar cooldown OOC individual existente;
10. Pacto F3 conserva su autoridad.

## Envelopes por etapa

El envelope por etapa debe registrar separadamente:

- qué ramas conoce;
- profundidad/maestría alcanzada en cada rama;
- afinidad principal;
- afinidad injertada si existe;
- build/puntos actuales;
- penalizaciones efectivas por no afinidad;
- Ultis realmente elegibles.

No asumir que una rama no injertada tiene menor techo de aprendizaje.

## Suites mínimas nuevas

### U0 — UNLOCK_ELIGIBILITY
Valida Ultis desde etapa + identidad principal/injertada + aprendizaje máximo. Debe comprobar que una rama no afín aprendida al máximo NO genera una tercera Ulti.

### B0 — BRANCH_DEPTH_INDEPENDENT_FROM_AFFINITY
Demuestra que principal, injertada y no afín pueden alcanzar la misma profundidad de aprendizaje.

### B1 — NON_AFFINITY_PENALTY
Compara la misma técnica/rama con y sin afinidad usando exactamente la penalización autorizada y CRN pareado.

### B2 — BUILD_FREEDOM
Comprueba que builds diferentes, incluida `2/2/2`, no cambian el estado histórico de maestría de rama.

### U1 — REPERTOIRE_CONTRACT
Valida asignación de slots de Ulti sólo a principal e injertada.

### U2 — SHARED_USE_BUDGET
Activa la Ulti primaria y demuestra que la injertada queda bloqueada; repetir invirtiendo orden cuando ambas estén desbloqueadas.

### U3 — CHOICE_POLICY
Dado el mismo estado/seed, compara: primaria, injertada, guardar la Ulti.

### U4 — CHOICE_DOMINANCE
Detecta si una opción domina materialmente a la otra en casi todos los contextos.

### U5 — OPPORTUNITY_REGRET
Calcula diferencia entre la decisión tomada y la mejor alternativa disponible bajo el mismo CRN.

### U6 — F3_PACT_CHOICE
Compara uso/retención de cada alternativa antes y durante F3 sin permitir bypass del primer turno real de la Grulla.

### U7 — TECHNIQUE_TO_ULTIMATE_STATE_TRANSFER
Comprueba que buffs, debuffs, Qi, HP, absorción, DoT, control, equipo y memoria producidos por técnicas normales llegan correctamente a la decisión de Ulti.

### U8 — ULTIMATE_TO_TECHNIQUE_FOLLOWUP
Comprueba efectos de Ultis que potencian acciones/técnicas posteriores usando las técnicas reales autorizadas.

### U9 — CROSS_ROOT_REPERTOIRE
Compara repertorios, afinidades, ramas dominadas y builds con CRN pareado.

### U10 — ORDER_WORKER_RESUME_SHARD
Demuestra equivalencia serial vs 5 notebooks, reanudación desde checkpoint, cambio de workers y consolidación.

## Gate de balance

La decisión de balance debe considerar simultáneamente:

- potencia de técnicas normales;
- profundidad real de cada rama;
- afinidad o no afinidad;
- penalizaciones aplicables;
- distribución de puntos/build;
- coste de oportunidad de gastar la única Ulti del combate;
- elección entre las dos Ultis permitidas;
- fase de uso;
- supervivencia;
- daño/tempo/control;
- Pacto;
- regret y polarización cross-root.

No usar un target win-rate aislado ni auto-optimizar hacia igualdad numérica.
