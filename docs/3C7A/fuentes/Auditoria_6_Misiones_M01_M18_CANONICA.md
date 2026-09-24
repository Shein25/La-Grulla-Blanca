# Auditoría 6 — Consolidación canónica del Prólogo + M01–M18
## La Grulla Blanca — Arco 1

**Tipo:** auditoría exclusivamente documental, narrativa, estructural y de estados. No modifica `grulla-blanca_ver68.html`, no implementa las 329 salas, no resuelve M2 ni Auditoría 5, no avanza a 3C.

---

## 1. Resumen ejecutivo

El Prólogo y las 18 misiones principales del Arco 1 (P + M01–M18) están **narrativamente completos a nivel de diseño jugable** en la Fuente Maestra, concentrados casi enteramente en seis turnos: `T286` (Prólogo+M01–M03), `T287` (M04–M07), `T288` (M08–M12), `T289` (M13–M15), `T290` (M17–M18) y `T281` (M16). `T254` aporta la matriz maestra (requiere/produce/abre/NPC/gates/compañeros) y `T257` el contrato de idempotencia. El propio **Backup Maestro de Continuidad** (autoridad máxima del proyecto) no aporta contenido narrativo adicional sobre las misiones: en su sección 50 remite exactamente a estos mismos turnos como fuente de la Auditoría 6, y su sección 51 es una matriz resumida que coincide con `T254`. Por tanto, para el contenido puramente narrativo de P–M18, el nivel 1 (decisión explícita más reciente) y el nivel 5 (Fuente Maestra) de la jerarquía de autoridad **no entran en conflicto**: coinciden.

Verificación técnica directa sobre `grulla-blanca_ver68.html` (grep sobre `QUESTS`, `MISIONES_ACTO_1` y nombres propios) confirma que **ninguna** misión P–M18 está implementada hoy: ver68 ejecuta íntegramente la campaña antigua (Acto I–IV: ratas, duelo/Fan Ji, hierbas, origen_personal, huerto_jade, jade/Shen Liang, veta_y_horno, peces_lunares, devoradores, memorias_verticales, reliquias_verticales, cazadores_verticales, guardianes_ocultos). Las fuentes narrativas declaran explícitamente reemplazado solo un subconjunto de ese contenido (ver §10).

Las 19 unidades tienen requisitos, productos, gates, NPC, revelaciones (R1–R10) y reglas de idempotencia trazables. Los anclajes espaciales citados literalmente en las fuentes (33 room_id) se verificaron uno a uno contra `Topologia_329_Estructurada_v2.json` y **todos existen** en el área declarada (`CONFIRMADO_329`). Varias localizaciones mencionadas solo en prosa (el almacén de M02, el sector marcial de M03, la Sala Anatómica de M10, etc.) no tienen un `room_id` literal en las fuentes leídas y quedan marcadas `DESTINO_329_PENDIENTE`, sin inferencia por semejanza de nombre.

M16 tiene dos pasadas en la Fuente Maestra: `T260` (versión anterior) y `T281` (revisión posterior y versión canónica vigente, tal como lo identifica el propio índice de `ver55`). Esta auditoría usa `T281` como fuente canónica de M16, sin evidencia de una revisión adicional posterior a `T281`.

**Declaración de cierre de esta auditoría (ver §15): `CADENA DOCUMENTAL CONSOLIDADA`, condicionada a las decisiones humanas pendientes listadas en §14.** No se declara "misiones listas para implementar".

---

## 2. Método y jerarquía de fuentes

### 2.1 Jerarquía de autoridad aplicada
- 1. Decisiones explicitas nuevas (Backup Maestro de Continuidad 2026-09-21)
- 2. Auditoria_3U_Mapa_329_Salas_CANONICA.md
- 3. Topologia_329_Estructurada_v2.json
- 4. Auditoria_3B_Validacion_Topologia_329.md (solo diagnostico historico; 3B2 no fue adjuntado, se usa 3B/3U como equivalentes disponibles)
- 5. La_Grulla_Blanca_Fuente_Maestra_Fusionada_ver55.md
- 6. Auditoria_C1_Maquinas_Narrativas_Companeros.md
- 7. Auditoria_M1_Dependencias_Rooms_ver67.md
- 8. Auditoria_4B_Movilidad_Postas_Carruajes_CORREGIDA.md
- 9. Informe_Etapa_2B_Atlas_Areas.md
- 10. grulla-blanca_ver68.html (solo comparacion tecnica)

### 2.2 Nota metodológica

Las fichas de mision (P + M01-M18) se reconstruyeron principalmente a partir de los turnos que el propio Backup Maestro (seccion 50) senala como fuentes principales de la Auditoria 6: T286 (Prologo+M01-M03), T287 (M04-M07), T288 (M08-M12), T289 (M13-M15), T290 (M17-M18), mas M16 (T260 -> version anterior; T281 -> revision posterior y version canonica vigente, segun el propio indice de ver55; no existe una revision M16 posterior a T281 dentro de ver55, que termina en T293), T254 (matriz maestra con columnas REQUIERE/PRODUCE/ABRE/NPC/gates/companeros) y T257 (contrato de idempotencia). T168/T169/T197/T222 son versiones mas tempranas de la misma columna vertebral narrativa; se revisaron sus encabezados para confirmar que T254/T286-290 no las contradicen en ningun punto detectado, por lo que no se citan como fuente independiente en cada ficha. El Backup Maestro de Continuidad no contiene fichas narrativas propias de M01-M18 (su seccion 51 es solo una matriz resumida REQUIERE/PRODUCE que coincide con T254); su autoridad maxima aplica a topologia, IDs de area y estado de proyecto, no aporta contenido narrativo adicional o distinto sobre las misiones.

### 2.3 Verificación técnica sobre ver68

