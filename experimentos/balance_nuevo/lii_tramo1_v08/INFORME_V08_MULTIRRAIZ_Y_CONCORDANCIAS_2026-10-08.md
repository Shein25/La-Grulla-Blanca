# V08 — Tramo I LianQi II: técnicas ajenas, Concordancias y control de balance
Fecha: 2026-10-08
Estado: **LABORATORIO / NO CANON / SIN CAMBIOS DE MOTOR**
Rama exclusiva: `experiment/lii-tramo1-multirraiz-v08-2026-10-08`.

## Alcance y autoridad
- LianQi I: 0 puntos; solo unitarget BASE, sin defensivas ni AOE. **Intacto**.
- LianQi II: 2 puntos, primer Tramo desbloqueado; unitarget + defensivas, sin AOE.
- Seis especies normales candidatas: Jabalí, Búho, Zorro, Cangrejo, Murciélago y Araña; T1/T2. No incluir élite ni T3/T4.
- Raíces elementales neutrales al daño (**×1,00**), conservando identidad y Concordancias.
- Equipos fijos: `POST_M03` y `EXPECTED_STAGE`. No cambiar monstruos ni economía.
- Candidato V07 (solo nodos T1 seleccionados): Fuego/Ascua Adherente `flat_per_tick 2→1`, Metal/Ejecución `crit_pp +10`, Viento/Punta de Tormenta `direct_pct 20→30`. **NO RATIFICADO**.
- Builds preelegidas de dos puntos: Fuego `OFF_0_DEF_1`, Metal `OFF_1_DEF_0`, Agua `OFF_1_DEF_0`, Tierra `OFF_1_DEF_2`, Viento `OFF_1_DEF_0`. No optimizadas por monstruo durante V08.

## Batería numérica realmente ejecutada
**61.440 combates** = 5 raíces principales × 4 raíces ajenas × 6 especies × 2 equipos × 2 políticas × 2 tiers × 16 semillas × 2 accesos (MONOROOT/FOREIGN_LEARNED) × 2 versiones (ORIGINAL/V07_CANDIDATE).
**15.360 contextos pareados**, repeticiones de 2000 a 2015, semillas compartidas en los cuatro brazos.

- `FOREIGN_LEARNED` expone **una sola técnica ofensiva BASE de otra raíz**, hipotéticamente aprendida; la usa cada tercera ronda si dispone de Qi. Nunca le asigna puntos ni concede AOE. Esto **NO** equivale a confirmar su adquisición narrativa o una política óptima.
- `MONOROOT` es el control: la etiqueta de la raíz ajena no altera el resultado.
- Dos políticas: `OFFENSE_ONLY` y `DEFENSE_REFRESH`.
- `CONCORDANCE_OFF` en toda la simulación: el puente V07 no tiene resolvedor numérico autorizado; NO inventar `+10%` universal ni inferir ON de los resultados.
- Sin modificaciones al HTML, al catálogo de técnicas, a los monstruos ni a LianQi I.

### T2, equipo POST_M03, porcentaje de victoria del jugador
| Raíz | V07 monorraíz | V07 con técnica ajena rotada | Variación de V07 vs ORIGINAL al rotar |
|---|---:|---:|---:|
| Fuego | 85,94 % | 79,95 % | -6,25 pp |
| Agua | 81,25 % | 68,10 % | 0,00 pp |
| Tierra | 82,81 % | 75,13 % | 0,00 pp |
| Metal | 74,48 % | 69,79 % | +4,95 pp |
| Viento | 74,48 % | 68,88 % | +5,47 pp |

Tamaño de muestra en esta tabla: 768 combates para cada raíz/acceso/versión; NO implica igual resultado con otra política de aprendizaje/rotación. La técnica ajena no es un bono gratuito. La alternancia automática puede reducir la eficacia y agotar Qi en momentos desfavorables.

### Controles comprobados
- **0 timeouts; 0 omisiones de técnicas canónicas programadas.**
- Mismas semillas en los cuatro brazos; 15.360 contextos completos sin duplicados.
- Candidato V07 no afecta resultados de Agua/Tierra (12.288 controles de igualdad exacta).
- MONOROOT no depende de la etiqueta de raíz extranjera.
- Controles de raíces, estadísticas, equipo y adaptación no alterados.

## Auditoría documental de Concordancias BASE (no combate ON)
Se transcribió explícitamente el mapeo aprobado `docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md` para las **10 técnicas permitidas en LianQi II**. Se controlaron 40 pares dirigidos fuente ajena → receptor BASE:
- 35 pares con primer hook compatible declarado.
- 5 pares `BASE NONE`, que deben tener **cero consumo** por Concordancia y **cero fallback universal de daño**.
- 20 relaciones dirigidas representadas.
- **Esto verifica una tabla documental**, no ejecuta el resolvedor canónico: ni efectos numéricos, ni duración, ni transformaciones estructurales, ni hooks condicionales del Tramo I están validados.

## Bloqueos y decisión
**NO CERRAR V07, T1/T2 de seis especies, ni emitir números finales.**
1. Conectar el resolvedor real `CONCORDANCE_ON/OFF`, incluyendo Eco, prioridades, hook de rama condicional, consumo, HALF_UP, interacciones PRE_COST y estados STRUCTURAL. Nunca inventar una escala de Concordancia.
2. Probar adquisición válida de otras técnicas y la oportunidad real de invocarlas, no asumir todas aprendidas.
3. Contrastar con HTML candidato evento por evento (es laboratorio experimental).
4. Repetir con políticas tácticas que alternen solo cuando corresponda, equipos y condiciones legales; no penalizar la opción extranjera porque una macro la use incorrectamente.
5. Realizar regresión independiente en LianQi I: 0 Tramos, 0 defensivas, 0 AOE; preservar monstruos congelados.
6. Mutantes raros y Concordancias ON en la etapa final, si se integra el motor.

## Material reproducible y hashes
El paquete V08 del laboratorio contiene `run_v08.py`, `concordance_contract_gate_v08.py`, `PAIRED_V08.csv.gz`, `QA_V08.json`, `SUMMARY_V08.csv`, `CANDIDATE_EFFECT_V08.csv`, `BY_PAIR_V08.csv`, `BASE_CONCORDANCE_AUDIT.csv` y checksums.
- `run_v08.py` SHA-256: `4cbaad414f85c4789da80eeaf3536bc92b2c06cd46aab27e8bad82fbb6b30759`.
- `PAIRED_V08.csv.gz` SHA-256: `144d6373a2d54a7fa15bc1974b3599a481e874355514277bb304845253d1c2af`.
- `concordance_contract_gate_v08.py` SHA-256: `17a7f81d26c49f6ecd72c4bdcc2aef908f2c413836a3657a4f6b94dee14d6709`.
- Requiere el paquete local V07 y su fuente congelada `BUILDSPACE_16/run_buildspace_v05.py`, no está autocontenido en Git solo con este documento.

**Guardias:** no main; no merge; no cambios de runtime; no T3/T4; no élite; no auto-freeze; no gastos de contribución ni cambios de materiales.
