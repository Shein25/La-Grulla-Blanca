# PRE-A08 V30 — Veneno reduce 10% la recuperación de Qi fuera de combate

**Fecha:** 2026-10-09. **Estado:** MECÁNICA ELEGIDA POR USUARIO; PROTOTIPO LAB PASS; **NO INTEGRADO EN HTML / NO FREEZE A08**.

## Decisión de diseño

El veneno activo perjudica la recuperación de Qi **fuera del combate** un **10%** para diferenciarse de la quemadura. La quemadura no impone esta penalización. Los demás efectos DOT, daño, DEF, absorción, curas, Qi máximo y economía permanecen sin cambios. No se introduce regeneración pasiva por turno.

**Semántica de la propuesta técnica:** chequeo de `player.aflicciones` con `tipo === 'veneno'` y `duracion > 0` al **comenzar la acción**; es un único modificador sin acumulación por múltiples venenos. Aplica a meditar, meditar profundo, dormir y consumibles con recuperación de Qi cuando se usan fuera de combate. No aplica a recompensas de misiones, botín de batalla ni devoluciones en combate. Calculamos primero la recuperación bruta con modificadores ya existentes, después `ROUND_HALF_UP(bruto * 0.90)` una sola vez, **antes** del cap por `qi_max`. El personaje envenenado al iniciar una meditación recibe menos Qi aunque el mismo pulso extinga el veneno. Si se trata antes, recupera lo normal. Familias y grados de veneno comparten el mismo 10%; la compatibilidad de los antídotos no cambia.

**Ejemplos:** 20→18, 15→14, 22→20, 10→9; 5→5 por redondeo discreto, sin ledger fraccional oculto. Estos detalles de mapeo y redondeo son una propuesta de implementación probada; lo expresamente elegido por el usuario es la reducción del 10% extracomabte.

## Implementación aislada y QA

- Código JavaScript listo para integrar en una etapa posterior: `POISON_QI10_ADAPTER_CANDIDATE_V30.js`. El blob comprometido coincide **exactamente** con el archivo sometido a pruebas locales (Git blob `1b2a26ec240f33b8501fce42e4d73256114479ea`).
- `test_v30_js.cjs`: regresión Node; valor de Qi, quemadura, múltiples venenos, compatibilidad, recompensa, combate, cap, persistencia temporal de snapshot, 501 valores y 15.000 escenarios aleatorios.
- En el ZIP externo: `qi_poison_modifier_v30.py`, `test_v30_qi.py`, `run_v30_qi_balance.py`, `analyze_v30.py`, RAW gzip, tablas pareadas, QA y dependencias V21–V29. Suite Python: 26 checks, 15.000 límites aleatorios; suite Node: PASS.
- Fuente histórica ver74 para locators `cmd_meditar`, `cmd_dormir`, `beber`, `aplicarAfliccion`, `avanzarAflicciones`, `tratarAfliccion` (Git blob `d34f7ea3f9de9344130aa072fac34d14a7a474d6`). **No adaptar automáticamente sistemas legacy** a `NEW_COMBAT_STATS_V0_1`; Astra debe resolver los bindings productivos reales después del balance.

## Batería de combate V30 (LAB)

**Fixture de recuperación 20 Qi** para exponer una diferencia de 2 Qi. Este valor **no ratifica una medicina de 20 Qi**. Primer duelo: Serpiente de Qi o Avispa de Jade (veneno), o Sapo de Ceniza (quemadura control). El veneno por golpe básico Serpiente/Avispa aún depende de la interpretación diagnóstica `VER74_BASIC_DIRECT` de V29 y **no está ratificada en el registro de monstruos**. Después: recuperar Qi, caminar un pulso, enfrentar uno de seis monstruos normales T1/T2 con cinco raíces, dos builds por raíz, dos estilos y dos equipos de referencia (M03 y Sobretúnica DEF1 candidata).

| Indicador | Resultado |
|---|---:|
| DISCOVERY | 5.880 combates |
| HOLDOUT | 5.904 combates |
| **Combates nuevos** | **11.784** |
| Contextos pareados / filas de brazos | **5.760 / 11.520** |
| Contextos con veneno al iniciar la recuperación | **1.392** |
| Contextos con quemadura, sin veneno | **972** |
| Qi efectivamente menos disponible con veneno | **1,966 de media** |
| Contextos donde cambió el vencedor | **18 (10 perjuicio, 8 beneficio situacional por secuencia de acciones)** |
| Victoria con veneno, regla OFF → ON | **12,50% → 12,36%** |
| Cambios de resultado SIN veneno / con solo quemadura | **0 / 0** |
| Timeouts y acciones de monstruos omitidas | **0 / 0** |
| Reproducción COLD | **2.880 filas × 37 columnas exactas** |

No interpretar los porcentajes absolutos como balance final del Arco 1: el protagonista sigue con los recursos reales restantes del primer encuentro y el estudio comprueba la diferencia incremental de 2 Qi. Es una penalización de **recuperación**, no de recursos existentes ni de costes de técnica. No hay evidencia en V30 para modificar daño del veneno o potencia de medicamentos.

## Estado de integración, próximos pasos y límites

La **regla numérica fue aceptada por el usuario** y quedó registrada con código y regresiones, pero **NO se aplicó al HTML**, a ningún catálogo canónico ni a la economía. La integración debe verificar fuentes reales de recuperación y momento del tick, persistencia/guardado y UI, preservar las 84 entradas A07, y evitar lógica económica legacy. El equipo de comercio sigue esperando B01 y el cierre general de balance.

No main. No merge. No cambios a `ROOMS.exits`, ver76, A07, NPCs, monstruos, precios ni comercio.

**ZIP reproducible:** `GRULLA_PRE_A08_V30_VENENO_RECUPERACION_QI_10PORCIENTO_2026-10-09.zip`. SHA-256: `cdcc3af2845265d18f56a098e22dc1a365f98481db269a0312f9803097826dc8`; **91 archivos**, CRC/manifiesto PASS; pruebas Python, Node, ejecución COLD y análisis PASS desde carpeta limpia. El ZIP se entrega en conversación y no fue subido a GitHub.