ver68 implementa unicamente la campana narrativa antigua (Acto I-IV): ratas, duelo (Fan Ji), hierbas, origen_personal, huerto_jade (opcional), jade (Shen Liang), veta_y_horno (opcional), peces_lunares, devoradores, memorias_verticales, reliquias_verticales, cazadores_verticales (opcional), guardianes_ocultos (opcional). No existe ninguna estructura P/M01-M18, ni arc1.estado, ni los permisos del nuevo diseno (PATRULLA_TERRITORIAL, SECTA_INTERIOR, FORMACIONES_INVESTIGACION, NUCLEO_PROFUNDO, etc.). Por tanto TODAS las misiones P-M18 son NO_IMPLEMENTADO en ver68 salvo donde se identifica explicitamente contenido legacy que las fuentes narrativas declaran reemplazado (LEGACY_A_REEMPLAZAR): M02<-ratas, M03<-duelo/Fan Ji, M12/M17<-reliquias_verticales (Sombra/Centinela como llaves), M18<-tramo final eco_grulla/altar/reliquias. El resto de contenido legacy (jade/Shen Liang, huerto_jade, veta_y_horno, peces_lunares, devoradores, memorias_verticales, cazadores_verticales, guardianes_ocultos, origen_personal) no tiene una correspondencia declarada en las fuentes leidas con ninguna mision P-M18 especifica; su destino (eliminar / convertir en contenido lateral opcional / Arc2) queda NO CERRADO EN FUENTE para efectos de esta auditoria.

### 2.4 Salas verificadas contra Topología v2

Se verificó programáticamente la existencia y el área de cada `room_id` citado literalmente en las fuentes narrativas de P–M18, contra `Topologia_329_Estructurada_v2.json`. Las 33 salas siguientes existen y su área coincide con lo descrito en la fuente narrativa (`CONFIRMADO_329`):

`patio_raices`, `descansillo`, `mirador_niebla`, `patio_practica`, `sendero_pinos`, `camino`, `puerta`, `registro`, `sala_jade`, `dormitorio_externos`, `bosque_refugio_patrulla`, `sauces_casa_huespedes`, `formaciones_sello_antiguo`, `formaciones_descenso_tecnico`, `ala_vestibulo`, `ala_nudo_seis_corrientes`, `ala_camara_dos_alas`, `ala_umbral_mantenimiento`, `mantenimiento_acceso`, `mantenimiento_dormitorio_turnos`, `mantenimiento_compuerta_nucleo`, `nucleo_pozo_voto`, `nucleo_camara_voto`, `nucleo_galeria_primer_pacto`, `nucleo_primer_pacto`, `nucleo_archivo_promesa`, `nucleo_descenso_pulso`, `nucleo_galeria_pulso`, `nucleo_camara_regulacion`, `nucleo_sala_relevo`, `nucleo_exterior_ancla`, `nucleo_camara_memoria`, `nucleo_umbral_santuario`, `nucleo_santuario_vinculo`, `mojon_regional`

### 2.5 Convención de etiquetas
- CONFIRMADO_329 / ID_HISTORICO / DESTINO_329_PENDIENTE / EXTERNO_ARC1_DOCUMENTADO (anclajes espaciales)
- NO CERRADO EN FUENTE / NO RECUPERADO / NO FORMALIZADO / PROPUESTA_NO_CANONICA / OBSOLETO / DECISION_HUMANA_PENDIENTE (huecos)

---

## 3. Matriz canónica principal — P + M01–M18

