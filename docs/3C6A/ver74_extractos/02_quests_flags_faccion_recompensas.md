# Extracto 02 — QUESTS/flags/facción/recompensas

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## QUESTS y contrato de misiones

Fuente: `grulla-blanca_ver74.html` · líneas 14155-14220

```js
14155:     },
14156:     "items": [],
14157:     "mobs": [],
14158:     "npcs": []
14159:   }
14160: };
14161: 
14162: // ----------------------------------------------------------------------------
14163: // Cómo escribir una misión nueva (leer antes de agregar una a QUESTS)
14164: // ----------------------------------------------------------------------------
14165: // Cada misión necesita estos campos de texto, y ninguno debería quedar en una
14166: // sola frase mecánica. auditarMisiones() (sección 7) revisa esto al arrancar
14167: // y avisa por consola si algo queda corto o incompleto.
14168: //
14169: //   nombre           Título corto, el que ve el jugador en los menús.
14170: //   desc             UNA línea mecánica y objetiva ("mata 3 ratas en la
14171: //                     despensa"). Es el resumen de agenda/atlas, no la
14172: //                     presentación: puede ser seco a propósito.
14173: //   lore             El texto largo que se muestra en el panel de MISIONES.
14174: //                     Mínimo 3 oraciones. Tiene que explicar (a) por qué
14175: //                     existe el encargo, (b) qué está en juego para el NPC
14176: //                     o el lugar, y (c) algo específico de este mundo (un
14177: //                     nombre, un objeto, un detalle) — no una descripción
14178: //                     genérica que serviría para cualquier misión de "matar
14179: //                     bichos". Si lore describe solo la mecánica, reescribir.
14180: //   objetivo          Instrucción concreta en segunda persona ("Derrota...
14181: //                     y regresa con...").
14182: //   frase             LA LÍNEA QUE DICE EL NPC AL RECIBIR LA ENTREGA. Es
14183: //                     obligatoria si `entrega` apunta a un NPC. Empieza con
14184: //                     "—" para que se renderice como diálogo. Tiene que
14185: //                     reaccionar a ESTA entrega puntual (qué trajiste, qué
14186: //                     significa para él), no ser un genérico "gracias por
14187: //                     tu ayuda". Usar la voz propia del NPC (ver DESCS_NPC
14188: 
14189: //                     referencia de tono). Si `entrega` es una función que
14190: //                     varía según el jugador (como en origen_personal),
14191: //                     `frase` también debe serlo.
14192: //   recompensaTexto   Lo que el jugador puede anticipar antes de completar.
14193: //
14194: // completarMision() intercala `frase` justo antes de las líneas de
14195: // recompensa, así que no hace falta repetir "misión completada" dentro de
14196: // la frase — eso ya lo agrega el motor.
14197: // ----------------------------------------------------------------------------
14198: 
14199: // ---------- QUESTS · pendiente de progresión canónica P–M18 ----------
14200: const QUESTS = {};
14201: 
14202: 
14203: 
14204: const CATALOGO = [];
14205: 
14206: const RECETAS = {
14207:   sangre: {
14208:     categoria: "vitalidad",
14209:     nombre: "poción de sangre refinada", dificultad: "sencilla",
14210:     ingredientes: { raiz_sangre: 1, hierba_claridad: 1 }, resultado: "pocion_refinada", patron: [2, 2, 2],
14211:     pista: "La raíz libera su esencia con rapidez si la llama sube demasiado. La claridad debe acompañar el flujo antes de que el rojo se oscurezca.",
14212:     desbloqueo: { tipo: "inicial" },
14213:   },
14214:   antidoto: {
14215:     categoria: "purificacion",
14216:     nombre: "antídoto de jade menor", dificultad: "normal",
14217:     ingredientes: { aguijon_jade: 1, fibra_jade: 1, hierba_claridad: 1 }, resultado: "antidoto_jade", patron: [1, 2, 2],
14218:     pista: "La toxina no debe despertar por completo. La fibra sostiene la mezcla mientras la claridad separa veneno de medicina.",
14219:     desbloqueo: { tipo: "material", item: "aguijon_jade" },
14220:   },
```

## Facciones, rangos y servicios

Fuente: `grulla-blanca_ver74.html` · líneas 14485-14535

