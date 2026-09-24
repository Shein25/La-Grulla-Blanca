# Auditoría de cierre — 3C.6A REV3 (Prólogo + M01–M07)

| Campo | Valor |
|---|---|
| Agente auditor | Claude |
| Modelo/versión | Claude Sonnet 5 |
| Fecha | 2026-09-24 |
| Repositorio | https://github.com/Shein25/La-Grulla-Blanca |
| Rama | `audit/3c6a-rev3` |
| HEAD | esperado `06dcba2f18616ca9e3c7e928a59cefc18bfef101` — **no verificable** (`raw.githubusercontent.com` no expone el commit) |
| Baseline | `grulla-blanca_ver74.html` |
| SHA baseline | `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566` (declarado; **no recalculado**) |
| REV3 MD | `docs/3C6A/Reconciliacion_3C6A_Prologo_M01_M07_REV3.md` (SHA declarado en el paquete: `6c77cebb…b6b6`; no recalculado) |
| REV3 JSON | `docs/3C6A/Matriz_Implementacion_3C6A_Prologo_M01_M07_REV3.json` (SHA declarado: `a21ce88a…350d`; no recalculado) |
| Auditoría previa usada | `Auditoria_3C6A_REV2_Prologo_M01_M07_CLAUDE.md` |
| Tipo | auditoría de cierre documental/técnica |

**Límites de esta auditoría.** Se leyeron completos el MD, el JSON, el índice del paquete y mi auditoría de REV2. Los extractos de ver74 `01`–`09` **no pudieron abrirse** (la herramienta sólo abre URLs que aparecen literalmente en la conversación; sólo el `00_INDICE.md` estaba disponible). Toda afirmación sobre ver74 se apoya en las citas de línea de mi auditoría de REV2 (`ver74:NNNNN`); lo que esa auditoría no cubrió figura como **NO VERIFICADO**. No se modificó nada, no hubo commits ni merges.

---

## 0. Resumen

- **No hay BLOQUEANTE ni fallo conceptual.** REV3 es sólida: el modelo de tres dominios de afiliación/rango, el evaluador central de gates con puntos de evaluación explícitos, la economía desacoplada (aritmética correcta), la migración de saves y M02/M06/M07 están bien resueltos.
- **MD y JSON no se contradicen**; sólo hay omisiones unilaterales (§2).
- **8 de 11 hallazgos de REV2 quedan RESUELTOS; 3 PARCIALMENTE_RESUELTOS** (CD-03, CD-07, CD-08), por huecos concretos en la migración y en los criterios de M03/M05/M04.
- **Hallazgos nuevos relevantes** (todos corregibles en un addendum documental, sin tocar decisiones humanas):
  1. Ciclo de vida de anclajes no especificado para Tao Ming (P/M01→M02) y Gao Shun (M04): como está escrito, M02 podría no activarse en `oficina_servicios` (N-02).
  2. La migración omite `equipoInicialEntregado` y demás one-shots de P–M03: riesgo de **duplicar uniforme/arma** al entrar en `descansillo` (N-01).
  3. M06 sólo garantiza cierre state-based; la **activación** no lo es (N-05).
  4. Reemisión de la píldora sin tope: posible bucle de dinero (vender → recargar → reemitir) (N-07).
  5. M03: el muñeco puede destruirse antes de la respuesta defensiva; "MEDITAR con éxito" no cubre vaso lleno (N-03).

---

## 1. Los once hallazgos de REV2

