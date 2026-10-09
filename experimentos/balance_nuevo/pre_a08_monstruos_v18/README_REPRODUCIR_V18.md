# V18 · Reproducción en Python local o Colab

El ZIP V18 incluye tres carpetas hermanas:
- `GRULLA_PRE_A08_MONSTRUOS_V18/` — código de prueba y resultados.
- `GRULLA_PRE_A08_HABILIDADES_CIERRE_V17/` — overlay V17 (dos scripts + perfil de habilidades).
- `GRULLA_LII_TRAMO1_BALANCE_V07/` — fuentes congeladas del puente de combate, catálogos y monstruos.

Descomprimir en una carpeta cualquiera. Con Python 3, pandas y módulos de la biblioteca estándar disponibles:

```
python GRULLA_PRE_A08_MONSTRUOS_V18/run_screen_v18.py --label DISCOVERY --start 71000 --reps 4
python GRULLA_PRE_A08_MONSTRUOS_V18/run_screen_v18.py --label HOLDOUT --start 72000 --reps 4
python GRULLA_PRE_A08_MONSTRUOS_V18/analyze_v18.py
python GRULLA_PRE_A08_MONSTRUOS_V18/run_micro_v18.py --label DISCOVERY --start 73000 --reps 4
python GRULLA_PRE_A08_MONSTRUOS_V18/run_micro_v18.py --label HOLDOUT --start 74000 --reps 4
```

**Atención:** los comandos regeneran los CSV de resultados de la carpeta V18, de modo que guarde copia previa si quiere comparar hashes del paquete. Para smoke tests use extracción independiente y `--reps 1`, manteniendo las semillas 71000 y 73000. El script de compilar V17 crea una tabla de regresión de nodos en la carpeta V17 de la extracción; no altera el juego ni Git.

El paquete no contiene HTML integrado ni ejecuta Concordancias ON. No se probaron pociones, antídotos, compra o extracción. `CARRY_OVER_LI_HIGH` es una referencia de estrés y `EXPECTED_STAGE` es un kit candidato cuya obtención hay que cerrar.

Se recomienda no promover parámetros de supervivencia T1 ni stats de monstruos hasta revisar el dictamen, la QA y la disponibilidad del equipo. Todas las partidas y modificaciones de knobs suceden en el adaptador Python en RAM, nada se implementa en runtime.