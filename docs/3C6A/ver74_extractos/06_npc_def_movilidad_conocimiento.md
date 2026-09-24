# Extracto 06 — NPC_DEF/movilidad/conocimiento

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## NPC `tao_ming` · líneas 5303-5365

```js
05303:   "tao_ming": {
05304:     "id": "tao_ming",
05305:     "nombre": "Tao Ming",
05306:     "categoria": "intermedio",
05307:     "rol": "Registro de Servicios",
05308:     "sala_inicial": "oficina_servicios",
05309:     "sala_inicial_clasificacion": "CANÓNICO",
05310:     "movilidad": "RUTA",
05311:     "territorio_normal": [
05312:       "oficina_servicios",
05313:       "patio_servicios",
05314:       "deposito_comun"
05315:     ],
05316:     "transito_tecnico": [],
05317:     "posicion_valida": [
05318:       "deposito_comun",
05319:       "oficina_servicios",
05320:       "patio_servicios"
05321:     ],
05322:     "rutas": [
05323:       [
05324:         "oficina_servicios",
05325:         "patio_servicios"
05326:       ],
05327:       [
05328:         "oficina_servicios",
05329:         "deposito_comun"
05330:       ]
05331:     ],
05332:     "gates_en_ruta": [],
05333:     "territorio_por_etapa": {
05334:       "LI": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Prácticamente fijo en Registro/Oficina de Servicios.",
05335:       "LII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Prácticamente fijo en Registro/Oficina de Servicios.",
05336:       "LIII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Prácticamente fijo en Registro/Oficina de Servicios.",
05337:       "M16": "CANÓNICO (T211 §10): Deja de registrar trabajos rutinarios y registra emergencias. (Dato tomado de presencia_crisis_m16; territorio_por_etapa no tiene clave M16 propia para este NPC.)",
05338:       "M17": "NO_CERRADO_EN_FUENTE",
05339:       "EPILOGO": "NO_CERRADO_EN_FUENTE"
05340:     },
05341:     "anclajes_documentados": [
05342:       "M01",
05343:       "M02"
05344:     ],
05345:     "conocimiento_inicial": {
05346:       "R1": "DESCONOCIDO",
05347:       "R2": "DESCONOCIDO",
05348:       "R3": "DESCONOCIDO",
05349:       "R4": "DESCONOCIDO",
05350:       "R5": "DESCONOCIDO",
05351:       "R6": "DESCONOCIDO",
05352:       "R7": "DESCONOCIDO",
05353:       "R8": "DESCONOCIDO",
05354:       "R9": "DESCONOCIDO",
05355:       "R10": "DESCONOCIDO"
05356:     },
05357:     "aliases": {
05358:       "id_canonico": "tao_ming",
05359:       "nombre_completo_normalizado": "tao ming",
05360:       "alias_cortos_inequivocos": [
05361:         "ming"
05362:       ]
05363:     },
05364:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05365:   },
```

## NPC `madre_wen` · líneas 5235-5302

```js
05235:   "madre_wen": {
05236:     "id": "madre_wen",
05237:     "nombre": "Madre Wen",
05238:     "categoria": "intermedio",
05239:     "rol": "Responsable de vida cotidiana de externos",
05240:     "sala_inicial": "patio_cabanas",
05241:     "sala_inicial_clasificacion": "ELECCION_TECNICA_3C5",
05242:     "movilidad": "RUTA",
05243:     "territorio_normal": [
05244:       "patio_cabanas",
05245:       "comedor_externos",
05246:       "corredor_cabanas",
05247:       "sala_comun_externos"
05248:     ],
05249:     "transito_tecnico": [],
05250:     "posicion_valida": [
05251:       "comedor_externos",
05252:       "corredor_cabanas",
05253:       "patio_cabanas",
05254:       "sala_comun_externos"
05255:     ],
05256:     "rutas": [
05257:       [
05258:         "patio_cabanas",
05259:         "comedor_externos"
05260:       ],
05261:       [
05262:         "patio_cabanas",
05263:         "corredor_cabanas"
05264:       ],
05265:       [
05266:         "patio_cabanas",
05267:         "sala_comun_externos"
05268:       ]
05269:     ],
05270:     "gates_en_ruta": [],
05271:     "territorio_por_etapa": {
05272:       "LI": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Sin variación documentada por etapa; presencia constante como figura de continuidad.",
05273:       "LII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Sin variación documentada por etapa; presencia constante como figura de continuidad.",
05274:       "LIII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Sin variación documentada por etapa; presencia constante como figura de continuidad.",
05275:       "M16": "No aparece en la tabla de 6 frentes ni en la tabla de movimiento en crisis; T283 sugiere un rol informal durante M16, pero no lo cierra.",
05276:       "M17": "NO_CERRADO_EN_FUENTE",
05277:       "EPILOGO": "NO_CERRADO_EN_FUENTE"
05278:     },
05279:     "anclajes_documentados": [
05280:       "M01 (integración cotidiana de aspirantes)"
05281:     ],
05282:     "conocimiento_inicial": {
05283:       "R1": "DESCONOCIDO",
05284:       "R2": "DESCONOCIDO",
05285:       "R3": "DESCONOCIDO",
05286:       "R4": "DESCONOCIDO",
05287:       "R5": "DESCONOCIDO",
05288:       "R6": "DESCONOCIDO",
05289:       "R7": "DESCONOCIDO",
05290:       "R8": "DESCONOCIDO",
05291:       "R9": "DESCONOCIDO",
05292:       "R10": "DESCONOCIDO"
05293:     },
05294:     "aliases": {
05295:       "id_canonico": "madre_wen",
05296:       "nombre_completo_normalizado": "madre wen",
05297:       "alias_cortos_inequivocos": [
05298:         "madre"
05299:       ]
05300:     },
05301:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05302:   },
```

## NPC `chen_bo` · líneas 5498-5559