```js
14485: //     · Correr DIAGNOSTICO/GB.PRUEBAS.correr() y las pruebas `balance v8`.
14486: // ============================================================================
14487: 
14488: const TIPOS_AFLICCION_PERSISTENTE = new Set(["veneno", "quemadura"]);
14489: 
14490: // Cada organización conserva su propio libro mayor. El saldo se gasta; el mérito
14491: // histórico nunca disminuye y sirve para rangos, permisos y promociones.
14492: const FACCION_PRINCIPAL = "grulla_blanca";
14493: const FACCIONES = {
14494:   grulla_blanca: {
14495:     nombre: "Secta de la Grulla Blanca",
14496:     tipo: "secta ortodoxa",
14497:     rangos: [
14498:       { id: "aspirante", nombre: "Aspirante sin tablilla", merito: 0 },
14499:       { id: "servidor_externo", nombre: "Servidor externo", merito: 8 },
14500:       { id: "discipulo_acreditado", nombre: "Discípulo acreditado", merito: 20 },
14501:       { id: "merito_interno", nombre: "Mérito del patio interno", merito: 40 },
14502:     ],
14503:     servicios: {
14504:       pocion: { nombre: "Poción de sangre", coste: 3, merito: 0, item: "pocion",
14505:         descripcion: "Una medicina básica retirada del almacén de externos." },
14506:       claridad: { nombre: "Hoja de claridad", coste: 4, merito: 8, item: "hierba_claridad",
14507:         descripcion: "Material de estudio y alquimia reservado a quienes ya cumplieron una tablilla." },
14508:       consolidacion: { nombre: "Píldora de consolidación", coste: 8, merito: 20, item: "pildora_consolidacion",
14509:         descripcion: "Preparación para las puertas de LianQi; exige servicio acreditado." },
14510:     },
14511:   },
14512: };
14513: 
14514: const VARIANTES_ALQUIMIA = {
14515:   sangre: {
14516:     impura: { id: "pocion_refinada_impura", cura: "2d4+2", impureza: 1 }, estable: { id: "pocion_refinada" },
14517:     superior: { id: "pocion_refinada_superior", cura: "4d4+4", impureza: 0 }, excepcional: { id: "pocion_refinada_excepcional", cura: "4d4+6", impureza: 0 },
14518:   },
14519:   antidoto: {
14520:     impura: { id: "antidoto_jade_impuro", cura_afliccion: { tipo:"veneno", familia:"jade", gradoMax:1 }, impureza:1 }, estable:{ id:"antidoto_jade" },
14521:     superior:{ id:"antidoto_jade_superior" }, excepcional:{ id:"antidoto_jade_excepcional" },
14522:   },
14523:   purificacion: {
14524:     impura: { id: "pildora_purificacion_impura", purifica: 1 }, estable: { id: "pildora_purificacion" },
14525:     superior: { id: "pildora_purificacion_superior", purifica: 4 }, excepcional: { id: "pildora_purificacion_excepcional", purifica: 5 },
14526:   },
14527:   elixir: {
14528:     impura: { id: "elixir_qi_impuro", recupera_qi: 12, impureza: 2 }, estable: { id: "elixir_qi" },
14529:     superior: { id: "elixir_qi_superior", recupera_qi: 28, impureza: 0 }, excepcional: { id: "elixir_qi_excepcional", recupera_qi: 36, impureza: 0 },
14530:   },
14531:   ceniza: {
14532:     impura:{ id:"balsamo_ceniza_impuro", cura_afliccion:{tipo:"quemadura",familia:"ceniza",gradoMax:1}, impureza:1 }, estable:{ id:"balsamo_ceniza" },
14533:     superior:{ id:"balsamo_ceniza_superior" }, excepcional:{ id:"balsamo_ceniza_excepcional" },
14534:   },
14535:   meridianos: {
```

## Inicialización de flags/quests

Fuente: `grulla-blanca_ver74.html` · líneas 15768-15838

