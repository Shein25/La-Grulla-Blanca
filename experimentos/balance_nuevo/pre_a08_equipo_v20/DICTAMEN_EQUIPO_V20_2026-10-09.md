# La Grulla Blanca — V20 · Equipamiento LianQi II antes de A08

**Fecha:** 2026-10-09 · **Estado:** LAB PASS / RECOMENDACIÓN DE MICROBALANCE / NO CANON / NO HTML / NO MAIN.

## 1. Pregunta de diseño

Tras los ensayos V17–V19, `EXPECTED_STAGE` producía porcentajes de victoria ~97–99 % contra criaturas normales de LianQi II. Se evaluó **qué piezas provocaban el salto** con técnicas V17 congeladas, T0/T1/T2, seis monstruos normales originales (sin activar todavía los candidatos V19 en el screen principal), 16 builds monorraíz por cada una de cinco raíces y estrategias EARLY/DELAYED_TRIGGER.

**Fuente numérica:** `equipment_arc1_catalog.json`, esquema `arc1-equipment-v0.2`, 68 piezas (14 LI, **21 LII**, 19 LIII, 14 LIV). 14 loadouts comparativos; las piezas LII son diseño PROVISIONAL y no se acreditó compra/canje jugable. La fuente de referencia de semillas se mantuvo fija en `POST_M03`, cambiando únicamente los objetos equipados (Common Random Numbers). Por raíz se eligió **una** relación BASE de Concordancia defensiva V17 aplicable, no las veinte; no se simularon transformaciones estructurales ni hooks condicionales de Tramo I. Se asume, solo en laboratorio, la técnica ajena necesaria para generar Eco. Las estadísticas se recuperaron del catálogo después de cada microtest.

## 2. Cuatro campañas completas y controles

| Bloque | Discovery | Holdout | Total |
|---|---:|---:|---:|
| 14 kits × cinco raíces × seis monstruos × T0/T1/T2 × 16 builds × dos políticas | 80.640 | 80.640 | **161.280** |
| Sobretúnica con DEF 0/1/2 vs uniforme M03 × T1/T2 | 30.720 | 30.720 | **61.440** |
| Monster V19 ORIGINAL/CANDIDATE × Sobretúnica/M03 × T1/T2 | 15.360 | 15.360 | **30.720** |
| `EXPECTED_STAGE` vestidura DEF2 vs DEF1 sin tocar otros ítems × T1/T2 | 15.360 | 15.360 | **30.720** |
| **Total** | **142.080** | **142.080** | **284.160** |

Semillas independientes: 91000–91001/92000–92001; 93000–93003/94000–94003; 95000–95003/96000–96003; 97000–97003/98000–98003. **0 timeouts, 0 técnicas de cadencia omitidas, mismo seed dentro de cada comparación**, y cambios a vestidura/monstruo restituidos en memoria. Una prueba inicial de 40.320 combates se excluyó del total. Las cifras descriptivas no equivalen a prueba de adquisición real.

## 3. ¿Qué produce el salto? (T2, resultados de jugador)

En el screen de 14 kits, 3.840 combates T2 por kit:

| Kit | WR T2 | Diferencia vs M03 |
|---|---:|---:|
| PROLOGUE (espada madera + uniforme) | 69,92 % | −0,05 pp |
| **M03_ISSUED** (lo anterior + fajín M03) | **69,97 %** | base |
| + Bandana cuero reforzada | 72,97 % | +3,00 pp |
| + Sandalias corriente ligera | 75,05 % | +5,08 pp |
| + Espada hierro equilibrada | 79,19 % | +9,22 pp |
| + Túnica ruta Sauces (DEF1/EVA3) | 73,59 % | +3,62 pp |
| + **Sobretúnica patrulla DEF2/HP2** | **89,87 %** | **+19,90 pp** |
| Sobretúnica DEF2 + espada hierro | 93,96 % | +23,98 pp |
| `EXPECTED_STAGE` de siete piezas | **96,85 %** | **+26,88 pp** |

Por tanto, no corresponde mejorar universalmente los seis monstruos ni nerfear todas las piezas: **vestidura DEF2 es la fuente dominante en LII**. El equipamiento esperado no es una dotación garantizada.

## 4. Breakpoint físico de defensa plana aislado

Se mantuvo la Sobretúnica con **HP+2** y se cambió **solo su DEF**; 7.680 combates T2 por brazo:

- M03 con uniforme (DEF1, HP+1): **69,47 %** victoria del jugador.
- Sobretúnica DEF0/HP2: **50,43 %**.
- Sobretúnica **DEF1/HP2: 72,38 %**.
- Sobretúnica **DEF2/HP2: 90,53 %**.

Un único punto DEF2→DEF1 reduce **18,15 puntos** sobre las mismas semillas; frente a M03, la Sobretúnica nerfeada sigue aportando +2,92 puntos de victorias y HP extra. El salto DEF2→DEF1 es especialmente fuerte contra Cangrejo (**27,89 pp**), y afecta a los seis monstruos. El daño básico y DoT actuales atraviesan la defensa según sus contratos; **no usar 0 daño salvo absorción**.

