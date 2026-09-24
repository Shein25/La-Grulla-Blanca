# Extracto 07 — Rooms/topología/alojamientos

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## GATES_329 y ALOJAMIENTOS_329

Fuente: `grulla-blanca_ver74.html` · líneas 2195-2308

```js
02195: }
02196: // 3C.1 — Fundación estructural. Fuente física única: Topologia_329_Estructurada_v2.json.
02197: const SAVE_SCHEMA_VERSION = 2;
02198: const MENSAJE_SAVE_INCOMPATIBLE = "Save incompatible con el mundo de 329 salas. No se importó ningún estado. Inicia una Nueva Partida.";
02199: const GATES_329 = [
02200:   {
02201:     "id": "ATAJO_ALA_AGUAS",
02202:     "extremos": [
02203:       "aguas_conducto_antiguo",
02204:       "ala_aguas_06"
02205:     ]
02206:   },
02207:   {
02208:     "id": "ATAJO_ALA_ARCHIVOS",
02209:     "extremos": [
02210:       "ala_archivos_06",
02211:       "archivos_conducto_antiguo"
02212:     ]
02213:   },
02214:   {
02215:     "id": "ATAJO_ALA_CANTERA",
02216:     "extremos": [
02217:       "ala_cantera_06",
02218:       "conducto_antiguo_cantera"
02219:     ]
02220:   },
02221:   {
02222:     "id": "ATAJO_ALA_FORMACIONES",
02223:     "extremos": [
02224:       "ala_formaciones_06",
02225:       "formaciones_conducto_antiguo"
02226:     ]
02227:   },
02228:   {
02229:     "id": "ATAJO_ALA_JARDINES",
02230:     "extremos": [
02231:       "ala_jardines_06",
02232:       "conducto_antiguo_jardines"
02233:     ]
02234:   },
02235:   {
02236:     "id": "ATAJO_ALA_MEDICINA",
02237:     "extremos": [
02238:       "ala_med_06",
02239:       "sotano_conductos_medicina"
02240:     ]
02241:   },
02242:   {
02243:     "id": "PASO_MANTENIMIENTO",
02244:     "extremos": [
02245:       "ala_umbral_mantenimiento",
02246:       "mantenimiento_acceso"
02247:     ]
02248:   },
02249:   {
02250:     "id": "SECTA_INTERIOR",
02251:     "extremos": [
02252:       "escalinata_interior",
02253:       "interior_umbral_sur"
02254:     ]
02255:   },
02256:   {
02257:     "id": "M12",
02258:     "extremos": [
02259:       "formaciones_descenso_tecnico",
02260:       "formaciones_sello_antiguo"
02261:     ]
02262:   },
02263:   {
02264:     "id": "PASO_NUCLEO",
02265:     "extremos": [
02266:       "mantenimiento_compuerta_nucleo",
02267:       "nucleo_pozo_voto"
02268:     ]
02269:   },
02270:   {
02271:     "id": "PASO_PULSO",
02272:     "extremos": [
02273:       "nucleo_archivo_promesa",
02274:       "nucleo_descenso_pulso"
02275:     ]
02276:   }
02277: ];
02278: const ALOJAMIENTOS_329 = [
02279:   "dormitorio_externos",
02280:   "sala_recuperacion",
02281:   "caseta_jardineros",
02282:   "barracon_trabajadores",
02283:   "puesto_valle",
02284:   "bosque_refugio_patrulla",
02285:   "barracon_canteros",
02286:   "aguas_refugio_cauce",
02287:   "sauces_casa_huespedes",
02288:   "interior_cuartos_huespedes",
02289:   "alturas_caseta_guardacumbre",
02290:   "mantenimiento_dormitorio_turnos",
02291:   "nucleo_sala_relevo"
02292: ];
02293: const PENDIENTES_3C1 = Object.freeze({ alquimia: { sala: null, decision: "P03" }, sangre_huerto: { sala: null, decision: "P06" } });
02294: function esSalidaRegional(origen, direccion, destino) {
02295:   return origen === "mojon_regional" && direccion === "sur" && destino === "ruta_regional_arc2";
02296: }
02297: function crearEstadoGates() { return Object.fromEntries(GATES_329.map(g => [g.id, false])); }
02298: function normalizarEstadoGates(estado = {}) {
02299:   const limpio = crearEstadoGates();
02300:   for (const id of Object.keys(limpio)) limpio[id] = estado?.[id] === true;
02301:   if (!limpio.SECTA_INTERIOR) for (const id of Object.keys(limpio)) if (id === "M12" || id.startsWith("ATAJO_ALA_")) limpio[id] = false;
02302:   return limpio;
02303: }
02304: function gateEntre(origen, destino) { return GATES_329.find(g => g.extremos.includes(origen) && g.extremos.includes(destino)); }
02305: function pasoGateAbierto(origen, destino, estado) {
02306:   const gate = gateEntre(origen, destino);
02307:   return !gate || normalizarEstadoGates(estado)[gate.id] === true;
02308: }
```

## ROOM `patio_raices` · líneas 7586-7604

```js
07586:   "patio_raices": {
07587:     "id": "patio_raices",
07588:     "area": "acceso",
07589:     "name": "Patio de las Raíces",
07590:     "desc": "Un patio de piedra se abre alrededor de la Piedra de las Raíces. Una mesa baja ocupa uno de los lados y un arco de madera marca la salida hacia el norte. El espacio está dispuesto para recibir aspirantes, registrar resultados y separar a quienes continúan hacia el interior de la secta.",
07591:     "scenery": {
07592:   "piedra": "Una losa gris, lisa y fría ocupa el centro del patio; su superficie muestra el desgaste de innumerables manos.",
07593:   "marcas": "Huellas de palmas, humedad y polvo se acumulan sobre la piedra y alrededor de su base.",
07594:   "mesa": "Tinta, tablillas y registros provisionales ocupan la mesa utilizada durante los ingresos.",
07595:   "arco": "Un arco de madera delimita la salida norte y separa el patio de los espacios reservados a quienes ya han sido admitidos."
07596: },
07597:     "exits": {
07598:       "norte": "descansillo"
07599:     },
07600:     "items": [],
07601:     "mobs": [],
07602:     "npcs": [],
07603:     "vena": "normal"
07604:   },
```