```js
15768:     this.cbLogEl = document.getElementById("cbLog");
15769:     this.cbDrawerEl = document.getElementById("cbDrawer");
15770:     this.cbAccionesEl = document.getElementById("cbAcciones");
15771:     this.cbResumenPreparadasEl = document.getElementById("cbResumenPreparadas");
15772:     this.cbTituloEl = document.getElementById("cbTitulo");
15773:     this.cbRondaEl = document.getElementById("cbRonda");
15774:     this.cbResultadoEl = document.getElementById("cbResultado");
15775:     this.cbResultadoPanelEl = document.getElementById("cbResultadoPanel");
15776:     this.mapaSalaEl = document.getElementById("mapaSala");
15777:     this.panelInfoEl = document.getElementById("panelInfo");
15778:     this.vitalesEl = document.getElementById("vitales");
15779:     this.rooms = null; this.player = null;
15780:     this.flags = {}; this.quests = {}; this.gates = crearEstadoGates();
15781:     this.pos = "camino"; this.vivos = []; this.cadaveres = {}; this.objetosTirados = {};
15782:     this.combate = null; this.terminado = false; this.pregunta = null;
15783:     this.eleccionActivaEl = null;
15784:     this.visitadas = new Set();
15785:     this.atlas = { salas: {}, personas: {}, criaturas: {} };
15786:     this.atlasCapaVista = null;
15787:     // Estado SÓLO de interfaz (ver68 · Etapa 2B). Ninguno de los dos entra en serializar()
15788:     // ni en deserializar(): el Atlas se reconstruye al abrirse desde la posición física.
15789:     this.atlasAreaVista = null;
15790:     this.atlasAcordeones = { lugares: new Set(), personas: new Set(), bestiario: new Set() };
15791:     this.ofiSeleccion = "examen";
15792:     this.ofiReceta = "sangre";
15793:     this.elaboracion = null;
15794:     this.alquimiaResultado = null;
15795:     this.alquimiaCategoriaAbierta = "vitalidad";
15796:     this.alquimiaRecetasAbiertas = new Set(); // Bitácora: fichas de receta desplegadas (por defecto, todas contraídas)
15797:     this.ofiUltimoResultado = null;
15798:     this.ofiUltimoResultadoHerboristeria = null;
15799:     this.ofiUltimoResultadoExamen = null;
15800:     this.saturacion = {};
15801:     this.turnoGlobal = 0;
15802:     this.relojEcologico = 0;
15803:     this.respawnEn = {};
15804:     this.interrupcionEn = {};
15805:     this.errantes = JSON.parse(JSON.stringify(ERRANTES_INICIALES));
15806:     this.posicionNPC = crearPosicionNPC();
15807:     this.conocimientoNPC = crearConocimientoNPC();
15808:     this._tAviso = null;
15809:     this.misionesNuevas = new Set();
15810:     this.misionAbierta = null;
15811:     this.categoriasMisionesAbiertas = new Set(["activas", "rumores"]);
15812:   }
15813: 
15814:   // ---------- salida ----------
15815: 
15816:   arranque() {
15817:     const claves=[CLAVE_AUTO,...Array.from({length:NSLOTS},(_,i)=>CLAVE_SLOT(i+1))];
15818:     const slots=claves.map(k=>this.leerSlotDetallado(k));
15819:     const vieja=this.leerSlotDetallado(CLAVE_VIEJA);
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
```

## entregarRecompensa

Fuente: `grulla-blanca_ver74.html` · líneas 17180-17208

```js
17180:   registroLogro(tipo) {
17181:     this.flags["logro_" + tipo] = (this.flags["logro_" + tipo] || 0) + 1;
17182:   }
17183: 
17184:   logros() {
17185:     return {
17186:       combate: this.flags["logro_combate"] || 0,
17187:       comprension: this.player ? this.player.comprension : 0,
17188:     };
17189:   }
17190: 
17191:   entregarRecompensa(piedras, qi, comprension, contribucion = 0) {
17192:     const out = [], p = this.player;
17193:     if (piedras) { p.piedras += piedras; out.push(`   +${piedras} piedras espirituales.`); }
17194:     if (qi) { const antes = p.qi; p.qi = Math.min(p.qi + qi, p.qi_max); out.push(`   +${p.qi - antes} qi.`); }
17195:     if (comprension) { p.comprension += comprension; out.push(`   +${comprension} comprensión.`); }
17196:     if (contribucion) {
17197:       const registro = this.otorgarContribucion(contribucion, "Encargo completado");
17198:       if (registro) {
17199:         out.push(`   +${contribucion} contribución de la Grulla Blanca. Disponible ${registro.saldo} · mérito ${registro.merito}.`);
17200:         if (registro.rangoNuevo) out.push(`   ✦ Rango de facción: ${registro.rangoNuevo}.`);
17201:       }
17202:     }
17203:     return out;
17204:   }
17205: 
17206:   ajustarAfinidad(npc, cantidad) {
17207:     const p = this.player;
17208:     if (!p.afinidad) p.afinidad = {};
```

## activar/completar misión y facción/contribución

Fuente: `grulla-blanca_ver74.html` · líneas 18828-19005

