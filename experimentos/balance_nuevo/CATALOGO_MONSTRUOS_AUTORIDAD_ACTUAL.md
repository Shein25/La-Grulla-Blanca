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
