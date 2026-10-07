# Hotfix LI Full System V03 — barra de progreso

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: UX/RUNNER HOTFIX ONLY / SIN CAMBIO DE BALANCE

## Alcance

Se agrega progreso visible al runner de:
- primary Concordance sweep;
- final all-root validation;
- equipment item marginal audit;
- T2 tail stress.

La barra muestra:
- porcentaje;
- jobs/contextos completados;
- combates representados completados / totales;
- velocidad;
- ETA.

## Checkpoints

Los chunks ya terminados:
- se reutilizan;
- cuentan inmediatamente como progreso completado;
- no se recalculan.

## Guardia

Este hotfix NO cambia:
- seeds;
- R;
- cohortes;
- magnitudes;
- Concordance resolver;
- equipo;
- técnicas;
- monstruos;
- criterios de verdict.

Es únicamente observabilidad de ejecución.

No main. No merge. No runtime. No auto-freeze.
