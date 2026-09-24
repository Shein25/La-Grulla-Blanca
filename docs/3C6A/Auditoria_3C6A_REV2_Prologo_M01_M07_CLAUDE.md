# Auditoría externa independiente — 3C.6A REV2 (Prólogo + M01–M07)

| Campo | Valor |
|---|---|
| Agente auditor | Claude |
| Modelo/versión | Claude Sonnet 5 |
| Fecha | 2026-09-24 |
| Repositorio | https://github.com/Shein25/La-Grulla-Blanca |
| Rama auditada | `audit/3c6a-rev2` |
| HEAD informado por el solicitante | `e40046d869f2ed65e7ab56408c31c635b6730988` (no verificable por el auditor: `raw.githubusercontent.com` no expone el commit) |
| Baseline | `grulla-blanca_ver74.html` |
| SHA baseline | `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566` (declarado por el solicitante y por el informe 3C.5; el auditor no tuvo el HTML completo y **no recalculó el hash**) |
| Archivos auditados | `PAQUETE_AUDITORIA_3C6A_REV2.md`, `Reconciliacion_3C6A_Prologo_M01_M07_REV2.md`, `Matriz_Implementacion_3C6A_Prologo_M01_M07_REV2.json`, `Informe_Implementacion_3C5_ver74.md`, `EXTRACTOS_VER74_3C6A_PARA_CLAUDE.zip` (9 extractos con numeración de línea original) |
| Tipo de revisión | documental/técnica independiente |

**Alcance y límites.** Los dos REV2 y el informe 3C.5 se leyeron completos. De `ver74.html` sólo se dispuso de los nueve extractos (≈257 KB de 1,57 MB); las citas `ver74:NNNNN` remiten a esas líneas. Todo lo que los extractos no cubren figura en §0.2 como **NO VERIFICADO** y no se da por bueno. No se modificó ningún archivo, no se implementó código, no hubo commits ni merges.

**Autoridad aplicada:** decisiones humanas posteriores > REV2 > ver74 > REV1/históricos. Las decisiones que contradicen ver74 o fuentes históricas se marcan `OVERRIDE_HUMANO_VALIDO` y no cuentan como error.

---

## 0. Resumen ejecutivo

**Veredicto: `3C6A_REV2_REQUIERE_CORRECCIONES`** (sin fallo conceptual; ningún BLOQUEANTE).

- REV2 es **coherente con ver74 en lo estructural**: el schema 2 no necesita subir, no hace falta ninguna clave top-level nueva, `flags` es libre, `QUESTS`/`this.quests` ya existen, el enum de `conocimientoNPC` soporta lo que M07 escribe, y todas las rooms de las misiones existen con la topología esperada.
- Las correcciones son de **especificación** (11 puntos `CORRECCION_DOCUMENTAL`) y de **implementación nueva esperable** (11 `CAMBIO_NECESARIO_3C6`). Los tres que más importan:
  1. **Dos modelos de rango/afiliación** en paralelo (`flags.rango`/`estadoAfiliacion` de REV2 frente a `FACCIONES.rangos` derivados de mérito y `facciones.grulla_blanca.estado` en ver74) sin reconciliar (CD-01).
  2. **Gates sin punto de evaluación definido**: si LI→LII se evalúa sólo al consagrar y el jugador ya estaba en etapa 2 al cerrar M03, hay **soft-lock** (CD-02).
  3. **Contribución y mérito "por canales separados"** choca con el invariante `merito >= saldo` de `normalizarFacciones` y con el total de mérito de REV2, que está mal sumado: da **5 con incidente opcional**, no 4 (CD-05, CN-01).
- **Hay un aviso técnico crítico para el contrato:** `compruebaPuerta()` **ignora en silencio** cualquier token de `PUERTAS[n].logros` que no sea `"combate"` o `"comprension:N"` (`ver74:17144-17150`). Si el contrato sustituye el hard-gate de combate agregando tokens nuevos sin su handler, la puerta 2→3 **queda abierta** (fail-open) (CN-03).

### 0.1 Recuento de hallazgos

| Categoría | Cantidad |
|---|---|
| BLOQUEANTE | 0 |
| CORRECCION_DOCUMENTAL | 11 (CD-01…CD-11) |
| CAMBIO_NECESARIO_3C6 | 11 (CN-01…CN-11) |
| ENDURECIMIENTO_FUTURO | 8 (EF-01…EF-08) |
| EDITORIAL_NO_BLOQUEANTE | 5 (ED-01…ED-05) |
| OVERRIDE_HUMANO_VALIDO | 8 (OV-01…OV-08) |

### 0.2 NO VERIFICADO (no cubierto por los extractos)

1. Recálculo del SHA-256 y del HEAD.
2. `cmd_hablar`, `cmd_entregar`, `DESCS_NPC` y el cableado de diálogo (sólo se ve `gestionarMisionesNpc()` como stub que devuelve `""`, `ver74:18869`).
3. `recordarCriatura`, `describirCadaver`, `resolverCadaver`, el manejador de victoria (`ver74:16873`, `16946-16951`, sólo vistos por grep).
4. `mostrarConsagracion`, `HOJA` y textos que muestren el qi tras consagrar; cuerpo de `desbloquearProfesion` (`ver74:19074`, sólo la firma).
5. Dónde se obtiene `manual_piel` (ROOMS/tienda) y si `muneco_practica` está colocado en alguna room (las rooms M03 extraídas tienen `mobs: []`).
6. Distancias/rutas reales entre `puesto_valle`, `puerta`, `bosque_*`, `mercado_valle`, `granero_valle`, `sauces_*` (los extractos traen sólo las rooms puntuales y sus salidas inmediatas).
7. El test histórico que exigía `QUESTS={}` (no aparece en los extractos; véase EF-08).
8. Si otro contenido de ver74 depende de `player.etapa` (no se halló ninguno en los extractos, pero no se recorrió el archivo entero).

---

## 1. Coherencia MD ↔ JSON

**Coinciden íntegramente:** las 17 decisiones humanas (texto idéntico); los gates `PROLOGO_LI`, `LI_LII`, `LII_LIII`; para P y M01–M07: id, nombre, etapa, REQUIERE, activación, rooms/checkpoints, objetivos, cierre, PRODUCE, ABRE y recompensas; compañeros (prioridad, máx. 1 escena, géneros); pendientes; veredicto; fecha; `SAVE_SCHEMA_VERSION=2`.

**Divergencias concretas:**

| # | Divergencia | Categoría |
|---|---|---|
| D1 | M06: los cuatro tipos (`DESPLAZAMIENTO_FAUNA`, `ALTERACION_VEGETAL`, `ALTERACION_HIDRICA`, `PATRON_TERRITORIAL`) figuran **sólo en el JSON** (`misiones[M06].evidencias`); el MD da el evaluador sin nombrarlos. | CD-04 |
| D2 | El JSON define el valor `INSUFICIENTE_SOSPECHA_FUERTE` para 2 tipos; el MD/DHP_3C6_03 fijan un enum de 3 niveles. | CD-04 |
| D3 | `this.quests`: el JSON dice "activa/hecha; rumor/fallida sólo si se usan", el MD sólo "activa/hecha". **ver74 sí soporta `rumor` y `fallida`** (`activarMision`, `ver74:18838-18853`; categoría UI `rumores`), así que el JSON refleja mejor la realidad. | CD-09 |
| D4 | `arc1.estado=LIII_INVESTIGACION` y la sección "Estado de salida" existen sólo en uno de los dos archivos (valor de estado sólo en JSON; frontera de salida sólo en MD). Reglas de alcance de compañeros ("3C.6 sólo incorpora escenas LI/LII que intersecten P–M07", "posición 3C.5 es fuente de verdad") sólo en MD. | CD-10 |
| D5 | M04 usa las claves `merito_base` / `merito_incidente_opcional`; el resto usa `merito` (igual en ambos archivos). | CD-08 |

---

