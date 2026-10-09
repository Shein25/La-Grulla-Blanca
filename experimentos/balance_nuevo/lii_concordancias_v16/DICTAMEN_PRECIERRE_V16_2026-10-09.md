# V16 — Pre-cierre estructural y auditoría de paridad de LianQi II

**Fecha:** 2026-10-09  
**Estado:** PASS PARCIAL DE LABORATORIO / NO CANON / NO FREEZE / NO RUNTIME.  
**Rama:** `experiment/lii-tramo1-multirraiz-v08-2026-10-08`. No se toca `main`, no merge, no cambios de HTML ni stats.

## 1. Qué se ejecutó REALMENTE

Se cruzaron técnicas originales y **candidato V07** con Concordancia estructural **OFF/ON**, mediante el *puente físico experimental* LI V04B aplicado a LianQi II. Esta batería cubre exclusivamente:
- **Tierra→Metal / Placa Fundacional**
- **Tierra→Agua / Embalse**

**Dos campañas independientes:** 36.864 + 36.864 = **73.728 peleas**; **18.432 contextos de cuatro brazos**. Seeds 27100–27103 y 28100–28103, sin intersección.

Factores: 2 raíces receptoras × 6 monstruos normales × T0/T1/T2 × 2 equipos POST_M03/EXPECTED_STAGE × 2 políticas EARLY/DELAYED_TRIGGER × 16 builds monorraíz por raíz × 4 seeds/campaña × 4 brazos. **No se ejecutaron** Concordancias condicionales de Tramo I, cuatro escalas aún sin ratificar, economía/adquisición real de arte extranjera, ni motor HTML real.

Brazos `ORIGINAL_OFF`, `ORIGINAL_ON`, `V07_OFF`, `V07_ON`. El único nodo alterado por V07 dentro de esta prueba es **Metal / Ejecución +10 pp críticos**; Agua no tiene cambio V07 y funciona como control nulo.

## 2. QA y reproducción

| Control | Resultado |
|---|---|
| Fights | **73.728** |
| Contextos de cuatro brazos | **18.432** |
| Timeouts | **0** |
| Acciones programadas de monstruo omitidas | **0** |
| Resoluciones ON | **32.028** |
| Resoluciones OFF | **0** |
| Preservaciones de primera placa ON | **16.566** |
| Golpes reforzados ON | **16.285** |
| Embalse: unidades almacenadas ON | **4.547,6064** |
| Embalse: unidades liberadas ON | **3.757,3146** |
| Builds sin nodo V07 | **16.128 contextos con igualdad exacta ORIGINAL↔V07** |
| Reproducción desde ZIP extraído a carpeta limpia | **9.216 filas idénticas, sin desviaciones** |
| Integridad del ZIP | **CRC y SHA-256 por miembro PASS** |

Las transformaciones estructurales fueron ejecutadas físicamente en el *puente de laboratorio*. **Esta prueba NO demuestra paridad con el motor del juego.**

## 3. Resultado focal: Metal con nodo Ejecución seleccionado

Contra T2 y equipo POST_M03, usando los dos cohorts (**384 contextos**):

| Escenario | Victorias jugador |
|---|---:|
| ORIGINAL_OFF | 74,219 % |
| ORIGINAL_ON (Placa) | 82,812 % |
| V07_OFF | 77,865 % |
| V07_ON (Placa) | 84,896 % |

V07 añade **+2,083 pp** con Placa ON; la Placa por sí sola suma **+8,594 pp** en el original y **+7,031 pp** en V07. Interacción: **−1,5625 pp** (solapamiento parcial). No sumar los bonos como si fueran independientes.

Desglose por las seis especies queda en `PAIRED_V16_STRUCT.csv.gz` (dentro de ZIP); no optimizar sobre los mismos seeds. La confirmación independiente da +2,083 pp V07_ON en este grupo.

Agua, con Embalse, permaneció **idéntica** entre ORIGINAL y V07. En T2 POST_M03 ganó **63,021 %** tanto ON como OFF, aunque sí hubo activaciones físicas de almacenamiento/liberación.

## 4. Contrato y motor: BLOQUEOS DEL FREEZE

