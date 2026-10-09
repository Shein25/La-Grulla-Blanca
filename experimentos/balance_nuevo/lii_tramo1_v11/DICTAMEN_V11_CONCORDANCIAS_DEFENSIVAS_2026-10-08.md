# V11 — Concordancias defensivas BASE y auditoría de Tramo I (LianQi II)
Fecha: 2026-10-08. **LAB PASS PARCIAL / NO CANON / NO RUNTIME**.

## Alcance ejecutado
- **43.008 combates T1/T2**; 21.504 contextos pareados Concordancia ON/OFF, 16 semillas por contexto, cinco raíces, seis especies normales LII, equipos POST_M03 y EXPECTED_STAGE.
- Cuatro builds monorraíz por raíz: BASE_0 y DEF_T1_0/1/2. La ofensiva ajena BASE se supone aprendida para generar un Eco el turno inicial; la defensiva propia se intenta en turno 2. No hay certificación de adquisición narrativa ni coste de raíz ajena en el HTML.
- Solo la Concordancia del receptor **defensivo BASE** usa magnitudes por relación tomadas **prestadas de LI V04B como sensibilidad**, NO valores autorizados para LII. No se aplica numeración condicional de Tramo I en combate. Las transformaciones estructurales se excluyen.
- No élite, T3/T4, AOE, cambios de monstruos, ajuste V07 aplicado, HTML, main ni merge.

## QA
**PASS**: cero timeouts y cero técnicas de cadencia omitidas; 17.164 resoluciones ON, cero OFF. Los 1.536 pares Agua→Fuego `BASE NONE` fueron exactamente iguales en victoria, vida, Qi, rondas, absorción y uso de técnicas; no hubo fallback. Hubo 723 pares con victoria adicional ON y 66 con derrota adicional ON (20.715 invariables). Los cambios aleatorios de trayectoria no garantizan victoria monótona.

## Victoria del jugador (escenario prestado, NO LII canon)
| Equipo | Tier | OFF | ON | Diferencia |
|---|---|---:|---:|---:|
| POST_M03 | T1 | 63,37% | 68,51% | +5,13 pp |
| POST_M03 | T2 | 59,45% | 64,94% | +5,49 pp |
| EXPECTED_STAGE | T1 | 95,67% | 96,41% | +0,74 pp |
| EXPECTED_STAGE | T2 | 94,96% | 95,81% | +0,86 pp |

Contra T2 temprano: Agua +0,00 pp, Fuego +0,17 pp, Metal +8,46 pp, Tierra +5,73 pp y Viento +18,23 pp. **El resultado no avala estos escalados**: hay saltos extremos en Agua→Tierra (+22,66 pp), Fuego→Viento (+21,09 pp), Fuego→Metal (+15,89 pp); exigir microgate y autoridad LII antes de ratificar cifras.

## Cobertura y bloqueos
Se auditaron **80 celdas** (4 variantes defensivas × 20 relaciones dirigidas), con los siguientes resultados:
- **52** celdas con magnitud experimental LI V04B aplicable en el puente BASE.
- **16** celdas sin magnitud: `METAL_TO_FUEGO`, `AGUA_TO_METAL`, `AGUA_TO_VIENTO`, `TIERRA_TO_VIENTO` (cuatro relaciones × cuatro builds). En LI eran negativas para receptor unitarget BASE; en LII pueden tener receptor DEF. **No inventar magnitud.**
- **8** celdas estructurales: Tierra→Metal = **Placa Fundacional**, Tierra→Agua = **Embalse**. Se ejecutaron ocho verificaciones de selección del descriptor con cero efectos escalares indebidos; **NO se ejecutaron sus efectos físicos en combate**.
- **4** controles NONE: Agua→Fuego con Cuerpo-Horno.

## Auditoría de Tramo I
Compiladas las **80 builds monorraíz legales** de LianQi II (16 por raíz), se inspeccionaron **320 combinaciones build × raíz extranjera**: 80 exponen un hook condicional adicional desde 20 builds distintas. Disponibilidad condicional, **NO resolución del hook**:
- Fuego CONVERSION: `INTERNAL_RESOURCE`.
- Metal ADAPTATION: `TENACITY_GRANTED`.
- Agua EFFICIENCY: `QI_COST_PERCENT`.
- Viento RESPONSE: `REACTIVE_RESPONSE`; Viento EFFICIENCY: `QI_COST_PERCENT`.
- Tierra: ninguno nuevo entre los hooks del Tramo I defensivo.

**Breakpoints medidos del compilador LAB:** Espejo de Luna Agua base coste bruto 5,25 → 5 Qi; con EFFICIENCY coste bruto 4,50 → también 5 Qi (ahorro efectivo **0**). Paso de Nube Viento con EFFICIENCY sí reduce 7→6 Qi. Antes de rebalancear Agua, verificar paridad HTML, orden de descuentos y si el nodo posee beneficios condicionales de Concordancia.

## Integridad y reproducción
ZIP: `GRULLA_LII_V11_CONCORDANCIAS_DEFENSIVAS_TRAMO1_2026-10-08.zip`; SHA-256: `3e107ad8d0a0b035664dcbcef59eac218050dabfb4573c55eae1e3a2e173bce3`. 30 archivos con sus fuentes de laboratorio y datos crudos. Integridad CRC/SHA-256 PASS. **Reproducción fría 5.376/5.376 filas idénticas** al subconjunto de semillas 6000–6001; la reproducción no altera esta rama Git.

## Dictamen y próximo gate
**NO congelar V07 ni las seis especies.** Es necesaria autoridad numérica para las cuatro relaciones nuevas de LII, resolver Placa/Embalse operativamente y verificar precedencia de hooks de Tramo I y adquisición legal de la ofensiva ajena. Después repetir ON/OFF con defensas temporizadas y cotejar eventos contra HTML correcto; solo entonces reconsiderar el rebalance del catálogo de técnicas. Preservar LI 0 PT / sin defensivas / sin AOE; V11 no repite regresión LI (V10 ya la pasó).

Fuentes: contrato global `docs/experimentos/CONTRATO_CONCORDANCIAS_GLOBALES_V0_1.md`, mapeo `docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`, plan LII por etapa y runners V07/V10. No cambios a runtime ni a `main`.
