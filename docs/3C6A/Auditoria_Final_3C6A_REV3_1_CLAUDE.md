# Auditoría final de cierre — 3C.6A REV3.1 (Prólogo + M01–M07)

| Campo | Valor |
|---|---|
| Agente auditor | Claude |
| Modelo/versión | Claude Sonnet 5 |
| Fecha | 2026-09-24 |
| Repositorio | https://github.com/Shein25/La-Grulla-Blanca |
| Rama | `audit/3c6a-rev3-1` |
| HEAD | `3a9f9e59cf7b84a346de52ffda2b332055177216` — **verificado** (`git ls-remote` coincide exactamente con el HEAD declarado) |
| Baseline | `grulla-blanca_ver74.html` |
| SHA baseline | `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566` (declarado en MD/JSON/paquete; **no recalculado** — el .html no está disponible para descarga en este entorno) |
| REV3.1 MD | `docs/3C6A/Reconciliacion_3C6A_Prologo_M01_M07_REV3_1.md` |
| REV3.1 JSON | `docs/3C6A/Matriz_Implementacion_3C6A_Prologo_M01_M07_REV3_1.json` |
| Auditoría previa usada | `Auditoria_Cierre_3C6A_REV3_CLAUDE.md` (veredicto: `3C6A_REV3_REQUIERE_CORRECCIONES`) |
| Tipo | Auditoría final de cierre documental/técnica — checklist contractual sobre N-01…N-10 |

**Método.** A diferencia de la auditoría de REV3, en esta sesión **sí pude abrir** el índice y los extractos `01`–`09` de ver74 (URLs explícitas en el paquete), además de la auditoría previa completa, el paquete de auditoría y el estado real del repositorio (`git ls-remote`, descarga y hash de los artefactos REV3.1). No se modificó, comiteó ni fusionó nada. Todo lo marcado **VERIFICADO** se apoya en cita de línea de ver74 comprobada en esta sesión; lo marcado **NO VERIFICADO EN EXTRACTOS** es una limitación de cobertura de los extractos entregados, no una objeción de fondo.

---

## 0. Resumen ejecutivo

REV3.1 cierra correctamente los diez hallazgos de la auditoría REV3 (N-01…N-10). Los mecanismos críticos —migración legacy discriminada, tabla completa de anclajes, evento de práctica de M03 desacoplado del vaso lleno, checkpoints M04/M05 por evento, activación state-based de M06, guarda central de la píldora, formulación determinista de M07— quedan bien especificados y, en los puntos que pude contrastar contra el código real de ver74, son técnicamente implementables tal como están escritos (el hook de `cmd_meditar` cae exactamente entre el chequeo de hostiles y la rama `qi>=qi_max`; `casa_guardia` y `oficina_servicios` existen y son alcanzables; `otorgarContribucion` en efecto sólo rechaza `expulsado`; `normalizarFacciones` en efecto fuerza `miembro`/`merito>=saldo` hoy, confirmando que ese es el cambio pendiente correcto).

No encontré ningún soft-lock documental nuevo de severidad media o alta. Encontré:

- **Una discrepancia de paridad real** entre el JSON adjuntado en esta conversación y el JSON que está en el HEAD verificado del repositorio (no son el mismo archivo, aunque son equivalentes en sustancia). Ver §2.
- **Un matiz no resuelto de N-05** (menor, no bloqueante): la activación state-based de M06 está garantizada en los puntos de reconciliación listados, pero el documento no dice explícitamente que registrar una evidencia dispara `reconciliarProgresionArc1()` en el acto; ver §6.
- Confirmación de que varios "requisitos técnicos para el contrato" (N-10) corresponden a comportamiento **actualmente distinto** en ver74 (p. ej. `normalizarFacciones` fuerza `estado=miembro` y `merito>=saldo` hoy), lo cual es exactamente lo que REV3.1 dice que hay que cambiar — no es una contradicción, es la confirmación de que la especificación apunta al lugar correcto del código.

Veredicto: **`3C6A_REV3_1_APTA_PARA_CONTRATO`**.

---

## 1. Los diez hallazgos de REV3 (checklist contractual)

