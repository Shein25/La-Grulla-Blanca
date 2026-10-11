# V74 — Diagnóstico causal de Sentencia del Filo Celestial contra Sombra V72

**Fecha:** 10 de octubre de 2026. **Estado:** `DIAGNOSTIC_ONLY / NO_CHANGE_HUMAN_APPROVED_SOFT_M02 / EXPERIMENTAL_V67_BRIDGE_NOT_HTML`.
**Pregunta humana:** «¿Qué pasó con la Ulti de Metal? ¿Es por el último nerf que quedó tan debilitada?»

## Respuesta

**Sí, el nerf aprobado en V67 es una causa material de la escasa ventaja de Sentencia en Sombra V72, pero el contexto y uso importan.** La reducción era necesaria para no destruir al Rey Escarabajo con la variante original (100% WR jugador original frente a 78,89% con SOFT_M02); no es evidencia de que V67 fuera incorrecto globalmente. Sobre Sombra 110HP/DEF1, la utilidad de penetración es muy escasa y cuesta un turno completo más 16 Qi, con lanzamiento forzado en ronda 2. Un nerf simultáneo a apertura + bleed + remate debilitó la identidad de la Ulti contra este rival.

**Ficha aprobada de balance de diseño (no HTML):** `experimentos/balance_nuevo/handoffs/V67_CIERRE_GUARDIANES_ULTIS_2026-10-10/BALANCE_ULTIS_METAL_VIENTO_APROBADO_V67.json` = Sentencia SOFT_M02 (apertura ×0,5, penetración adicional +45pp, una hemorragia potencia1 ×2 acciones, cierre ×0,5, coste16 Qi). Previo V03: apertura ×1, penetración +90pp, 3 cargas de hemorragia potencia4 ×3 acciones, cierre ×1, coste16 Qi.

## Análisis exacto de los resultados V73 ya ejecutados

Se filtraron directamente los **13.824** combates Metal de `V73_SOMBRA_ULTIS_69120_COMBATES.csv`: **6.912 por brazo**, 2 semillas/cohortes ×3 builds LIII 4PT ×3 equipos (entrada LII DEF/EVA, y LIII opcional) ×3 políticas ×128 réplicas.

- Sin Ulti: **2.854/6.912 = 41,2905%**.
- Con Sentencia V67 SOFT_M02, siempre lanzada **en ronda 2**: **2.816/6.912 = 40,7407%**.
- Contrastes iniciales pareados: **1.023 derrotas convertidas en victorias** y **1.061 victorias convertidas en derrotas**. Delta neto −38/6.912 = **−0,5498 puntos porcentuales**, con **IC descriptivo pareado aproximado 95% [−1,84; +0,74] pp**. Esta diferencia no prueba que la Ulti empeore realmente el WR: evidencia que ese uso no muestra mejora clara.
- Ulti usada en **100%** de esos enfrentamientos (ronda 2), daño directo medio medido **17,375 HP**, Punto de Ruptura preparado en **3.796/6.912** y rematado en **3.795/6.912**, hemorragia media **1,538** en el puente. Sombra tiene **DEF1**, por lo que restaurar penetración sola apenas cambia nada.

## Contrafactuales con exactamente el mismo fixture V73/Sombra V72

**Laboratorio complementario nuevo:** se utilizó el mismo motor sellado E1/V66 + mismo puente E1/V67, Sombra V72 intacta (110 HP, DEF1, Velo CD4 ×2, Espejo absorción8); mismas dos cohortes, 6.912 duelos por variante, cinco valores de ablation one-factor-at-a-time, dos timings, original y control medio hipotético. Cifras de `Win Rate` del jugador Metal, **sin alterar especificaciones aprobadas ni juego**:

| Versión en laboratorio | WR Metal jugador | Diferencia vs SOFT_M02 temprano |
|---|---:|---:|
| Sin Ulti, resultado V73 | **41,29 %** | +0,55 pp |
| **SOFT_M02 V67 (ronda2), resultado V73** | **40,74 %** | referencia |
| SOFT_M02, uso retrasado a ronda4 | **43,72 %** | +2,98 pp |
| SOFT_M02, uso retrasado a ronda6 | **33,68 %** | −7,06 pp |
| Solo daño inicial ×0,5 → ×0,75 | **47,87 %** | +7,13 pp |
| Solo cierre ×0,5 → ×0,75 | **47,28 %** | +6,54 pp |
| Solo hemorragia potencia 1 → 2 | **46,37 %** | +5,63 pp |
| Solo hemorragias 1 → 2 cargas, potencia 1 | **46,37 %** | +5,63 pp |
| Solo penetración adicional +45 → +90 pp | **41,17 %** | +0,43 pp |
| **Hipótesis intermedia combinada**, apertura ×0,75, cierre ×0,75, potencia2, penetración45, 1 carga ×2 acciones, ronda2 | **56,09 %** | +15,35 pp |
| **Restaurar todos los números PRE-NERF V03, ronda2** | **99,90 %** | +59,16 pp |

El caso de 2 cargas ×1 y 1 carga ×2 coincide en esta configuración porque el mecanismo DOT produce la misma cantidad total de daño en el motor E1 bajo este fixture; eso **no equivale a validar equivalencia general de la Ulti**. Las comparaciones son análisis de sensibilidad, no propuestas aprobadas de otra Ulti; solo una de 25 Ultis Metal posibles fue evaluada y todos los porcentajes heredan limitaciones del puente E1/V03.1.

**Por equipo, SOFT_M02 V67 ronda2 vs sin Ulti:** máximo LII DEF 36,15 vs 40,41%; LII EVA 16,19 vs 19,57%; LIII opcional 69,88 vs 63,89%. Esto explica que el resultado promedio pueda ocultar una mejora tardía con equipamiento fuerte y perjuicios al inicio de etapa.

## Lectura de diseño y acción recomendada

1. **No reabrir automáticamente SOFT_M02**, ratificada por el autor en V67 para un equilibrio interjefes.
2. **No compensar aumentando penetración**, un nerf/buff prácticamente irrelevante ante DEF1 de Sombra.
3. El problema central es el **coste de oportunidad de una acción + 16 Qi** junto a la reducción simultánea de apertura, hemorragia y cierre; y el uso fijo temprano de V73.
4. Si se decide reabrir V67 en un nuevo frente, ensayar **un buff moderado de daño inicial o remate** (cada uno aislado), comparando obligatoriamente los cinco guardianes de AOE, Sombra, otros enemigos LIII, las cinco raíces y legalidad de la Ulti. **No restaurar los daños originales**: 99,90% contra Sombra implica rotura manifiesta en este puente.
5. Documentar que la diferencia **−0,55 pp** no es concluyente, y que la política de activación afecta fuertemente al resultado. **No nerfear a Sombra HP110** por esta sola observación.
6. No mezclar el equipo LIII opcional con el máximo LII de entrada; Ultis exigen maestría completa, una sola activación por combate, nada de injerto LIII.

**Guardas:** NO MAIN, NO MERGE, NO HTML, NO T0 ni Ultis aprobadas cambiadas, NO AOE multiblanco. Los datos proceden de escenarios 1v1 PRE_AOE y las versiones físicas del adaptador pueden diferir de NEW/HTML. El usuario debe autorizar cualquier nuevo ajuste numérico.