```js
18828:   puedeIntentar() {
18829:     return this.player.inventario.includes("pildora_fundacion") || this.player.comprension >= UMBRAL_COMPRENSION_FUNDACION;
18830:   }
18831: 
18832:   claveInicioMision(qid, contador) { return `inicio_mision_${qid}_${contador}`; }
18833: 
18834:   avanceMision(qid, contador) {
18835:     return Math.max(0, (this.flags[contador] || 0) - (this.flags[this.claveInicioMision(qid, contador)] || 0));
18836:   }
18837: 
18838:   activarMision(qid, estado = "activa") {
18839:     const q = QUESTS[qid], anterior = this.quests[qid];
18840:     if (!q || anterior === "hecha" || anterior === "fallida") return false;
18841:     if (estado === "rumor") {
18842:       if (anterior) return false;
18843:       this.quests[qid] = "rumor";
18844:     } else {
18845:       if (anterior === "activa") return false;
18846:       for (const contador of q.contadores || []) this.flags[this.claveInicioMision(qid, contador)] = this.flags[contador] || 0;
18847:       this.quests[qid] = "activa";
18848:     }
18849:     this.misionesNuevas.add(qid);
18850:     this.actualizarBotonMisiones();
18851:     this.autoguardar();
18852:     return true;
18853:   }
18854: 
18855:   completarMision(qid) {
18856:     const q = QUESTS[qid];
18857:     if (!q || this.quests[qid] !== "activa" || !q.listo(this)) return [];
18858:     if (q.entregar) q.entregar(this);
18859:     this.quests[qid] = "hecha";
18860:     const recompensa = q.recompensa ? q.recompensa(this) : [];
18861:     this.misionesNuevas.add(qid);
18862:     this.actualizarBotonMisiones();
18863: 
18864:     this.autoguardar();
18865:     const frase = this.valorMision(q, "frase", null);
18866:     return [...(frase ? [frase] : []), `[Misión completada: ${q.nombre}]`, ...recompensa];
18867:   }
18868: 
18869:   gestionarMisionesNpc(npc) {
18870: return "";
18871:   }
18872: 
18873:   
18874: 
18875:   marcarProgresoMisiones() {
18876:     for (const [qid, estado] of Object.entries(this.quests)) {
18877:       if (estado === "activa" && QUESTS[qid]?.listo(this)) this.misionesNuevas.add(qid);
18878:     }
18879:     this.actualizarBotonMisiones();
18880:   }
18881: 
18882:   valorMision(q, campo, defecto = "—") {
18883:     const valor = q && q[campo];
18884:     if (typeof valor === "function") return valor(this);
18885:     return valor ?? defecto;
18886:   }
18887: 
18888:   consecuenciaMision(qid, q) {
18889: return "";
18890:   }
18891: 
18892:   normalizarFacciones() {
18893:     if (!this.player) return;
18894:     const p = this.player;
18895:     p.facciones ||= {};
18896:     let registro = p.facciones[FACCION_PRINCIPAL];
18897:     if (!registro) {
18898:       registro = p.facciones[FACCION_PRINCIPAL] = {
18899:         estado: "miembro", saldo: 0, merito: 0,
18900:         reputacion: 0, gastos: 0, historial: [],
18901:       };
18902:     } else {
18903:       registro.estado ||= "miembro";
18904:       registro.saldo = Math.max(0, Number(registro.saldo) || 0);
18905:       registro.merito = Math.max(registro.saldo, Number(registro.merito) || 0);
18906:       registro.reputacion = Number(registro.reputacion) || 0;
18907:       registro.gastos = Math.max(0, Number(registro.gastos) || 0);
18908:       registro.historial = Array.isArray(registro.historial) ? registro.historial.slice(-30) : [];
18909:     }
18910:     p.facciones_version = 1;
18911:     p.faccion_principal ||= FACCION_PRINCIPAL;
18912:     p.contribucion = registro.saldo; // reflejo del saldo actual para los consumidores del personaje
18913:   }
18914: 
18915:   afiliarFaccion(id, estado = "miembro", principal = false) {
18916:     if (!this.player || !FACCIONES[id]) return { ok: false, texto: "La organización no existe en este mundo." };
18917:     this.player.facciones ||= {};
18918:     const registro = this.player.facciones[id] ||= {
18919:       estado, saldo: 0, merito: 0, reputacion: 0, gastos: 0, historial: [],
18920:     };
18921:     registro.estado = estado;
18922:     if (principal) this.player.faccion_principal = id;
18923:     return { ok: true, registro };
18924:   }
18925: 
18926:   cambiarEstadoFaccion(id, estado) {
18927:     const permitidos = ["miembro", "huesped", "aliado", "inactivo", "expulsado"];
18928:     const registro = this.player?.facciones?.[id];
18929:     if (!registro || !permitidos.includes(estado)) return false;
18930:     registro.estado = estado;
18931:     return true;
18932:   }
18933: 
18934:   ajustarReputacionFaccion(id, cantidad) {
18935:     const registro = this.player?.facciones?.[id];
18936:     if (!registro) return null;
18937:     registro.reputacion = (Number(registro.reputacion) || 0) + (Number(cantidad) || 0);
18938:     return registro.reputacion;
18939:   }
18940: 
18941:   registroFaccion(id = FACCION_PRINCIPAL) {
18942:     this.normalizarFacciones();
18943:     return this.player?.facciones?.[id] || null;
18944:   }
18945: 
18946:   rangoFaccion(id = FACCION_PRINCIPAL) {
18947:     const faccion = FACCIONES[id], registro = this.registroFaccion(id);
18948:     if (!faccion || !registro) return null;
18949:     let rango = faccion.rangos[0];
18950:     for (const candidato of faccion.rangos) if (registro.merito >= candidato.merito) rango = candidato;
18951:     return rango;
18952:   }
18953: 
18954:   otorgarContribucion(cantidad, motivo = "Servicio reconocido", id = FACCION_PRINCIPAL) {
18955:     const registro = this.registroFaccion(id);
18956:     if (!registro || registro.estado === "expulsado") return null;
18957:     const valor = Math.max(0, Number(cantidad) || 0);
18958:     if (!valor) return null;
18959:     const rangoAntes = this.rangoFaccion(id)?.id;
18960:     registro.saldo += valor;
18961:     registro.merito += valor;
18962:     registro.historial.push({ tipo: "ingreso", cantidad: valor, motivo, turno: this.turnoGlobal });
18963:     registro.historial = registro.historial.slice(-30);
18964:     this.player.contribucion = this.registroFaccion(FACCION_PRINCIPAL)?.saldo || 0;
18965:     const rangoDespues = this.rangoFaccion(id);
18966:     return { saldo: registro.saldo, merito: registro.merito,
18967:       rangoNuevo: rangoDespues?.id !== rangoAntes ? rangoDespues?.nombre : null };
18968:   }
18969: 
18970:   gastarContribucion(cantidad, motivo, id = FACCION_PRINCIPAL) {
18971:     const registro = this.registroFaccion(id);
18972:     const valor = Math.max(0, Number(cantidad) || 0);
18973:     if (!registro || registro.estado !== "miembro") return { ok: false, texto: "No tienes acceso activo a los servicios de esa facción." };
18974:     if (registro.saldo < valor) return { ok: false, texto: `Necesitas ${valor} de contribución disponible; tienes ${registro.saldo}.` };
18975:     registro.saldo -= valor;
18976:     registro.gastos += valor;
18977:     registro.historial.push({ tipo: "gasto", cantidad: valor, motivo, turno: this.turnoGlobal });
18978:     registro.historial = registro.historial.slice(-30);
18979:     this.player.contribucion = this.registroFaccion(FACCION_PRINCIPAL)?.saldo || 0;
18980:     return { ok: true, saldo: registro.saldo, merito: registro.merito };
18981:   }
18982: 
18983:   normalizarProfesiones() {
18984:     if (!this.player) return;
18985:     const p = this.player;
18986:     p.profesiones ||= {};
18987: 
18988:     // CONSERVAR_NORMALIZACION_ACTUAL: completar registros sin importar otros oficios.
18989:     const baseExamen = p.profesiones.examen || {};
18990:     p.profesiones.examen = Object.assign({
18991:       xp: 0, rango: 0, materiales: {}, total: 0, cadaveres: 0,
18992:       hallazgos: {}, descubrimientos: {}, procedimientos: {}, desbloqueada: false,
18993:     }, baseExamen);
18994:     p.profesiones.examen.materiales ||= {};
18995:     p.profesiones.examen.hallazgos ||= {};
18996:     p.profesiones.examen.descubrimientos ||= {};
18997:     p.profesiones.examen.procedimientos ||= {};
18998:     // Validar familiaridad actual; un booleano no acredita observaciones.
18999:     for (const [mobId, previo] of Object.entries(p.profesiones.examen.descubrimientos)) {
19000:       if (!previo || typeof previo !== "object" || Array.isArray(previo)) {
19001:         delete p.profesiones.examen.descubrimientos[mobId];
19002:       } else {
19003:         previo.observaciones = Math.max(0, Math.floor(Number(previo.observaciones) || 0));
19004:         previo.exitos = Math.max(0, Math.floor(Number(previo.exitos) || 0));
19005:         previo.procedimientos ||= {};
```

