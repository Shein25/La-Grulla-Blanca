# V35 — Cierre numérico de seis monstruos normales LianQi II

**2026-10-09 · HUMAN-DIRECTED NUMERIC DESIGN CLOSED · LAB PASS · NO RUNTIME / NO HTML / NO MAIN.**

Decisión del usuario: revisar Viento y, tras esa revisión, dar por cerrado el balance numérico de los monstruos normales y avanzar al frente élite. Se mantienen intactas la Sobretúnica de patrulla **DEF+2 HP+2** y el criterio de expectativa/progresión ratificado. No reabrir el balance del equipamiento por esta causa.

## Prueba nueva V35: Viento T1–T2
Dos cohortes con semillas 112200–112207 y 112800–112807; **24.576 combates cada una; 49.152 nuevos en total**, dos brazos (ORIGINAL / V33_MODERADO) × seis especies × 16 builds de Viento × EARLY/DELAYED_TRIGGER × T1/T2 × cuatro equipos. **24.576 contextos pareados**. COLD = **6.144 filas ×32 columnas exactamente repetidas**, no se incluyen como nuevos. 0 timeouts, 0 turnos de monstruo omitidos; perfiles y equipo restaurados.

### Viento T2 — victoria del jugador (n=3.072 por celda)

| Equipo | Original | V33 moderado |
|---|---:|---:|
| Uniforme inicial M03 | 58,66 % | **51,20 %** |
| Sobretúnica original | 85,03 % | **78,78 %** |
| M05 pesado común experimental | 94,92 % | **91,73 %** |
| M05 ligero Sauces experimental | 82,85 % | **77,18 %** |

Con monstruos moderados: DISCOVERY uniforme 51,50 %, HOLDOUT 50,91 %. Intervalo descriptivo agrupado por semilla/política/build: **49,45–52,96 %**. El valor V34 de 48,96 % con uniforme procedía de una muestra independiente menor (n=768). En V35 el tier T1 con uniforme da 55,27 %. Los peores cruces T2/uniforme/moderados son Jabalí 43,36 % y Cangrejo 48,63 %; con la Sobretúnica, los resultados por especie aumentan considerablemente. Las 16 builds de Viento no son equivalentes: observamos de 44,27 % a 63,02 % T2 con uniforme. No hay umbral universal de WR ratificado que obligue a reducir monstruos en estos contextos.

**Dictamen:** Viento es la raíz con margen más exigente del conjunto en equipamiento inicial; ya lo era con los monstruos originales. La mejora sensible al progresar con equipo y la replicación independiente permiten **no reabrir los ajustes moderados**. El balance específico de técnicas de Viento sigue siendo dominio del frente de habilidades, no del catálogo de monstruos.

## Valores cerrados como TARGET NUMÉRICO para entrega a integración (solo seis normales)

| Monstruo | Atributo | Original | Objetivo V33 |
|---|---|---|---|
| Jabalí de Pizarra | daño de Embestida | `1d3+6` | **`1d3+8`** |
| Búho de Niebla Gris | daño de Picado | `1d2+7` | **`1d2+8`** |
| Zorro de Bancales | evasión | `19` | **`21`** |
| Cangrejo de Cauce | daño de Pinza | `1d2+7` | **`1d2+8`** |
| Murciélago Resonante | daño de Pulso | `1d2+5` | **`1d2+6`** |
| Araña de Veta Sombría | HP base | `71` | **`75`** |

Esos números provienen de V33 y están validados por V34 y V35. Descartar V34 ROLE_STRONG. Las propuestas V19 de debilitar buff de Cangrejo y mitigación del Jabalí **NO** se incorporan simultáneamente. No modificar especiales, adaptativo T1, DOT, técnicas, equipo o economía por este cierre.

## Límites y pase a élites

**El frente normal LII queda cerrado numéricamente**, NO significa que se hayan parcheado registros canónicos ni validado su paridad en A08/HTML. Fuente LAB: V17 una Concordancia BASE ESCALAR representativa por raíz; no todas las condicionales/estructurales; tampoco T3/T4, élites, jefes, AOE, persistencia productiva ni disponibilidad efectiva de equipos opcionales. Integración y regresiones de runtime son un paso de otro agente.

**Nuevo frente:** Eco del Caído, élite LII. Archivo histórico V02 de 34.560 duelos T0 conservado y re-auditado, E8 preferente pero sin ratificación. Ver `experimentos/balance_nuevo/pre_a08_elite_v36/PREFLIGHT_ECO_CAIDO_V36_2026-10-09.md`. No repetir benchmarks ni inventar perfiles.

## Paquete portable y fuentes

`GRULLA_PRE_A08_V35_CIERRE_NORMALES_Y_PREFLIGHT_ELITE_2026-10-09.zip` · SHA256 `bb944e145d39a23ef9d106b39bcca33fafd13c31abf32ef28814ec0199fe2a7a` · 63 archivos · manifiesto SHA256 y CRC PASS · ejecutado en carpeta nueva: COLD 6.144 filas exactas, análisis y preflight élite PASS. ZIP se entrega en conversación, no subido a Git. Contiene runners, datos brutos, matriz por build, raí­z V34 como referencia histórica, y el paquete Eco T0 previo.

**Guardias:** no `main`, no merge, no `ROOMS.exits`, no HTML, no precio/comercio, sin modificación a catálogos canónicos, sin inventar NPC o monster.
