# LianQi I — V04B Full Regression Exhaustive — Review

Fecha: 2026-10-07  
Fuente: `LI_V04B_FULL_REGRESSION_EXHAUSTIVE_REVIEW.zip`  
ZIP SHA-256: `3a358477a6ffecd367d6d1b859e0722829fe8c5fee3d63724a50fd1c64b9e0a4`  
Source commit ejecutado: `5897643b89ec21157e2fdae4f593c4fc5f01e2eb`  
Runner SHA-256: `5da44a24a93718d6389817c59d799c80a37a868de0ea99c46ac30dd11f3edd4f`

## 1. Integridad

- ZIP válido; `ZipFile.testzip() = None`.
- 38 archivos.
- Todos los archivos listados en `PACKAGE_MANIFEST.json` verifican SHA-256.
- `issues=[]`.
- Sin NaN numéricos en Attribution, Exhaustive Signature, High-R, Item Marginal, T2 ni Negative Sentinel.
- 7.686.400 combates físicos representados según manifiesto y cardinalidades.
- 2 workers.
- 5 técnicas BASE LI.
- 0 defensivas LI.
- 0 AOE LI.
- 20 pares ordenados: 16 activos + 4 BASE NONE.
- Espacio candidato de equipo: 13 piezas / 4.096 loadouts / 2.688 firmas mecánicas.

## 2. Resultado global

Attribution, mismo cohort y mismas semillas:

- CURRENT_OFF: 57,0953%
- CURRENT_V03_ON: 60,1547%
- PLAYER_RECAL_OFF: 56,6906%
- PLAYER_RECAL_ON: 59,0195%

El sistema candidato completo queda sólo ~1,14 pp por debajo del V03 ON previo, pero corrige casi por completo el desequilibrio entre raíces.

Ganancia de Concordancia:
- V03 universal 10%: +3,059 pp
- V04B relation-specific: +2,329 pp

La nueva Concordancia es menos influyente globalmente y más controlada.

## 3. Raíces

Spread en Attribution:

- CURRENT_OFF: 15,94 pp — Agua 51,57% vs Fuego 67,51%
- CURRENT_V03_ON: 15,06 pp — Agua 54,77% vs Fuego 69,83%
- PLAYER_RECAL_OFF: 3,46 pp
- PLAYER_RECAL_ON: 4,69 pp — Agua 56,39% vs Metal 61,07%

High-R general:
- OFF spread: 3,63 pp
- ON spread: 4,86 pp

Exhaustive 2.688-signature screen:
- Agua ON 61,42%
- Fuego ON 64,17%
- Metal ON 66,79%
- Tierra ON 65,34%
- Viento ON 65,09%

Conclusión: la recalibración de raíces cumple su propósito. Metal queda como raíz de mejor rendimiento medio y Agua como la menor, pero la diferencia global es muy inferior a la de V03 y no presenta un cliff sistémico.

Nota: en el loadout EXPECTED_STAGE hay spreads puntuales mayores (~8,6 pp ON), por interacción raíz×equipo×especie. Se consideran matchups, no una reapertura automática de raíces.

## 4. Concordancias

Exhaustive:
- T0: +2,368 pp
- T1: +2,197 pp

High-R:
- T0: +2,461 pp
- T1: +2,235 pp

Por raíz High-R:
- Agua: +2,316 pp
- Fuego: +2,031 pp
- Metal: +3,549 pp
- Tierra: +2,012 pp
- Viento: +1,832 pp

Por par High-R, el delta real de juego oscila aproximadamente entre +0,98 y +4,32 pp.

Todos los 16 relation_id activos resolvieron en el exhaustive screen:
- mínimo: TIERRA_TO_FUEGO = 465.124 resoluciones
- máximo: VIENTO_TO_METAL = 583.009 resoluciones

Hooks:
- CONTAINED_TRIGGER: 465.124
- CONTROL_POWER: 2.242.741
- CRIT_CHANCE: 548.012
- DIRECT_DAMAGE: 2.766.540
- EVASION_DEBUFF: 572.203
- PERCENT_PENETRATION: 1.668.224
- PRECISION: 554.900

Magma funciona en full-system: en High-R del par Golpe/Palma se observan creaciones, detonaciones y daño real; no queda como hook muerto.

## 5. BASE NONE

Sentinel aislado:

- AGUA_TO_METAL: 0 resoluciones
- AGUA_TO_VIENTO: 0 resoluciones
- METAL_TO_FUEGO: 0 resoluciones
- TIERRA_TO_VIENTO: 0 resoluciones

Total:
- `negative_control_leak = 0.0`
- 9.485,71875 oportunidades negativas medias acumuladas en los 3.200 rows de control
- ningún fallback

Conclusión: PASS fuerte.

## 6. Equipo

Curva canónica High-R:

- NAKED: OFF 39,15% / ON 41,79%
- MANDATORY_ENTRY: OFF 63,48% / ON 65,96%
- EXPECTED_STAGE: OFF 67,80% / ON 69,98%
- HIGH_ROLL_STRESS: OFF 68,55% / ON 70,72%

Saltos ON:
- NAKED → MANDATORY_ENTRY: +24,18 pp
- MANDATORY_ENTRY → EXPECTED_STAGE: +4,01 pp
- EXPECTED_STAGE → HIGH_ROLL_STRESS: +0,74 pp