```js
05498:   "chen_bo": {
05499:     "id": "chen_bo",
05500:     "nombre": "Chen Bo",
05501:     "categoria": "intermedio",
05502:     "rol": "Instructor de Examen / Anatomía-Medicina",
05503:     "sala_inicial": "sala_anatomica",
05504:     "sala_inicial_clasificacion": "CANÓNICO",
05505:     "movilidad": "RUTA",
05506:     "territorio_normal": [
05507:       "sala_anatomica",
05508:       "corredor_medicina",
05509:       "archivo_clinico"
05510:     ],
05511:     "transito_tecnico": [],
05512:     "posicion_valida": [
05513:       "archivo_clinico",
05514:       "corredor_medicina",
05515:       "sala_anatomica"
05516:     ],
05517:     "rutas": [
05518:       [
05519:         "sala_anatomica",
05520:         "corredor_medicina"
05521:       ],
05522:       [
05523:         "sala_anatomica",
05524:         "archivo_clinico"
05525:       ]
05526:     ],
05527:     "gates_en_ruta": [],
05528:     "territorio_por_etapa": {
05529:       "LI": "[Desglosado de LI-LIII, mismo texto fuente] Medicina (T211 §3).",
05530:       "LII": "[Desglosado de LI-LIII, mismo texto fuente] Medicina (T211 §3).",
05531:       "LIII": "Medicina + investigación (clave propia LIII adicional a la LI-LIII general; se conserva el detalle más específico).",
05532:       "M16": "ANCLADO Medicina (T211 §3); prioriza pacientes (T211 §10); co-responsable del frente MEDICINA con Lan Meihua y Yao Fen (T281).",
05533:       "M17": "NO_CERRADO_EN_FUENTE",
05534:       "EPILOGO": "CANÓNICO (T211 §3): Medicina."
05535:     },
05536:     "anclajes_documentados": [
05537:       "M02 (Examen Espiritual)",
05538:       "M10",
05539:       "M16 (co-responsable Medicina)"
05540:     ],
05541:     "conocimiento_inicial": {
05542:       "R1": "DESCONOCIDO",
05543:       "R2": "DESCONOCIDO",
05544:       "R3": "DESCONOCIDO",
05545:       "R4": "SOSPECHA",
05546:       "R5": "DESCONOCIDO",
05547:       "R6": "DESCONOCIDO",
05548:       "R7": "DESCONOCIDO",
05549:       "R8": "DESCONOCIDO",
05550:       "R9": "DESCONOCIDO",
05551:       "R10": "DESCONOCIDO"
05552:     },
05553:     "aliases": {
05554:       "id_canonico": "chen_bo",
05555:       "nombre_completo_normalizado": "chen bo",
05556:       "alias_cortos_inequivocos": []
05557:     },
05558:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05559:   },
```

## NPC `shen_baojun` · líneas 5172-5234

```js
05172:   "shen_baojun": {
05173:     "id": "shen_baojun",
05174:     "nombre": "Shen Baojun",
05175:     "categoria": "intermedio",
05176:     "rol": "Instructor marcial externo",
05177:     "sala_inicial": "sala_formas",
05178:     "sala_inicial_clasificacion": "ELECCION_TECNICA_3C5",
05179:     "movilidad": "RUTA",
05180:     "territorio_normal": [
05181:       "sala_formas",
05182:       "patio_marcial",
05183:       "patio_respiracion"
05184:     ],
05185:     "transito_tecnico": [],
05186:     "posicion_valida": [
05187:       "patio_marcial",
05188:       "patio_respiracion",
05189:       "sala_formas"
05190:     ],
05191:     "rutas": [
05192:       [
05193:         "sala_formas",
05194:         "patio_marcial"
05195:       ],
05196:       [
05197:         "sala_formas",
05198:         "patio_respiracion"
05199:       ]
05200:     ],
05201:     "gates_en_ruta": [],
05202:     "territorio_por_etapa": {
05203:       "LI": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] RUTA estable dentro de su territorio marcial; sin variación documentada por etapa.",
05204:       "LII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] RUTA estable dentro de su territorio marcial; sin variación documentada por etapa.",
05205:       "LIII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] RUTA estable dentro de su territorio marcial; sin variación documentada por etapa.",
05206:       "M16": "NO_CERRADO_EN_FUENTE (presencia_crisis_m16.clasificacion=NO CERRADO EN FUENTE; no aparece en la tabla de 6 frentes ni en la de movimiento en crisis.)",
05207:       "M17": "NO_CERRADO_EN_FUENTE",
05208:       "EPILOGO": "NO_CERRADO_EN_FUENTE"
05209:     },
05210:     "anclajes_documentados": [
05211:       "M03 (entrenamiento básico y Paso de Nube)"
05212:     ],
05213:     "conocimiento_inicial": {
05214:       "R1": "SOSPECHA",
05215:       "R2": "DESCONOCIDO",
05216:       "R3": "DESCONOCIDO",
05217:       "R4": "DESCONOCIDO",
05218:       "R5": "DESCONOCIDO",
05219:       "R6": "DESCONOCIDO",
05220:       "R7": "DESCONOCIDO",
05221:       "R8": "DESCONOCIDO",
05222:       "R9": "DESCONOCIDO",
05223:       "R10": "DESCONOCIDO"
05224:     },
05225:     "aliases": {
05226:       "id_canonico": "shen_baojun",
05227:       "nombre_completo_normalizado": "shen baojun",
05228:       "alias_cortos_inequivocos": [
05229:         "baojun",
05230:         "shen"
05231:       ]
05232:     },
05233:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05234:   },
```

## NPC `jiang_rui` · líneas 5366-5428

```js
05366:   "jiang_rui": {
05367:     "id": "jiang_rui",
05368:     "nombre": "Jiang Rui",
05369:     "categoria": "intermedio",
05370:     "rol": "Capitán de patrulla",
05371:     "sala_inicial": "puesto_valle",
05372:     "sala_inicial_clasificacion": "ELECCION_TECNICA_3C5",
05373:     "movilidad": "RUTA",
05374:     "territorio_normal": [
05375:       "puesto_valle",
05376:       "valle_explanada",
05377:       "patio_puesto_valle"
05378:     ],
05379:     "transito_tecnico": [],
05380:     "posicion_valida": [
05381:       "patio_puesto_valle",
05382:       "puesto_valle",
05383:       "valle_explanada"
05384:     ],
05385:     "rutas": [
05386:       [
05387:         "puesto_valle",
05388:         "valle_explanada"
05389:       ],
05390:       [
05391:         "puesto_valle",
05392:         "patio_puesto_valle"
05393:       ]
05394:     ],
05395:     "gates_en_ruta": [],
05396:     "territorio_por_etapa": {
05397:       "LI": "Puerta/Puesto (T211 §3).",
05398:       "LII": "rutas completas (clave propia LII).",
05399:       "LIII": "territorio + investigación (clave propia LIII).",
05400:       "M16": "ANCLADO Rutas (T211 §3); rutas/Bosques (T244); responsable principal (junto a Ren Bo) del frente RUTAS (T281).",
05401:       "M17": "NO_CERRADO_EN_FUENTE",
05402:       "EPILOGO": "CANÓNICO (T211 §3): patrulla/reparaciones."
05403:     },
05404:     "anclajes_documentados": [
05405:       "M04–M07 (ANCLADO en Cruce Patrullas → Sala Informes según avance)",
05406:       "M16 (responsable Rutas)"
05407:     ],
05408:     "conocimiento_inicial": {
05409:       "R1": "SOSPECHA",
05410:       "R2": "DESCONOCIDO",
05411:       "R3": "DESCONOCIDO",
05412:       "R4": "DESCONOCIDO",
05413:       "R5": "DESCONOCIDO",
05414:       "R6": "DESCONOCIDO",
05415:       "R7": "DESCONOCIDO",
05416:       "R8": "DESCONOCIDO",
05417:       "R9": "DESCONOCIDO",
05418:       "R10": "DESCONOCIDO"
05419:     },
05420:     "aliases": {
05421:       "id_canonico": "jiang_rui",
05422:       "nombre_completo_normalizado": "jiang rui",
05423:       "alias_cortos_inequivocos": [
05424:         "jiang"
05425:       ]
05426:     },
05427:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05428:   },
```

