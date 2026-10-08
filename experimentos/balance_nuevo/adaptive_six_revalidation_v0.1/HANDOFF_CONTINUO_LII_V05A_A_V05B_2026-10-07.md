# HANDOFF CONTINUO — La Grulla Blanca — LianQi II V05A → V05B

**Pausa solicitada por el autor:** 2026-10-07, antes de ejecutar V05A en Colab.  
**Repositorio:** https://github.com/Shein25/La-Grulla-Blanca  
**Rama autorizada:** `experiment/monster-adaptive-six-revalidation-v0.1`  
**ESTADO:** HANDOFF LISTO · V05A PREPARADO · COLAB AÚN NO EJECUTADO · V05B SIN IMPLEMENTAR.  
**Ámbito exclusivo:** laboratorio de balance; Astra integra al final, nunca desde este frente.

## 0. LECTURA INICIAL OBLIGATORIA EN UN CHAT NUEVO

Leer, en este orden, en la rama autorizada:

1. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/HANDOFF_CONTINUO_LII_V05A_A_V05B_2026-10-07.md` (este archivo).
2. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/BACKUP_MANIFEST_LII_V05A_PAUSE_2026-10-07.md`.
3. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/notebooks/QA_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.json`.
4. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/notebooks/COLAB_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.ipynb`.
5. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/LII_V04_EXHAUSTIVE_BALANCE_GATE_AUDIT_2026-10-08.md`.
6. `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md`.

El notebook incluye **los cuatro runners** íntegros dentro de sus celdas; no se requiere recodificarlos para empezar. Si el usuario trae el ZIP de resultados de V05A, **auditarlo primero** y NO reejecutar la matriz ciegamente.

## 1. Punto exacto de interrupción — V05A

**Cuaderno ya creado y respaldado en Git:**
`notebooks/COLAB_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.ipynb`

SHA-256 exacto del archivo notebook: `78aff2ba6671c7984a9c11d4b112ef7a7e5da4c4f52eabce7bec7e9c73c6a3ba`.  
Git blob SHA exacto: `85fc561112bffc7c3c5bd5dec0282e35a2b268aa`.  
Paquete ZIP local entregable:
`COLAB_LII_V05A_MUTANT_AUTHORITY_AND_HISTORICAL_SENSITIVITY.zip`, SHA-256 `a17608b7b38f54be761c3386b6c07a0d50dc66aa1784d5aa5c682b2417aa0f3e`.  
El ZIP contiene notebook, cuatro runners, README y QA; **este ZIP binario se entrega como respaldo descargable de la conversación, no está almacenado dentro del repo Git**. El notebook sí está en Git íntegro.

**Entrada autoritativa de código:** Git commit `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`. **No apuntar al HEAD cambiante**, porque el notebook compara los ocho blobs del bridge T0/T1/T2 y cuatro fuentes adicionales de variabilidad y sufijos.

**Trabajo previsto (NO realizado aún):**
- **212.992 combates** de sensibilidad LII; 2 monstruos READY: `sapo_ceniza`, `escarabajo_hierro`.
- **100.000 generaciones LI** para verificar que la tasa/distribución mutante ratificada funciona; **no** son generaciones mutantes LII.
- T1/T2 ratificados, cuatro equipamientos de referencia, ocho builds por raíz; candidatos experimentales de Agua y Fuego.
- Dos ejes claramente etiquetados: **T0 LII CANON** y **HISTORICAL_ENVELOPE_NONCANONICAL**.
- `WORKERS=2`,  checkpoints reanudables (Drive activado por defecto), barras persistentes y verificación de sus hashes.
- QA local `PASS_LOCAL_STRUCTURE_AND_CHECKPOINT_QA__COLAB_RUNTIME_PENDING`. No anunciar PASS de motor/resultado de V05A antes de ejecutar Colab.
- Salida que deberá subir el usuario: `LII_V05A_MUTANT_AUTHORITY_AND_HISTORIC_ENVELOPE_CROSSCHECK_REVIEW.zip`.

**Runners incluidos y hashes SHA-256:**
- `LAB_RUNNER.py`: `fc14ff185419d694160121ad9684539bfd324ea171fda8fe8ef8261566510fa9`.
- `LII_TRAMO_I_QI_BREAKPOINT_AND_POLICY_DIAG_V03_RUNNER.py`: `bfcac6ba62b29798ad333bcf9f44534f0d45b5f2948ace6a4f6e356b7b885105`.
- `LII_V04_EXHAUSTIVE_BALANCE_GATE_RUNNER.py`: `bafc8a14904d2c61276e2feafe7e3e08476db22fdc80f3b2b227aa487384eee0`.
- `LII_V05_VARIANCE_STRESS_CROSSCHECK_RUNNER.py`: `bc2446c315210c5eaba5106b5a9000fd28a54bf36626a3757873c602c49dee56`.

## 2. Balance ya realizado; NO repetir sin causa

- LianQi I: 5 técnicas ofensivas BASE, T0/T1/T2 de cinco especies ratificados; raíces/equipamiento LI ya afinados y congelados según documentos propios. LI Concordancias: 20 pares dirigidos, 16 activos, 4 BASE NONE; prueba NO_TRAP anterior pasó, pero no congelar automáticamente como integración productiva. No rediseñar las rutas sin la fuente ratificada.
- LII: 5 ofensivas + 5 defensivas, Tramo I, 2 puntos de técnica, **sin AOE**; 80 builds monorraíz legales; faltan builds de injerto y Concordancias LII.
- LII monsters: `sapo_ceniza` (NORMAL) y `escarabajo_hierro` (TANK), T0/T1/T2 ratificados. No se permite ajustar su T0/T1/T2 automáticamente por un resultado de jugador.
- `LII_STAGE_REAL_PREFLIGHT_V01`: 23.040 combates, sólo T0, PASS_PREFlIGHT_ONLY.
- `LII_T1_T2_ADAPTIVE_BRIDGE_CONTRACT_GATE_V01`: 30.720 combates, 10/10 eventos, PASS_BRIDGE_ONLY, ejecutado.
- `LII_DEFENSIVE_T1_T2_CAUSAL_SCREEN_V01`: 163.840 combates, ejecución íntegra; 542 alertas heurísticas, no bugs.
- `LII_DEFENSIVE_T1_T2_FOCAL_R256_V02`: 78.848 combates, focal, NO FREEZE.
- `LII_TRAMO_I_QI_BREAKPOINT_AND_POLICY_DIAG_V03`: 75.264 combates, hotfix JSON `PosixPath` aplicado, NO FREEZE.
- **V04** `LII_V04_EXHAUSTIVE_BALANCE_GATE_REVIEW.zip` completado con hotfix `DataFrame.isna(subset=...)`, SHA-256 del ZIP `3e43c3038933a3a7d68e36d95aa79879b6990297329bbc52b50462d44b3dfddc`; 462.848 principales + 16.384 R512 = **479.232**. Manifiesto 20/20, tests eventos 10/10, sin timeout, AOE ilegal ni supresión de cadencia. Autoridad: `LII_V04_EXHAUSTIVE_BALANCE_GATE_AUDIT_2026-10-08.md`.
- No confundir validación de ejecución V04 con congelamiento de balance: **V04_CORE_PASS_BALANCE_REVIEW_PENDING**.

## 3. Candidatos V04 que V05A debe estresar

**Agua:** `latigazo_marea` y `espejo_luna`, especialización **EFFICIENCY T1** actualmente compilada a 5 Qi igual que sin invertir el punto debido a redondeo; experimento `eff.t1_flat_cost=-2` hace coste 4 Qi. No alterar redondeo global ni catálogo canónico. En V04 Latigazo mejoró ~+4,98 pp win y ahorro de 4,21 Qi por combate (OFFENSE_ONLY); Espejo ahorró Qi sin aumentar materialmente la victoria. Candidatos, no decisiones implementadas.

**Fuego:** `palma_ardiente` T1 rama `OFF_T1_0` **DOT**, `OFF_T1_1` DIRECT, `OFF_T1_2` EFFICIENCY. NO repetir la etiqueta errónea de V02 que adjudicó los +38–53 pp a DIRECT: pertenecían a DOT. En V04 el DOT actual **2 daño × 3 ticks** resultó muy fuerte (~98% victoria en algunos perfiles); candidatos **2×2** y **1×3** aún fuertes pero menos. Valores sólo en memoria y en escenarios definidos; no nerfear Fuego antes de evidencia cruzada. Redondeo de daño: 12% y 10% pueden producir la MISMA cifra entera por tick; no simular duplicados.

**Defensivas:** Cuerpo-Horno/Piel de Cobre no necesitan buff general por apertura mala. Algunas políticas gastan turnos/Qi y empeoran resultados pese a absorber daño; distinguir decisiones tácticas de poder intrínseco. V05A no es un rediseño de IA del jugador.

## 4. Mutantes/variabilidad: autoridad vs simulación hipotética

**FUENTES ratificadas en Git (en la ruta exacta):**
- `experimentos/balance_nuevo/individual_variance_v0.1/monster_individual_variance_v0.1.json` — schema `monster-individual-variance-v0.4` y distribución LI.
- `experimentos/balance_nuevo/individual_variance_v0.1/suffix_lab_v0.1/MUTANT_SUFFIX_CONTRACT_V1.json` — `HUMAN_RATIFIED_FROZEN_FOR_T2_LAB`.
- `experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/SIX_REPEATABLE_T0_VARIANCE_AUTHORITY_V01.json` — LII.
- Archivos freezes LII T0/T1/T2 en `t0_lii/`, `t1_lii/`, `t2_lii/`, NO depender del snapshot `monster_arc1_registry.json` desfasado.

**Regla obligatoria para Sapo y Escarabajo LII:** la variación ordinaria fue deliberadamente **colapsada al valor T0 a través del freeze T2**. Sus `historical_upper_evidence` son evidencia histórica, NO techo canónico habilitado en spawns LII, NO un mutante LII ratificado. V05A es explícitamente un **stress/sensitivity lab no canónico**. No asignarles efectos de sufijo automáticamente.

**LI mutantes/sufijos congelados:** q independientes por eje variable, spawn único, incidencia objetivo 0,75% y guardia <1%, clasificación especializada/excepcional/ascendido por ejes q>=.95. Cinco grupos: ACORAZADO A15 (reserva absorción 15% HPmax al cruzar HP<=50%), FUGAZ F25 (+25 EVA próximo golpe ofensivo después de crítico recibido), ACECHANTE C20 (+20 precisión próximo ataque tras fallar), INDOMITO I25 (+25 tenacidad al primer control), VORAZ V2 (siguiente básico ×1.5 tras HP jugador<=40%). La mutación no concede tier adaptativo; sufijo sin RNG adicional. Loot/XP combate x1.5. **Estos son contratos LI ratificados**; para V05B no activar en las dos especies LII sin nueva decisión humana.

**V05B realmente pendiente:** pedir/ratificar autoridad de variabilidad y mutantes específica para LII; luego efectos y combinaciones con T1/T2, builds injertadas legítimas y Concordancias multielementales. Si falta un contrato, fail closed; no inventar builds, manuales, efectos ni estados.

## 5. Guardianes únicos AOE — decisión ya ratificada y no olvidar

Documento fuente local en repo: `DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md`.
T0 ratificado de cuatro únicos: Git commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35` con `UNIQUE_T0_CLOSED_NO_T1_T4`. **No leer sólo el viejo registry de esta rama para concluir que son PENDING**.

