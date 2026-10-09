# PRE-A08 V22 — CORRECCIÓN POR AUTORIDAD DE COMERCIO YA RATIFICADA
**Fecha:** 2026-10-09. **Estado:** auditoría documental corregida; **NO implementación runtime**. **Esta revisión reemplaza íntegramente la primera versión de V22**, que erróneamente trataba precios/gates y clasificación ya resueltos como decisiones pendientes.

## 1. Fuente de autoridad recuperada (otra rama, SOLO LECTURA)
Repositorio: `Shein25/La-Grulla-Blanca`.
Rama de diseño: `experiment/monster-loot-equipment-economy-v0.1`.
Directorio: `experimentos/balance_nuevo/loot_equipment_v0.1/`.
- `ARC1_COMMERCE_AUTHORITY_V0_4.json` (blob `656641519b93633474bcbe976a2c2aaacb9b5e7f`, `HUMAN_RATIFIED_DESIGN_AUTHORITY__PRE_IMPLEMENTATION`): **supersede** V03, V02 y split preliminar; 68 ítems, canales, precios, gates y políticas de materiales.
- `ARC1_MERCHANT_CAPABILITIES_V0_1.json` (blob `e794ffa5e3b6b6627c92b5b23479b05d54300a5c`): capacidades aprobadas de NPC; no inferir vendedor por `source_npc`.
- `ARC1_COMMERCE_TRANSACTION_CONTRACT_V0_1.json`: pipeline atómico, sin autoridad de UI/IA para mutaciones.
- `ARC1_COMMERCE_CATALOG_UI_V0_1.json`: UI catálogo MUD vía conversación, no parser público.
- `ARC1_CONTRIBUTION_CLEANSLATE_V0_1.json`: Contribución acumulativa única, no gastable.
- `ARC1_EQUIPMENT_RUNTIME_BINDING_V0_1.json`: 11 slots, ARRAY_PER_SLOT, stats nuevos sin traducción legacy.
- `ARC1_COMMERCE_SLICE1_A07_PREFLIGHT_V0_1.json`: piloto Ning Cai ratificado.
- `backups/HANDOFF_CONVERSACION_GRULLA_COMERCIO_B01_2026-10-02.md`: auditoría Astra Slice1 aceptada y bloqueador B01 documentado.
- `backups/ACLARACION_B01_NEW_COMBAT_STATS_DEPRECATED_LEGACY_2026-10-02.md`: único destino válido `NEW_COMBAT_STATS_V0_1`, no legacy.
Estos archivos **no están físicamente en la rama V21/V22**. Leerlos desde la rama indicada; no inventar su ausencia ni copiarlos automáticamente al runtime.

## 2. Dictamen corregido: comercio LianQi II 21/21
Conteo derivado de **entradas efectivas** en `ARC1_COMMERCE_AUTHORITY_V0_4.json`:
- **11** `INSTITUTIONAL_STONES_GATE` (piedras + Contribución acumulada como requisito, nunca restada).
- **5** `PUBLIC_OPEN_STONES`.
- **4** `PUBLIC_CONTEXTUAL_STONES` (permiso local existente, sin coste de Contribución).
- **1** `MATERIAL_SERVICE_ONLY` (solo servicio con materiales, sin sustituto 100% piedras).

