# V73 — Sombra Ahogada 110 HP con Ultis de la raíz principal

**Corte:** 2026-10-10. **Estado:** `PHYSICAL_LAB_PASS / ULTIMATES_BRIDGE_EXPERIMENTAL / NO_RUNTIME_PARITY / NO_T0_CHANGES`.

## Parámetros de Sombra: EXACTAMENTE V72

T0 de diseño `sombra_ahogada`: **110 HP**, DEF 1, Precisión 106, Evasión 20, Tenacidad 19, básico 1d2+7; Velo de Ahogo cada **4 rondas**, veneno `1d2+2 ×2 pulsos`; Espejo del Remanso **8 absorción** después del primer impacto que quite al menos 16 HP reales, máximo una activación. **Ningún parámetro se modificó** para estas simulaciones.

## Resultados E1: 69.120 duelos físicos

34.560 encuentros SIN Ulti y 34.560 con **una** Ulti de raíz principal candidata; 2 lotes de semillas ×5 raíces ×3 builds legales LIII de **4 PT** ×3 equipamientos ×3 políticas ×128 réplicas. Equipo máximo LII al entrar o equipo LIII opcional (no regalado), nunca equipamiento LIV. Sin AOE, injerto o Concordancias extranjeras.

| Raíz | Ulti V67 candidata | Victoria jugador sin Ulti | Con Ulti | Diferencia |
|---|---|---:|---:|---:|
| Fuego | Renacer del Sol Carmesí | 62,53% | **66,78%** | +4,25 pp |
| Agua | Océano Invertido | 50,85% | **80,32%** | +29,47 pp |
| Viento | Vendaval de Mil Heridas **SOFT_W01** | 56,02% | **74,78%** | +18,76 pp |
| Tierra | Sepulcro de las Diez Mil Montañas | 43,01% | **82,74%** | +39,73 pp |
| Metal | Sentencia del Filo Celestial **SOFT_M02** | 41,29% | **40,74%** | −0,55 pp |
| **Global, raíces igualmente ponderadas** | | **50,74%** | **69,07%** | **+18,33 pp** |

| Equipo | Sin Ulti | Con Ulti |
|---|---:|---:|
| Máximo LII defensivo | 49,13% | **67,28%** |
| Máximo LII evasivo | 32,90% | **54,08%** |
| Conjunto LIII esperado **opcional** | 70,19% | **85,86%** |

## Configuraciones legales y sensibilidad

**Gate V67:** LianQi I–II sin Ultis; LIII solo **una Ulti de la raíz principal** con rama dominada; LIV hasta dos conocidas (raíz + injerto), pero **solo una activación exitosa por combate**. El dominio de rama es precondición del fixture y NO se deduce automáticamente de la build de 4 PT. En el laboratorio se elige 1 candidata de las **25 Ultis**, no se testearon las 25 ni los injertos.

**Fuego — Renacer:** las pruebas mostraron que lanzarla tan pronto como hay Qi desde ronda 2 disminuye WR del jugador hasta **46,77%**, frente a **62,53%** sin Ulti. La variante táctica que espera hasta **HP ≤30%** produjo **66,78%** y solo se activó en **22,76%** de encuentros; es una política de estudio, no IA humana ya implementada.

**Metal — Sentencia SOFT_M02:** penetración adicional +45, directo apertura ×0,5, un stack de Hemorragia potencia1 por 2 acciones voluntarias y cierre ×0,5. **Viento — Vendaval SOFT_W01:** directo de dos cortes ×0,45 y un stack de Hemorragia potencia2 por cada impacto. Son los **candidatos moderados V67**, NO las variantes rotas originales.

**Agua — Océano:** `CONTROL_BASE=80` procede de un **fixture sin ratificar de V67**, por lo que no debe interpretarse como tasa de victoria productiva. **Tierra — Sepulcro:** la enorme mejora sigue requiriendo paridad de efectos y duración contra V03.1/NEW.

Metal con Sentencia moderada puede jugar peor que sin gastarla: no nerfearla automáticamente ni forzar su uso. Elegir otras Ultis de las mismas familias podría cambiar las conclusiones; eso no se ha ensayado aquí.

## Verificaciones

- **0 timeouts**, 69.120 filas completas.
- **810/810 pares de regresión del brazo sin Ulti** frente al motor E1 original, 0 diferencias.
- El segundo lote S2 reprodujo **exactamente 17.280 peleas del ZIP V72** en victoria, ronda, HP final y Qi final, **0 diferencias**. El primer lote es una cohorte independiente nueva, no una copia exacta del HOLDOUT_A de V72.
- Ninguna pelea tuvo más de 1 activación de Ulti; Fuego la reserva según condición.
- La semilla inicial es pareja, pero introducir eventos cambia la extracción posterior de RNG; estas cifras no certifican flujos aleatorios pareados evento por evento.
- Fuente: ZIP portable `GRULLA_V73_SOMBRA_110HP_CON_ULTIS_2026-10-10.zip` SHA256 `615db972e5006c571ec60c703025d8c06a24ec17b54c380d71d7be282c2964aa`, **95 entradas**, CRC/manifiesto SHA256 PASS; incluye CSV, ejecutor, V66 y V03.1. Adjunto al chat, **no subido a Git**.

## Dictamen

**Con las Ultis elegidas, Sombra V72 mantiene dificultad razonable para un jugador que acaba de ingresar a LIII con equipo máximo LII, pero puede volverse fácil para Agua/Tierra y con equipo LIII opcional (85,86% global).** No aumentar HP/DEF de Sombra todavía: la autoridad definitiva del control Agua, el puente de Ultis y el momento real de adquisición/uso siguen pendientes. Este experimento documenta sensibilidad, no aprueba un nuevo T0 ni completa el frente de AOE multiblanco.

**Guardias:** no `main`, no merge, no HTML, no `ROOMS.exits`, no spawns/gates/quests, no T0 ajenos, sin AOE. Mantener Sombra en **110 HP** y Eco en **84 HP** como decisiones de diseño.