## ROOM `descansillo` · líneas 7605-7626

```js
07605:   "descansillo": {
07606:     "id": "descansillo",
07607:     "area": "acceso",
07608:     "name": "Descansillo de Piedra",
07609:     "desc": "Una plataforma de losas grises interrumpe la pendiente y reparte el paso antes de que el camino se cierre entre los pinos. No tiene la solemnidad de una puerta ni la comodidad de un patio: es un lugar de transición, con bancos bajos, marcas de botas y espacio suficiente para ordenar las pocas pertenencias con las que llega un aspirante.",
07610:     "scenery": {
07611:   "losas": "La piedra muestra bordes gastados y líneas claras donde incontables suelas barrieron el polvo.",
07612:   "bancos": "Dos bancos de madera descansan contra el muro de contención. Están hechos para esperar o ajustar el equipo, no para instalarse.",
07613:   "muro": "Bloques desnudos contienen la ladera. Entre sus juntas crecen hebras de musgo y pequeñas raíces.",
07614:   "pendiente": "Desde aquí se percibe con claridad que el ascenso continúa: la montaña aún no ha concedido ninguna llegada."
07615: },
07616:     "exits": {
07617:       "sur": "patio_raices",
07618:       "este": "mirador_niebla",
07619:       "oeste": "patio_practica",
07620:       "norte": "sendero_pinos"
07621:     },
07622:     "items": [],
07623:     "mobs": [],
07624:     "npcs": [],
07625:     "vena": "pobre"
07626:   },
```

## ROOM `mirador_niebla` · líneas 7627-7644

```js
07627:   "mirador_niebla": {
07628:     "id": "mirador_niebla",
07629:     "area": "acceso",
07630:     "name": "Mirador de la Niebla",
07631:     "desc": "Una baranda de piedra mira hacia el mundo mortal. Muy abajo, los caminos son hilos oscuros entre campos apagados y tejados minúsculos. La niebla sube por la ladera sin prisa; aquí el qi es débil, pero circula limpio y constante.",
07632:     "scenery": {
07633:   "valle": "Desde aquí ya no distingues tu casa, tu calle ni la academia: sólo manchas de tierra y humo. La montaña vuelve pequeño todo lo que todavía pesa.",
07634:   "niebla": "Cruza la baranda y se deshace alrededor de tus manos. Entre una ráfaga y otra percibes un ritmo respirable.",
07635:   "baranda": "La piedra está pulida por aspirantes que necesitaron detenerse un momento antes de seguir subiendo."
07636: },
07637:     "exits": {
07638:       "oeste": "descansillo"
07639:     },
07640:     "items": [],
07641:     "mobs": [],
07642:     "npcs": [],
07643:     "vena": "normal"
07644:   },
```

## ROOM `patio_practica` · líneas 7645-7663

```js
07645:   "patio_practica": {
07646:     "id": "patio_practica",
07647:     "area": "acceso",
07648:     "name": "Patio de Práctica",
07649:     "desc": "Un rectángulo de tierra apisonada se abre contra la ladera, cercado por postes sencillos y un cobertizo estrecho. Surcos de pies, golpes en la madera y remiendos recientes muestran que aquí se aprende antes de entrar de lleno en la vida de la secta. Nada en el lugar busca impresionar: todo está hecho para resistir errores.",
07650:     "scenery": {
07651:   "suelo": "La tierra está compactada por pasos repetidos. Algunas huellas forman círculos torpes; otras terminan en largas marcas de arrastre.",
07652:   "postes": "Maderos de distinto grosor presentan abolladuras, astillas y vendas de cuerda donde la superficie se abrió.",
07653:   "cobertizo": "Bajo el techo se guardan piezas de entrenamiento, paños y herramientas de reparación. No hay objetos ceremoniales.",
07654:   "marcas": "Pequeñas líneas de cal delimitan posiciones y distancias de práctica, borradas y rehechas muchas veces."
07655: },
07656:     "exits": {
07657:       "este": "descansillo"
07658:     },
07659:     "items": [],
07660:     "mobs": [],
07661:     "npcs": [],
07662:     "vena": "pobre"
07663:   },
```

## ROOM `sendero_pinos` · líneas 7664-7682

```js
07664:   "sendero_pinos": {
07665:     "id": "sendero_pinos",
07666:     "area": "acceso",
07667:     "name": "Sendero de los Pinos",
07668:     "desc": "El paso se estrecha entre pinos viejos cuyas raíces levantan la tierra y obligan a mirar dónde se pisa. La senda conserva señales de uso constante sin llegar a parecer una vía principal: piedra, agujas secas y pequeños escalones hechos donde la pendiente lo exige. La presencia de la secta empieza a sentirse más en el cuidado del camino que en cualquier adorno.",
07669:     "scenery": {
07670:   "pinos": "Los troncos crecen inclinados hacia fuera de la ladera. Las ramas más bajas han sido podadas para mantener libre el paso.",
07671:   "raices": "Cruzan la senda como nudillos oscuros. Algunas fueron rebajadas con herramientas; otras obligan a levantar el pie.",
07672:   "escalones": "Bloques irregulares completan los tramos más empinados. Ninguno parece pertenecer a la misma obra.",
07673:   "agujas": "Una capa de agujas secas amortigua los pasos y guarda pequeñas manchas de resina."
07674: },
07675:     "exits": {
07676:       "sur": "descansillo",
07677:       "norte": "camino"
07678:     },
07679:     "items": [],
07680:     "mobs": [],
07681:     "npcs": []
07682:   },
```

