# PRE-A08 V38 — Rebalance de Lanza que Parte Nubes
**9 de octubre de 2026 · LAB PASS / ENMIENDA NUMÉRICA CANDIDATA / NO APLICADA / PENDIENTE RATIFICACIÓN HUMANA.**

## Alcance
El usuario aclaró que la preocupación no era crear una técnica llamada "Viento Cortante", ni balancear otra vez monstruos, sino mejorar **la habilidad ofensiva existente de Viento** en tasa de victoria frente a las otras raíces. Se revisó `lanza_nubes` en LianQi II, preservando el cierre ratificado de V35/V36, la Sobretúnica **DEF+2/HP+2** y los seis monstruos moderados. El sangrado se testeó como **contrafactual NO canónico**, sin añadir estados al juego.

## A — Comparación de cinco raíces con las rotaciones de combate completas
Seis monstruos normales V33 aprobados, 16 builds por raíz, T1/T2 adaptativo, dos políticas EARLY/DELAYED_TRIGGER, equipo uniforme M03 o Sobretúnica DEF2 original, dos cohortes independientes 117100–117101 y 117500–117501. **30.720 combates nuevos**, 0 errores, COLD exacto 7.680 filas. Correcciones V17 físicamente instaladas para las cinco raíces y V36 ratificado para Viento. UNA Concordancia BASE escalar representativa por raíz, como supuesto LAB, sin certificación de acceso real.

| Raíz | WR jugador T2 uniforme | WR jugador T2 Sobretúnica |
|---|---:|---:|
| Agua | 58,72% | 84,64% |
| Fuego | 60,16% | 82,42% |
| Metal | 64,84% | 90,49% |
| Tierra | 70,44% | 89,45% |
| **Viento, V36 vigente** | **58,85%** | **80,60%** |
| **Viento con coste Lanza -1 Qi** | **63,67%** | **85,03%** |
| Viento, sangrado garantizado 1×2 pulsos DIAGNÓSTICO | 72,27% | 87,50% |
| Viento, Lanza daño base +1 universal DIAGNÓSTICO | 70,05% | 86,07% |

**El sangrado incondicional rebasa Tierra en T2 con uniforme**, por lo que no es el ajuste moderado indicado. El +1 universal también resulta muy amplio. El coste -1 mejora de forma mesurada.

## B — Especializaciones T1
**18.432 ejecuciones**, incluidas **6.144 repeticiones exactas** de los dos brazos V36/-1Qi del ensayo A. Comparaciones T2/uniforme: V36 58,85%; sangrado 1×1 para toda Lanza 69,53%; sangrado 1×2 solo T1 Eficiencia 63,02%; sangrado 1×2 T1 Precisión/Eficiencia 70,44%; +1 daño solo T1 Eficiencia 62,37%; coste -1 general 63,67%. COLD exacto 4.608.

## C — Técnica ofensiva aislada
**25.344 peleas nuevas** con las cinco raíces, mismas seis especies/tier/build/equipo, **SIN lanzar defensivas ni técnicas extranjeras/Concordancias**, y perfil natural generado realmente para cada batalla. El runner inicial que omitía materialización de perfil se descartó; solo se conservaron resultados del runner corregido. COLD 4.224 filas exactas.

**T2/uniforme:** Metal 42,19%; **Viento V36 47,74%**; Tierra 49,13%; Fuego 59,38%; Agua 60,76%; **Viento coste -1 Qi 55,03%**; Viento sangrado en cada impacto 1×2 65,80%. Es incorrecto afirmar que Lanza es siempre la peor de las cinco: sin defensa, Metal tiene menos victorias en esta muestra. La desventaja de Viento en rotación completa depende también de los otros componentes del combate.

## D — Eco del Caído E8 T0, solo diagnóstico
**39.424 combates nuevos**: DISCOVERY 28.672 (119100–119163), HOLDOUT 10.752 (119500–119523); COLD 3.584 exactas. Jugador LianQi II, 16 builds T1, cinco raíces, equipo verdaderamente garantizado de prólogo o posterior M03; defensiva de prueba no acreditada. E8 seis cifras históricas auténticas; **Control=0 NO verificado**, sin especiales ni T1/T2 adaptativo y sin paridad productiva. Perfil original PENDING intacto.

**Con equipo de prólogo** y Viento, 1.408 escenarios por política/brazo: solo ofensiva **68,54% V36 → 71,80% coste -1 Qi**; defensiva hipotética **68,96% → 74,72%**. Sangrado forzado 1×2 sube respectivamente a **81,89% y 80,75%**, sin contrato legítimo que permita a un espíritu sangrar físicamente: no promoverlo.

## Dictamen V38
**Propuesta única, todavía NO ratificada:** coste de `lanza_nubes` en LianQi II **6 → 5 Qi**. Si se elige su nodo T1 de Eficiencia, seguir aplicando la reducción de 1 punto de ese nodo: **5 → 4 Qi**. NO modificar LianQi I, daño, evasión ni reglas DOT. Mantener V36 ya aprobado: T1 DIRECT 30%, T1 PRECISIÓN `2d4+4`, Paso T1 EVA 45. No reabrir seis monstruos normales. No instalar un status nuevo de sangrado.

## QA y límites
V38A 30.720, V38B 18.432 (6.144 ya repetidos), V38C 25.344, V38D 39.424: **113.920 ejecuciones no-COLD, 107.776 casos nuevos únicos; 20.096 filas COLD reproducidas exactamente.** Cero timeouts. Pareo de semillas válido **entre brazos de la misma raíz**; las distintas raíces no usan el mismo flujo RNG. Las cifras de A/B/C/D son de fixtures diferentes y no deben agregarse como si representaran un único torneo.

Portable: `GRULLA_PRE_A08_V38_REBALANCE_LANZA_VIENTO_2026-10-09.zip` SHA256 `d441fea5db0d19851f9f343166554b57246b68523d7a1a5948f6ad65c759611f`, 102 archivos, CRC+manifiesto PASS, cuatro COLD reproducidos desde ZIP extraído. ZIP adjunto a conversación, no subido a Git.

**Guardias:** rama experimental solamente; NO `main`, merge, HTML, `ROOMS.exits`, A07, economía/precios, perfiles de monstruos ni equipo. E8 no ratificado. Esta enmienda de Qi es propuesta pendiente de decisión humana, y no sustituye el cierre V36 hasta entonces.
