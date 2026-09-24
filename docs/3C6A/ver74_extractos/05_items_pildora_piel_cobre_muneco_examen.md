# Extracto 05 — Ítems/Píldora/Piel de Cobre/Muñeco/Examen

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## Píldora de consolidación y manual Piel de Cobre

Fuente: `grulla-blanca_ver74.html` · líneas 6838-6875

```js
06838:   },
06839: pocion: {
06840:     name: "poción de sangre", tipo: "consumible", cura: "3d6+6", precio: 5,
06841:     desc: "Un vial de rojo apagado que sabe a hierro y a ciruela. Cura deprisa, pero el qi barato deja un sedimento que el cuerpo no agradece. (impureza +1)"
06842:   },
06843: pildora_consolidacion: {
06844:     name: "píldora de consolidación", tipo: "reliquia", precio: 8,
06845:     desc: "Una pastilla oscura, sin brillo, del tamaño de una uña. No cura, no da qi: prepara al cuerpo para sostener más. Los externos la llaman «llave de alquiler».\n(Se consume al CONSAGRAR una etapa con el qi al tope.)"
06846:   },
06847: hierba_claridad: {
06848:     name: "hoja de claridad", tipo: "material",
06849:     desc: "Plateada y fría, zumba junto al oído sin descanso. Los escribas las mastican cuando llevan demasiado tiempo mirando letras."
06850:   },
06851: pildora_fundacion: {
06852:     name: "Píldora de Fundación", tipo: "reliquia",
06853:     desc: "Una esfera ámbar con una luz que gira dentro. Huele a trueno y a invierno, y pesa en la mano mucho más de lo que parece.\n(Se consume meditando con el qi al tope del tope.)"
06854:   },
06855: manual_sello: {
06856:     name: "manual del Sello de la Montaña", tipo: "manual", tecnica: "sello",
06857:     desc: "El pergamino es más viejo que la secta y la escritura está apretada hasta el borde. Enseña a oprimir el qi como oprime una montaña; no encaja con nada de lo que la secta enseña a sus externos.\n(Grado TIERRA: exige qi de reino ZhuJi. ÚSALO para aprender.)"
06858:   },
06859: manual_paso: {
06860:     name: "manual del Paso de Nube Ligera", tipo: "manual", tecnica: "paso_nube", precio: 12,
06861:     desc: "Diagramas de pies descalzos sobre nubes pintadas explican dónde poner cada paso. Enseña a dejar que el viento te preste su sitio sin hacer demasiadas preguntas.\n(ÚSALO para aprender.)"
06862:   },
06863: manual_piel: {
06864:     name: "manual de Piel de Cobre", tipo: "manual", tecnica: "piel_cobre", precio: 12,
06865:     desc: "Un tratado de forja aplicada a la carne, con dibujos y notas al margen. Explica cómo conseguir que el golpe que te alcance llegue cansado.\n(ÚSALO para aprender.)"
06866:   },
06867: manual_filamento: {
06868:     name: "manual del Filamento de Agua", tipo: "manual", tecnica: "filamento", precio: 16,
06869:     desc: "El hilo de qi aparece tensado en los dibujos como una cuerda de laúd. Enseña a enredar al enemigo y, con raíz de agua, hacerlo sin gastar de más.\n(ÚSALO para aprender.)"
06870:   },
06871: bolsa_piedras: {
06872:     name: "bolsa lacrada de piedras espirituales", tipo: "tesoro", piedras: 12,
06873:     desc: "Seda lacrada con doce piedras dentro: el salario de alguien que ya no lo necesita."
06874:   },
06875: manual_espejo: {
```

## TECNICAS.piel_cobre

Fuente: `grulla-blanca_ver74.html` · líneas 4088-4125