## 2. Baseline ver74 — verificación de infraestructura

| Requisito | Resultado | Evidencia |
|---|---|---|
| `SAVE_SCHEMA_VERSION === 2` | ✔ | `ver74:2197` |
| `QUESTS` existe | ✔ **vacío** (`const QUESTS = {}` con comentario "pendiente de progresión canónica P–M18") | `14199-14200` |
| `this.quests` | ✔ (`{}` en constructor y `nuevaPartida`) | `15780`, `15829` |
| `activarMision` / `completarMision` | ✔; `completarMision` exige estado `activa` y `q.listo(this)`, ejecuta `entregar`, marca `hecha`, calcula `recompensa`, autoguarda | `18838-18867` |
| `flags` | ✔, objeto libre | `15780`; validador `02397` |
| `conocimientoNPC` / `posicionNPC` + persistencia NPC v1 | ✔ (`npc_version:1`, 32 IDs, R1–R10, enum DESCONOCIDO/SOSPECHA/SABE/CONFIRMADO) | `2372-2393`, `16295-16305` |
| `VASO_ETAPA` | ✔ `{1:25, 2:45, 3:75, 4:110}` | `3110` |
| `PUERTAS` | ✔ `{2:null, 3:{pildoras:1, logros:["combate"]}, 4:{pildoras:2, logros:["comprension:6"]}}` | `3112-3116` |
| `pildora_consolidacion` | ✔ ítem `reliquia`, precio 8; servicio de facción (coste 8, mérito 20); botín de 4 mobs (0,2–0,35) | `6843`, `14508`, `7143/7170/7179/7194` |
| `TECNICAS.piel_cobre` | ✔ (mortal, tierra, guardia 3, coste 5, duración 2) + `manual_piel` | `4101`, `6863` |
| `MOBS.muneco_practica` | ✔ (`practica:true`, hp 14, sin botín) | `7133` |
| `profesiones.examen` y desbloqueo | ✔ `desbloqueada:false` al crear; `desbloquearProfesion(id)`; `observarCadaver`/`recolectarCadaver` devuelven "Enseñanza de Examen pendiente de implementación canónica 3C." si no está desbloqueada | `15936`, `19074`, `19194`, `19213` |
| Alojamientos usados | ✔ `dormitorio_externos`, `puesto_valle`, `bosque_refugio_patrulla`, `sauces_casa_huespedes` están en `ALOJAMIENTOS_329` y tienen `alojamiento` | `2278-2292`; rooms en extracto 07 |

**Se apoya directamente en infraestructura existente:** raíz como cadena `fuego|metal|agua`; `flags` para arc1/permisos/evidencia/one-shots; `this.quests` + `completarMision` (one-shot inherente: sólo actúa desde `activa`); `conocimientoNPC` (enum exacto); `desbloquearProfesion("examen")`; consumo de la píldora en CONSAGRAR (`20121-20126`); `compruebaPuerta()` como punto único de puertas; `gates.SECTA_INTERIOR` con cascada a `M12`/`ATAJO_ALA_*`; `visitadas` + Atlas para "conocido/visitado"; la rata como errante existente `rata_despensa`.

**Requiere implementación nueva:** las 8 definiciones de misión en `QUESTS`; API de anclaje/liberación de NPC; escritura monotónica de conocimiento; `otorgarMerito`; evidencia territorial; guardas locales del encuentro tutorial; diálogo NPC; gates de puerta nuevos; transiciones LI→LII y LII→LIII; hooks en CONSAGRAR; rediseño del flujo de raíz y del estado inicial; muñeco y bloqueo del manual.

---

## 3. Estado inicial

**Colisión confirmada** (`crearPersonaje`, `ver74:15908-15984`):

- `titulo: "aspirante aceptado"` (`15917`)
- `facciones.grulla_blanca.estado: "miembro"` (`15944`) y `normalizarFacciones` lo rellena a `"miembro"` si falta (`18899`, `18903`)
- `inventario: ["pocion","uniforme","espada_madera"]` con el comentario `PROVISIONAL_3C1 · REVISAR_EN_PROLOGO_M01` (`15950-15951`)
- `herboristeria.desbloqueada: true`, también marcada `PROVISIONAL_3C1 · REVISAR_EN_PROLOGO_M01` (`15937-15938`)
- `salida("[Fundación estructural 3C.1. Campaña y NPC pendientes…]")` (`15981`), texto provisional a retirar.

**¿Viable sin `SAVE_SCHEMA_VERSION=3`? Sí.** `validarSave329` sólo exige `titulo` string (`02430`), `facciones.*.estado` string (`02447`) y referencias de `inventario` a `ITEMS` (`02433`). Ninguna de las tres cosas cambia de forma. Los saves ver74 existentes seguirán validando (ver CD-03 sobre su semántica).

Cambios necesarios (CN-04): valores iniciales en `crearPersonaje`; retirar uniforme/espada del inventario inicial y entregarlos en `descansillo` con flag; ampliar la lista blanca de `cambiarEstadoFaccion` (`18927`: hoy `miembro/huesped/aliado/inactivo/expulsado`, no admite `pendiente_registro`/`admitido`/`aspirante`). `gastarContribucion` exige `estado === "miembro"` (`18973`), coherente con que no haya servicios antes de M03.

---

## 4. Raíz espiritual

- **RAICES** tiene exactamente tres entradas (`fuego`, `metal`, `agua`) con `tecnica` inicial (`palma`, `filo`, `latigo`) (`4653-4660`) → coincide con el "Fuego/Metal/Agua" de REV2. **Compatible.**
- **Formato persistido sin cambio:** `player.raiz` es string validado con `ref(RAICES, p.raiz)` (`02431`); `raiz_secundaria: null`. **No hace falta tocar el formato.**
- **Técnicas iniciales:** se derivan de `RAICES[raiz].tecnica` (`15957-15959`). Compatible mientras la raíz esté resuelta antes de construir `p`.
- **Advertencia de flujo (CN-05):** hoy la selección ocurre en `creacionRaiz` **antes** de `crearPersonaje` y de que exista `this.player`, con una sola pregunta y mapa directo (`15890-15905`). Un `player` con `raiz` nula/ausente **falla la validación** y `escribirSlot` rechaza guardar (`16290`). El diagnóstico de tres elecciones + reacción final debe resolverse **antes de `crearPersonaje`** (o usar una raíz provisional no guardable), porque `ataque`, `defensa`, `tecnica` y `tecnicas_preparadas` salen de ella.
- **Reasignación:** si el diagnóstico corre en el flujo de creación, es imposible repetirlo al volver a `patio_raices` (su `scenery.piedra` es sólo texto). Si se hiciera interactivo dentro de la room, haría falta flag de una sola vez.
- **Desempate:** con tres elecciones sobre tres elementos sólo hay empate en 1-1-1; la reacción ante la Piedra lo resuelve de forma determinista (sin RNG). No inventé las tres preguntas (pendiente editorial).

---

## 5. CONSAGRAR y qi

**Comportamiento actual** (`cmd_meditar`, `ver74:20087-20180`): con `p.qi >= p.qi_max` y puerta cumplida → consume `pildoras` de `PUERTAS[siguiente]` (`20121-20126`), **`p.qi = Math.max(0, p.qi - vasoAnterior)` (`20130`)**, `etapa+1`, `qi_max = VASO_ETAPA[etapa]`, `max_hp+4`, `ataque+1`, `hp=60%`.

El cambio (DHP_3C6_01) es **una sola línea**: eliminar la resta de `20130`. El resultado es 25/25 → consagrar → 25/45, compatible con:

- `qi_max`: se recalcula igual (`20132`).
- Comprobación de vaso lleno (`20100`): tras consagrar `qi < qi_max`, así que no dispara otra consagración inmediata.
- `progresoFundacion()`: sólo mira etapa, puerta y comprensión (`17158-17178`).
- Técnicas que gastan qi (`15048`, `15078`, `15436`), `entregarRecompensa` (`17194`), DORMIR (`19825`): todos usan `min(qi_max, …)`, sin suponer qi 0.
- Save/load: `qi` sólo se valida como número ≥ 0 (`02432`); no se relaciona con `qi_max`.

