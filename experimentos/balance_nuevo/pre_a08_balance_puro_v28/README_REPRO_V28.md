# Reproducibilidad V28
El paquete ZIP adjunto trae las carpetas `grulla_v21_work/`, `grulla_v24_balance_only/`, `grulla_v27_balance_only/` y `grulla_v28_balance_only/` con dependencias locales. Requiere Python 3.11+ y pandas. Ejecutar:
```
python grulla_v28_balance_only/test_v28_contract.py
python grulla_v28_balance_only/run_v28_native_bridge.py --cohort CHECKS
python grulla_v28_balance_only/run_v28_native_bridge.py --cohort DISCOVERY --start 102100 --reps 2
python grulla_v28_balance_only/run_v28_native_bridge.py --cohort HOLDOUT --start 102500 --reps 2
python grulla_v28_balance_only/run_v28_native_bridge.py --cohort COLD --start 102100 --reps 1
python grulla_v28_balance_only/analyze_v28.py
```
COLD reconstruye 43.200 filas (42 columnas salvo cohorte) y no cuenta como combate nuevo. Las dos rutas `CONNECTED_ONLY` y `VER74_BASIC_DIRECT` son **diagnósticas**, no valores canónicos. No tocar HTML, `main` ni economía.
