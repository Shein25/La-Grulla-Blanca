# Extracto 03 — Creación/raíces/estado inicial

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## RAICES y ORIGENES

Fuente: `grulla-blanca_ver74.html` · líneas 4648-4695

```js
04648:     }
04649:   }
04650:   return fallos;
04651: }
04652: 
04653: const RAICES = {
04654:   fuego: { nombre: "yang de fuego", qi_med: 5, hp_med: 2, ataque: 1, defensa: 0, tecnica: "palma",
04655:            texto: "La piedra se enciende bajo tu mano. Un rojo profundo corre por su superficie y el calor de una fragua te alcanza.\n«Raíz de fuego — yang impaciente. El qi te arde rápido.»" },
04656:   metal: { nombre: "metal afilado", qi_med: 3, hp_med: 3, ataque: 2, defensa: 0, tecnica: "filo",
04657:            texto: "La piedra canta y un filo de luz blanca cruza su superficie. El sonido es limpio y corto.\n«Raíz de metal — cortante. Golpearás como un cincel.»" },
04658:   agua:  { nombre: "yin de agua", qi_med: 4, hp_med: 6, ataque: 0, defensa: 2, tecnica: "latigo",
04659:            texto: "La piedra ondula bajo tu palma y toma un azul sereno. Las ondas se extienden por la superficie y vuelven a quedarse quietas.\n«Raíz de agua — yin fluido. Difícil de herir, fácil de sanar.»" },
04660: };
04661: 
04662: const ORIGENES = {
04663:   campesino: {
04664:     nombre: "hijo de campesinos",
04665:     texto: "El recaudador se llevó la mitad de la cosecha el año pasado y la otra mitad este. Tu madre vació el costurero para pagarte el camino y te entregó sus remedios, guardados y embotellados hasta el último momento. Al despedirse, apretó tus manos: «Si la montaña no te quiere, vuelve. Y si te quiere, vuelve igual, que te seguiré necesitando».",
04666:   },
04667:   escolar: {
04668:     nombre: "escolar sin plaza",
04669:     texto: "Tres exámenes imperiales. Tres veces un apellido con padrinos ocupó tu lugar. Vendiste los clásicos para pagar la deuda, salvo un manual de respiración interior de un ermitaño excéntrico que ningún librero quiso. Lo releíste a oscuras tantas noches que algunas líneas dejaron de ser tinta y empezaron a tener sentido.",
04670:   },
04671:   callejero: {
04672:     nombre: "callejero del mercado sur",
04673:     texto: "En el mercado sur de Anling aprendiste a contar dinero ajeno antes que el tuyo. Dormías con un cuchillo bajo la mejilla. El incendio del gremio se llevó el callejón, así que rebuscaste entre las ruinas y saliste con lo que cupo en dos manos.",
04674:   },
04675: };
04676: 
04677: // 3C.5: datos estáticos REV3; ninguna cadencia o narrativa se deriva de esta tabla.
04678: const NPC_DEF = {
04679:   "ji_xueying": {
04680:     "id": "ji_xueying",
04681:     "nombre": "Ji Xueying",
04682:     "categoria": "autoridad",
04683:     "rol": "Maestra de Secta",
04684:     "sala_inicial": "interior_sala_consejo",
04685:     "sala_inicial_clasificacion": "ELECCION_TECNICA_3C5",
04686:     "movilidad": "ANCLADO",
04687:     "territorio_normal": [
04688:       "interior_sala_consejo"
04689:     ],
04690:     "transito_tecnico": [],
04691:     "posicion_valida": [
04692:       "interior_sala_consejo"
04693:     ],
04694:     "rutas": [],
04695:     "gates_en_ruta": [],
```

## nuevaPartida / creación de personaje

Fuente: `grulla-blanca_ver74.html` · líneas 15820-16010

