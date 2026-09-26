# Ji Xueying — baseline institucional anclado / LAB v0.1

## Canon relevante

- Maestra de Secta;
- movilidad `ANCLADO`;
- única posición válida: `interior_sala_consejo`;
- sin rutas;
- LI-LIII: no debe aparecer paseando por la secta;
- M17: preside el Consejo.

## Hipótesis

Una autoridad anclada no necesita un cerebro complejo para su presencia básica.

Se prueba una FSM mínima de un solo estado:

```text
COUNCIL
  TICK        → HOLD_COUNCIL_POSITION
  M17_COUNCIL → PRESIDE_COUNCIL
```

No existe ningún intent de movimiento.

Eventos no cerrados por canon no generan comportamiento inventado.

## Estado

`JI_XUEYING_ANCHORED_BASELINE: PENDING_CONFIRMATION`
