# REFERENCIA CANÓNICA ACTUAL — MONSTRUOS DE LA GRULLA BLANCA (V3)

**Fecha de reconciliación:** 2026-10-10.
**Autoridad:** decisión expresa del autor de considerar **canónicas todas las especies nuevas creadas en LianQi II y III**; fuentes de diseño V35, V45 y V46.
**Registro maestro actual:** [`CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json`](CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json).
**Estado de aplicación:** canon de IDENTIDADES y diseño. Integración a runtime/HTML y cierre individual T0 no se presumen.

## 1. Conteo actual, sin omisiones

El catálogo maestro verificado documenta **31 identidades distintas**:
- **18 identidades históricas** del registro original `monster_arc1_registry.json`, que sigue sirviendo de fuente histórica numérica.
- **6 nuevos repetibles de LianQi II**, diseño y ajustes V35 ratificados por el autor el 9/10/2026.
- **6 nuevos repetibles de LianQi III**, identidades y diseños V45 aprobados por el autor en V46 (9/10/2026), fichas numéricas V45 aún candidatas.
- **1 nuevo guardián único de LianQi III**, `custodio_eco_petreo`, con nombre/ID de diseño aprobados, pero T0 y spawn pendientes.

**Es falso y queda DEPRECADO usar la frase «18 monstruos en total».** También queda deprecado el índice parcial V2 de **25** identidades, que omitía los seis nuevos repetibles LIII. **31 es el número verificado actual, no un máximo inmutable para futuras incorporaciones.**

Distribución por `native_stage` histórica o etapa de diseño: LI = 5; LII = 11; LIII = 11; LIV = 4. La etapa nativa histórica de un jefe puede diferir de la etapa legal de encuentro (los cinco guardianes AOE se habilitan legalmente en LIII). Los perfiles LIII incluyen 8 repetibles (Pez, Anguila y seis V45), la Sombra Ahogada única, Coral y Custodio; otros guardianes tienen etiquetas históricas LIΙ/LIV pero gate de encuentro LIII.

## 2. Seis repetibles nuevos LianQi II — RATIFICADOS

| ID canónico | Nombre | Estado |
|---|---|---|
| `jabali_pizarra` | Jabalí de Pizarra | V35 aprobado (numérico), HTML pendiente |
| `buho_niebla_gris` | Búho de la Niebla Gris | V35 aprobado, HTML pendiente |
| `zorro_bancales` | Zorro de los Bancales | V35 aprobado, HTML pendiente |
| `cangrejo_cauce` | Cangrejo del Cauce Pétreo | V35 aprobado, HTML pendiente |
| `murcielago_resonante` | Murciélago Resonante | V35 aprobado, HTML pendiente |
| `arana_veta_sombria` | Araña de la Veta Sombría | V35 aprobado, HTML pendiente |

