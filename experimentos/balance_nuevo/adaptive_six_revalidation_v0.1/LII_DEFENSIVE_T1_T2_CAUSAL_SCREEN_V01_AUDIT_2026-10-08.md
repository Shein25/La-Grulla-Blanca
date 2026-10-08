# LianQi II — Defensa T1/T2, auditoría causal R32

Fecha de auditoría: 2026-10-08.
Estado: **PASS_SCREEN_ONLY / FOCUS_R256_REQUIRED / NO_FREEZE**

## Evidencia y controles
- Zip: `LII_DEFENSIVE_T1_T2_CAUSAL_SCREEN_V01_REVIEW.zip`
- SHA-256: `b19cb08668dd4efb08a3bfbbb8d074b8c8ba36496407cc97cf195bef864e1e31`
- Source commit: `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`.
- Runner SHA-256: `fc14ff185419d694160121ad9684539bfd324ea171fda8fe8ef8261566510fa9`
- Manifiesto 12/12, ZIP CRC PASS; 163.840 filas de combates sin duplicados, nulos ni no finitos.
- Matriz 80 builds monorraíz, cuatro gears, dos especies nativas READY, tiers T1/T2, cuatro políticas, R32.
- 10/10 pruebas de eventos; 0 AOE, 0 `canonical_due_missed`, 0 timeout.
- 3.840 contrastes de política; 4.800 contrastes de Tramo I; 542 alertas heurísticas correlacionadas por semillas/builds, NO 542 bugs.

## Política: resultados descriptivos
Victorias: `OFFENSE_ONLY` 74,34%; `DEFENSE_OPEN` 76,49%; `DEFENSE_DUE` 78,74%; `DEFENSE_GUARD` 79,73%. `DEFENSE_GUARD` gasta 45,30 Qi promedio vs 41,45 ofensiva y prolonga combates (11,35 vs 9,01 rondas).

Deltas de victoria vs OFFENSE_ONLY (pp):
- Agua: OPEN +1,51 / DUE +1,44 / GUARD +5,98.
- Fuego: OPEN −3,43 / DUE +0,65 / GUARD +1,09.
- Metal: OPEN +3,78 / DUE +7,18 / GUARD +7,48.
- Tierra: OPEN +6,77 / DUE +3,60 / GUARD +3,88.
- Viento: OPEN +2,14 / DUE +9,17 / GUARD +8,53.

En Fuego T2: OPEN −5,69; DUE −1,78; GUARD +0,32 pp. Estos son efectos netos de estrategias que consumen turnos y Qi; no un juicio sobre la potencia intrínseca del escudo.

## Tramo I — investigación prioritaria
- Agua, `espejo_luna` EFICIENCIA T1: ninguna diferencia observable en los resultados de esta matriz. Hipótesis verificable: redondeo de coste 7×0,75→5 y (7−1)×0,75→5. Antes de concluir se requiere preflight explícito del compilador y analizar el punto de progresión sin inventar un cambio.
- Metal ADAPTATION T1 y Tierra STABILITY T1 no influyen en los dos monstruos actuales sin control: limitación de enemigos, NO declaración de skill inútil global.
- Fuego ofensiva `palma_ardiente` DIRECT T1: +25,93 pp de victoria vs base promediando políticas/estratos; investigar umbrales de daño, kill timing y especialización versus defensa.
- Viento DEF_T1 EVA añade valor a estrategias DUE/GUARD; no requiere buff preventivo.
- Tierra DEF_T1 FORTIFICATION: algunas señales negativas leves; investigar sin reabrir contrato.
- Foco R32 muy negativo: Fuego BASE, MANDATORY_ENTRY, Sapo T2, DEFENSE_OPEN −34,375 pp (CI normal aproximado sup. −13,53). Tierra OFF_1_DEF_0, MANDATORY_ENTRY, Sapo T2, DEFENSE_GUARD −34,375 pp.

## Advertencias estadísticas y de alcance
Las 542 alertas contienen dependencias por semillas compartidas y builds derivadas. Los intervalos R32 son exploratorios, y las mismas semillas acoplan los brazos, pero acciones diferentes pueden desincronizar el stream RNG. No asumir independencia de todas las filas. Igual ponderación por equipos no representa distribución del juego.

Excluidos: mutantes, variación individual/sufijos, builds multielementales, Concordancias LII, equipo por adquisición efectiva.

## Decisión
**PASS_SCREEN_ONLY, no freeze, no mutación canónica**. Ejecutar `LII_DEFENSIVE_T1_T2_FOCAL_R256_V02` con semillas nuevas y enfoque jerárquico. Luego verificar mutantes por contrato, multielemento y Concordancias. Sólo laboratorio, no main, no merge/push ni HTML. Astra recibe handoff tras cierre.