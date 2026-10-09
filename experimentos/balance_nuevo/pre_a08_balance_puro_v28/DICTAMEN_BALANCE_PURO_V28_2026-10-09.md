# PRE-A08 V28 — Puente de aflicciones desde ataques de monstruos
**Fecha: 2026-10-09 · LAB PASS / NO CANON / NO FREEZE / NO RUNTIME.** Continuación de V27, excluyendo comercio, precios y economía.

## Hallazgo prioritario: un problema de traducción del golpe, no simplemente potencia de veneno
En `monster_arc1_registry.json` del LAB, las técnicas de **Serpiente de Qi** y **Avispa de Jade** declaran `POISON_DOT` sin `direct_damage`. El resolver LAB trata ese especial como un chequeo de impacto SIN daño directo, aunque lo considera suficiente para añadir `MONSTER_DOT`. El contrato de aflicciones persistentes de ver74 exige daño positivo real de Vida para aplicar veneno o quemadura. Por tanto, si se exige estrictamente `actual_hp_damage>0`, estos especiales no pueden infectar.

**Pero en ver74** `respuestaEnemigos` (aprox. 15375–15450) ejecutaba `atacar(eMod,def)` también durante el especial: si `tec.daño` no existía, se conservaba el daño básico del monstruo. Es probable que el traductor de técnicas al nuevo LAB omitiera ese golpe. **No cambiar el contrato ni decidir balance antes de auditar el descriptor traducido.**

## Tres brazos diagnósticos, NO cambios canónicos
- `STRICT_HP_DAMAGE`: descriptor LAB vigente, estado solo después de daño positivo de HP.
- `CONNECTED_ONLY`: permite estado tras impacto aunque no llegue daño; CONTRADICE la regla estricta; sirve exclusivamente como sensibilidad.
- `VER74_BASIC_DIRECT`: cuando especial carece de daño directo, usa hipotéticamente el daño básico de la especie y mantiene `actual_hp_damage>0`; contraste de fidelidad a ver74. No promueve legacy al nuevo runtime.

**Sapo de Ceniza** ya posee `direct_damage=1d2+4` en LAB; estricta y ver74-hipótesis producen las mismas trayectorias en su caso.

## Ejecución y reproducibilidad
Primera pelea T0 real contra Serpiente/Avispa/Sapo, 5 raíces × 4 builds por raíz × 2 políticas × M03 o Sobretúnica DEF1/HP2 candidata; aflicción causada por evento del ataque realmente ejecutado en LAB y persistida por adapter. Segunda pelea con 6 monstruos originales LII, T1/T2, conservando HP y Qi y avanzando una caminata. Comparaciones: sin remedio, remedio después de caminar, medicina HP Templada estable `3d4+9`, ambos, remedio incompatible.

- DISCOVERY semillas 102100–102101: **85.320 ejecuciones físicas**.
- HOLDOUT semillas 102500–102501: **85.200 ejecuciones físicas**.
- **170.520 combates nuevos**, incluidos 2.880 primeros combates únicos y 167.640 segundos.
- **172.800 filas de escenarios comparativos** (no confundir filas con combates ejecutados).
- COLD 102100: **43.200 filas × 42 columnas exactas** frente a DISCOVERY, excluyendo solo `cohort`; NO sumadas al total de combates nuevos.
- Timeouts **0**; due_missed **0**; remedio incompatible = brazo no tratado en métricas; sin mutar canon, equipo ni monstruos.
- El daño por aflicción **ignora DEF pero atraviesa Absorción** según el nuevo contrato; control 3 DOT contra reserva de 4 absorbe 3 y no pierde HP.

## Primera pelea: estado todavía activo después de victoria
Cada fila representa **320 primeras peleas únicas** por fuente y brazo, no todos los segundos combates duplicados.

| Fuente | Modo | Victorias iniciales | Aplicaciones durante primer duelo | Estado activo al ganar |
|---|---|---:|---:|---:|
| Serpiente | STRICT | 320 | 0 | **0** |
| Serpiente | CONNECTED_ONLY | 319 | 749 | 247 |
| Serpiente | VER74_BASIC_DIRECT | 319 | 390 | **157** |
| Avispa | STRICT | 320 | 0 | **0** |
| Avispa | CONNECTED_ONLY | 315 | 843 | 153 |
| Avispa | VER74_BASIC_DIRECT | 319 | 252 | **52** |
| Sapo | STRICT | 297 | 276 | **132** |
| Sapo | CONNECTED_ONLY | 288 | 428 | 167 |
| Sapo | VER74_BASIC_DIRECT | 297 | 276 | **132** |

La aplicación varias veces puede dar una única aflicción activa porque rige la reutilización de familia y duración. El número de estados **activos después de ganar** es mucho menor que las aplicaciones.

## Segundo duelo T2, Sobretúnica DEF1 candidata, entre ganadores del primero
| Fuente / variante | Sin tratamiento | Medicina HP sola | Tratamiento compatible + HP |
|---|---:|---:|---:|
| Serpiente / STRICT | 24,27% | 34,48% | 34,48% |
| Serpiente / VER74_BASIC_DIRECT | 4,40% | 22,12% | **25,37%** |
| Avispa / STRICT | 30,10% | 34,17% | 34,17% |
| Avispa / VER74_BASIC_DIRECT | 15,51% | 32,08% | 32,08% |
| Sapo / STRICT | 4,25% | 17,00% | **18,68%** |

No comparar tasas absolutas de variantes como si fueran igual de fuertes: introducir golpe básico también cambia el daño inicial recibido. En este diseño las medicinas específicas se usan **después de caminar**. La duración corta de Avispa suele agotarse con ese movimiento; corresponde luego estudiar tratamiento **antes** de caminar antes de concluir que el antídoto carece de valor.

## Resultado para el balance
1. **NO tocar números de veneno/quemadura ni remedios por V28.** Primero auditar si el nuevo descriptor omite por error el daño básico de Serpiente y Avispa. El contrato exige decisión explícita y una prueba de integración posterior.
2. No aprobar `CONNECTED_ONLY` por ser más sencillo: omite el requisito de que el veneno entre solo si se perdió HP.
3. El puente persistente V28 **ES LAB**; no prueba integración con HTML/A08. Existe un anclaje a golpes reales del motor LAB, no una exposición guionizada como V27, pero no es la autoridad productiva.
4. Mantener **Sobretúnica DEF+1/HP+2** como candidata, Cangrejo/Jabalí originales, Embalse V25 pendiente y condicionales V26 sin magnitudes ratificadas.
5. No tocar `main`, no merge, no cambios en HTML, `ROOMS.exits`, A07, comercio ni precios.

## Paquete reproducible
`GRULLA_PRE_A08_V28_BALANCE_PURO_PUENTE_AFLICCIONES_NATIVAS_2026-10-09.zip` — **80 archivos**; SHA-256 `5cf0b3bedc8e28b3f2bb5a7e91adbdc6fc2027fd6fb9dccf87fd0f40bee244c3`. CRC PASS, manifiesto SHA PASS, pruebas mecanicistas PASS, COLD desde carpeta limpia PASS. Incluye runner, tests, RAW gzip, análisis, matrices y dependencias V27. ZIP adjunto a la conversación y **NO** subido a Git; este archivo documenta el experimento.
