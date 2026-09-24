# Auditoría externa 3C.7A — Fase 1 (M08–M15) — La Grulla Blanca

- **Agente auditor:** Claude
- **Modelo/versión:** Claude Sonnet 5
- **Fecha:** 2026-09-24
- **Repositorio:** https://github.com/Shein25/La-Grulla-Blanca
- **Rama:** `audit/3c7a-m08-m15`
- **HEAD:** esperado según el pedido `67b5d6a976f47c464b187896b121467bd4cc5094`. **No verificable** desde URLs raw (ver H-05).
- **Baseline:** `grulla-blanca_ver74.html`
- **SHA baseline:** esperado `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`. Coincide entre el pedido, el índice, la Matriz y el Informe 3C.5. **El hash del archivo no pudo recalcularse** (archivo truncado, sin red en el sandbox).
- **Fase1 MD:** `docs/3C7A/Auditoria_3C7A_M08_M15_FASE1_REV1.md` — **NO LEÍDO** (ver §0)
- **Fase1 JSON:** `docs/3C7A/Matriz_3C7A_M08_M15_FASE1_REV1.json` — leído completo
- **Fuentes usadas:** ver tabla de acceso en §0
- **Tipo:** auditoría documental externa de recuperación canónica. Solo lectura; no se modificó nada ni se escribió en GitHub.

---

## 0. Alcance efectivo y limitaciones (leer primero)

Esta auditoría es **parcial**. No fabrico lo que no pude leer.

| Archivo | Estado de acceso |
|---|---|
| Prompt de auditoría | Leído completo |
| Fase1 MD (`Auditoria_3C7A_M08_M15_FASE1_REV1.md`) | **No accesible.** 3 intentos, la herramienta devolvió "requested file reference is not currently visible" |
| Matriz JSON | Leído completo |
| Índice `PAQUETE_3C7A_M08_M15_FASE1.md` | Leído completo |
| Auditoría 6 canónica (MD) | Leída **hasta el objetivo obligatorio de M11**. Incluye la matriz principal §3 con las filas P–M18 completas, pero **truncada antes de las fichas M11 (resto), M12, M13, M14, M15 y del gate LIII→LIV** |
| Auditoría 6 estructurada (JSON) | Leída hasta el inicio de M10 (truncada) |
| Informe 3C.5 | Leído completo |
| `ver74.html` | **Truncado** durante el CSS. No se llegó al JS (`PUERTAS`, `NPC_DEF`, `ROOMS`) |

Consecuencias directas:

1. **§2 (coherencia MD↔JSON) no puede completarse.** Solo audité el JSON contra las fuentes y contra el índice.
2. Para M12–M15 verifiqué **a nivel de la matriz principal §3 de Auditoría 6** (requiere/produce/abre/NPC/áreas/revelación), no contra las fichas completas.
3. Toda comprobación contra ver74 queda `NO_VERIFICADO`. Lista concreta en §14.

---

## 1. Resumen de resultados

- Recuperación de la columna vertebral, revelaciones R2–R9 y `requiere/produce/abre` de M08–M15: **fiel** en todo lo comparable.
- No detecté **canon inventado** ni **revelación adelantada** en el JSON.
- Sí detecté **pérdida de restricciones narrativas negativas** en el JSON (H-01, H-02), una **afirmación de cierre de 3C.5 sin respaldo** en el paquete (H-04) y **asimetría de tratamiento** entre M08 y M10 respecto de ver74 (H-03).
- Ningún hallazgo llega a `BLOQUEANTE` con lo que pude leer.

---

## 2. Coherencia Fase1 MD ↔ JSON

**No verificable: el MD no fue accesible.** No emito juicio sobre frontera, dependencias, áreas, rooms, gaps, gate, F1-01…F1-09 ni pendientes *en el MD*.

Lo que sí comprobé (JSON ↔ índice ↔ Informe):