| ID | Estado | Evidencia |
|---|---|---|
| **N-01** | **RESUELTO** | `migracion_saves_ver74` (JSON) y §5 (MD) listan los doce one-shots P–M03 completos (incluye `equipoInicialEntregado`, que era la omisión que arriesgaba doble entrega de uniforme/arma). Discriminante explícito: `flags.arc1` ausente→migrar; presente-válido→normalizar; presente-inválido→**fallar cerrado, nunca legacy**. Regla explícita para `SECTA_INTERIOR` legacy=true: se guarda `legacySectaInteriorPrevia=true` sólo diagnóstico y se normaliza a `false` hasta M07. Etapas 1/2/≥3 cubiertas con `transicionLILIIHecha` y `cultivoLIIIPreexistente`. |
| **N-02** | **RESUELTO** | Tabla completa de 10 anclajes (P, M01×2, M02×2, M03×2, M04×2, M07) con room/owner/hasta/liberación/destino. El ciclo de Tao Ming (P→M01→M02) y de Gao Shun (M04→`casa_guardia`) —el hueco que en REV3 arriesgaba que M02 no pudiera activarse en `oficina_servicios`— queda cerrado: `casa_guardia` **existe** (`ver74:7999`, salida norte de `deposito_comun`) y `oficina_servicios` **existe y es alcanzable** (`ver74:7946-7964`, ruta `registro→sala_jade→patio→patio_servicios→oficina_servicios`). No-preempción de CRISIS explícita (`anclajes_mision.preempcion`). Reglas de carga: owner sin anclaje→descartar; anclaje sin owner→no liberable por subsistema social; owner con misión cerrada→reconciliar según tabla. `hasta` declarado inerte/simbólico. |
| **N-03** | **RESUELTO** | Práctica: "usar con éxito `piel_cobre` durante el encuentro con `muneco_practica`", sin exigir derrotarlo ni recibir daño. `MOBS.muneco_practica` existe en ver74 (`ver74:7133-7135`, `practica: true`, `loot: []`) y `piel_cobre` es una técnica de guardia autolanzable (`coste 5, guardia 3, duracion 2`, `ver74:4101-4106`) — un evento observable y determinista que no depende de que el muñeco ataque. Recreación: "si murió/desapareció o tras load mientras el paso siga pendiente". Evaluación: el hook de `cmd_meditar` se ubica "después de checks de seguridad… y antes de cualquier rama qi>=qi_max/CONSAGRAR". Contrastado contra el código real: en `ver74:20093-20100` el chequeo de hostiles vivos ocurre primero y la rama `if (p.qi >= p.qi_max)` empieza en la línea 20100 — el hook cae exactamente en el hueco que REV3.1 describe, entre ambos. Esto cierra el soft-lock de "vaso lleno" de forma verificable contra el código, no sólo contra la intención. |
| **N-04** | **RESUELTO** | M04 y M05 declaran actuador y tipo (`evento`/`entrada`) por checkpoint: `HABLAR jiang_rui`, `HABLAR gao_shun`, `ENTER bosque_refugio_patrulla`, `HABLAR xu_an`, `EXAMINAR registros`, `ENTER sauces_casa_huespedes`/`mercado_valle`/`granero_valle`. Cada uno marca explícitamente "sólo con misión activa" y "visitadas históricas no cuentan". `registros` en `sauces_casa_comunal` es scenery real (`ver74:11097-11100`, confirmado con el nombre exacto). |
| **N-05** | **RESUELTO**, con un matiz documental menor (ver §6) | `M06.activacion`: "state-based en `reconciliarProgresionArc1`: M04=HECHA && M05=HECHA && `evidenciaTerritorial.tipos.size>=1` y M06 no activa/hecha → activar M06". Esto cierra exactamente el caso que REV3 señaló como abierto (evidencia reunida *antes* de cerrar M05 nunca disparaba activación). |
| **N-06** | **RESUELTO** | `"otorgamiento": "+1 mérito se ejecuta exactamente en el primer disparo del evento, después de fijar el flag one-shot; el cierre de M04 no vuelve a otorgarlo."` Punto único, sin doble entrega ni omisión. |
| **N-07** | **RESUELTO** | Guarda central: mientras `PILDORA_CONSOLIDACION_OTORGADA && etapa<3 && !transicionLIILIIIHecha`, se rechaza SOLTAR/VENDER/DEPOSITAR/ENTREGAR/TRANSFERIR/limpieza por muerte, salvo el consumidor autorizado `CONSAGRAR_2_3`. Reemisión: máx. 1, gobernada por `PILDORA_REEMITIDA`, fijado a `true` antes de agregar el ítem — cierra el bucle vender→recargar→reemitir que señalaba REV3. Contrastado contra ver74: `pildora_consolidacion` es hoy un ítem de inventario común sin protección especial (`cmd_soltar` en `ver74:19921-19947` es genérico para cualquier ítem del inventario) — confirma que la guarda es, correctamente, un requisito de código nuevo y no algo ya cubierto por el motor. |
| **N-08** | **RESUELTO** | Activación: `HABLAR qiao_ren @ pabellon_disciplina` con M06=HECHA y evidencia≥SUFICIENTE; Jiang Rui se ancla al activar. Tres ramas deterministas, sin rama de rechazo: CAUTA+SUFICIENTE/CONCLUYENTE→cierra CAUTA; FUERTE+CONCLUYENTE→cierra FUERTE; FUERTE+SUFICIENTE→corrección automática a CAUTA, `corregida=true`, sin penalización. Persistencia declarada (`formulacionFinal`, `corregida`). Liberación de Jiang Rui únicamente al cerrar. |
| **N-09** | **RESUELTO** | D1–D7 sincronizadas — ver §9 para el detalle rasgo por rasgo. |
| **N-10** | **RESUELTO_DOCUMENTALMENTE** | Ampliación correcta y suficiente para pasar a contrato sin más decisiones humanas pendientes — ver §11. |

**Regresión nueva: ninguna.** No hay ningún hallazgo que haya empeorado respecto de REV3.

---

## 2. Paridad de archivos: hallazgo de discrepancia

**MD**: el archivo adjuntado en esta conversación (`Reconciliacion_3C6A_Prologo_M01_M07_REV3_1.md`) es **byte-idéntico** al que está en el HEAD verificado del repositorio. Mismo SHA-256 (`6ddf3cff6db22960d78f568bf25cb60ea9fd1354071c230063654cd5457c7070`), coincide con el declarado en `PAQUETE_AUDITORIA_3C6A_REV3_1.md`.

**JSON**: el archivo adjuntado en esta conversación **no es byte-idéntico** al JSON que está en el HEAD verificado del repositorio.