**Supuestos del motor que esperan qi 0 tras consagrar:** en los extractos, **el único es la propia línea `20130`**. Los tests históricos fijan sus estados de forma explícita (`ver74:25692`, `25759` (`etapa=2; qi=0`), `25880`, `25909`), de modo que no dependen de la resta; **no se pudo comprobar** si la UI de `mostrarConsagracion`/HOJA imprime "qi 0/…" (NO VERIFICADO).

**Efectos laterales que el contrato debe declarar:**

1. **Pacing:** el qi acumulado necesario para llegar a etapa 4 baja de 25+45+75 = 145 a 75 (sin contar gasto en técnicas). Es una decisión humana válida (OV-01), pero las pruebas `balance v8` deberán revisarse (CN-02).
2. **`player.qi >= 45` (LII→LIII) es casi trivial:** DORMIR devuelve `ceil(qi_max·0.5)` = 23 (`19825`), así que desde 25 basta un descanso en un alojamiento para llegar a 45. La condición no protege nada; es coherente con REV2, pero conviene declararlo (ED-05).

---

## 6. Gate LI→LII

Condición REV2: `etapa>=2 ∧ rango==DISCIPULO_EXTERNO ∧ primerServicioFormal ∧ evaluacionCirculacion==SUPERADA`.

- **Redundancia:** `rango`, `primerServicioFormal` (M02) y `evaluacionCirculacion` (M03) se fijan al cerrar M02/M03; en la práctica el gate es "M03 HECHA ∧ etapa≥2".
- **Carrera consagración ↔ misión (CD-02, soft-lock):** `PUERTAS[2] = null` → CONSAGRAR 1→2 no tiene requisitos (`3113`) y el jugador puede llegar a etapa 2 **antes** de M03 (incluso en el Prólogo, con ≈6-8 meditaciones). Si el gate sólo se evalúa en CONSAGRAR, un jugador que ya es etapa 2 cierra M03 y **no hay nada que dispare la transición**; M04 exige `arc1.estado=LII_TERRITORIO` y CONSAGRAR 2→3 exige M04+M05 → **deadlock**. REV2 debe declarar que el gate se evalúa **(a)** al cerrar M03 y **(b)** al consagrar 1→2, y que también se reevalúa al cargar (idempotente).
- **M03 sigue teniendo sentido** si el jugador ya está en etapa 2: aporta rango, Piel de Cobre y la evaluación; sólo cambia cuándo se dispara la transición.
- **One-shot:** debe protegerse con flag propio (REV2 no nombra la clave) **y** con monotonía del estado (`LI → LII` sólo si el actual es `LI_INTEGRACION`). Con ambas, la transición no puede repetirse.
- **Contenido LII prematuro:** en los extractos no hay contenido condicionado por `arc1.estado` (no existe) ni por `etapa` (salvo `PUERTAS`). Las misiones LII se abren únicamente por `arc1.estado`. Sin hallazgos negativos, pero no se recorrió el archivo entero (§0.2, punto 8).

---

## 7. Gate LII→LIII

**Encaje con `PUERTAS[3]`:** hoy `{pildoras:1, logros:["combate"]}`. `compruebaPuerta(3)` cuenta píldoras en inventario (`17139-17142`) y valida `logros` (`17143-17150`); `cmd_meditar` la usa como único punto de decisión (`20112`) y consume la píldora **después** (`20121-20126`). REV2 se apoya en ese punto sin duplicar lógica si se sustituye `logros:["combate"]` por los requisitos nuevos **dentro de `compruebaPuerta`**.

Riesgos de implementación:

1. **Fail-open** (`17144-17150`): tokens desconocidos no producen `faltan`. Todo token nuevo necesita handler explícito (CN-03).
2. **Comparación de `evidenciaTerritorial`:** debe ser **ordinal** (índice en `[INSUFICIENTE, SUFICIENTE, CONCLUYENTE]`). Una comparación de strings (`"CONCLUYENTE" >= "SUFICIENTE"`) da falso (`C < S`). Con comparación ordinal, **CONCLUYENTE sí satisface todos los gates `>=SUFICIENTE`** (CD-04).
3. **`servicioTerritorial`** debe ser derivado (`M04==hecha ∧ M05==hecha`), no un flag almacenado, para que no diverja.
4. **Caminos para saltarse M04–M07:** el único código que incrementa `etapa` visto en los extractos es `cmd_meditar` (`20131`) y pasa por `compruebaPuerta`. M06/M07 quedan cubiertos de forma indirecta porque `evidenciaTerritorial` y `informeFronteraAceptado` sólo los fijan esas misiones. No se halló atajo, pero otras vías que asignen `etapa` (p. ej. `20533`, `qi_max=140` para Fundación) están fuera de LianQi 2→3.
5. **Píldora:** se consume con `PUERTAS[3].pildoras` en CONSAGRAR (`20121-20126`), como REV2 prevé. Una píldora puede provenir del botín (`7143`, `7170`, `7179`, `7194`) o del servicio de facción; que haya "otra" píldora no rompe el gate, sólo hace que la de M05 no sea única en el mundo.
6. **`SECTA_INTERIOR`** sólo se pone a `true` en la transición (nueva). `normalizarEstadoGates` (`2298-2303`) y `validarSave329` (`02402`) ya obligan a `M12=false` y `ATAJO_ALA_*=false` mientras `SECTA_INTERIOR=false`. **Invariante ya protegido por código.**

---

## 8. Prólogo

Rooms verificadas (existen, área `acceso`, salidas recíprocas): `patio_raices` →N `descansillo` →N `sendero_pinos` →N `camino` →N `puerta` →N `registro`; `mirador_niebla` (E) y `patio_practica` (O) son ramas sin salida desde `descansillo`. `ver74:7586-7743`. Supervivientes exigidos por `auditarMundo329` (`2341`).

- **Equipamiento en `descansillo`:** la room existe y su `scenery.bancos` habla de "ajustar el equipo" (encaja). Cambio necesario: sacar `uniforme` y `espada_madera` del inventario inicial (CN-04) y entregar con flag `equipoInicialEntregado`. Nota: el origen *callejero* recibe `cuchillo_hueso` "en lugar de la espada" (`15971`); REV2 no dice cómo se entrega ese caso (ED-04).
- **Tao Ming en `registro`:** `registro ∉ NPC_DEF.tao_ming.posicion_valida` (territorio `oficina_servicios`, `patio_servicios`, `deposito_comun`; `ver74:5303-5365`). Sólo es posible con **anclaje**, y hoy **no existe API de anclar/liberar** (`puedeMoverNPC` sólo rechaza anclados, `16778-16785`). CN-06.
- **Guardia y ayudante genéricos:** deben ser texto/escenario, **no** entradas de `NPC_DEF`. Agregar NPC nuevos cambiaría el conjunto exacto de IDs que `validarSave329` exige (`keys(posiciones, ids)`, `02381`) y rompería saves. Además Gao Shun ya existe como "Guardia de la Puerta Roja" (ED-03).
- **Idempotencia de raíz y registro:** raíz OK si se resuelve antes de crear el personaje (CN-05); registro requiere flag `REGISTRO_INICIAL_COMPLETADO` + estado de quest.
- **No revelar R1–R10:** ningún extracto muestra UI de `conocimientoNPC`; `DESCS_NPC` está vacío y `EXAMINAR` NPC imprime sólo nombre y rol (`19859-19863`).
- **Sin gate físico:** nada impide al jugador ir de `registro` a `sala_jade` sin hablar con Tao Ming (no hay gate en el Prólogo). Las misiones deben evaluar por estado (`visitadas`, flags) y no sólo por eventos de entrada (EF-06).

---

## 9. M01