| ID | Nombre | Etapa Arc1 | Requiere | Produce | Abre | NPC principales | Área/s | Gate/autorización | Revelaciones | Estado documental | Estado ver68 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P | La Piedra y la Puerta | PROLOGO | Nueva Partida valida | estadoAfiliacion=ADMITIDO; PROLOGO=HECHO; arc1.estado=LI_INTEGRACION | M01 | Tao Ming, guardia de la Puerta Roja, ayudante de ingreso | acceso | entrada a LI | — | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M01 | Un nombre entre miles | LI_INTEGRACION | PROLOGO=HECHO; arc1.estado=LI_INTEGRACION | rango=ASPIRANTE; SECTA_EXTERIOR_BASE; alojamiento conocido: dormitorio_externos | M02 (junto con otras condiciones) | Tao Ming, Madre Wen, Gao Shun (opcional) | secta_exterior | necesaria para continuar LI | — | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M02 | Trabajo que alguien debe hacer | LI_INTEGRACION | M01=HECHA | primerServicioFormal=true; Examen Espiritual desbloqueado; Contribucion pequeña | M03 (junto con otras condiciones) | Tao Ming / Ma Qiren o Madre Wen (informan), Chen Bo (ensena Examen) | secta_exterior | 'primer servicio formal' es componente del gate LI->LII | — | CANÓNICO (T254/T286–T290/T281) | LEGACY_A_REEMPLAZAR |
| M03 | Aprender a permanecer | LI_INTEGRACION | M01=HECHA; M02=HECHA; condiciones basicas de cultivo apropiadas | rango: ASPIRANTE->DISCIPULO_EXTERNO; estadoAfiliacion=MIEMBRO; evaluacionCirculacion=SUPERADA; acceso a Piel de Cobre como formacion basica | M04 (tras gate LI->LII) | Shen Baojun, Qiao Ren (supervision institucional, no obligatoria en escena) | secta_exterior | gate LI->LII: qi>=25 + rango==DISCIPULO_EXTERNO + primerServicioFormal + evaluacionCirculacion==SUPERADA | — | CANÓNICO (T254/T286–T290/T281) | LEGACY_A_REEMPLAZAR |
| M04 | Más allá de la Puerta Roja | LII_TERRITORIO | arc1.estado=LII_TERRITORIO (tras gate LI->LII); rango=DISCIPULO_EXTERNO | PATRULLA_TERRITORIAL (permiso, fuente=MISION, origen=M04); refugio bosque_refugio_patrulla conocido | M05 | Jiang Rui, Gao Shun | secta_exterior, bosques | componente del servicio territorial LII | — | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M05 | Los caminos de la Grulla | LII_TERRITORIO | M04=HECHA o servicio territorial suficientemente iniciado | reconocimientoSauces=HUESPED; sauces_casa_huespedes conocido (alojamiento) | M06 (como parte de la combinacion de condiciones) | Duan Shibo o Jiang Rui, Han Qiao (opcional, HAN_02_PROCEDIMIENTO), Xu An, Mei Shufen | valle, produccion, sauces | contribuye al conocimiento territorial (no es gate duro por si sola) | — | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M06 | Lo que no debería estar aquí | LII_TERRITORIO | M04 y M05 suficientes para conocer el territorio (no exige combinacion unica) | conocimiento.anomaliasTerritoriales -> SOSPECHA/PARCIAL fuerte; R1=PARCIAL | M07 | Jiang Rui, Ma Gu, patrullas, Zhao Wen/Mei Lian/Lin Yue (segun lugar) | bosques, aguas_barrancos, cantera_vetas | — | R1 PARCIAL | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M07 | Informe de frontera | LII_TERRITORIO | M06=HECHA; evidenciaTerritorial>=SUFICIENTE | informeFronteraAceptado=true; R1=CONFIRMADO; Comprension +1 (ARC1_M07_PATRON_TERRITORIAL) | M08, M09, M10 (tras gate LII->LIII y avance de cultivo) | Jiang Rui, Qiao Ren, He Zhen (consulta breve, no revela R2), Ren Bo, Su Lian | secta_exterior | requisito narrativo principal para gate LII->LIII | R1 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M08 | Una montaña que no coincide consigo misma | LIII_INVESTIGACION | arc1.estado=LIII_INVESTIGACION; SECTA_INTERIOR concedido | FORMACIONES_INVESTIGACION (permiso); R2=CONFIRMADO | M11 (junto con M09/M10) | He Zhen, Wen Tao | formaciones | componente de M11 | R2 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M09 | Los nombres que faltan | LIII_INVESTIGACION | arc1.estado=LIII_INVESTIGACION | ARCHIVO_COMUN (inicio); ARCHIVO_RESTRINGIDO (progreso, autorizado por Qiao Ren); R3=PARCIAL | M11 (junto con M08/M10) | Song Rui, Zhao Wen, Qiao Ren (autoriza ARCHIVO_RESTRINGIDO), Luo Yan (discusion), Yu Shun | archivos, secta_interior | componente de M11 | R3 PARCIAL | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M10 | El cuerpo recuerda | LIII_INVESTIGACION | arc1.estado=LIII_INVESTIGACION | R4=CONFIRMADO | M11 (junto con M08/M09) | Lan Meihua, Chen Bo, Guo Chen (relacion tematica), Luo Yan (oposicion por riesgo) | medicina | componente de M11 | R4 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M11 | Las Dos Alas | LIII_INVESTIGACION | M08=HECHA; M09=HECHA; M10=HECHA | R3=CONFIRMADO; DOS_ALAS=PRINCIPIO; SEGUNDA_RAMA=APLICACION_CORPORAL; Comprension +1 (ARC1_M11_DOS_ALAS) | M12 | He Zhen, Song Rui, Lan Meihua | formaciones, archivos, medicina | requisito directo de M12 | R3 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M12 | La red que nadie dibuja | LIII_INVESTIGACION | M11=HECHA | PRIMERA_ALA_INVESTIGACION (permiso); R5=CONFIRMADO; Comprension +1 (ARC1_M12_RED_PRIMERA_ALA); ala_umbral_mantenimiento conocido | M13 (tras gate LIII->LIV) | He Zhen, posiblemente Song Rui/Wen Tao | formaciones, primera_ala | principal LIII->LIV | R5 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M13 | Todo consume algo | LIV_REVELACION | arc1.estado=LIV_REVELACION (tras gate LIII->LIV) | acceso a Mantenimiento Antiguo (concepto: MANTENIMIENTO_INVESTIGACION, fuente institucional, limitado a corredores necesarios; no concede Nucleo); R6=CONFIRMADO; Comprension +1 (ARC1_M13_CONSUMO_ACTUAL) | M14 | Duan Shibo, He Zhen, Ma Qiren, Lu Cheng, Song Rui | mantenimiento, produccion, archivos | acceso a la investigacion del Nucleo (prepara M14) | R6 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M14 | La promesa aplazada | LIV_REVELACION | M13=HECHA | NUCLEO_SUPERIOR (permiso); R8=CONFIRMADO; Comprension +1 (ARC1_M14_CONSENTIMIENTO) | M15 | pocos NPC en escena; investigacion principalmente material/documental (Consejo autoriza el acceso) | mantenimiento, nucleo | prepara M15 | R8 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M15 | Lo que debía terminar | LIV_REVELACION | M14=HECHA | R9=CONFIRMADO; Comprension +1 (ARC1_M15_RELEVO_APLAZADO); condiciones para el inicio de M16 (crisis narrativa) | M16 (arc1.estado->LIV_CRISIS tras avisos simultaneos posteriores) | contraste documental; sin NPC de escena central citados explicitamente | nucleo | prepara M16 | R9 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M16 | Cuando falla el centro | LIV_CRISIS | M15=HECHA; avisos simultaneos posteriores a M15 (Formaciones/Medicina/Sauces/patrulla) | arc1.estado=LIV_CRISIS; crisis_<frente>_resuelta por cada uno de los 6 frentes; EMERGENCIA_SECTA (temporal, expira al cerrar M16) | M17 | Lan Meihua, Jiang Rui, He Zhen, Duan Shibo, Xu An, Su Lian | medicina, bosques, formaciones, produccion, sauces, jardines | — | — | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M17 | Descender | LIV_CRISIS/LIV_DESCENSO | M16=HECHA | NUCLEO_PROFUNDO (permiso, fuente=ORDEN, origen=M17); R7=CONFIRMADO; R10=CONFIRMADO; Comprension +1 (ARC1_M17_DEPENDENCIA_VIVA); nucleo_sala_relevo conocido (alojamiento) | M18 | Ji Xueying (preside Consejo), He Zhen, Lan Meihua, Song Rui, Qiao Ren, Centinela de Plumas Petrificadas | secta_interior, primera_ala, mantenimiento, nucleo | acceso a M18 | R7 CONFIRMADO, R10 CONFIRMADO | CANÓNICO (T254/T286–T290/T281) | NO_IMPLEMENTADO |
| M18 | El Voto Inmóvil | LIV_DESCENSO | M17=HECHA; R7 y R10 conocidos | decisionFinal=LIBERAR|CUSTODIAR (irreversible); M18=HECHA; arc1.estado=EPILOGO; gate de Gran Perfeccion habilitado (no automatico) | Epilogo jugable (Gran Perfeccion -> Iluminacion -> Tribulacion -> Fundacion -> ZhuJi -> Consejo -> Salida Regional); fuera del alcance de esta auditoria salvo para verificar dependencias. | La Grulla (entidad, jefe narrativo) | nucleo | habilita Gran Perfeccion cuando qi/condiciones corresponden (no automatico) | — | CANÓNICO (T254/T286–T290/T281) | LEGACY_A_REEMPLAZAR |