## ROOM `camino` · líneas 7683-7703

```js
07683:   "camino": {
07684:     "id": "camino",
07685:     "area": "acceso",
07686:     "name": "Camino de la Montaña",
07687:     "desc": "Los escalones de piedra suben entre pinos torcidos. A ambos lados, la niebla tapa la montaña y arriba las nubes se tragan el camino. Más abajo queda todo lo que conocías; aquí parece empezar la fila de los que llegaron con poco y esperaban mucho. La hierba crece entre las piedras del borde allí donde el tránsito deja algo de espacio.",
07688:     "scenery": {
07689:   "escalones": "Están tallados a pico, uno por cada discípulo de otra era, dicen. Algunos están torcidos, otros parecen hechos con prisa y unos cuantos tienen golpes secos en los bordes, como si quien los talló estuviera enfadado con la piedra.",
07690:   "pinos": "Los pinos se agarran a la roca con las raíces al descubierto. El viento no los dobló: los torció.",
07691:   "hierba": "La hierba se aprieta entre piedras y raíces, más alta en los bordes donde casi nadie pisa."
07692: },
07693:     "exits": {
07694:       "sur": "sendero_pinos",
07695:       "norte": "puerta"
07696:     },
07697:     "items": [
07698:       "anillo"
07699:     ],
07700:     "mobs": [],
07701:     "npcs": [],
07702:     "vena": "pobre"
07703:   },
```

## ROOM `puerta` · líneas 7704-7723

```js
07704:   "puerta": {
07705:     "id": "puerta",
07706:     "area": "acceso",
07707:     "name": "Puerta Roja",
07708:     "desc": "Dos hojas de madera teñida de rojo ocupan el paso entre muros de piedra oscura. El color está gastado en bordes y travesaños, pero la puerta conserva una gravedad que el camino no tenía: cruzarla significa dejar de ser alguien que simplemente sube la montaña. Más allá comienza el espacio administrado de la Grulla Blanca.",
07709:     "scenery": {
07710:   "hojas": "La madera es gruesa, reforzada con bandas de hierro ennegrecido. El rojo no brilla; ha sido renovado tantas veces que forma capas visibles en las grietas.",
07711:   "clavos": "Cabezas de hierro cuadradas sujetan los refuerzos. Algunas llevan pequeñas marcas de inspección.",
07712:   "muros": "La piedra encaja sin ornamentación. No es una muralla de guerra, sino una frontera hecha para durar.",
07713:   "umbral": "El desgaste del suelo forma una franja pálida bajo las hojas. Miles de pasos atravesaron exactamente el mismo punto."
07714: },
07715:     "exits": {
07716:       "sur": "camino",
07717:       "norte": "registro"
07718:     },
07719:     "items": [],
07720:     "mobs": [],
07721:     "npcs": [],
07722:     "vena": "normal"
07723:   },
```

## ROOM `registro` · líneas 7724-7743

```js
07724:   "registro": {
07725:     "id": "registro",
07726:     "area": "acceso",
07727:     "name": "Vestíbulo del Registro",
07728:     "desc": "Un vestíbulo sobrio recibe a quienes han cruzado la Puerta Roja. Mesas estrechas, estantes de tablillas y cajas numeradas convierten la llegada en un procedimiento: nombres, procedencias, asignaciones y pertenencias deben ocupar su sitio antes de que alguien pueda llamarse miembro de la secta. El aire parece más quieto aquí, como si hasta el qi respetara el orden de los registros.",
07729:     "scenery": {
07730:   "mesas": "Superficies largas y sin adornos, manchadas de tinta en los bordes donde se apoyan los pinceles.",
07731:   "tablillas": "Filas de madera fina esperan nombres, notas y sellos. Algunas están recién lijadas; otras muestran correcciones raspadas.",
07732:   "cajas": "Cajones bajos llevan números y caracteres de clasificación. Nada indica qué contienen sin conocer el sistema.",
07733:   "sellos": "Varios sellos descansan en soportes de piedra junto a almohadillas de tinta oscura. Su uso parece más importante que su aspecto."
07734: },
07735:     "exits": {
07736:       "sur": "puerta",
07737:       "norte": "sala_jade"
07738:     },
07739:     "items": [],
07740:     "mobs": [],
07741:     "npcs": [],
07742:     "vena": "muerta"
07743:   },
```

## ROOM `sala_jade` · líneas 7766-7785

```js
07766:   "sala_jade": {
07767:     "id": "sala_jade",
07768:     "area": "secta_exterior",
07769:     "name": "Sala del Jade",
07770:     "desc": "Un recinto silencioso sirve de umbral entre el registro de los recién llegados y la vida cotidiana de la secta. El aire huele a piedra fría y cera vieja. Un muro monumental de jade verde oliva domina la sala, cubierto por miles de nombres tallados con una paciencia que vuelve insignificante a cualquier visitante individual. Entre las hileras regulares, una irregularidad rompe por un instante la continuidad de la superficie.",
07771:     "scenery": {
07772:   "muro": "Miles de caracteres recorren el jade en hileras disciplinadas. Algunos conservan un barniz dorado que señala ascensos o reconocimientos; la mayoría permanece sobria, parte de una memoria demasiado grande para destacar a todos.",
07773:   "nombres": "Hay generaciones enteras comprimidas en la piedra: caracteres nítidos, otros suavizados por restauraciones y algunos casi absorbidos por vetas del propio jade.",
07774:   "tajo": "Entre las inscripciones, un nombre fue atravesado por un corte profundo e irregular. El surco rompe la superficie pulida y borra parte de los caracteres de Shen Liang sin borrar del todo que estuvieron allí.",
07775:   "cera": "Pequeñas acumulaciones endurecidas junto al muro revelan antiguos trabajos de iluminación y mantenimiento. No forman un altar.",
07776:   "suelo": "La piedra frente al muro está más pulida que el resto, como si muchas personas se hubieran detenido allí antes de seguir."
07777: },
07778:     "exits": {
07779:       "sur": "registro",
07780:       "norte": "patio"
07781:     },
07782:     "items": [],
07783:     "mobs": [],
07784:     "npcs": []
07785:   },
```

