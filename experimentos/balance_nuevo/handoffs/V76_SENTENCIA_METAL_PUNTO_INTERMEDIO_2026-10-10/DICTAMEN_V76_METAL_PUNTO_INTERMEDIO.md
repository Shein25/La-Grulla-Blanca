# V76 — búsqueda de punto intermedio para Sentencia de Metal

**10/10/2026 · Diseño propuesto, NO aprobado para sustituir V67.** La orden humana fue buscar una versión intermedia después de comprobar que V03.1 gana casi 100% contra Sombra y el nerf V67 apenas mejora frente a no utilizar Ultis. V67 SOFT_M02 mantiene la autoridad ratificada hasta nueva decisión del autor.

## Ficha propuesta «MID_B_V76»

| Mecánica | Original V03.1 | V67 ratificada | V76 intermedia propuesta |
|---|---:|---:|---:|
| Golpe inicial, escala | 100 % | 50 % | **65 %** |
| Penetración extra, pp | 90 | 45 | **10** |
| Hemorragia | 3 cargas × potencia4 × 3 activaciones | 1 carga × potencia1 × 2 activaciones | **1 carga × potencia2 × 2 activaciones** |
| Punto de Ruptura, escala | 100 % | 50 % | **65 %** |
| Coste | 16 Qi | 16 Qi | **16 Qi** |

Se preservan precisión adicional +30, activación de hemorragia tras daño real al HP, herida sometida a absorción/inmunidad anatómica, dos ticks efectivos antes del remate, ataque Metal vinculado y condición de una Ulti por combate. La penetración adicional de la Ulti pasa a +10pp; **la penetración habitual del personaje no se toca**. No modificar técnicas normales Metal ni Ultis de otras raíces.

## Holdouts independientes H1/H2, mismo E1 V66 + puente V67/V03.1

Misma **Sombra V72**: 110 HP, DEF1, veneno CD4 ×2, Espejo de 8. Cinco guardianes mantienen kits del laboratorio V67. Todos los jugadores usan builds LIII legales de 4 PT; conjuntos LII máximos de DEF/EVA y un LIII hipotético opcional que **no se concede al ascender**. Tres políticas; una sola Ulti de raíz Metal, sin injerto, AOE multiblanco ni Concordancias ON.

| Enemigo | V67 SOFT_M02 lanzada R2 | V67 SOFT_M02 lanzada R4 | **MID_B_V76 lanzada R4** |
|---|---:|---:|---:|
| **Sombra Ahogada** | 40,54% | 43,43% | **54,83%** |
| **Rey Escarabajo** | 78,67% | 72,92% | **83,56%** |
| Sapo de la Caldera | 61,34% | 54,28% | **69,33%** |
| Mantis de Nube | 68,98% | 69,36% | **77,86%** |
| Guardián de Coral | 34,55% | 33,71% | **39,67%** |
| Custodio Eco Pétreo | 35,19% | 34,55% | **40,48%** |

**Tamaño:** Sombra **6912 duelos por alternativa**; guardianes **3456 por alternativa y por enemigo**. MID_B_V76 lanzada R4 obtuvo 3790/6912 victorias ante Sombra, 2888/3456 ante Rey, y 0 muertes de guardianes hasta ronda3. Son porcentajes reales del adaptador físico, **no certificación del HTML**, no resultados AOE reales.

### Cuándo conviene usarla

Sombra V72, V76 B: **R1 49,91%**, **R2 50,16%**, **R4 54,83%**. El laboratorio difiere en el primer turno elegible; no se debe imponer un autocast en R4. El jugador elige en función de Qi, defensa, control, ventana de daño y disposición del enemigo. Ninguna política es óptima universal.

**Por equipo V76 B R4 contra Sombra:** máximo LII defensivo 52,95%; LII evasivo 32,55%; LIII opcional 78,99%. Builds Metal 0/1/2 71,92/48,74/43,84%; el 54,83% es promedio experimental, no hardcap por build.

### Conservadora alternativa A

Escala de apertura **65%**, remate **50%**, penetración extra **+10pp**, sangrado potencia2 ×2, una carga. Reservada a R4: Sombra **51,43%** y Rey **79,46%**. Es menos ofensiva y respeta mejor el resultado previo contra Rey, pero fortalece menos el remate.

**Candidata C descartada:** 70% apertura, 65% remate, penetración extra0, sangrado potencia2; R2: Sombra51,61%, Rey89,50%; en el holdout hubo una muerte temprana ante Mantis. No ofrece una ventaja suficiente frente a B.

## QA, fuentes y limitaciones

- **6912/6912 replays exactos**, 0 diferencias de V67 SOFT_M02 contra los CSV V73 en victoria, rondas, HP final y Qi final.
- Benchmark V67 Rey SOFT_M02: **78,889%** sobre la misma batería histórica de 720 peleas, reproducido exactamente.
- Pantalla de búsqueda Sombra con 34.560 combates de nuevas cohortes y cruce guardianes con 69.120 duelos. Dos lotes H1/H2; los distintos brazos comparten seeds iniciales y no equivalen a pruebas independientes por evento.
- Ajustes de ronda4: 6912 duelos Sombra por brazo y 3456 de cada guardián por brazo; detalle físico individual B R4 Sombra en CSV con 6912 filas.
- Inmunidad de Sangrado de Coral/Custodio y T0 numérico de Custodio son **hipótesis de laboratorio aún no ratificadas**. El puente E1/V03.1 no certifica el HTML ni los efectos nativos de las 25 Ultis.
- ZIP portable: **`GRULLA_V76_SENTENCIA_METAL_PUNTO_INTERMEDIO_2026-10-10.zip`**, SHA256 **`6d0891daf20dedda7ff2d387d748435b03d27baa79ef7b07c8a61706422ab15c`**, 2.210.439 bytes, 31 entradas, CRC y SHA256 manifiesto PASS. Incluye V73 sellado de referencia, ejecutores, resultados, y comprobación portable: extraído en limpio y pasado `prepare_v76.py` + `v76_qa.py` sin fallos. Entregado por chat, **no Git**.

### Estado autoritativo

**Propuesta B preferida para un siguiente gate de validación, NO ratificada por el autor.** No tocar `BALANCE_ULTIS_METAL_VIENTO_APROBADO_V67.json`; no patch HTML, main, merges, registro T0, kits de monstruos o guardianes. Un cambio de técnica definitiva requiere aprobación humana explícita y después paridad en runtime real, antes de considerarlo cerrado.