```js
04088:   },
04089:   lanza_nube: {
04090:     name: "Lanza que Parte Nubes", corto: "Lanza", rango: "tierra", elemento: "viento", tipo: "ofensiva",
04091:     coste: 10, daño: "3d8+3", req: { reino: "ZhuJi" },
04092:     flavor: ["Tu qi dibuja una línea recta hacia el cielo.", "La línea separa el aire en dos silencios.",
04093:              "Una nube se parte antes de que la toques.", "El mundo recuerda que también puede ser atravesado."],
04094:   },
04095:   paso_nube: {
04096:     name: "Paso de Nube Ligera", corto: "Paso", rango: "mortal", elemento: "viento", tipo: "esquiva",
04097:     coste: 5, esquiva: 15, duracion: 2,
04098:     flavor: ["Tus pies apenas rozan la arena.", "Un paso, y ya estás en otro sitio.",
04099:              "El viento te presta su sitio.", "Ya no caminas: te colocas."],
04100:   },
04101:   piel_cobre: {
04102:     name: "Piel de Cobre", corto: "Piel", rango: "mortal", elemento: "tierra", tipo: "guardia",
04103:     coste: 5, guardia: 3, duracion: 2,
04104:     flavor: ["Tu piel tira a bronce.", "El golpe que llegue, llegará cansado.",
04105:              "Tu piel es yunque.", "El cobre recuerda al hierro."],
04106:   },
04107:   filamento: {
04108:     name: "Filamento de Agua", corto: "Filamento", rango: "mortal", elemento: "agua", tipo: "control",
04109:     coste: 6, atadura: 1,
04110:     flavor: ["Un hilo de qi tensa el aire.", "El hilo aprieta antes de que lo vean.",
04111:              "El agua se enreda como liana.", "Tu hilo es la corriente del río."],
04112:   },
04113:   circulo_ascuas: {
04114:     name: "Círculo de las Cien Ascuas", corto: "Ascuas AOE", rango: "tierra", elemento: "fuego", tipo: "ofensiva",
04115:     coste: 15, daño: "2d6+3", area: true, req: { reino: "ZhuJi" },
04116:     flavor: ["Trazas un círculo y las ascuas buscan toda respiración hostil.",
04117:              "El círculo se cierra como una flor encendida.",
04118:              "Cada enemigo proyecta una sombra roja antes de arder.",
04119:              "Cien ascuas responden a una sola apertura de tu palma."],
04120:   },
04121:   lluvia_filos: {
04122:     name: "Lluvia de los Mil Filos", corto: "Filos AOE", rango: "tierra", elemento: "metal", tipo: "ofensiva",
04123:     coste: 13, daño: "2d6+2", area: true, req: { reino: "ZhuJi" },
04124:     flavor: ["Fragmentas tu qi en filos que caen sobre todo el campo.",
04125:              "Los filos encuentran huecos entre cuerpos y respiraciones.",
```

## otra definición/uso Piel de Cobre

Fuente: `grulla-blanca_ver74.html` · líneas 4228-4255

```js
04228:   },
04229:   lanza_nube: {
04230:     proposito: "Ataque de viento de gran daño contra un solo objetivo, con evoluciones orientadas a precisión y crítico.",
04231:     uso: "Conviene para derribar rápidamente al enemigo más peligroso de un grupo.",
04232:     limite: "No alcanza a los demás hostiles y exige una reserva de qi considerable.",
04233:   },
04234:   paso_nube: {
04235:     proposito: "Técnica de movilidad que aumenta tu defensa durante varias rondas en lugar de absorber daño.",
04236:     uso: "Conviene contra rivales precisos: hace que sus ataques fallen por completo mientras preparas otra acción.",
04237:     limite: "No reduce un golpe que consiga alcanzarte y no causa daño al activarse.",
04238:   },
04239:   piel_cobre: {
04240:     proposito: "Burbuja corporal que resta una cantidad fija al daño de cada golpe recibido hasta agotar su reserva.",
04241:     uso: "Conviene contra grupos o criaturas que atacan repetidamente con golpes pequeños y medianos.",
04242:     limite: "No evita el impacto ni causa daño; se gasta con el daño que absorbe, no con el paso de las rondas, y un ataque muy fuerte todavía atravesará parte de la protección.",
04243:   },
04244:   filamento: {
04245:     proposito: "Arte de control que ata al objetivo y le impide actuar durante una o más rondas.",
04246:     uso: "Conviene para interrumpir al enemigo principal, beber una poción o atacar sin recibir respuesta inmediata.",
04247:     limite: "Debe superar una prueba de control y entra en enfriamiento. Los jefes sólo pierden una acción y después obtienen Tenacidad durante dos rondas.",
04248:   },
04249:   circulo_ascuas: {
04250:     proposito: "Ataque de fuego en área que intenta alcanzar a todos los enemigos y puede quemarlos.",
04251:     uso: "Conviene contra grupos numerosos, especialmente si sobrevivirán varias rondas a la quemadura.",
04252:     limite: "Consume mucho qi y, contra un único enemigo, sólo conserva el 65% del daño que logre causar.",
04253:   },
04254:   lluvia_filos: {
04255:     proposito: "Ataque metálico en área: lanza una tirada separada contra cada enemigo presente.",
```