| ID LII | Canal autorizado de diseño | Precio piedras | Contribución mínima | Fuente hito | Referente nominal |
|---|---|---:|---:|---|---|
| `espada_hierro_equilibrada` | INSTITUTIONAL_STONES_GATE | 12 | 3 | M04 | Lu Cheng |
| `sable_patrulla_valle` | INSTITUTIONAL_STONES_GATE | 10 | 3 | M04 | Lu Cheng |
| `aguja_acero_frio` | INSTITUTIONAL_STONES_GATE | 11 | 8 | M06 | Lu Cheng |
| `bandana_cuero_reforzada` | INSTITUTIONAL_STONES_GATE | 7 | 3 | M04 | Ning Cai |
| `capucha_observador_valle` | PUBLIC_OPEN_STONES | 7 | 0 | M05 | Puestos del Mercado del Valle |
| `sobretunica_patrulla` | INSTITUTIONAL_STONES_GATE | 12 | 3 | M04 | Jiang Rui |
| `tunica_ruta_sauces` | PUBLIC_CONTEXTUAL_STONES | 10 | 0 | M05 | Artesanos de Sauces |
| `brazales_cuero_cruzado` | INSTITUTIONAL_STONES_GATE | 9 | 3 | M04 | Ning Cai |
| `brazales_pulso_firme` | INSTITUTIONAL_STONES_GATE | 9 | 8 | M06 | Chen Bo |
| `fajin_patrulla` | INSTITUTIONAL_STONES_GATE | 10 | 3 | M04 | Jiang Rui |
| `calzas_sendero_pinos` | PUBLIC_OPEN_STONES | 8 | 0 | M04 | Ning Cai |
| `sandalias_corriente_ligera` | PUBLIC_CONTEXTUAL_STONES | 11 | 0 | M05 | Artesanos de Sauces |
| `botas_piedra_humeda` | PUBLIC_OPEN_STONES | 9 | 0 | M05 | Puestos del Mercado del Valle |
| `amuleto_colmillo_montado` | MATERIAL_SERVICE_ONLY | — | 0 | M05 | Ning Cai |
| `amuleto_sauce_sereno` | PUBLIC_CONTEXTUAL_STONES | 10 | 0 | M05 | Artesanos de Sauces |
| `pulsera_cauce_trenzado` | PUBLIC_CONTEXTUAL_STONES | 8 | 0 | M05 | Artesanos de Sauces |
| `anillo_sello_hierro` | INSTITUTIONAL_STONES_GATE | 8 | 8 | M06 | Lu Cheng |
| `anillo_corriente_clara` | PUBLIC_OPEN_STONES | 10 | 0 | M05 | Puestos del Mercado del Valle |
| `pulsera_tension_meridiana` | INSTITUTIONAL_STONES_GATE | 7 | 8 | M06 | Lan Meihua |
| `calzas_guardia_externa` | INSTITUTIONAL_STONES_GATE | 10 | 3 | M04 | Jiang Rui |
| `anillo_reserva_menor` | PUBLIC_OPEN_STONES | 8 | 0 | M05 | Puestos del Mercado del Valle |

**Siete precios falsamente declarados «pendientes» en V21/V22 inicial:** aguja 11; sobretúnica 12; brazales pulso firme 9; fajín patrulla 10; anillo sello hierro 8; pulsera tensión meridiana 7; calzas guardia externa 10. Todos son `INSTITUTIONAL_STONES_GATE` y sus umbrales acumulativos siguen autoridad V04.

**Inconsistencia menor en resumen precalculado V04:** `stage_summary.LianQi_II` declara `PUBLIC_OPEN_STONES: 6`, pero el array `equipment` cuenta **5 public open + 1 material only**. No corregir ni mutar la autoridad de otra rama; usar las 21 entradas detalladas como evidencia y avisar al custodio del contrato.

