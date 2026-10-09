# V27 · Reproducibilidad sin red
ZIP: `GRULLA_PRE_A08_V27_BALANCE_PURO_AFLICCIONES_SECUENCIALES_2026-10-09.zip`.
Extraer toda la estructura de carpetas; requiere Python 3.11+ y pandas. Incluye `grulla_v27_balance_only/` más `grulla_v24_balance_only/run_v24_structural.py` y dependencias nativas LAB en `grulla_v21_work/`. Ver `MANIFEST_SHA256_V27.json` dentro del ZIP.

```bash
python grulla_v27_balance_only/run_v27_persistence.py --cohort CHECKS
python grulla_v27_balance_only/run_v27_persistence.py --cohort DISCOVERY --start 101200 --reps 2
python grulla_v27_balance_only/run_v27_persistence.py --cohort HOLDOUT --start 101600 --reps 2
python grulla_v27_balance_only/run_v27_persistence.py --cohort COLD --start 101200 --reps 1
python grulla_v27_balance_only/analyze_v27.py
```
`COLD` reejecuta casos históricos y **no** suma nuevos duelos. QA exacto: 53.760 filas (37 columnas salvo `cohort`). Las primeras peleas se calculan una vez por semilla/build/política/equipo y se comparten entre comparaciones, evitando inflar combates físicos. Aflicciones inyectadas al terminar primer combate (Jade I/Ceniza I); no es prueba de aplicación nativa del nuevo motor. Sobretúnica DEF1 solo candidata. No precios/economía, no canon/HTML.