## ROOM `patio` · líneas 7744-7765

```js
07744:   "patio": {
07745:     "id": "patio",
07746:     "area": "secta_exterior",
07747:     "name": "Patio de los Discípulos Externos",
07748:     "desc": "Un patio amplio articula la vida de la Secta Exterior. Desde aquí se distribuyen los caminos hacia los dormitorios, los servicios y el sector de práctica, mientras el tránsito deja una mezcla constante de pasos, voces contenidas y tareas que cambian de manos. La arquitectura es sencilla pero cuidada: piedra barrida, aleros reparados y espacios pensados para que mucha gente pueda convivir sin confundirse.",
07749:     "scenery": {
07750:   "pavimento": "Grandes losas forman una superficie desigual pero limpia. Las juntas han sido rellenadas tantas veces que muestran distintos tonos de mortero.",
07751:   "aleros": "Los tejados bajos rodean parte del patio y ofrecen resguardo sin convertir el lugar en un corredor cerrado.",
07752:   "canales": "Canaletas poco profundas conducen el agua hacia los bordes del recinto. Están libres de hojas y sedimentos.",
07753:   "marcas": "Pequeños símbolos pintados en postes y esquinas orientan hacia servicios, dormitorios y práctica sin necesidad de carteles grandes."
07754: },
07755:     "exits": {
07756:       "sur": "sala_jade",
07757:       "oeste": "patio_cabanas",
07758:       "este": "patio_servicios",
07759:       "norte": "patio_campana"
07760:     },
07761:     "items": [],
07762:     "mobs": [],
07763:     "npcs": [],
07764:     "vena": "normal"
07765:   },
```

## ROOM `patio_cabanas` · líneas 7786-7806

```js
07786:   "patio_cabanas": {
07787:     "id": "patio_cabanas",
07788:     "area": "secta_exterior",
07789:     "name": "Patio de Cabañas",
07790:     "desc": "Un patio menor distribuye las dependencias residenciales de los discípulos externos. Cabañas bajas, tendederos discretos y pasos cubiertos hacen que el lugar se sienta utilizado sin caer en el desorden. Aquí la secta deja de parecer una institución abstracta y se vuelve un sitio donde la gente guarda ropa, comparte espacio y aprende a vivir con poco.",
07791:     "scenery": {
07792:   "cabanas": "Construcciones de madera oscura y piedra baja se alinean sin lujo. Las reparaciones no coinciden entre sí, prueba de años de uso.",
07793:   "tendederos": "Cuerdas tensadas entre postes sostienen paños, vendas y prendas sencillas. No bloquean los pasos.",
07794:   "canal": "Una acequia estrecha recoge agua de lavado y lluvia, separada de las zonas de tránsito.",
07795:   "tablillas": "Pequeñas placas numeradas identifican dormitorios y dependencias comunes sin nombres personales."
07796: },
07797:     "exits": {
07798:       "este": "patio",
07799:       "oeste": "corredor_cabanas",
07800:       "norte": "comedor_externos",
07801:       "sur": "sala_comun_externos"
07802:     },
07803:     "items": [],
07804:     "mobs": [],
07805:     "npcs": []
07806:   },
```

## ROOM `corredor_cabanas` · líneas 7807-7826

```js
07807:   "corredor_cabanas": {
07808:     "id": "corredor_cabanas",
07809:     "area": "secta_exterior",
07810:     "name": "Corredor de Cabañas",
07811:     "desc": "Un corredor cubierto enlaza las dependencias más estrechas del sector residencial. El piso de madera cruje en algunos tramos y ha sido reforzado con piezas de distinto tono. Puertas sencillas, ganchos para ropa húmeda y bancos pegados a la pared hablan de un espacio pensado para circular, no para detenerse demasiado.",
07812:     "scenery": {
07813:   "piso": "Las tablas tienen zonas pulidas por el paso y pequeños parches donde la madera fue sustituida.",
07814:   "puertas": "No llevan adornos, solo números y marcas de asignación.",
07815:   "ganchos": "Clavijas de madera sostienen capas, toallas y algún cinturón de entrenamiento.",
07816:   "bancos": "Asientos estrechos permiten calzarse o esperar sin obstruir el corredor."
07817: },
07818:     "exits": {
07819:       "este": "patio_cabanas",
07820:       "oeste": "dormitorio_externos",
07821:       "sur": "lavadero_externos"
07822:     },
07823:     "items": [],
07824:     "mobs": [],
07825:     "npcs": []
07826:   },
```

## ROOM `dormitorio_externos` · líneas 7827-7849

```js
07827:   "dormitorio_externos": {
07828:     "id": "dormitorio_externos",
07829:     "area": "secta_exterior",
07830:     "name": "Dormitorio de Externos",
07831:     "desc": "Filas ordenadas de camas estrechas ocupan un dormitorio colectivo donde cada discípulo dispone de poco más que un colchón, un arcón y algunos ganchos. La austeridad no llega al abandono: las mantas están remendadas, el suelo limpio y los espacios medidos para que nadie pueda apropiarse de mucho más de lo necesario. Dormir aquí es aceptar que la vida en la secta también consiste en compartir límites.",
07832:     "scenery": {
07833:   "camas": "Estructuras de madera resistentes y casi idénticas. Los remiendos de algunas patas revelan reparaciones repetidas.",
07834:   "arcones": "Cada cama tiene un arcón bajo con cierre simple. La madera está marcada con números de asignación.",
07835:   "mantas": "Tejidos gruesos de color apagado, lavados tantas veces que las fibras se han vuelto suaves.",
07836:   "ganchos": "Unos pocos ganchos por plaza obligan a mantener el equipo reducido y ordenado."
07837: },
07838:     "exits": {
07839:       "este": "corredor_cabanas"
07840:     },
07841:     "items": [],
07842:     "mobs": [],
07843:     "npcs": [],
07844:     "alojamiento": {
07845:       "nombre": "Dormitorio de Externos",
07846:       "inicio": "Encuentras una cama asignada entre las filas del dormitorio. El espacio es austero, pero suficiente para descansar sin abandonar la seguridad de la Secta Exterior.",
07847:       "purifica": true
07848:     }
07849:   },
```