---
## 4. Fichas completas por misión

### P — La Piedra y la Puerta

**ETAPA_ARC1:** PROLOGO

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** Nueva Partida valida

**PRODUCE:** estadoAfiliacion=ADMITIDO · PROLOGO=HECHO · arc1.estado=LI_INTEGRACION

**ABRE:** M01

**CONDICIÓN_DE_DISPONIBILIDAD:** Nueva Partida (personaje recien creado).

**CONDICIÓN_DE_ACTIVACIÓN:** Automatica al crear personaje; recorrido patio_raices->registro.

**CONDICIÓN_DE_FINALIZACIÓN:** Evento REGISTRO_INICIAL_COMPLETADO en `registro` (Tao Ming).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Tao Ming · guardia de la Puerta Roja · ayudante de ingreso

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** acceso

**SALAS_329_CONFIRMADAS:** patio_raices · descansillo · mirador_niebla · patio_practica · sendero_pinos · camino · puerta · registro

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** NO CERRADO EN FUENTE

**GATES:** entrada a LI

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** NO CERRADO EN FUENTE

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** NO CERRADO EN FUENTE

**FLAGS_CREADOS:** estadoAfiliacion=ADMITIDO · raiz elegida (persistente, no se vuelve a sortear)

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: 0; contribucion: 0; notas: Recompensa puramente institucional: acceso a Registro. Equipo inicial (uniforme gris de ingreso + espada de madera) en descansillo.

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** Volver a `registro` tras cerrar el Prologo no repite tutorial ni reasigna raiz (T257).

**EVENTOS_ONE_SHOT:** REGISTRO_INICIAL_COMPLETADO · sorteo/eleccion de raiz

**EVENTOS_REPETIBLES:** MEDITAR en mirador_niebla · practica opcional en patio_practica

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** NO CERRADO EN FUENTE

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** Presentacion publica de la fundacion: OBSOLETO=Version antigua de ver55 presenta la leyenda de la Grulla como hecho llano. | CANÓNICO=Se reescribe como 'version publica que se cuenta' (leyenda), reservando la verdad (R1-R10) para mucho despues. | FUENTE=T286

**VERSIÓN_OBSOLETA:** ver: Version antigua de ver55 presenta la leyenda de la Grulla como hecho llano.

**VERSIÓN_CANÓNICA:** ver: Se reescribe como 'version publica que se cuenta' (leyenda), reservando la verdad (R1-R10) para mucho despues.

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** Texto final exacto de la leyenda pendiente de integrarse a ver68/implementacion (M2/3C).

---

### M01 — Un nombre entre miles

**ETAPA_ARC1:** LI_INTEGRACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** PROLOGO=HECHO · arc1.estado=LI_INTEGRACION

**PRODUCE:** rango=ASPIRANTE · SECTA_EXTERIOR_BASE · alojamiento conocido: dormitorio_externos

**ABRE:** M02 (junto con otras condiciones)

**CONDICIÓN_DE_DISPONIBILIDAD:** PROLOGO=HECHO.

**CONDICIÓN_DE_ACTIVACIÓN:** Conversacion formal con Tao Ming en Registro (no basta con entrar a la sala).

**CONDICIÓN_DE_FINALIZACIÓN:** Evento ALOJAMIENTO_CONFIRMADO (Madre Wen asigna cama en dormitorio_externos).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Tao Ming · Madre Wen · Gao Shun (opcional)

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** secta_exterior

**SALAS_329_CONFIRMADAS:** registro · sala_jade · dormitorio_externos

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** 'patio exterior' / 'Cabañas' citados en T286 sin room_id 329 literal confirmado en las fuentes leidas; requiere M2.

**GATES:** necesaria para continuar LI

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Presentarse/inscribirse en Sala de Jade (NOMBRE_INSCRITO, una sola vez) · Recibir alojamiento de Madre Wen

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** NO CERRADO EN FUENTE

**FLAGS_CREADOS:** NOMBRE_INSCRITO · rango=ASPIRANTE · SECTA_EXTERIOR_BASE · alojamiento_conocido.dormitorio_externos=true

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: 0; contribucion: 0; notas: Recompensa institucional pura: pertenencia + primer alojamiento conocido garantizado (destino de rescate para el futuro sistema de muerte/recuperacion).

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** Repetir EXAMINAR TAJO/MURO tras NOMBRE_INSCRITO produce texto de repeticion, no reprocesa el evento (T286, T257).

**EVENTOS_ONE_SHOT:** NOMBRE_INSCRITO · ALOJAMIENTO_CONFIRMADO

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Aparicion incidental de varios companeros durante la promocion (T254).

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** Room_id 329 exacto para 'patio exterior'/'Cabañas Externas' citado en fase 3 (DESTINO_329_PENDIENTE).

---

### M02 — Trabajo que alguien debe hacer

**ETAPA_ARC1:** LI_INTEGRACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** M01=HECHA

**PRODUCE:** primerServicioFormal=true · Examen Espiritual desbloqueado · Contribucion pequeña

**ABRE:** M03 (junto con otras condiciones)

**CONDICIÓN_DE_DISPONIBILIDAD:** M01=HECHA.

**CONDICIÓN_DE_ACTIVACIÓN:** Aceptar el servicio (revisar almacen/despensa) con Tao Ming/Ma Qiren/Madre Wen.

**CONDICIÓN_DE_FINALIZACIÓN:** Entrega/validacion del servicio: Examen realizado correctamente + informacion sobre el ejemplar obtenida (NO depende de una extraccion exitosa de material).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Tao Ming / Ma Qiren o Madre Wen (informan) · Chen Bo (ensena Examen)

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** secta_exterior

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** Almacen/despensa exterior concreto de M02: sin room_id 329 literal en las fuentes leidas (DESTINO_329_PENDIENTE).

**GATES:** 'primer servicio formal' es componente del gate LI->LII

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Investigar el almacen/despensa · Combatir/resolver una Rata de qi de mision · Aprender Examen Espiritual con Chen Bo