Ruta y recíprocas verificadas una a una: `registro`→N `sala_jade`→N `patio`→O `patio_cabanas`→O `corredor_cabanas`→O `dormitorio_externos`; retornos S/S/E/E/E coinciden. **Topología real: idéntica a la de REV2.**

- `corredor_cabanas` tiene además salida S a `lavadero_externos`; que sea "sólo tránsito" es intención narrativa, no propiedad del motor.
- **Madre Wen:** `sala_inicial = patio_cabanas`; territorio `patio_cabanas`, `comedor_externos`, `corredor_cabanas`, `sala_comun_externos`. Aparece en `patio_cabanas` **sin anclaje** (`5235-5302`). ✔ (su territorio incluye el corredor, no `dormitorio_externos`, lo que encaja).
- **`dormitorio_externos`:** existe, está en `ALOJAMIENTOS_329`, tiene `alojamiento{inicio,purifica:true}`.
- **Visita física antes de marcar conocido:** `entrarSala` hace `visitadas.add(pos)` y `recordarAtlas()` (`16701-16703`); alcanza con comprobar `visitadas`. Nota: **en ver74 no existe "cama asignada"**: DORMIR funciona en cualquier `alojamiento` sin condición (`19820-19842`). La asignación es puramente narrativa.
- **`SECTA_EXTERIOR_BASE`:** debe vivir sólo en `flags`. **No** debe agregarse a `GATES_329` (`validarSave329` exige exactamente esas claves en `gates`, `02400`).
- **Tao Ming** (activación de M01 "en `registro`"): requiere anclaje (véase §8). M01 y M02 son sus anclajes documentados (`anclajes_documentados: ["M01","M02"]`).

---

## 10. M02 — Rata tutorial

**Descubrimiento clave:** la "rata de la despensa" **ya es un errante**: `rata_despensa` (`mobId: rata_qi`, territorio `deposito_comun`+`tablon_encargos`, origen `deposito_comun`; `ver74:3690-3700`). `despensa` no es una room. `deposito_comun` tiene `mobs: []`. Por tanto **no hace falta un mob nuevo ni tocar el número de errantes**.

**¿Se puede implementar localmente?** Sí, con un envoltorio de misión, sin cambiar la semántica global:

| Requisito REV2 | Mecanismo local propuesto | Verificación |
|---|---|---|
| Sin alterar la semántica global de errantes | Tabla `ENCUENTROS_TUTORIAL = {rata_despensa: {mision:"M02", …}}` consultada en pocos puntos; el motor sigue siendo genérico | ✔ (`16628-16652`) |
| Número exacto de errantes | Se reutiliza `rata_despensa`; no se agrega ni quita ningún errante | ✔ el validador exige cantidad e identidades (`02408-02409`) |
| Save validation | `muertoHasta = Number.MAX_SAFE_INTEGER` es finito y pasa `num(...)` (`02412`); `errantes[].sala/desde` ya validados | ✔ |
| No reaparece tras M02 | Con `muertoHasta` gigante, `actualizarErrante` nunca lo revive (`16619-16625`); `moverErrante` ni lo mueve (`16634`) | ✔ |
| No contaminar `HALLAZGOS_CADAVER` | Marcar el cadáver con `tutorial:true` (el validador **no** exige un conjunto cerrado de claves en cadáveres, `02415-02418`) y ramificar temprano en `observarCadaver`/`recolectarCadaver` | Requiere guardas locales (CN-07) |
| Sin recursos duplicados | Con muerte permanente, el botín (`pocion` 20 %) sólo cae una vez; sin EXTRAER no hay `grasa_qi_roida` | ✔ |
| Sin Atlas/bestiario/registro/familiaridad | `cmd_examinar` llama a `recordarCriatura(mob, true)` para cualquier mob vivo (`19851`), y `observarCadaver` incrementa `descubrimientos[mob].observaciones` (`19202-19203`) | **Requiere guardas** en esos puntos, keyed a `erranteId==="rata_despensa"` |
| Cadáver recuperable hasta aprender Examen | Los cadáveres duran `DURACION_CADAVER = 6` pulsos (`3669`, `16873`); hay que **extender `desapareceEn`** (número finito grande) mientras dure el tutorial y liberarlo al terminar | CN-07 |

**Lo que sí falta en REV2 (CD-06):** (a) el orden real de los objetivos es inconsistente: "obtener información del cadáver" figura **antes** de "aprender Examen con Chen Bo", pero sin Examen desbloqueado el cadáver no puede investigarse (`19194`, `19213`); (b) no se nombra qué NPC da M02 (`Tao Ming` es el candidato: territorio `oficina_servicios`); (c) la regla "tras morir/cerrar M02 no reaparece" es ambigua: si el cadáver no se fija, y la rata ya no reaparece, el jugador queda sin el cadáver que necesita (soft-lock, ver §20).

**Efecto lateral cosmético (EF-04):** con `muertoHasta > 0` permanente, `entrarSala` pone `_huboMobsEnCooldown = true` (`16688-16689`) y las dos rooms del territorio mostrarán para siempre "…lo que fuera que rondaba se movió hace poco".

**Ninguna modificación global de 3C.4 hace falta.**

---

## 11. M03

- **Bloquear el manual antes de M03 sin destruirlo:** `aprenderManual` (`20070-20083`) enseña cualquier técnica sin gate de misión. Una guarda local `if (tid==="piel_cobre" && !flags.piel_cobre_habilitada) return [[…],false]` lo bloquea sin tocar el ítem. Tras M03 el jugador ya conoce la técnica y `aprenderManual` responde "Ya conoces esa técnica" (`20078`) **sin consumir** el manual. En ver74 **no existe mecánica de "práctica/maestría por manual"**, así que el manual queda inerte, no "sirviendo para maestría" (habría que diseñarlo; EF/CD-07).
- **Dónde está el manual:** NO VERIFICADO (§0.2). Precio 12 sugiere tienda.
- **Idempotencia de aprender Piel de Cobre:** si el jugador ya aprendió por manual (antes de la guarda o por otra vía), el paso de Shen Baojun debe usar `tid in tecnicas` y `TECNICA_PIEL_COBRE_APRENDIDA` no debe depender de que el evento lo haya generado el NPC, o M03 se atasca (CN-08).
- **Condiciones básicas "room sin hostiles vivos + sin combate activo":** se apoyan en `this.vivos` (`hp>0`) y `this.combate`. **Interacción con el muñeco:** `muneco_practica` es un mob (`practica:true`); si está en la misma room que la activación de Shen Baojun o de la evaluación, cuenta como hostil vivo y `cmd_meditar` responde "Con algo moviéndose en la sala, la quietud no llega" (`20093-20095`). El muñeco debe estar en **otra room** que la del inicio y la evaluación, o el predicado debe excluir mobs `practica`. Colocación viable: `patio_marcial` (scenery `postes`, `armarios`) con inicio en `sala_formas` (`Shen Baojun` inicia allí) y evaluación en `patio_respiracion`.
- **Evaluación por meditación/estabilización:** **REV2 no la define** (sólo "superar evaluación de circulación"). `cmd_meditar` no tiene hook. Hay que decidir criterio y punto de enganche (CD-07, CN-08).
- **Repetición sin duplicar promoción:** `completarMision` sólo actúa desde `activa` (`18857`); con estado `hecha` y flag `evaluacionCirculacion` no puede repetirse.
- **NPC de cierre:** el `NPC_DEF` documenta a Qiao Ren "M03 (cierre de misión, ANCLADA en `pabellon_disciplina`)"; REV2 incluye `pabellon_disciplina` en las rooms de M03 pero no nombra quién promueve (CD-07).

---

## 12. M04

Rooms verificadas: `puesto_valle` (alojamiento ✔, salidas E `valle_explanada`, S `patio_puesto_valle`), `puerta`, `bosque_senda_patrulla` (O `bosque_puesto_marcas`, S `bosque_refugio_patrulla`), `bosque_refugio_patrulla` (alojamiento ✔; N/O/S).