## 3. Economía y extracción ya diseñadas: NO REABRIR
- Moneda de compra: piedras espirituales; Contribución es acumulativa, monotónica, no se descuenta; méritos y reputación son dimensiones separadas.
- Venta: especialistas con `BUY` explícito, no compra universal. La mercancía vendida por el jugador se destruye económicamente por defecto (`sink`), no pasa automáticamente a stock visible.
- Servicio alternativo: equipo público o institucional puede tener una receta NPC de materiales + tarifa reducida. Acceso institucional sigue sujeto al umbral de Contribución/permiso. Drops automáticos **≠** extracción espiritual; ambas fuentes pueden requerirse en la misma receta.
- `amuleto_colmillo_montado`: servicio exclusivo de **1 `colmillo_lobo_legitimo` + 1 `tendon_tres_colas` + 2 piedras**. No venderlo directamente por piedras.
- `aguja_acero_frio`: compra institucional 11 piedras **o** servicio de 1 `fragmento_caparazon_jade` + 1 `camara_jade` + 4 piedras; acceso requiere Contribución 8. 
- La autoridad contiene tablas de recompra especializada por unidad y lotes de extracción, probabilidades de extracción rediseñadas (simple 60%, normal 45%, difícil 30%, muy difícil 18%; bono novato +5 pp; cap 90%). No recalibrar aquí sin nueva evidencia.
- Se ratificó **purga de legacy** en integración futura, sin migración de saves, aliases, compatibilidad ni coexistencia.
- No atribuir automáticamente capacidad SELL a Jiang Rui / Chen Bo / Lan Meihua: el registro ratificado diferencia `AUTHORIZE`, `FULFILL`, `SERVICE`, `SELL`, `BUY`.

## 4. Integración A07: diseñada y ratificada, pero no declarar «jugable»
Piloto `ning_cai`, `taller_ning_cai`: `calzas_sendero_pinos` 8 piedras, `ROUTINE_UNLIMITED`, M04 realmente completada, LianQi II, `hp_max +3`, `evasion +1`. Flujo por `HABLAR -> handler canónico primero -> host A07 -> DOMAIN:COMMERCE -> catálogo`. No nuevos comandos públicos.
Pipeline: `EVALUATE -> CONFIRM -> REVALIDATE -> BUILD_DELTA -> COMMIT -> RECEIPT`; replay/doble clic protegido, transacción atómica; regreso a diálogo sin relanzar misiones.
Handoff B01: `SLICE1_A07_INTEGRATION_BLOCKED`; auditoría Astra **aprobada**, sin cambios al HTML. Bloqueador: `B01_NEW_COMBAT_EQUIPMENT_CONSUMERS_NOT_CONNECTED`. Próximo trabajo en ese frente: `NEW_PLAYER_STATS_EQUIPMENT_PRODUCTIVE_BINDING_PREFLIGHT`; no reiniciar auditoría Astra ni implementar Comercio prematuramente.

## 5. Impacto preciso sobre V21 y futuro V23
- **V21 batalla permanece un resultado histórico reproducible**, no se reejecuta; su **diagnóstico económico del catálogo solo** quedó superado por la autoridad V04. No cambiar sus CSV crudos ni resultados.
- El trabajo pertinente del frente balance ahora es **consumir los loadouts y umbrales V04 como autoridad documental**, identificar qué combinación por misión es factible económicamente según tablas existentes, y aislar los verdaderos gaps de runtime/corredor. No rediseñar precios, vendedores, Contribución o barter.
- V19 (Cangrejo, Jabalí), V20 (Sobretúnica DEF2→1 manteniendo HP+2) siguen **candidatos no ratificados**; no modifican contratos de comercio.
- Diferenciar: `HUMAN_RATIFIED_DESIGN_AUTHORITY__PRE_IMPLEMENTATION` **≠** runtime implementado; `LAB` **≠** canon productivo.
- Prohibido tocar `main`, merge, A07 congelado, `ROOMS.exits`, NPCs, misiones, gates, HTML sin autorización.

## 6. QA documental de esta corrección
- Autoridad V04 verificada por blob; 68 entradas, LII 21, canales {"INSTITUTIONAL_STONES_GATE":11,"PUBLIC_OPEN_STONES":5,"PUBLIC_CONTEXTUAL_STONES":4,"MATERIAL_SERVICE_ONLY":1}.
- Siete precios resueltos contrastados contra V04, no extrapolados desde el catálogo legacy.
- Handoff B01 y documento de aclaración examinados directamente desde la rama de comercio.
- **No se ejecutaron nuevos combates ni se hicieron cambios en runtime**. La única mutación es este documento V22 en la rama de balance.