## NPC `gao_shun` · líneas 5625-5700

```js
05625:   "gao_shun": {
05626:     "id": "gao_shun",
05627:     "nombre": "Gao Shun",
05628:     "categoria": "funcional",
05629:     "rol": "Guardia de la Puerta Roja",
05630:     "sala_inicial": "casa_guardia",
05631:     "sala_inicial_clasificacion": "CANÓNICO",
05632:     "movilidad": "RUTA",
05633:     "territorio_normal": [
05634:       "casa_guardia",
05635:       "deposito_comun",
05636:       "puerta",
05637:       "registro"
05638:     ],
05639:     "transito_tecnico": [
05640:       "tablon_encargos",
05641:       "patio_servicios",
05642:       "patio",
05643:       "sala_jade"
05644:     ],
05645:     "posicion_valida": [
05646:       "casa_guardia",
05647:       "deposito_comun",
05648:       "patio",
05649:       "patio_servicios",
05650:       "puerta",
05651:       "registro",
05652:       "sala_jade",
05653:       "tablon_encargos"
05654:     ],
05655:     "rutas": [
05656:       [
05657:         "casa_guardia",
05658:         "deposito_comun",
05659:         "tablon_encargos",
05660:         "patio_servicios",
05661:         "patio",
05662:         "sala_jade",
05663:         "registro",
05664:         "puerta"
05665:       ]
05666:     ],
05667:     "gates_en_ruta": [],
05668:     "territorio_por_etapa": {
05669:       "LI": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Prácticamente fijo en la Puerta.",
05670:       "LII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Prácticamente fijo en la Puerta.",
05671:       "LIII": "[Regla general (T-fuente marca 'General'), sin variación documentada por etapa] Prácticamente fijo en la Puerta.",
05672:       "M16": "PROPUESTA_HISTORICA (T211 §10): mencionado genéricamente entre los NPC funcionales que 'hacen su trabajo' durante la crisis, sin frente propio de los 6 de T281.",
05673:       "M17": "NO_CERRADO_EN_FUENTE",
05674:       "EPILOGO": "CANÓNICO (T211 §12) [CORREGIDO EN REV2 — ausente/NO_CERRADO por error en REV1]: Permanece en la puerta; 'una simple línea suya puede tener más efecto que un gran discurso' en el epílogo."
05675:     },
05676:     "anclajes_documentados": [
05677:       "M01 (según escena, junto a Tao Ming)",
05678:       "M04 (ANCLADO en puerta_roja/puerta)"
05679:     ],
05680:     "conocimiento_inicial": {
05681:       "R1": "SOSPECHA",
05682:       "R2": "DESCONOCIDO",
05683:       "R3": "DESCONOCIDO",
05684:       "R4": "DESCONOCIDO",
05685:       "R5": "DESCONOCIDO",
05686:       "R6": "DESCONOCIDO",
05687:       "R7": "DESCONOCIDO",
05688:       "R8": "DESCONOCIDO",
05689:       "R9": "DESCONOCIDO",
05690:       "R10": "DESCONOCIDO"
05691:     },
05692:     "aliases": {
05693:       "id_canonico": "gao_shun",
05694:       "nombre_completo_normalizado": "gao shun",
05695:       "alias_cortos_inequivocos": [
05696:         "gao"
05697:       ]
05698:     },
05699:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05700:   },
```

## NPC `duan_shibo` · líneas 5042-5105

```js
05042:   "duan_shibo": {
05043:     "id": "duan_shibo",
05044:     "nombre": "Duan Shibo",
05045:     "categoria": "autoridad",
05046:     "rol": "Recursos / Producción",
05047:     "sala_inicial": "oficina_logistica",
05048:     "sala_inicial_clasificacion": "CANÓNICO",
05049:     "movilidad": "RUTA",
05050:     "territorio_normal": [
05051:       "oficina_logistica",
05052:       "patio_produccion",
05053:       "cochera_carros"
05054:     ],
05055:     "transito_tecnico": [],
05056:     "posicion_valida": [
05057:       "cochera_carros",
05058:       "oficina_logistica",
05059:       "patio_produccion"
05060:     ],
05061:     "rutas": [
05062:       [
05063:         "oficina_logistica",
05064:         "patio_produccion"
05065:       ],
05066:       [
05067:         "oficina_logistica",
05068:         "cochera_carros"
05069:       ]
05070:     ],
05071:     "gates_en_ruta": [],
05072:     "territorio_por_etapa": {
05073:       "LI": "NO_CERRADO_EN_FUENTE (solo existe clave LII en la fuente; regla aplicada: 'si sólo existe LII, NO inventar LI'). [CORREGIDO EN REV2: en REV1 se copió aquí, por error, información de LII.]",
05074:       "LII": "Producción/Cantera (T211 §3).",
05075:       "LIII": "NO_CERRADO_EN_FUENTE (sin clave LIII en la fuente.)",
05076:       "M16": "ANCLADO Recursos (T211 §3), entre almacenes y centro de coordinación (T244); responsable principal del frente RECURSOS junto a Ma Qiren y Lu Cheng (T281).",
05077:       "M17": "NO_CERRADO_EN_FUENTE",
05078:       "EPILOGO": "CANÓNICO (T211 §17): Reparando cadenas logísticas / reconstrucción."
05079:     },
05080:     "anclajes_documentados": [
05081:       "M13",
05082:       "M16 (responsable Recursos)"
05083:     ],
05084:     "conocimiento_inicial": {
05085:       "R1": "SOSPECHA",
05086:       "R2": "DESCONOCIDO",
05087:       "R3": "DESCONOCIDO",
05088:       "R4": "DESCONOCIDO",
05089:       "R5": "DESCONOCIDO",
05090:       "R6": "SOSPECHA",
05091:       "R7": "DESCONOCIDO",
05092:       "R8": "DESCONOCIDO",
05093:       "R9": "DESCONOCIDO",
05094:       "R10": "DESCONOCIDO"
05095:     },
05096:     "aliases": {
05097:       "id_canonico": "duan_shibo",
05098:       "nombre_completo_normalizado": "duan shibo",
05099:       "alias_cortos_inequivocos": [
05100:         "duan",
05101:         "shibo"
05102:       ]
05103:     },
05104:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05105:   },
```

## NPC `xu_an` · líneas 6230-6287