## ROOM `oficina_servicios` · líneas 7946-7964

```js
07946:   "oficina_servicios": {
07947:     "id": "oficina_servicios",
07948:     "area": "secta_exterior",
07949:     "name": "Oficina de Servicios",
07950:     "desc": "Mesas de registro, casilleros y estantes de formularios llenan una oficina pequeña donde el trabajo de la secta se convierte en asignaciones concretas. El mobiliario obliga a separar solicitudes, entregas y asuntos pendientes antes de que alguien pueda considerarlos resueltos. Todo sugiere una burocracia modesta, pero suficientemente rigurosa para que nadie pueda fingir que una tarea desapareció.",
07951:     "scenery": {
07952:   "casilleros": "Compartimentos rotulados separan solicitudes, materiales entregados y registros por revisar.",
07953:   "formularios": "Hojas y tablillas siguen formatos repetidos: nombre, tarea, responsable, resultado.",
07954:   "mesa": "La superficie principal tiene marcas de tinta y una zona limpia reservada para sellos.",
07955:   "sellos": "Sellos administrativos de uso corriente descansan en una bandeja; ninguno parece ceremonial."
07956: },
07957:     "exits": {
07958:       "sur": "patio_servicios",
07959:       "este": "deposito_comun"
07960:     },
07961:     "items": [],
07962:     "mobs": [],
07963:     "npcs": []
07964:   },
```

## ROOM `deposito_comun` · líneas 7985-8004

```js
07985:   "deposito_comun": {
07986:     "id": "deposito_comun",
07987:     "area": "secta_exterior",
07988:     "name": "Depósito Común",
07989:     "desc": "Estanterías robustas dividen un depósito dedicado a materiales de uso cotidiano: cuerda, recipientes, repuestos, tejidos, herramientas menores y reservas asignadas a servicios internos. Cada sección está marcada y casi todo se cuenta por unidades o lotes. La austeridad del lugar no proviene de la escasez, sino de una vigilancia constante sobre lo que entra y sale.",
07990:     "scenery": {
07991:   "estanterias": "Madera gruesa reforzada con escuadras. Los estantes bajos soportan las cargas más pesadas.",
07992:   "etiquetas": "Tablillas colgantes indican categoría y cantidad esperada, con números corregidos muchas veces.",
07993:   "cajas": "Contenedores cerrados protegen objetos pequeños que serían fáciles de extraviar.",
07994:   "registro": "Una tabla de movimientos permite anotar retiros y devoluciones sin depender de la memoria."
07995: },
07996:     "exits": {
07997:       "oeste": "oficina_servicios",
07998:       "sur": "tablon_encargos",
07999:       "norte": "casa_guardia"
08000:     },
08001:     "items": [],
08002:     "mobs": [],
08003:     "npcs": []
08004:   },
```

## ROOM `sala_anatomica` · líneas 8396-8414

```js
08396:   "sala_anatomica": {
08397:     "id": "sala_anatomica",
08398:     "area": "medicina",
08399:     "name": "Sala Anatómica",
08400:     "desc": "Mesas de estudio, modelos articulados y láminas anatómicas convierten esta sala en un espacio de observación sistemática. No hay espectáculo en la disposición: cada herramienta existe para comparar, medir y reconocer estructuras antes de intervenir sobre ellas. En esta sala se realiza el Examen Espiritual, apoyado en la misma práctica de observación sistemática que guía el resto del trabajo anatómico.",
08401:     "scenery": {
08402:   "modelos": "Figuras de madera y arcilla representan articulaciones, órganos y trayectos internos con distintos niveles de detalle.",
08403:   "laminas": "Dibujos anotados comparan anatomía común, lesiones y alteraciones asociadas al qi.",
08404:   "mesas": "Superficies amplias permiten colocar muestras, instrumentos y registros sin mezclarlos.",
08405:   "marcas": "Escalas y líneas de referencia facilitan medir tamaño, simetría y posición."
08406: },
08407:     "exits": {
08408:       "este": "corredor_medicina",
08409:       "oeste": "archivo_clinico"
08410:     },
08411:     "items": [],
08412:     "mobs": [],
08413:     "npcs": []
08414:   },
```

## ROOM `patio_marcial` · líneas 8082-8101

```js
08082:   "patio_marcial": {
08083:     "id": "patio_marcial",
08084:     "area": "secta_exterior",
08085:     "name": "Patio Marcial",
08086:     "desc": "Un patio abierto concentra la práctica física de los discípulos externos. Líneas pintadas, postes de impacto y zonas de espera ordenan ejercicios individuales y por parejas; la disposición favorece la práctica disciplinada antes que el espectáculo. Las huellas de uso son abundantes, pero también lo es el mantenimiento: aquí se espera que cada error deje aprendizaje, no ruinas.",
08087:     "scenery": {
08088:   "lineas": "Trazos de cal dividen espacios de práctica y distancias de seguridad. Algunas se superponen a marcas más antiguas.",
08089:   "postes": "Maderos de impacto presentan vendajes de cuerda y reparaciones donde la fibra se abrió.",
08090:   "armarios": "Gabinetes laterales guardan equipo común de práctica y materiales de reparación.",
08091:   "suelo": "Tierra firme mezclada con grava fina ofrece agarre sin volverse barro con facilidad."
08092: },
08093:     "exits": {
08094:       "oeste": "patio_campana",
08095:       "este": "sala_formas",
08096:       "norte": "pabellon_disciplina"
08097:     },
08098:     "items": [],
08099:     "mobs": [],
08100:     "npcs": []
08101:   },
```

