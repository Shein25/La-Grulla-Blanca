# LianQi II · Gate V09 — Tramo I, multirraíz, decisiones de Qi
**Fecha:** 2026-10-08
**Estado:** `LAB_PASS_NOT_CANON`; V07 continúa candidato, Concordancias **OFF** y sin integración HTML.

## Autoridades y restricciones
- LianQi I: 0 puntos, solo técnicas unitarget BASE, sin defensivas o AOE; no reabrir contratos congelados.
- LianQi II: Tramo I desbloqueado, 2 puntos, 16 builds legales monorraíz por raíz; defensivas admitidas, AOE ausentes.
- Seis especies nuevas normales T1/T2; el élite no está diseñado, T3/T4 se posponen a LianQi III.
- Raíces elementales neutrales ×1,00; **no anular Concordancias**. No se modificaron monstruos, equipo, técnica base, `main`, ni el HTML.
- Candidato V07, *solo si el usuario eligió ese nodo*: Fuego Ascua Adherente 2→1 daño por pulso; Metal Ejecución +10 pp de crítico; Viento Punta de Tormenta daño directo +20%→+30%. **No autorizado para runtime**.
- El aprendizaje de técnica BASE extranjera es un sobreconjunto hipotético. Su adquisición narrativa, restricción/coste extranjero y posible incompatibilidad todavía no están certificados por el motor oficial.

## Ejecuciones
| Batería | Combates | Contextos pareados | Semillas |
|---|---:|---:|---|
| Screen: 5 raíces, 4 extranjeras, 6 especies, 2 equipos, 2 tácticas, 16 builds, T1/T2; 4 estrategias acceso, ORIGINAL/V07 | 491.520 | 61.440 | 3000–3003 |
| Corrección: primera ronda **ofensiva**, no primera ronda absoluta | 122.880 | 30.720 | 3000–3001 |
| Focal confirmatoria: Metal/Tierra/Viento con Agua BASE, T2, POST_M03 | 73.728 | 18.432 | 4000–4031 |
| **Total** | **688.128** | **110.592** | — |

Todos PASS: 0 timeouts, 0 pérdidas de técnica de cadencia, igualdad exacta de Agua/Tierra entre ORIGINAL/V07, MONOROOT invariante respecto a la etiqueta extranjera, semillas consistentes. Reproducción independiente en carpeta limpia: **4.608 de 4.608 combates y 8 métricas idénticas**.

## Resultado de V09, T2 POST_M03, todas las 16 builds
Porcentaje de victorias del jugador con **V07**, Concordancias desactivadas.

| Raíz | Monorraíz | Técnica ajena cada tercera ronda | Delta pp |
|---|---:|---:|---:|
| Fuego | 73,70 % | 69,14 % | −4,56 |
| Agua | 74,35 % | 64,91 % | −9,44 |
| Tierra | 64,58 % | 63,70 % | −0,88 |
| Metal | 59,38 % | 61,33 % | +1,95 |
| Viento | 54,95 % | 54,98 % | +0,03 |

La estrategia genérica de rotar técnicas no es una solución. El brazo `FOREIGN_OPEN` original no se disparó con `DEFENSE_REFRESH` (la primera ronda se usó para defender); se corrigió por separado como `FOREIGN_FIRST_OFFENSIVE`, **una activación efectiva por duelo**. Esa apertura corregida no mejoró de forma sistemática los resultados (Agua −7,55 pp, Fuego −2,87 pp, Metal −0,65 pp, Tierra −0,85 pp, Viento +0,59 pp en R2).

## Focal independiente: aprender Latigazo de Marea BASE (sin puntos en la rama extranjera)
Todos T2 POST_M03; seis monstruos, dos políticas, 16 builds, R32, mismos individuos y semillas por brazo:

| Raíz primaria | Sin técnica ajena | Rotar BASE Agua | Mejora |
|---|---:|---:|---:|
| Metal | 59,42 % | 71,58 % | **+12,16 pp** |
| Tierra | 65,56 % | 71,00 % | **+5,44 pp** |
| Viento | 56,02 % | 63,07 % | **+7,05 pp** |

**Riesgo de dominancia:** Latigazo de Marea BASE podría ser elección secundaria muy eficiente, pero no aprobar nerf/buff por resultados obtenidos sin adquisición, coste de raíz ajena y Concordancias oficiales. Este efecto existe con ORIGINAL y V07, así que no lo produjo por sí solo el ajuste V07.

## Bloqueos del cierre
1. Montar auténtico resolvedor `CONCORDANCE_ON/OFF` del candidato LI V04B y extensiones legales LII, con mapeo explícito de hooks BASE/Tramo I; NO aplicar porcentaje genérico inventado.
2. Comprobar adquisición y coste efectivo de técnica ajena antes de simular que puede usarse indiscriminadamente. En particular, validar qué rol cumple Agua sin convertirlo en selección obligatoria.
3. Ejecutar pares con política de uso realmente táctica y Concordancias activas: 5 receptores BASE NONE de V08 siguen siendo guardias, no bonos.
4. Verificar paridad de eventos con HTML candidato, continuidad de cadencia T1/T2 y regresar a LI para control 0 puntos/0 defensivas/0 AOE.
5. No congelar ni incorporar V07 o los seis monstruos todavía; equipo y economía están fuera del cambio.

## Paquete reproducible del laboratorio
`GRULLA_LII_V09_POLITICAS_MULTIRRAIZ_AGUA_2026-10-08.zip`: 36 entradas, CRC y SHA-256 verificados. Archivo SHA-256:
`2b2d3bcc7738721bed60e53a6335b2a171ff78a6e13bcda5945d22397c95c37e`.
Runners SHA-256:
- `run_v09.py`: `86564d95e5030a0683bcea8f946d1b6419766bf9bcc1209650963cf0789368a6`
- `run_v09_first.py`: `2f9964b41dc4a4828c5f9ec3988d623c3da7ea3eca1408fc643920ff27ecc403`
- `run_v09_water.py`: `853296a70d85360cce41fa4f5edd9fdabe51cc7696a8b8e9d749fb042b91f01e`

Los CSV comprimidos y el entorno reproducible están en el ZIP adjunto a la conversación, no en el repositorio. Los documentos V08 de la misma rama siguen siendo fuentes de contraste.