```js
06230:   "xu_an": {
06231:     "id": "xu_an",
06232:     "nombre": "Xu An",
06233:     "categoria": "funcional",
06234:     "rol": "Representante de Sauces",
06235:     "sala_inicial": "sauces_casa_comunal",
06236:     "sala_inicial_clasificacion": "CANÓNICO",
06237:     "movilidad": "RUTA",
06238:     "territorio_normal": [
06239:       "sauces_casa_comunal",
06240:       "sauces_plaza"
06241:     ],
06242:     "transito_tecnico": [],
06243:     "posicion_valida": [
06244:       "sauces_casa_comunal",
06245:       "sauces_plaza"
06246:     ],
06247:     "rutas": [
06248:       [
06249:         "sauces_casa_comunal",
06250:         "sauces_plaza"
06251:       ]
06252:     ],
06253:     "gates_en_ruta": [],
06254:     "territorio_por_etapa": {
06255:       "LI": "NO_CERRADO_EN_FUENTE (la fuente solo documenta LIV_crisis/M16 para este NPC). [CORREGIDO EN REV2: en REV1 se copió aquí, por error, información de M16.]",
06256:       "LII": "NO_CERRADO_EN_FUENTE",
06257:       "LIII": "NO_CERRADO_EN_FUENTE",
06258:       "M16": "ANCLADO/ANCLADA Sauces (T244); responsable principal del frente SAUCES (T281).",
06259:       "M17": "NO_CERRADO_EN_FUENTE",
06260:       "EPILOGO": "NO_CERRADO_EN_FUENTE"
06261:     },
06262:     "anclajes_documentados": [
06263:       "M05 (contexto de retorno a Sauces)",
06264:       "M16 (responsable Sauces)"
06265:     ],
06266:     "conocimiento_inicial": {
06267:       "R1": "DESCONOCIDO",
06268:       "R2": "DESCONOCIDO",
06269:       "R3": "DESCONOCIDO",
06270:       "R4": "DESCONOCIDO",
06271:       "R5": "DESCONOCIDO",
06272:       "R6": "DESCONOCIDO",
06273:       "R7": "DESCONOCIDO",
06274:       "R8": "DESCONOCIDO",
06275:       "R9": "DESCONOCIDO",
06276:       "R10": "DESCONOCIDO"
06277:     },
06278:     "aliases": {
06279:       "id_canonico": "xu_an",
06280:       "nombre_completo_normalizado": "xu an",
06281:       "alias_cortos_inequivocos": [
06282:         "an",
06283:         "xu"
06284:       ]
06285:     },
06286:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
06287:   },
```

## NPC `qiao_ren` · líneas 4731-4815

```js
04731:   "qiao_ren": {
04732:     "id": "qiao_ren",
04733:     "nombre": "Qiao Ren",
04734:     "categoria": "autoridad",
04735:     "rol": "Disciplina y Administración",
04736:     "sala_inicial": "pabellon_disciplina",
04737:     "sala_inicial_clasificacion": "CANÓNICO",
04738:     "movilidad": "RUTA",
04739:     "territorio_normal": [
04740:       "pabellon_disciplina",
04741:       "corredor_norte",
04742:       "interior_sala_consejo"
04743:     ],
04744:     "transito_tecnico": [
04745:       "escalinata_interior",
04746:       "interior_umbral_sur",
04747:       "interior_patio_blanco",
04748:       "interior_patio_internos",
04749:       "interior_sala_estudio",
04750:       "interior_corredor_consejo",
04751:       "interior_antesala_consejo"
04752:     ],
04753:     "posicion_valida": [
04754:       "corredor_norte",
04755:       "escalinata_interior",
04756:       "interior_antesala_consejo",
04757:       "interior_corredor_consejo",
04758:       "interior_patio_blanco",
04759:       "interior_patio_internos",
04760:       "interior_sala_consejo",
04761:       "interior_sala_estudio",
04762:       "interior_umbral_sur",
04763:       "pabellon_disciplina"
04764:     ],
04765:     "rutas": [
04766:       [
04767:         "pabellon_disciplina",
04768:         "corredor_norte",
04769:         "escalinata_interior",
04770:         "interior_umbral_sur",
04771:         "interior_patio_blanco",
04772:         "interior_patio_internos",
04773:         "interior_sala_estudio",
04774:         "interior_corredor_consejo",
04775:         "interior_antesala_consejo",
04776:         "interior_sala_consejo"
04777:       ]
04778:     ],
04779:     "gates_en_ruta": [
04780:       "SECTA_INTERIOR"
04781:     ],
04782:     "territorio_por_etapa": {
04783:       "LI": "[Desglosado de LI-LIII, mismo texto fuente] RUTA entre Disciplina/Interior/Consejo.",
04784:       "LII": "[Desglosado de LI-LIII, mismo texto fuente] RUTA entre Disciplina/Interior/Consejo.",
04785:       "LIII": "[Desglosado de LI-LIII, mismo texto fuente] RUTA entre Disciplina/Interior/Consejo.",
04786:       "M16": "Coordinación institucional durante M16 (T244, tabla 'NPC en crisis'); no es responsable de un frente concreto de los 6 de T281.",
04787:       "M17": "Asiste; debe autorizar la excepción que habilita NUCLEO_PROFUNDO (T290 §1: 'Qiao Ren debe autorizar una excepción...').",
04788:       "EPILOGO": "PROPUESTA_HISTORICA (T211): anclaje declarado en 'epílogo', sin sala/estado descrito más allá de su rol."
04789:     },
04790:     "anclajes_documentados": [
04791:       "M03 (cierre de misión, ANCLADA en pabellon_disciplina)",
04792:       "M07",
04793:       "M16 (coordinación)",
04794:       "M17",
04795:       "comparecencia/epílogo"
04796:     ],
04797:     "conocimiento_inicial": {
04798:       "R1": "SOSPECHA",
04799:       "R2": "DESCONOCIDO",
04800:       "R3": "DESCONOCIDO",
04801:       "R4": "DESCONOCIDO",
04802:       "R5": "SOSPECHA",
04803:       "R6": "DESCONOCIDO",
04804:       "R7": "DESCONOCIDO",
04805:       "R8": "DESCONOCIDO",
04806:       "R9": "DESCONOCIDO",
04807:       "R10": "DESCONOCIDO"
04808:     },
04809:     "aliases": {
04810:       "id_canonico": "qiao_ren",
04811:       "nombre_completo_normalizado": "qiao ren",
04812:       "alias_cortos_inequivocos": []
04813:     },
04814:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
04815:   },
```

## NPC `he_zhen` · líneas 5106-5171