## ROOM `sala_formas` · líneas 8102-8120

```js
08102:   "sala_formas": {
08103:     "id": "sala_formas",
08104:     "area": "secta_exterior",
08105:     "name": "Sala de Formas",
08106:     "desc": "Una sala rectangular ofrece un espacio controlado para repetir posturas, desplazamientos y secuencias sin las distracciones del patio. Marcas en el suelo indican ejes y posiciones, mientras espejos de metal pulido ocupan algunos tramos de pared sin llegar a devolver una imagen perfecta. El lugar favorece la corrección paciente por encima de la fuerza.",
08107:     "scenery": {
08108:   "marcas": "Líneas rectas y círculos discretos ayudan a comprobar distancia, orientación y colocación de los pies.",
08109:   "placas": "Placas de metal pulido reflejan siluetas deformadas pero suficientes para detectar posturas torcidas.",
08110:   "paredes": "La superficie está casi desnuda, salvo por anotaciones breves sobre equilibrio y respiración.",
08111:   "suelo": "Madera firme con reparaciones visibles en los puntos de mayor presión."
08112: },
08113:     "exits": {
08114:       "oeste": "patio_marcial",
08115:       "norte": "patio_respiracion"
08116:     },
08117:     "items": [],
08118:     "mobs": [],
08119:     "npcs": []
08120:   },
```

## ROOM `patio_respiracion` · líneas 8121-8139

```js
08121:   "patio_respiracion": {
08122:     "id": "patio_respiracion",
08123:     "area": "secta_exterior",
08124:     "name": "Patio de Respiración",
08125:     "desc": "Un patio resguardado reduce el ruido del sector marcial sin aislarse por completo de él. Bancos bajos y losas separadas dejan espacios individuales suficientes para trabajar respiración y circulación sin convertir la práctica en retiro solemne. El aire se mueve con facilidad entre los muros, y el lugar parece construido para aprender a mantener un ritmo en medio de una institución que nunca se detiene.",
08126:     "scenery": {
08127:   "losas": "Piedras planas separadas a distancias regulares marcan lugares de práctica individual.",
08128:   "bancos": "Asientos bajos permiten descansar entre ejercicios sin tumbarse.",
08129:   "muros": "No llegan a cerrar el patio por completo; dejan pasar aire y sonidos amortiguados del sector marcial.",
08130:   "inscripciones": "Frases breves recuerdan principios básicos de respiración y postura, sin técnicas avanzadas."
08131: },
08132:     "exits": {
08133:       "sur": "sala_formas",
08134:       "oeste": "pabellon_disciplina"
08135:     },
08136:     "items": [],
08137:     "mobs": [],
08138:     "npcs": []
08139:   },
```

## ROOM `pabellon_disciplina` · líneas 8140-8159

```js
08140:   "pabellon_disciplina": {
08141:     "id": "pabellon_disciplina",
08142:     "area": "secta_exterior",
08143:     "name": "Pabellón de Disciplina",
08144:     "desc": "Un pabellón sobrio reúne registros de faltas, normas de convivencia y asuntos que requieren una respuesta formal. El espacio no parece diseñado para intimidar: mesas ordenadas, estantes de expedientes y asientos separados bastan para recordar que las acciones dentro de la secta dejan constancia. La disciplina aquí se presenta como procedimiento antes que como castigo.",
08145:     "scenery": {
08146:   "normas": "Tablillas visibles resumen obligaciones básicas, límites de conducta y canales de reclamación.",
08147:   "expedientes": "Estantes cerrados contienen registros etiquetados por asunto y referencia administrativa, sin quedar expuestos a cualquiera.",
08148:   "mesa": "La mesa principal deja espacio para escribir, escuchar y revisar documentos sin adornos ceremoniales.",
08149:   "asientos": "Bancos individuales mantienen una distancia incómoda pero deliberada entre quienes esperan."
08150: },
08151:     "exits": {
08152:       "sur": "patio_marcial",
08153:       "este": "patio_respiracion",
08154:       "oeste": "corredor_norte"
08155:     },
08156:     "items": [],
08157:     "mobs": [],
08158:     "npcs": []
08159:   },
```

## ROOM `puesto_valle` · líneas 9182-9204

```js
09182:   "puesto_valle": {
09183:     "id": "puesto_valle",
09184:     "area": "valle",
09185:     "name": "Puesto del Valle",
09186:     "desc": "Un edificio robusto combina funciones de patrulla, mensajería, auxilio y descanso para quienes tienen autorización para usar la red territorial. Bancos, tablillas de rutas, equipo básico y camas sencillas comparten espacio sin que el puesto se convierta en cuartel. Es un lugar de frontera cotidiana, donde la secta trata con caminos y personas además de consigo misma.",
09187:     "scenery": {
09188:   "tablillas": "Rutas, avisos de tránsito e incidencias se organizan por sector.",
09189:   "equipo": "Capas, cuerdas, linternas y útiles de patrulla ocupan soportes accesibles.",
09190:   "bancos": "Asientos largos reciben viajeros, mensajeros o personas que esperan indicaciones.",
09191:   "camastros": "Un pequeño sector de descanso queda separado del área de atención."
09192: },
09193:     "exits": {
09194:       "este": "valle_explanada",
09195:       "sur": "patio_puesto_valle"
09196:     },
09197:     "items": [],
09198:     "mobs": [],
09199:     "npcs": [],
09200:     "alojamiento": {
09201:       "nombre": "puesto_valle",
09202:       "inicio": "El puesto te ofrece un camastro limpio y espacio para dejar el equipo. No es una residencia, pero sí un refugio seguro en medio de la red de caminos del Valle."
09203:     }
09204:   },
```