- Hash del JSON adjuntado: `40022e3aae7ea8f5691b92ec367d8763584a60f15d2dd622a6398c5b5a433330` (coincide con el declarado en el paquete como "artefacto local generado").
- Hash del JSON en el repositorio al HEAD `3a9f9e59...`: `96d6a73383fdd5636005460bd3483f3e6b7f8f358a5354fdaa1f76cab0e3d881`.

Diferencia real (diff línea a línea): son dos redacciones del mismo contenido. La inmensa mayoría de las ~35 líneas distintas son reformulaciones más breves o con/sin tildes ("posicion valida" ↔ "posición válida", "activacion" ↔ "activación", `->` ↔ `→`) sin cambio de regla. Dos diferencias sí tienen sustancia, ambas menores:

1. La descripción de la corrección **N-02** en el JSON del repositorio dice *"Tabla completa de anclajes P/M01/M02/M03/M04/M07"* (incluye M03); la versión adjuntada aquí omite M03 en esa frase-resumen. El cuerpo de `misiones[M03].anclajes` (Shen Baojun, Qiao Ren) está presente y es idéntico en ambas versiones — es sólo el resumen de una línea el que está incompleto en el archivo adjuntado. La versión del repositorio es la más precisa.
2. `invariante_afiliacion` en el archivo adjuntado añade explícitamente *"...y no se auto-promueve"* al caso `expulsado`; la versión del repositorio dice sólo *"preservar expulsado"*. Mismo efecto práctico, redacción más explícita en el adjuntado.

**Conclusión de esta sección:** no hay contradicción de reglas entre las dos versiones del JSON, y el HEAD del repositorio (la fuente de verdad para el veredicto) es internamente coherente y coincide con el MD. Pero el paquete de auditoría declara un hash para "el JSON de REV3.1" que **no es el que está en la rama de sólo lectura al HEAD indicado** — es el archivo que además fue adjuntado directamente a esta conversación. Esto no bloquea el cierre, pero debe corregirse antes de considerar "el paquete" trazable de punta a punta.

→ Clasificación: **CORRECCION_DOCUMENTAL** (no bloqueante): sincronizar el artefacto de `PAQUETE_AUDITORIA_3C6A_REV3_1.md` con el JSON real del HEAD, o viceversa, y volver a declarar un único hash canónico.

---

## 3. N-01 — Migración (detalle)

Los doce one-shots pedidos están todos presentes en `migracion_saves_ver74.one_shots_P_M03` (JSON) y en la lista equivalente del MD §5: `raizDiagnosticada`, `equipoInicialEntregado`, `REGISTRO_INICIAL_COMPLETADO`, `NOMBRE_INSCRITO`, `ALOJAMIENTO_CONFIRMADO`, `SERVICIO_DESPENSA_VALIDADO`, `EXAMEN_ESPIRITUAL_APRENDIDO`, `M03_PIEL_COBRE_INSTRUIDA`, `M03_PRACTICA_MUNECO_COMPLETADA`, `EVALUACION_CIRCULACION_SUPERADA`, `M03_PROMOCION_FORMALIZADA`, `TECNICA_PIEL_COBRE_APRENDIDA`. Con `equipoInicialEntregado=true` fijado en la migración, el riesgo de doble entrega en `descansillo` (si la entrega es state-based por ese flag) queda cerrado.

Discriminante: ausente→migrar; presente-y-válido→normalizar/reconciliar; presente-pero-inválido→**fallar cerrado, nunca tratarlo como legacy**. Esto es exactamente lo que REV3 pedía y evita que un `arc1` corrupto dispare una migración sobre datos corruptos.

Etapas: 1→`LI_INTEGRACION`, `transicionLILIIHecha=false`; 2→`LII_TERRITORIO`, `transicionLILIIHecha=true`; ≥3→`LII_TERRITORIO` + `cultivoLIIIPreexistente=true`, con `SECTA_INTERIOR` forzado `false` hasta M04–M07. `SECTA_INTERIOR` legacy=true→`legacySectaInteriorPrevia=true` (sólo diagnóstico) + normalización a `false`/`M12=false`/`ATAJO_ALA_*=false`. `dormitorio_externos` se marca conocido/visitado explícitamente.

No hay rediagnóstico de raíz (`"no volver a ejecutar diagnostico de raiz"`) ni recomputación de saldo/mérito existente. Cierra N-01 sin cabos sueltos.

---

## 4. N-02 — Anclajes (detalle)

Los 10 anclajes de la tabla se contrastaron contra la topología real:

| NPC/Misión | Room | ¿Existe en ver74? |
|---|---|---|
| Tao Ming / P, M01 | `registro` | Sí (`ver74:7724-7743`) |
| Madre Wen / M01 | `patio_cabanas` | Sí (`ver74:7786-7806`) |
| Tao Ming / M02 | `oficina_servicios` | Sí y alcanzable (`ver74:7946-7964`) |
| Chen Bo / M02 | `sala_anatomica` | Sí (`ver74:8396-8414`) |
| Shen Baojun / M03 | `sala_formas` | Sí (`ver74:8102-8120`) |
| Qiao Ren / M03, M07 | `pabellon_disciplina` | Sí (`ver74:8140-8159`) |
| Jiang Rui / M04 | `puesto_valle` | Sí (`ver74:9182-9204`) |
| Gao Shun / M04 | `puerta` → `casa_guardia` | Ambas existen; `casa_guardia` es salida norte de `deposito_comun` (`ver74:7999`) |
| Jiang Rui / M07 | `pabellon_disciplina` → `puesto_valle` | Ambas existen |