### Hook Tramo I, 80 builds × 4 Ecos = 320 contextos
Auditoría independiente `audit_conditional_v16.py`:
- 240 contextos solo BASE;
- 16 con prioridad condicional bien determinada por mapeo;
- 60 con hook condicional expuesto pero efecto/precedencia no demostrado;
- 4 de **Agua→Viento / Paso de Nube** presentan discrepancia entre el resumen de receptor y la matriz general; no inventar una prioridad.

El PRE_COST de Espejo de Luna mantiene breakpoint: BASE raw 5,25→5 Qi; Eficiencia 4,50→5 Qi. Un descuento porcentual experimental previo al HALF_UP puede producir 5→4, **pero no existe validación de ese descuento en runtime**. No congelar solución inventada.

### Cuatro relaciones numéricas LII sin autoridad ratificada
`METAL_TO_FUEGO`, `AGUA_TO_METAL`, `AGUA_TO_VIENTO`, `TIERRA_TO_VIENTO`. Las escalas V14 fueron hipótesis de sensibilidad, **no valores canónicos**.

### HTML de comparación disponible
`grulla-blanca_ver76_A07_9_G03_B1_B4_CANDIDATE.html` contiene la **tabla v49 de siete secuencias** y bonos genéricos, mientras el contrato contemporáneo exige **20 relaciones dirigidas** y primer hook compatible. Este HTML B1_B4 es un **candidato anterior**, NO autoridad vigente. Ausencia textual de `PLACA_FUNDACIONAL` o `EMBALSE` no prueba que no exista mecánica equivalente.

**Paridad de eventos contra HTML vigente:** no ejecutada; no se dispone de motor vigente sincronizado en este paquete.

### Técnica BASE extranjera
El puente permite lanzar una ofensiva extranjera suponiendo que fue aprendida. Su disponibilidad narrativa, tier, coste real, penalidades y ganancias de afinidad NO están reconciliados contra el motor actualizado. No afirmar que los porcentajes multirraíz son canon.

## 5. Decisión y ruta de cierre

**V16 estructural = PASS experimental. Freeze integral = BLOQUEADO POR AUTORIDAD/PARIDAD.**

Para convertirla en V16 definitiva:
1. Resolver documentalmente las cuatro prioridades de Paso de Nube con Agua.
2. Aprobar o descartar **candidatos numéricos específicos** para las cuatro relaciones y para Placa/Embalse; el análisis V12–V14 sirve de punto de partida, NO de norma.
3. Exigir a integración el **HTML vigente** con las 20 relaciones, T1 condicionales, Eco, PRE_COST, aprendizaje y costes reales. No basta el candidato B1_B4.
4. Ejecutar `event-by-event` frente al puente (sin atajos por win-rate) y regresar a LI para validar 0 PT, 0 defensivas, 0 AOE.
5. Solo después repetir comparación original/V07 completa con los seis monstruos T0–T2, 16 builds × 5 raíces, equipos y políticas; decidir ajuste de técnicas.

No tocar números de monstruos ni aceptar V07 todavía. **No ejecutar nueva batería general masiva mientras falte autoridad mecánica**, porque arrojaría solo otra sensibilidad en un modelo incompleto.

## 6. Reproducibilidad

ZIP de laboratorio: `GRULLA_LII_V16_PRECIERRE_ESTRUCTURAS_Y_PARIDAD_2026-10-09.zip`. Incluye 46 archivos: scripts de V16, código/fuentes V15/V12/V11/V10/V07 de referencia, datos de ambas campañas, auditores contractuales, HTML antiguo claramente etiquetado como referencia y manifiesto SHA-256. La copia se ejecuta desde cero con `--reps 1 --start 27100` y reproduce exactamente 9.216 filas.

ZIP SHA-256: `1907dde5c6a1478899d11c8af75cd637a33c7fa68c5a28ce1355162bbdc93838`. Fuente V16 SHA-256: `69cdeb1034d8c9993573eeedb5f64d68b812ee8f509ae254c878e2cd2b0ccb3c`.

**Guardias:** no main, no merge/push, no nuevos NPCs/rooms/gates, no cambios de monstruos ni equipo, sin élite ni T3/T4, sin Tramos en LI, sin número canónico inferido del laboratorio.