## configuración Piel de Cobre

Fuente: `grulla-blanca_ver74.html` · líneas 4468-4495

```js
04468:   paso_nube: {
04469:     1: [{ nombre: "Paso prolongado", mod: { duracionExtra: 1 } },
04470:         { nombre: "Paso corto", mod: { esquiva: 22 } },
04471:         { nombre: "Paso sobrio", mod: { coste: -1 } }],
04472:     2: [{ nombre: "Respiración de nube", mod: { coste: -1 } },
04473:         { nombre: "Paso velado", mod: { esquiva: 25 } },
04474:         { nombre: "Aliento sostenido", mod: { duracionExtra: 1 } }],
04475:     3: [{ nombre: "Cuerpo sin peso", mod: { esquiva: 32, duracionExtra: 1, coste: 1 } },
04476:         { nombre: "Viento entre hojas", mod: { duracionExtra: 2 } },
04477:         { nombre: "Ausencia instantánea", mod: { esquiva: 22, coste: -1 } }],
04478:   },
04479:   piel_cobre: {
04480:     1: [{ nombre: "Cobre endurecido", mod: { guardia: 6 } },
04481:         { nombre: "Cobre flexible", mod: { duracionExtra: 1 } },
04482:         { nombre: "Cobre sobrio", mod: { coste: -1 } }],
04483:     2: [{ nombre: "Aliento económico", mod: { coste: -1 } },
04484:         { nombre: "Cobre grueso", mod: { guardia: 7 } },
04485:         { nombre: "Placas continuas", mod: { duracionExtra: 1 } }],
04486:     3: [{ nombre: "Coraza de montaña", mod: { guardia: 9, duracionExtra: 1, coste: 1 } },
04487:         { nombre: "Cobre asentado", mod: { duracionExtra: 2 } },
04488:         { nombre: "Coraza económica", mod: { guardia: 5, coste: -1 } }],
04489:   },
04490:   respiracion_horno: {
04491:     1: [{ nombre: "Horno persistente", mod: { duracionExtra: 1 } },
04492:         { nombre: "Brasa protectora", mod: { guardia: 5 } },
04493:         { nombre: "Horno sobrio", mod: { coste: -1 } }],
04494:     2: [{ nombre: "Aliento de caldera", mod: { coste: -2 } },
04495:         { nombre: "Cerámica dura", mod: { guardia: 6 } },
```

## MOBS.muneco_practica

Fuente: `grulla-blanca_ver74.html` · líneas 7125-7145

