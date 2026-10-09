# PRE-A08 V34 — Reproducción
Paquete adjunto fuera de Git: `GRULLA_PRE_A08_V34_VALIDACION_MONSTRUOS_Y_PROGRESION_2026-10-09.zip` (SHA256 `c49ea86b9eb819348f547c53f3deaa50c60a8d5f9a31313bcef5a2f13488b558`, 56 archivos, CRC+manifiesto SHA PASS).

Desde la raíz extraída, Python 3.11+ y pandas:
```bash
python grulla_v34_monster_validation/run_v34_monster_stage.py --cohort CHECKS
python grulla_v34_monster_validation/run_v34_monster_stage.py --cohort DISCOVERY --start 111100 --reps 2
python grulla_v34_monster_validation/run_v34_monster_stage.py --cohort HOLDOUT --start 111500 --reps 2
python grulla_v34_monster_validation/run_v34_monster_stage.py --cohort COLD --start 111100 --reps 1
python grulla_v34_monster_validation/analyze_v34.py
```
`COLD` repite 34.560 filas ×32 columnas exactamente, excluyendo solo la columna `cohort`; no computarlo como nuevos duelos. Los RAW están en `grulla_v34_monster_validation`, las dependencias V17–V20 en `v32_equip_progression/grulla_v21_work`. No toca `main`, runtime, catálogo ni economía; Sobretúnica DEF+2/HP+2 intacta.