```js
05106:   "he_zhen": {
05107:     "id": "he_zhen",
05108:     "nombre": "He Zhen",
05109:     "categoria": "autoridad",
05110:     "rol": "Formaciones / Territorio",
05111:     "sala_inicial": "formaciones_sala_control",
05112:     "sala_inicial_clasificacion": "CANÓNICO",
05113:     "movilidad": "RUTA",
05114:     "territorio_normal": [
05115:       "formaciones_sala_control",
05116:       "formaciones_patio_medicion",
05117:       "formaciones_galeria_norte"
05118:     ],
05119:     "transito_tecnico": [],
05120:     "posicion_valida": [
05121:       "formaciones_galeria_norte",
05122:       "formaciones_patio_medicion",
05123:       "formaciones_sala_control"
05124:     ],
05125:     "rutas": [
05126:       [
05127:         "formaciones_sala_control",
05128:         "formaciones_patio_medicion"
05129:       ],
05130:       [
05131:         "formaciones_sala_control",
05132:         "formaciones_galeria_norte"
05133:       ]
05134:     ],
05135:     "gates_en_ruta": [],
05136:     "territorio_por_etapa": {
05137:       "LI": "NO_CERRADO_EN_FUENTE (solo existen claves LII/LIII en la fuente; regla aplicada: 'si sólo existe LII, NO inventar LI').",
05138:       "LII": "restringido (T211 §3).",
05139:       "LIII": "Formaciones.",
05140:       "M16": "ANCLADO Nodo Central (T211 §3); centro de Formaciones (T244); responsable principal del frente FORMACIONES (T281).",
05141:       "M17": "NO_CERRADO_EN_FUENTE",
05142:       "EPILOGO": "CANÓNICO (T211 §3, §17): Entre Formaciones y Primera Ala."
05143:     },
05144:     "anclajes_documentados": [
05145:       "M08",
05146:       "M12",
05147:       "M16 (responsable Formaciones)",
05148:       "M17"
05149:     ],
05150:     "conocimiento_inicial": {
05151:       "R1": "SOSPECHA",
05152:       "R2": "SABE",
05153:       "R3": "SOSPECHA",
05154:       "R4": "DESCONOCIDO",
05155:       "R5": "SOSPECHA",
05156:       "R6": "SOSPECHA",
05157:       "R7": "SABE",
05158:       "R8": "DESCONOCIDO",
05159:       "R9": "DESCONOCIDO",
05160:       "R10": "DESCONOCIDO"
05161:     },
05162:     "aliases": {
05163:       "id_canonico": "he_zhen",
05164:       "nombre_completo_normalizado": "he zhen",
05165:       "alias_cortos_inequivocos": [
05166:         "he",
05167:         "zhen"
05168:       ]
05169:     },
05170:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05171:   },
```

## NPC `ren_bo` · líneas 6172-6229

```js
06172:   "ren_bo": {
06173:     "id": "ren_bo",
06174:     "nombre": "Ren Bo",
06175:     "categoria": "funcional",
06176:     "rol": "Patrullero veterano",
06177:     "sala_inicial": "patio_puesto_valle",
06178:     "sala_inicial_clasificacion": "ELECCION_TECNICA_3C5",
06179:     "movilidad": "RUTA",
06180:     "territorio_normal": [
06181:       "patio_puesto_valle",
06182:       "puesto_valle",
06183:       "valle_explanada"
06184:     ],
06185:     "transito_tecnico": [],
06186:     "posicion_valida": [
06187:       "patio_puesto_valle",
06188:       "puesto_valle",
06189:       "valle_explanada"
06190:     ],
06191:     "rutas": [
06192:       [
06193:         "patio_puesto_valle",
06194:         "puesto_valle"
06195:       ],
06196:       [
06197:         "puesto_valle",
06198:         "valle_explanada"
06199:       ]
06200:     ],
06201:     "gates_en_ruta": [],
06202:     "territorio_por_etapa": {
06203:       "LI": "NO_CERRADO_EN_FUENTE (la fuente solo documenta LIV_crisis/M16 para este NPC). [CORREGIDO EN REV2: en REV1 se copió aquí, por error, información de M16.]",
06204:       "LII": "NO_CERRADO_EN_FUENTE",
06205:       "LIII": "NO_CERRADO_EN_FUENTE",
06206:       "M16": "rutas/Aguas (T244); co-responsable del frente RUTAS junto a Jiang Rui (T281).",
06207:       "M17": "NO_CERRADO_EN_FUENTE",
06208:       "EPILOGO": "NO_CERRADO_EN_FUENTE"
06209:     },
06210:     "anclajes_documentados": [],
06211:     "conocimiento_inicial": {
06212:       "R1": "SOSPECHA",
06213:       "R2": "DESCONOCIDO",
06214:       "R3": "DESCONOCIDO",
06215:       "R4": "DESCONOCIDO",
06216:       "R5": "DESCONOCIDO",
06217:       "R6": "DESCONOCIDO",
06218:       "R7": "DESCONOCIDO",
06219:       "R8": "DESCONOCIDO",
06220:       "R9": "DESCONOCIDO",
06221:       "R10": "DESCONOCIDO"
06222:     },
06223:     "aliases": {
06224:       "id_canonico": "ren_bo",
06225:       "nombre_completo_normalizado": "ren bo",
06226:       "alias_cortos_inequivocos": []
06227:     },
06228:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
06229:   },
```

## NPC `su_lian` · líneas 5429-5497

```js
05429:   "su_lian": {
05430:     "id": "su_lian",
05431:     "nombre": "Su Lian",
05432:     "categoria": "intermedio",
05433:     "rol": "Maestra de Herboristería",
05434:     "sala_inicial": "bancal_central",
05435:     "sala_inicial_clasificacion": "ELECCION_TECNICA_3C5",
05436:     "movilidad": "RUTA",
05437:     "territorio_normal": [
05438:       "bancal_central",
05439:       "bancal_norte",
05440:       "bancal_sur",
05441:       "sendero_herbolario"
05442:     ],
05443:     "transito_tecnico": [],
05444:     "posicion_valida": [
05445:       "bancal_central",
05446:       "bancal_norte",
05447:       "bancal_sur",
05448:       "sendero_herbolario"
05449:     ],
05450:     "rutas": [
05451:       [
05452:         "bancal_central",
05453:         "bancal_norte"
05454:       ],
05455:       [
05456:         "bancal_central",
05457:         "bancal_sur"
05458:       ],
05459:       [
05460:         "bancal_central",
05461:         "sendero_herbolario"
05462:       ]
05463:     ],
05464:     "gates_en_ruta": [],
05465:     "territorio_por_etapa": {
05466:       "LI": "Jardines (T211 §3).",
05467:       "LII": "Jardines/Bosque Bajo.",
05468:       "LIII": "Jardines/nodos.",
05469:       "M16": "ANCLADA Jardines (T211 §3); Jardines (T244); responsable principal (única) del frente JARDINES (T281).",
05470:       "M17": "NO_CERRADO_EN_FUENTE",
05471:       "EPILOGO": "CANÓNICO (T211 §3): Jardines."
05472:     },
05473:     "anclajes_documentados": [
05474:       "tutorial de Herboristería (ANCLADA en bancal_central)",
05475:       "M16 (responsable Jardines)"
05476:     ],
05477:     "conocimiento_inicial": {
05478:       "R1": "SOSPECHA",
05479:       "R2": "DESCONOCIDO",
05480:       "R3": "DESCONOCIDO",
05481:       "R4": "DESCONOCIDO",
05482:       "R5": "DESCONOCIDO",
05483:       "R6": "DESCONOCIDO",
05484:       "R7": "DESCONOCIDO",
05485:       "R8": "DESCONOCIDO",
05486:       "R9": "DESCONOCIDO",
05487:       "R10": "DESCONOCIDO"
05488:     },
05489:     "aliases": {
05490:       "id_canonico": "su_lian",
05491:       "nombre_completo_normalizado": "su lian",
05492:       "alias_cortos_inequivocos": [
05493:         "su"
05494:       ]
05495:     },
05496:     "descripcion_estado": "DESCRIPCION_NO_CERRADA (no existe descripción física cerrada en las fuentes auditadas; no se inventa apariencia)."
05497:   },
```

