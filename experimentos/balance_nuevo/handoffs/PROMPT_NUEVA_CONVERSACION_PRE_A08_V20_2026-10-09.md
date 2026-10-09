# Prompt de reanudación — La Grulla Blanca · Pre-A08 (corte V20)

Retomá el proyecto **La Grulla Blanca** desde el **HANDOFF PRE-A08 V20 (2026-10-09)**. Repositorio oficial: https://github.com/Shein25/La-Grulla-Blanca. Rama de trabajo y documentación: `experiment/lii-tramo1-multirraiz-v08-2026-10-08`. **No tocar main ni hacer merge.**

**PRIMERA ACCIÓN OBLIGATORIA:** leé completos en Git:
- `experimentos/balance_nuevo/handoffs/HANDOFF_PRE_A08_V20_2026-10-09.md`
- `experimentos/balance_nuevo/handoffs/BACKUP_REGISTRY_PRE_A08_V20_2026-10-09.json`
- `experimentos/balance_nuevo/pre_a08_equipo_v20/DICTAMEN_EQUIPO_V20_2026-10-09.md`
- `experimentos/balance_nuevo/pre_a08_equipo_v20/PATCH_CANDIDATO_SOBRETUNICA_V20.json`
- `experimentos/balance_nuevo/pre_a08_equipo_v20/QA_MANIFEST_V20_2026-10-09.json`
- `experimentos/balance_nuevo/pre_a08_equipo_v20/README_REPRODUCIR_V20.md`.
Verificá rama, HEAD, catálogo `arc1-equipment-v0.2` y hashes. Si adjunto `GRULLA_HANDOFF_ESENCIAL_V17_V20_2026-10-09.zip` o el respaldo de 33 ZIPs, utilizalos.

**ÚLTIMO PUNTO**: V20 terminó **284.160 combates válidos**: 161.280 screen de 14 kits, 61.440 DEF plana de Sobretúnica y dos cruces independientes de 30.720 cada uno. El número anterior 222.720 era solo parcial. Reproducción limpia de 55.680 filas exactas. Contra T2, M03 69,97 % WR jugador; M03 + Sobretúnica de patrulla DEF+2 da 89,87 %; EXPECTED_STAGE completo 96,85 %. Microtest con HP+2 constante: vestidura DEF+1 da 72,38 % frente a DEF+2 90,53 %. Si se modifica SOLO DEF2→DEF1 en el kit esperado, WR baja de 96,32 % a 88,37 %. **Candidato**: `sobretunica_patrulla` HP+2 sin cambios, DEF+2→+1, NO aprobado ni incorporado al HTML.

**CONTEXTO PREVIO**: V17 dejó línea base experimental fija para habilidades, cuatro nodos candidatos y Concordancias de LII (no canon); V18–V19 comprobaron los seis monstruos normales y dos candidatos: Cangrejo `DEFENSE_UP` T1 +3→+2, Jabalí `MITIGATE_NEXT` T1 40 %→35 %. Sin tocar los otros cuatro. Con Sobretúnica DEF+1 estos dos ajustes mantienen utilidad. LianQi I sin puntos, defensas ni AOE. LianQi II solo Tramo I/2 PT, técnicas BASE unitarget y defensivas, sin AOE. T0–T2 de monstruos no equivale al cultivo. No élites/T3/T4 aquí.

**MISIÓN AL RETOMAR:** no volver a empezar V05–V20. Continuar el balance de **equipamiento y economía**: catálogo `equipment_arc1_catalog.json` v0.2, 68 piezas (21 LII opcionales); verificar M04/M05/M06, permisos, obtención real, fuente de misión, NPC vendedores existentes y tiendas, piedras, precios de compra/venta, intercambio, drops distintos de extracción y suministros. **La Contribución NO es moneda gastable**, decisión humana vigente; hay diez piezas LII con precio antiguo en Contribución por corregir sin inventar canon. EXPECTED_STAGE (siete piezas) no está probado obtenible; no endurecer criaturas por ese kit.

Después realizar SOLO los cruces focales necesarios **V17 habilidades × V19 monstruos × V20 equipo accesible**, incluyendo Qi, aflicciones, consumibles y antídotos cuando estén soportados. Si millones de combates: prepararme Colab/Kaggle con barra, checkpoints y ZIP comprimido; si pequeño, ejecutalo localmente. Documentar **siempre** scripts, QA, hashes, informes y decisiones en Git experimental. Si se necesita una decisión humana, traer las alternativas para aprobación en lugar de inventar autoridad.

**META FINAL:** terminar habilidades, seis monstruos normales, equipamiento y economía antes de entregar a Astra el paquete de autoridad congelado para iniciar A08; Astra implementará/parificará luego el motor HTML. Respetar no main, no merge, no tocar ROOMS.exits, no inventar NPCs/misiones/vendedores. Distinguir entre RESULTADO DE LAB, CANDIDATO y CANON APROBADO.

Comenzá confirmando la lectura del handoff y auditando fuentes reales de adquisición de las 21 piezas LII. No repitas experimentos ya cerrados.