```js
07125: 
07126: 
07127: 
07128: 
07129: // ---------- MOBS · catálogo de criaturas y ecología vigente ----------
07130: // Distribución: ROOMS para poblaciones fijas y ERRANTES_INICIALES para fauna móvil.
07131: 
07132: const MOBS = {
07133: muneco_practica: { name: "muñeco articulado de práctica", corto: "muñeco", hp: 14, ataque: 1, defensa: 9, daño: "1d3", qi: 0,
07134:              desc: "Un armazón de madera, cuerda y sacos de arena. Sus brazos vuelven al centro con cada golpe; fue construido para enseñar errores sin tener que enterrarlos.",
07135:              loot: [], practica: true },
07136: rata_qi: { name: "rata de qi", corto: "rata", hp: 9, ataque: 1, defensa: 10, daño: "1d4", qi: 2,
07137:              desc: "Ratas comunes que aprendieron a roer el aire tanto como el grano: sus dientes brillan con un residuo de qi robado a las reservas de la despensa.",
07138:              loot: [{ item: "pocion", prob: 0.2 }] },
07139: serpiente_qi: { name: "serpiente de qi verdosa", corto: "serpiente", hp: 13, ataque: 2, defensa: 11, daño: "1d4+1", qi: 3,
07140:              elemento: "agua",
07141:              desc: "Se enrosca cerca de fuentes de agua espiritual, con escamas del mismo verde que el qi que bebe. Su veneno no mata: entorpece la circulación de quien muerde.",
07142:              tecnica: { name: "Colmillos Venenosos", cada: 3, veneno: { daño: "1d2", turnos: 3, familia: "jade", grado: 1, nombre: "Veneno de Jade I" } },
07143:              loot: [{ item: "pildora_consolidacion", prob: 0.3 }] },
07144: lobo_espiritual: { name: "lobo espiritual de tres colas", corto: "lobo", hp: 18, ataque: 3, defensa: 11, daño: "1d6+1", qi: 5,
07145:              desc: "Caza como si fuera tres animales a la vez: sus tres colas se mueven de forma independiente, cada una vigilando una dirección distinta del bosque.",
```

## HALLAZGOS_CADAVER / rata_qi

Fuente: `grulla-blanca_ver74.html` · líneas 7250-7315