**OBJETIVOS_OPCIONALES:** Extraer material del cadaver (no obligatorio para cerrar la mision)

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** NO CERRADO EN FUENTE

**FLAGS_CREADOS:** primerServicioFormal=true · EXAMEN_ESPIRITUAL_APRENDIDO

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: 0; contribucion: pequeña; notas: Primera vez que el jugador recibe Contribucion; sin Merito (trabajo rutinario).

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** El cadaver/material de mision no puede duplicarse indefinidamente; si desaparece o el jugador abandona la zona debe existir recuperacion narrativa controlada, no reaparicion infinita (T257).

**EVENTOS_ONE_SHOT:** EXAMEN_ESPIRITUAL_APRENDIDO

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** Explicitamente sinalado en fuente: evitar duplicacion de recursos si el tutorial de Examen se repite (T257).

**RELACIÓN_CON_COMPAÑEROS:** Guo y Han pueden aparecer en actividad laboral (T254).

**ESTADO_EN_VER68:** LEGACY_A_REEMPLAZAR

**CONFLICTOS_HISTÓRICOS:** M02 reemplaza la mision de las ratas: OBSOLETO=ver68: quest 'ratas' ('La plaga de la despensa') exige matar exactamente 3 Ratas de qi y entrega recompensa generica de Contribucion+piedras+experiencia. | CANÓNICO=M02: un solo encuentro con una Rata de qi, enfoque en aprender Examen Espiritual real; la mision NO depende de una extraccion exitosa; recompensa es servicio+Examen+Contribucion pequeña, sin piedras/experiencia genericas. | FUENTE=T286 vs grulla-blanca_ver68.html (const QUESTS.ratas)

**VERSIÓN_OBSOLETA:** ver: ver68: quest 'ratas' ('La plaga de la despensa') exige matar exactamente 3 Ratas de qi y entrega recompensa generica de Contribucion+piedras+experiencia.

**VERSIÓN_CANÓNICA:** ver: M02: un solo encuentro con una Rata de qi, enfoque en aprender Examen Espiritual real; la mision NO depende de una extraccion exitosa; recompensa es servicio+Examen+Contribucion pequeña, sin piedras/experiencia genericas.

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** Room_id 329 exacto del almacen/despensa de M02: DESTINO_329_PENDIENTE.

---

### M03 — Aprender a permanecer

**ETAPA_ARC1:** LI_INTEGRACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** M01=HECHA · M02=HECHA · condiciones basicas de cultivo apropiadas

**PRODUCE:** rango: ASPIRANTE->DISCIPULO_EXTERNO · estadoAfiliacion=MIEMBRO · evaluacionCirculacion=SUPERADA · acceso a Piel de Cobre como formacion basica

**ABRE:** M04 (tras gate LI->LII)

**CONDICIÓN_DE_DISPONIBILIDAD:** M01 y M02 HECHAS.

**CONDICIÓN_DE_ACTIVACIÓN:** Shen Baojun inicia la formacion (instruccion + practica).

**CONDICIÓN_DE_FINALIZACIÓN:** Evento EVALUACION_CIRCULACION_SUPERADA (no exige llenar el vaso a 25/25; comprueba estabilizacion, finalizacion del ejercicio y ausencia de estado critico).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Shen Baojun · Qiao Ren (supervision institucional, no obligatoria en escena)

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** secta_exterior

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** 'sector marcial / Respiracion / Disciplina' sin room_id 329 literal citado en las fuentes leidas.

**GATES:** gate LI->LII: qi>=25 + rango==DISCIPULO_EXTERNO + primerServicioFormal + evaluacionCirculacion==SUPERADA

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Instruccion con Shen Baojun (incluye ensenanza de Piel de Cobre) · Practica contra el muneco de entrenamiento (respuesta valida: Piel de Cobre u otra legitima: DEFENDER/evasion/control) · Evaluacion de circulacion (MEDITAR o equivalente contextual)

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** NO CERRADO EN FUENTE

**FLAGS_CREADOS:** evaluacionCirculacion=SUPERADA · rango=DISCIPULO_EXTERNO · estadoAfiliacion=MIEMBRO

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: 0; contribucion: posible pequeña; notas: La recompensa central es el cambio de rango, no economica.

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** La evaluacion puede practicarse de nuevo despues, pero la promocion de rango ocurre una sola vez (T257).

**EVENTOS_ONE_SHOT:** EVALUACION_CIRCULACION_SUPERADA · promocion Aspirante->Discipulo Externo

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Lin, Han y Luo tienen mayor presencia potencial (T254). Posible escena breve de evaluacion paralela de un companero.

**ESTADO_EN_VER68:** LEGACY_A_REEMPLAZAR

**CONFLICTOS_HISTÓRICOS:** M03 reemplaza el duelo con Fan Ji: OBSOLETO=ver68: quest 'duelo' ('El arrogante') exige derrotar a Fan Ji en la arena, con eleccion ejecutar/perdonar y recompensa de Contribucion+piedras+experiencia+decision de Dao. | CANÓNICO=M03: evaluacion de circulacion e intencion bajo presion con el muneco de entrenamiento, sin duelo con un NPC humano; unica promocion real de Arc1 (Aspirante->Discipulo Externo); sin piedras/experiencia generica. | FUENTE=T286 vs grulla-blanca_ver68.html (const QUESTS.duelo, fan_ji)

**VERSIÓN_OBSOLETA:** ver: ver68: quest 'duelo' ('El arrogante') exige derrotar a Fan Ji en la arena, con eleccion ejecutar/perdonar y recompensa de Contribucion+piedras+experiencia+decision de Dao.

**VERSIÓN_CANÓNICA:** ver: M03: evaluacion de circulacion e intencion bajo presion con el muneco de entrenamiento, sin duelo con un NPC humano; unica promocion real de Arc1 (Aspirante->Discipulo Externo); sin piedras/experiencia generica.

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** Room_id 329 exacto del sector marcial: DESTINO_329_PENDIENTE. · 'Si CONSAGRAR exige literalmente 25/25' queda explicitamente abierto en T286 (a revisar al adaptar progresion de ver55): NO CERRADO EN FUENTE.

---