No hay ningún NPC de misión anclado en una sala inexistente ni en una sala sin salida de reubicación. El ciclo Tao Ming (P→M01→M02) no deja ningún hueco: se transfiere el owner sin mover en el cierre de P, se reubica atómicamente a `oficina_servicios` al producir `NOMBRE_INSCRITO`, y esa sala ya es donde M02 lo necesita — no hace falta una tercera reubicación. Gao Shun no queda eternamente anclado: se libera "después del control y cuando el jugador sale de `puerta`", a `casa_guardia`, fuera de vista.

No-preempción: declarada explícitamente para CRISIS/PERSONAL/AMBIENTAL sobre cualquier anclaje con owner de misión. Invariantes de carga (owner sin anclaje, anclaje sin owner, owner con misión cerrada) cubiertas. `hasta` declarado explícitamente simbólico, nunca diegético.

**No encontré ningún soft-lock M01→M02 nuevo ni remanente.**

---

## 5. N-03 — M03 (detalle)

- Evento de práctica: usar `piel_cobre` con éxito contra `muneco_practica`, sin exigir derrota ni recibir daño. `piel_cobre` (`ver74:4101-4106`) es una técnica de guardia autolanzable de coste fijo (5 qi) — el jugador puede activarla proactivamente sin depender de que el muñeco ataque primero o de RNG de impacto enemigo. Esto es coherente y observable.
- El muñeco (`MOBS.muneco_practica`, `ver74:7133-7135`) existe en el catálogo de mobs con `practica: true` y `loot: []` — soporta "sin loot de misión" e "instancia de misión, no permanente en ROOMS" sin fricción con el motor.
- Recreación: "si murió/desapareció, o tras load mientras el paso siga pendiente, se recrea" — cierra el caso save/load.
- Evaluación (`EVALUACION_CIRCULACION_SUPERADA`): el hook se coloca "después de checks de seguridad (sin combate activo y sin hostiles vivos) y antes de cualquier rama qi>=qi_max/CONSAGRAR". **Verificado contra el código real**: `cmd_meditar` (`ver74:20087-20100`) comprueba primero `this.vivos.some(m => m.hp > 0)` (línea 20093) y recién en la línea 20100 entra a `if (p.qi >= p.qi_max)`. El hueco entre ambas líneas es exactamente donde REV3.1 pide insertar el evento — no hay ninguna rama intermedia que lo bloquee, y colocarlo ahí garantiza que cuente "aunque no gane qi o el vaso esté lleno", cerrando el soft-lock original de "vaso lleno + M03 pendiente" de forma verificable.

Probé mentalmente los cuatro escenarios pedidos (qi<max, qi=max, etapa 1, etapa 2, vaso lleno con puerta cerrada): en todos, el hook se dispara antes de que `cmd_meditar` decida si hay CONSAGRAR, rechazo de puerta, o ganancia normal de qi — así que ninguno puede impedir que se marque `EVALUACION_CIRCULACION_SUPERADA`.

---

## 6. N-05 + tabla de evidencia M06 (detalle)

**Activación:** `M04=HECHA && M05=HECHA && evidenciaTerritorial.tipos.size>=1 && M06 no activa/hecha → activar M06`, evaluado dentro de `reconciliarProgresionArc1()`. Esto cubre sin ambigüedad los casos A/B (evidencia insuficiente o reunida antes de cerrar M05: el primer chequeo tras cerrar M04/M05 la activa igual) y C/D (3 o 4 tipos ya reunidos: activa igual, sin doble beneficio ni bloqueo — "state-based: `nivel>=SUFICIENTE` aunque los 3 tipos se hubieran reunido antes de activar M06").

**Matiz no cerrado (menor):** la lista de puntos donde se invoca `reconciliarProgresionArc1()` —cierres M04/M05/M06/M07, CONSAGRAR 2→3, carga/migración— no incluye explícitamente "al registrar un nuevo tipo de evidenciaTerritorial". Es decir: si el jugador cierra M04 y M05 con **cero** evidencia y **después** examina una fuente de evidencia por primera vez, el documento no dice que esa acción de EXAMINAR dispare la reconciliación en el acto; formalmente, M06 podría no activarse hasta el siguiente punto de la lista (el más próximo y trivial de alcanzar es un guardado/carga). No es un soft-lock — cualquier acción de guardado/carga lo resuelve, y `PATRULLA_TERRITORIAL` (ventana de recolección) ya supone que el jugador puede seguir jugando con normalidad — pero es una laguna de especificación que conviene cerrar explícitamente antes del contrato.

→ Clasificación: **CORRECCION_DOCUMENTAL**, severidad baja. Añadir: *"reconciliarProgresionArc1() se invoca también inmediatamente después de registrar un tipo nuevo en evidenciaTerritorial."*

**Tabla concreta de evidencia (8 fuentes, 4 tipos):**