```js
07250:     simple: .75, normal: .60, dificil: .40, muy_dificil: .25,
07251:   });
07252:   const BONO_RANGO_EXAMEN = Object.freeze([0, .05, .10]);
07253:   const BONO_PRIMERA_ESPECIE_EXAMEN = 2;
07254:   const BONO_PRIMER_PROCEDIMIENTO_EXAMEN = 1;
07255: 
07256:   const HALLAZGOS_CADAVER = {
07257:     rata_qi: {
07258:       descripcion: "El pelaje gris sigue erizado, como si el qi robado no hubiera terminado de asentarse.",
07259:       pistas: "El qi robado no está en los dientes: se ha acumulado en una pequeña bolsa grasa junto al estómago.",
07260:       hallazgos: [
07261:         { id: "bolsa_grasa", item: "grasa_qi_roida", cantidad: 1, dificultad: "simple", metodo: "separar bolsa de qi", pista: "El qi robado no está en los dientes: se ha acumulado en una pequeña bolsa grasa junto al estómago." },
07262:       ],
07263:     },
07264:     serpiente_qi: {
07265:       descripcion: "Escamas verdosas con un brillo húmedo que no se seca ni después de muerta.",
07266:       pistas: "La toxina viaja por una glándula verde y por una membrana de canales finísimos que evita que el propio veneno alcance la carne.",
07267:       hallazgos: [
07268:         { id: "glandula_jade", item: "aguijon_jade", cantidad: 1, dificultad: "normal", metodo: "extraer glándula de jade", pista: "La toxina viaja por una glándula verde antes de llegar al colmillo." },
07269:         { id: "membrana_meridiana", item: "membrana_serpentina", cantidad: 1, dificultad: "dificil", metodo: "separar membrana meridiana", pista: "Una membrana de canales finísimos evita que el propio veneno alcance la carne de la serpiente." },
07270:       ],
07271:     },
07272:     lobo_espiritual: {
07273:       descripcion: "Tres colas rígidas, erizadas como si el viento aún soplara sobre ellas.",
07274:       pistas: "Las tres colas comparten tensión por una red de tendones; la médula cercana conserva una corriente de viento incluso después de la muerte.",
07275:       hallazgos: [
07276:         { id: "medula_viento", item: "medula_viento", cantidad: 1, dificultad: "normal", metodo: "extraer médula de viento", pista: "La médula cercana a la cola conserva una corriente de viento incluso después de la muerte." },
07277:         { id: "tendon_colas", item: "tendon_tres_colas", cantidad: 1, dificultad: "dificil", metodo: "separar tendón de las tres colas", pista: "Las tres colas comparten tensión gracias a una red de tendones." },
07278:       ],
07279:     },
07280:     avispa_jade: {
07281:       descripcion: "El caparazón verde jade conserva el filo intacto de sus mandíbulas.",
07282:       pistas: "El aguijón está conectado a una cámara abdominal que regula la toxina antes de cada picadura.",
07283:       hallazgos: [
07284:         { id: "aguijon", item: "aguijon_jade", cantidad: 1, dificultad: "normal", metodo: "retirar aguijón de jade", pista: "El aguijón está conectado a una cámara abdominal que regula la toxina antes de cada picadura." },
07285:         { id: "camara", item: "camara_jade", cantidad: 1, dificultad: "dificil", metodo: "abrir cámara de jade", pista: "La cámara abdominal regula la toxina que alimenta al aguijón." },
07286:       ],
07287:     },
07288:     mono_pildoras: {
07289:       descripcion: "Las mejillas siguen hinchadas, con restos de píldoras ajenas a medio tragar.",
07290:       pistas: "Años de tragar medicinas ajenas endurecieron una vesícula cerca del hígado; los residuos siguen separados en capas.",
07291:       hallazgos: [
07292:         { id: "vesicula", item: "vesicula_medicinal", cantidad: 1, dificultad: "normal", metodo: "aislar vesícula medicinal", pista: "Años de tragar medicinas ajenas endurecieron una vesícula cerca del hígado." },
07293:       ],
07294:     },
07295:     sapo_ceniza: {
07296:       descripcion: "La piel gris todavía humea, como si no hubiera terminado de enfriarse.",
07297:       pistas: "Dos estructuras sobreviven al calor: una glándula oscura que acumula temperatura y un saco respiratorio saturado de hollín.",
07298:       hallazgos: [
07299:         { id: "glandula_termica", item: "glandula_termica", cantidad: 1, dificultad: "normal", metodo: "extraer glándula térmica", pista: "Una glándula oscura acumula temperatura y sobrevive al calor mucho después de la muerte." },
07300:         { id: "saco_hollin", item: "saco_hollin", cantidad: 1, dificultad: "dificil", metodo: "separar saco de hollín", pista: "Un saco respiratorio saturado de hollín sigue formando remolinos diminutos." },
07301:       ],
07302:     },
07303:     escarabajo_hierro: {
07304:       descripcion: "Un caparazón oscuro y metálico que suena a piedra al golpearlo.",
07305:       pistas: "Bajo la coraza rígida hay una placa aprovechable y, todavía más adentro, una membrana flexible que distribuye la tensión de cada impacto.",
07306:       hallazgos: [
07307:         { id: "placa", item: "caparazon_hierro", cantidad: 1, dificultad: "normal", metodo: "desprender placa férrea", pista: "Bajo la coraza rígida hay una placa aprovechable." },
07308:         { id: "membrana", item: "membrana_ferrea", cantidad: 1, dificultad: "dificil", metodo: "separar membrana férrea", pista: "Todavía más adentro hay una membrana flexible que distribuye la tensión de cada impacto." },
07309:       ],
07310:     },
07311:     pez_lunar: {
07312:       descripcion: "Escamas pálidas y translúcidas, sin rastro alguno de ojos.",
07313:       pistas: "La cavidad branquial guarda un fluido pálido; sus filamentos separan agua y sedimento espiritual sin mezclarlos.",
07314:       hallazgos: [
07315:         { id: "fluido", item: "fluido_lunar", cantidad: 1, dificultad: "normal", metodo: "recoger fluido lunar", pista: "La cavidad branquial guarda un fluido pálido." },
```

## profesiones iniciales

Fuente: `grulla-blanca_ver74.html` · líneas 15928-15948