## validación conocimientoNPC/posicionNPC

Fuente: `grulla-blanca_ver74.html` · líneas 2328-2400

```js
02328:       if (!rooms[dest]) { if (esSalidaRegional(id,d,dest)) externos.push({origen:id,direccion:d,destino:dest}); else errores.push("Destino interno inexistente: " + id + "." + d + " → " + dest); continue; }
02329:       internos++;
02330:       if (rooms[dest].exits?.[DIRECCION_OPUESTA[d]] !== id) rotas.push(id + "." + d);
02331:     }
02332:     if (!internos) aisladas.push(id);
02333:   }
02334:   let componentes = 0; const resto = new Set(ids);
02335:   while (resto.size) { componentes++; for (const id of recorrerMundo329(resto.values().next().value,null,rooms)) resto.delete(id); }
02336:   const abiertas = recorrerMundo329("patio_raices",null,rooms), cerradas = recorrerMundo329("patio_raices",crearEstadoGates(),rooms);
02337:   const bloqueadasPorArea = {}; for (const id of ids) if (!cerradas.has(id)) bloqueadasPorArea[rooms[id].area] = (bloqueadasPorArea[rooms[id].area]||0)+1;
02338:   for (const [actual,esperado,nombre] of [[ids.length,329,"rooms"],[areas.size,17,"áreas"],[exits,787,"exits"],[externos.length,1,"excepción externa"],[rotas.length,0,"reciprocidades rotas"],[aisladas.length,0,"aisladas"],[componentes,1,"componentes"],[abiertas.size,329,"alcanzables físicas"],[cerradas.size,185,"alcanzables iniciales"]]) if(actual!==esperado) errores.push(nombre+": "+actual+" / esperado "+esperado);
02339:   const esperado = {primera_ala:41,alturas:20,archivos:16,formaciones:17,secta_interior:22,mantenimiento:15,nucleo:13};
02340:   for(const area of new Set([...Object.keys(esperado),...Object.keys(bloqueadasPorArea)]))if(bloqueadasPorArea[area]!==esperado[area])errores.push("Distribución bloqueada: "+area);
02341:   for (const id of ["patio_raices","descansillo","mirador_niebla","patio_practica","camino","puerta","registro","patio"]) if(!rooms[id])errores.push("Superviviente ausente: "+id);
02342:   for(const g of GATES_329)if(!g.extremos.every((id,i)=>Object.values(rooms[id]?.exits||{}).includes(g.extremos[1-i])))errores.push("Gate sin conexión: "+g.id);
02343:   if(GATES_329.filter(g=>g.id.startsWith("ATAJO_ALA_")).length!==6)errores.push("Atajos: se esperan 6");
02344:   if(Object.values(rooms).filter(r=>r.alojamiento).length!==13||ALOJAMIENTOS_329.some(id=>!rooms[id]?.alojamiento))errores.push("Alojamientos: se esperan los 13 canónicos");
02345:   if(Object.values(rooms.ala_camara_dos_alas?.exits||{}).includes("ala_galeria_distribucion")||Object.values(rooms.ala_galeria_distribucion?.exits||{}).includes("ala_camara_dos_alas"))errores.push("Conexión directa prohibida");
02346:   return {ok:!errores.length,errores,rooms:ids.length,areas:areas.size,exits,externos,reciprocidadesRotas:rotas.length,aisladas:aisladas.length,componentes,alcanzablesFisicas:abiertas.size,alcanzablesIniciales:cerradas.size,bloqueadas:ids.length-cerradas.size,bloqueadasPorArea};
02347: }
02348: function validarSave329(data) {
02349:   const errores = [];
02350:   try {
02351:     // La versión se inspecciona antes de cualquier otro campo, incluso con getters hostiles.
02352:     if (data?.saveSchemaVersion !== SAVE_SCHEMA_VERSION) return [MENSAJE_SAVE_INCOMPATIBLE];
02353:     const fail = p => errores.push(p + ": estructura o valor inválido");
02354:     const plain = x => x !== null && typeof x === "object" && !Array.isArray(x) && [Object.prototype, null].includes(Object.getPrototypeOf(x));
02355:     const obj = (x,p) => { if (!plain(x)) { fail(p); return {}; } return x; };
02356:     const arr = (x,p) => { if (!Array.isArray(x)) { fail(p); return []; } return x; };
02357:     const has = (o,k) => Object.hasOwn(o,k);
02358:     const ref = (o,k) => typeof k === "string" && has(o,k);
02359:     const num = (x,p,min=0) => { if (typeof x !== "number" || !Number.isFinite(x) || x < min) fail(p); };
02360:     const integer = (x,p,min=0) => { num(x,p,min); if (!Number.isInteger(x)) fail(p); };
02361:     const str = (x,p) => { if (typeof x !== "string") fail(p); };
02362:     const bool = (x,p) => { if (typeof x !== "boolean") fail(p); };
02363:     const keys = (x,expected,p) => { if (Object.keys(x).length !== expected.length || expected.some(k=>!has(x,k))) fail(p); };
02364:     const references = (x,table,p) => arr(x,p).forEach(k=>{if(!ref(table,k))fail(p);});
02365:     // Sólo JSON finito; sin ciclos ni claves capaces de modificar prototipos al copiar.
02366:     const pending=[data], seen=new Set();
02367:     while(pending.length){const x=pending.pop();if(x===null||typeof x==='string'||typeof x==='boolean')continue;
02368:       if(typeof x==='number'){if(!Number.isFinite(x))fail('JSON');continue;}
02369:       if(typeof x!=='object'||seen.has(x)){fail('JSON');continue;}seen.add(x);
02370:       for(const k of Object.keys(x)){if(['__proto__','constructor','prototype'].includes(k))fail('JSON.'+k);pending.push(x[k]);}}
02371:     obj(data,'save');
02372:     const required=['saveSchemaVersion','gates','player','pos','flags','quests','salas','visitadas','atlas','saturacion','turnoGlobal','relojEcologico','respawnEn','interrupcionEn','errantes','cadaveres','objetosTirados','fecha'];
02373:     const npcV1=has(data,'npc_version');
02374:     keys(data,npcV1 ? [...required,'npc_version','posicionNPC','conocimientoNPC'] : required,'save.campos');
02375:     if(npcV1){
02376:       if(data.npc_version!==1)fail('npc_version');
02377:       const posiciones=obj(data.posicionNPC,'posicionNPC');
02378:       const conocimientos=obj(data.conocimientoNPC,'conocimientoNPC');
02379:       const ids=Object.keys(NPC_DEF),revelaciones=Array.from({length:10},(_,i)=>'R'+(i+1));
02380:       const estados=new Set(['DESCONOCIDO','SOSPECHA','SABE','CONFIRMADO']);
02381:       keys(posiciones,ids,'posicionNPC.ids');keys(conocimientos,ids,'conocimientoNPC.ids');
02382:       for(const id of ids){
02383:         const posicion=obj(posiciones[id],'posicionNPC.'+id),saber=obj(conocimientos[id],'conocimientoNPC.'+id);
02384:         keys(posicion,['sala','anclaje'],'posicionNPC.'+id);
02385:         const anclaje=posicion.anclaje;
02386:         if(!ref(ROOMS,posicion.sala))fail('posicionNPC.'+id+'.sala');
02387:         if(anclaje===null){if(!NPC_DEF[id].posicion_valida.includes(posicion.sala))fail('posicionNPC.'+id+'.territorio');}
02388:         else {const a=obj(anclaje,'posicionNPC.'+id+'.anclaje');keys(a,['room','hasta'],'posicionNPC.'+id+'.anclaje');
02389:           if(!ref(ROOMS,a.room)||posicion.sala!==a.room)fail('posicionNPC.'+id+'.anclaje.room');}
02390:         keys(saber,revelaciones,'conocimientoNPC.'+id);
02391:         for(const r of revelaciones)if(!estados.has(saber[r]))fail('conocimientoNPC.'+id+'.'+r);
02392:       }
02393:     }
02394:     if(!ref(ROOMS,data.pos))fail('pos');
02395:     integer(data.turnoGlobal,'turnoGlobal');integer(data.relojEcologico,'relojEcologico');num(data.fecha,'fecha');
02396:     if(!Number.isFinite(new Date(data.fecha).getTime()))fail('fecha');
02397:     obj(data.flags,'flags');
02398:     for(const [k,v]of Object.entries(obj(data.quests,'quests')))if(!ref(QUESTS,k)||typeof v!=='string')fail('quests.'+k);
02399:     references(data.visitadas,ROOMS,'visitadas');
02400:     const gates=obj(data.gates,'gates');keys(gates,GATES_329.map(g=>g.id),'gates');
```

