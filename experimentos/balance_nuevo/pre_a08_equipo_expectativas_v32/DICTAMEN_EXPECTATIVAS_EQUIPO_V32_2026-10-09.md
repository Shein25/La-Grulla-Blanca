# PRE-A08 V32 — Balance según etapa y expectativas del equipamiento
**Fecha 2026-10-09 · LAB PASS, NO CANON, NO RUNTIME, SIN ECONOMÍA.**
Autoridad humana: [Principio ratificado](../../handoffs/PRINCIPIO_RATIFICADO_EXPECTATIVA_PROGRESION_EQUIPO_2026-10-09.md) (ruta en Git: `experimentos/balance_nuevo/handoffs/PRINCIPIO_RATIFICADO_EXPECTATIVA_PROGRESION_EQUIPO_2026-10-09.md`). *Nota: el enlace relativo aquí es secundario; la ruta explícita es la referencia.*

## Contrato de progresión verificado
- **Uniforme gris de aspirante**, LI, P: `DEF+1, HP+1`.
- **Sobretúnica de patrulla**, LII, M04: **`DEF+2, HP+2`**, máxima DEF de cualquier VESTIDURA LII.
- **Túnica de ruta de Sauces**, LII, M05: `DEF+1, EVA+3, HP+1`, alternativa ligera.
- **Túnica reforzada de trama de cobre**, LIII, M08: `DEF+3, HP+2`, escalón posterior.
Estos campos provienen del catálogo `equipment_arc1_catalog.json` de 68 entradas, **diseño experimental, no prueba de disponibilidad productiva**.

## Matriz V32 — nueva
Seis monstruos normales V19 ORIGINALES; cinco raíces, 16 builds/raíz; T1/T2, EARLY/DELAYED_TRIGGER, una relación V17 BASE SCALAR representativa por raíz. Equipamiento M03 mínimo (espada madera+fajín+vestidura) y M05 común hipotético (espada hierro+fajín+calzas pinos+vestidura). Cuatro brazos por dotación: Uniforme, Sobretúnica DEF2, Sauces EVA3, Sobretúnica DEF1 **solo control**. Igual monstruo/raíz/tier/política/build/RNG dentro de ocho brazos. No cambios canónicos, sin precios ni comercio.

DISCOVERY `107100–107101`: **30.720 combates**, HOLDOUT `107500–107501`: **30.720**, total **61.440 combates nuevos** y 7.680 contextos pareados ×8. COLD reejecutado fuera del workspace, con dependencias del ZIP: **15.360 filas ×30 columnas exactamente iguales** a rep 107100 de DISCOVERY (sin `cohort`), no sumadas como combates nuevos. 0 timeouts, 0 cadencias incumplidas, 100% de habilidades de monstruo y estadísticas de Sobretúnica originales restauradas.

## Victoria de jugador T2, 3.840 peleas por celda
| Vestidura | Dotación mínima post M03 | Dotación común simulada M05 |
|---|---:|---:|
| Uniforme anterior | 69,82% | 86,82% |
| **Sobretúnica DEF2 original** | **89,53%** | **96,59%** |
| Túnica ligera Sauces | 73,78% | 88,59% |
| Sobretúnica DEF1 contrafactual | 72,71% | 88,62% |

La Sobretúnica original es **+19,71 pp** frente al uniforme en T2 con dotación mínima; un avance perceptible de su especialidad de protección. Con dotación común M05 la Sobretúnica supera a Sauces por **+7,99 pp**. La ventaja se reproduce en ambos cohortes y frente a cada una de las seis especies.

**Túnica de Sauces**: 17,41 evasiones por 100 rondas, contra 14,65 de Sobretúnica con dotación común (+2,76), y sube +1,77 pp de victoria frente al uniforme con el mismo acompañamiento. La evasión existe, pero no compensa DEF2 contra los monstruos normales seleccionados; todavía no se identificó una especialización con mejor victoria. En todos los monstruos se observa más evasión de Sauces.

**Sobretúnica DEF1**: sin otros cambios pierde su papel de máxima protección: 72,71% frente a 73,78% de Sauces en M03 y 88,62% frente a 88,59% en M05 común. Además, rompería el escalón legible LI DEF1 → LII DEF2 → LIII DEF3. Esta evidencia refuerza el mandato de **NO aplicar el candidato DEF2→1**. Preservar los datos históricos V20–V31 sin tratarlos como autorización de nerf.

## Dictamen
1. **Mantener intacta la Sobretúnica** `sobretunica_patrulla.stats.defense=2`, `hp_max=2`. Su alta supervivencia contra monstruos normales cumple la expectativa de equipo superior. El nerf DEF1 está **SUSPENDIDO y solo disponible como experimento**; no enviar como cambio a Astra.
2. **No buffear automáticamente la Túnica de Sauces**: investigar con los peligros reales apropiados para LII si la EVA tiene valor diferenciador (ataques que causan estados al acertar, impactos potentes, distribuciones de precisión), sin inventar monstruos ni romper la progresión con la vestidura ligera LIII (EVA+4/Qi+2).
3. 96,59% de victoria en una dotación rica ante criaturas normales T2 revela un techo en *esta muestra*, no una obligación de nerfear equipo. Comprobar desafíos pertinentes y si realmente se consigue la dotación antes de decidir dificultad.
4. **No FREEZE PRE-A08**: una relación escalar BASE por raíz, no todas las relaciones, sin hooks estructurales/condicionales V24/V26, ni aflicciones persistentes V27–V30, élites/T3/T4/jefes/AOE, ni runtime. No abrir comercio, precios, NPC, inventario ni autoridad A07.

## Reproducción
ZIP fuera de Git: `GRULLA_PRE_A08_V32_EXPECTATIVA_Y_PROGRESION_EQUIPAMIENTO_2026-10-09.zip`; SHA256 `329d95bea1925565e6c2b441e008249071788b08333c2af84ccded50ce59d603`; **58 archivos**, CRC/manifiesto SHA256 PASS, COLD desde carpeta extraída PASS. Scripts `run_v32_expectations.py` SHA256 `7362baa8e09903dbe49b12f31d686edd88f475dddb15cd573fc50907189f4152` y `analyze_v32_expectations.py` SHA256 `be972f5038f896d7b35b8b8a89ead5efce2ad7c09e30cf18470570ddf120e2a6`. ZIP contiene CSV brutos y análisis por monstruo, raíz y cohorte con todas las dependencias.

Guardias: rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`, sin `main`, sin merge, sin HTML, sin `ROOMS.exits`, sin modificación de datos canónicos, economía o precios.
