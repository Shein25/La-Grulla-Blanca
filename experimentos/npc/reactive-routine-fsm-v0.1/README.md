# Reactive Routine FSM v0.1 — Laboratorio NPC

Experimento aislado para cubrir NPC sencillos que necesitan **rutina + reacción**, sin cargar Utility AI, GOAP ni Autonomous NPC Loop.

## Hipótesis

Una FSM declarativa pequeña debería cubrir bien tres patrones frecuentes del canon de 32 NPC:

1. guardia reactivo;
2. trabajador con ciclo de rutina;
3. patrullero que investiga y regresa a su puesto.

Los fixtures son sintéticos. No modifican ni sustituyen a Gao Shun, Pei Luo, Ren Bo ni ningún NPC canónico.

## Principio

```text
estado actual + evento observable
            ↓
       guarda declarativa
            ↓
      transición única
            ↓
       intent(s) emitidos
```

El motor **no ejecuta efectos del mundo**. Sólo cambia su estado interno y emite IDs de intención para una capa externa futura.

## API

```js
validateMachine(machine)
createRuntime(machine)
stepFSM(machine, runtime, event)
```

`stepFSM()` es determinista, no muta inputs y procesa como máximo una transición por evento.

## Contrato v0.1 REV2

- máquinas, estados y transiciones son datos declarativos;
- no se admiten callbacks dentro de la definición;
- prioridades de transiciones deben ser únicas por estado/evento;
- sólo una transición puede ganar por evento;
- el target debe existir;
- un evento no manejado conserva el estado;
- una transición resetea `stateAge` a 0;
- `stateAge` y `step` aumentan de a 1 hasta `Number.MAX_SAFE_INTEGER`; al alcanzar ese valor quedan saturados para preservar la validez del runtime;
- los intents emitidos son strings declarativos sin duplicados;
- facts aceptan únicamente primitivos JSON finitos;
- arrays contractuales no admiten huecos, accessors, Symbols ni propiedades extra;
- se rechazan accessors, Symbols, herencia y campos extra en estructuras contractuales;
- guards con `source:'runtime'` sólo pueden leer `machineId`, `state`, `stateAge` o `step`;
- `GT/GTE/LT/LTE` exigen un `value` numérico; sobre runtime sólo pueden aplicarse a `stateAge` o `step`;
- la profundidad máxima de guardas compuestas es `MAX_GUARD_DEPTH = 32`;
- entradas hostiles que no puedan inspeccionarse deben cerrar con `ContractError`;
- `EQ/NEQ` usan `Object.is`, por lo que distinguen `-0` de `0`;
- un fact ausente produce `undefined`: `EQ/IN` no coinciden y `NEQ` se considera verdadero frente a cualquier valor declarable distinto de `undefined`;
- el motor no conoce rooms, gates, pathfinding, misiones, combate ni save/load de producción.

## Fixtures

- `fixture_guard` — puesto → patrulla → alerta → advertencia/combate → retorno.
- `fixture_worker` — preparación → servicio → limpieza; una alarma interrumpe la rutina.
- `fixture_patroller` — patrulla → investigación/combate → retorno.

## Ejecutar

```bash
node tests.mjs
node tests-rev2.mjs
node stress.mjs 100000 1337
```

La suite histórica v0.1 conserva sus 30 pruebas. REV2 añade 17 regresiones específicas para H1–H6 de la auditoría externa de Claude.

## Fuera de alcance

- horarios reales del mundo;
- pathfinding;
- duración física de acciones;
- NPC canónicos;
- diálogos;
- memoria social;
- Utility AI;
- GOAP;
- Behavior Trees;
- integración con `grulla-blanca_ver*.html`.

## Estado

`CANDIDATE_STATUS: REV2_PENDING_EXTERNAL_RETEST`
