# Cómo reproducir PRE-A08 V26

1. Extraer ZIP de V26 en un directorio vacío conservando sus tres carpetas hermanas: `grulla_v26_balance_only`, `grulla_v24_balance_only`, `grulla_v21_work`.
2. Python 3.11+ con `pandas` instalado.
3. Ejecutar desde el directorio padre de esas carpetas:

```bash
python grulla_v26_balance_only/run_v26_conditional.py --name CHECKS
python grulla_v26_balance_only/run_v26_conditional.py --name DISCOVERY --start 100100 --reps 4
python grulla_v26_balance_only/run_v26_conditional.py --name HOLDOUT --start 100500 --reps 4
python grulla_v26_balance_only/run_v26_conditional.py --name COLD --start 100100 --reps 1
python grulla_v26_balance_only/analyze_v26.py
```

DISCOVERY y HOLDOUT hacen 73.728 duelos **nuevos** en total. COLD 9.216 filas **duplicadas para auditoría**, no sumarlas; `RAW` en gzip. Todas las variables son hipótesis locales sobre V17 y no pasan al runtime.

Comercio/precios fuera de alcance. Monstruos V19 originales. Sin HTML/A07/main/merge/ROOMS.exits. La Sobretúnica DEF+1 es solamente candidata. El adaptador especial de evasión se usa **simétricamente en ambos brazos**.