| Tipo | Fuente | Estado de verificación en extractos disponibles |
|---|---|---|
| PATRON_TERRITORIAL | `bosque_refugio_patrulla.registro` | **VERIFICADO**: scenery `registro` existe literalmente en `ver74:9696-9719` |
| PATRON_TERRITORIAL | `bosque_puesto_marcas.tablillas` | Sala **confirmada indirectamente**: `bosque_puesto_marcas` aparece como territorio real del errante `serpiente_bambu` (`ver74:3701-3712`). El scenery `tablillas` puntual **no aparece en los extractos entregados** (07/08/09) — **NO VERIFICADO EN EXTRACTOS**, no contradicho. |
| DESPLAZAMIENTO_FAUNA | `bosque_collado_alto.huellas` | **NO VERIFICADO EN EXTRACTOS** — la sala no aparece en los extractos 01–09 entregados. |
| DESPLAZAMIENTO_FAUNA | `aguas_poza_profunda.marcas` | **NO VERIFICADO EN EXTRACTOS**, ídem. |
| ALTERACION_VEGETAL | `aguas_senda_bosque.vegetacion` | **NO VERIFICADO EN EXTRACTOS**, ídem. |
| ALTERACION_VEGETAL | `terraza_cantera.vegetacion` | **NO VERIFICADO EN EXTRACTOS**, ídem. |
| ALTERACION_HIDRICA | `aguas_cauce_alto.corriente` | **NO VERIFICADO EN EXTRACTOS**, ídem. |
| ALTERACION_HIDRICA | `aguas_paso_piedras.corriente` | **NO VERIFICADO EN EXTRACTOS**, ídem. |

Nota importante: el propio JSON REV3.1 sólo declara `scenery_verificado_ver74` explícitamente para las dos fuentes del incidente de M04 (`bosque_puesto_marcas.tablillas`, `bosque_refugio_patrulla.registro`) — **no** hace esa misma declaración de verificación para las otras 6 fuentes de la tabla de M06. Es decir, la propia REV3.1 no afirma haber verificado esas 6 contra ver74 línea por línea; sólo compromete la tabla como especificación a implementar y a comprobar en el contrato. Dado que ninguna de esas 6 salas apareció tampoco como contradicha en ningún extracto (áreas `bosques`/`aguas_barrancos`/`cantera_vetas` son áreas reales y consistentes con la nomenclatura de salas ya vista: `bosque_*`, `aguas_*`, y "cantera" aparece en `terraza_cantera`, coherente con el área de canteras del mundo de 329 salas), no hay señal de que estas salas o su scenery no existan — pero tampoco puedo confirmarlo con la evidencia entregada en esta sesión.

→ Clasificación: **CAMBIO_NECESARIO_3C6** (no bloqueante para el veredicto de esta auditoría documental, pero si el contrato quiere evitar retrabajo): antes de implementar, confirmar contra el `.html` completo (no sólo extractos) la existencia literal de las 6 salas/scenery restantes y, si alguna falta, sustituir esa fuente conservando 2 fuentes independientes por tipo. Esto **no invalida N-05** (la lógica de activación de M06 es correcta independientemente de cuántas fuentes existan) y **no bloquea** el veredicto de esta auditoría, porque ≥3 tipos alcanzables ya están respaldados por el diseño (2 tipos con al menos una fuente cada uno ya confirmada o fuertemente indiciada: PATRON_TERRITORIAL con `bosque_refugio_patrulla.registro` verificado).

---

## 7. N-04 + N-06 — M04/M05 (detalle)

M04: los cuatro checkpoints (`M04_ASIGNADA`, `M04_CONTROL_PUERTA`, `M04_REFUGIO_ALCANZADO`, `M04_RETORNO_INFORMADO`) están tipados como `evento`/`entrada` con actuador y sala explícitos, y `M04_CONTROL_PUERTA` anota expresamente "no usar visitadas; puerta ya fue visitada en P" — cierra la ambigüedad que REV3 señalaba sobre si el checkpoint podía colarse por `visitadas` históricas.

Incidente opcional: dos disparadores (`EXAMINAR tablillas`/`EXAMINAR registro`), sin RNG, one-shot, +1 mérito otorgado "exactamente en el primer disparo del evento, después de fijar el flag; el cierre de M04 no vuelve a otorgarlo" — descarta doble otorgamiento y omisión.

M05: los cuatro checkpoints (`M05_VALLE_LOGISTICA_REVISADA`, `M05_XU_AN_CONTACTADO`, `M05_CIRCUITO_REGISTRADO`, `M05_HOSPEDAJE_VISITADO`) tienen actuador (`ENTER`/`HABLAR`/`EXAMINAR`) y todos están marcados "sólo con M05 activa" o "visitadas históricas no cuentan" — resuelve el hueco de actuador indefinido que REV3 señalaba para "registrar el circuito" y "contactar a Xu An". `M05_CIRCUITO_REGISTRADO` requiere explícitamente `M05_XU_AN_CONTACTADO` primero, sin crear una dependencia circular ni un orden imposible dado el layout real de Sauces (`sauces_plaza`↔`sauces_casa_comunal`↔`sauces_casa_huespedes`, todas confirmadas en `ver74:11028-11071`).

---

## 8. N-07 — Píldora (detalle)

Condición de protección: `PILDORA_CONSOLIDACION_OTORGADA && etapa<3 && !transicionLIILIIIHecha`. Bajo esa condición se rechaza cualquier vía de remoción/transferencia salvo `CONSAGRAR_2_3`. Intenté "romperla" mentalmente por las nueve vías pedidas:

