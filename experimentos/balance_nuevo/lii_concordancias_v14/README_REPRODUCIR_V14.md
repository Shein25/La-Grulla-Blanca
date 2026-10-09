# Reproducción V14

Extraer `GRULLA_LII_V14_RELACIONES_PENDIENTES_2026-10-09.zip` sin cambiar nombres de carpetas.

Requiere Python 3, `pandas` y `numpy`. El paquete incluye las fuentes de laboratorio V07/V10/V11/V12/V13 para que los `import` relativos resuelvan correctamente.

Ejecutar desde el directorio extraído:

```
python GRULLA_LII_CONCORDANCE_V14/run_v14.py --reps 4
python GRULLA_LII_CONCORDANCE_V14_HOLDOUT/run_v14.py --reps 4
python GRULLA_LII_CONCORDANCE_V14/audit_conditional_v14.py
python GRULLA_LII_CONCORDANCE_V14/compare_v14.py
```

**Aviso:** los runners sobreescriben los CSV de su carpeta. Ejecutar sobre **otra copia** del ZIP si se desea conservar las huellas del archivo entregado. Las pruebas numéricas prueban magnitudes de sensibilidad NO canónicas; el HTML de juego NO se ejecuta ni modifica. No hay gates de élite, T3/T4 o aprendices LI.