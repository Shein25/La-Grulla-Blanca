# V25 balance puro: reproducibilidad
Paquete portable adjunto: `GRULLA_PRE_A08_V25_BALANCE_PURO_EMBALSE_SENSIBILIDAD_2026-10-09.zip`; SHA256 `6be1c3a41fce22230f60dd6d0d2eb21c4d6f2ab5c293a30bed3443a6fd3ed2e8`. Extraer tres directorios hermanos: `grulla_v25_balance_only`, `grulla_v24_balance_only` y `grulla_v21_work`. Python 3.11+ con pandas.

```bash
python grulla_v25_balance_only/run_v25_embalse_sensitivity.py --cohort DISCOVERY --start 99700 --reps 4
python grulla_v25_balance_only/run_v25_embalse_sensitivity.py --cohort HOLDOUT --start 99800 --reps 4
python grulla_v25_balance_only/run_v25_embalse_sensitivity.py --cohort COLD --start 99700 --reps 1
python grulla_v25_balance_only/run_v25_multihit_probe.py
python grulla_v25_balance_only/conditional_preflight_v25.py
python grulla_v25_balance_only/analyze_v25.py
```
Recuento nuevo: 46.080 duelos; COLD 5.760 filas reproducidas NO añadidas; scripted 36.000 trayectorias NO duelos. Escalas 0,30/0,60/1,00 y 1,00 multihit son sensibilidades extremas no propuestas. Condicionales permanecen sin ejecución física. Ni comercio ni HTML ni canon.
