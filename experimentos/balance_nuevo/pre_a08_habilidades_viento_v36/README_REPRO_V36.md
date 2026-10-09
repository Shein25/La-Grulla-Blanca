# V36 — Reproducibilidad y contrato
Archivo portable entregado por conversación: `GRULLA_PRE_A08_V36_AJUSTE_HABILIDADES_VIENTO_2026-10-09.zip` · SHA256 `71389d6803c7081cc61568cd2804089cca1ed0dd9811819a854b2d70699c9bb9` · 104 entradas CRC+manifiesto SHA PASS.

Código reproducible completo **NO subido a Git** (archivado en ZIP): `run_v36_wind_skills.py`, `run_v36b_wind_nodes.py`, `run_v36c_minimal.py`, `analyze_v36_wind.py` más dependencias y CSV brutos. Python 3.11+, pandas; extraer preservando carpetas hermanas `grulla_v35_viento_normal_elite_preflight/` y `v32_equip_progression/grulla_v21_work/`.

```bash
python grulla_v35_viento_normal_elite_preflight/run_v36_wind_skills.py --cohort COLD --start 113100 --reps 1
python grulla_v35_viento_normal_elite_preflight/run_v36b_wind_nodes.py --cohort COLD --start 114100 --reps 1
python grulla_v35_viento_normal_elite_preflight/run_v36c_minimal.py --cohort COLD --start 114100 --reps 1
python grulla_v35_viento_normal_elite_preflight/analyze_v36_wind.py
```

Los tres comandos COLD son **23.040 filas de repetición**, no simulaciones nuevas; las columnas CSV descomprimidas se reproducen exactamente en carpeta limpia (los bytes del contenedor gzip pueden variar por marcas de tiempo del header). Para reprocesar discovery/holdout, usar --cohort DISCOVERY --start 113100/114100 --reps 2 y --cohort HOLDOUT --start 113500/114500 --reps 2, según V36A vs B/C. El analizador audita pareo, preservación de equipo y diferencias por kit, build y monstruo.

**No implementar automáticamente** en HTML: ajustes V36 en estado CANDIDATO. El hallazgo V35 fue un problema de activación V17 del LAB, no un error productivo confirmado. El cierre numérico de seis monstruos normales V35 permanece vigente. Próximo frente: élite Eco del Caído.