| Punto | Resultado |
|---|---|
| Frontera provisional 3C.6A→3C.7 | Índice y Matriz coinciden: provisional hasta PASS de 3C.6A REV3.1 — **VERIFICADO** |
| SHA-256 de ver74 | Pedido = índice = Matriz = Informe 3C.5 (salida ver74) — **VERIFICADO** en las 4 fuentes; hash del archivo **NO_VERIFICADO** |
| Entregables del paquete | El índice lista MD + JSON REV1 — coincide con los nombres del pedido — **VERIFICADO** |
| Referencias de HEAD | Tres hashes distintos entre documentos (H-05) |

---

## 3. Columna vertebral

Contra la matriz §3 de Auditoría 6:

| Afirmación | Fuente | Resultado |
|---|---|---|
| M08/M09/M10 paralelas, orden libre | Estructurado JSON: `orden_relativo` en M08 y M09 (T288); MD M11: "las tres, sin orden fijo". M10 truncado | **VERIFICADO** (M10 por consistencia con M11) |
| M11 exige M08+M09+M10 | Fila M11 | **VERIFICADO** |
| M12 exige M11 | Fila M12 | **VERIFICADO** |
| M13 solo tras LIII→LIV | Fila M12 "abre M13 (tras gate LIII->LIV)"; fila M13 requiere `LIV_REVELACION` | **VERIFICADO** |
| M14 exige M13; M15 exige M14 | Filas M14, M15 | **VERIFICADO** |
| M16 fuera de alcance | Matriz lo menciona solo como `abre` de M15 y como frontera; no desarrolla contenido | **VERIFICADO** (no hay adelanto) |

Matiz preservado correctamente: M08 exige además `SECTA_INTERIOR`; M09 y M10 solo LIII.

---

## 4. Revelaciones

| Misión | Esperado | Matriz JSON | Fuente (tabla §3) |
|---|---|---|---|
| M08 | R2 CONFIRMADO | ✔ | ✔ |
| M09 | R3 PARCIAL | ✔ | ✔ |
| M10 | R4 CONFIRMADO | ✔ | ✔ |
| M11 | R3 CONFIRMADO | ✔ | ✔ |
| M12 | R5 CONFIRMADO | ✔ | ✔ |
| M13 | R6 CONFIRMADO | ✔ | ✔ |
| M14 | R8 CONFIRMADO | ✔ | ✔ |
| M15 | R9 CONFIRMADO | ✔ | ✔ |

**VERIFICADO.** R7 y R10 no figuran como producidas en ninguna misión M08–M15 de la Matriz; identidad de la Grulla, dependencia viva y decisión LIBERAR/CUSTODIAR tampoco. **Reserva:** la Matriz no tiene ningún campo que *declare* esas exclusiones (ver H-02). La ausencia es correcta pero implícita.

---

## 5. M08

| Punto | Resultado |
|---|---|
| He Zhen concede `FORMACIONES_INVESTIGACION` | **VERIFICADO** |
| M08 confirma R2 | **VERIFICADO** |
| Repetición de medición en sector/nodo independiente | **VERIFICADO** |
| Área Formaciones cerrada | **VERIFICADO** (Auditoría 6: confirmada en topología v2) |
| Room IDs de puntos exteriores y "Sala de Mapas de Flujo" no cerrados por Auditoría 6 | **VERIFICADO** (`DESTINOS_329_PENDIENTES` en ficha y JSON estructurado) |
| Cautela sobre `formaciones_sala_mapas` | **La cautela es correcta.** Que ver74 tenga una room con nombre parecido no convierte un `NO CERRADO EN FUENTE` en canon. La existencia del id en ver74 es `NO_VERIFICADO` por mí |
| Recompensas: Comprensión 0, mérito moderado, contribución sí | **VERIFICADO** |

Omisión menor: la ficha dice que `FORMACIONES_INVESTIGACION` **permanece activo** tras cerrar M08. La Matriz no lo recoge (H-01).

---

## 6. M09

