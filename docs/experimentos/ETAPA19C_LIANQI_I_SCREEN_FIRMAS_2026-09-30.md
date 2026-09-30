# ETAPA19C — LianQi I · exhaustividad lógica y screen de firmas

**Fecha:** 2026-09-30  
**Rama:** \`experiment/combat-stat-contract-v0.1\`  
**Estado:** LAB / FRAMEWORK LISTO PARA COLAB. No runtime. No HTML. No merge.

## 1. Punto de partida

ETAPA19B ya existe en la rama y proporciona:
- catálogo machine-readable de las 15 técnicas;
- compilador de ramas;
- motor 1v1;
- T0/T1 con CADENCE_COMPAT;
- raíces, progresión, equipo y monstruos traducidos;
- métricas reproducibles;
- self-check estructural.

Por tanto ETAPA19C no reimplementa combate: consume \`etapa19b_combat_engine.py\`.

## 2. Espacio exacto LianQi I

Equipo LI disponible: **14 piezas**.

Combinaciones estructurales permitiendo slots vacíos:
- **6.144 loadouts**.

Al agrupar por firma mecánica de combate:
- **4.864 firmas únicas de equipo**;
- reducción estructural: **20,8333%**;
- multiplicidad máxima observada: 3.

La diferencia aparece por loadouts que producen exactamente la misma suma de estadísticas de combate. El efecto \`MEDITATION_BONUS\` del Anillo de hierro oxidado está marcado \`OUT_OF_COMBAT_PENDING\` y, correctamente, no separa firmas de combate 1v1.

Con cinco raíces:
- raw jugador: 30.720;
- firmas mecánicas jugador: **24.320**.

## 3. Cruce del screen LI

Por firma mecánica se cruzan:
- 5 raíces;
- 5 monstruos nativos LI;
- T0 / T1;
- 3 políticas iniciales:
  - UNITARGET_FIRST;
  - DEFENSE_OPEN;
  - AOE_FIRST.

Total screen completo:
- **729.600 celdas** antes de iteraciones Monte Carlo.

No se materializan las 30.720 builds raw por separado cuando dos loadouts son mecánicamente equivalentes. Se conserva:
- multiplicidad;
- mapping loadout→firma;
- loadout representativo;
- lista completa de miembros de la firma.

## 4. Nuevo artefacto

\`experimentos/balance_nuevo/etapa19c_li_screen.py\`

Funciones principales:
- \`enumerate_loadouts()\`;
- \`build_li_signature_catalog()\`;
- \`coverage_signature_ids()\`;
- \`run_signature_screen()\`;
- \`select_refinement_cells()\`;
- \`write_catalog_outputs()\`.

El script aserta:
- 6.144 loadouts LI;
- 4.864 firmas únicas.

Si cualquiera de esos conteos cambia, el pipeline se detiene para evitar ejecutar una matriz sobre un catálogo alterado sin darse cuenta.

## 5. Cobertura mínima antes del full screen

Se seleccionan firmas de cobertura sin elegir builds "a ojo".

Criterios:
1. al menos una firma que contenga cada objeto LI;
2. MANDATORY_ENTRY;
3. EXPECTED_STAGE;
4. HIGH_ROLL_STRESS;
5. mínimo y máximo de cada stat relevante de combate.

Con el catálogo actual esto produce **25 firmas de cobertura**.

Estas 25 firmas se cruzan primero contra:
- las 5 raíces;
- los 5 monstruos LI;
- T0/T1;
- 3 políticas.

Objetivo:
- verificar que el pipeline completo funciona;
- detectar errores de integración antes de gastar cómputo;
- NO sacar conclusiones de balance definitivo.

## 6. Notebook Colab actualizado

\`COLAB_ETAPA19_MATRIZ_MASIVA_ARCO1.ipynb\` ahora incorpora:

### Bloque 7
Self-check ETAPA19B.

### Bloque 8
Construcción exacta:
- 6.144 raw;
- 4.864 firmas.

### Bloque 9
Screen de las 25 firmas de cobertura.

### Bloque 10
Screen completo controlado por:

\`RUN_FULL_LI_SCREEN = False\`

Se deja en \`False\` para impedir lanzar accidentalmente las 729.600 celdas.

Cuando el self-check y la cobertura pasan:
\`RUN_FULL_LI_SCREEN = True\`

## 7. Checkpoints

El screen escribe Parquet por lotes.

Esto permite:
- no perder todo el trabajo ante desconexión de Colab;
- conservar seeds por celda;
- reanudar/analisar por bloques;
- auditar procedencia.

La semilla de cada celda depende de:
- signature_id;
- raíz;
- monstruo;
- tier;
- política;
- seed base.

Por tanto no cambia si se modifica el tamaño del chunk o el orden físico de escritura.

## 8. Refinamiento

Después del low-N se seleccionan automáticamente:
- frontera de win rate;
- mejores/peores extremos por matchup;
- mayor sensibilidad T0→T1;
- firmas necesarias para cobertura de objetos/perfiles.

Sólo esas celdas pasan al high-N.

Esto mantiene la metodología acordada:

**exhaustividad lógica → screen barato → Monte Carlo fuerte donde aporta información.**

## 9. Guardias

- no tocar runtime/HTML;
- no cambiar equipo;
- no cambiar monstruos;
- no promover bridges LAB a CANON;
- no declarar un objeto/técnica roto por una sola política;
- no interpretar HIGH_ROLL como baseline;
- no usar todavía adquisición económica como filtro;
- no empezar LII hasta cerrar el análisis LI.

## 10. Próximo paso

Ejecutar en Colab, en este orden:

1. ETAPA19B self-check;
2. construir firmas LI;
3. screen de 25 firmas de cobertura;
4. revisar errores/anomalías del pipeline;
5. activar full screen LI low-N;
6. seleccionar refinement;
7. high-N de frontera/anomalías;
8. producir:
   - build_catalog;
   - matchups;
   - aggregate_stage;
   - item_impact;
   - root_impact;
   - outliers;
9. recién entonces discutir números de balance.

No modificar stats antes de obtener esos datos.