### M04 — Más allá de la Puerta Roja

**ETAPA_ARC1:** LII_TERRITORIO

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** arc1.estado=LII_TERRITORIO (tras gate LI->LII) · rango=DISCIPULO_EXTERNO

**PRODUCE:** PATRULLA_TERRITORIAL (permiso, fuente=MISION, origen=M04) · refugio bosque_refugio_patrulla conocido

**ABRE:** M05

**CONDICIÓN_DE_DISPONIBILIDAD:** arc1.estado=LII_TERRITORIO + Discipulo Externo.

**CONDICIÓN_DE_ACTIVACIÓN:** Asignacion de Jiang Rui (primera salida de servicio).

**CONDICIÓN_DE_FINALIZACIÓN:** Regreso/validacion de la primera salida ante Jiang Rui (informe breve).

**NPC_ANCLADOS:** npc=Gao Shun; sala=Puerta Roja (region secta_exterior); condicion=ANCLADO durante el objetivo obligatorio de M04; vuelve a movilidad normal despues (Backup Maestro §40).

**NPC_RELEVANTES:** Jiang Rui

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** secta_exterior · bosques

**SALAS_329_CONFIRMADAS:** bosque_refugio_patrulla

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** NO CERRADO EN FUENTE

**GATES:** componente del servicio territorial LII

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Revisar tramo de camino / puesto / refugio · Regresar con informe breve

**OBJETIVOS_OPCIONALES:** Inspeccionar senal caida/huellas del 'incidente de servicio'

**EVIDENCIAS:** observacion FAUNA_FUERA_DE_RANGO, estado NO_INTERPRETADA (no genera evidencia R1 todavia)

**REVELACIONES_R1_R10:** NO CERRADO EN FUENTE

**FLAGS_CREADOS:** PATRULLA_TERRITORIAL=activa_permanente · refugio bosque_refugio_patrulla conocido (seguro=true, purifica=false)

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: posible pequeño si hay incidente real (no por caminar la ruta normal); contribucion: pequeña

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** Si el jugador ya visito alguna zona antes, la mision reconoce ese conocimiento espacial; no obliga a 'redescubrir' (T257).

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Lin especialmente adecuada (T254); Luo tambien con presencia potencial.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** No hay evidencia de que M04 reemplace contenido especifico de ver68 (region no cubierta por el Acto I-IV legacy).

---

### M05 — Los caminos de la Grulla

**ETAPA_ARC1:** LII_TERRITORIO

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** M04=HECHA o servicio territorial suficientemente iniciado

**PRODUCE:** reconocimientoSauces=HUESPED · sauces_casa_huespedes conocido (alojamiento)

**ABRE:** M06 (como parte de la combinacion de condiciones)

**CONDICIÓN_DE_DISPONIBILIDAD:** M04 HECHA o servicio territorial suficientemente iniciado.

**CONDICIÓN_DE_ACTIVACIÓN:** Encargo que conecta secta con Valle/Sauces (revision de ruta de intercambio).

**CONDICIÓN_DE_FINALIZACIÓN:** Confirmacion de que el jugador comprendio/ejecuto la ruta institucional (registro de la modificacion en Sauces).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Duan Shibo o Jiang Rui · Han Qiao (opcional, HAN_02_PROCEDIMIENTO) · Xu An · Mei Shufen

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** valle · produccion · sauces

**SALAS_329_CONFIRMADAS:** sauces_casa_huespedes

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** Rooms especificas del Valle/Produccion recorridas en M05 (graneros, puestos de intercambio): sin room_id 329 literal citado.

**GATES:** contribuye al conocimiento territorial (no es gate duro por si sola)

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Paso por el Valle · Llegada a Sauces y conversacion con Xu An · Registrar la modificacion del circuito

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** NO CERRADO EN FUENTE

**FLAGS_CREADOS:** reconocimientoSauces=HUESPED · sauces_casa_huespedes conocido (seguro=true, purifica=true)

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: normalmente pequeño o ninguno, salvo incidente extraordinario; contribucion: pequeña/moderada

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** reconocimientoSauces=HUESPED es relacion local, no autorizacion institucional; no se crea flag redundante 'SaucesExiste' (Sauces ya existia) (T257).

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** MEI_03_REGRESO_SAUCES puede ocurrir aqui si Mei acompaña; HAN_02_PROCEDIMIENTO en el Valle.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** Primera ruta 'occidental Cantera/Bosque' vs 'oriental Agua/Jardines' (Backup Maestro §40): declarado explicitamente NO exclusion permanente, sin decision final de cual se usa por defecto.

---

### M06 — Lo que no debería estar aquí

**ETAPA_ARC1:** LII_TERRITORIO

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** M04 y M05 suficientes para conocer el territorio (no exige combinacion unica)

**PRODUCE:** conocimiento.anomaliasTerritoriales -> SOSPECHA/PARCIAL fuerte · R1=PARCIAL

**ABRE:** M07

**CONDICIÓN_DE_DISPONIBILIDAD:** Combinacion razonable de M04/M05 HECHAS + alguna observacion territorial sospechosa (no hay combinacion unica).

**CONDICIÓN_DE_ACTIVACIÓN:** Primer incidente reconocido como anomalo (mision formal o reinterpretacion de una observacion previa NO_INTERPRETADA).

**CONDICIÓN_DE_FINALIZACIÓN:** evaluarEvidenciaTerritorial() alcanza SUFICIENTE (CONCLUYENTE mejora dialogo/preparacion pero no es obligatorio).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Jiang Rui · Ma Gu · patrullas · Zhao Wen/Mei Lian/Lin Yue (segun lugar)

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** bosques · aguas_barrancos · cantera_vetas

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** Rooms especificas de avistamiento no citadas literalmente.

**GATES:** NO CERRADO EN FUENTE

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Reunir evidencia semantica suficiente (DESPLAZAMIENTO_FAUNA / ALTERACION_VEGETAL / ALTERACION_HIDRICA / PATRON_TERRITORIAL); diversidad > cantidad

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** DESPLAZAMIENTO_FAUNA · ALTERACION_VEGETAL · ALTERACION_HIDRICA · PATRON_TERRITORIAL

**REVELACIONES_R1_R10:** R1 PARCIAL

