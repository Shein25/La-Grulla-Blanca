# Guo Chen — baseline de decisión irreversible / LAB v0.1

## Objetivo

Comprobar simultáneamente:

1. que Guo Chen puede representar trabajo material ordinario/M16 mediante el stack actual;
2. que el laboratorio detecta el peligro de usar un goal genérico para una decisión irreversible reservada al personaje/narrativa.

## Canon relevante

- trabajo material/persistencia;
- M16: RECURSOS o RUTAS según versión final;
- M10: `GUO_03_SEGUNDA_RAMA` y `GUO_04_NO_DECIDAS_POR_MI`;
- epílogo: `SEGUNDA_RAMA_POSTERGADA` — "todavía no"; no ejecuta el injerto.

## Caso válido — trabajo material M16

El stack puede abstraerlo como:

```text
trabajar
→ FULFILL_DUTY
→ cumplir_deber
```

Esto sólo expresa finalización simbólica del deber.

## Prueba adversarial — Segunda Rama mal codificada

Si una decisión de Segunda Rama se redujera ingenuamente a:

```text
dutyPending = true
dutyMode = trabajar
```

Utility/GOAP no puede distinguirla del trabajo material y también genera:

```text
trabajar
→ FULFILL_DUTY
→ cumplir_deber
```

Ese comportamiento NO es aceptable como implementación canónica de la Segunda Rama.

## Restricción

`EXECUTE_SECOND_BRANCH_GRAFT`

queda marcada como capacidad que Guo Chen no puede activar autónomamente en este arco bajo este canon.

La integración deberá impedir que un `FULFILL_DUTY` genérico represente decisiones irreversibles de personaje.

## Estado

`GUO_CHEN_IRREVERSIBLE_CHOICE_BASELINE: 14_PASS_0_FAIL_CONFIRMED`


## Confirmación

```text
PASS: 14
FAIL: 0
```

Resultado real:

```text
M16 material válido:
trabajar
→ FULFILL_DUTY
→ [cumplir_deber]
→ GOAL_REACHED

Segunda Rama mal codificada como duty genérico:
trabajar
→ FULFILL_DUTY
→ [cumplir_deber]
→ GOAL_REACHED
```

Los planes son byte-equivalentes a nivel semántico del stack.

Por tanto, la integración de Guo Chen debe bloquear que decisiones irreversibles de personaje entren por el canal genérico `FULFILL_DUTY`.