- SOLTAR/VENDER/DEPOSITAR/ENTREGAR/TRANSFERIR: cubiertas explícitamente por `vias_cubiertas`.
- Pérdida por muerte: cubierta ("limpieza por muerte si existe").
- Cargar un save sin el ítem: cubierto por la reemisión (`PILDORA_REEMITIDA=false` + falta el ítem → reemitir una vez, fijando el flag antes de agregarlo, así que no puede reemitir dos veces aunque se recargue el mismo save repetidamente).
- Cargar repetidamente: como el flag se fija *antes* de agregar el ítem y es persistente, recargar el mismo punto de guardado no reemite una segunda vez.
- Duplicar el ítem antes del gate: la guarda es sobre remoción/transferencia, no sobre duplicación; pero no hay ninguna vía de duplicación descrita en REV3.1 ni en ver74 para `pildora_consolidacion` fuera de loot de mobs (`serpiente_qi`, `avispa_jade`, etc., con probabilidad — no controlable por el jugador de forma determinista) — no detecté un bucle económico documental.

Contrastado contra ver74: `pildora_consolidacion` es hoy un ítem de inventario ordinario (reliquia, precio 8, `ver74:6843-6846`) sin protección especial, y `cmd_soltar` (`ver74:19921-19947`) es completamente genérico — confirma que la guarda central es, correctamente, trabajo de código nuevo (ya listado en "requisitos técnicos para el contrato"), no algo que REV3.1 esté asumiendo incorrectamente que ya existe.

---

## 9. N-08 — M07 (detalle)

Activación determinista (`HABLAR qiao_ren` con M06=HECHA y evidencia≥SUFICIENTE), anclaje de Jiang Rui al activar, tres ramas sin rama de rechazo, persistencia de `formulacionFinal`/`corregida`, liberación de Jiang Rui únicamente al cerrar con "escena de salida diegética y reubicación atómica a `puesto_valle`". Recompensa (contribución 4, mérito 3, comprensión 1) y gate (abre LII→LIII) son fijos independientemente de la formulación — "efecto_mecanico: ninguno sobre recompensas/gates" está declarado explícitamente. No hay ruta muerta: las tres combinaciones posibles de formulación×nivel de evidencia (CAUTA+SUFICIENTE/CONCLUYENTE, FUERTE+CONCLUYENTE, FUERTE+SUFICIENTE) están todas resueltas; no existe FUERTE+INSUFICIENTE porque M07 exige evidencia≥SUFICIENTE para activarse.

---

## 10. N-09 — Paridad MD↔JSON (D1–D7)

| # | Divergencia REV3 | Estado en REV3.1 |
|---|---|---|
| D1 | Estado inicial de facción = `inactivo` | **SINCRONIZADO**: MD §2 ("Nueva partida: `player.facciones.grulla_blanca.estado = inactivo`") y JSON (`faccion_economica.estado_inicial_nueva_partida: "inactivo"`, `paridad_md_json.estado_inicial_faccion: "inactivo"`) dicen exactamente lo mismo. |
| D2 | Puntos de evaluación LII→LIII + ceremonia | **SINCRONIZADO**: MD §4 lista los mismos cuatro puntos (cierres M04-M07, CONSAGRAR 2→3, carga/migración, reconciliación) y menciona "presentación ceremonial one-shot"; JSON los repite en `gates.LII_LIII.evaluacion_en` y `paridad_md_json.LII_LIII_evaluacion_en`/`LII_LIII_presentacion`. |
| D3 | Secuencia M02 (fusión vs. pasos separados) | **SINCRONIZADO en contenido**: MD §8 y JSON `misiones[M02].objetivos_en_orden` describen la misma secuencia (Tao Ming→depósito/rata→cadáver→Chen Bo→observar→informar); la redacción sigue siendo distinta entre ambos documentos (uno más compacto que otro) pero ya no hay omisión de contenido, sólo estilo — esto es aceptable como paridad de regla, no de prosa literal. |
| D4 | Id `M03_PRACTICA_MUNECO_COMPLETADA` | **SINCRONIZADO**: aparece en MD §9 y en JSON (`misiones[M03].pasos[1].id`, `paridad_md_json.M03_practica_id`). |
| D5 | `sospechaFuerte` para 3/4 tipos + áreas de M06 | **SINCRONIZADO**: MD §12 tabla del evaluador coincide exactamente con JSON `evidencia.evaluador` (1→false, 2/3/4→true); áreas (`bosques`, `aguas_barrancos`, `cantera_vetas`) están en JSON `misiones[M06].areas` y `paridad_md_json.M06_areas`; el MD no repite la lista de áreas palabra por palabra pero no la contradice. |
| D6 | Migración: `NOMBRE_INSCRITO`, dormitorio, `transicionLILIIHecha` por etapa | **SINCRONIZADO**: presentes en MD §5 y en JSON `migracion_saves_ver74`/`paridad_md_json.migracion_incluye`. |
| D7 | Invariantes 329/17/787 + sin tiempo diegético | **SINCRONIZADO**: MD §1 los declara en prosa ("329 rooms / 17 areas / 787 directed exits / 0 broken reciprocity / 0 isolated rooms / 1 physical component" + "sin tiempo diegético"); JSON los repite como lista en `alcance.invariantes` y `paridad_md_json.invariantes_mundo`. Idénticos en sustancia. |