| ID | Estado | Motivo |
|---|---|---|
| CD-01 | **RESUELTO** | `estadoAfiliacion` / `rangoInstitucional` / `facciones.grulla_blanca` + `rangoFaccion()` separados; gates usan `rangoInstitucional`; `rangoFaccion()` deriva sólo de mérito; M03 lleva la facción a `miembro`. MD y JSON coinciden. Queda un endurecimiento (N-11). |
| CD-02 | **RESUELTO** | `reconciliarProgresionArc1()` idempotente y fail-closed; LI→LII se evalúa al cerrar M03, al consagrar 1→2 y al cargar/migrar; one-shots nombrados (`transicionLILIIHecha`, `transicionLIILIIIHecha`). Los siete escenarios de §4 quedan cubiertos. |
| CD-03 | **PARCIALMENTE_RESUELTO** | La migración está definida (P–M03 hechas, raíz/inventario/stats/economía preservados, M04–M07 se juegan). Faltan: `equipoInicialEntregado` y demás one-shots de P–M03, la regla si `gates.SECTA_INTERIOR` ya venía `true`, y el discriminante "ausente" vs "inválido" de `flags.arc1` (N-01). |
| CD-04 | **RESUELTO** | Cuatro tipos nombrados en MD y JSON; enum de 3 niveles; `sospechaFuerte` booleano; comparador ordinal explícito; conjunto persistido sin duplicados; desaparece `conocimiento.anomaliasTerritoriales`; tabla externa a `ROOMS`. |
| CD-05 | **RESUELTO** | Aritmética correcta: Contribución 1+2+3+2+4 = **12**; Mérito 1 (M06) + 3 (M07) = **4**, **5** con incidente M04; Comprensión 1; Píldora 1. MD, JSON y recompensas por misión coinciden. Consecuencias de implementación en §3 (N-10). |
| CD-06 | **RESUELTO** | Secuencia coherente: cadáver fijado *antes* de ir con Chen Bo, sin errante nuevo, sin loot duplicado, sin Atlas/bestiario/familiaridad, recreación única sin loot. Tao Ming nombrado. Ver §5.2. |
| CD-07 | **PARCIALMENTE_RESUELTO** | Definidos: Shen Baojun, muñeco como instancia de misión (no en `ROOMS`), evaluación por MEDITAR, Qiao Ren, manual sin maestría. Pero "respuesta defensiva válida" y "MEDITAR con éxito" tienen huecos que reintroducen soft-locks (N-03). |
| CD-08 | **PARCIALMENTE_RESUELTO** | Incidente M04 determinista con evento/flag one-shot (bien); checklist de siete rooms eliminado, OR mercado/granero real (bien). Persisten: el "registro" de M05 sigue sin actuador definido y el punto de otorgamiento del +1 Mérito es ambiguo (N-04, N-06). |
| CD-09 | **RESUELTO** | MD y JSON declaran `activa/hecha` para P–M07, `rumor/fallida` sólo compatibilidad, `BLOQUEADA/DISPONIBLE` derivados. |
| CD-10 | **RESUELTO** | `estado_salida`, `LIII_INVESTIGACION` y reglas de compañeros están en ambos archivos con contenido equivalente. |
| CD-11 | **RESUELTO** | Participantes, anclaje propietario M07 de Jiang Rui, escritura directa a He Zhen/Ren Bo/Su Lian, efecto de la formulación (sólo diálogo + persistencia). Matices en N-08. |

---

## 2. Coherencia MD ↔ JSON

Comparados sección por sección: **no hay contradicciones de contenido**. Coinciden modelo de afiliación/rango, gates, one-shots, migración, economía, P–M07, compañeros, persistencia, estado de salida y requisitos técnicos. Divergencias exactas (todas omisiones unilaterales):

| # | Divergencia | Dónde falta |
|---|---|---|
| D1 | `player.facciones.grulla_blanca.estado` **comienza `inactivo`** | Sólo MD (§R3_01); JSON lista el enum pero no el valor inicial |
| D2 | LII→LIII: lista de puntos de evaluación (cierres M04/M05/M06/M07, CONSAGRAR 2→3, carga) y "presentación ceremonial one-shot" | Sólo JSON; el MD sólo describe la ejecución tras CONSAGRAR y la espera M04–M07 para legacy |
| D3 | M02: JSON fusiona "investigar `deposito_comun` y resolver la rata" en un objetivo y lista `rooms`; MD separa los pasos 2 y 3 | Formulación distinta, contenido compatible |
| D4 | M03: el paso 2 (muñeco) tiene id `M03_PRACTICA_MUNECO_COMPLETADA` | Sólo JSON |
| D5 | M06: `sospechaFuerte=true` también para 3 y 4 tipos; `areas` de la misión | Sólo JSON |
| D6 | Migración: `NOMBRE_INSCRITO=true`, marcar `dormitorio_externos` conocido/visitado, `transicionLILIIHecha` true/false por etapa | Sólo JSON |
| D7 | Invariantes numéricos del mundo (329/17/787/…) y "sin tiempo diegético" | Sólo JSON (MD: "no modificar `ROOMS.exits`", "no tiempo diegético") |