| Elemento | ID | HP T0 ratificado | Sala histórica | Decisión |
|---|---|---:|---|---|
| Fuego | `sapo_caldera` | 83 | `camara_caldera` | Conservar |
| Metal | `rey_escarabajo` | 87 | `nido_escarabajos` | Conservar |
| Agua | `guardian_coral` | 80 | `aguas_rama_oscura` | Conservar |
| Viento | `mantis_nube` | 72 | `alturas_senda_mantis` | Reubicar a `bosque_corredor_viento` sólo cuando Astra implemente |
| Tierra | **`custodio_eco_petreo`** | **PENDIENTE** | No tiene spawn | **El Custodio del Eco Pétreo**, ubicación preferida `bosque_rocas_blancas` |

Únicos T0: una derrota, sin respawn, sin fases, sin T1–T4 persistente; mecánicas propias y contrajuego aún requieren pruebas. No confundir perfiles históricos de guardianes II/III/IV con umbral de percepción desde LIII. AOE se obtiene legalmente **LIII post-guardian y manual aprendido**. Balance principal de guardianes: `LIII_PRE_AOE + MAIN_ROOT_ULTI_READY` (una Ulti por combate) y control sin Ulti. El diseño del jefe de Tierra ya tiene nombre aprobado; sin T0, spawn ni manual runtime ratificados.