| Punto | Resultado |
|---|---|
| `ARCHIVO_COMUN` al inicio; `ARCHIVO_RESTRINGIDO` autorizado por Qiao Ren durante el progreso | **VERIFICADO** (la Matriz conserva "temporalmente") |
| R3 PARCIAL | **VERIFICADO** |
| LEER ESCRITURAS sin Hoja de Claridad, sin coste, sin +2 Comprensión repetible | **VERIFICADO** |
| Tres clases de inconsistencia | **VERIFICADO** |
| "Dos Alas" aparece sin definición completa | **VERIFICADO** (`finalizacion_fuente`) |
| **No revelar Primera Ala como red completa** | **Presente en la fuente, ausente en la Matriz** (H-01) |
| Dejar pendiente el mapping de rooms de Archivo Común/Restringido | **Correcto.** Auditoría 6 no fija rooms (`NO CERRADO EN FUENTE`) |

Nota estructural: la Matriz usa `[]` en `salas_confirmadas_fuente` y `destinos_pendientes_fuente` de M09, donde la fuente dice literalmente `NO CERRADO EN FUENTE`. Un array vacío puede leerse como "no hay pendientes" (H-07).

---

## 7. M10

| Punto | Resultado |
|---|---|
| Auditoría 6: "Sala Anatómica"/"Archivo Clínico" sin room_id literal | **VERIFICADO** |
| Fase1 (F1-03): ver74 tiene `sala_anatomica` y `archivo_clinico`, ambas en territorio de Chen Bo | **NO_VERIFICADO** (ver74 truncado; el Informe 3C.5 no enumera rooms ni el territorio de NPC) |
| R4 CONFIRMADO | **VERIFICADO** |
| No confundir Segunda Rama con Dos Alas | Presente en la fuente; **ausente en la Matriz** (H-01) |
| No habilitar injerto jugable | Ídem (H-01) |
| M10 no concede la síntesis de M11 | Implícito: recompensa Comprensión 0 y M11 concentra R3 CONFIRMADO. No declarado |

Omisiones de la Matriz en M10, todas de la ficha de Auditoría 6: injerto jugable no se habilita (requiere ZhuJi + método específico); `ESTUDIAR INJERTO` se elimina del contenido visible de Arc1 y el verbo futuro es `LEER APENDICE`; nadie realiza injerto en M10.

**Problema de método (H-03):** Fase1 trata el hueco de M10 como `RESOLUBLE_CON_VER74` ("ya tiene IDs literales") pero el de M08 como `A_RECONCILIAR` ante el mismo tipo de evidencia (id con nombre coincidente en ver74). Auditoría 6 dice expresamente que no infiere por semejanza de nombre. Con la jerarquía del prompt (§1), el mapeo M10→ids de ver74 es una **propuesta de mapeo**, no un cierre.

---

## 8. M11

| Punto | Resultado |
|---|---|
| Requiere M08+M09+M10 | **VERIFICADO** |
| Reunión de síntesis, no nueva expedición | **VERIFICADO** |
| Participantes: He Zhen, Song Rui, Lan Meihua | **VERIFICADO** |
| R3 CONFIRMADO | **VERIFICADO** |
| `DOS_ALAS=PRINCIPIO`; `SEGUNDA_RAMA=APLICACION_CORPORAL` | **VERIFICADO** |
| Comprensión +1 (`ARC1_M11_DOS_ALAS`) | **VERIFICADO** |
| Mantener pendiente la room de la reunión | **Correcto.** La fuente no fija room; "Manantial Partido" es explícitamente ambiguo (único ecológico, no necesariamente room de M11) |

Detalle: el `destinos_pendientes_fuente` de la Matriz para M11 recoge "Manantial Partido", pero ni F1-06 ni la lista de pendientes lo mencionan (H-09).

---

## 9. M12

Verificado contra la fila M12 de la matriz §3 (la ficha completa estaba truncada):

