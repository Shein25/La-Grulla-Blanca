# Extracto 09 — EXAMINAR/scenery/gates

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## gateEntre / normalización gates

Fuente: `grulla-blanca_ver74.html` · líneas 2295-2348

```js
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
02309: function recorrerMundo329(inicio = "patio_raices", estado = null, rooms = ROOMS) {
02310:   const vistos = new Set(rooms[inicio] ? [inicio] : []), cola = [...vistos];
02311:   for (let i = 0; i < cola.length; i++) for (const destino of Object.values(rooms[cola[i]].exits || {})) {
02312:     if (!rooms[destino] || vistos.has(destino) || (estado && !pasoGateAbierto(cola[i], destino, estado))) continue;
02313:     vistos.add(destino); cola.push(destino);
02314:   }
02315:   return vistos;
02316: }
02317: function auditarMundo329(rooms = ROOMS) {
02318:   const errores = [], ids = Object.keys(rooms), areas = new Set(), externos = [], rotas = [], aisladas = [];
02319:   let exits = 0;
02320:   for (const [id, r] of Object.entries(rooms)) {
02321:     areas.add(r.area);
02322:     if (r.id !== id) errores.push("ID incoherente: " + id);
02323:     if (!AREAS[r.area]) errores.push("Área inexistente: " + id);
02324:     let internos = 0;
02325:     for (const [d, dest] of Object.entries(r.exits || {})) {
02326:       exits++;
02327:       if (!DIRECCION_OPUESTA[d]) errores.push("Dirección inválida: " + id + "." + d);
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
```

## cmd_examinar

Fuente: `grulla-blanca_ver74.html` · líneas 19820-19965

