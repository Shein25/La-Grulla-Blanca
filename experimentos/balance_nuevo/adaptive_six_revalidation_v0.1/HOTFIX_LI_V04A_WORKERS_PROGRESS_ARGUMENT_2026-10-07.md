# Hotfix LI V04A — workers/progress argument

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: RUNNER HOTFIX ONLY / SIN CAMBIO DE BALANCE

## Error

El helper:

`run_jobs_weighted(jobs, func, phase_dir, workers, phase_label)`

requiere cinco argumentos, pero V04A invocaba las cuatro fases sin pasar `args.workers`.

Esto provoca un `TypeError` y el subprocess termina con exit status 1 antes de iniciar la campaña.

## Corrección

Las cuatro fases pasan explícitamente:
- `args.workers`;
- luego su `phase_label`.

Además, el notebook fija `WORKERS = 2` para el runtime Colab conocido de 2 CPU lógicas.

## Guardia

NO cambia:
- seeds;
- R;
- grids;
- relaciones;
- raíces candidatas;
- equipo candidato;
- monstruos;
- técnicas;
- Concordancias;
- criterios;
- checkpoints.

No main. No merge. No runtime productivo. No auto-freeze.