| Punto | Resultado |
|---|---|
| Requiere M11; produce `PRIMERA_ALA_INVESTIGACION`, R5 CONFIRMADO, Comprensión +1 (`ARC1_M12_RED_PRIMERA_ALA`), `ala_umbral_mantenimiento` conocido | **VERIFICADO** |
| Las seis rooms (`formaciones_sello_antiguo`, `formaciones_descenso_tecnico`, `ala_vestibulo`, `ala_nudo_seis_corrientes`, `ala_camara_dos_alas`, `ala_umbral_mantenimiento`) | Las seis figuran entre las 33 rooms literales que Auditoría 6 declara verificadas en topología v2 — **VERIFICADO** en existencia. **Asignación a M12: NO_VERIFICADO** (ficha truncada) |
| Entrada oficial Formaciones→Primera Ala no es uno de los seis atajos | Presente en Matriz (`activacion_fuente`) |
| M12 no exige 6/6 atajos | Presente en Matriz (`objetivos_obligatorios_fuente`) |
| Custodio: COMBATE o PROTOCOLO | Presente en Matriz |
| Protocolo sin secretos opcionales ni Afinidad alta | Presente en Matriz (6 atajos/14 secretos/único ecológico/Afinidad alta) |
| `ala_umbral_mantenimiento` **conocido pero no accesible** al cerrar M12 | Matriz dice solo "conocido". **La parte "no accesible" no está** (H-02) |

**Qué falta realmente antes de implementar** (inventario del auditor a partir de lo declarado; no es canon):

1. Evaluador `evaluarEvidenciaPrimeraAla()`: qué evidencias cuentan y umbrales INSUFICIENTE/SUFICIENTE/CONCLUYENTE.
2. Contrato del Custodio: rama COMBATE, rama PROTOCOLO, y qué pasa si el jugador falla o huye.
3. Idempotencia / one-shots.
4. Anclajes NPC de M12.
5. Recompensas numéricas de mérito, contribución y prestigio.
6. Modelo de permiso `PRIMERA_ALA_INVESTIGACION` (fuente, origen, vigencia).
7. Relación entre el cierre de M12 y el gate (H-08).
8. Regla de acceso a `ala_umbral_mantenimiento`: conocido sí, accesible no, hasta que corresponda.

---

## 10. Gate LIII→LIV

| Punto | Resultado |
|---|---|
| Fuente: `qi>=75 + DosAlas==COMPRENDIDAS + redPrimeraAla==CONCLUYENTE + autorización institucional`; sin exigir seis atajos, únicos ni todas las rooms | **NO_VERIFICADO contra la fuente primaria.** La sección del gate está en la parte truncada de Auditoría 6. Solo comprobé que las filas M12/M13 refieren "gate LIII->LIV". Matriz F1-08 y el prompt afirman la fórmula, pero ninguno es la fuente |
| ver74 conserva `PUERTAS[4]` legacy = 2 píldoras + `comprensión:6` | **NO_VERIFICADO** (ver74 truncado antes del JS) |
| Clasificación de la sustitución del gate legacy | **`CAMBIO_NECESARIO_3C7`**, no contradicción documental. Razones verificadas: el Informe 3C.5 declara que **no se implementaron M01–M18**; Auditoría 6 documenta que el baseline legacy no tiene `arc1.estado` ni los permisos nuevos. Un gate viejo en un baseline previo a 3C.7 es deuda esperable |

Condición: la clasificación se sostiene si `PUERTAS[4]` existe con esa forma. Confirmarlo es una de las comprobaciones técnicas pendientes (§14).

No diseño el gate nuevo. Registro solo dos puntos de nomenclatura a reconciliar (H-08).

---

## 11. M13–M15

Contra las filas M13–M15 de la matriz §3:

| Misión | Punto | Resultado |
|---|---|---|
| M13 | R6 CONFIRMADO; Comprensión +1; acceso a Mantenimiento Antiguo (`MANTENIMIENTO_INVESTIGACION`, corredores necesarios, **no concede Núcleo**); NPC Duan Shibo, He Zhen, Ma Qiren, Lu Cheng, Song Rui; áreas mantenimiento/producción/archivos | **VERIFICADO** |
| M13 | No revela dependencia viva | No declarado en Matriz (H-02); en la fuente `NO_VERIFICADO` (ficha truncada) |
| M14 | R8 CONFIRMADO; produce `NUCLEO_SUPERIOR`; pocos NPC; Consejo autoriza el acceso | **VERIFICADO** |
| M14 | No confirma todavía que el pacto debía ser temporal | No declarado en Matriz (H-02); fuente `NO_VERIFICADO` |
| M15 | R9 CONFIRMADO; Comprensión +1 (`ARC1_M15_RELEVO_APLAZADO`); abre M16 | **VERIFICADO** |
| M15 | Cadena de tres aplazamientos: "prototipo insuficiente → ruptura de Primera Ala → normalización del mantenimiento" | **NO_VERIFICADO.** Son hitos específicos con nombre; debe cotejarse con la ficha de M15 (T289) para descartar que sean reformulación de Fase1 |
| M15 | No revela R7/R10; `nucleo_descenso_pulso` cerrado hasta M17 | La Matriz no lo declara (H-02). Además `nucleo_descenso_pulso` aparece en la lista de 33 rooms, pero no es room de M13–M15 en la Matriz: **coherente** |