La mayor parte de la supervivencia inicial viene del Uniforme gris garantizado. Su marginal es ~+22,23 pp ON, por lo que debe entenderse como parte del baseline de aspirante y no como una pieza opcional ordinaria.

Marginal candidato ON:
- Uniforme gris: +22,225 pp — MANDATORY_RISK sólo si se tratara como opcional.
- Pantalón de viaje: +5,850 pp.
- Cuchillo de hueso: +5,450 pp.
- Vendas: +3,475 pp.
- Fajín: +2,350 pp.
- Zapatos: +2,125 pp.
- Bastón candidato TEN+1/PREC+1: +2,000 pp.
- Cinta: +1,963 pp.
- Anillo hierro oxidado: +0,688 pp global.
- Anillo cobre: +0,525 pp global.
- Pulsera candidata QI+1/CONTROL+1: +0,438 pp global.
- Colgante candidato CONTROL+4: +0,200 pp global.

Especialización:
- Anillo hierro oxidado aporta ~+3,44 pp en Agua y ~0 fuera de Agua.
- Anillo cobre aporta ~+2,56 pp en Agua.
- Pulsera aporta ~+2,06 pp en Agua; en contextos Agua+Latigazo llega a ~+3,13 pp.
- Colgante aporta ~+1,09 pp en Agua+Latigazo, pero sigue siendo la pieza más tenue en su nicho.

Conclusión: la mayoría de piezas sí aporta. Las piezas de Qi/control se comportan como especialistas y no como mejoras universales.

Pendientes humanos de equipo:
1. `bandana_lino_simple`: V04B la excluyó de LI como `DEFER_TO_LII_CANDIDATE`. Si se acepta, reconciliar su adquisición M02 antes de modificar el catálogo.
2. `colgante_fragmento_jade`: CONTROL+4 es funcional pero sutil. Puede congelarse como pieza niche o retocarse con un microtest; no justifica otra corrida masiva.
3. `uniforme_gris_aspirante`: conservarlo como baseline garantizado; no usar su marginal contra NAKED para nerfearlo automáticamente.

## 7. Monstruos

High-R ON general:
- Avispa: T0 74,38% / T1 70,36%
- Rata: T0 71,75% / T1 72,83%
- Serpiente: T0 73,71% / T1 67,62%
- Lobo: T0 42,32% / T1 37,85%
- Mono: T0 44,50% / T1 33,46%

Con EXPECTED_STAGE ON:
- Lobo: T0 56,25% / T1 50,06%
- Mono: T0 65,25% / T1 51,31%
- Normales quedan aproximadamente 74,8–83,8% según especie/tier.

El registry clasifica:
- Lobo = `APEX_BRIDGE`
- Mono = `SKIRMISHER`
- Rata / Serpiente / Avispa = `NORMAL`

Por tanto la jerarquía de dificultad observada es coherente con roles distintos. No hay evidencia suficiente para reabrir los T0/T1 congelados.

## 8. T2 stress

Global aproximado:
- OFF 56,87%
- ON 58,95%
- delta +2,08 pp

Por raíz ON:
- Agua 56,17%
- Fuego 58,54%
- Metal 60,55%
- Tierra 59,74%
- Viento 59,77%

Por especie ON:
- Avispa 73,50%
- Lobo 40,50%
- Mono 36,45%
- Rata 76,18%
- Serpiente 68,12%

T2 conserva la estructura del sistema; no revela colapso y sigue tratándose sólo como stress, no target de calibración.

## 9. Exhaustive signature space

2.688/2.688 firmas mecánicas candidatas recorridas.

Distribución ON:
- mínimo 41,4%
- p5 47,2%
- mediana 64,55%
- p95 81,2%
- máximo 86,7%

Delta Concordancia por firma:
- mínimo +0,2 pp
- p5 +1,1 pp
- mediana +2,3 pp
- p95 +3,5 pp
- máximo +4,8 pp

No hay una firma en la que Concordancia produzca un salto sistémico extremo.

## 10. Modelo de respuesta futuro

Como prueba inicial sobre las 2.688 firmas, usando sólo los stats mecánicos de equipo y validación cruzada 5-fold con ExtraTrees:

- predicción de WR ON: MAE ~1,25 pp; R² ~0,983; error absoluto p95 ~3,11 pp.
- predicción de WR OFF: MAE ~1,26 pp; R² ~0,984; error absoluto p95 ~3,06 pp.
- predicción del delta de Concordancia es mucho más difícil: MAE ~0,52 pp pero R² ~0,18.

Conclusión: el dataset ya permite construir un surrogate muy útil para predecir potencia global de equipo y filtrar futuras firmas. No debe usarse todavía como sustituto directo de simulación para interacciones de Concordancia.

## 11. Estado recomendado

- MONSTERS: **PRESERVE**
- TECHNIQUES LI BASE: **PASS**
- ROOTS: **PASS — candidate pack V04B**
- CONCORDANCES: **PASS — candidate relation-specific pack V04B**
- EQUIPMENT: **PASS WITH HUMAN DECISIONS**
- SYSTEM: **READY_FOR_HUMAN_FREEZE AFTER EQUIPMENT DECISIONS**

No se recomienda otra regresión masiva de millones de combates.

Si se decide cambiar únicamente Bandana/Colgante, basta un microgate dirigido. Si se acepta el pack V04B tal como fue probado, el siguiente paso es documentar/fijar los valores y reconciliar adquisición, no volver a simular todo.
