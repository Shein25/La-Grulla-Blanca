# LII defensivas × T1/T2 — Focal R256 V02 — Auditoría

Estado: **PASS_RUN_INTEGRITY_REVIEW_REQUIRED / NO_AUTO_FREEZE**.
Revisión del artefacto `LII_DEFENSIVE_T1_T2_FOCAL_R256_V02_REVIEW.zip` con SHA-256
`91b5cc9d995897d96f3f3c1acba84041aa10cd87b6482d4f207ea5b1ffea0c4b`.
Source-lock `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`.

## Integridad
- ZIP CRC OK; 14/14 artefactos del manifiesto con SHA-256 y tamaño exactos.
- 78.848 filas únicas = 11 estratos × 7 builds × 4 políticas × R256.
- 10/10 tests de evento PASS; 0 AOE, 0 canonical_due_missed, 0 timeouts.
- 231 contrastes pareados de política, 264 de Tramo I.
- 21 alertas de política con pérdidas materiales, relacionadas y no independientes.

## Confirmaciones
1. **Agua, Espejo de Luna, EFICIENCIA Tramo I queda mecánicamente inerte en LII:** coste crudo 5,25→4,50, redondeo final 5→5 Qi; la defensa compilada es idéntica. En 2.048 pares por semilla/política, 24 campos por combate muestran cero diferencias. No tocar motor global sin aprobación humana.
2. **Políticas defensivas tienen costes de oportunidad reales:** Tierra MANDATORY_ENTRY vs Sapo T2 BASE, DEFENSE_DUE −10,16 pp win [CI95 −17,41; −2,90]; Fuego MANDATORY_ENTRY vs Sapo T1 BASE, DEFENSE_GUARD −8,59 pp [−16,42; −0,77]. No prueba que defensa misma esté rota.
3. **Fuego OFF_T1_0 DIRECT:** +38,28 a +53,13 pp vs BASE en las cohortes focales. Verificar cohortes representativas antes de considerar rebalance ofensivo.
4. **Fuego DEF_T1_1 CONVERSION:** +8,20 a +23,44 pp en varios escenarios Sapo: no es defensa universalmente ineficaz.
5. **Fuego y Viento EFICIENCIA:** ahorran 1 Qi por activación aunque no alteren victorias en estos escenarios; no confundir con el caso Agua.
6. **Viento, Metal, Agua:** defensivas oportunamente usadas generan ventajas claras en estratos específicos (+12–18 pp BASE frente al Escarabajo T2).

## Reglas de interpretación
Los 11 estratos se seleccionaron por alertas anteriores, no representan distribución real de encuentros. Las políticas modifican acciones, turnos, Qi y la subsecuencia RNG; estos deltas miden estrategia completa, no un bono mecánico aislado. IC95 exploratorio sin corrección por múltiples tests. T0/T1/T2 LII siguen congelados.

## Próximo gate recomendado
**LII_TRAMO_I_QI_BREAKPOINT_AND_POLICY_DIAG_V03**
- probar dos propuestas acotadas de ahorro efectivo de Qi en Agua, revisar consecuencias en Tramos II/III sin escribir números canónicos;
- política tácticamente consciente ante amenaza y ventanas de defensa para Tierra/Fuego;
- estratos de referencia no seleccionados para confirmar poder OFFENSIVE DIRECT de Fuego;
- microescalación sólo de anomalías persistentes.
Luego: mutantes autorizados (contrato oficial antes de generar), builds multielementales, Concordancias LII. No cerrar balance ni enviar a Astra hasta finalizar laboratorio.

Guardias: no main, no merge, no push, no HTML/runtime, no cambios de monster freezes ni equipo LI.
