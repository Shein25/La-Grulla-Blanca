# LianQi II — V15: balance cruzado de Tramo I y Concordancias BASE

**Fecha:** 2026-10-09
**Estado:** PASS_LAB_EXPERIMENTAL / NO CANON / NO FREEZE / NO RUNTIME
**Rama:** `experiment/lii-tramo1-multirraiz-v08-2026-10-08`. No main, no merge, no HTML.

## Diseño
Se compararon **cuatro brazos pareados por semilla y monstruo**:
- ORIGINAL_OFF
- ORIGINAL_ON (solo Concordancias defensivas BASE con escalas por relación del paquete experimental LI V04B)
- V07_OFF
- V07_ON

Los cambios **V07 CANDIDATOS, no ratificados**, solo existen cuando se selecciona el nodo ofensivo de Tramo I:
- Fuego Ascua Adherente: 2→1 daño por pulso;
- Metal Ejecución: +10 puntos porcentuales críticos;
- Viento Punta de Tormenta: bono directo 20→30%;
- Agua y Tierra sin cambios.

Ámbito: LianQi II con 2 PT; seis especies normales; T1/T2, dos equipos POST_M03 y EXPECTED_STAGE; las 16 builds monorraíz por raíz, dos políticas de defensa EARLY y DELAYED_TRIGGER, elementos neutros ×1. **Solo 14 relaciones numéricas BASE**. Las cuatro relaciones sin valor y las dos estructurales están explícitamente excluidas de la campaña V15 de combate. El eco se genera usando ofensiva BASE ajena hipotéticamente aprendida; adquisición y recargo de Qi no verificados.

## Ejecuciones y controles
- Discovery: **86.016 peleas**, **21.504 contextos de cuatro brazos**, semillas 19000–19001, 14 relaciones y 16 builds por raíz.
- Holdout: **86.016 peleas adicionales**, **21.504 contextos de cuatro brazos**, semillas 20000–20015. Todas las cuatro builds ofensivas afectadas de Fuego, Metal y Viento.
- **Total 172.032 peleas; 43.008 contextos completos.**
- **0 timeouts, 0 técnicas programadas omitidas**; OFF registra cero resoluciones de Concordancia.
- **18.816 contextos discovery sin nodo modificado** con igualdad exacta ORIGINAL = V07, con/sin Concordancia, en todas las métricas auditadas. Agua/Tierra preservadas.
- **Reproducción fría:** 43.008 peleas discovery + 5.376 heldout = **48.384 resultados idénticos, todas las columnas** desde ZIP limpio. ZIP CRC/SHA-256: PASS.

## Heldout: T2 POST_M03; porcentaje de victorias del jugador, solo builds afectadas

| Raíz | N contextos | ORIGINAL_ON | V07_ON | Delta V07 al activar Concordancia | Delta V07 con Concordancia OFF | Interacción ON−OFF |
|---|---:|---:|---:|---:|---:|---:|
| Fuego | 2.304 | 91,80% | 81,47% | **−10,33 pp** | −10,42 pp | +0,09 pp |
| Metal | 1.536 | 77,34% | 80,86% | **+3,52 pp** | +5,14 pp | −1,63 pp |
| Viento | 1.536 | 78,13% | 81,97% | **+3,84 pp** | +6,90 pp | −3,06 pp |

Intervalo exploratorio t95 agrupando por las 16 semillas de holdout (no sustituye la paridad con HTML):
- Fuego, delta V07_ON: [−12,11; −8,55] pp.
- Metal: [+2,25; +4,78] pp.
- Viento: [+2,56; +5,12] pp.
- Interacción Metal: [−2,49; −0,77] pp; Viento [−5,05; −1,07] pp.

Por especie T2: Fuego V07_ON reduce victorias entre 7–14 pp según monstruo; Metal suma ~2–6 pp, Viento ~1–6 pp. Contra Cangrejo, Viento gana +5,47 pp con el ajuste, pero su interacción V07×Concordancia es de ~−7,42 pp, por solapamiento de protecciones y rendimiento. **No asumir que la ganancia de una técnica sin Concordancia es acumulativa.**

## Contratos y Qi
- **80 builds/320 contextos de hooks** revalidados contra el compilador: 240 BASE_ONLY; 16 prioridad condicional clara; 60 receptor condicional expuesto pero prioridad/efecto no demostrados; **4 Agua→Viento con Paso de Nube RESPONSE necesitan resolución de prioridad canónica**.
- **20 pares raíz principal × ofensiva BASE ajena:** en el puente de laboratorio, Fuego/Metal/Tierra/Viento pagan 6 Qi y Agua 5 Qi. **No es verificación de adquisición ni costes finales del HTML**, porque el compilador BASE no aplica contrato narrativo o penalidades extranjeras.
- Espejo de Luna Eficiencia: raw 5,25→4,5 pero **5→5 Qi efectivos** tras ROUND_HALF_UP. Un descuento PRE_COST hipotético de 0,5% cambia el redondeo de 4,5 a 4, pero no se ha aprobado ni ejecutado como resolución real de Concordancia.

## Dictamen
**V15 PASS PARCIAL; mantener V07 como candidato sin aprobar.** Fuego nerf considerable; Metal/Viento obtienen beneficios menores al convivir con Concordancias BASE; no alterar los seis monstruos para compensar. Antes de la V16 definitiva hay que resolver prioridades y hooks CONDICIONALES en motor real, calibración de cuatro relaciones, Placa Fundacional/Embalse, PRE_COST, adquisición/coste de artes ajenas y paridad de eventos contra el HTML actualizado. LI permanece 0 puntos, 0 defensivas y 0 AOE.

## Reproducibilidad
Paquete completo `GRULLA_LII_V15_CROSS_TRAMO1_CONCORDANCIAS_2026-10-09.zip`
SHA-256: `a1635eb522537fc91c5173d06c5e9bd5c39e84ebba5a41bd17ad52df29812008`.
**34 entradas**, manifiesto interno SHA-256 y CRC PASS. Incluye `run_cross_v15.py`, `run_holdout_v15.py`, `audit_contract_v15.py`, fuentes V07/V10/V11/V12, monstruos, técnicas, `RAW_*.csv.gz`, controles QA y documentación.

El ZIP binario queda adjunto a la conversación; **no está en Git**. Esta entrada Git contiene el dictamen y el manifiesto QA; para reproducción física se requiere el ZIP.
