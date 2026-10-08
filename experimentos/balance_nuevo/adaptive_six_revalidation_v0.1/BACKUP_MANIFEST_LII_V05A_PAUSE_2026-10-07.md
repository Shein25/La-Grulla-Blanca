# BACKUP MANIFEST — Pausa LII en V05A

**Fecha de respaldo:** 2026-10-07  
**Repo:** `Shein25/La-Grulla-Blanca`  
**Rama de escritura:** `experiment/monster-adaptive-six-revalidation-v0.1`  
**Último estado de trabajo:** V04 auditado / V05A creado, estructuralmente validado, **NO EJECUTADO EN COLAB** / V05B pendiente.

## Objetos respaldados íntegros EN GIT

| Objeto | Ruta Git relativa a `adaptive_six_revalidation_v0.1/` | Verificación |
|---|---|---|
| Handoff integral | `HANDOFF_CONTINUO_LII_V05A_A_V05B_2026-10-07.md` | Guardado en la rama experimental |
| Notebook Colab V05A autocontenido | `notebooks/COLAB_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.ipynb` | **git blob `85fc561112bffc7c3c5bd5dec0282e35a2b268aa`**, igual al archivo local original |
| QA previo V05A | `notebooks/QA_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.json` | **git blob `10f6307851455a49ed29fc80db09e3160c060ea4`**, igual al archivo local original |
| Auditoría V04 y contexto | `LII_V04_EXHAUSTIVE_BALANCE_GATE_AUDIT_2026-10-08.md` | Commit de autoría `9479f44a00f8b2a090f72a0cdc17a4c6e7549263` |
| Cinco guardianes AOE | `DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md` | Commit `0f59db18357abadc168cd117d14aa0010e8453e2` |
| Este manifiesto | `BACKUP_MANIFEST_LII_V05A_PAUSE_2026-10-07.md` | Verificar mediante `fetch_file` |

**NOTA sobre los 4 runners:** el notebook V05A contiene su código fuente íntegro embebido en las celdas, no necesita ficheros `.py` adyacentes:
- `LAB_RUNNER.py` SHA-256 `fc14ff185419d694160121ad9684539bfd324ea171fda8fe8ef8261566510fa9`;
- `LII_TRAMO_I_QI_BREAKPOINT_AND_POLICY_DIAG_V03_RUNNER.py` SHA-256 `bfcac6ba62b29798ad333bcf9f44534f0d45b5f2948ace6a4f6e356b7b885105`;
- `LII_V04_EXHAUSTIVE_BALANCE_GATE_RUNNER.py` SHA-256 `bafc8a14904d2c61276e2feafe7e3e08476db22fdc80f3b2b227aa487384eee0`;
- `LII_V05_VARIANCE_STRESS_CROSSCHECK_RUNNER.py` SHA-256 `bc2446c315210c5eaba5106b5a9000fd28a54bf36626a3757873c602c49dee56`.

**Notebook local:** SHA-256 `78aff2ba6671c7984a9c11d4b112ef7a7e5da4c4f52eabce7bec7e9c73c6a3ba`; `13` celdas, notebook JSON válido; QA sintáctico y checkpoint sintético PASS; **integración Colab PENDING**.

## Artefactos BINARIOS de la conversación (respaldo local descargable, NO bytes almacenados en Git)

1. `COLAB_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.zip` — SHA-256 `a17608b7b38f54be761c3386b6c07a0d50dc66aa1784d5aa5c682b2417aa0f3e`, 7 integrantes, ZIP CRC PASS. Contiene notebook y 4 runners.
2. `LII_V04_EXHAUSTIVE_BALANCE_GATE_REVIEW.zip` — SHA-256 `3e43c3038933a3a7d68e36d95aa79879b6990297329bbc52b50462d44b3dfddc`; **479.232 combates auditados**. Binario de resultados histórico, no hace falta reejecutarlo para continuar.
3. `LII_V04_EXHAUSTIVE_BALANCE_GATE_AUDITORIA_2026-10-08.md` — SHA-256 `22e0a1586b660ede66f7fe3ee08d2b947e03ae7b3cc7eb9b35931c4dc75d591e`; copia local de la auditoría V04.
4. `QA_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.json` — SHA-256 `aa44088cff88bc35a3511c7f8b8364f7bb8f5f5bf64511537eed348c2b21197e`.

**La copia Git del notebook y QA está verificada contra sus hashes de blob locales.** No confundir un enlace temporal `sandbox:` con almacenamiento Git; Git queda navegable vía los paths anteriores.

## Fuente de ejecución bloqueada por SHA

`SOURCE_COMMIT = 9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`.

No sustituir automáticamente por este nuevo HEAD: la documentación/backup de hoy cambia HEAD pero no las reglas ni el código en que se ejecuta el laboratorio. Fijar el commit original, validar los blobs T0/T1/T2, mutantes LI y los extremos históricos LII.

## Límites conservados

- **V05A: 212.992 combates de estrés histórico + 100.000 generaciones LI**; aún no ejecutados.
- **V05B:** mutantes LII reales, sufijos en combate, builds multielementales e injertos/Concordancias; todavía NO disponibles en un contrato ejecutable y ratificado que podamos dar por válido. Diseñar después de revisar V05A.
- Sapo y Escarabajo LII: variabilidad ordinaria congelada al T0 hasta T2; extremos históricos NO canónicos.
- Cuatro guardianes únicos AOE: fuente T0 ratificada `45c3a9c240ea74208a0d8fd4d5be187bc817df35`; quinta identidad de Tierra `custodio_eco_petreo`, **El Custodio del Eco Pétreo**. Ver decisión Git; sin mezclar con LII V05A.
- Ninguna modificación en `main`, no merge, no HTML/runtime, ni importación Astra.

## Procedimiento de recuperación (nuevo chat)

1. Abrir este manifiesto y el HANDOFF; comprobar rama y notebook Git.
2. Si la persona todavía NO ejecutó V05A: descargar notebook de Git y correrlo en Colab, con dos workers y checkpoints.
3. Si ya ejecutó V05A: pedir/subir `LII_V05A_MUTANT_AUTHORITY_AND_HISTORIC_ENVELOPE_CROSSCHECK_REVIEW.zip`; validar antes de cualquier nueva prueba.
4. Discutir resultados y decisión humana de variabilidad para LII; sólo después preparar V05B. Jamás reconstruir inventando los efectos de mutantes LII.

**Fin del manifiesto de backup.**
