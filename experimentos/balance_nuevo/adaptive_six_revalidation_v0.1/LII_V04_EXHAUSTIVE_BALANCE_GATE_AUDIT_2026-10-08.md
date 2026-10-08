# LianQi II — V04 Exhaustive Core Gate — AUDITORÍA

Fecha: 2026-10-08.
Estado: **PASS_RUN_INTEGRITY / REVIEW_REQUIRED_NO_AUTO_FREEZE**.
Fuente exacta: commit `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`.
ZIP review: `LII_V04_EXHAUSTIVE_BALANCE_GATE_REVIEW.zip` SHA256 `3e43c3038933a3a7d68e36d95aa79879b6990297329bbc52b50462d44b3dfddc`.

## Integridad
- 20/20 manifest SHA/size coinciden, ZIP CRC OK.
- 462.848 base fights: GENERAL 327.680; FIRE_DOT 49.152; WATER_QI 24.576; TIMING 61.440.
- 16 pares de confirmación R512 = 16.384 adicionales. **479.232 combates** en total.
- 3.424 contextos, 6.016 contrastes de pantalla, 10/10 paridad de eventos.
- 0 filas duplicadas, nulos de métricas obligatorias, timeouts, AOE y técnicas canónicas perdidas.
- Variantes solo en memoria, ningún freeze/ajuste de catálogo.

## Fuego
Identidad real: `OFF_T1_0=DOT`, `OFF_T1_1=DIRECT`, `OFF_T1_2=EFFICIENCY`.
- Palma Ardiente DOT actual: daño 2×3, victoria **98,535%** OFFENSE_ONLY y **97,778%** DEFENSE_GUARD.
- Candidato 2×2: **96,533% / 94,873%**.
- Candidato 1×3: **93,115% / 91,650%**.
- DIRECT: **87,378% / 84,131%**.
- EFFICIENCY: **75,586% / 77,393%**.
- Comparación pareada DOT CANON vs DIRECT: **+11,157/+13,647 pp**. DOT 1×3 vs DIRECT: **+5,737/+7,520 pp**. Incluso 1×3 conserva ventajas en los contextos ensayados.
- R512: mejoras de DOT CANON frente BASE en cuatro cohortes seleccionadas de +50,586 a +57,617 pp. Rebajar DOT CANON→1×3 en Sapo T2 MANDATORY_ENTRY DEFENSE_GUARD: **−15,039 pp** IC95 [−18,138; −11,940].
- **No canonical nerf aún**: validar mutantes, multirroot, otros enemigos/encuentros mixtos. Dos candidatos 12%/10% que compilen mismo 1 tick no requieren simulación duplicada.

## Agua
Ambos `latigazo_marea` y `espejo_luna` tienen costo BASE=5, EFF CANON=5 debido al redondeo.
Candidato lab-only `eff.t1_flat_cost=-2` compila a **4 Qi**.
- Latigazo: vs eficiencia canon, OFFENSE_ONLY **+4,980 pp win, −4,212 Qi** gasto; DEFENSE_GUARD **+4,639 pp, −1,763 Qi**.
- Espejo: DEFENSE_OPEN **+0,488 pp, −0,204 Qi**; DEFENSE_GUARD **+0,195 pp, −0,869 Qi**.
- Diferencias netas de Qi dependen de longitud de pelea. R512 en cuatro estratos ofensivos confirma ahorro, victoria de −0,195 a +1,758 pp. **Ratificación pendiente** tras cobertura avanzada; no tocar redondeo global.

## Timing
BASE_0 con fuego: win OFFENSE_ONLY 71,484%, OPEN 68,506%, DUE 72,656%, GUARD 72,754%, THREAT_AWARE 70,947%.
BASE_0 con tierra: 69,238%, 73,193%, 72,461%, 72,412%, 72,900%.
- Fuego BASE vs Sapo T2 MANDATORY_ENTRY R512 THREAT_AWARE −15,234 pp [−21,047; −9,422], +7,211 Qi gastado, +2,406 rondas, +16 daño absorbido. **Coste táctico real, no evidencia de escudo inherentemente débil**.
- No buff automático a defensivas Fuego/Tierra.

## Cobertura y autoridad
Este V04 es exhaustivo para la matriz **80 builds monorraíz, cuatro gears, dos especies LII T1/T2**. No cubre mutantes (0), variabilidad individual (0), multielemento (0), Concordancias LII (0), jefes únicos (0), Tramos II/III (0).
Contrato mutante localizado en `experimentos/balance_nuevo/individual_variance_v0.1/suffix_lab_v0.1/MUTANT_SUFFIX_CONTRACT_V1.json`; requiere gate ejecutable independiente, no simular mutaciones inventadas.
Guardianes AOE únicos: fuente T0 humana histórica correcta commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35`, `UNIQUE_T0_CLOSED_NO_T1_T4` para Sapo Caldera/Rey Escarabajo/Coral/Mantis. Evitar versión antigua pendiente del registry de esta rama. Nombre Tierra `El Custodio del Eco Pétreo`, diseño `custodio_eco_petreo`, documento `DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md`.

## Dictamen
**V04_CORE_PASS_BALANCE_REVIEW_PENDING**.
Candidatos próximos: Agua EFICIENCIA -2 ambas técnicas; Fuego DOT 1×3 como comparador conservador, no como nerf aprobado.
Siguiente bloque: contrato real de mutantes/variabilidad, builds multielementales y Concordancias, más especies disponibles; evaluar efectos cruzados y cerrar decisión humana. No reabrir T0/T1/T2 congelados de las dos especies READY sin evidencia de bug. No `main`, merge, push ni HTML. Astra integra solo después del cierre de laboratorio.