**FLAGS_CREADOS:** evidenciaTerritorial>=SUFICIENTE

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: limitado, no se ha formalizado conclusion; contribucion: sí

**CONSECUENCIAS:** NO CERRADO EN FUENTE

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** No existe objetivo tipo 'ANOMALÍAS 0/4'; el evaluador es semantico, no un contador estricto (T257).

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Zhao insiste en 'patron posible, todavia no causa'; Jiang Rui aporta experiencia; Mei y Lin pueden aportar avistamientos.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** NO CERRADO EN FUENTE

---

### M07 — Informe de frontera

**ETAPA_ARC1:** LII_TERRITORIO

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** M06=HECHA · evidenciaTerritorial>=SUFICIENTE

**PRODUCE:** informeFronteraAceptado=true · R1=CONFIRMADO · Comprension +1 (ARC1_M07_PATRON_TERRITORIAL)

**ABRE:** M08, M09, M10 (tras gate LII->LIII y avance de cultivo)

**CONDICIÓN_DE_DISPONIBILIDAD:** M06 HECHA y evidencia suficiente.

**CONDICIÓN_DE_ACTIVACIÓN:** Decision explicita del jugador de presentar el informe.

**CONDICIÓN_DE_FINALIZACIÓN:** Evento INFORME_ACEPTADO (revision de Jiang Rui/Qiao Ren; He Zhen puede recibir copia).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Jiang Rui · Qiao Ren · He Zhen (consulta breve, no revela R2) · Ren Bo · Su Lian

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** secta_exterior

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** Sala donde se prepara/entrega el informe: sin room_id 329 literal.

**GATES:** requisito narrativo principal para gate LII->LIII

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Preparar el informe (interfaz contextual con arc1.evidencia.territorial) · Elegir grado de certeza en la formulacion (afirmacion fuerte vs cauta; se puede corregir sin penalizacion si Qiao Ren/Jiang Rui la cuestionan)

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** R1 CONFIRMADO

**FLAGS_CREADOS:** informeFronteraAceptado=true · conocimiento.anomaliasTerritoriales=CONFIRMADO · difusion institucional (Jiang Rui, Qiao Ren, He Zhen, Ren Bo, Su Lian y autoridades)

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** HISTORY candidato: PRESENTAR_EVIDENCIA_INCIERTA.

**RECOMPENSAS:** comprension: +1 (ARC1_M07_PATRON_TERRITORIAL); merito: significativo; contribucion: moderada; notas: Prestigio puede modificarse ligeramente segun conducta conocida durante el proceso.

**CONSECUENCIAS:** No concede SECTA_INTERIOR todavia (se concede al entrar oficialmente en LIII, tras el avance de cultivo, evento separado).

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** Equivocar el grado de certeza no falla la mision ni reduce Merito/Prestigio ni obliga a repetir M06 (T287).

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Zhao y Luo con mayor presencia potencial en la formulacion del informe.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** NO CERRADO EN FUENTE

---

### M08 — Una montaña que no coincide consigo misma

**ETAPA_ARC1:** LIII_INVESTIGACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** arc1.estado=LIII_INVESTIGACION · SECTA_INTERIOR concedido

**PRODUCE:** FORMACIONES_INVESTIGACION (permiso) · R2=CONFIRMADO

**ABRE:** M11 (junto con M09/M10)

**CONDICIÓN_DE_DISPONIBILIDAD:** LIII + acceso interior (SECTA_INTERIOR).

**CONDICIÓN_DE_ACTIVACIÓN:** He Zhen concede FORMACIONES_INVESTIGACION y proporciona marco/instrumentacion.

**CONDICIÓN_DE_FINALIZACIÓN:** Repeticion de medicion en otro sector/nodo independiente confirma la discrepancia (no es fallo de instrumento).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** He Zhen · Wen Tao

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** formaciones

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** Puntos de medicion exteriores revisitados de M04-M07 y 'Sala de Mapas de Flujo': sin room_id 329 literal confirmado (aunque el area Formaciones si esta confirmada en topologia v2).

**GATES:** componente de M11

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Lectura inicial (visitar puntos ya conocidos de M04-M07) · Trabajo de campo · Comparacion en el centro de Formaciones · Confirmacion en sector/nodo independiente

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** R2 CONFIRMADO

**FLAGS_CREADOS:** NO CERRADO EN FUENTE

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: moderado; contribucion: sí; notas: No concede Comprension aqui: es observacion tecnica, no sintesis (llegara en M11).

**CONSECUENCIAS:** FORMACIONES_INVESTIGACION permanece activo para los sectores correspondientes tras cerrar M08.

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** NO CERRADO EN FUENTE (no se detalla explicitamente en T257 mas alla del contrato general BLOQUEADA/DISPONIBLE/ACTIVA/HECHA)

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Zhao/Luo posibles.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** NO CERRADO EN FUENTE

---

### M09 — Los nombres que faltan

**ETAPA_ARC1:** LIII_INVESTIGACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** arc1.estado=LIII_INVESTIGACION

**PRODUCE:** ARCHIVO_COMUN (inicio) · ARCHIVO_RESTRINGIDO (progreso, autorizado por Qiao Ren) · R3=PARCIAL

**ABRE:** M11 (junto con M08/M10)

**CONDICIÓN_DE_DISPONIBILIDAD:** arc1.estado=LIII_INVESTIGACION.

**CONDICIÓN_DE_ACTIVACIÓN:** Song Rui identifica inconsistencias en referencias cruzadas usadas durante M08.

**CONDICIÓN_DE_FINALIZACIÓN:** Investigacion alcanza base suficiente para que Qiao Ren autorice temporalmente ARCHIVO_RESTRINGIDO y aparece el termino 'Dos Alas' (sin definicion completa).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Song Rui · Zhao Wen · Qiao Ren (autoriza ARCHIVO_RESTRINGIDO) · Luo Yan (discusion) · Yu Shun

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** archivos · secta_interior

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** NO CERRADO EN FUENTE

**GATES:** componente de M11

**AUTORIZACIONES:** ARCHIVO_COMUN · ARCHIVO_RESTRINGIDO