## NPC runtime: presencia/movimiento/anclajes

Fuente: `grulla-blanca_ver74.html` · líneas 16735-16815

```js
16735:       this.addLine("En el suelo: " + tirados.join(", "), "sala-meta sala-objetos");
16736:     }
16737:     const criaturasVivas = this.vivos.filter(m => m.hp > 0);
16738:     const cadaveres = this.cadaveresEnSala().filter(c => !this.cuerpoExamenAgotado(c));
16739:     if (criaturasVivas.length) this.addLine("Criaturas: " + criaturasVivas.map(m => capitalizarUI(etiquetaMob(m))).join(", "), "sala-meta sala-criaturas");
16740:     if (cadaveres.length) {
16741:       const grupos = new Map();
16742:       for (const c of cadaveres) {
16743:         const nombre = this.etiquetaCadaver(c);
16744:         grupos.set(nombre, (grupos.get(nombre) || 0) + 1);
16745:       }
16746:       const nombres = [...grupos].map(([nombre, cantidad]) => capitalizarUI(nombre) + (cantidad > 1 ? ` (${cantidad})` : ""));
16747:       this.addLine("Restos: " + nombres.join(", "), "sala-meta sala-restos");
16748:     } else if (!criaturasVivas.length && this._huboMobsEnCooldown) {
16749:       this.addLine("No hay nada aquí ahora: lo que fuera que rondaba se movió hace poco.", "sala-meta sala-movimiento");
16750:     }
16751:     const recienLlegados = criaturasVivas.filter(m => m.errante_id && m.errante_desde && m.errante_movido_en === this.turnoGlobal);
16752:     if (recienLlegados.length) {
16753:       this.addLine("Movimiento reciente: " + recienLlegados.map(m => `${capitalizarUI(etiquetaMob(m))} llegó desde ${ROOMS[m.errante_desde].name}`).join("; ") + ".", "sala-meta sala-movimiento");
16754:     }
16755:     const npcs = this.npcsEnSala(this.pos);
16756:     if (npcs.length) this.addLine("Gente: " + npcs.map(n => capitalizarUI(NOMBRES_NPC[n])).join(", "), "sala-meta sala-gente");
16757:     this.addLine("Salidas: " + Object.keys(sala.exits || {}).map(capitalizarUI).join(", "), "sala-meta sala-salidas");
16758:     this.abajo();
16759:   }
16760: 
16761:   cumple(req) {
16762:     if (req.comprension && this.player.comprension < req.comprension) return false;
16763:     if (req.flag && !this.flags[req.flag]) return false;
16764:     if (req.no_flag && this.flags[req.no_flag]) return false;
16765:     return true;
16766:   }
16767: 
16768:   npcsEnSala(rid) {
16769:     if (!Object.hasOwn(ROOMS,rid)) return [];
16770:     return Object.keys(NPC_DEF).filter(id => this.posicionNPC?.[id]?.sala === rid);
16771:   }
16772: 
16773:   npcPresente(id, rid=this.pos) {
16774:     return Object.hasOwn(NPC_DEF,id) && Object.hasOwn(ROOMS,rid) && this.posicionNPC?.[id]?.sala === rid;
16775:   }
16776: 
16777:   // Un paso explícito; la dirección/cadencia futura queda sin definir.
16778:   puedeMoverNPC(id, origen, destino) {
16779:     if (!this.npcPresente(id,origen) || !Object.hasOwn(ROOMS,destino)) return false;
16780:     const actual=this.posicionNPC[id];
16781:     if (actual.anclaje !== null) return false;
16782:     if (!NPC_DEF[id].posicion_valida.includes(destino)) return false;
16783:     if (!Object.values(ROOMS[origen].exits).includes(destino)) return false;
16784:     return pasoGateAbierto(origen,destino,this.gates);
16785:   }
16786: 
16787:   aplicarMovimientoNPC(id, destino) {
16788:     const origen=this.posicionNPC?.[id]?.sala;
16789:     if (!this.puedeMoverNPC(id,origen,destino)) return false;
16790:     this.posicionNPC[id]={...this.posicionNPC[id],sala:destino};
16791:     return true; // No altera Atlas: sólo observar actualiza el último avistamiento.
16792:   }
16793: 
16794:   // ---------- bucle ----------
16795: 
16796:   itemsNaturalesVisibles() {
16797:     const sala = this.rooms[this.pos];
16798:     const vis = [...(sala.items || [])];
16799:     if (this.tieneSentido()) vis.push(...(sala.oculto || []));
16800:     // Guardarraíl: ningún material de planta recolectable puede colarse en "Ves:".
16801:     // Si una sala declara uno por error, se ignora aquí en vez de mostrarse como
16802:     // objeto suelto (las plantas viven en NODOS_HERBORISTERIA y salen en "Plantas:").
16803:     return vis.filter(mid => !MATERIALES_RECOLECTABLES.has(mid));
16804:   }
16805: 
16806:   objetosTiradosEnSala(rid = this.pos) {
16807:     this.objetosTirados ||= {};
16808:     const activos = (this.objetosTirados[rid] || []).filter(reg =>
16809:       reg && ITEMS[reg.mid] && Number.isFinite(reg.desapareceEn) && this.turnoGlobal < reg.desapareceEn);
16810:     if (activos.length) this.objetosTirados[rid] = activos;
16811:     else delete this.objetosTirados[rid];
16812:     return activos;
16813:   }
16814: 
16815:   itemsVisibles() {
```