- **Territorios/anclajes 3C.5:** Jiang Rui `sala_inicial = puesto_valle` ✔ (activación sin anclaje). Gao Shun tiene `puerta` en `posicion_valida` (`casa_guardia`, `deposito_comun`, `puerta`, `registro`…) y **anclaje documentado** "M04 (ANCLADO en puerta_roja/puerta)": funciona **con** anclaje (su posición inicial es `casa_guardia`).
- **Rutas físicas:** NO VERIFICADO. Los extractos sólo traen adyacencias inmediatas; no se puede confirmar la distancia `puesto_valle`→`puerta`→`bosque_senda_patrulla`. El auditor de mundo garantiza 1 componente y que estas áreas no están bloqueadas por gates (`2337-2340` lista sólo `primera_ala`, `alturas`, `archivos`, `formaciones`, `secta_interior`, `mantenimiento`, `nucleo` como bloqueadas).
- **Dificultad ambiental (no soft-lock):** `bosque_puesto_marcas` pertenece al territorio del errante `serpiente_bambu` (`3702-3712`) y `bosque_quebrada_niebla` (adyacente al refugio) al de `avispa_exploradora` (`3714-3725`). El "incidente de fauna" ocurre de forma natural, pero **no es determinista** (CD-08 debe definir su disparo).
- **Jiang Rui puede volver al puesto:** sólo mediante liberación con reubicación (CN-06). Si se libera un anclaje dejando `sala` fuera de `posicion_valida`, el save deja de validar (`02387`).
- **`PATRULLA_TERRITORIAL` no abre gates físicos:** correcto mientras no se agregue a `GATES_329`.

---

## 13. M05

Rooms verificadas: `oficina_logistica` (S `patio_produccion`, E `cochera_carros`; Duan Shibo la tiene como `sala_inicial`, sin anclaje), `mercado_valle`, `granero_valle`, `sauces_plaza` (O `sauces_camino_valle`, N `sauces_casa_huespedes`, S `sauces_pozo`, E `sauces_casa_comunal`), `sauces_casa_comunal` (Xu An `sala_inicial`, territorio `sauces_casa_comunal`+`sauces_plaza`), `sauces_casa_huespedes` (alojamiento ✔).

- **Territorio:** Duan Shibo (`oficina_logistica`, `patio_produccion`, `cochera_carros`) **no** cubre el valle; sólo asigna la misión desde su oficina, como dice REV2. ✔ Xu An ✔.
- **Ruta cardinal única:** REV2 **no exige** un orden, pero tampoco dice si los 7 checkpoints son obligatorios, en qué orden o cuántos alcanzan (CD-08). Con `mercado_valle` (adyacente a `encrucijada_valle`/`valle_desvio_carretero`) y `granero_valle` (a `terrazas_norte/sur`) no contiguos entre sí, un conjunto de checkpoints por estado (`visitadas`) es la forma robusta.
- **Píldora exactamente una vez:** garantía combinada de `completarMision` (one-shot) + flag `PILDORA_CONSOLIDACION_OTORGADA` dentro de `entregar` (para que un fallo intermedio no duplique al reintentar). En ver74 `entregarRecompensa` **no maneja ítems** (`17191-17204`); se hace en `entregar`/`recompensa` de la quest.
- **`sauces_casa_huespedes` conocido:** se conoce al visitarla (Atlas). Es checkpoint de M05, así que queda coherente. `reconocimientoSauces=HUESPED` es un flag (Sauces no es una facción de `FACCIONES`, que sólo contiene `grulla_blanca`).

---

## 14. M06 — evidencia

- **Determinismo / monotonía / idempotencia:** el evaluador se define como función del **conjunto** de tipos distintos (`|tipos|`: 1→INSUFICIENTE, 2→INSUFICIENTE+sospecha, 3→SUFICIENTE, 4→CONCLUYENTE); repetir no suma, nunca baja, y es idempotente. ✔ Requiere persistir el conjunto en `flags` (p. ej. `flags.evidenciaTerritorial.tipos`), libre en el validador.
- **Sin tocar respawns/ecología 3C.4:** ✔ a condición de **no** derivar las observaciones de posiciones/estados de errantes (dependen de RNG: `PROB_MOVIMIENTO_ERRANTE=0.28`). Deben salir de fuentes estáticas: `scenery` + EXAMINAR.
- **Observaciones desde scenery/EXAMINAR:** `cmd_examinar` devuelve `scenery[texto]` sin efectos (`19870-19873`); hace falta una tabla externa `(room, clave_scenery) → tipo` y un hook justo antes del `return esc` (CN-10). No se modifican los `ROOMS` ni sus `exits`.
- **CONCLUYENTE satisface los gates `>=SUFICIENTE`:** sólo con comparación ordinal (§7).
- **Riesgo (EF-07):** M06 cierra al alcanzar SUFICIENTE; REV2 no dice si el cuarto tipo se sigue registrando después (para qué sirve CONCLUYENTE) ni si las observaciones previas a la activación cuentan. Si se cuentan y el nivel ya es ≥SUFICIENTE cuando M06 se activa, `listo()` debe evaluarse **por estado**, no por evento de transición, o M06 se atasca.

---

## 15. M07

- **Compatibilidad con el enum:** ✔ `CONFIRMADO` y `SABE` ∈ `{DESCONOCIDO, SOSPECHA, SABE, CONFIRMADO}` (`02380`). `PARCIAL` **no** está en el enum: el validador lo rechazaría, lo que protege la separación (§16).
- **Estados iniciales (`NPC_DEF.conocimiento_inicial.R1`):** Jiang Rui, Qiao Ren, He Zhen, Ren Bo y Su Lian están todos en `SOSPECHA`; las escrituras de M07 son **ascensos válidos** (SOSPECHA→SABE/CONFIRMADO).
- **Participantes:** Qiao Ren tiene `pabellon_disciplina` como `sala_inicial` (sin anclaje). Jiang Rui **no** (territorio `puesto_valle`, `valle_explanada`, `patio_puesto_valle`): necesita anclaje en `pabellon_disciplina`. Sus anclajes documentados hablan de "Cruce Patrullas → Sala Informes"; REV2 lo reemplaza por decisión humana (OV-07).
- **Anclaje reversible:** `puedeMoverNPC` rechaza mover anclados (`16781`); el validador exige que sin anclaje `sala ∈ posicion_valida` (`02387`). Liberar sin reubicar deja un save inválido. Se necesita `liberarAnclaje(id, salaValida)` atómico (CN-06). La reubicación es un salto: hacerla fuera de la vista del jugador.
- **He Zhen sin teletransporte:** ✔ Recibe conocimiento por escritura directa; no requiere presencia. Coherente con 3C.5: "no se implementó propagación de conocimiento".
- **Comprensión +1 one-shot:** inherente a `completarMision` (`recompensa`); `entregarRecompensa` suma `p.comprension` directamente (`17195`).

---

## 16. R1 del jugador vs. conocimiento NPC

Separación **correcta** en REV2: `arc1.revelaciones.R1 ∈ {PARCIAL, CONFIRMADO}` (M06/M07) y `conocimientoNPC[npc].R1 ∈ {DESCONOCIDO, SOSPECHA, SABE, CONFIRMADO}` (M07); "PARCIAL nunca se escribe en `conocimientoNPC`" está explícito.

**Único punto de mezcla (CD-04):** M06 PRODUCE `conocimiento.anomaliasTerritoriales=SOSPECHA_FUERTE`. Esa clave no pertenece a ninguno de los almacenes definidos (`QUESTS`/`this.quests`/`flags`/`player`/`conocimientoNPC`), y `SOSPECHA_FUERTE` no es un valor del enum NPC. Debe reubicarse en `flags` con nombre y dominio propios, o eliminarse.

---

## 17. Recompensas

**Aritmética (CD-05):**