Rooms que Fase1 considera cerradas: M13 (`ala_umbral_mantenimiento`, `mantenimiento_acceso`, `mantenimiento_dormitorio_turnos`), M14 (`mantenimiento_compuerta_nucleo`, `nucleo_pozo_voto`, `nucleo_camara_voto`, `nucleo_galeria_primer_pacto`, `nucleo_primer_pacto`), M15 (`nucleo_archivo_promesa`). Todas existen en la lista de 33 verificadas. **La asignación por misión es `NO_VERIFICADO`** (fichas truncadas). Ojo especial con `mantenimiento_dormitorio_turnos` y `nucleo_camara_voto`: no aparecen en los objetivos obligatorios de la Matriz, así que su vínculo con M13/M14 debe confirmarse en la ficha.

---

## 12. Compatibilidad con 3C.5 NPC

El Informe 3C.5 declara 32 definiciones en `NPC_DEF` (7 autoridad, 7 intermedio, 12 funcional, 6 compañero) pero **no las enumera**, y la fuente `Matriz_Implementacion_3C5_NPC_REV3.json` no está en el paquete.

| NPC | Aparece en Auditoría 6 (M08–M13) | Existe en ver74 |
|---|---|---|
| He Zhen | ✔ | NO_VERIFICADO |
| Wen Tao | ✔ (M08; "posiblemente" en M12) | NO_VERIFICADO |
| Song Rui | ✔ | NO_VERIFICADO |
| Lan Meihua | ✔ | NO_VERIFICADO |
| Chen Bo | ✔ | NO_VERIFICADO |
| Qiao Ren | ✔ | NO_VERIFICADO |
| Duan Shibo | ✔ | NO_VERIFICADO |
| Ma Qiren | ✔ | NO_VERIFICADO |
| Lu Cheng | ✔ | NO_VERIFICADO |

Fase1 **no inventa NPC**: todos los nombres de la Matriz para M08–M13 salen de Auditoría 6. Los adicionales (Zhao Wen, Luo Yan, Yu Shun, Guo Chen) tampoco están inventados, pero su presencia en ver74 también es `NO_VERIFICADO`.

---

## 13. Hallazgos consolidados

### H-01 — CORRECCION_DOCUMENTAL — El JSON pierde restricciones narrativas negativas de M08/M09/M10
Verificado contra las fichas de Auditoría 6 (campo `CONSECUENCIAS`):
- M08: `FORMACIONES_INVESTIGACION` permanece activo para los sectores correspondientes.
- M09: no revela Primera Ala como red completa; "Dos Alas" puede aparecer como encabezado sin significado cerrado (preserva M12).
- M10: no confirma Segunda Rama = Dos Alas; injerto jugable no se habilita; `ESTUDIAR INJERTO` se elimina del contenido visible de Arc1 y pasa a `LEER APENDICE`; nadie realiza injerto en M10.

Ninguna está en la Matriz. Si el MD las conserva, hay divergencia MD↔JSON; si tampoco, es pérdida de restricción. Ambas requieren corrección. Sugerencia: campo `consecuencias_fuente` o `no_adelantar` por misión.