Ninguna cambia un gate ni una recompensa. Se recomienda igualarlas en el addendum (§9).

---

## 3. Afiliación, rangos y economía

**Afiliación/rango.** Sin dos fuentes de verdad *conflictivas*: `rangoInstitucional` gobierna gates (LI→LII, requisito de M04); `rangoFaccion()` sólo cuenta para servicios y mensajes económicos. `estadoAfiliacion=MIEMBRO` y `facciones.grulla_blanca.estado=miembro` cambian en el mismo evento (M03) y por tanto **codifican lo mismo dos veces**; no hay contradicción hoy, pero puede divergir (N-11). Ningún gate consulta `estadoAfiliacion`.

**Economía (`otorgarContribucion` → saldo; `otorgarMerito` → mérito; sin `merito>=saldo`).**

| Punto | Evaluación |
|---|---|
| `gastarContribucion` | Coherente: sólo baja saldo. Exige `estado==="miembro"` (`ver74:18973`), lo que encaja con "sin servicios antes de M03". |
| `rangoFaccion()` | Coherente (sólo mérito). Consecuencia: en partida nueva el mérito máximo P–M07 es 5 (<8), así que el rango económico **nunca sale de `aspirante`** mientras `rangoInstitucional` es `DISCIPULO_EXTERNO`. Dos "rangos" visibles con nombres distintos (`aspirante`/`servidor_externo`… vs `ASPIRANTE`/`DISCIPULO_EXTERNO`): la UI debe rotularlos distinto (EDITORIAL). |
| Servicios | `claridad` exige mérito 8 y `consolidacion` 20 (`ver74:14497-14511`): con REV3 quedan **inalcanzables en LII para partida nueva** (antes, el acoplamiento los habría acercado). Decisión humana válida; declararla (ENDURECIMIENTO). |
| Save/load | Saves ver74 conservan `saldo`/`mérito` (cumplen `merito>=saldo`). Partidas nuevas pueden tener `merito<saldo`. **NO VERIFICADO** que `validarSave329` o alguna prueba impongan `merito>=saldo` fuera de `normalizarFacciones`; el contrato debe comprobarlo (N-10). |
| Tests | El requisito técnico 9 cubre "merito>=saldo" (`ver74:25581-25588`). Correcto. |
| Historial de facción | **NO VERIFICADO** (sin extractos). Si el historial registra contribución+mérito en una sola entrada, hay que separarlas. |
| Otros llamadores de `otorgarContribucion` | REV3 no los enumera. Todo llamador legacy que contaba con el mérito implícito cambia de comportamiento en silencio (N-10). |
| Contribución con `estado=inactivo` | M02 paga +1 Contribución **antes** de que la facción pase a `miembro` (M03). Si `otorgarContribucion` o `normalizarFacciones` exigen `miembro`, la recompensa se pierde o falla. **NO VERIFICADO** (N-10). |

Aritmética confirmada: **12 / 4 (5 con incidente) / 1 / 1**. No se usa el acoplamiento saldo→mérito como requisito canónico.

---

## 4. Gates y soft-locks (`reconciliarProgresionArc1()`)