| Concepto | REV2 | Suma real |
|---|---|---|
| Contribución | 12 | 1+0+2+3+2+4 = **12** ✔ |
| Mérito | "4" con incidente opcional | 1 (M04 opc.) + 1 (M06) + 3 (M07) = **5** con incidente; **4 sin él** ✘ |
| Comprensión | 1 | **1** ✔ |
| Píldora | 1 | **1** ✔ |

**`otorgarContribucion` (`18954-18968`) suma simultáneamente a `saldo` y `merito`.** Además `normalizarFacciones` fuerza `merito = max(saldo, merito)` (`18905`) y una prueba histórica fija ese comportamiento (`ver74:25581-25588`). Por tanto:

- "canales separados" **no puede** significar que la contribución deje de sumar mérito (`merito` volvería a subirse a `saldo` en cada normalización).
- Lectura compatible: `otorgarContribucion` no cambia; se agrega `otorgarMerito(n)` que suma sólo a `merito`. El mérito de REV2 sería **adicional** al que ya aporta la contribución, y el invariante `merito >= saldo` se mantiene. Es un **CAMBIO_NECESARIO_3C6** (CN-01), no una contradicción de diseño, siempre que REV2 lo declare.

**Contraste con progresión de facción** (`ver74:14497-14511`):

- Rangos por mérito acumulado: `aspirante` 0, `servidor_externo` 8, `discipulo_acreditado` 20, `merito_interno` 40.
- Servicios: `pocion` (coste 3, mérito 0), `claridad` (4, 8), `consolidacion` (8, 20).
- Con la lectura compatible, tras M06 el mérito acumulado es ≥ 8 (→ `servidor_externo`, y aparecerá `✦ Rango de facción: Servidor externo` por `entregarRecompensa`, `17200`); al final de M07, ≈ 16–17: **no alcanza 20**. Consecuencias: no hay compra de píldora por servicio en LII (mitigación de soft-lock inexistente, EF-01) y el mensaje de rango de facción convive con el `rango` institucional de REV2 (CD-01).

---

## 18. Persistencia

| Almacén | Rol REV2 | ¿Cabe en ver74? |
|---|---|---|
| `QUESTS` | definición P–M07 | ✔ es `const` de código, hoy `{}` |
| `this.quests` | activa / hecha | ✔; el validador exige que cada clave exista en `QUESTS` y valor `string` (`02398`) → cargar un save con P/M0x **exige** que estén definidas |
| `flags` | arc1, rango, afiliación, permisos, evidencia, one-shots | ✔ objeto libre, **sin validación de contenido** (`02397`) |
| `player` | recursos | ✔ sin conjunto cerrado de claves salvo las verificadas |
| `conocimientoNPC` | R1–R10 | ✔ |

- **Schema 2 sin cambios:** el validador exige exactamente `required` (+ `npc_version`, `posicionNPC`, `conocimientoNPC`) (`02372-02374`); ninguna clave top-level nueva es necesaria ✔.
- **Cargas legacy:** ver74 acepta saves sin `npc_version` (forma LEGACY) y con NPC v1. Un save ver74 **carga** en 3C.6, pero REV2 no define su estado semántico (CD-03).
- **Saves corruptos:** rechazo atómico ya implementado (`16308-16349`); la debilidad es que **`flags` no se valida** y `quests[k]` acepta cualquier string (EF-03): un `flags.evidenciaTerritorial` alterado pasaría. Se debe sanear al cargar.
- **Test `QUESTS={}`:** no aparece en los extractos (véase EF-08). Si existe, **debe actualizarse** al implementar 3C.6: `QUESTS` está declarado "pendiente de progresión canónica P–M18" (`14199`), no como invariante permanente. Además, `auditarTextosActivos3C1R` prohíbe cadenas como `this.quests["ratas"]` y `activarMision("jade")` (`25558-25559`): los IDs nuevos (`P`, `M01…M07`) no chocan, pero el texto nuevo deberá pasar ese auditor.

---

## 19. Compañeros / DHP_17

- **Compatibilidad estructural:** ✔ una sola `posicionNPC[id].sala` por NPC → sin duplicación física; `afinidad` está indexada por ID de NPC y validada contra `NOMBRES_NPC` (`02434`); movilidad y territorios 3C.5 son datos estáticos.
- **Prioridad CRISIS > MISIÓN > PERSONAL > AMBIENTAL / una escena por entrada:** no hay código que arbitre; es contador de sesión, sin persistencia necesaria.
- **Punto débil (EF-02):** el anclaje es un único slot `{room,hasta}` (el validador exige exactamente esas dos claves, `02388`), **sin "propietario"**. Una escena social y una misión pueden anclar al mismo NPC y una pisa a la otra. Se resuelve guardando el propietario en `flags` (p. ej. `flags.anclajeNPC[id]="M07"`), sin tocar la forma del anclaje ni el schema.
- No se desarrolló el arco de los seis compañeros (fuera de alcance).

---

## 20. Soft-locks

| # | Caso | SOFTLOCK | Causa | Recuperación necesaria | Severidad |
|---|---|---|---|---|---|
| 1 | Consagró antes de M03 (etapa 2 en LI) | **SÍ, si no se evalúa el gate al cerrar M03** | `PUERTAS[2]=null`; gate sólo en CONSAGRAR (CD-02) | Evaluar al cerrar M03, al consagrar 1→2 y al cargar (idempotente) | **Alta** |
| 2 | Perdió/gastó la píldora antes del gate | **SÍ (raro)** | `cmd_soltar` la tira sin protección (`19921-19947`); el objeto desaparece a los 500 turnos (`3666`). No se usa en otro sitio (`tipo: reliquia`). Vías de reposición: botín RNG y servicio (mérito 20, inalcanzable en LII) | Reemisión controlada desde `PILDORA_CONSOLIDACION_OTORGADA=true` sin píldora en inventario, o marcar el ítem no tirable (EF-01) | Media |
| 3 | La rata tutorial desapareció | **SÍ si se implementa "no reaparece" sin fijar el cadáver**; no si se fija (`desapareceEn` extendido) | Cadáver dura 6 pulsos y la rata ya no vuelve (CD-06/CN-07) | Cadáver fijado hasta terminar M02; o "información" sin cadáver | **Alta** |
| 3b | Rata muerta **antes** de M02 | No | Reaparece normalmente (`RESPAWN_COOLDOWN_DEFAULT=10`); muerte permanente sólo dentro del tutorial | — | — |
| 4 | Chen Bo no disponible | No (bajo) | Sin scheduler (3C.5), sólo se mueve por acción explícita; territorio `sala_anatomica`/`corredor_medicina`/`archivo_clinico`. Riesgo sólo si otra escena lo ancla | La misión debe localizarlo en su territorio o reanclarlo | Baja |
| 5 | Jiang Rui en otra ruta | No | Territorio de 3 rooms adyacentes; M04 se activa donde esté dentro de `puesto_valle`/`valle_explanada`/`patio_puesto_valle`. Si queda anclado en `pabellon_disciplina` tras M07, no bloquea nada pero viola "anclaje reversible" | `liberarAnclaje` con reubicación | Baja |
| 6 | Evidencia llegó a CONCLUYENTE | No | Todos los gates usan `>=SUFICIENTE`; el riesgo es comparar por igualdad o por string | Comparación ordinal | Media (impl.) |
| 7 | Informe ya entregado | No | `completarMision` no re-ejecuta desde `hecha` | — | — |
| 8 | Recompensa parcialmente aplicada | Riesgo bajo | `entregar` corre antes de marcar `hecha`; si lanzara excepción tras dar la píldora, el reintento la duplicaría; `recompensa` corre tras marcar `hecha` (sin rollback) | Flags de una sola vez dentro de `entregar`; recompensas en un solo bloque síncrono | Baja-media |
| 9 | M04/M05 en orden inesperado | No | M05 `REQUIERE M04=HECHA` y `servicioTerritorial` derivado. Cuidado con checkpoints visitados **antes** de activar (contar por estado o por línea base) | — | Baja |
| 10 | Save cargado en medio de una transición | **Posible** | Si se guarda entre `etapa=3`/consumo de píldora y `SECTA_INTERIOR=true`, queda etapa 3 sin gate y sin píldora para repetirlo. En ver74 `cmd_meditar` no llama a `autoguardar()` en la rama de consagración, pero `mostrarConsagracion`/`registrarActividadReposo` no se pudieron revisar | Aplicar todo en un bloque síncrono sin `autoguardar` intermedio **y** reconciliar al cargar (etapa≥3 ⇒ estado LIII/gate) | Media |
| 11 | NPC anclado "desaparece" tras recarga | No | `posicionNPC` se guarda y valida exacto (`02382-02389`); `deserializar` restaura el estado (`16341`). Sólo falla si se libera sin reubicar (save inválido) | `liberarAnclaje` atómico | Media (impl.) |
| 12 | Escena social ocupa al NPC de la misión | **SÍ, potencial** | Slot único de anclaje sin dueño (EF-02) | Propietario en `flags`, prioridad CRISIS>MISIÓN>PERSONAL | Media |
| 13 | Aprendió Piel de Cobre por manual antes de M03 | **SÍ si M03 depende del evento del NPC** | `TECNICA_PIEL_COBRE_APRENDIDA` sin comprobar `tid in tecnicas` | Guarda del manual y `listo()` por estado (CN-08) | Media |

