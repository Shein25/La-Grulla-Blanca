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
- regla explícita sobre intento de Ulti rechazado y consumo del presupuesto;
- regla de legalidad para primary==grafted si llegara a ser relevante.

Cualquier ausencia debe producir `AUTHORITY_REQUIRED`, nunca un valor inventado.

## Invariantes de repertorio

1. máximo 2 Ultis equipadas;
2. máximo 1 del elemento principal;
3. máximo 1 del elemento injertado;
4. presupuesto compartido = 1 activación válida por combate;
5. tras activación válida, la otra queda bloqueada;
6. nunca ejecutar ambas en una misma simulación válida;
7. preservar cooldown OOC individual existente;
8. Pacto F3 conserva su autoridad.

## Suites mínimas nuevas

### U1 — REPERTOIRE_CONTRACT
Valida asignación de slots y raíces.

### U2 — SHARED_USE_BUDGET
Activa la Ulti primaria y demuestra que la injertada queda bloqueada; repetir invirtiendo orden.

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
Compara todos los repertorios legales principal/injertado con CRN pareado.

### U10 — ORDER_WORKER_RESUME_SHARD
Demuestra equivalencia serial vs 5 notebooks, reanudación desde checkpoint, cambio de workers y consolidación.

## Gate de balance

Las pruebas mecánicas pueden dar PASS sin declarar balance CANON.

La decisión de balance debe considerar simultáneamente:
- potencia de técnicas normales;
- coste de oportunidad de gastar la única Ulti del combate;
- elección entre las dos Ultis equipadas;
- fase de uso;
- supervivencia;
- daño/tempo/control;
- Pacto;
- identidad elemental;
- regret y polarización cross-root.

No usar un target win-rate aislado ni auto-optimizar hacia igualdad numérica.