```js
15820:     if(vieja.estado!=="VACÍO")this.salida(MENSAJE_SAVE_INCOMPATIBLE,"sistema");
15821:     if(slots.some(s=>s.estado!=="VACÍO"&&s.estado!=="VÁLIDO"))this.salida("Hay slots incompatibles o corruptos. Se conservan sin cambios; sólo pueden cargarse los VÁLIDOS.","sistema");
15822:     if(slots.some(s=>s.estado==="VÁLIDO"))this.preguntar("Hay partidas válidas. ¿(c)argar o (n)ueva?",r=>{if(r.trim().toLowerCase().startsWith("c"))this.menuCargar();else this.nuevaPartida();},"(c/n)");
15823:     else { if(slots.some(s=>s.estado!=="VACÍO"))this.salida("Inicia una Nueva Partida.");this.nuevaPartida(); }
15824:   }
15825: 
15826:   nuevaPartida() {
15827:     this.atlas = { salas: {}, personas: {}, criaturas: {} };
15828:     this.rooms = JSON.parse(JSON.stringify(ROOMS));
15829:     this.flags = {}; this.quests = {}; this.gates = crearEstadoGates();
15830:     this.combate = null; this.vivos = []; this.cadaveres = {}; this.objetosTirados = {}; this.terminado = false;
15831:     this.visitadas = new Set();
15832:     this.saturacion = {};
15833:     this.turnoGlobal = 0;
15834:     this.relojEcologico = 0;
15835:     this.respawnEn = {};
15836:     this.interrupcionEn = {};
15837:     this.errantes = JSON.parse(JSON.stringify(ERRANTES_INICIALES));
15838:     this.posicionNPC = crearPosicionNPC();
15839:     this.conocimientoNPC = crearConocimientoNPC();
15840:     this.misionesNuevas = new Set();
15841:     this.misionAbierta = null;
15842:     this.categoriasMisionesAbiertas = new Set(["activas", "rumores"]);
15843:     this.actualizarBotonMisiones();
15844: 
15845:     const div = document.createElement("div");
15846:     div.className = "intro";
15847:     div.innerHTML = `
15848:       <div class="intro-kanji">${INTRO.kanji}</div>
15849:       <div class="intro-titulo">${INTRO.titulo}</div>
15850:       <div class="intro-sub">${INTRO.sub}</div>
15851:       <div class="intro-texto">${INTRO.texto.replace(/\n/g, "<br>")}</div>`;
15852:     this.contenido.appendChild(div);
15853:     this.abajo();
15854: 
15855:     this.pedirNombrePersonaje();
15856:   }
15857: 
15858:   pedirNombrePersonaje() {
15859:     this.preguntar("Tu nombre:", (r) => {
15860:       const error = errorNombrePersonaje(r);
15861:       if (error) {
15862:         this.salida(error, "error");
15863:         this.pedirNombrePersonaje();
15864:         return;
15865:       }
15866:       const nombre = String(r ?? "").replace(/\s+/g, " ").trim();
15867:       this.creacionOrigen(nombre);
15868:     });
15869:   }
15870: 
15871:   creacionOrigen(nombre) {
15872:     this.preguntarEleccionMultiple({
15873:       contexto: ["\nAntes de la piedra, el examinador te mira por primera vez:"],
15874:       pregunta: "«Los nombres aquí no me dicen nada. Dime de dónde vienes.»",
15875:       opciones: [
15876:         { valor: "1", insignia: "1)", texto: "«De la tierra. Del arrozal que ya no nos pertenece.»" },
15877:         { valor: "2", insignia: "2)", texto: "«De la academia. Del examen que no me quiso.»" },
15878:         { valor: "3", insignia: "3)", texto: "«De la calle. Del mercado sur de Anling.»" },
15879:       ],
15880:       marcador: "(1/2/3)",
15881:       hint: "1, 2 o 3",
15882:       callback: (r) => {
15883:         const origen = { "1": "campesino", "2": "escolar", "3": "callejero" }[r.trim()] || "campesino";
15884:         this.salida("\n" + ORIGENES[origen].texto, "destacado");
15885:         this.creacionRaiz(nombre, origen);
15886:       }
15887:     });
15888:   }
15889: 
15890:   creacionRaiz(nombre, origen) {
15891:     this.preguntarEleccionMultiple({
15892:       contexto: ["\nEl examinador tiende la PIEDRA DE LAS RAÍCES, gris como un huevo de paloma."],
15893:       pregunta: "¿Cómo respondes al primer contacto con la piedra?",
15894:       opciones: [
15895:         { valor: "1", insignia: "1)", texto: "Apoyas la palma entera, sin miedo." },
15896:         { valor: "2", insignia: "2)", texto: "Rozas la piedra con la yema de un solo dedo." },
15897:         { valor: "3", insignia: "3)", texto: "Esperas, y dejas que la piedra te lea a ti." },
15898:       ],
15899:       marcador: "(1/2/3)",
15900:       hint: "1, 2 o 3",
15901:       callback: (r) => {
15902:         const raiz = { "1": "fuego", "2": "metal", "3": "agua" }[r.trim()] || "agua";
15903:         this.crearPersonaje(nombre, raiz, origen);
15904:       }
15905:     });
15906:   }
15907: 
15908:   crearPersonaje(nombre, raiz, origen) {
15909:     const r = RAICES[raiz], o = ORIGENES[origen];
15910:     this.salida("\n" + r.texto, "destacado");
15911:     const p = {
15912:       name: nombre, es_jugador: true, mob_id: "", unico: false,
15913:       hp: 16, max_hp: 16, ataque: 1 + r.ataque, defensa: 10 + r.defensa, esquiva: ESQUIVA_INNATA, daño: "1d3",
15914:       qi_recompensa: 0, loot: [],
15915:       raiz, raiz_secundaria: null, reino: "LianQi", etapa: 1, qi: 0, qi_max: VASO_ETAPA[1],
15916:       comprension: 0, piedras: 0, impurezas: 0, origen, metodo: null,
15917:       contribucion: 0, prestigio: 0, titulo: "aspirante aceptado", calidad_fundacion: null,
15918:       // --- cultivo (ver CONTRATO UI · CULTIVO) ---
15919:       // granPerfeccionLianQi es un HITO IRREVERSIBLE, no un valor derivado: se
15920:       // fija una vez al consagrar formalmente la Gran Perfección y no se vuelve
15921:       // a evaluar. Si se calculara como qi === qi_max, gastar qi en una técnica
15922:       // "revertiría" narrativamente un hito que ya ocurrió.
15923:       granPerfeccionLianQi: false,
15924:       iluminacion: { alcanzada: false, semillaCorazonDao: null },
15925:       tribulacionCorazon: { superada: false, pendienteReintento: false },
15926:       // Ambos historiales guardan SOLO lo ya cerrado, nunca el presente: el
15927:       // arco/reino actual se calcula siempre con arcoActual(p) y p.reino/p.etapa.
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
15949:       afinidad: {},
15950:       // PROVISIONAL_3C1 · REVISAR_EN_PROLOGO_M01: uniforme y espada para usar el estado intermedio.
15951:       inventario: ["pocion", "uniforme", "espada_madera"],
15952:       equipado: {},
15953:       tecnicas: {}, puntos_tecnica_total: 1, meridianos_version: 3, equipo_version: 2,
15954:       // Configuración de combate y presets. Ver CONTRATO DE DISEÑO · BUILDS Y COMBATE.
15955:       // La técnica concedida por la raíz empieza preparada, pero SIN invertir
15956:       // puntos ni elegir ramas: preparar es loadout, no especialización.
15957:       tecnicas_preparadas: [r.tecnica], builds: [], build_activa: null, build_seq: 0, builds_version: 2,
15958:     };
15959:     p.tecnicas[r.tecnica] = { maestria: 0, usos: 0, practica: 0, ramas: { 1: 0, 2: 0, 3: 0 } };
15960:     const perk = [];
15961:     if (origen === "campesino") {
15962:       p.max_hp += 2; p.hp = p.max_hp;
15963:       p.inventario.push("pocion", "pocion");
15964:       perk.push("Manos de campo: +2 de vida máxima. Las pociones de tu madre viajan contigo.");
15965:     } else if (origen === "escolar") {
15966:       p.comprension = 2;
15967:       perk.push("Tres exámenes fracasados enseñan a leer el mundo: empiezas con comprensión 2.");
15968:     } else if (origen === "callejero") {
15969:       p.inventario.push("cuchillo_hueso");
15970:       p.piedras = 4;
15971:       perk.push("El cuchillo de hueso de Anling sigue contigo; podrás elegirlo en lugar de la espada de práctica. Piedras rescatadas de la ruina: +4.");
15972:     }
15973:     this.player = p;
15974:     this.gates = crearEstadoGates();
15975:     this.pos = "patio_raices";
15976:     // El examen termina antes de la puerta: el tutorial exterior empieza físicamente aquí.
15977:     this.visitadas.add(this.pos);
15978:     this.recordarAtlas();
15979:     this.salida(`\n«${nombre}, ${o.nombre}, raíz de ${r.nombre}.» El examinador anota el resultado en una tablilla provisional.`);
15980:     if (perk.length) this.salida(perk.join("\n"), "destacado");
15981:     this.salida("[Fundación estructural 3C.1. Campaña y NPC pendientes. Equipo inicial disponible en INVENTARIO.]");
15982:     this.entrarSala();
15983:     this.actualizarBarra();
15984:   }
15985: 
15986:   // ---------- historial de acciones narrativas ----------
15987: 
15988:   tipoAccionCanonico(tipo) {
15989:     return String(tipo ?? "").trim().toUpperCase().replace(/[\s-]+/g, "_");
15990:   }
15991: 
15992:   datosNarrativosPlanos(valor, defecto = {}) {
15993:     if (!valor || typeof valor !== "object" || Array.isArray(valor)) return { ...defecto };
15994:     try { return JSON.parse(JSON.stringify(valor)); }
15995:     catch { return { ...defecto }; }
15996:   }
15997: 
15998:   normalizarHistorialAcciones() {
15999:     const p = this.player;
16000:     if (!p) return null;
16001:     if (!p.historialAcciones || typeof p.historialAcciones !== "object" || Array.isArray(p.historialAcciones)) {
16002:       p.historialAcciones = { version: HISTORIAL_ACCIONES_VERSION, secuencia: 0, eventos: [] };
16003:     }
16004:     const h = p.historialAcciones;
16005:     if (!Array.isArray(h.eventos)) h.eventos = [];
16006:     if (!Number.isFinite(h.secuencia) || h.secuencia < 0) h.secuencia = 0;
16007: 
16008:     const limpios = [];
16009:     const claves = new Set();
16010:     for (const bruto of h.eventos) {
```