**No basta con "compatibles": confirmo que expresan la misma regla en los siete casos**, con la única salvedad de D3 (redacción distinta pero regla idéntica, lo cual es aceptable — MD y JSON no tienen por qué ser el mismo texto, sólo no pueden contradecirse, y no se contradicen).

---

## 11. N-10 — Cambios técnicos: ¿suficientemente especificados para el contrato?

Repasé la lista de "requisitos_tecnicos_para_contrato" (20 ítems en el JSON) contra lo que verifiqué del código real. Para cada rubro pedido:

- **`normalizarFacciones`, estado `inactivo`, separación contribución/mérito**: especificado sin ambigüedad ("`otorgarContribucion` aumenta sólo saldo; `otorgarMerito` aumenta sólo mérito; `normalizarFacciones` no fuerza `merito>=saldo`"). Verificado contra ver74 que **hoy** `normalizarFacciones` (`ver74:18892-18913`) sí crea con `estado:"miembro"` por defecto y sí fuerza `registro.merito = Math.max(registro.saldo, ...)` — confirma que la especificación apunta exactamente al código que hay que tocar, sin inventar un problema inexistente.
- **Separar historial de contribución/mérito**: especificado ("el historial debe distinguir una entrada de contribución de una de mérito"). Verificado que `otorgarContribucion` hoy (`ver74:18954-18968`) escribe `tipo:"ingreso"` en el historial sin distinguir contribución de mérito y **también incrementa `merito` a la vez que `saldo`** — confirma que además de separar el historial, `otorgarContribucion` debe dejar de tocar `merito` (ya cubierto por el ítem de separación de semántica) y que hace falta una función `otorgarMerito` nueva, que hoy no existe en el extracto disponible.
- **Auditar callers de `otorgarContribucion`**: listados (`entregarRecompensa`, test de persistencia, definición). Verificado: `entregarRecompensa` (`ver74:17191-17204`) en efecto la llama, y su firma actual (`piedras, qi, comprension, contribucion`) **no tiene parámetro de mérito** — esto es información útil para el contrato: la extensión de `entregarRecompensa` (o una ruta paralela) para mérito es trabajo necesario no explicitado en detalle de firma, pero sí cubierto conceptualmente por el requisito de separación. Aceptable como especificación de alto nivel para un documento que explícitamente "no implementa código".
- **Reemplazar `gestionarMisionesNpc`**: verificado que es hoy un stub literal (`ver74:18869-18871`, `return "";`) — confirma la necesidad tal cual está declarada.
- **`cambiarEstadoFaccion` ya admite `inactivo`**: verificado (`ver74:18926-18932`, lista `["miembro","huesped","aliado","inactivo","expulsado"]` ya incluye `inactivo`) — REV3.1 acierta al no pedir tocar esta función.
- **Wrapper de rata M02, instancia de muñeco M03, hook de MEDITAR, guardia de píldora, tabla de evidencia, `normalizarArc1`+migración, tests legacy, no tocar `ROOMS.exits`/errantes, schema 2**: todos estos ítems están descritos con suficiente precisión operativa (qué función, qué condición, qué efecto) para que un implementador no tenga que tomar una decisión de diseño nueva; son decisiones ya cerradas por REV3/REV3.1, no ambigüedades.

**Conclusión N-10:** la ampliación es completa y estas piezas pertenecen naturalmente al contrato de implementación (no son "faltantes documentales" disfrazadas de trabajo de código) — corresponde `RESUELTA_DOCUMENTALMENTE`, no una reapertura del hallazgo.

---

## 12. Normalización fail-closed (saves corruptos)

Repasé las ocho normas de `persistencia.normalizacion_carga` contra los ocho escenarios pedidos:

| Save corrupto | Regla aplicable | Resultado |
|---|---|---|
| M05=hecha, M04 no hecha | "coherencia de cadena: downstream HECHA con prerequisito no HECHO se degrada fail-closed" | Degrada M05 a no-hecha. Correcto. |
| M07=hecha, M06 no hecha | Misma regla | Degrada M07. Correcto. |
| evidencia.nivel=CONCLUYENTE, tipos=[] | "nivel y sospechaFuerte se derivan de tipos" | Se recalcula desde `tipos` (vacío→INSUFICIENTE), ignorando el valor persistido. Correcto. |
| informeFronteraAceptado=true, M07 no hecha | "informeFronteraAceptado se deriva de M07=HECHA" | Se recalcula a false. Correcto. |
| arc1.estado=LIII sin requisitos | "arc1.estado no puede superar lo sostenido por etapa+quests+flags válidos" | Se degrada a lo que los datos válidos sostengan. Correcto. |
| owner de NPC sin anclaje | "owner sin anclaje ⇒ descartar owner" | Correcto. |
| anclaje de misión sin owner | "anclaje sin owner de misión ⇒ no lo libera el subsistema social" | Correcto (no promueve, no rompe; simplemente el social no lo toca — coherente con fail-closed en el sentido de "no actuar sobre datos ambiguos"). |
| quest con estado desconocido | "estado desconocido ⇒ descartar/no-hecha; nunca promover" | Correcto. |

**Las ocho reglas implican degradar/recomputar/rechazar, nunca promover.** No encontré ningún camino de carga que suba `arc1.estado`, marque una quest como hecha sin sus prerrequisitos, o reactive `SECTA_INTERIOR`/`M12`/`ATAJO_ALA_*` a partir de un save corrupto.

---