### H-02 — CORRECCION_DOCUMENTAL — La Matriz no declara restricciones de revelación de M12–M15
Ausentes: `ala_umbral_mantenimiento` conocido pero no accesible al cerrar M12; M13 no revela dependencia viva; M14 no confirma pacto temporal; M15 no revela R7/R10; `nucleo_descenso_pulso` cerrado hasta M17; ninguna misión revela identidad actual de la Grulla ni adelanta LIBERAR/CUSTODIAR. El prompt afirma que Auditoría 6 las contiene, pero no pude confirmarlo (ficha truncada). Las restricciones críticas para "no adelantar revelaciones" deberían ser explícitas, no inferidas por ausencia.

### H-03 — CORRECCION_DOCUMENTAL — Tratamiento asimétrico M08 vs M10 respecto de ver74
F1-03 (`RESOLUBLE_CON_VER74`, "ya tiene IDs literales") contradice en espíritu la cautela de F1-04 y la jerarquía del prompt. Recomiendo reetiquetar F1-03 como `A_RECONCILIAR` con "candidato de mapeo: `sala_anatomica`, `archivo_clinico`". Además, el mapeo M10 no figura en `pendientes_para_reconciliacion`, aunque F1-03 lo deja abierto.

### H-04 — CORRECCION_DOCUMENTAL — "3C5: CERRADO_AUDITADO" sin respaldo en el paquete
La Matriz declara `baseline_produccion.3C5 = CERRADO_AUDITADO`. El Informe 3C.5 del paquete es el de implementación y termina en `3C5_IMPLEMENTACION_REQUIERE_CORRECCIONES`, dice que ver74 es "candidata", que **no declara cerrado 3C.5** y que la suite no se corrió en navegador real (309/398 en DOM simulado). Si existe una auditoría posterior que lo cerró, debe citarse con su veredicto y fecha; si no, el estado debe bajarse.

### H-05 — CORRECCION_DOCUMENTAL (menor) — Tres HEAD distintos en documentos del mismo paquete
Pedido: `67b5d6a…`. Prompt dentro del repo: `330cb6c…`. Índice ("al crear este índice"): `9cb44a4…`. Es compatible con commits sucesivos, pero no pude verificar el HEAD real. El prompt del repo declara un HEAD esperado desactualizado respecto del pedido.

### H-06 — PENDIENTE_RECONCILIACION — Inconsistencia interna de Auditoría 6 sobre M12/M17 y `reliquias_verticales`
El texto (§1 y §2.3) dice que M12/M17 reemplazan contenido legacy (`reliquias_verticales`, Sombra/Centinela como llaves). Pero la tabla §3 marca M12 y M17 como `NO_IMPLEMENTADO` (solo M02, M03, M18 son `LEGACY_A_REEMPLAZAR`). Fase1 no lo menciona. Debe entrar al inventario porque afecta cómo 3C.7 trata el contenido legacy en M12.

### H-07 — CORRECCION_DOCUMENTAL (menor) — `[]` usado donde la fuente dice `NO CERRADO EN FUENTE`
M09 (`salas_confirmadas_fuente`, `destinos_pendientes_fuente`) y los `destinos_pendientes_fuente` de M13–M15 usan array vacío. Recomiendo un valor explícito (`"NO_CERRADO_EN_FUENTE"`) o `null` con nota, para no leer "sin pendientes".

### H-08 — PENDIENTE_RECONCILIACION — Dos puntos de coherencia interna para el gate
(a) M12 se cierra con evidencia `SUFICIENTE` (y el protocolo exige "evidencia principal suficiente"), mientras el gate pide `redPrimeraAla==CONCLUYENTE`. Habría que aclarar si M12 puede quedar HECHA sin poder pasar el gate, y cómo se sube de SUFICIENTE a CONCLUYENTE, para evitar un soft-lock. Es una pregunta, no una propuesta de canon.
(b) Nomenclatura: M11 produce `DOS_ALAS=PRINCIPIO`; el gate dice `DosAlas==COMPRENDIDAS`. Falta la tabla de equivalencia.

