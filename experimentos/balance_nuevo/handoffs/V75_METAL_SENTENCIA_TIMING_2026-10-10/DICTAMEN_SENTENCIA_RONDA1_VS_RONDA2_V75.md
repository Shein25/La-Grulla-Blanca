# V75 — ¿Metal debe abrir con Sentencia? Prueba ronda 1 contra Sombra 110 HP

**Fecha:** 2026-10-10. **Estado:** diagnóstico físico E1/V67/V73, no reabre balance ratificado ni modifica runtime.

**Respuesta:** no. La Ulti V67 SOFT_M02 puede pagarse **en primera ronda** (coste 16 Qi; equipamiento de ensayo parte de 53–55 Qi), pero no mejora la tasa de victoria frente al lanzamiento en ronda 2 ni frente a no usarla. Se ejecutaron **27.648 peleas físicas nuevas** (cuatro estrategias 6.912 cada una) con las mismas cohortes de semillas y la misma Sombra V72: HP110, DEF1, absorción8 y veneno cada cuatro rondas. Se mantuvieron 3 builds legales de LIII con 4 PT, 3 políticas y 3 equipos: dos máximos LII de entrada y LIII esperado solo opcional. No Ultis de injerto, AOE ni buffs nuevos.

| Estrategia | Victorias jugador Metal |
|---|---:|
| Sin usar Ulti (referencia V73) | **41,2905%** |
| **Ulti primera ronda** | **39,8293%** |
| Ulti segunda ronda | **40,7407%** |
| Ulti tercera ronda | **40,0463%** |
| **Ulti cuarta ronda** | **43,7211%** |

R1 vs R2 (pares mismos contextos/semillas) es **−0,9115 pp**, con intervalo de Monte Carlo descriptivo aproximado **[−2,2691; +0,4462] pp**: diferencia de R1 y R2 no concluyente. R1 vs no Ulti es **−1,4612 pp** [−2,7935; −0,1289] en este fixture; no extrapolar a todo el juego. R4 vs R2 es +2,9803 pp [1,6717; 4,289]. Una Ulti como máximo por combate; usada en 100% en estos escenarios y cero timeouts.

**Por equipo (R1 / R2 / R4):** LII máximo DEF: **35,89 / 36,16 / 39,63%**; LII máximo EVA: **18,19 / 16,19 / 20,05%**; LIII opcional: **65,41 / 69,88 / 71,48%**. No regalar equipo LIII al ascender.

**Por qué:** Sentencia SOFT_M02 exige sacrificar una acción +16 Qi; apertura y cierre están multiplicados por ×0,5, hemorragia se redujo a 1 carga potencia1 ×2 turnos. En Sombra DEF1, penetración adicional de 45pp apenas ofrece valor; reponer penetración90 sin revertir otros nerfs tampoco mejora de modo relevante (V74). La hemorragia y Punto de Ruptura aún se ejecutan: uso en R1 preparó cierre en 59,14% de peleas y en R2 en 54,91%, sin mejorar el resultado final por oportunidad perdida. Una Ulti original V03.1 pre-nerf garantizaba ~99,90% de victorias (V74), por lo que el nerf global fue necesario.

**QA:** ronda 2 replicó **6.912/6.912 filas V73** exactamente (victoria, rondas, HP, Qi, ronda de activación), con **0 diferencias**; 27.648 duelos nuevos, cero timeouts. No aporta equivalencia al HTML: uso E1 con adaptador experimental de Ultis V03.1/V67. El cambio es únicamente `rn>=2` → `rn>=1/3/4` como puerta de oportunidad, sin tocar mecánicas aprobadas.

**ZIP portable:** `GRULLA_V75_METAL_SENTENCIA_RONDA1_VS_RONDA2_2026-10-10.zip`, SHA-256 `6258e5129698d4d591b68d2395eb9fc93a3b4ee067db9632ca8bb65131469cfa`; contiene fuente del experimento, 27.648 filas CSV, resumen JSON, manifiesto y dictamen, CRC/SHA256 PASS. Requiere el ZIP fuente V73 para reproducir los módulos sellados, disponible en esta conversación. ZIP no subido al GitHub.

**Decisión:** no cambiar la Ulti SOFT_M02 aprobada ni Sombra V72 por esta prueba. Si el autor abre un nuevo balance de Sentencia, comparar ajustes puntuales de **apertura o remate**, no penetración, contra Sombra, Rey Escarabajo y guardianes donde aplique. **NO main; no merge; no HTML, ROOMS.exits, spawns, Ultis o T0 canónicos modificados.**