Además, sobre los siete objetos inalterados de `EXPECTED_STAGE`, DEF2→DEF1 reduce el T2 de **96,32 % a 88,37 %** (7.680 combates por brazo) y evita el techo casi automático sin borrar la progresión.

## 5. Cruce controlado con los candidatos de monstruos V19

La matriz incluye a los dos monstruos Original/Candidate y los kits M03, Sobretúnica DEF1 y DEF2 (T1/T2). En T2 y DEF1, 1.280 comparaciones por versión:

| Monstruo | Original + Sobretúnica DEF1 | Candidato V19 + Sobretúnica DEF1 | Efecto candidato |
|---|---:|---:|---:|
| **Cangrejo de Cauce** | 66,25 % | **72,11 %** | **+5,86 pp** victoria jugador |
| **Jabalí de Pizarra** | 74,69 % | **77,42 %** | **+2,73 pp** victoria jugador |

Los candidatos V19 conservan su efecto con el ajuste de armadura (Cangrejo T1 DEFENSE_UP +3→+2; Jabalí T1 MITIGATE_NEXT 40→35 %), **sin autorizarlos aún**. Con Sobretúnica DEF2 existe techo >90 %, que reduce su relevancia y oculta diferencias reales.

## 6. Auditoría de adquisición y economía: BLOQUEO DOCUMENTAL

El catálogo Etapa18 **sí contiene 68 piezas** en su v0.2; versiones previas de 58 quedaron superadas. **Las 21 piezas LII aparecen OPTIONAL**, con misión de procedencia M04 (8), M05 (9) o M06 (4). Los campos `source_mission`, `source_npc`, `required_permission` y `source_type` son propuestas de diseño, NO evidencia de que las tiendas, inventarios y misiones ya permitan obtenerlas.

Hay **42 piezas del Arco 1 con `price_contribution`**, de ellas **10 de LII**, pero la decisión humana del frente de comercio es **deprecar el gasto de Contribución**. La propuesta anterior de gastar puntos no puede canonizarse. Es necesario decidir de forma verificable si la Contribución funciona como *umbral/requisito de reputación* (no se resta), y cómo se pagan los objetos con piedras, materiales, canje o misión, sin inventar NPCs, permisos o fuentes. No convertir automáticamente «requiere contribución» en «puede comprarse» ni fijar precios nuevos sin estudio de generación de recursos y sinks.

Referencias: `docs/experimentos/AUDITORIA_EQUIPO_Y_PROGRESION_ARCO1_2026-09-29.md`, `docs/experimentos/ETAPA18_EQUIPO_ARCO1_DISENO_COMPLETO_2026-09-29.md` y catálogo numérico v0.2. El documento Etapa18 sigue indicando «Contribución se gasta» y debe actualizarse *con la decisión humana actual* antes de entregarse a Astra. El objeto único `espejo_pulso_velado` no se rebalancea en este frente.

## 7. Propuesta de decisión para el siguiente paso

**Candidato V20:** `sobretunica_patrulla` — `stats.defense: 2 → 1`, `stats.hp_max: 2` sin cambios. No tocar Uniforme LI, estatísticas de otras piezas, `technique_direct_damage_percent`, precio ni monstruos por este experimento. Otras vestiduras más avanzadas LIII/LIV se revisarán al llegar a sus etapas, no ahora.

**No congelar aún toda la economía del equipo.** Antes de una entrega A08, verificar: (1) disponibilidad real M04/M05/M06 y permisos; (2) propuesta de precio compra/venta/canje coherente con piedras y materiales; (3) Contribución no gastable; (4) perfiles de carga realisticamente obtenibles para LII; (5) regresiones finales V17 habilidades + V19 monstruos + armadura V20, aflicciones y consumibles.

**Guardias:** no `main`, no merge, no alteraciones del HTML, inventarios oficiales, `ROOMS.exits`, equipo ni monstruos canónicos. T0/T1/T2 son tiers adaptativos, no reinos de cultivo; élites/T3/T4 excluidos. Todos los números son *de laboratorio* y requieren decisión humana antes de freeze.

## 8. Verificación de entrega

El paquete ZIP pasó CRC y SHA-256 para sus 76 entradas. Se extrajo en una carpeta limpia y reprodujo exactamente **55.680 duelos** de los cuatro corredores independientes (40.320 + 7.680 + 3.840 + 3.840), todas las columnas. SHA-256 del ZIP final: `1d4834dd3d12b2ed34798975d59a25b2233277bc7ae5594f9e3665863c321851`.

Los cuatro corredores y todas sus dependencias de laboratorio están en el ZIP descargable; los binarios grandes no fueron subidos a Git. Las cifras y recomendaciones son experimentales y no representan modificación del runtime.