**OBJETIVOS_OBLIGATORIOS:** Examinar 3 tipos de inconsistencia: referencia ausente, copia modificada, nombres presentes/ausentes entre versiones · Usar LEER ESCRITURAS (sin Hoja de Claridad, sin coste, sin +2 Comprension repetible)

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** R3 PARCIAL

**FLAGS_CREADOS:** NO CERRADO EN FUENTE

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: sí si produce hallazgo reconocido; contribucion: posible; notas: Candidata fuerte para HISTORY: como maneja el jugador un documento sensible antes de tener certeza completa.

**CONSECUENCIAS:** M09 NO revela Primera Ala como red completa; el termino puede aparecer en un encabezado antiguo sin significado cerrado todavia (preserva M12).

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** NO CERRADO EN FUENTE (detalle tecnico no cubierto explicitamente mas alla del contrato general).

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Zhao y Luo especialmente.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** NO CERRADO EN FUENTE

---

### M10 — El cuerpo recuerda

**ETAPA_ARC1:** LIII_INVESTIGACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** arc1.estado=LIII_INVESTIGACION

**PRODUCE:** R4=CONFIRMADO

**ABRE:** M11 (junto con M08/M09)

**CONDICIÓN_DE_DISPONIBILIDAD:** arc1.estado=LIII_INVESTIGACION.

**CONDICIÓN_DE_ACTIVACIÓN:** Casos clinicos con registros de pacientes/metodos antiguos agrupados bajo 'Segunda Rama'.

**CONDICIÓN_DE_FINALIZACIÓN:** Se confirma que los cuerpos fueron modificados para tolerar/conducir dos corrientes incompatibles (R4).

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** Lan Meihua · Chen Bo · Guo Chen (relacion tematica) · Luo Yan (oposicion por riesgo)

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** medicina

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** 'Sala Anatomica'/'Archivo Clinico' de Medicina: sin room_id 329 literal citado en las fuentes leidas.

**GATES:** componente de M11

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Leer registros/examinar diagramas · Conversar con Chen Bo sobre lesiones sin sentido bajo anatomia meridiana estandar

**OBJETIVOS_OPCIONALES:** NO CERRADO EN FUENTE

**EVIDENCIAS:** NO CERRADO EN FUENTE

**REVELACIONES_R1_R10:** R4 CONFIRMADO

**FLAGS_CREADOS:** NO CERRADO EN FUENTE

**FLAGS_CONSUMIDOS:** NO CERRADO EN FUENTE

**ESTADOS_DE_MUNDO_MODIFICADOS:** NO CERRADO EN FUENTE

**RECOMPENSAS:** comprension: 0; merito: sí por investigacion importante; contribucion: posible; notas: Candidata fuerte para HISTORY, especialmente por manejo de conocimiento corporal peligroso.

**CONSECUENCIAS:** M10 NO confirma que Segunda Rama y Dos Alas sean exactamente lo mismo (eso queda para M11). · Injerto jugable NO se habilita (requiere ZhuJi + metodo especifico, sin cambios). · 'ESTUDIAR INJERTO' se elimina de contenido visible de Arc1; el verbo futuro sera LEER APENDICE.

**DEPENDENCIAS_POSTERIORES:** NO CERRADO EN FUENTE

**IDEMPOTENCIA:** NO CERRADO EN FUENTE.

**EVENTOS_ONE_SHOT:** NO CERRADO EN FUENTE

**EVENTOS_REPETIBLES:** NO CERRADO EN FUENTE

**RIESGOS_DE_DUPLICACIÓN:** NO CERRADO EN FUENTE

**RELACIÓN_CON_COMPAÑEROS:** Mei, Guo y Luo con mayor presencia potencial; nadie realiza injerto en M10.

**ESTADO_EN_VER68:** NO_IMPLEMENTADO

**CONFLICTOS_HISTÓRICOS:** NO CERRADO EN FUENTE

**VERSIÓN_OBSOLETA:** NO CERRADO EN FUENTE

**VERSIÓN_CANÓNICA:** NO CERRADO EN FUENTE

**FUENTES:** T254, T286, T287, T288, T289, T290, T281, T257

**PENDIENTES:** NO CERRADO EN FUENTE

---

### M11 — Las Dos Alas

**ETAPA_ARC1:** LIII_INVESTIGACION

**ESTADO_CANÓNICO:** CANÓNICO — fuente principal T254/T286–T290/T281 (Fuente Maestra ver55); sin conflicto con Backup Maestro §50/§51.

**REQUIERE:** M08=HECHA · M09=HECHA · M10=HECHA

**PRODUCE:** R3=CONFIRMADO · DOS_ALAS=PRINCIPIO · SEGUNDA_RAMA=APLICACION_CORPORAL · Comprension +1 (ARC1_M11_DOS_ALAS)

**ABRE:** M12

**CONDICIÓN_DE_DISPONIBILIDAD:** M08, M09 y M10 HECHAS (las tres, sin orden fijo).

**CONDICIÓN_DE_ACTIVACIÓN:** Reunion pequeña (He Zhen aporta mediciones, Song Rui textos, Lan Meihua casos corporales).

**CONDICIÓN_DE_FINALIZACIÓN:** Se reconstruye el principio: Dos Alas = principio general de coexistencia/concordancia (contencion + presion/circulacion); Segunda Rama = aplicacion corporal concreta y peligrosa.

**NPC_ANCLADOS:** NO CERRADO EN FUENTE

**NPC_RELEVANTES:** He Zhen · Song Rui · Lan Meihua

**DEPENDENCIAS_AUDITORIA_5:** NO CERRADO EN FUENTE

**ÁREAS:** formaciones · archivos · medicina

**SALAS_329_CONFIRMADAS:** NO CERRADO EN FUENTE

**IDS_HISTÓRICOS:** NO CERRADO EN FUENTE

**DESTINOS_329_PENDIENTES:** 'Manantial Partido' citado en T254 como posible region cruzada de M11: sin confirmacion literal de que M11 visite esa sala; el Manantial Partido corresponde al unico ecologico Anguila Manantial Partido, no necesariamente a un room_id de M11.

**GATES:** requisito directo de M12

**AUTORIZACIONES:** NO CERRADO EN FUENTE

**OBJETIVOS_OBLIGATORIOS:** Participar en la sintesis conjunta (no es una nueva expedicion, es integracion de lo ya investigado)