## ROOM `bosque_senda_patrulla` · líneas 9637-9655

```js
09637:   "bosque_senda_patrulla": {
09638:     "id": "bosque_senda_patrulla",
09639:     "area": "bosques",
09640:     "name": "Senda de Patrulla",
09641:     "desc": "Una ruta angosta pero reconocible atraviesa el bosque siguiendo una línea más práctica que escénica. Ramas cortadas, piedras movidas y pequeñas marcas de orientación revelan mantenimiento periódico. La senda conecta puntos útiles para vigilancia y refugio sin intentar domesticar el terreno que atraviesa.",
09642:     "scenery": {
09643:   "cortes": "Ramas bajas han sido retiradas para permitir el paso con equipo.",
09644:   "mojones": "Piedras apiladas discretamente confirman el trazado cuando la senda pierde definición.",
09645:   "pisadas": "El suelo compacto en ciertos tramos demuestra uso repetido por grupos pequeños.",
09646:   "margen": "La vegetación invade los bordes en cuanto deja de ser retirada, estrechando el paso de manera natural."
09647: },
09648:     "exits": {
09649:       "oeste": "bosque_puesto_marcas",
09650:       "sur": "bosque_refugio_patrulla"
09651:     },
09652:     "items": [],
09653:     "mobs": [],
09654:     "npcs": []
09655:   },
```

## ROOM `bosque_refugio_patrulla` · líneas 9696-9719

```js
09696:   "bosque_refugio_patrulla": {
09697:     "id": "bosque_refugio_patrulla",
09698:     "area": "bosques",
09699:     "name": "Refugio de Patrulla",
09700:     "desc": "Una construcción baja de piedra y madera ofrece techo, agua y suministros mínimos en medio del Bosque de la Niebla. El interior está pensado para que una patrulla pueda secar equipo, dormir y dejar notas antes de continuar. Es un refugio agreste: seguro para descansar, pero sin las instalaciones necesarias para purificar automáticamente heridas o aflicciones complejas.",
09701:     "scenery": {
09702:   "camastros": "Plataformas de madera con mantas gruesas ocupan una pared y pueden usarse sin preparación especial.",
09703:   "deposito": "Un armario protegido contiene cuerda, vendas, recipientes y provisiones sencillas.",
09704:   "hogar": "Un fogón de piedra permite calor y preparación básica sin llenar el refugio de humo.",
09705:   "registro": "Tablillas de patrulla guardan observaciones breves sobre rutas, daños y fauna vista en los alrededores."
09706: },
09707:     "exits": {
09708:       "norte": "bosque_senda_patrulla",
09709:       "oeste": "bosque_senda_niebla",
09710:       "sur": "bosque_quebrada_niebla"
09711:     },
09712:     "items": [],
09713:     "mobs": [],
09714:     "npcs": [],
09715:     "alojamiento": {
09716:       "nombre": "bosque_refugio_patrulla",
09717:       "inicio": "El refugio ofrece uno de sus camastros y un techo firme frente al bosque. Puedes recuperar fuerzas aquí, aunque el lugar carece de instalaciones para purificar estados complejos."
09718:     }
09719:   },
```

## ROOM `oficina_logistica` · líneas 8869-8887

```js
08869:   "oficina_logistica": {
08870:     "id": "oficina_logistica",
08871:     "area": "produccion",
08872:     "name": "Oficina de Logística",
08873:     "desc": "Una oficina estrecha concentra manifiestos, registros de consumo y movimientos de materiales. Estantes con tablillas, mapas de rutas y listas de necesidades ocupan más espacio que cualquier adorno. La administración de Producción se parece menos a mandar que a saber qué falta, qué sobra y por dónde debe moverse cada cosa.",
08874:     "scenery": {
08875:   "manifiestos": "Listas de entradas, salidas y destinos se apilan por lotes y procedencia.",
08876:   "mapas": "Esquemas sencillos muestran caminos hacia Cantera, Valle y dependencias internas.",
08877:   "estantes": "Compartimentos marcados separan pedidos pendientes, entregas confirmadas y registros archivados.",
08878:   "mesa": "La superficie principal está dividida en zonas de escritura, revisión y sellado."
08879: },
08880:     "exits": {
08881:       "sur": "patio_produccion",
08882:       "este": "cochera_carros"
08883:     },
08884:     "items": [],
08885:     "mobs": [],
08886:     "npcs": []
08887:   },
```

## ROOM `mercado_valle` · líneas 9245-9263

```js
09245:   "mercado_valle": {
09246:     "id": "mercado_valle",
09247:     "area": "valle",
09248:     "name": "Mercado del Camino",
09249:     "desc": "Puestos ligeros, toldos y mesas de intercambio ocupan un tramo abierto junto a la ruta. Comerciantes, trabajadores y viajeros pueden abastecerse o mover pequeñas mercancías sin entrar en una comunidad cerrada. El mercado pertenece al flujo del Valle: aparece como punto de encuentro entre caminos, no como plaza central de una aldea.",
09250:     "scenery": {
09251:   "puestos": "Estructuras desmontables ofrecen espacio para productos, herramientas y provisiones.",
09252:   "toldos": "Telas sencillas protegen mercancías sensibles sin cerrar la circulación.",
09253:   "balanzas": "Instrumentos de comercio común permiten pesar grano, sal y cargas menores.",
09254:   "zona_carga": "Un borde despejado conecta el mercado con el desvío usado por carros."
09255: },
09256:     "exits": {
09257:       "oeste": "encrucijada_valle",
09258:       "este": "valle_desvio_carretero"
09259:     },
09260:     "items": [],
09261:     "mobs": [],
09262:     "npcs": []
09263:   },
```

