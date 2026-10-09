# La Grulla Blanca — PRE-A08 V24 / balance puro (sin economía)
**Fecha:** 2026-10-09. **Estado:** LAB PASS / NO CANON / NO RUNTIME / NO FREEZE A08.

## Límite de trabajo actual
Por decisión del usuario, **precios, economía, mercaderes, recompensa y comercio quedan fuera del frente** hasta nuevo aviso. Esta V24 usa únicamente estadísticas, técnicas, defensas y monstruos. La autoridad comercial ratificada existente no se rediseña ni se modifica.

## Evidencia numérica V24
Partiendo de V17 (habilidades como overlay LAB), seis especies normales V19 **ORIGINALES**, 16 builds por raíz, T1/T2, políticas EARLY/DELAYED_TRIGGER, se probaron dos Concordancias BASE estructurales V17 antes excluidas:
- `TIERRA_TO_AGUA` — **Embalse**, `defensive_scale: 0.15`.
- `TIERRA_TO_METAL` — **Placa Fundacional**, `defensive_scale: 0.15625`.

Tres dotaciones: M03 base, Sobretúnica de patrulla DEF+2/HP+2 (actual), Sobretúnica DEF+1/HP+2 (candidata). Cada escenario compara Concordancia OFF/ON con semilla y contexto pareados. Dos cohortes independientes DISCOVERY seeds 99510–99513 y HOLDOUT 99610–99613: **18.432 + 18.432 = 36.864 nuevos duelos**, 0 timeouts, 0 due_missed. Reproducción fría separada **4.608/4.608 filas exactas** (no son duelos nuevos). Contrato estructural físico probado: Embalse almacena y libera absorción; Placa preserva el primer impacto y refuerza el segundo.

### Victoria del jugador T2 (1.536 duelos por celda)
| Raíz | Equipo | Concordancia OFF | Concordancia ON | Δ ON |
|---|---|---:|---:|---:|
| Agua | M03 | 65,36% | 65,36% | 0,00 pp |
| Agua | Sobretúnica DEF+1 | 68,42% | 68,42% | 0,00 pp |
| Agua | Sobretúnica DEF+2 | 86,91% | 86,91% | 0,00 pp |
| Metal | M03 | 66,73% | 71,42% | +4,69 pp |
| Metal | Sobretúnica DEF+1 | 70,38% | 75,00% | +4,62 pp |
| Metal | Sobretúnica DEF+2 | 92,90% | 93,49% | +0,59 pp |

**Lectura:** la armadura DEF+2 eclipsa buena parte del valor de Placa Fundacional. El candidato DEF+1 mantiene la identidad protectora sin anular la utilidad de esta Concordancia. La ventaja de DEF+2 sobre DEF+1 en las comparaciones T2 es de 18,49 pp para Agua, 22,53 pp para Metal OFF y 18,49 pp para Metal ON.

**Observación Embalse:** registró 1.819,927 unidades acumuladas de absorción liberada a través de todas las batallas ON, pero en los **9.216 contextos pareados Agua OFF/ON** no hubo cambios en victoria, solo 27 cambios en HP final fraccional y 40 en absorción registrada. **Efecto físicamente activo pero con poca relevancia práctica demostrada**; corresponde auditar su umbral/consumidor, sin aumentar arbitrariamente su escala.

## Dictamen de balance
**Candidato preferido, PENDIENTE aprobación humana:** `sobretunica_patrulla.stats.defense 2 → 1`, `stats.hp_max +2` **sin cambio**. No modificar otras estadísticas, técnicas, monstruos ni sistemas como compensación. V19 Cangrejo (+3→+2) y Jabalí (40→35%) siguen candidatos no ratificados y NO se aplicaron en V24.

No se ensayaron los hooks condicionales V17 de Tramo I, persistencia de veneno/quemaduras, antídotos o bálsamos, ni T3/T4/minijefes. **No declarar freeze integral**. Se usó un adaptador estructural histórico de LAB instalado en memoria sobre ambos brazos, distinto del V23, por lo que los porcentajes absolutos entre V23 y V24 **no son directamente equiparables**; sirven las comparaciones apareadas internas.

## Reproducibilidad y QA
- Código original ejecutado: `run_v24_structural.py`; análisis: `analyze_v24.py`.
- Datasets: `RAW_V24_DISCOVERY.csv.gz`, `RAW_V24_HOLDOUT.csv.gz`, `RAW_V24_COLD.csv.gz`.
- Tablas: `SUMMARY_V24_COMBINED.csv`, `PAIRED_STRUCTURAL_V24.csv`, `COAT_STRUCTURAL_V24.csv`, `DEF1_VS_DEF2_STRUCTURAL_V24.csv`.
- ZIP portable: `GRULLA_PRE_A08_V24_BALANCE_PURO_ESTRUCTURALES_2026-10-09.zip`, SHA256 `713387505118fa269ce94e39fce204fd03485ab96dc28ca2f9e3ec7f8f82ec0d`; **68 archivos, CRC/manifiesto PASS y reproducción en carpeta limpia PASS**. El ZIP es adjunto de la conversación; **no subido a Git**.
- QA agregada: `QA_V24_BALANCE_PURO.json` en la misma carpeta de Git.

Sin `main`, merge, HTML, `ROOMS.exits`, A07 o cambios de motor comercial. Nuestro frente termina el balance y presenta cifras para aprobación; B01 lo integra posteriormente Astra.
