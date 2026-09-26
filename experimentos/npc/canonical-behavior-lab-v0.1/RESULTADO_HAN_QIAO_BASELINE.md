# Han Qiao — baseline de compañero / LAB v0.1

## Objetivo

Probar un compañero orientado a recursos/logística bajo conflicto entre ayuda social y deber institucional.

## Canon relevante

- aspirante — recursos/contactos, logística;
- territorio base: Oficina de Servicios / Patio de Servicios / Depósito Común;
- M16: anclado en Recursos/Logística; responsable/apoyo del frente RECURSOS;
- epílogo: HERENCIA_APROPIADA.

## Perfil experimental

Traits y relación base son `EXPERIMENTAL_NON_CANONICAL`.

## Escenario A — solicitud ordinaria

Con deber bajo y sin superior alcanzable, el perfil de calibración debe preferir:

```text
ayudar_jugador
→ HELP_PLAYER
→ [ir_jugador, ayudar_jugador]
```

## Escenario B — M16 Recursos

Mismo jugador solicitando ayuda, pero:

- dutyImportance alto;
- dutyPending=true;
- danger/urgency elevados;
- dutyMode=trabajar;
- superior no alcanzable.

La expectativa es que el deber de recursos domine:

```text
trabajar
→ FULFILL_DUTY
→ [cumplir_deber]
```

Esto mide una prioridad contextual, no una personalidad canónica definitiva.

## Gap de dominio material

El GOAP actual representa `cumplir_deber` sólo como:

```text
dutyPending=false
dutySatisfied=true
```

No representa cantidades, inventario, raciones, carros, reservas, destinos ni asignación concreta de recursos.

Por tanto:

`RESOURCE_ALLOCATION_AND_LOGISTICS = CANONICAL_DOMAIN_CAPABILITY_GAP`

El baseline puede comprobar prioridad y finalización simbólica, pero todavía no simula logística material real.

## Estado

`HAN_QIAO_COMPANION_BASELINE: 14_PASS_0_FAIL_RUNTIME_CONFIRMED`


## Ejecución confirmada

Resultado:

```text
PASS: 14
FAIL: 0
```

### Solicitud ordinaria

```text
ayudar_jugador
→ HELP_PLAYER
→ [ir_jugador, ayudar_jugador]
→ GOAL_REACHED
→ playerHelped = true
```

### M16 Recursos

```text
trabajar
→ FULFILL_DUTY
→ [cumplir_deber]
→ GOAL_REACHED
→ dutySatisfied = true
```

El mismo jugador estaba solicitando ayuda; el cambio de contexto hizo que el deber logístico experimental dominara.

### Límite material confirmado

La acción real `cumplir_deber` tiene únicamente:

```text
effects:
  dutyPending   = false
  dutySatisfied = true
```

No modela asignación de recursos.