---

## 21. Idempotencia

| Elemento | Mecanismo garantizado / requerido | Estado |
|---|---|---|
| Raíz | Resolver antes de `crearPersonaje`; `raiz` no se reescribe | ✔ con CN-05 |
| Equipo del Prólogo | Flag `equipoInicialEntregado` | Requiere implementación |
| `NOMBRE_INSCRITO` | Flag/estado de quest | Requiere implementación |
| Cama | No existe asignación en ver74; sin riesgo | ✔ |
| Contribución | `completarMision` one-shot | ✔ |
| Mérito | Ídem; el +1 opcional de M04 necesita flag propio (CD-08) | Requiere implementación |
| Píldora | Quest one-shot + `PILDORA_CONSOLIDACION_OTORGADA` | ✔ con flag |
| Promoción de rango | Derivada de estado de quest/flags | ✔ (una vez resuelto CD-01) |
| Piel de Cobre | `tid in tecnicas` | ✔ en `aprenderManual`; el NPC debe hacer lo mismo |
| Examen | `desbloquearProfesion("examen")`; el cuerpo de la función no se pudo ver | NO VERIFICADO |
| Comprensión +1 (M07) | Recompensa dentro de `completarMision` | ✔ |
| Conocimiento NPC | Escritura monotónica (sólo si sube en el orden del enum) | Requiere `elevarConocimientoNPC` |
| Transición LI→LII / LII→LIII | Flag + estado monotónico + reconciliación al cargar | Requiere implementación (CD-02) |

---

## 22. Invariantes que 3C.6 no puede romper

| Invariante | Estado en ver74 | Riesgo de 3C.6 |
|---|---|---|
| 329 rooms · 17 áreas · 787 salidas dirigidas · 0 reciprocidades rotas · 0 aisladas · 1 componente | Fijadas como constantes en `auditarMundo329` (`02338`), más `alcanzables físicas = 329` e `iniciales = 185` y 9 distribuciones bloqueadas; el informe 3C.5 reporta PASS (329 salas, 17 áreas, 787 = 786 internas + 1 externa). *No se ejecutó el auditor.* | REV2 no toca `ROOMS`. Ubicar el muñeco (`ROOMS[x].mobs`) **no** cambia exits. La tabla de evidencia debe ser externa a `ROOMS`. |
| `SECTA_INTERIOR=false ⇒ M12=false ⇒ ATAJO_ALA_*=false` | Aplicada por `normalizarEstadoGates` (`02301`) **y** por `validarSave329` (`02402`) | La transición a LIII pone `SECTA_INTERIOR=true`; `M12` y `ATAJO_*` siguen `false` |
| No tocar `ROOMS.exits` | ✔ REV2 no lo requiere | — |
| No romper Atlas | El Atlas se actualiza sólo al observar (`16791`); anclar/mover NPC no lo toca | Guardas del encuentro tutorial para no escribir bestiario/Atlas (CN-07) |
| No modificar globalmente 3C.4 | ✔ con envoltorio local sobre `rata_despensa` | Guardas de 3-4 puntos, todas condicionales |
| Sin tiempo diegético | ✔ REV2 no lo usa; `hasta` del anclaje es libre y no tiene consumidor | Definir su semántica sin introducir calendario |
| No subir schema | ✔ Viable (§18) | — |

---

## 23. Catálogo de hallazgos

### CORRECCION_DOCUMENTAL

| ID | Hallazgo | Dónde corregir |
|---|---|---|
| **CD-01** | **Dos modelos de afiliación/rango.** REV2 guarda `rango` (`ASPIRANTE`, `DISCIPULO_EXTERNO`) y `estadoAfiliacion` (`PENDIENTE_REGISTRO`, `ADMITIDO`, `MIEMBRO`) en `flags`; ver74 deriva el rango de facción por mérito (`aspirante`, `servidor_externo`, `discipulo_acreditado`, `merito_interno`) y guarda el estado en `player.facciones.grulla_blanca.estado` (minúsculas). `DISCIPULO_EXTERNO` ≠ `discipulo_acreditado`. | MD: DHP_3C6_15/16, "Persistencia", "Estado de salida". JSON: `persistencia.flags`, `misiones[M01].produce`, `misiones[M03].produce`. Declarar cuál es fuente de verdad (recomendado: `estadoAfiliacion` ↔ `facciones.…estado`; `rango` como "cargo institucional" distinto del rango por mérito). |
| **CD-02** | Sin punto de evaluación ni claves one-shot de los gates → soft-lock #1. | MD y JSON `gates.LI_LII` / `LII_LIII`: agregar "evaluación en cierre de M03, en CONSAGRAR 1→2 y al cargar", y nombrar flags `transicionLILII` / `transicionLIILIII` (nombres a criterio, pero explícitos). |
| **CD-03** | Nada define qué es un save ver74 existente (título "aspirante aceptado", miembro, sin `arc1`). | MD: nueva DHP o sección "Saves legacy". Decidir: ¿P y M01–M03 derivadas como HECHAS?, ¿`rango`/estado a qué valores?, ¿raíz conservada?, ¿se repite el Prólogo? |
| **CD-04** | Evidencia: tipos no nombrados en el MD; `INSUFICIENTE_SOSPECHA_FUERTE` frente al enum de 3 niveles; `conocimiento.anomaliasTerritoriales=SOSPECHA_FUERTE` sin almacén ni enum; falta exigir comparación ordinal y decir dónde se guarda el conjunto de tipos. | MD "M06" y JSON `misiones[M06].evaluador` / `.produce`. |
| **CD-05** | Total de mérito = **5** con incidente (4 sin él); no está declarado si contribución sigue sumando mérito. | MD "Balance de recompensas" (línea de totales). JSON: agregar `balance.total`. Declarar la lectura de CN-01. |
| **CD-06** | M02: orden de objetivos inconsistente (cadáver antes que Examen), NPC de activación no nombrado, la regla "morir/cerrar" ambigua, rata = errante `rata_despensa` (no hay room "despensa"). | MD/JSON `misiones[M02]`: `objetivos`, `activacion`, `rooms`, `reglas`. |
| **CD-07** | M03: mecanismo de evaluación no definido, ubicación del muñeco, criterio de "practicar", NPC de cierre (Qiao Ren) y predicado de hostiles frente al muñeco. | MD/JSON `misiones[M03]`. |
| **CD-08** | M04: incidente opcional sin objetivo/evento/flag one-shot; claves de recompensa distintas al resto. M05: no dice si los 7 checkpoints son obligatorios ni en qué orden; "registrar modificación del circuito" sin definición. | MD/JSON `misiones[M04]`, `misiones[M05]`. |
| **CD-09** | `this.quests`: alinear el MD con el JSON (rumor/fallida existen en ver74). | MD "Persistencia". |
| **CD-10** | Frontera de salida y valor `LIII_INVESTIGACION` sólo en un archivo cada uno; alcance de compañeros sólo en MD. | JSON: agregar `estado_salida`. MD: nombrar `LIII_INVESTIGACION`. |
| **CD-11** | M07: participantes, anclaje de Jiang Rui y copia a He Zhen sólo figuran en la DHP_3C6_12; "elegir grado de certeza" no tiene efecto declarado. | JSON `misiones[M07]`: `participantes`, `anclajes`, `efecto_certeza` (o eliminarlo). |

