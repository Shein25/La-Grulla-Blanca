# V70 — Cierre del balance numérico de Eco del Caído (T0 ratificado, LianQi II)

**Decisión humana de este frente:** validar las habilidades de Eco sobre su T0 histórico y equipo realmente admisible de LianQi II, y cerrar el balance antes del frente AOE.

**Estado:** `NUMERIC_LAB_CLOSED / SELECTED_DESIGN_PARAMETERS / NOT_RUNTIME_READY`. Documento de parámetros obligatorios: [`V70_ECO_CIERRE_NUMERICO_CANDIDATO.json`](V70_ECO_CIERRE_NUMERICO_CANDIDATO.json).

## 1. Corrección definitiva del conflicto V69/E8

El T0 con autoridad humana en commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35` es: `eco_caido` único LII, **HP51, Precisión102, EVA24, DEF1, Tenacidad24, Control0, básico 1d3+6**. El antiguo candidato E8 del frente PRE-A08 (84HP, Precisión96, EVA18, etc.) **NO se usa más para determinar el equilibrio V70**. El T0 antiguo se conserva inalterado; no se editó `monster_arc1_registry.json`.

V69 de 192.000 peleas con 84HP **NO era el balance del Eco ratificado**. En V70 se repitieron los tres brazos relevantes sobre los 51HP correctos y se calibraron SOLO las habilidades nuevas.

## 2. Equipamiento auditado y etapa

Todas las pruebas usan `LianQi_II`, **2 PT**, técnicas ofensiva y defensiva normales; sin AOE, Ultis, objetos LIII ni ventajas de LIV. Solo se cargaron equipos `min_stage<=LII`:

| Cohorte | Composición / condición | Admisibilidad real |
|---|---|---|
| `P_GUARANTEED` | Espada de entrenamiento de madera + uniforme gris aspirante | Catálogo dice entregados en prólogo |
| `M03_GUARANTEED` | Los dos anteriores + Fajín del Discípulo Externo | Solo después de completar M03 |
| `M04_PARTIAL_OPTIONAL` | Conjunto opcional esperado LII de **M04 y M05 mezclados** | NO garantizado; el nombre técnico NO significa solo M04 |
| `ENTRY_LII_MAX_DEFENSE` | 11 objetos, incluida Sobretúnica de patrulla DEF+2 | Opcionales M04/M05/M06 |
| `ENTRY_LII_MAX_EVASION` | 11 objetos, incluida túnica de Sauces | Opcionales M04/M05/M06 |

El motor usa un catálogo de EQUIPO con adquisición todavía provisional, por lo que lo garantizado tiene autoridad de **diseño**, no certificación del inventario actual de `grulla-blanca_ver76.html`. Verificar el momento de adquisición antes de activar el combate: en ver74 podía llegarse a la habitación secreta `cruce_vetas` desde LI sin cruzar gate, pero **ver76 no fue inspeccionado con resultado concluyente**. No inventar puertas, NPCs, objetos ni alterar `ROOMS.exits`.

## 3. Tres habilidades definitivas de diseño numérico V70

- **Veta Resentida**: primer turno en el que Eco sigue vivo a ≤60% HP y recibe **al menos 10 HP reales de daño directo** del jugador, activa **12 puntos de absorción una sola vez**. No cura, no suma DEF.
- **Lamento del Caído**: telegráfico cada 4 rondas, intento directo `1d2+3` y, si conecta, DOT espiritual `1d2+3` durante 2 pulsos; DOT evita DEF pero respeta absorción; el origen no se duplica. Defender con técnica pagada durante el aviso reduce a un pulso con ×0,5; impactar por ≥18% HPmax de Eco durante el aviso o Control válido que cancele su acción lo interrumpe.
- **Reverberación del Agravio**: al perder ≥25% HPmax por golpe real mientras está vivo (**mínimo 13 HP**), prepara una réplica anunciada para su siguiente acción voluntaria. Paquete espiritual `1d2+8 + floor(min(30,5×max(0, daño_real_del_golpe−7)))`, atraviesa DEF pero respeta absorción. Máximo dos veces y CD3 rondas, cancelable por defensa pagada/Control que suprima su acción. La réplica depende **del impacto real recibido**, sin identificar raíces ni ítems.

Todos estos efectos son **kit T0 local único**, no T1–T4 ni Mutantes persistentes.

## 4. Estadísticas reproducidas — fuentes E1 físicas

En V70 se hicieron **192.000 peleas** útiles de cierre: original sin nuevas habilidades 48.000, V69 sin recalibrar sobre 51HP 48.000 y configuración V70 seleccionada en **dos holdouts independientes de 48.000 cada uno**, ambos con 0 timeouts y nuevas semillas. Cada holdout V70 cruza 5 raíces, 3 builds legales, 5 equipos, 4 políticas y 160 réplicas por celda.

| Loadout | Eco base 51HP sin habilidades | V69 en 51HP | V70 seleccionado |
|---|---:|---:|---:|
| Equipo prólogo garantizado | 66,93% | 13,58% | **28,89%** |
| Equipo tras M03 garantizado | 68,04% | 14,91% | **29,72%** |
| Equipo medio opcional M04+M05 | 91,33% | 37,76% | **62,14%** |
| Máximo LII defensivo opcional | 97,85% | 54,23% | **67,13%** |
| Máximo LII evasivo opcional | 93,27% | 41,82% | **59,10%** |

**V70 global: 49,39% de victorias del jugador** sobre 96.000 peleas de la candidata final.

Por raíz: Fuego **42,15%**, Agua **61,20%**, Tierra **50,77%**, Metal **47,31%**, Viento **45,54%**.

Por política: atacar siempre **36,02%**; defender en apertura **41,25%**; protegerse al ver Lamento **51,65%**; responder a Lamento y Reverberación **68,66%**.

**El límite del 70% se cumple para los promedios global, de raíz, de equipo y de política**. El 95% Wilson de `READ_ALL_CUES` fue 68,07–69,25%. Esto NO implica cap universal para cada combinación cruzada: Agua + mejor equipo DEF tiene ≈82,19%; si además reacciona óptimamente, ≈95,94%. No se manipula RNG para impedir que un jugador preparado gane.

## 5. QA: PASS

- **96.000/96.000** combates en holdouts finales V70, **0 timeouts**, +48k base y +48k V69-original para comparativas.
- **1.050 pares exactos** `fight_once` físico E1 versus puente base para HP51, equipo/raíz/build/política con **0 diferencias**.
- **600 replays exactos** del CSV V70 desde el ejecutor portátil.
- Escudo una vez; réplicas ≤2; DOT no aparece sin Lamento conectado; pruebas no detectaron duplicación ni recargos de energía por habilidad gratuita.
- ZIP con **44 archivos**, CRC PASS, manifiesto SHA-256 de **43 archivos** verificado, SHA-256 ZIP `861cb5a612c1b05f290c7f6a7d2a484e8c53a7d591955abba9ff8e32849e7542`.

Artefacto reproducible: `GRULLA_V70_ECO_T0_51_CIERRE_BALANCE_LII_2026-10-10.zip`, disponible en el chat que produjo V70. Contiene fuentes, scripts, CSV de 192.000 combates, hashes, configuración y dictamen extenso. El ZIP binario **no fue subido a Git**; solo sus resultados y referencia/hashes, por integridad y tamaño.

## 6. Qué se cierra y qué queda pendiente

**CERRADO como balance numérico experimental del kit:** T0 congelado HP51 + tres habilidades nuevas parametrizadas en V70, combate **LianQi II**, comparación por equipo de adquisición obligatoria/optativa, dos holdouts independientes. No repetir pantallas previas sin nueva hipótesis causal.

**NO está integrado ni probado en el HTML**: autorización temporal del encuentro secreto si un LI puede llegar a `cruce_vetas`, visibilidad de avisos, defensas efectivamente aprendidas, DOT/absorción/control por eventos NEW, SAVE/LOAD, derrota única por partida, Concordancias, acceso de equipo. Mantener **bloqueo de integración** hasta verificar; no alterar rutas para que pase la prueba.

**Guardias:** no `main`, no merge, no HTML, no `ROOMS.exits`, no cambios de T0, no misiones/items/NPC o economía nuevos. No usar T1–T4 en élite único. El próximo frente AOE se trata por separado.