```js
19820:       return `Todavía conservas el reposo anterior. Viaja, combate o cultiva durante ${faltan} ${faltan === 1 ? "acción" : "acciones"} más antes de volver a dormir.`;
19821:     }
19822: 
19823:     const antesHp = p.hp, antesQi = p.qi;
19824:     p.hp = p.max_hp;
19825:     p.qi = Math.min(p.qi_max, p.qi + Math.ceil(p.qi_max * 0.5));
19826:     this.airarSaturacion();
19827:     if (sala.alojamiento.purifica && impurezas > 0) p.impurezas = impurezas - 1;
19828:     this.reiniciarActividadReposo();
19829: 
19830:     const out = [sala.alojamiento.inicio];
19831:     if (emergencia && actividad < ACCIONES_DORMIR) out.push("No tenías verdadero sueño, pero las heridas exigían reposo.");
19832:     if (p.hp > antesHp) out.push(`Despiertas entero. Recuperas ${p.hp - antesHp} de vida.`);
19833:     if (p.qi > antesQi) out.push(`El reposo devuelve ${p.qi - antesQi} de qi a tu dantian.`);
19834:     out.push("El reposo renueva las venas espirituales. (saturación 100%)");
19835:     if (sala.alojamiento.purifica && impurezas > 0) out.push("El sueño seguro destila parte del sedimento que llevabas. (impureza −1)");
19836:     else if (!sala.alojamiento.purifica && impurezas > 0) out.push("El lecho permite dormir, pero su qi estancado no purifica tus impurezas.");
19837:     out.push(sala.alojamiento.cierre || "El reposo termina y el cuerpo está listo para continuar.");
19838:     this.avanzarEcologia(PULSOS_DORMIR);
19839:     out.push(...this.avanzarAflicciones(PULSOS_DORMIR));
19840:     this.moverErrantesTrasReposo(out);
19841:     this.salida(out.join("\n"));
19842:     this.autoguardar();
19843:   }
19844: 
19845:   cmd_examinar(args) {
19846:     if (!args.length) { this.mostrarSala(); return; }
19847:     const texto = args.join("_");
19848:     
19849:     const mobExaminado = resolverMobPorArgs(this.vivos.filter(m => m.hp > 0), args);
19850:     if (mobExaminado) {
19851:         this.recordarCriatura(mobExaminado, true);
19852:         this.mostrarFichaCriatura(mobExaminado);
19853:         return;
19854:     }
19855:     const cadaver = this.resolverCadaver(args);
19856:     if (cadaver) return this.describirCadaver(cadaver);
19857:     const sala = this.rooms[this.pos];
19858:     const npcs = this.npcsEnSala(this.pos);
19859:     const npc=resolverNPC(args.join(" "),npcs);
19860:     if (npc) {
19861:       const descripcion=DESCS_NPC[npc] || `${NOMBRES_NPC[npc]} — ${NPC_DEF[npc].rol}.`;
19862:       this.atlas.personas[npc] = { ...(this.atlas.personas[npc] || {}), sala:this.pos, turno:this.turnoGlobal, descripcion };
19863:       return descripcion;
19864:     }
19865:     
19866:     
19867:     
19868:     
19869:     
19870:     const scenery = sala.scenery || {};
19871:     const esc = scenery[texto]
19872:       ?? Object.entries(scenery).find(([k]) => quitaAcentos(k.toLowerCase()) === texto)?.[1];
19873:     if (esc) return esc;
19874:     const mid = this.resolverItem(args, "ambos");
19875:     if (!mid) return "No ves eso por aquí.";
19876:     const it = ITEMS[mid];
19877:     const st = statsItem(mid);
19878:     const base = it.desc || `Un ${it.name}.`;
19879:     const perfil = it.tecnica ? `\n[Para ti: ${this.perfilTecnica(it.tecnica)}]` : "";
19880:     const dejado = this.objetosTiradosEnSala().filter(reg => reg.mid === mid)
19881:       .map(reg => reg.desapareceEn - this.turnoGlobal);
19882:     const suelo = dejado.length
19883:       ? `\n[Dejado en el suelo: ${Math.min(...dejado)} turnos antes de desaparecer.]`
19884:       : "";
19885:     return (st ? `${base}\n  [${st}]` : base) + perfil + suelo;
19886:   }
19887: 
19888:   cmd_tomar(args) {
19889:     const texto = args.join("_");
19890: 
19891:     const mid = this.resolverItem(args, "sala");
19892:     if (!mid) return "No hay eso aquí.";
19893:     const sala = this.rooms[this.pos];
19894:     if ((sala.items || []).includes(mid)) {
19895:       const idx = sala.items.indexOf(mid);
19896:       if (idx >= 0) sala.items.splice(idx, 1);
19897:     }
19898:     else if (this.tieneSentido() && (sala.oculto || []).includes(mid)) {
19899:       const idxo = sala.oculto.indexOf(mid);
19900:       if (idxo >= 0) sala.oculto.splice(idxo, 1);
19901:     } else {
19902:       const tirados = this.objetosTiradosEnSala();
19903:       const idxTirado = tirados.findIndex(reg => reg.mid === mid);
19904:       if (idxTirado >= 0) {
19905:         tirados.splice(idxTirado, 1);
19906:         if (tirados.length) this.objetosTirados[this.pos] = tirados;
19907:         else delete this.objetosTirados[this.pos];
19908:       }
19909:     }
19910:     const it = ITEMS[mid];
19911:     if (it.piedras) {
19912:       this.player.piedras += it.piedras;
19913:       return `Tomas ${it.name}: +${it.piedras} piedras espirituales.`;
19914:     }
19915:     this.player.inventario.push(mid);
19916:     return `Tomas: ${it.name}.`;
19917:   }
19918: 
19919:   
19920: 
19921:   cmd_soltar(args) {
19922:     if (!args?.length) return "¿Qué quieres tirar? Escribe TIRAR <objeto>.";
19923:     let mid = this.resolverItem(args, "inv");
19924:     let equipadoEn = null;
19925:     if (!mid) {
19926:       const texto = args.join("_");
19927:       for (const [slot, candidato] of Object.entries(this.player.equipado || {})) {
19928:         const nombre = quitaAcentos(ITEMS[candidato]?.name?.toLowerCase() || "");
19929:         if (candidato === texto || args.every(w => candidato.includes(w) || nombre.includes(w))) {
19930:           mid = candidato;
19931:           equipadoEn = slot;
19932:           break;
19933:         }
19934:       }
19935:     }
19936:     if (!mid) return "No llevas eso ni lo tienes equipado.";
19937:     if (equipadoEn) delete this.player.equipado[equipadoEn];
19938:     else this.player.inventario.splice(this.player.inventario.indexOf(mid), 1);
19939:     this.objetosTirados ||= {};
19940:     (this.objetosTirados[this.pos] ||= []).push({
19941:       mid,
19942:       tiradoEn: this.turnoGlobal,
19943:       desapareceEn: this.turnoGlobal + DURACION_OBJETO_TIRADO,
19944:     });
19945:     const accion = equipadoEn ? "Te lo quitas y lo dejas" : "Lo dejas";
19946:     return `${accion} en el suelo: ${ITEMS[mid].name}. Permanecerá durante ${DURACION_OBJETO_TIRADO} turnos.`;
19947:   }
19948: 
19949:   cmd_inventario() {
19950:     const p = this.player;
19951:     if (!p.inventario.length) return "Vacías las manos: nada. (Todo lo llevado puesto: EQUIPO)";
19952:     const out = ["Llevas:"];
19953:     for (const { mid, cantidad } of agruparObjetos(p.inventario)) {
19954:       const it = ITEMS[mid];
19955:       out.push(`  - ${nombreCantidad(mid, cantidad)}${it.slot ? ` [${it.slot}]` : ""}`);
19956:     }
19957:     out.push(`Piedras espirituales: ${p.piedras}`);
19958:     return out.join("\n");
19959:   }
19960: 
19961:   cmd_equipo() { this.mostrarEquipo(); }
19962: 
19963:   cmd_equipar(args) {
19964:     const p = this.player;
19965:     const mid = this.resolverItem(args, "inv");
```