| Escenario | Resultado |
|---|---|
| Consagrar antes de M03 | OK. CONSAGRAR 1→2 evalúa LI→LII, falla por rango, no es error; al cerrar M03 se vuelve a evaluar y dispara. |
| Cerrar M03 ya en etapa 2 | OK (evaluación al cierre). |
| Cargar etapa 2 | OK (evaluación al cargar). |
| Save legacy etapa ≥3 | OK: `cultivoLIIIPreexistente`; transición LII→LIII espera M04–M07 y se dispara al cerrar M07 vía reconciliación (`etapa>=3` + M04 + M05 + evidencia≥SUFICIENTE + informe). |
| M07 cerrada sin qi | OK: el qi sólo cuenta en CONSAGRAR; en legacy `etapa>=3` la reconciliación dispara sin qi. |
| CONCLUYENTE | OK con comparador ordinal; sin efecto en gate/recompensa. |
| Requisito desconocido en `compruebaPuerta` | OK en intención ("bloquea o produce error"). Preferir "bloquea y reporta": un error lanzado tras consumir la píldora dejaría estado parcial (`ver74:20121-20126`). |
| Transición repetida | OK: one-shot + estado monotónico. |
| Save a mitad de transición | OK: tras `etapa>=3` la protección de la píldora se apaga (`etapa<3`) y la reconciliación completa la transición al cargar. Requiere bloque síncrono sin autoguardado intermedio (ya indicado en REV2). |
| `SECTA_INTERIOR=false ⇒ M12=false ⇒ ATAJO_ALA_*=false` | Se mantiene hasta la transición oficial y ya lo imponen `normalizarEstadoGates` (`ver74:2298-2303`) y `validarSave329` (`ver74:02402`). |

**Casos abiertos nuevos:** N-03 (vaso lleno pre-M03), N-05 (activación de M06), N-02 (M02 sin Tao Ming disponible).

---

## 5. Migración de saves ver74

Trigger: schema 2 sin `flags.arc1`. Se preserva raíz/origen/stats/inventario/técnicas/economía/posición/gates/NPC; Examen y Piel de Cobre se completan si faltan; no se repite Prólogo ni diagnóstico.

| Caso | Estado resultante | Riesgos |
|---|---|---|
| **A. etapa 1** | `LI_INTEGRACION`, `transicionLILIIHecha=false`; debe consagrar (PUERTAS[2]=null → sin requisitos) | Sin soft-lock. |
| **B. etapa 2** | `LII_TERRITORIO`, `transicionLILIIHecha=true` (se omite la ceremonia, intencional) | Sin soft-lock. |
| **C. etapa ≥3** | `LII_TERRITORIO` + `cultivoLIIIPreexistente=true`; `SECTA_INTERIOR` cerrada hasta M07 | Ver abajo. |

- **Duplicación de técnicas/items:** Piel de Cobre "se concede si falta" — correcto si comprueba `tid in tecnicas` y no fuerza `tecnicas_preparadas`. **Riesgo real: `equipoInicialEntregado` no figura en la lista de flags migrados** (ni en MD ni en JSON). Si la entrega en `descansillo` es state-based por ese flag, un save legacy que pasa por `descansillo` recibiría de nuevo uniforme y arma (N-01).
- **Pérdida de progreso:** ninguna; "no recalcular ni reducir saldo/mérito" cubierto.
- **Estado imposible:** el JSON dice "preservar gates" y a la vez que `SECTA_INTERIOR` sigue `false`. Si un save legacy tuviera `SECTA_INTERIOR=true` (ver74 no lo pone en ningún camino conocido; NO VERIFICADO fuera de extractos) la regla es ambigua (N-01).
- **`SECTA_INTERIOR` prematuro:** no, salvo lo anterior.
- **Discriminante:** "flags.arc1 ausente" ≠ "flags.arc1 inválido". Si `normalizarArc1` trata un `arc1` corrupto como ausente, dispara la migración y **abre P–M03** a partir de datos corruptos; debe fallar cerrado (rechazar o normalizar conservadoramente sin migrar) (N-01).
- **`SAVE_SCHEMA_VERSION=3`: no es necesario.** `flags` es objeto libre, no hay clave top-level nueva, los saves nuevos siempre llevan `arc1`. Un bump sólo simplificaría el discriminante; no compensa.

---

## 6. Misiones (sólo lo que resta por decir)

### 6.1 M02 — cumplido
Resuelve el soft-lock de REV2 (cadáver antes que Examen). No crea errante ni cambia identidad/cantidad (validador `ver74:02408-02409`); botín una sola vez (muerte permanente + sin EXTRAER); sin Atlas/bestiario/familiaridad (guardas en `recordarCriatura`/`observarCadaver`); la recreación única sin loot no permite abuso (además `observarCadaver` no escribe `descubrimientos`). Retiro permanente sólo si muere con M02 activa: la rata muerta *antes* de M02 reaparece normalmente. Observación menor: exigir orden estricto de los pasos 3–5 no está dicho; lo robusto es state-based (Examen aprendido ⇒ vale aunque se aprendiera antes de matar a la rata).

