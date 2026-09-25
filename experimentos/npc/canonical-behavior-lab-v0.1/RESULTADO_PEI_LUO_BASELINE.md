# Resultado baseline — Pei Luo / LAB v0.1

## Alcance

Segundo ensayo de comportamiento sobre un NPC canónico, sin integración con producción.

Canon usado: `NPC_DEF.pei_luo` de `grulla-blanca_ver74.html`.

Motores:

- Reactive Routine FSM v0.1 REV2 — snapshot auditado.
- Behavior Tree v0.1 REV2 — snapshot auditado.

## Separación canon / hipótesis

Canónico:

- responsable de Cocina/Comedor;
- sala inicial `cocina_comunal`;
- ruta `cocina_comunal ↔ comedor_externos`;
- sin tránsito técnico;
- M16: organiza raciones durante la crisis.

Experimental:

- fases normales de preparación, servicio, retorno y reset;
- nombres concretos de intents de la rutina normal.

La respuesta `ORGANIZE_CRISIS_RATIONS` está tratada como hipótesis de política respaldada por el dato canónico de M16, no como literal del juego.

## Verificación

```text
PASS: 21
FAIL: 0
```

## Escenario 1 — rutina experimental

FSM:

```text
PREP
  SERVICE_DUE
    ↓
MOVE_OUT       / MOVE_TO_DINING
    ↓
SERVE          / SERVE_RATIONS
    ↓
RETURN         / RETURN_KITCHEN
    ↓
RESET          / RESET_KITCHEN
    ↓
PREP           / PREPARE_RATIONS
```

Behavior Tree produce la misma secuencia observable:

```text
MOVE_TO_DINING
SERVE_RATIONS
RETURN_KITCHEN
RESET_KITCHEN
PREPARE_RATIONS
```

Sin falsas preempciones entre acciones que terminaron con `SUCCESS`.

## Escenario 2 — crisis durante servicio

FSM:

```text
SERVE
  ↓ CRISIS
CRISIS / ORGANIZE_CRISIS_RATIONS
  ↓ CRISIS_ENDED
RETURN
  ↓
RESET
  ↓
PREP
```

Behavior Tree:

```text
serve RUNNING
   ↓ crisis=true
serve PREEMPTADA
   ↓
ORGANIZE_CRISIS_RATIONS
   ↓
RETURN_KITCHEN
   ↓
RESET_KITCHEN
   ↓
PREPARE_RATIONS
```

## Escenario 3 — crisis durante preparación

FSM entra directamente:

```text
PREP → CRISIS → RETURN → RESET → PREP
```

Behavior Tree:

```text
prepare RUNNING
   ↓ crisis=true
prepare PREEMPTADA
   ↓
ORGANIZE_CRISIS_RATIONS
```

y luego retorna a la rutina experimental.

## Observación técnica

A diferencia del baseline de Gao Shun, aquí los dos motores generan exactamente la misma secuencia observable durante la rutina normal.

La diferencia aparece cuando una prioridad extraordinaria interrumpe el trabajo:

- FSM expresa explícitamente el modo `CRISIS` y la recuperación posterior;
- Behavior Tree muestra la interrupción de la acción activa mediante preempción y reevaluación de prioridad.

Todavía no se asigna un motor definitivo a Pei Luo.
