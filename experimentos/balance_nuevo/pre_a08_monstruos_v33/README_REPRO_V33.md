# PRE-A08 V33 · Runners y reproducibilidad
Paquete externo: `GRULLA_PRE_A08_V33_MONSTER_BALANCE_FINALISTS_2026-10-09.zip`, SHA256 `97abd380cc48388431ed4887e1da63c3bd7027f349171f17d8c113109be23800`, 84 entradas con manifiesto y CRC verificados.

Extraer el ZIP preservando las carpetas hermanas `grulla_v33_monster_balance` y `v32_equip_progression/grulla_v21_work`; requiere Python 3.11+, pandas/numpy. Desde carpeta raíz:

```bash
python grulla_v33_monster_balance/run_v33_final_candidates.py --cohort CHECKS
python grulla_v33_monster_balance/run_v33_final_candidates.py --cohort DISCOVERY --start 110100 --reps 2
python grulla_v33_monster_balance/run_v33_final_candidates.py --cohort HOLDOUT --start 110500 --reps 2
python grulla_v33_monster_balance/run_v33_final_candidates.py --cohort COLD --start 110100 --reps 1
python grulla_v33_monster_balance/analyze_v33_monsters.py
```

Frío: 23.040 filas ×32 columnas iguales frente a DISCOVERY rep 110100, excluyendo columna `cohort`; no sumadas como nuevas. Código, perfiles de referencia, brutos y runners V33 exploratorio/V33B focal incluidos en ZIP. No cambiar `main`, la armadura ni el juego productivo.