### 6.2 M03 — hallazgos en N-03
- `room_sin_hostiles`: el muñeco vive en `patio_marcial` y la evaluación en `patio_respiracion`; no bloquea. Correcto que no sea mob permanente en `ROOMS`.
- Piel de Cobre idempotente y `manual_piel` no salta M03: bien.

### 6.3 M04
- Incidente determinista (`EXAMINAR` de dos scenery), sin RNG, una vez, opcional: bien. **Los scenery `tablillas` (`bosque_puesto_marcas`) y `registro` (`bosque_refugio_patrulla`) no pudieron verificarse**; si no existen el incidente es inactivable (no soft-lock, es opcional).
- Ruta obligatoria coherente a nivel documental. `puerta` ya se visitó en el Prólogo, así que el checkpoint "control con Gao Shun" **debe ser un evento de NPC durante M04**, no una comprobación de `visitadas`. Distancias físicas: NO VERIFICADO.

### 6.4 M05
OR real entre `mercado_valle`/`granero_valle`; Xu An localizable (`sauces_casa_comunal`/`sauces_plaza`, sin scheduler); sin orden imposible. Píldora una vez (quest one-shot + flag). Huecos: N-04, N-07.

### 6.5 M06
Tres niveles, comparación ordinal, conjunto sin duplicados, `listo()` state-based, registro válido hasta cerrar M07 y previo a activar M06. Sin `conocimiento.anomaliasTerritoriales`. Falta la **tabla concreta** (no puede verificarse que haya al menos 3 tipos alcanzables en scenery real) y que la **activación** sea state-based (N-05, N-10).

### 6.6 M07
Qiao Ren `sala_inicial` en `pabellon_disciplina`; Jiang Rui por anclaje propietario M07; He Zhen/Ren Bo/Su Lian por escritura directa; R1 jugador ≠ R1 NPC. Escrituras SOSPECHA→SABE/CONFIRMADO válidas (`ver74:02380`), `PARCIAL` nunca entra en `conocimientoNPC`. La formulación no altera reward ni gate y no crea rutas alternativas; matices en N-08.

---

## 7. Anclajes y compañeros

`flags.arc1.anclajePropietario[npcId]` **cabe en schema 2** (flags libre) y no cambia la forma `{room,hasta}` exigida por el validador (`ver74:02388`). Resuelve la colisión misión vs escena social **siempre que** las escenas consulten el owner. Liberación atómica viable con una única función que actualice `posicionNPC`, el owner y valide `sala ∈ posicion_valida` (`ver74:02387`) en una sola mutación síncrona.

**Falta especificar antes del contrato (N-02):**
1. Ciclo de vida de los anclajes de **Tao Ming** (P/M01, en `registro`) y **Gao Shun** (M04, en `puerta`): owner, disparador y destino de liberación. Sólo Jiang Rui/M07 los tiene. `puedeMoverNPC` rechaza mover NPC anclados y no hay scheduler, así que sin liberación Tao Ming permanece en `registro` y M02 ("asigna y valida desde `oficina_servicios`") no puede activarse ni cerrarse como está escrito.
2. Preempción: una escena CRISIS con un único slot `{room,hasta}` y un único owner por NPC sobrescribiría el anclaje de misión y perdería el owner. En 3C.6 basta declarar que **CRISIS no preempta un anclaje con owner de misión** (o definir una pila); el arco completo de compañeros queda fuera.
3. Invariante de carga: owner sin anclaje ⇒ se descarta; anclaje sin owner ⇒ no liberable por escenas sociales.
4. Semántica de `hasta` sin introducir tiempo diegético (hoy sin consumidor): declararlo inerte.

---

## 8. Persistencia e invariantes

