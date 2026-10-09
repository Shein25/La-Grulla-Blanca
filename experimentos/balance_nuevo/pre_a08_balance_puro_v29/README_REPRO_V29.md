# PRE-A08 V29 — reproducibilidad

El código ejecutable, dependencias locales, RAW CSV.gz, matrices de confianza agrupadas y QA completa se encuentran en el ZIP entregado en esta conversación. No es código del runtime.

ZIP: `GRULLA_PRE_A08_V29_BALANCE_PURO_GOLPE_Y_TRATAMIENTOS_2026-10-09.zip`.
SHA256: `f5e6f20e82bcb467fe3b9495d451b9c99fb79de0a6f758bbf56e978949cfcde6`.

Python 3.11+; pandas y numpy. Extraer el archivo preservando carpetas hermanas y ejecutar:
```bash
python grulla_v29_balance_only/test_v29_contract.py
python grulla_v29_balance_only/run_v29_timing.py --cohort CHECKS
python grulla_v29_balance_only/run_v29_timing.py --cohort DISCOVERY --start 103100 --reps 2
python grulla_v29_balance_only/run_v29_timing.py --cohort HOLDOUT --start 103500 --reps 2
python grulla_v29_balance_only/run_v29_timing.py --cohort COLD --start 103100 --reps 1
python grulla_v29_balance_only/analyze_v29.py
python grulla_v29_balance_only/bootstrap_v29.py
```

COLD reconstruye 40.320 filas con 44 columnas idénticas a la primera repetición DISCOVERY salvo `cohort`. No contar COLD como combate nuevo. No duplicar primeros encuentros entre siete tratamientos. Los intervalos agrupados de T2 se computan por primer encuentro y no por monstruo de continuación.

`VER74_BASIC_DIRECT` es una variante diagnóstica; no modificar el registro de monstruos ni aprobar aplicación por mero impacto. No comercio ni runtime.
