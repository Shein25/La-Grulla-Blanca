# Resultado inicial — Gao Shun / LAB v0.1

## Alcance

Primer ensayo de comportamiento sobre un NPC canónico, sin integración con producción.

Canon usado: `NPC_DEF.gao_shun` de `grulla-blanca_ver74.html`.

Motores:

- Reactive Routine FSM v0.1 REV2 — snapshot auditado.
- Behavior Tree v0.1 REV2 — snapshot auditado.

La política de reacción de este laboratorio es **experimental y no canónica**.

## Checks canónicos

- la ruta canónica completa está contenida en `posicion_valida`: PASS;
- `casa_guardia` está incluida en `posicion_valida`: PASS;
- no se añadió ninguna room al perfil canónico;
- no se modificó `conocimiento_inicial`.

## Escenario 1 — rutina

FSM:

```text
PATROL_DUE      -> PATROL       / PATROL_ROUTE
PATROL_COMPLETE -> RETURN       / RETURN_POST
ARRIVED         -> POST         / HOLD_POST
```

Behavior Tree:

```text
patrolDue=true              -> PATROL_ROUTE
patrol SUCCESS              -> sin nuevo intent
sin prioridad extraordinaria -> HOLD_POST
```

## Escenario 2 — escalada

FSM:

```text
SUSPICIOUS   -> OBSERVE / OBSERVE_TARGET
PERSISTS     -> WARN    / WARN_TARGET
HOSTILE      -> BLOCK   / BLOCK_PASSAGE
THREAT_ENDED -> RETURN  / RETURN_POST
ARRIVED      -> POST    / HOLD_POST
```

Behavior Tree:

```text
suspicious              -> OBSERVE_TARGET
persistentSuspicion     -> WARN_TARGET
hostile                 -> BLOCK_PASSAGE
fin de BLOCK + sin alerta -> HOLD_POST
```

El árbol preempta `warn` cuando aparece hostilidad.

## Escenario 3 — patrulla interrumpida

FSM cambia de `PATROL` a `BLOCK` en el evento hostil y luego usa un retorno explícito.

Behavior Tree preempta la acción `patrol` en el mismo tick y selecciona `BLOCK_PASSAGE`.

## Observación técnica inicial

Los dos motores pueden expresar el patrón de Gao Shun sin salirse del whitelist experimental.

La diferencia observada no se interpreta todavía como ganador:

- FSM conserva memoria explícita de fase y recuperación;
- Behavior Tree reevalúa prioridades directamente y hace visible la preempción;
- FSM modela `RETURN_POST` como fase propia;
- el árbol vuelve a `HOLD_POST` cuando la acción prioritaria termina y ya no existen hechos de alerta.

Este resultado sirve para diseñar los siguientes escenarios; todavía no asigna una IA definitiva a Gao Shun.