- Cabe en schema 2: `QUESTS` (catálogo; las claves de `this.quests` deben existir en él, `ver74:02398`), `this.quests`, `flags.arc1`, `player`, `conocimientoNPC`. `BLOQUEADA/DISPONIBLE` derivados; `normalizarArc1` sin clave top-level nueva.
- **Estados inválidos:** "se rechazan o normalizan fail-closed" es ambiguo: definir "desconocido ⇒ se descarta (no hecha)"; y coherencia entre quests (M05 `hecha` con M04 no hecha ⇒ degradar) (N-11).
- **`flags.arc1` corrupto:** `nivel`, `sospechaFuerte` e `informeFronteraAceptado` son valores almacenados derivables (de `tipos` y de M07). `normalizarArc1` debe **recomputarlos**, no confiar en ellos (`servicioTerritorial` ya es derivado; conviene igualar el criterio) y nunca subir `arc1.estado` por encima de lo que quests+flags sostienen (N-11).
- **Invariantes:** REV3 no requiere cambiar 329 rooms / 17 áreas / 787 salidas dirigidas / 0 reciprocidades rotas / 0 aisladas / 1 componente; no toca `ROOMS.exits` (el muñeco es instancia, la tabla de evidencia es externa); no agrega ni quita errantes; no rompe Atlas (guardas locales); no introduce tiempo diegético; no abre M12/ATAJO antes de la transición. **No se ejecutó `auditarMundo329`.**

---

## 9. Hallazgos nuevos

### CORRECCION_DOCUMENTAL

| ID | Hallazgo | Severidad | Corrección |
|---|---|---|---|
| **N-01** | Migración incompleta: falta `equipoInicialEntregado=true` (riesgo de doble entrega); faltan flags de cierre de P–M03 (`REGISTRO_INICIAL_COMPLETADO`, `ALOJAMIENTO_CONFIRMADO`, `SERVICIO_DESPENSA_VALIDADO`, `M03_*`, `TECNICA_PIEL_COBRE_APRENDIDA`, marca de raíz ya diagnosticada); sin regla si `SECTA_INTERIOR` ya era `true`; `flags.arc1` presente-pero-inválido no debe disparar migración. | Media | Listar el conjunto completo de one-shots P–M03 en MD y JSON; regla explícita de `SECTA_INTERIOR`; definir ausente ⇒ migrar, inválido ⇒ rechazar/normalizar sin migrar. |
| **N-02** | Ciclo de vida de anclajes de Tao Ming (P/M01) y Gao Shun (M04); preempción CRISIS; invariante owner↔anclaje; `hasta` inerte. | **Media-alta** (soft-lock de M02 si se implementa literal) | Tabla `NPC → room, owner, disparador de liberación, destino` para P, M01, M02, M04, M07; regla de no-preempción; normalización de carga. |
| **N-03** | M03: (a) "MEDITAR con éxito" no define qué pasa con **vaso lleno** (`qi>=qi_max` → el comando consagra o rechaza según puerta; un jugador en etapa 2 con 45/45 y M03 pendiente podría no poder "meditar con éxito"); (b) el muñeco puede derrotarse antes de la respuesta defensiva ⇒ paso irrecuperable si no se recrea; (c) persistencia/recreación de la instancia tras guardar/cargar; (d) no se dice si el muñeco ataca (sin ataque, "respuesta defensiva" sólo puede ser una técnica). | Media | (a) éxito = comando aceptado sin hostiles/combate, con o sin ganancia de qi y contando la consagración; (b/c) instancia recreada por estado mientras el paso esté pendiente; (d) definir el evento exacto (p. ej. usar técnica con guardia o DEFENDER con el muñeco como objetivo). El comportamiento de `cmd_meditar` con vaso lleno y puerta cerrada es NO VERIFICADO. |
| **N-04** | M05: el actuador de "registrar el circuito" y de "contactar a Xu An" no está definido; M04/M05 no declaran qué checkpoints son por estado (`visitadas`) y cuáles por evento. | Media | Definir verbos/eventos (`HABLAR`, `EXAMINAR` o comando propio) y marcar cada checkpoint estado/evento. |
| **N-05** | M06: sólo `listo()` es state-based. Si el jugador registró evidencia antes de cerrar M05 (permitido desde `PATRULLA_TERRITORIAL`), no hay "primer incidente" posterior que active M06; con los cuatro tipos ya reunidos, M06 podría no activarse nunca (bloquea M07 y LIII). El texto no lo excluye. | Media | La reconciliación activa M06 por estado (`M04 ∧ M05 hechas ∧ ≥1 tipo`). |
| **N-06** | M04: no se fija el punto único del +1 Mérito (¿al evento o al cierre por flag?). Riesgo de doble otorgamiento o de omisión. | Baja | Otorgar en el evento, con flag one-shot, y que la recompensa de cierre no lo recompute. |
| **N-07** | Píldora: la reemisión "una sola" no tiene tope; SOLTAR se rechaza, pero otras salidas (vender, depositar, entregar, pérdida por muerte, si existen) provocan reemisión: bucle vender→recargar→reemitir (ITEMS.precio 8, `ver74:6843`). No se verificó si existe compra de reliquias. | Media | Enumerar vías de pérdida; tope (`PILDORA_REEMITIDA`, una vez) o ítem no transferible mientras dure la protección. |
| **N-08** | M07: "pueden pedir reformulación" sin regla determinista; no se dice si la corrección FUERTE→CAUTA cambia `formulacion` a CAUTA ni si rechazarla bloquea; "abandonar M07" no existe como acción; falta quién activa M07 (Qiao Ren en `pabellon_disciplina`) y el momento del anclaje de Jiang (aparición a la vista). | Baja | Cerrar M07 en cualquier elección; persistir la formulación final y `corregida`; liberar sólo al cerrar. |
| **N-09** | Omisiones unilaterales MD↔JSON (D1–D7). | Baja | Igualarlas en addendum. |

