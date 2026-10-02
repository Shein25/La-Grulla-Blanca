# GRULLA F3 — Pacto del Último Vuelo

Fecha: 2026-10-02

Estado: **DECISIÓN HUMANA CERRADA / LAB CONTRACTUAL / NO MAIN / NO MERGE / NO PUSH**

## Objetivo

Evitar que una Definitiva permita borrar por completo la Fase III de la Grulla antes de que el jugador llegue a enfrentar al menos una intención real de esa fase.

La solución pertenece a la **Grulla**, no al balance numérico de las Ultis.

## Regla autoritativa

Al entrar en Fase III, la Grulla obtiene `PACTO_ULTIMO_VUELO`.

Mientras el Pacto esté activo:

1. Todo daño se resuelve normalmente.
2. Absorción, DEF, crítico, DOT, Hemorragia, conversión y demás primitivas conservan su orden normal.
3. Si un compromiso de daño a Vida llevaría a la Grulla a `HP <= 0`, su Vida queda en **1 HP**.
4. No se reduce ni se borra el daño calculado: el exceso se registra como `prevented_lethal_damage` / `overkill_prevented`.
5. El Pacto protege también contra paquetes posteriores de la misma acción. Una Ulti multi-hit no puede saltarse la Fase III con su segundo golpe.
6. El Pacto no cura, no limpia estados, no restaura Absorción y no concede reducción de daño.
7. La Grulla sigue pudiendo quedar en 1 HP y conservar todos los estados que recibió.

El Pacto se libera **solamente después de que se resuelva una intención real de Fase III de la Grulla**.

- Un intento de acción impedido por Control/incapacidad **no libera** el Pacto.
- Mostrar una intención sin resolverla **no libera** el Pacto.
- Después de la primera intención F3 realmente resuelta, cualquier fuente de daño puede matar a la Grulla normalmente.

## Estado en dos etapas

Para UI/telemetría se permite distinguir:

- `ACTIVE`: todavía no hubo daño letal prevenido.
- `CRACKED_WAITING_FOR_F3_ACTION`: ya se previno al menos un letal, pero la protección sigue vigente hasta la primera intención F3 resuelta.
- `RELEASED`: la Grulla ya ejecutó una intención real F3; no existe más death-gate.

La transición visual de "pacto roto" puede ocurrir al primer letal prevenido, pero **la protección mecánica no desaparece hasta `RELEASED`**.

## Fuentes cubiertas

El death-gate se aplica al compromiso final de Vida, independientemente de la fuente:

- daño directo;
- golpes múltiples;
- DOT;
- Hemorragia;
- daño derivado o convertido;
- retaliación/reflejo;
- cualquier otra fuente que comprometa Vida.

No modifica las reglas internas de esas fuentes.

## Invariantes

- `F3_KILL_BEFORE_FIRST_REAL_ACTION == 0`.
- No puede existir una ruta multi-hit que mate a la Grulla durante `ACTIVE` o `CRACKED_WAITING_FOR_F3_ACTION`.
- El Pacto no debe consumir turnos ni introducir reloj nuevo.
- No usa `Date.now()`, timers ni tiempo real.
- No altera Ultis.
- No altera la IA de la Grulla.
- No modifica F1 ni F2.

## Telemetría obligatoria para benchmark

Registrar al menos:

- `f3_gate_active`;
- `f3_gate_state`;
- `f3_lethal_preventions`;
- `f3_skip_attempted`;
- `f3_skip_source`;
- `f3_prevented_lethal_damage`;
- `f3_max_single_overkill_prevented`;
- `f3_first_real_action_resolved`;
- `f3_gate_release_turn`;
- `player_actions_after_gate_release_to_kill`.

## Criterio de experiencia

Una Fase III válida debe contener al menos una acción/intención real de la Grulla.

El benchmark puede medir cuántas veces una Ulti **habría** saltado la fase, pero el encuentro no lo permite.

## Fuente pendiente de integración

La rama `experiment/grulla-v2-final-boss-lab-v0.1` en su HEAD actual expone el monolito `grulla-blanca_ver74.html`, pero no contiene una implementación identificable de la Grulla F1–F3 sobre la cual aplicar el hook sin inventar identificadores o rutas.

Por lo tanto:

- esta decisión queda cerrada;
- el helper LAB queda implementado y probado;
- **la inserción en runtime productivo queda DEFER hasta disponer del source real del jefe**;
- no se parchea a ciegas el monolito.
