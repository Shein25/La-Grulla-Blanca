# Reproducir V20 — equipamiento LII (no canónico)

Extraer ZIP. Requiere Python 3.11+ y `pandas`. Ejecutar desde la carpeta raíz extraída (las dependencias se resuelven por rutas hermanas). No se necesita red ni Colab.

```bash
python GRULLA_EQUIPO_LII_V20/run_v20.py --cohort DISCOVERY --start 91000 --reps 2
python GRULLA_EQUIPO_LII_V20/run_v20.py --cohort HOLDOUT --start 92000 --reps 2
python GRULLA_EQUIPO_LII_V20/run_v20_defense.py --cohort DISCOVERY --start 93000 --reps 4
python GRULLA_EQUIPO_LII_V20/run_v20_defense.py --cohort HOLDOUT --start 94000 --reps 4
python GRULLA_EQUIPO_LII_V20/run_v20_cross.py --cohort DISCOVERY --start 95000 --reps 4
python GRULLA_EQUIPO_LII_V20/run_v20_cross.py --cohort HOLDOUT --start 96000 --reps 4
python GRULLA_EQUIPO_LII_V20/run_v20_expected.py --cohort DISCOVERY --start 97000 --reps 4
python GRULLA_EQUIPO_LII_V20/run_v20_expected.py --cohort HOLDOUT --start 98000 --reps 4
python GRULLA_EQUIPO_LII_V20/analyze_v20.py
python GRULLA_EQUIPO_LII_V20/finalize_v20.py
```

Todas las variantes equipan objetos únicamente **en memoria**, manteniendo fijo el identificador de gear de semilla `POST_M03`, el monstruo, sus estadísticas originales, raíz, build, tier y política. Así, cada fila de contexto usa la misma semilla entre brazos. Los cambios experimentales de defensa y reacciones monstruosas se restauran después del duelo; el HTML original queda intacto.

**Advertencias:** el aprendizaje de técnica ajena está asumido, la Concordancia usa una relación BASE escalar de V17 por raíz principal, sin estructuras ni hooks condicionales. `M03_ISSUED` y `PROLOGUE` se tratan como dotaciones de referencia; los kits de piezas M04/M05 son hipótesis del catálogo Etapa18, no rutas de adquisición verificadas. Ninguna conclusión de este paquete autoriza modificar estadísticas o economía directamente.

Los CSV `.gz` de cada campaña, tabla de acceso, resumen, QA y hashes están dentro del ZIP junto al código fuente exacto del puente V07/V10/V11/V12/V17/V19. `MANIFEST_SHA256_V20.json` valida todos los miembros salvo sí mismo.