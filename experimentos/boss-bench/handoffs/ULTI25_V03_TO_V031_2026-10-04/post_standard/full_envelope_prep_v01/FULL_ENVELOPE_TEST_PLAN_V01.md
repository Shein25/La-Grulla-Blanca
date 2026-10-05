# PLAN DE PRUEBAS — FULL ENVELOPE TÉCNICAS + 2 ULTIS + GRULLA V01

## Estado

`PREPARED_WAITING_FOR_FINAL_TECHNIQUE_AUTHORITY`

V03.1 de Ultis queda congelado como evidencia mecánica. Este frente no lo modifica.

## Preflight obligatorio

La campaña NO puede comenzar hasta disponer de:

- catálogo final/candidato autorizado de 15 técnicas (3 por raíz);
- SHA-256 del catálogo;
- catálogo de 25 Ultis y SHA-256;
- runner/autoridad de Grulla y SHA-256;
- perfiles de jugador/loadout autorizados;
- estado de progresión por perfil: etapa LianQi, rama principal aprendida al máximo, existencia de injerto y rama injertada aprendida al máximo;
- distribuciones de puntos/builds a testear como variable de combate, **nunca como gate de desbloqueo de Ulti**;
- regla explícita sobre intento de Ulti rechazado y consumo del presupuesto;
- regla de legalidad para primary==grafted si llegara a ser relevante.

Cualquier ausencia debe producir `AUTHORITY_REQUIRED`, nunca un valor inventado.

## Gate de desbloqueo por aprendizaje máximo de rama

Las Ultis no aparecen automáticamente por etapa y tampoco dependen del reparto de puntos de especialización.

### Principal
Disponible sólo si:
1. etapa >= **LianQi III**;
2. rama principal = **APRENDIDA_AL_MAXIMO**.

### Injertada
Disponible sólo si:
1. existe injerto elemental;
2. etapa >= **LianQi IV**;
3. rama injertada = **APRENDIDA_AL_MAXIMO**.

El aprendizaje máximo de una rama es un estado de progresión/conocimiento separado del build. **No se exige tener puntos en todas las especializaciones.** Una distribución `2/2/2` sigue siendo elegible, y cualquier otra distribución legal debe conservar la Ulti si la rama está aprendida al máximo.

Los generadores de casos deben calcular `ULTIMATE_UNLOCK_ELIGIBILITY` exclusivamente desde etapa + injerto cuando corresponda + estado de aprendizaje máximo de la rama. La distribución de puntos se usa después como variable del build.

## Invariantes de repertorio

1. máximo 2 Ultis equipadas;
2. máximo 1 del elemento principal;
3. máximo 1 del elemento injertado;
4. sólo se equipa/simula una Ulti si su gate de desbloqueo es válido para ese perfil;
5. la distribución de puntos de especialización nunca bloquea una Ulti ya elegible;
6. presupuesto compartido = 1 activación válida por combate;
7. tras activación válida, la otra queda bloqueada;
8. nunca ejecutar ambas en una misma simulación válida;
9. preservar cooldown OOC individual existente;
10. Pacto F3 conserva su autoridad.

## Envelopes por etapa

- **LianQi I–II:** no asumir Ultis.
- **LianQi III sin rama principal aprendida al máximo:** no Ulti principal.
- **LianQi III + rama principal aprendida al máximo:** 1 Ulti principal elegible, independientemente del build.
- **LianQi III + injerto:** el injerto no habilita todavía la Ulti injertada.
- **LianQi IV + injerto + rama injertada aprendida al máximo:** segunda Ulti elegible, independientemente del build.
- Con dos Ultis elegibles: siguen compartiendo un solo uso válido por combate.

## Suites mínimas nuevas

### U0 — UNLOCK_ELIGIBILITY
Valida etapa, injerto y aprendizaje máximo de rama antes de construir repertorio. Debe incluir pruebas donde builds distintas (incluida `2/2/2`) mantienen la misma elegibilidad.

### U1 — REPERTOIRE_CONTRACT
Valida asignación de slots y raíces únicamente con Ultis elegibles.

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
Comprueba efectos de Ultis que potencian acciones/técnicas posteriores usando las técnicas reales autorizadas, no fixtures sintéticos cuando ya exista autoridad.

### U9 — CROSS_ROOT_REPERTOIRE
Compara todos los repertorios legales principal/injertado con CRN pareado y respetando disponibilidad por etapa/aprendizaje máximo, sin convertir el reparto de puntos en gate.

### U10 — ORDER_WORKER_RESUME_SHARD
Demuestra equivalencia serial vs 5 notebooks, reanudación desde checkpoint, cambio de workers y consolidación.

## Gate de balance

Las pruebas mecánicas pueden dar PASS sin declarar balance CANON.

La decisión de balance debe considerar simultáneamente:
- potencia de técnicas normales;
- etapa y aprendizaje real de la rama del perfil;
- diferentes builds/distribuciones de puntos;
- coste de oportunidad de gastar la única Ulti del combate;
- elección entre las dos Ultis equipadas cuando ambas existan;
- fase de uso;
- supervivencia;
- daño/tempo/control;
- Pacto;
- identidad elemental;
- regret y polarización cross-root.

No usar un target win-rate aislado ni auto-optimizar hacia igualdad numérica.
