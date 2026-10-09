# PRE-A08 V23 — Equipamiento LII y economía comercial ratificada
**2026-10-09 · LAB PASS / MICROBAlANCE RECOMENDADO · NO CANON / NO RUNTIME / NO A08**

## Autoridad que V21 desconocía
La economía comercial **YA ESTABA RATIFICADA** en otra rama: `experiment/monster-loot-equipment-economy-v0.1`, archivo `experimentos/balance_nuevo/loot_equipment_v0.1/ARC1_COMMERCE_AUTHORITY_V0_4.json` (blob `656641519b93633474bcbe976a2c2aaacb9b5e7f`). Prevalece sobre V02/V03, el split preliminar y los precios legacy de `equipment_arc1_catalog.json`. Contribución **acumulativa y no gastable**, precio de compra en piedras; servicio alternativo con materiales y tarifa donde está ratificado. Los 7 precios institucionales sin piedras en el catálogo antiguo **están resueltos en V04**; no reabrirlos. V22 fue corregido por este hallazgo.

El piloto A07 Ning Cai **ya fue diseñado y auditado por Astra**; su bloqueo `B01_NEW_COMBAT_EQUIPMENT_CONSUMERS_NOT_CONNECTED` es productivo, no una petición para rediseñar comercio. Autoridad de stats: `NEW_COMBAT_STATS_V0_1`, **nunca** puente legacy.

## Experimento V23 nuevo
15 kits de compra hipotética con **precio V04**, tres kits de Sobretúnica duplicados en DEF2/DEF1: **18 brazos**. Seis monstruos normales, cinco raíces, 16 builds por raíz, dos políticas, T1/T2 adaptativos. V17 técnicas con **solo una Concordancia BASE escalar representativa por raíz**, monstruos V19 **ORIGINALES**, sin activar candidatos. Cohortes independientes DISCOVERY 99300–99301 / HOLDOUT 99400–99401: **69.120 + 69.120 = 138.240 duelos**, zero timeout, zero due_missed, seeds pareadas entre kits y DEF, stats/mob originales restaurados. Prueba fría **34.560/34.560 filas y 28 columnas** idénticas aparte de etiqueta `cohort`; no contar en duelos nuevos.

## Resultados T2 combinados (3.840 duelos por brazo)
| Kit | Piedras condicionales | Victoria jugador | vs M03 |
|---|---:|---:|---:|
| M03 base | 0 | **68,93 %** | — |
| Bandana cuero | 7 | 71,59 % | +2,66 pp |
| Calzas sendero pinos | 8 | 77,45 % | +8,52 pp |
| Espada hierro equilibrada | 12 | 79,32 % | +10,39 pp |
| **Sobretúnica DEF2/HP2 (original)** | **12** | **89,61 %** | **+20,68 pp** |
| **Sobretúnica DEF1/HP2 (candidato)** | **12** | **71,59 %** | **+2,66 pp** |
| Bandana + Calzas | 15 | 80,00 % | +11,07 pp |
| Espada + Calzas | 20 | 86,43 % | +17,50 pp |
| Sobretúnica DEF2 + Calzas | 20 | **93,70 %** | +24,77 pp |
| Sobretúnica DEF1 + Calzas | 20 | **80,00 %** | +11,07 pp |
| Espada + Sobretúnica DEF2 | 24 | **93,98 %** | +25,05 pp |
| Espada + Sobretúnica DEF1 | 24 | **81,69 %** | +12,76 pp |
| M05 Túnica Sauces + Sandalias | 21 | 77,34 % | +8,41 pp |
| M05 Calzas + Pulsera cauce | 16 | 80,36 % | +11,43 pp |
| M05 Bandana + Calzas + Pulsera | 23 | 82,60 % | +13,67 pp |
| M05 Espada + Túnica + Sandalias | 33 | 85,60 % | +16,67 pp |
| M06 Aguja + Pulsera tensión | 18 | 75,65 % | +6,72 pp |
| M06 Espada + Pulsera tensión | 19 | 80,29 % | +11,35 pp |

A igualdad de semilla, en los tres kits con Sobretúnica DEF1 vs DEF2 el promedio combinado T2 es **−14,67 pp** de victoria jugador. Cangrejo T2 con M03 **59,38 %**, con Sobretúnica DEF2 **94,84 %**, con DEF1 **63,59 %**. El cambio corrige el breakpoint de defensa plana, sin deshacer la progresión. Las Calzas de pinos (+3 HP,+1 EVA por 8 piedras) ayudan notablemente, pero no existe por ahora evidencia suficiente para otro nerf: **mantener**.

## Decisión de microbalance que recomendamos a aprobación humana
```text
sobretunica_patrulla
stats.defense: 2 → 1
stats.hp_max: 2 (sin cambio)
precio V04: 12 piedras (sin cambio)
Contribution gate V04: 3 acumulada, no gastable (sin cambio)
source_mission: M04 (sin cambio)
```
**No aplicado**. No mutar catálogo original, monstruos, comercio ni HTML antes de ratificación. V19 Cangrejo `DEFENSE_UP +3→+2` y Jabalí `MITIGATE_NEXT 40→35%` siguen candidatos no aprobados. El cruce V20 ya comprobó que favorecen al jugador bajo DEF1 (+5,86 y +2,73 pp T2); por tanto **conservar monstruos originales de momento**, no repetir V19 masivo.

## Límites antes de freeze integral
Los loadouts son **condicionales**: los precios/gates están ratificados, pero el experimento **no acredita fondos obtenidos, permiso efectivo, stock o compra real runtime**. No modela ingresos/reventa/crafting, aflicciones persistentes/antídotos ni las Concordancias defensivas completas (17 escalares, 2 estructurales, 1 NONE y hooks condicionales). Ningún resultado autoriza proclamar paridad productiva A08. Además, V04 tiene inconsistencia pequeña entre sumario LII (`PUBLIC_OPEN_STONES=6`) y desagregado (5 `PUBLIC_OPEN_STONES` + 1 `MATERIAL_SERVICE_ONLY`): usar registros detallados hasta rectificación en la rama dueña.

**Próximo paso real:** ratificar microbalance DEF1, cerrar/etiquetar los gaps físicos restantes (Concordancias estructurales/condicionales y curación de aflicciones) y preparar handoff numérico para Astra separado de su implementación B01. No reabrir comercio. NO `main`, NO merge, NO `ROOMS.exits`, NO modificar A07 ni ver76, NO LLM libre.

## Reproducción
ZIP portable preparado por este frente: `GRULLA_PRE_A08_V23_BALANCE_EQUIPO_Y_ECONOMIA_RATIFICADA_2026-10-09.zip`; SHA256 `1ee935e77c3461391739d94fdff6aee0ace80f5ef30031abcadc5cc09ab1789d`; 44 entradas, ZIP CRC+manifest PASS y smoke de carpeta limpia PASS 34.560 casos. Contiene `run_v23_affordable.py`, `analyze_v23.py`, inputs de autoridad extraídos V04, dependencias V17–V20, todos los RAW gzip, QA y análisis. **El ZIP no fue subido al repositorio**: se entrega como adjunto a la conversación. Git conserva decisión y QA documental.