### CAMBIO_NECESARIO_3C6 (implementación nueva esperable, no contradicción)

| ID | Cambio | Puntos de ver74 |
|---|---|---|
| CN-01 | `otorgarMerito(n)` separado; mantener `merito ≥ saldo`; ajustar prueba `25581-25588` | `18954-18968`, `18905`, `17191-17204` |
| CN-02 | Quitar `p.qi = Math.max(0, p.qi - vasoAnterior)`; revisar `balance v8` y tests con qi 0 explícito | `20130`, `25692`, `25759`, `25880`, `25909` |
| CN-03 | Sustituir `logros:["combate"]` de `PUERTAS[3]` por requisitos M04/M05/evidencia/informe **con handler en `compruebaPuerta`** (fail-open hoy); hook post-consagrar de LII→LIII (`SECTA_INTERIOR=true`, `arc1.estado`) | `3114`, `17143-17150`, `20112-20142` |
| CN-04 | Estado inicial (título, estado de afiliación, inventario) y lista blanca de `cambiarEstadoFaccion`; retirar texto "Fundación estructural 3C.1"; resolver `herboristeria` provisional | `15908-15984`, `18927` |
| CN-05 | Diagnóstico de raíz (3 elecciones + reacción) **antes** de `crearPersonaje` | `15890-15959` |
| CN-06 | API de anclaje/liberación con reubicación atómica, y `elevarConocimientoNPC` monotónico | `16768-16792`, `02382-02389` |
| CN-07 | Guardas locales del encuentro tutorial (`recordarCriatura`, `observarCadaver`, `recolectarCadaver`, `desapareceEn`, `muertoHasta`) | `19851`, `19190-19268`, `16873`, `16946-16951` |
| CN-08 | Guarda del manual, muñeco (rooms), evaluación por meditación, enseñanza idempotente | `20070-20083`, `7133`, `20093` |
| CN-09 | Definiciones de `QUESTS` P–M07 (`listo`, `entregar`, `recompensa`), plumbing de diálogo NPC (`gestionarMisionesNpc` es un stub), actualización de pruebas | `14199-14200`, `18869-18871` |
| CN-10 | Tabla y hook de evidencia territorial en `cmd_examinar` (scenery), fuera de `ROOMS` | `19870-19873` |
| CN-11 | Reconciliación al cargar (`etapa`↔`arc1.estado`) e idempotencia de transiciones | `16308-16349` |

### ENDURECIMIENTO_FUTURO

- **EF-01** Reemisión/protección de la píldora (tirarla la pierde tras 500 turnos).
- **EF-02** Propietario del anclaje (flags) para arbitrar misión vs escena social.
- **EF-03** Sanear `flags` y estados de `quests` al cargar (el validador no los examina).
- **EF-04** Mensaje "se movió hace poco" perpetuo con `muertoHasta` permanente.
- **EF-05** Reubicar al NPC liberado fuera de la vista del jugador.
- **EF-06** Misiones basadas en estado (`visitadas`), no sólo en eventos, dado que no hay gates físicos en el Prólogo.
- **EF-07** Definir qué hace CONCLUYENTE y si se registra evidencia posterior a M06 o previa a su activación.
- **EF-08** Localizar el test que exigía `QUESTS={}` (no aparece en los extractos) y actualizarlo.

### EDITORIAL_NO_BLOQUEANTE

- **ED-01** `qi=45` (DHP_3C6_05) frente a `qi>=45` (gates).
- **ED-02** `REGISTRO_INICIAL_COMPLETADO` (P) y `NOMBRE_INSCRITO` (M01): ambos con Tao Ming en `registro`; separar los eventos.
- **ED-03** La "guardia genérica" del Prólogo y Gao Shun (Guardia de la Puerta Roja) ocupan el mismo rol en `puerta`.
- **ED-04** Origen *callejero* (`cuchillo_hueso`) frente a "uniforme y espada en `descansillo`".
- **ED-05** `qi>=45` se cumple con un solo descanso (`19825`); la condición es decorativa.

### OVERRIDE_HUMANO_VALIDO

| ID | Decisión | Contradice |
|---|---|---|
| OV-01 | DHP_3C6_01 (CONSAGRAR no resta qi) | `ver74:20130` |
| OV-02 | DHP_3C6_05 (se elimina el hard-gate de combate) | `PUERTAS[3].logros` (`3114`) |
| OV-03 | DHP_3C6_06 (raíz determinista por 3 elecciones) | Selección directa (`15890-15905`) |
| OV-04 | DHP_3C6_15 (Aspirante/PENDIENTE_REGISTRO, uniforme/espada en `descansillo`) | Estado inicial (`15917`, `15944`, `15950`) |
| OV-05 | DHP_3C6_08 (rata tutorial sin respawn/Atlas/EXTRAER) | Semántica 3C.4 (aplicada sólo localmente) |
| OV-06 | DHP_3C6_09 (Piel de Cobre con Shen Baojun en M03) | `anclajes_documentados` de Shen Baojun ("Paso de Nube") |
| OV-07 | DHP_3C6_12 (M07 en `pabellon_disciplina`) | Anclajes documentados de Jiang Rui ("Cruce Patrullas → Sala Informes") |
| OV-08 | DHP_3C6_10 (asignaciones y checkpoints de M04/M05) | Anclajes documentados de Duan Shibo (M13/M16) |

---

## 24. Correcciones exactas requeridas antes del contrato

**En `Reconciliacion_3C6A_Prologo_M01_M07_REV2.md`:**

1. *Balance de recompensas* → cambiar "4 Mérito" por "5 Mérito con incidente opcional (4 sin él)"; aclarar que `otorgarContribucion` sigue sumando a mérito y que el mérito listado es adicional (CD-05).
2. *Gates reconciliados* → añadir puntos de evaluación y nombres de flags one-shot (CD-02).
3. *Persistencia* → definir la relación `rango`/`estadoAfiliacion` con `facciones.grulla_blanca` (CD-01); alinear `this.quests` con `rumor/fallida` (CD-09).
4. *M02, M03, M04, M05, M06, M07* → completar según CD-04 a CD-08 y CD-11.
5. Nueva sección "Saves legacy" (CD-03).
6. Nombrar `LIII_INVESTIGACION` (CD-10).

**En `Matriz_Implementacion_3C6A_Prologo_M01_M07_REV2.json`:**

1. `misiones[M06].evaluador`: sustituir `"INSUFICIENTE_SOSPECHA_FUERTE"` por `INSUFICIENTE` + flag de sospecha (CD-04); reubicar o eliminar `produce[conocimiento.anomaliasTerritoriales]`.
2. `misiones[M04].recompensas`: normalizar claves (`merito`) y añadir un `incidente_opcional` con evento y flag (CD-08).
3. `gates.LI_LII` / `LII_LIII`: agregar `evaluacion_en` y `flag_one_shot`.
4. Agregar `estado_salida` y `balance.total` (mérito 5/4).
5. `misiones[M07]`: añadir `participantes` y `anclajes`; resolver "elegir grado de certeza".

**No** hace falta modificar ningún archivo de código ni subir `SAVE_SCHEMA_VERSION`.

---

3C6A_REV2_REQUIERE_CORRECCIONES