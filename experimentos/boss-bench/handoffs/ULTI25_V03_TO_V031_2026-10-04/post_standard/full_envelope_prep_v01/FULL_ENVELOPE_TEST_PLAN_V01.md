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
- estado de progresión por perfil: etapa LianQi, maestría de rama principal, existencia de injerto y maestría de rama injertada;
- regla explícita sobre intento de Ulti rechazado y consumo del presupuesto;
- regla de legalidad para primary==grafted si llegara a ser relevante.

Cualquier ausencia debe producir `AUTHORITY_REQUIRED`, nunca un valor inventado.

## Gate de desbloqueo por maestría

Las Ultis no aparecen automáticamente por etapa.

### Principal
Disponible sólo si:
1. etapa >= **LianQi III**;
2. maestría completa de la rama principal.

### Injertada
Disponible sólo si:
1. existe injerto elemental;
2. etapa >= **LianQi IV**;
3. maestría completa de la rama injertada.

Para ambas ramas, "maestría completa" significa haber progresado lo suficiente como para **poder asignar al menos 1 punto en cada especialización de esa rama**. No requiere haber gastado efectivamente un punto en todas.

Los generadores de casos deben calcular `ULTIMATE_UNLOCK_ELIGIBILITY` antes de generar cualquier política de uso de Ulti.

## Invariantes de repertorio

1. máximo 2 Ultis equipadas;
2. máximo 1 del elemento principal;
3. máximo 1 del elemento injertado;
4. sólo se equipa/simula una Ulti si su gate de desbloqueo es válido para ese perfil;
5. presupuesto compartido = 1 activación válida por combate;
6. tras activación válida, la otra queda bloqueada;
7. nunca ejecutar ambas en una misma simulación válida;
8. preservar cooldown OOC individual existente;
9. Pacto F3 conserva su autoridad.

## Envelopes por etapa

- **LianQi I–II:** no asumir Ultis.
- **LianQi III sin maestría principal:** no Ulti principal.
- **LianQi III + maestría principal:** 1 Ulti principal elegible.
- **LianQi III + injerto:** el injerto no habilita todavía la Ulti injertada.
- **LianQi IV + injerto + maestría injertada:** segunda Ulti elegible.
- Con dos Ultis elegibles: siguen compartiendo un solo uso válido por combate.

## Suites mínimas nuevas

### U0 — UNLOCK_ELIGIBILITY
Valida etapa, injerto y maestría antes de construir repertorio.

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
Compara todos los repertorios legales principal/injertado con CRN pareado y respetando disponibilidad por etapa/maestría.

### U10 — ORDER_WORKER_RESUME_SHARD
Demuestra equivalencia serial vs 5 notebooks, reanudación desde checkpoint, cambio de workers y consolidación.

## Gate de balance

Las pruebas mecánicas pueden dar PASS sin declarar balance CANON.

La decisión de balance debe considerar simultáneamente:
- potencia de técnicas normales;
- etapa y maestría real del perfil;
- coste de oportunidad de gastar la única Ulti del combate;
- elección entre las dos Ultis equipadas cuando ambas existan;
- fase de uso;
- supervivencia;
- daño/tempo/control;
- Pacto;
- identidad elemental;
- regret y polarización cross-root.

No usar un target win-rate aislado ni auto-optimizar hacia igualdad numérica.