### CAMBIO_NECESARIO_3C6

| ID | Cambio |
|---|---|
| **N-10** | Ampliar los requisitos técnicos: (1) comprobar `validarSave329`/`normalizarFacciones` frente a `merito<saldo` y el relleno por defecto `miembro` (`ver74:18899-18905`) cuando la partida nueva arranca `inactivo`; (2) verificar que `otorgarContribucion`/`otorgarMerito` funcionan con `estado=inactivo` (M02); (3) enumerar llamadores de `otorgarContribucion`; (4) `titulo` inicial y lista blanca de `cambiarEstadoFaccion` (`ver74:15917`, `18927`); (5) sustituir el stub `gestionarMisionesNpc` (`ver74:18869`); (6) **tabla de evidencia** con cobertura demostrable (≥3 tipos alcanzables en scenery real, cada tipo con ≥2 fuentes independientes) y existencia verificada de los scenery de M04. |

### ENDURECIMIENTO_FUTURO

- **N-11** `estadoAfiliacion` ↔ `facciones.…estado` sin invariante; valores derivados almacenados (`nivel`, `sospechaFuerte`, `informeFronteraAceptado`); normalización de cadenas entre quests; `arc1.estado` no debe subir por sí solo; servicios de facción inalcanzables en LII (balance); "bloquea o produce error" ⇒ "bloquea y reporta".

### EDITORIAL_NO_BLOQUEANTE

- Rotulado UI de los dos "rangos"; `titulo` inicial "aspirante aceptado" (`ver74:15917`) tras M03; ambigüedad `qi>=45`/`qi=45`.

**BLOQUEANTE:** ninguno.

---

## 10. Correcciones exactas para pasar a APTA (addendum REV3.1)

**MD y JSON:** (1) N-01: lista completa de one-shots y reglas de migración; (2) N-02: tabla de anclajes y no-preempción; (3) N-03: definiciones de "éxito" y de "respuesta defensiva", recreación del muñeco; (4) N-04: actuadores y modelo estado/evento de M04/M05; (5) N-05: activación state-based de M06; (6) N-06: punto único del Mérito; (7) N-07: tope de reemisión de la píldora; (8) N-08: regla determinista de la formulación; (9) D1–D7; (10) N-10: ampliar requisitos técnicos. Ninguna corrección modifica decisiones humanas ni requiere subir el schema.

---

## 11. Veredicto

Cumplimiento de la condición de aptitud: CD-01…CD-11 **no todos resueltos** (tres parciales); MD/JSON coherentes; sin contradicción estructural nueva; **soft-locks documentales de severidad media-alta sin cerrar** (N-02); migración definida pero incompleta; gates fail-closed; schema 2 viable.

3C6A_REV3_REQUIERE_CORRECCIONES