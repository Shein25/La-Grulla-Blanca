# PRE-A08 V36 — Corrección focal de habilidades de Viento (LianQi II)

**Fecha:** 2026-10-09. **Estado:** LAB PASS / DOS BUFFS T1 CANDIDATOS / NO CANON / NO HTML / NO MAIN / SIX NORMALS REMAIN CLOSED.

## Corrección de alcance y auditoría

El usuario solicitó ajustar las **habilidades de la raíz Viento**, NO alterar nuevamente los seis monstruos normales LianQi II cerrados en V35. La Sobretúnica permanece **DEF+2 / HP+2** y no se estudian precios ni comercio.

**Hallazgo del runner V35:** su selector marcaba `tech.ACTIVE='SKILLS_V17'`, pero `f.ref.make_state` apuntaba efectivamente a `bridge_reference.make_state`. En builds con `lanza_t1_direct`, `lanza_nubes.direct_pct` compilaba **20**, aunque el candidato V17 establecía **30**. La discrepancia afecta al **laboratorio V35**, y NO implica que exista ese bug en el HTML. V36 reintrodujo explícitamente V17 mediante adaptador en memoria, restringido a LianQi II, sin tocar fuentes.

## Comparaciones realizadas

Seis monstruos normales con valores **V33 moderados y cerrados**, raíz Viento, 16 builds × T1/T2 adaptativos × dos políticas × cuatro cargas de equipo (M03 uniforme, Sobretúnica M04, M05 pesada, M05 ligera). Semillas pareadas entre brazos, monstruos y equipo no alterados, una BASE Concordancia escalar con fuente Fuego supuesta para laboratorio (aprendizaje real no validado).

- **V36:** seis brazos, incluyendo V35 legado, V17 restaurado, daño base +1 indiscriminado de Lanza (hipótesis **descartada**), +5 crítico de Precisión, +5 Evasión de Paso y +5 crítico de respuesta. DISCOVERY 18.432 + HOLDOUT 18.432; COLD exacto 9.216.
- **V36B:** V17 restaurado y comparaciones focales Precisión Lanza T1 +1 al dado, Evasión Paso T1 +5, Respuesta Paso T1 +15 crítico, Respuesta Paso -1 Qi, y combinación. 36.864 peleas; COLD 9.216.
- **V36C:** validación de **combinación mínima** (Precisión daño +1 y Evasión +5), frente a V17 reparado y combinación ampliada con crítico de respuesta. 18.432 ejecuciones, pero 12.288 repiten exactamente brazos de V36B y se descontaron de combates únicos. COLD 4.608.
- **TOTAL**: **92.160 ejecuciones no-COLD, 79.872 casos nuevos únicos, 12.288 reproducciones deliberadas**; 23.040 filas COLD reproducidas. **0 timeouts / 0 acciones debidas omitidas**. No se alteraron estadísticas de las criaturas, equipo ni datos productivos.

## Resultado T2 de la combinación mínima V36C

Cada celda tiene **768 peleas**, dos cohortes, cuatro semillas distintas.

| Equipo | V17 correctamente aplicado | V36 candidato mínimo | Cambio en victorias | Con crítico RESPONSE extra, descartado |
|---|---:|---:|---:|---:|
| Uniforme inicial | 52,86 % | **56,64 %** | **+3,78 pp** | 57,16 % |
| Sobretúnica original DEF2 | 80,86 % | **82,94 %** | **+2,08 pp** | 83,20 % |
| M05 pesada (hipotética) | 94,01 % | **95,44 %** | **+1,43 pp** | 95,70 % |
| M05 ligera (hipotética) | 78,39 % | **80,34 %** | **+1,95 pp** | 80,60 % |

T1 con uniforme: 55,86 % → **59,90 %** (+4,04 pp). En T2 uniforme hubo **34 victorias nuevas y 5 pérdidas** en contextos apareados al comparar candidata mínima vs V17 restaurado. Mejoran especialmente las especializaciones débiles; las no seleccionadas son control negativo exacto.

## Recomendación focal (NO autoriza implementación automática)

1. **V17 YA EXISTENTE:** asegurar que la especialización `lanza_t1_direct` de `lanza_nubes` use **30 % DIRECT** en LianQi II, en lugar de 20 % del runner V35. No confundir con fallo confirmado de runtime.
2. **CANDIDATO NUEVO — `lanza_t1_prec` PRECISION:** si el jugador escoge este nodo T1, daño base de Lanza **`2d4+3 → 2d4+4`**; sin cambio al daño de la técnica en builds que no lo seleccionan, ni en LI.
3. **CANDIDATO NUEVO — `paso_t1_eva` EVASION:** si el jugador escoge este nodo T1, evasión concedida **40 → 45**, con duración y coste de Qi intactos. Paso sin ese nodo continúa con base **35**.

**No promover:** aumento de +1 al daño base de *todas* las builds de Lanza: mejoró demasiado T2/uniforme en V36 (55,34 → 66,41 %) frente a la línea V17 en esa cohorte. Respuesta crítica adicional T1 +15 pp aportó solo +0,26 a +0,52 pp T2 encima de la combinación mínima; no compensa complejidad. Coste -1 Qi para Paso RESPONSE y +5 crítico en Lanza PRECISION resultaron sin ganancias importantes.

## Límites y handoff

Este es un estudio experimental 2 PT de habilidades T1 LianQi II, con una Concordancia BASE representativa; sin Tijera AOE, 20 relaciones completas, efectos V26, élites, jefes, T3/T4, acceso real a técnicas ajenas ni paridad A08. Por ello los dos buffs quedan **PENDIENTES DE RATIFICACIÓN HUMANA**, sin editar el catálogo canónico. Los seis monstruos normales V35 siguen cerrados; no reabrirlos por error del runner. **Siguiente frente: Eco del Caído**, recuperando descriptor E8 y paridad antes de repetir peleas.

ZIP portable en conversación: `GRULLA_PRE_A08_V36_AJUSTE_HABILIDADES_VIENTO_2026-10-09.zip` (SHA256 `71389d6803c7081cc61568cd2804089cca1ed0dd9811819a854b2d70699c9bb9`), **104 archivos**. CRC y manifiesto SHA256 PASS, COLD desde carpeta limpia PASS. Incluye código, CSV bruto, auditoría completa, QA y dependencias V17/V35.

**Guardias:** no main, merge, HTML, ROOMS.exits, A07, cambios de estadísticas de los monstruos o Sobretúnica, precios ni comercio.