Autoridad V35:
`experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/DECISION_HUMANA_CIERRE_LII_NORMAL_Y_VIENTO_2026-10-09.json`, rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`.

## 3. Seis repetibles nuevos LianQi III — CANON DE DISEÑO V45/V46

| ID canónico | Nombre | Identidad mecánica |
|---|---|---|
| `garza_bruma_roca` | Garza de Bruma de Roca | EVA y precisión |
| `cangrejo_laja_humeda` | Cangrejo de Laja Húmeda | DEF y tenacidad |
| `sanguijuela_remanso_turbio` | Sanguijuela de Remanso Turbio | Veneno |
| `salamandra_filtracion_tibia` | Salamandra de Filtración Tibia | Quemadura |
| `rana_cascajo_barranco` | Rana de Cascajo del Barranco | Ataque sostenido |
| `carpa_lamina_reflejo` | Carpa de Lámina Reflejada | Drenaje Qi |

Fuentes originales recuperadas y preservadas *sin alteración de su autoridad*:
- [`FUENTE_IMPORTADA_V45_NUEVA_FAUNA_LIII_2026-10-09.md`](handoffs/V67_CIERRE_GUARDIANES_ULTIS_2026-10-10/FUENTE_IMPORTADA_V45_NUEVA_FAUNA_LIII_2026-10-09.md): seis IDs, perfiles T0 numéricos candidatos, ubicaciones fijas propuestas, **219.240** combates, QA y limitaciones. El autor no había ratificado sus números individualmente.
- [`FUENTE_IMPORTADA_V46_CADENA_ADAPTATIVA_LIII_2026-10-09.md`](handoffs/V67_CIERRE_GUARDIANES_ULTIS_2026-10-10/FUENTE_IMPORTADA_V46_CADENA_ADAPTATIVA_LIII_2026-10-09.md): constancia textual de aprobación humana de **las seis identidades y diseños V45**. T1–T4/Mutantes todavía son **propuestas**, NO cierre ni activación productiva.

**Regla estricta:** ser identidad CANÓNICA no implica `stats_status=READY`, `technique.params_status=READY`, T1–T4 congelados, mobs ubicados/spawneados, botín ni XP integrados. Hasta aprobación numérica específica, la ficha numérica V45 permanece `PENDING_INTEGRAL_REBALANCE`. Ubicaciones en V45 también son propuestas, no spawns activos. Los anteriores normales LIII `pez_lunar` y `anguila_estelar` permanecen, sin reemplazo.

## 4. Guardián canónico sin integración

`custodio_eco_petreo`, **El Custodio del Eco Pétreo**, guardián único LIII de la técnica AOE Tierra. Nombre, ID y rol ratificados; sin T0 numérico canónico, manual de runtime ni spawn implementado. `bosque_rocas_blancas` es ubicación propuesta. No sustituir por `centinela_pluma`.

## 5. Uso obligatorio para futuros tests, agentes y Astra

1. Listas de monstruos: **siempre comenzar por V3**. V2 es histórico parcial, `monster_arc1_registry.json` de 18 es fuente T0 histórica, **ninguno de los dos es inventario completo vigente**.
2. Monstruos nuevos de LII y de LIII: forman parte del canon aunque no estén integrados en HTML; no omitirlos al planificar pruebas posteriores, incluyendo AOE POST_MANUAL.
3. Balance numérico: consultar autoridad propia por especie; no reabrir T0 ratificados ni convertir propuestas T0/T1–T4 de V45/V46 en READY sin decisión expresa.
4. AOE multiblanco: comprobar gate manual/etapa y objetivos reales; el motor V66 E1 1v1 no demuestra comportamiento contra 2+ enemigos. No inventar salas/spawns/grupos.
5. Repetibles son especies sujetas a su contrato de adaptación; únicos no usan T1–T4 persistentes. No mezclar `native_stage` histórico con acceso real.
6. Extensiones futuras: añadir nueva criatura documentada al índice V3 sucesor/versionado y aumentar el total. No crear techos fijos.

**Guardias:** No tocar `main`, no merge, no HTML, `ROOMS.exits`, T0 ratificados, economía, drops, spawns ni NPCs como efecto colateral de este cambio documental.

## 6. Actualización del único Eco del Caído — V69 (10/10/2026)

Por autorización humana se diseñaron tres habilidades propias del **élite único** `eco_caido`: **Veta Resentida**, **Lamento del Caído** y **Reverberación del Agravio**. La batería física V69 (192.000 combates con cinco brazos) produjo **45,27% de victoria del jugador** con todas las habilidades, y la regresión base pasó 1.050 parejas con cero diferencias. Están documentadas en `experimentos/balance_nuevo/handoffs/V69_ECO_ELITE_NUEVAS_HABILIDADES_2026-10-10/ECO_DEL_CAIDO_HABILIDADES_V69_CANDIDATO.json`. **Solo es diseño y valor candidato**, no habilidad ya integrada al HTML ni reemplazo del Eco T0. `45c3a9` documenta HP51 READY y PRE-A08/V39 documenta E8 HP84 PENDING: conflicto aún pendiente de conciliación, sin tocar ninguno. El límite de 70% se cumplió en los promedios globales y marginales; la política óptima con equipo LII máximo DEF alcanzó 79,46%. NO se debe anunciar un cap universal por build.

## 7. Cierre numérico V70 de Eco — T0 histórico 51HP conservado

**10/10/2026.** Por decisión del autor de cerrar el balance antes de AOE, la versión **V70** sustituye la recomendación experimental **V69 de Eco E8 84HP**. Se seleccionaron y validaron las mismas tres habilidades (`ECO_VETA_RESENTIDA`, `ECO_LAMENTO_DEL_CAIDO`, `ECO_REVERBERACION_AGRAVIO`) sobre el **T0 ratificado HP51** del commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35`. No modificar ese T0 ni reabrir valores antiguos.

**Cierre de balance de laboratorio V70:** 192.000 duelos documentados, de los cuales 96.000 son dos holdouts independientes del finalista; 0 timeouts; 1.050 pares exactos E1; 600 replays idénticos. Victoria global jugador **49,39%**; promedio con equipo de Prólogo garantizado **28,89%**, tras M03 **29,72%**, equipo superior DEF LII opcional **67,13%**. Las raíces y políticas también quedan bajo 70% en sus promedios, NO se impone límite fijo a todos los estratos; hay builds/combos >70% legítimas. Todos los ítems analizados son LI/LII, 2 PT, sin Ultis ni AOE.

**Autoridad machine-readable:** `experimentos/balance_nuevo/handoffs/V70_ECO_CIERRE_T0_51HP_LII_2026-10-10/V70_ECO_CIERRE_NUMERICO_CANDIDATO.json`. Informe y QA hermanos. Archivo portable ZIP del chat `GRULLA_V70_ECO_T0_51_CIERRE_BALANCE_LII_2026-10-10.zip`, SHA256 `861cb5a612c1b05f290c7f6a7d2a484e8c53a7d591955abba9ff8e32849e7542`.

