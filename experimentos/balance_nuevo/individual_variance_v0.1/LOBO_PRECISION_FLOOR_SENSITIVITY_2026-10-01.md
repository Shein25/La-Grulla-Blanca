# Lobo — sensibilidad del piso de PREC en variabilidad individual

Fecha: 2026-10-01

## Motivo

El Heavy original de `INDIVIDUAL_VARIANCE_LAB` heredó del trial 1463 un
`precision=96` como parte de la envolvente superior del Lobo, mientras el T0
ratificado tiene `precision=97`.

Eso permitía una variación descendente de un punto y contradecía el contrato:

`T0 = piso natural`.

Se corrigió la envolvente a:

```text
PREC base  = 97
PREC upper = 97
```

No se inventó un aumento nuevo.

## Revalidación focalizada

Corrida CI posterior a la corrección:

- 10.000 encuentros naturales;
- 2.500 Mutantes condicionados;
- mismos 10 contextos (5 raíces × 2 loadouts);
- T0 variable;
- T1–T4 no ejecutados.

Resultados:

```text
Incidencia Mutante natural: 0,790%
Victoria jugador normal:   26,4993%
HP final jugador normal:     6,7406%

Victoria vs Mutante:         0,6400%
HP final vs Mutante:         0,1444%
```

Heavy previo:

```text
Victoria jugador normal ≈ 26,72%
Victoria vs Mutante      ≈  1,19%
```

La diferencia no cambia la lectura de diseño: la población variable del Lobo
sigue siendo una amenaza APEX_BRIDGE muy alta y la cola Mutante sigue siendo
casi un mini-jefe natural.

## Guardia permanente

`individual_variance.py` falla si cualquier stat declara:

```text
upper_envelope < T0 base
```

Por tanto no hace falta repetir la sensibilidad de 12.500 peleas en cada
commit. El smoke general de combate permanece en CI.
