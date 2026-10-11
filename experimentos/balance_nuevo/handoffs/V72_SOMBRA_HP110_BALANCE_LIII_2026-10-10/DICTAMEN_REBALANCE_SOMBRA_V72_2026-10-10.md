# V72 — Sombra Ahogada (élite único LianQi III): rebalance >100 HP

**Fecha:** 10/10/2026. **Autoridad:** orden humana explícita de rehacer Sombra con **más de 100 HP**.
**Estado:** `LAB_VALIDATED_SELECTED_DESIGN_CANDIDATE`, **NO HTML**, **NO MAIN**, **NO MERGE**, sin congelar automáticamente el registro numérico histórico.
**Registro máquina:** `SOMBRA_T0_V72_HP110_CANDIDATO.json`; ZIP portable del chat `GRULLA_V72_SOMBRA_AHOGADA_LIII_HP110_REBALANCE_2026-10-10.zip` (SHA256 `b529570daf30df03f24a4952de56993cbc48fc8f4da7704d73730aaa9ffcc830`).

## Motivo del cambio
La ficha histórica con **HP 51** dejaba a Sombra casi trivial en LIII. La propuesta V71 (90 HP, Espejo 16 y Velo de Ahogo cada 3 rondas con 3 pulsos) mejoró su dificultad, pero el autor indicó que **90 HP** seguía siendo poco para un **élite único de LianQi III** frente a repetibles de 84–90 HP.

## Nueva referencia de diseño V72 (seleccionada)
| Componente | V71 | V72 seleccionada |
|---|---:|---:|
| **HP** | 90 | **110** |
| DEF plana | 1 | 1 |
| Precisión, evasión, tenacidad | 106 / 20 / 19 | sin cambio |
| Básico | `1d2+7` | sin cambio |
| Velo de Ahogo: veneno | `1d2+2 ×3` | **`1d2+2 ×2 pulsos`** |
| Cadencia de Velo | 3 rondas | **4 rondas** |
| Espejo del Remanso | 16 absorción | **8 absorción** |
| Activador de Espejo | recibir ≥16 HP efectivos de un golpe | sin cambio, **una sola vez** |

**Espejo:** primero se resuelve el golpe; si quita **≥16 HP reales** al élite y éste sigue vivo, se activa reserva de **8 de absorción**. NO absorbe el impacto activador, NO aumenta DEF plana, NO cura, NO añade ronda extra. DOT atraviesa DEF pero respeta absorción.

La reducción de daño sostenido y absorción es **deliberada**, necesaria para compensar los 20 HP adicionales sin convertir a Metal, Agua y Tierra en raíces inviables. Se mantiene veneno como identidad central; el monstruo permanece **único T0**, sin T1–T4 ni Mutantes.

## Métodos y resultados comprobados
Se ejecutaron **228.960 duelos físicos completos** en el LAB E1/V61C:
- Primer barrido: **30.240** enfrentamientos con candidatos de 105, 110, 120, 130 HP y diferentes Espejos.
- Segundo barrido: **51.840** enfrentamientos cruzando HP, cadencia, pulsos de DOT, Espejo y daño base.
- Cinco lotes de holdouts/variantes: **146.880** combates completos.
- **Selección final:** dos cohortes con semillas independientes, **17.280 combates por cohorte**; **34.560 duelos** de la misma candidata V72 (no confundir los 228.960 de exploración con réplicas finales).

**Entorno:** cinco raíces; 3 builds legales de **4 PT** por raíz; dos equipos máximos LII que pueden conservarse al ascender; un equipo **LIII opcional/hipotético**, NO otorgado gratuitamente; tres políticas. **Sin Ultis, AOE, Concordancias ON, Mutantes, T1–T4 ni monstruos acompañantes.** Se conserva todo lo demás y no se inventan encuentros.

| Comparación | Victoria del jugador |
|---|---:|
| V71, 90HP + Espejo16 (17.280 de la nueva batería) | **58,36 %** |
| 110HP, sin Espejo, Velo CD4 ×2 (17.280) | **60,68 %** |
| 115HP, sin Espejo, Velo CD4 ×2 (17.280) | **51,09 %** |
| **V72 seleccionada 110HP + Espejo8 + Velo CD4 ×2 (34.560)** | **50,611 %** |

**Resultado final:** 17.491 victorias del jugador en 34.560 duelos; IC Wilson 95% descriptivo Monte Carlo [50,083%, 51,138%]; **0 timeouts**, **0 muertes del élite antes de ronda 4**, mediana no informada, duración media 11,43 rondas.

**Por raíz:** Fuego 62,645%; Agua 50,579%; Viento 56,207%; Tierra 43,200%; Metal 40,422%.

**Por equipo:** máximo LII defensivo 48,672%; máximo LII evasivo 32,300%; equipo LIII esperado opcional 70,859%. Ese 70,859% de equipo avanzado **no viola una regla de 70% universal de Sombra** —no se fijó tal hard cap— y no se usa para calibrar su dificultad de entrada. Cruces raíz×equipo pueden superar 70%.

**Por política:** solo ofensiva 47,457%; defensa inicial 50,434%; respuesta a intención 53,941%. La política táctica ayuda, pero no decide automáticamente la victoria.

## QA y límites
- **405 pares de regresión exacta** de wrapper inactivo vs E1 original, **0 diferencias** en el evento/estado/resultados observados.
- Hash del registro E1 original `c9a0f517ec8cab3136a7b8d2b6cf3a44c9bb47603c1ec0455853f72e6f6118fd`; fuente física V66 ZIP `e8402ca195ba9f2d4fe97ae4a71351d25f691c7601a81c49693cdf77198d3a39`.
- ZIP portable de V72: **28 archivos**, 2.563.414 bytes, CRC y manifiesto SHA256 PASS. Contiene script de restauración V66, source lock, ejecutores, CSV físicos individuales, QA y configuraciones. ZIP adjunto al chat, **no subido a Git**.
- **No paridad end-to-end NEW/HTML:** quedan pendientes telegráfico de Espejo en el registro auténtico, impacto resuelto/dot, persistencia de único y SAVE/LOAD.
- Interacciones de Ultis adquiridas en LIII, Concordancias ON y AOE multiblanco deberán evaluarse después, sin extrapolar estos porcentajes PRE_AOE.

**Decisión documental:** V72 prevalece sobre el **candidato V71 de 90 HP** como nueva ficha **seleccionada** en experimentación, respetando la orden de más de 100 HP. No reescribir el antiguo T0 ratificado de 51 HP ni declarar integración HTML sin gate explícito. **No tocar main, no merge, ROOMS.exits, NPC, misiones, gates, spawns, tiendas o economía.**