### H-09 — PENDIENTE_RECONCILIACION — Faltan en el inventario de pendientes
- Mapeo M10 (`sala_anatomica`, `archivo_clinico`), ver H-03.
- "Manantial Partido" como región cruzada de M11.
- Cita del cierre de 3C.5, ver H-04.
- Modelo de permisos `FORMACIONES_INVESTIGACION`, `PRIMERA_ALA_INVESTIGACION`, `MANTENIMIENTO_INVESTIGACION`, `NUCLEO_SUPERIOR` (fuente/origen/vigencia). El pendiente actual solo cubre la autorización de LIII→LIV. Auditoría 6 define `fuente` y `origen` para `PATRULLA_TERRITORIAL` (M04) y `NUCLEO_PROFUNDO` (M17).
- Inconsistencia legacy M12/M17, ver H-06.

### Clasificación consolidada

| Elemento | Clasificación |
|---|---|
| Columna vertebral M08–M15 | VERIFICADO |
| Revelaciones R2/R3/R4/R5/R6/R8/R9 | VERIFICADO |
| Cautela de rooms M08, M09, M11 | VERIFICADO |
| Ausencia de canon inventado / adelantos en el JSON | VERIFICADO |
| H-01, H-02, H-03, H-04, H-05, H-07 | CORRECCION_DOCUMENTAL |
| H-06, H-08, H-09 | PENDIENTE_RECONCILIACION |
| Sustitución de `PUERTAS[4]` en 3C.7 | CAMBIO_NECESARIO_3C7 (condicionado, ver §10) |
| Evaluador Primera Ala, contrato Custodio, anclajes, one-shots, recompensas numéricas | PENDIENTE_RECONCILIACION (ya declarados; no penalizados) |
| Cadena de tres aplazamientos M15 (hitos nombrados) | NO_VERIFICADO |
| Todo lo que exige leer ver74 o el Fase1 MD | NO_VERIFICADO |
| Ningún hallazgo BLOQUEANTE ni ENDURECIMIENTO_FUTURO con lo leído | — |

---

## 14. Comprobaciones técnicas y documentales que faltan

**Documentales**
1. Leer `Auditoria_3C7A_M08_M15_FASE1_REV1.md` completo y ejecutar §2 (MD↔JSON) sobre frontera, dependencias, revelaciones, áreas, rooms, gaps, gate, F1-01…F1-09 y pendientes.
2. Leer las fichas M11 (resto), M12, M13, M14, M15 y la sección del gate LIII→LIV de Auditoría 6 (MD y JSON estructurado). Cerrar en particular: asignación de rooms por misión, restricciones negativas (H-02), cadena de tres aplazamientos, fórmula literal del gate.
3. Comprobar el HEAD real de la rama (`git rev-parse`).
4. Aportar la auditoría que cierra 3C.5 (H-04) o corregir el estado.

**Técnicas sobre ver74** (necesitan el archivo completo)
5. Recalcular SHA-256 y comparar con `8cd2d2f5…9566`.
6. Confirmar que `PUERTAS[4]` (o equivalente) usa 2 píldoras + `comprensión:6`.
7. Confirmar existencia de `sala_anatomica`, `archivo_clinico` y `formaciones_sala_mapas` en `ROOMS`, y el territorio de Chen Bo en `NPC_DEF`.
8. Confirmar en `NPC_DEF` los nueve NPC de §12 (más Zhao Wen, Luo Yan, Yu Shun, Guo Chen).
9. Confirmar que las 33 rooms literales de Auditoría 6 existen en `ROOMS` de ver74 (Auditoría 6 las verificó contra topología v2, no contra ver74).

---

## 15. Veredicto

La recuperación del canon en el JSON es fiel en todo lo que pude cotejar y no hay canon inventado ni revelaciones adelantadas. Aun así, **no puedo emitir `APTA_PARA_RECONCILIACION`**: no pude leer el Fase1 MD, no pude verificar nada contra ver74, y el JSON tiene pérdidas de restricciones narrativas (H-01, H-02), una afirmación de cierre de 3C.5 sin respaldo (H-04) y un tratamiento asimétrico de la evidencia de ver74 (H-03). Este veredicto se emite sobre lo verificable, no sobre una auditoría completa. Recomiendo repetir la parte pendiente (§14) una vez corregidos los puntos H-01 a H-05.

3C7A_FASE1_REQUIERE_CORRECCIONES