## ROOM `granero_valle` · líneas 9264-9282

```js
09264:   "granero_valle": {
09265:     "id": "granero_valle",
09266:     "area": "valle",
09267:     "name": "Granero del Valle",
09268:     "desc": "Una construcción elevada almacena parte de la producción agrícola del Valle antes de su distribución. Ventilación, separación del suelo y registros de lotes importan tanto como el volumen guardado. El granero es infraestructura comunitaria y logística, no una reserva secreta de la secta.",
09269:     "scenery": {
09270:   "tarima": "La estructura principal se eleva para reducir humedad y acceso de animales.",
09271:   "sacos": "Grano y semillas se agrupan por lote y procedencia.",
09272:   "ventilas": "Aberturas protegidas mantienen circulación de aire sin exponer el interior.",
09273:   "registro": "Tablillas anotan entrada, salida y destino de cada lote."
09274: },
09275:     "exits": {
09276:       "norte": "terrazas_norte",
09277:       "sur": "terrazas_sur"
09278:     },
09279:     "items": [],
09280:     "mobs": [],
09281:     "npcs": []
09282:   },
```

## ROOM `sauces_plaza` · líneas 11028-11048

```js
11028:   "sauces_plaza": {
11029:     "id": "sauces_plaza",
11030:     "area": "sauces",
11031:     "name": "Plaza de Sauces Bajos",
11032:     "desc": "Una plaza de tierra firme articula las calles, el pozo, la Casa Comunal y la Casa de Huéspedes sin intentar parecer un centro monumental. Bancos, árboles y espacios despejados permiten reuniones, intercambios y tareas cotidianas. La comunidad se siente anterior a cualquier visita de la secta: este lugar existe porque la gente de Sauces lo utiliza.",
11033:     "scenery": {
11034:   "bancos": "Asientos de madera y piedra ocupan los bordes sin cerrar el espacio central.",
11035:   "arboles": "Sauces maduros ofrecen sombra sobre sectores donde el suelo conserva humedad.",
11036:   "tablillas": "Avisos comunitarios anuncian trabajos, necesidades y asuntos comunes.",
11037:   "pavimento": "Tierra apisonada y franjas de piedra resisten el tránsito habitual sin convertir la plaza en patio institucional."
11038: },
11039:     "exits": {
11040:       "oeste": "sauces_camino_valle",
11041:       "norte": "sauces_casa_huespedes",
11042:       "sur": "sauces_pozo",
11043:       "este": "sauces_casa_comunal"
11044:     },
11045:     "items": [],
11046:     "mobs": [],
11047:     "npcs": []
11048:   },
```

## ROOM `sauces_casa_comunal` · líneas 11091-11109

```js
11091:   "sauces_casa_comunal": {
11092:     "id": "sauces_casa_comunal",
11093:     "area": "sauces",
11094:     "name": "Casa Comunal",
11095:     "desc": "Una sala de reuniones, archivos modestos y bancos compartidos permite discutir asuntos que afectan al conjunto de Sauces. Aquí se registran acuerdos, necesidades y responsabilidades sin imitar la burocracia de la secta. La comunidad trata con patrullas y autoridades externas desde este lugar, pero las decisiones locales no dejan por ello de ser propias.",
11096:     "scenery": {
11097:   "mesa": "Una mesa larga permite extender mapas, cuentas y documentos durante reuniones.",
11098:   "bancos": "Asientos desiguales han sido reparados muchas veces y acomodan grupos de tamaño variable.",
11099:   "registros": "Cuadernos y tablillas guardan cuentas, acuerdos y trabajos comunales.",
11100:   "mapa_local": "Un esquema sencillo muestra campos, canales, caminos y límites conocidos por la comunidad."
11101: },
11102:     "exits": {
11103:       "oeste": "sauces_plaza",
11104:       "sur": "sauces_calle_este"
11105:     },
11106:     "items": [],
11107:     "mobs": [],
11108:     "npcs": []
11109:   },
```

## ROOM `sauces_casa_huespedes` · líneas 11049-11071

```js
11049:   "sauces_casa_huespedes": {
11050:     "id": "sauces_casa_huespedes",
11051:     "area": "sauces",
11052:     "name": "Casa de Huéspedes",
11053:     "desc": "Una casa amplia mantiene varias habitaciones sencillas para comerciantes, patrulleros, emisarios y viajeros autorizados. El mobiliario es modesto pero cuidado, y la hospitalidad depende de la comunidad, no de la administración de la secta. Los huéspedes ocupan un espacio temporal dentro de una vida local que continúa alrededor de ellos.",
11054:     "scenery": {
11055:   "habitaciones": "Cuartos pequeños con cama, arcón y una mesa suficiente para una estancia breve.",
11056:   "registro": "Un cuaderno sencillo permite anotar quién se hospeda y quién responde por su visita.",
11057:   "cocina": "Un fogón común y estantes básicos permiten preparar comida sin depender de otra casa.",
11058:   "patio": "Un espacio trasero ofrece agua, tendederos y lugar para dejar equipo de viaje."
11059: },
11060:     "exits": {
11061:       "sur": "sauces_plaza",
11062:       "oeste": "sauces_calle_oeste"
11063:     },
11064:     "items": [],
11065:     "mobs": [],
11066:     "npcs": [],
11067:     "alojamiento": {
11068:       "nombre": "sauces_casa_huespedes",
11069:       "inicio": "Te preparan una habitación sencilla en la Casa de Huéspedes. No pertenece a la secta: es hospitalidad de Sauces, suficiente para descansar y recuperarte antes de volver al camino."
11070:     }
11071:   },
```