## 13. Economía

Verificado contra ver74 (`ver74:18954-18968`): `otorgarContribucion` hoy sólo rechaza `registro.estado === "expulsado"` — confirma que M02 puede otorgar +1 contribución con la facción en estado `inactivo` (antes de M03), tal como REV3.1 asume.

`normalizarFacciones` (`ver74:18892-18913`) es, confirmado, la función a corregir: hoy defaultea a `miembro` y fuerza `merito>=saldo`. REV3.1 lo señala correctamente como cambio pendiente, no como algo ya resuelto.

Totales confirmados por suma directa de las recompensas por misión en el JSON (`economia_rev3.recompensas`): Contribución 1(M02)+0(M03)+2(M04)+3(M05)+2(M06)+4(M07) = **12**. Mérito 0+0+0(M04 sin incidente)+0+1(M06)+3(M07) = **4**; con incidente M04 (+1) = **5**. Comprensión: 1 (M07). Píldora: 1 (M05). **Todos coinciden con lo declarado.**

La inalcanzabilidad de los servicios de mérito 8/20 durante LII (máximo teórico 5 mérito en partida nueva, confirmado contra `FACCIONES.grulla_blanca.servicios` en `ver74:14503-14510`: `claridad` exige mérito 8, `consolidacion` exige mérito 20) es, como dice REV3.1, una decisión de balance ya aceptada, no un defecto de esta revisión — la trato como tal y no la reabro.

---

## 14. Regresiones

Repasé la lista de invariantes que REV3.1 declara no tocar, contra `alcance.invariantes` del JSON y contra el código de auditoría del mundo (`auditarMundo329`, `ver74:2317-2346`, que exige exactamente 329 rooms/17 áreas/787 exits/0 rotas/0 aisladas/1 componente): REV3.1 no requiere ni implica cambiar ninguno de esos números, no toca `ROOMS.exits` (el muñeco de M03 es una instancia derivada de estado, no una entrada nueva en `ROOMS`; la tabla de evidencia de M06 es explícitamente externa a `ROOMS`), no agrega ni quita errantes globales (`rata_despensa` es el errante `rata_qi` ya existente, reutilizado con wrapper local), no reescribe 3C.4 globalmente, no introduce tiempo diegético (`hasta` es simbólico por declaración expresa), no sube `SAVE_SCHEMA_VERSION` (sigue en 2, y no hay clave top-level nueva fuera de `flags`, que ya es libre), y no abre `M12`/`ATAJO_ALA_*` antes de la transición oficial (la migración normaliza explícitamente cualquier caso legacy a `false`). **Sin regresiones.**

---

## 15. Clasificación final de hallazgos

**BLOQUEANTE:** ninguno.

**CORRECCION_DOCUMENTAL** (no bloqueante, recomendable antes de redactar el contrato):
- Sincronizar el hash/artefacto del JSON declarado en `PAQUETE_AUDITORIA_3C6A_REV3_1.md` con el JSON real del HEAD `3a9f9e59...` (§2).
- Declarar explícitamente que `reconciliarProgresionArc1()` se invoca también al registrar un nuevo tipo de `evidenciaTerritorial`, no sólo en cierres de misión/CONSAGRAR/carga (§6).

**CAMBIO_NECESARIO_3C6** (trabajo del contrato, no de esta revisión documental):
- Confirmar contra el `.html` completo (no sólo extractos) la existencia de las 6 fuentes de evidencia de M06 no verificadas en esta sesión (`bosque_collado_alto`, `aguas_poza_profunda`, `aguas_senda_bosque`, `terraza_cantera`, `aguas_cauce_alto`, `aguas_paso_piedras`) antes de implementar la tabla; sustituir cualquiera que no exista, conservando 2 fuentes por tipo (§6).
- Todos los ítems ya listados en `requisitos_tecnicos_para_contrato` (§11) — confirmados como necesarios y bien dirigidos, no nuevos.

**ENDURECIMIENTO_FUTURO:**
- N-11 de la auditoría REV3 (relación `estadoAfiliacion`↔`facciones.…estado`, servicios de facción inalcanzables en LII por diseño) permanece como endurecimiento futuro; no crea soft-lock ni contradice el contrato — se mantiene sin reabrir, tal como autoriza el alcance de esta auditoría.

**EDITORIAL_NO_BLOQUEANTE:**
- Las diferencias de redacción (tildes, brevedad, `->` vs `→`) entre el JSON adjuntado y el del repositorio, más allá de la línea de N-02 ya señalada como corrección documental.

---

## 16. Condición de aptitud — verificación punto por punto

- N-01…N-09 RESUELTOS: **cumplido**.
- N-10 RESUELTO_DOCUMENTALMENTE: **cumplido**.
- MD y JSON equivalentes: **cumplido** (con la salvedad de paridad de archivo físico en §2, no de contenido normativo).
- Sin soft-lock documental medio/alto: **cumplido**.
- Migración legacy cerrada: **cumplido**.
- Anclajes cerrados: **cumplido**.
- M03 sin soft-lock de vaso lleno: **cumplido, verificado contra el código real de `cmd_meditar`**.
- M06 activación state-based: **cumplido**, con el matiz menor de §6.
- Píldora sin exploit: **cumplido**.
- Schema 2 viable: **cumplido**.

---

## 17. Veredicto

`3C6A_REV3_1_APTA_PARA_CONTRATO`