## movimiento/entrada y gates contexto

Fuente: `grulla-blanca_ver74.html` · líneas 16480-16620

```js
16480:     return "   [Nueva condición persistente] El efecto seguirá contigo fuera del combate y avanzará cuando pase tiempo. ESTADO muestra su duración; AYUDA AFLICCIONES explica familias, grados y tratamientos.";
16481:   }
16482: 
16483:   normalizarAflicciones() {
16484:     if (!this.player) return [];
16485:     if (!Array.isArray(this.player.aflicciones)) this.player.aflicciones = [];
16486:     this.player.aflicciones = this.player.aflicciones.filter(a => a && TIPOS_AFLICCION_PERSISTENTE.has(a.tipo)).map(a => ({
16487:       tipo: a.tipo,
16488:       familia: String(a.familia || "desconocida"),
16489:       grado: Math.max(1, Math.floor(Number(a.grado) || 1)),
16490:       nombre: a.nombre || `${a.tipo === "veneno" ? "Veneno" : "Quemadura"} de ${capitalizarUI(String(a.familia || "origen desconocido"))}`,
16491:       daño: String(a.daño || a.params?.daño || "1"),
16492:       duracion: Math.max(1, Math.floor(Number(a.duracion) || 1)),
16493:       origen: a.origen || "desconocido",
16494:     }));
16495:     return this.player.aflicciones;
16496:   }
16497: 
16498:   aplicarAfliccion(conf = {}, origen = "desconocido") {
16499:     if (!this.player || !TIPOS_AFLICCION_PERSISTENTE.has(conf.tipo)) return null;
16500:     const lista = this.normalizarAflicciones();
16501:     const nueva = {
16502:       tipo: conf.tipo,
16503:       familia: String(conf.familia || "desconocida"),
16504:       grado: Math.max(1, Math.floor(Number(conf.grado) || 1)),
16505:       nombre: conf.nombre || `${conf.tipo === "veneno" ? "Veneno" : "Quemadura"} de ${capitalizarUI(String(conf.familia || "origen desconocido"))}`,
16506:       daño: String(conf.daño || "1"),
16507:       duracion: Math.max(1, Math.floor(Number(conf.turnos ?? conf.duracion) || 1)),
16508:       origen,
16509:     };
16510:     const idx = lista.findIndex(a => a.tipo === nueva.tipo && a.familia === nueva.familia);
16511:     if (idx < 0) {
16512:       lista.push(nueva);
16513:       return nueva;
16514:     }
16515:     const actual = lista[idx];
16516:     const reemplaza = nueva.grado > actual.grado || (nueva.grado === actual.grado && promedioDado(nueva.daño) > promedioDado(actual.daño));
16517:     if (reemplaza) {
16518:       nueva.duracion = Math.max(actual.duracion, nueva.duracion);
16519:       lista[idx] = nueva;
16520:       return nueva;
16521:     }
16522:     actual.duracion = Math.max(actual.duracion, nueva.duracion);
16523:     return actual;
16524:   }
16525: 
16526:   avanzarAflicciones(pulsos = 1, { combate = false } = {}) {
16527:     if (!this.player || !Number.isFinite(pulsos) || pulsos <= 0) return [];
16528:     const out = [];
16529:     this.normalizarAflicciones();
16530:     const pasos = Math.max(0, Math.floor(pulsos));
16531:     for (let paso = 0; paso < pasos && this.player.aflicciones.length; paso++) {
16532:       const supervivientes = [];
16533:       for (const af of this.player.aflicciones) {
16534:         const d = Math.max(0, tirar(af.daño));
16535:         const antes = this.player.hp;
16536:         this.player.hp = combate ? this.player.hp - d : Math.max(1, this.player.hp - d);
16537:         const real = Math.max(0, antes - this.player.hp);
16538:         if (real > 0) out.push(`${af.nombre} te causa ${real} de daño${!combate && this.player.hp === 1 && d > real ? " (fuera de combate no puede rematarte)" : ""}.`);
16539:         af.duracion -= 1;
16540:         if (af.duracion <= 0) out.push(`${af.nombre} se disipa.`);
16541:         else supervivientes.push(af);
16542:       }
16543:       this.player.aflicciones = supervivientes;
16544:       if (combate && this.player.hp <= 0) break;
16545:     }
16546:     return out;
16547:   }
16548: 
16549:   tratarAfliccion(cura = {}) {
16550:     const lista = this.normalizarAflicciones();
16551:     const gradoMax = Math.max(0, Math.floor(Number(cura.gradoMax) || 0));
16552:     const compatibles = lista.map((a, i) => ({ a, i })).filter(({a}) => a.tipo === cura.tipo && a.familia === cura.familia && a.grado <= gradoMax);
16553:     if (!compatibles.length) {
16554:       const mismoTipo = lista.find(a => a.tipo === cura.tipo);
16555:       if (mismoTipo) return { ok:false, mensaje:`La medicina no responde a ${mismoTipo.nombre}: requiere familia ${cura.familia} y grado ≤${gradoMax}. No la consumes.` };
16556:       return { ok:false, mensaje:`No padeces una ${cura.tipo} compatible de la familia ${cura.familia}. Guardas la medicina.` };
16557:     }
16558:     compatibles.sort((x,y) => y.a.grado - x.a.grado || y.a.duracion - x.a.duracion);
16559:     const elegido = compatibles[0];
16560:     lista.splice(elegido.i, 1);
16561:     return { ok:true, afliccion:elegido.a, mensaje:`${elegido.a.nombre} cede por completo.` };
16562:   }
16563: 
16564:   resumenAflicciones() {
16565:     const lista = this.normalizarAflicciones();
16566:     return lista.length ? lista.map(a => `${a.nombre} · ${a.duracion} acción${a.duracion === 1 ? "" : "es"}`).join(" · ") : "Ninguna";
16567:   }
16568: 
16569:   avanzarEcologia(pulsos = 1) {
16570:     if (!Number.isFinite(pulsos) || pulsos <= 0) return;
16571:     this.relojEcologico = (Number.isFinite(this.relojEcologico) ? this.relojEcologico : 0) + pulsos;
16572:     this.actualizarErrantes();
16573:   }
16574: 
16575:   intentarPulsoMeditacion() {
16576:     if (Azar.random() >= PROB_PULSO_MEDITACION) return false;
16577:     this.avanzarEcologia(1);
16578:     return true;
16579:   }
16580: 
16581:   
16582: 
16583:   registrarInterrupcionMeditacion() {
16584:     this.interrupcionEn ||= {};
16585:     this.interrupcionEn[this.pos] = this.relojEcologico + COOLDOWN_INTERRUPCION;
16586:   }
16587: 
16588:   airearVenaLocal() {
16589:     const actual = this.saturacionDe(this.pos);
16590:     if (actual <= 1) delete this.saturacion[this.pos];
16591:     else this.saturacion[this.pos] = actual - 1;
16592:     return { antes: actual, despues: Math.max(0, actual - 1) };
16593:   }
16594: 
16595:   moverErrantesTrasReposo(out) {
16596:     this.moverErrantes();
16597:     const presentes = (this.errantes || []).filter(e => e.muertoHasta === 0 && e.sala === this.pos);
16598:     for (const e of presentes) {
16599:       if (this.vivos.some(m => m.errante_id === e.id && m.hp > 0)) continue;
16600:       const mob = crearMob(e.mobId, MOBS[e.mobId], {
16601:         erranteId: e.id, erranteDesde: e.desde, erranteMovidoEn: e.movidoEn,
16602:       });
16603:       this.vivos.push(mob);
16604:       out.push(`Al levantar la mirada, descubres que ${mob.name} ha entrado en la zona mientras bajabas la guardia.`);
16605:     }
16606:     const totales = {};
16607:     for (const mob of this.vivos.filter(m => m.hp > 0)) totales[mob.mob_id] = (totales[mob.mob_id] || 0) + 1;
16608:     const vistos = {};
16609:     for (const mob of this.vivos.filter(m => m.hp > 0)) {
16610:       mob.indice_especie = (vistos[mob.mob_id] || 0) + 1;
16611:       vistos[mob.mob_id] = mob.indice_especie;
16612:       mob.total_especie = totales[mob.mob_id];
16613:     }
16614:   }
16615: 
16616:   // ---------- mobs errantes (array: cada uno con su propio territorio y estado) ----------
16617: 
16618:   actualizarErrante(e) {
16619:     if (e.muertoHasta > 0 && this.relojEcologico >= e.muertoHasta) {
16620:       // el cooldown venció: vuelve a la vida en su sala de origen, no donde murió
```

## Referencias runtime de gates

```js
22056:     const gate=gateEntre(origen,destino),cerrado=!!gate&&!this.gates[gate.id],atajo=gate?.id.startsWith("ATAJO_ALA_");
```