## 6. Instrucciones operativas para retomar

1. Verificar rama exacta, archivos documentales y notebook almacenado en Git.
2. Descargar notebook V05A desde el repo; abrir **.ipynb** en Colab, ejecutar de arriba a abajo sin cambiar source-pin. Mantener `WORKERS=2` y Drive checkpoints opcionales; no ejecutar inadvertidamente `.md` como notebook.
3. QA local es evidencia estructural, **NO implica que Colab haya terminado**.
4. En cuanto el autor comparta `LII_V05A_MUTANT_AUTHORITY_AND_HISTORIC_ENVELOPE_CROSSCHECK_REVIEW.zip`, inspeccionar: hashes/fuentes/manifiesto, grids y seeds, 100k LI samples, 212.992 combats, contrastes T0 vs extremos históricos, candidatos Agua/Fuego, paridad adaptativa y guardas. Si ocurre excepción, arreglar con hotfix reanudable, NO recomputar automáticamente 212k.
5. Elaborar informe V05A; distinguir cambios sugeridos de mutantes LII NO ratificados. Elegir si merece extender autoridad LII. Después diseñar V05B de forma legal. Integración Astra sólo cuando TODO el laboratorio esté cerrado.
6. En reportes por etapa usar dictámenes separados MONSTERS / TECHNIQUES / CONCORDANCES / EQUIPMENT / ROOTS / SYSTEM. No declarar freeze global con sólo un PASS de simulación.
7. No tocar `main`, no merge, no editar HTML/ROOMS.exits/gates, no rediseñar A07 ni G03, no inventar NPCs, jefes ni drops; autoridad humana prevalece.

## 7. Respuesta sugerida en el siguiente chat

«Retomamos La Grulla Blanca desde el handoff V05A→V05B guardado en Git. Rama `experiment/monster-adaptive-six-revalidation-v0.1`. V05A preparado en Git y pendiente de ejecutar en Colab. Antes de hacer trabajo nuevo, revisá el handoff, manifiesto, QA y notebook; si tengo el ZIP de resultados V05A, auditálo sin reabrir V01–V04. Respetá las autoridades congeladas y los cinco guardianes AOE, incluido El Custodio del Eco Pétreo».

FIN DEL HANDOFF.
