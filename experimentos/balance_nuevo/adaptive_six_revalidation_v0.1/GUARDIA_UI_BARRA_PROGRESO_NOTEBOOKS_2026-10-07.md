# Guardia UI — barra de progreso de notebooks

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: HUMAN_DECISION / ESTÁNDAR VISUAL DEL FRENTE

## Regla

Los próximos notebooks de simulación deben usar una barra de progreso compacta y legible, no la barra larga por defecto de tqdm.

## Estilo esperado

- ancho aproximado: media línea / barra visual de ~24-30 bloques;
- porcentaje visible;
- completado / total;
- tiempo transcurrido;
- ETA;
- velocidad;
- fase actual;
- chunk/checkpoint actual cuando corresponda.

## Estados visuales

- ejecución normal: color principal estable;
- lectura/recuperación de checkpoint: **amarillo**;
- fase terminada: verde;
- error/bloqueo técnico: rojo cuando la UI lo permita.

La transición a amarillo debe ser temporal mientras se procesa un checkpoint y volver luego al color normal.

## Formato orientativo

`3/4 Root passive recalibration  29% |███████················| 81,288/278,400  01:09<03:15  1.0k fight/s`

Al recuperar checkpoint:

`3/4 Root passive recalibration  42% |██████████·············| checkpoint 8/23`

## QA

Antes de entregar:
- comprobar que la barra realmente se renderiza en Colab;
- comprobar el cambio visual de checkpoint;
- comprobar que no ocupe todo el ancho de pantalla;
- comprobar ETA y contador;
- mantener checkpoints funcionales;
- no sacrificar rendimiento por la UI.

No main. No merge. No cambio de balance.