```js
15928:       historialReinos: [],
15929:       historialArcos: [],
15930:       cultivo_version: 1,
15931:       // Biografía narrativa canónica. No contiene moralidad ni afinidad de Dao.
15932:       historialAcciones: { version: HISTORIAL_ACCIONES_VERSION, secuencia: 0, eventos: [] },
15933:       alquimia: 0, fallos_alquimia: 0, heridas_meridianos: 0,
15934:       aflicciones: [],
15935:       profesiones: {
15936:         examen: { xp: 0, rango: 0, materiales: {}, total: 0, cadaveres: 0, hallazgos: {}, descubrimientos: {}, procedimientos: {}, desbloqueada: false },
15937:         // PROVISIONAL_3C1 · REVISAR_EN_PROLOGO_M01: acceso práctico, sin concesión narrativa.
15938:         herboristeria: { xp: 0, rango: 0, materiales: {}, total: 0, especies: {}, procedimientos: {}, nodos: {}, desbloqueada: true },
15939:         alquimia: { xp: 0, rango: 0, elaboraciones: 0, calidades: {}, recetas: {}, desbloqueada: false },
15940:         forja: { xp: 0, rango: 0, desbloqueada: false }, inscripcion: { xp: 0, rango: 0, desbloqueada: false },
15941:       },
15942:       profesiones_version: 6,
15943:       facciones: {
15944:         grulla_blanca: { estado: "miembro", saldo: 0, merito: 0, reputacion: 0, gastos: 0, historial: [] },
15945:       },
15946:       faccion_principal: "grulla_blanca",
15947:       facciones_version: 1,
15948:       actividad_reposo: ACCIONES_DORMIR,
```

## desbloquearProfesion

```js
19074:   desbloquearProfesion(id) {
25177:     j.desbloquearProfesion("examen");
25325:   j.desbloquearProfesion("examen"); j.cadaveres[j.pos]=[cuerpo];
26727:   j.desbloquearProfesion("examen");
26805:   j.desbloquearProfesion("examen");
26819:   j.desbloquearProfesion("examen");
26836:   j.desbloquearProfesion("examen");
26859:   j.desbloquearProfesion("examen");
26882:   j.desbloquearProfesion("examen");
26899:   j.desbloquearProfesion("examen");
26935:   j.desbloquearProfesion("herboristeria");
26951:   j.desbloquearProfesion("herboristeria");
26970:   j.desbloquearProfesion("herboristeria");
26989:   j.desbloquearProfesion("herboristeria");
27006:   j.desbloquearProfesion("herboristeria");
27015:   j.desbloquearProfesion("herboristeria");
27027:   j.desbloquearProfesion("herboristeria");
27995:   j.desbloquearProfesion("examen");
28034:   j.desbloquearProfesion("examen");
28057:   j.desbloquearProfesion("examen");
28074:   j.desbloquearProfesion("examen");
28092:   j.desbloquearProfesion("herboristeria");
28116:   j.desbloquearProfesion("examen"); j.desbloquearProfesion("herboristeria");
```

## Referencias pildora_consolidacion

```js
06784: //   reliquias                  pildora_consolidacion, pildora_fundacion,
06843: pildora_consolidacion: {
07143:              loot: [{ item: "pildora_consolidacion", prob: 0.3 }] },
07170:              loot: [{ item: "pocion", prob: 0.45 }, { item: "polvo_nube", prob: 0.5 }, { item: "pildora_consolidacion", prob: 0.25 }] },
07179:              loot: [{ item: "pildora_consolidacion", prob: 0.35 }, { item: "pocion", prob: 0.25 }] },
07194:              loot: [{ item: "pildora_consolidacion", prob: 0.2 }] },
14508:       consolidacion: { nombre: "Píldora de consolidación", coste: 8, merito: 20, item: "pildora_consolidacion",
17139:     const tiene = this.player.inventario.filter(x => x === "pildora_consolidacion").length;
20123:             const idx = p.inventario.indexOf("pildora_consolidacion");
21744:           const nPild = p.inventario.filter(x => x === "pildora_consolidacion").length;
```