**No cerrar integración HTML:** la disponibilidad de sala secreta `cruce_vetas` para LI en ver76 no fue verificada; los telegráficos/Control/defensa/salvado y adquisición real de equipo tampoco. No inventar gates ni reescribir `ROOMS.exits`. **V69 debe usarse solo como evidencia histórica de laboratorio, jamás como la ficha final del Eco.**

## 7. Autoridad humana V71 — Eco 84HP y Sombra LIII a revisión (2026-10-10)

**Eco del Caído, élite único LII: el autor RATIFICÓ COMO NUEVO DISEÑO 84 HP**, sustituyendo el HP51 de la ficha histórica. Conservar esa ficha vieja como artefacto trazable, pero NO usar HP51 como diseño vigente de Eco; sus habilidades V69 están aceptadas conceptualmente y sus números requieren paridad. Fuente: `experimentos/balance_nuevo/handoffs/V71_ECO84_SOMBRA_URGENTE_2026-10-10/DECISION_HUMANA_ECO_HP84_Y_REAPERTURA_SOMBRA.md` y campo `current_design_t0_override` de `CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json`.

**Sombra Ahogada del Estanque, élite único LIII:** reapertura de T0 expresamente autorizada. **Candidato V71** HP90, DEF1, veneno M11 sin cambios; nueva defensa reactiva de una sola vez **Espejo del Remanso**, absorción 16 después de sufrir en un golpe >=16 HP reales. En holdout independiente de 51.840 combates físicos 1v1 LIII PRE_AOE, el jugador ganó 58,11% ante la candidata, frente al 99,68% del M11 histórico. **La candidata Sombra todavía requiere ratificación numérica final humana e integración al runtime; no escribir READY ni modificar fuente histórica de modo silencioso.** Fuente: `experimentos/balance_nuevo/handoffs/V71_ECO84_SOMBRA_URGENTE_2026-10-10/DICTAMEN_REBALANCE_SOMBRA_V71_2026-10-10.md`.

**Conteo canónico sin cambios: 31 identidades.** Ambos siguen siendo monstruos únicos sin T1–T4 ni Mutantes. No se ha probado AOE multiblanco.

## 8. V72 — Sombra Ahogada LIII vuelve a balancearse, HP > 100 (10/10/2026)

**NUEVA AUTORIDAD DE DISEÑO, prevalece sobre la ficha candidata V71 de HP90:** el autor pidió expresamente que Sombra, élite único de LIII, tuviera más de 100 HP. Después de 228.960 peleas completas de screening y holdouts de distintas variantes, se **seleccionó en laboratorio HP110, DEF1, Velo de Ahogo cadencia 4 con veneno `1d2+2 ×2 pulsos`, y Espejo del Remanso que absorbe 8 puntos una sola vez tras recibir >=16 HP reales en un golpe**. Conserva PREC106, EVA20, TEN19, básico `1d2+7`.

El finalista se comprobó en **dos lotes independientes de 17.280 duelos** (34.560): victorias del jugador **50,611%** global (Fuego 62,645; Agua 50,579; Viento 56,207; Tierra 43,200; Metal 40,422). Entrada con LII mejor DEF: **48,672%**, LII evasivo **32,300%**; equipo LIII opcional/no regalado: **70,859%**. Esto es un **promedio de laboratorio PRE_AOE**, no cap por build ni paridad HTML. QA 405 pares de regresión E1, 0 diferencias, 0 timeouts. No se probaron Ultis legales ni Concordancias ON, ni AOE 2+ hostiles.

Fuente vigente: `experimentos/balance_nuevo/handoffs/V72_SOMBRA_HP110_BALANCE_LIII_2026-10-10/SOMBRA_T0_V72_HP110_CANDIDATO.json`; dictamen: `experimentos/balance_nuevo/handoffs/V72_SOMBRA_HP110_BALANCE_LIII_2026-10-10/DICTAMEN_REBALANCE_SOMBRA_V72_2026-10-10.md`. ZIP con runner, CSV, motor sellado y hashes en esta conversación. **La referencia V71 HP90 queda solo como antecedente superado**; el histórico T0 HP51 queda como historia verificable, no se sobreescribió el registro viejo. **No elevar el nuevo T0 a READY productivo sin cierre numérico humano/paridad de motor NEW/HTML**. Único: sin T1–T4/Mutantes.

El índice global continúa con **31 identidades** y el Eco del Caído conserva la decisión humana de **84 HP**; no introducir cambios laterales a Eco, normales LI/LII/LIII, Ultis ni guardianes AOE.
