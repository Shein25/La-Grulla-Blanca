# V21 · Reproducir paquete focal (no canon)

Dependencias: Python 3.11+ y pandas. Extraer `GRULLA_EQUIPO_LII_V20_BALANCE_MARGINAL_2026-10-09.zip`, SHA256 `1d4834dd3d12b2ed34798975d59a25b2233277bc7ae5594f9e3665863c321851`, preservando `GRULLA_EQUIPO_LII_V20/` y módulos hermanos. Colocar `run_v21_focal_access.py` de este directorio al lado de `run_v20.py`.

```bash
python GRULLA_EQUIPO_LII_V20/run_v21_focal_access.py --cohort DISCOVERY --start 99100 --reps 2
python GRULLA_EQUIPO_LII_V20/run_v21_focal_access.py --cohort HOLDOUT --start 99200 --reps 2
```

Produce 28.160 combates, dos CSV `.gz`, resúmenes y QA. Un réplica en carpeta limpia con `--cohort DISCOVERY --start 99100 --reps 1` reprodujo 7.040 filas exactas. Cero timeout y acciones omitidas.

Paquete completo externo `GRULLA_PRE_A08_V21_ACCESO_ECONOMIA_Y_FOCAL_2026-10-09.zip`: SHA256 `d9f5b7e952c4c617c82b7fca9746a2e1aef15b8f6b0b42e9a54a936a4dd1e01a`, 56 archivos CRC PASS. El ZIP contiene datasets, QA por cohorte, dependencias y runner exacto. Datos grandes no incluidos en Git.

Los kits M03/Prólogo son referencias hipotéticas de diseño, NO adquisición comprobada en ver74; ninguna pieza nueva LII se equipa. V17 usa Concordancias BASE escalares representativas (no hooks estructurales/condicionales). Aflicciones y antídotos no se simulan. Consulta `DICTAMEN_AUDITORIA_Y_FOCAL_V21_2026-10-09.md`, `MATRIZ_21_LII_V21.csv` y `QA_V21_2026-10-09.json`. No ejecutar de nuevo las baterías V17–V20.

Guardias: sin main, sin merge, sin HTML/ROOMS.exits, sin compra con Contribución, sin canonizar cambios sin aprobación.
