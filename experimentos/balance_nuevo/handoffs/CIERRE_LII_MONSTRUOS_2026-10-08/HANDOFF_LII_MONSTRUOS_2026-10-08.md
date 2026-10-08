# HANDOFF — cierre de conversación LI/LII, Concordancias y balance de monstruos
Fecha: 2026-10-08. Repositorio: Shein25/La-Grulla-Blanca.
Rama de respaldo: `handoff/lii-monsters-close-2026-10-08` (derivada de `experiment/monster-adaptive-six-revalidation-v0.1`).
**ESTADO: HANDOFF / LABORATORIO. NO FREEZE NUEVO. NO MERGE. NO MAIN.**

## DECISIÓN HUMANA PRIORITARIA — corregir el alcance
La etapa de combate de los dos guardianes de manuales AOE es **LianQi III**, aunque el registro numérico histórico contiene `native_stage: LianQi_II`.
- `sapo_caldera` — **Sapo Caldera de Tres Gargantas**: guardián único del manual **Círculo de las Cien Ascuas** (AOE de Fuego), enfrentamiento y desbloqueo desde **LianQi III**.
- `rey_escarabajo` — **Rey Escarabajo de la Veta Negra**: guardián único del manual **Lluvia de Filos** (AOE de Metal), enfrentamiento y desbloqueo desde **LianQi III**.
- No reaparecen al morir. **Excluir adaptaciones T1–T4 y Mutantes**. Cuando se balanceen en el frente LIII, jugador **todavía sin su AOE**; con Ulti principal según decisión de progresión, a contrastar con autoridad de desbloqueo.
- Esta autoridad proviene de la decisión humana del 2026-10-04, documentada en `HANDOFF_LA_GRULLA_TECNICAS_HEAVY_2026-10-04.md`. **NO** reinterpretar a partir del campo `native_stage`. Antes de un parche de gating, localizar la ruta real de ese documento y la progresión efectiva.

## ALCANCE EXCLUSIVO DE LianQi II
| ID | Nombre | Rol | Estado |
|---|---|---|---|
| `sapo_ceniza` | Sapo de Ceniza | NORMAL | perfil READY; T0 y T1/T2 ratificados según cierre de autoridad anterior |
| `escarabajo_hierro` | Escarabajo de Hierro | TANK | perfil READY; T0 y T1/T2 ratificados según cierre de autoridad anterior |
| `eco_caido` | Eco del Caído | ELITE | `PENDING_INTEGRAL_REBALANCE`; solo candidatos T0 experimentales, **sin cifras aprobadas** |

No inventar adversarios nuevos. No devolver los guardianes AOE a esta etapa.

## TRABAJO Y PRUEBAS QUE SÍ EXISTEN
1. Resolver de Concordancias V03: 46/46 pruebas y 11.200 combates reales LI+LII en entorno de pruebas. Núcleo de Magma corregido para detonar el pendiente antes de crear otro. No autoriza freeze de escalas.
2. `GRULLA_BALANCE_MONSTRUOS_LI_LII_V01`: 55.680 combates LI+LII; dictamen **PILOTO EXITOSO / NO FREEZE**. Incluye 13.440 solo técnica principal y 42.240 experimentales. T1/T2 del puente V06 requiere paridad evento-a-evento con la IA adaptativa congelada.
3. Hallazgos piloto con técnica principal, T0 y equipo de entrada: Sapo de Ceniza WR jugador 83,13 %, Escarabajo 57,34 %. Con equipo `EXPECTED_STAGE` suben a 98,44 % y 97,03 %, pero permisos y adquisición no acreditados: **no adaptar enemigos a ese escenario artificial**.
4. `GRULLA_LII_PENDIENTES_T0_V01` fue un laboratorio provisional con T0, técnicas principales, clones READY sólo en memoria y 5 raíces. `eco_caido` E8 (HP 84, PREC 96, EVA 18, DEF 1, TEN 18, básico 1d2+4) es **candidato exploratorio**, NO decisión. Ver `FINAL_VERIFY/eco_caido_5000_5255.csv`, 7.680 peleas, 256 semillas por raíz/equipo/política. Con MANDATORY_ENTRY: WR jugador 58,44 % UNITARGET_FIRST vs 70 % DEFENSE_OPEN, ambos **fixtures** sin paridad completa de técnicas/equipo legal.
5. Las corridas de `sapo_caldera` y `rey_escarabajo` de este laboratorio son **CUARENTENA HISTÓRICA**: sólo para trazabilidad de un error de alcance, no para balancear LII, no para ratificar guardianes LIII. No reciclar S*, R* ni propuestas de HP/DEF/daño/cadencia.

## CÓMO SE PRODUJO EL ERROR
Se eligió por `native_stage: LianQi_II` del registro antiguo, sin comprobar la decisión de progresión del 4 de octubre. A partir de ese filtro inválido se lanzaron simulaciones para los dos guardianes. El usuario detectó el conflicto y corrigió el alcance. La decisión del usuario tiene precedencia.

## ESTADO ACTUAL, BLOQUEOS Y PRÓXIMA ACCIÓN
- Objetivo del siguiente chat: **balance integral y definitivo de Eco del Caído T0**. Mantener Sapo de Ceniza y Escarabajo de Hierro como autoridades; después validar los tres en cinco raíces, equipamiento que de verdad se consigue en LII, defensa de LII, Concordancias, Qi, alquimia y acceso de progresión.
- Primero inspeccionar contrato de elite, drops, misiones, etapa y disponibilidad efectiva. No otorgar AOE LIII ni ultis por conveniencia de laboratorio.
- Para Eco: comparación controlada de E8 y alternativas, semillas adicionales independientes, análisis por raíz, muerte/turnos/HP final/coste Qi con `MANDATORY_ENTRY` y **equipos verdaderamente accesibles**. No aprobar E8 sin criterio de dificultad humano explícito.
- Paridad T1/T2: usar runner oficial congelado, no aceptar el puente V06 sin diff de eventos.
- NO cambiar `main`, no merge, no editar `ROOMS.exits`, técnicas ni equipamiento productivos, bosses, quests, gates ni perfiles originales. No declarar `READY` en archivos fuente mientras no haya ratificación.
- Fuentes fijas del motor para reproducir: commit `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`, bajo `experimentos/balance_nuevo/`.
- Cinco blobs Git: motor `131519da43adabff2e1ba8b4ce711889f3563f86`, guard `0dd32a940ff1ba18501f957a95ae4b8cd115b4b9`, técnicas `073ed88fdb9d00795a10972a4a850b22505b6d48`, monstruos `c0d2131f2cc8dbbb96babf9711c197e54fe97591`, equipo `3ac868a399118845b91da6ccd884633e7ac2b496`.

## BACKUP LOCAL ASOCIADO
El archivo ZIP del cierre incluye un índice SHA-256, este handoff, prompt de continuación, código/laboratorio, CSV de campañas, auditorías previas y paquetes V01/V03. **El backup completo y los registros masivos se entregan como adjunto de este chat; no asumir que esos binarios quedaron publicados en Git.** Este commit documenta el estado y las decisiones, no equivale a aplicar cambios de gameplay.