## crearConocimientoNPC

Fuente: `grulla-blanca_ver74.html` · líneas 6754-6794

```js
06754:   return id && presentes.includes(id) ? id : null;
06755: }
06756: function crearPosicionNPC() {
06757:   return Object.fromEntries(Object.entries(NPC_DEF).map(([id,def]) => [id,{sala:def.sala_inicial,anclaje:null}]));
06758: }
06759: function crearConocimientoNPC() {
06760:   return JSON.parse(JSON.stringify(Object.fromEntries(Object.entries(NPC_DEF).map(([id,def]) => [id,def.conocimiento_inicial]))));
06761: }
06762: 
06763: // Respuestas de ENTREGAR cuando no hay nada que entregarle a ese NPC todavía
06764: // (misión activa pero no lista) o directamente no hay ningún encargo suyo
06765: // pendiente. Cada NPC responde con su propia voz; "default" cubre a
06766: // cualquiera que no tenga entrada propia.
06767: const FRASES_MISION_INCOMPLETA = {default: progreso => `—Todavía no completaste eso. (${progreso})`};
06768: const FRASES_SIN_ENCARGO = {default: "No parece esperar nada de vos."};
06769: 
06770: const SLOTS = ["mano", "torso", "cabeza", "piernas", "dedo", "cuello"];
06771: 
06772: // ---------- ITEMS · índice por categoría (42 objetos) ----------
06773: // Agrupado por `tipo`/`slot`, no por acto: a diferencia de ROOMS y MOBS, un
06774: // arco nuevo no suma una categoría nueva, normalmente suma objetos a estas
06775: // mismas (o, si el arco trae un slot o tipo realmente nuevo, ese es el
06776: // momento de agregar una fila acá).
06777: //   equipo · mano (armas)     espada_madera, cuchillo_hueso, espada_hierro
06778: //   equipo · torso            uniforme, uniforme_interno, tunica_reforzada
06779: //   equipo · cabeza/piernas/  bandana_cuero, sandalias_viento,
06780: //     cuello/dedo             amuleto_diente, anillo
06781: //   consumibles                pocion, pocion_refinada, pildora_meridianos,
06782: //                              elixir_tempestad, pildora_purificacion,
06783: //                              elixir_qi
06784: //   reliquias                  pildora_consolidacion, pildora_fundacion,
06785: //                              perla_marea, pluma_celeste, corazon_grulla
06786: //   materiales (crafteo)       hierba_claridad, raiz_sangre, musgo_lunar,
06787: //                              polvo_nube, aguijon_jade, caparazon_hierro,
06788: //                              pluma_tempestad
06789: 
06790: //   tesoros                    semilla_bifurcada, bolsa_piedras, bolsa_qian
06791: //   manuales (enseñan una      manual_sello, manual_paso, manual_piel,
06792: //     técnica de TECNICAS)     manual_filamento, manual_espejo,
06793: //                              manual_lanza_nube, manual_circulo_ascuas,
06794: //                              manual_lluvia_filos, manual_marea_circular,
```

## crearPosicionNPC

Fuente: `grulla-blanca_ver74.html` · líneas 6751-6791

```js
06751: }
06752: function resolverNPC(valor, presentes=Object.keys(NPC_DEF)) {
06753:   const id=INDICE_ALIAS_NPC.get(normalizarAliasNPC(valor));
06754:   return id && presentes.includes(id) ? id : null;
06755: }
06756: function crearPosicionNPC() {
06757:   return Object.fromEntries(Object.entries(NPC_DEF).map(([id,def]) => [id,{sala:def.sala_inicial,anclaje:null}]));
06758: }
06759: function crearConocimientoNPC() {
06760:   return JSON.parse(JSON.stringify(Object.fromEntries(Object.entries(NPC_DEF).map(([id,def]) => [id,def.conocimiento_inicial]))));
06761: }
06762: 
06763: // Respuestas de ENTREGAR cuando no hay nada que entregarle a ese NPC todavía
06764: // (misión activa pero no lista) o directamente no hay ningún encargo suyo
06765: // pendiente. Cada NPC responde con su propia voz; "default" cubre a
06766: // cualquiera que no tenga entrada propia.
06767: const FRASES_MISION_INCOMPLETA = {default: progreso => `—Todavía no completaste eso. (${progreso})`};
06768: const FRASES_SIN_ENCARGO = {default: "No parece esperar nada de vos."};
06769: 
06770: const SLOTS = ["mano", "torso", "cabeza", "piernas", "dedo", "cuello"];
06771: 
06772: // ---------- ITEMS · índice por categoría (42 objetos) ----------
06773: // Agrupado por `tipo`/`slot`, no por acto: a diferencia de ROOMS y MOBS, un
06774: // arco nuevo no suma una categoría nueva, normalmente suma objetos a estas
06775: // mismas (o, si el arco trae un slot o tipo realmente nuevo, ese es el
06776: // momento de agregar una fila acá).
06777: //   equipo · mano (armas)     espada_madera, cuchillo_hueso, espada_hierro
06778: //   equipo · torso            uniforme, uniforme_interno, tunica_reforzada
06779: //   equipo · cabeza/piernas/  bandana_cuero, sandalias_viento,
06780: //     cuello/dedo             amuleto_diente, anillo
06781: //   consumibles                pocion, pocion_refinada, pildora_meridianos,
06782: //                              elixir_tempestad, pildora_purificacion,
06783: //                              elixir_qi
06784: //   reliquias                  pildora_consolidacion, pildora_fundacion,
06785: //                              perla_marea, pluma_celeste, corazon_grulla
06786: //   materiales (crafteo)       hierba_claridad, raiz_sangre, musgo_lunar,
06787: //                              polvo_nube, aguijon_jade, caparazon_hierro,
06788: //                              pluma_tempestad
06789: 
06790: //   tesoros                    semilla_bifurcada, bolsa_piedras, bolsa_qian
06791: //   manuales (enseñan una      manual_sello, manual_paso, manual_piel,
```

