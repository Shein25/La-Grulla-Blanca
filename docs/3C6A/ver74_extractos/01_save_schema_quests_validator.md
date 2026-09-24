# Extracto 01 — Save/schema/validador

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## Schema, gates, alojamientos y validarSave329

Fuente: `grulla-blanca_ver74.html` · líneas 2190-2455

```js
02190: <script>
02191: // Coordenadas exclusivamente de fixtures de regresión: nunca se guardan ni son cartografía canónica.
02192: function conAtlasPrueba329(fn) {
02193:  document.getElementById("atlas").close();
02194:  try { return fn(); } finally { document.getElementById("atlas").close(); }
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
02401:     for(const [k,v]of Object.entries(gates))bool(v,'gates.'+k);
02402:     if(gates.SECTA_INTERIOR===false&&(gates.M12===true||Object.keys(gates).some(k=>k.startsWith('ATAJO_ALA_')&&gates[k]===true)))fail('gates.invariante');
02403:     const salas=obj(data.salas,'salas');keys(salas,Object.keys(ROOMS),'salas');
02404:     for(const [id,raw]of Object.entries(salas)){const s=obj(raw,'salas.'+id);if(!ref(ROOMS,id))fail('salas.'+id);keys(s,['items','oculto'],'salas.'+id);references(s.items,ITEMS,id+'.items');references(s.oculto,ITEMS,id+'.oculto');}
02405:     for(const field of ['saturacion','interrupcionEn'])for(const [id,v]of Object.entries(obj(data[field],field))){if(!ref(ROOMS,id))fail(field+'.'+id);num(v,field+'.'+id);}
02406:     const fixed=new Set();for(const [id,r]of Object.entries(ROOMS)){const n={};for(const mid of r.mobs){n[mid]=(n[mid]||0)+1;fixed.add(`${id}:${mid}:${n[mid]}`);}}
02407:     for(const [id,v]of Object.entries(obj(data.respawnEn,'respawnEn'))){if(!fixed.has(id))fail('respawnEn.'+id);num(v,'respawnEn.'+id);}
02408:     const errantes=arr(data.errantes,'errantes');keys(Object.fromEntries(errantes.filter(plain).map(e=>[e.id,true])),ERRANTES_INICIALES.map(e=>e.id),'errantes.identidades');
02409:     if(errantes.length!==ERRANTES_INICIALES.length)fail('errantes.cantidad');
02410:     for(const raw of errantes){const e=obj(raw,'errante'),base=ERRANTES_INICIALES.find(b=>b.id===e.id);if(!base){fail('errante.id');continue;}
02411:       if(e.mobId!==base.mobId||e.origen!==base.origen||JSON.stringify(e.territorio)!==JSON.stringify(base.territorio)||!base.territorio.includes(e.sala))fail('errante.territorio');
02412:       if(has(e,"desde")&&e.desde!==null&&!base.territorio.includes(e.desde))fail('errante.desde');num(e.muertoHasta,'errante.muertoHasta');if(has(e,"movidoEn"))integer(e.movidoEn,'errante.movidoEn',-1);}
02413:     for(const [id,raw]of Object.entries(obj(data.objetosTirados,'objetosTirados'))){if(!ref(ROOMS,id))fail('objetosTirados.'+id);
02414:       for(const entry of arr(raw,'objetosTirados.'+id)){const e=obj(entry,'objetoTirado');if(!ref(ITEMS,e.mid))fail('objetoTirado.mid');num(e.desapareceEn,'objetoTirado.desapareceEn');}}
02415:     for(const [id,raw]of Object.entries(obj(data.cadaveres,'cadaveres'))){if(!ref(ROOMS,id))fail('cadaveres.'+id);
02416:       for(const entry of arr(raw,'cadaveres.'+id)){const e=obj(entry,'cadaver');if(!ref(MOBS,e.mob_id))fail('cadaver.mob_id');for(const k of ['name','corto','tipo'])str(e[k],'cadaver.'+k);num(e.caidoEn,'cadaver.caidoEn');num(e.desapareceEn,'cadaver.desapareceEn');
02417:         if(has(e,'investigado'))arr(e.investigado,'cadaver.investigado').forEach(v=>str(v,'cadaver.investigado'));
02418:         if(has(e,'examenProcedimientos'))for(const v of Object.values(obj(e.examenProcedimientos,'cadaver.examenProcedimientos')))str(v,'cadaver.procedimiento');}}
02419:     const atlas=obj(data.atlas,'atlas');keys(atlas,['salas','personas','criaturas'],'atlas');
02420:     for(const [id,raw]of Object.entries(obj(atlas.salas,'atlas.salas'))){const s=obj(raw,'atlas.sala');if(!ref(ROOMS,id))fail('atlas.sala.id');
02421:       for(const pair of arr(s.salidas,'atlas.salidas')){if(!Array.isArray(pair)||pair.length!==2||!DIRECCIONES.includes(pair[0])||ROOMS[id]?.exits[pair[0]]!==pair[1])fail('atlas.salida');}
02422:       references(s.items,ITEMS,'atlas.items');references(s.npcs,NOMBRES_NPC,'atlas.npcs');references(s.mobs,MOBS,'atlas.mobs');
02423:       integer(s.turno,'atlas.turno');str(s.vena,'atlas.vena');bool(s.salvaje,'atlas.salvaje');bool(s.resentida,'atlas.resentida');
02424:       if(s.alojamiento!==null){const l=obj(s.alojamiento,'atlas.alojamiento');str(l.nombre,'atlas.alojamiento.nombre');bool(l.purifica,'atlas.alojamiento.purifica');}}
02425:     for(const [id,raw]of Object.entries(obj(atlas.personas,'atlas.personas'))){const p=obj(raw,'atlas.persona');if(!ref(NOMBRES_NPC,id)||!ref(ROOMS,p.sala))fail('atlas.persona');integer(p.turno,'atlas.persona.turno');}
02426:     for(const [id,raw]of Object.entries(obj(atlas.criaturas,'atlas.criaturas'))){const c=obj(raw,'atlas.criatura');if(!ref(MOBS,id)||!ref(ROOMS,c.sala))fail('atlas.criatura');references(c.lugares,ROOMS,'atlas.lugares');integer(c.turno,'atlas.criatura.turno');bool(c.errante,'atlas.errante');bool(c.examinada,'atlas.examinada');
02427:       if(has(c,'botin'))for(const [mid,v]of Object.entries(obj(c.botin,'atlas.botin'))){if(!ref(ITEMS,mid))fail('atlas.botin.id');obj(v,'atlas.botin.registro');}}
02428:     const p=obj(data.player,'player');
02429:     for(const [k,v]of Object.entries({cultivo_version:1,profesiones_version:6,facciones_version:1,meridianos_version:3,equipo_version:2,builds_version:2}))if(p[k]!==v)fail('player.'+k);
02430:     for(const k of ['name','reino','raiz','origen','titulo','daño'])str(p[k],'player.'+k);
02431:     if(!ref(RAICES,p.raiz)||!ref(ORIGENES,p.origen))fail('player.origen/raiz');
02432:     for(const k of ['hp','max_hp','ataque','defensa','qi','qi_max','etapa','comprension','piedras','impurezas','heridas_meridianos','actividad_reposo','puntos_tecnica_total','build_seq'])num(p[k],'player.'+k,k==='hp'?-Infinity:0);
02433:     references(p.inventario,ITEMS,'player.inventario');for(const mid of Object.values(obj(p.equipado,'player.equipado')))if(!ref(ITEMS,mid))fail('player.equipado.id');
02434:     for(const id of Object.keys(obj(p.afinidad,'player.afinidad')))if(!ref(NOMBRES_NPC,id))fail('player.afinidad.id');
02435:     const tecnicas=obj(p.tecnicas,'player.tecnicas');
02436:     const ramas=(raw,path)=>{const v=obj(raw,path);for(const n of [1,2,3])if(![0,1,2,3].includes(v[n]))fail(path+'.'+n);};
02437:     for(const [id,raw]of Object.entries(tecnicas)){const t=obj(raw,'tecnica');if(!ref(TECNICAS,id))fail('tecnica.id');for(const k of ['maestria','usos','practica'])num(t[k],'tecnica.'+k);ramas(t.ramas,'tecnica.ramas');}
02438:     references(p.tecnicas_preparadas,tecnicas,'player.tecnicas_preparadas');
02439:     for(const raw of arr(p.builds,'player.builds')){const b=obj(raw,'build');str(b.id,'build.id');str(b.nombre,'build.nombre');references(b.preparadas,tecnicas,'build.preparadas');for(const [tid,rs]of Object.entries(obj(b.ramas,'build.ramas'))){if(!ref(tecnicas,tid))fail('build.tecnica');ramas(rs,'build.ramas');}}
02440:     if(p.build_activa!==null&&!arr(p.builds,'builds').some(b=>b?.id===p.build_activa))fail('build_activa');
02441:     for(const raw of arr(p.aflicciones,'player.aflicciones')){const a=obj(raw,'afliccion');if(!TIPOS_AFLICCION_PERSISTENTE.has(a.tipo))fail('afliccion.tipo');for(const k of ['familia','nombre','daño','origen'])str(a[k],'afliccion.'+k);num(a.grado,'afliccion.grado',1);num(a.duracion,'afliccion.duracion',1);}
02442:     const h=obj(p.historialAcciones,'historialAcciones');if(h.version!==HISTORIAL_ACCIONES_VERSION)fail('historialAcciones.version');integer(h.secuencia,'historialAcciones.secuencia');
02443:     for(const raw of arr(h.eventos,'historialAcciones.eventos')){const e=obj(raw,'evento');str(e.id,'evento.id');if(!TIPOS_ACCION_VALIDOS.has(e.tipo))fail('evento.tipo');integer(e.orden,'evento.orden',1);num(e.importancia,'evento.importancia',1);arr(e.etiquetas,'evento.etiquetas').forEach(v=>str(v,'etiqueta'));obj(e.contexto,'evento.contexto');obj(e.consecuencias,'evento.consecuencias');const m=obj(e.momento,'evento.momento');str(m.reino,'momento.reino');for(const k of ['arco','etapa','turno'])num(m[k],'momento.'+k);}
02444:     arr(p.historialReinos,'historialReinos');arr(p.historialArcos,'historialArcos');const ilu=obj(p.iluminacion,'iluminacion'),trib=obj(p.tribulacionCorazon,'tribulacionCorazon');bool(ilu.alcanzada,'iluminacion.alcanzada');bool(trib.superada,'tribulacion.superada');bool(trib.pendienteReintento,'tribulacion.pendienteReintento');bool(p.granPerfeccionLianQi,'granPerfeccionLianQi');
02445:     for(const k of ['historialReinos','historialArcos'])for(const raw of arr(p[k],k)){const e=obj(raw,k+'.entrada');str(e.reino,k+'.reino');integer(e.arco,k+'.arco',1);}
02446:     if(ilu.semillaCorazonDao!==null)str(ilu.semillaCorazonDao,'iluminacion.semillaCorazonDao');
02447:     const fac=obj(p.facciones,'facciones');if(!ref(fac,p.faccion_principal))fail('faccion_principal');for(const [id,raw]of Object.entries(fac)){const f=obj(raw,'faccion');if(!ref(FACCIONES,id))fail('faccion.id');str(f.estado,'faccion.estado');for(const k of ['saldo','merito','gastos'])num(f[k],'faccion.'+k);num(f.reputacion,'faccion.reputacion',-Infinity);arr(f.historial,'faccion.historial').forEach(x=>obj(x,'faccion.movimiento'));}
02448:     const prof=obj(p.profesiones,'profesiones');for(const id of ['examen','herboristeria','alquimia','forja','inscripcion']){const o=obj(prof[id],'profesiones.'+id);num(o.xp,id+'.xp');integer(o.rango,id+'.rango');bool(o.desbloqueada,id+'.desbloqueada');}
02449:     for(const [id,fields]of Object.entries({examen:['materiales','hallazgos','descubrimientos','procedimientos'],herboristeria:['materiales','especies','procedimientos','nodos'],alquimia:['calidades','recetas']}))for(const k of fields)obj(prof[id]?.[k],id+'.'+k);
02450:     for(const id of ['examen','herboristeria']){const o=plain(prof[id])?prof[id]:{};for(const k of ['materiales','procedimientos'])for(const v of Object.values(obj(o[k],id+'.'+k)))num(v,id+'.'+k);
02451:       const records=id==='examen'?o.descubrimientos:o.especies;for(const raw of Object.values(obj(records,id+'.especies'))){const r=obj(raw,id+'.especie');num(r.observaciones,'especie.observaciones');num(r.exitos,'especie.exitos');obj(r.procedimientos,'especie.procedimientos');}}
02452:     for(const [id,raw]of Object.entries(obj(prof.herboristeria?.nodos,'herboristeria.nodos'))){if(!ref(NODOS_HERBORISTERIA,id))fail('nodo.id');const n=obj(raw,'nodo');for(const v of Object.values(obj(n.partes,'nodo.partes')))num(v,'nodo.parte');for(const k of ['observaciones','exitos','cambios','muertaHasta'])num(n[k],'nodo.'+k);num(n.cambioObservado,'nodo.cambioObservado',-1);}
02453:     for(const [id,raw]of Object.entries(obj(prof.alquimia?.recetas,'alquimia.recetas'))){if(!ref(RECETAS,id))fail('receta.id');const r=obj(raw,'receta');bool(r.conocida,'receta.conocida');num(r.validas,'receta.validas');if(r.mejor!==null&&!ref(CALIDADES_ALQUIMIA,r.mejor))fail('receta.mejor');obj(r.hitos,'receta.hitos');const ds=obj(r.dominios,'receta.dominios');for(const d of Object.values(ds)){const dr=obj(d,'receta.dominio');bool(dr.excepcional,'dominio.excepcional');if(dr.metodo!==null)arr(dr.metodo,'dominio.metodo').forEach(v=>{if(![1,2,3].includes(v))fail('dominio.metodo');});}for(const rawQ of arr(r.pulsos,'receta.pulsos')){const q=obj(rawQ,'pulso');obj(q.aciertos,'pulso.aciertos');arr(q.descartados,'pulso.descartados');if(q.confirmado!==null&&![1,2,3].includes(q.confirmado))fail('pulso.confirmado');}}
02454:   } catch { errores.push("Estructura de save ilegible o inválida"); }
02455:   return errores;
```

## serializar / deserializar

Fuente: `grulla-blanca_ver74.html` · líneas 16288-16385

```js
16288:   escribirSlot(clave, data) {
16289:     try {
16290:       if (validarSave329(data).length) return false;
16291:       localStorage.setItem(clave, JSON.stringify(data)); return true;
16292:     } catch { return false; }
16293:   }
16294: 
16295:   serializar() {
16296:     // Snapshot puro: guardar no poda recursos ni adelanta contadores. Sin estado UI.
16297:     const salas = {};
16298:     for (const [rid, s] of Object.entries(this.rooms)) salas[rid] = { items: s.items || [], oculto: s.oculto || [] };
16299:     return JSON.parse(JSON.stringify({ saveSchemaVersion: SAVE_SCHEMA_VERSION,
16300:       gates: this.gates, player: this.player, pos: this.pos, flags: this.flags, quests: this.quests,
16301:       salas, visitadas: [...this.visitadas], atlas: this.atlas, saturacion: this.saturacion,
16302:       turnoGlobal: this.turnoGlobal, relojEcologico: this.relojEcologico, respawnEn: this.respawnEn,
16303:       interrupcionEn: this.interrupcionEn, errantes: this.errantes, cadaveres: this.cadaveres,
16304:       objetosTirados: this.objetosTirados, npc_version: 1,
16305:       posicionNPC: this.posicionNPC, conocimientoNPC: this.conocimientoNPC, fecha: Date.now() }));
16306:   }
16307: 
16308:   deserializar(data) {
16309:     if (data?.saveSchemaVersion !== SAVE_SCHEMA_VERSION) { this.salida(MENSAJE_SAVE_INCOMPATIBLE, "error"); return false; }
16310:     const fallos = validarSave329(data);
16311:     if (fallos.length) { this.salida("Partida CORRUPTA/INVÁLIDA: " + fallos.join(" · ") + ". Inicia una Nueva Partida.", "error"); return false; }
16312:     let estado, preservado, vivos, huboCooldown;
16313:     try {
16314:       const copia = JSON.parse(JSON.stringify(data));
16315:       if (validarSave329(copia).length) throw new Error("Snapshot inválido");
16316:       const preparar = c => {
16317:         const rooms = JSON.parse(JSON.stringify(ROOMS));
16318:         for (const [rid, s] of Object.entries(c.salas)) { rooms[rid].items = s.items; rooms[rid].oculto = s.oculto; }
16319:         const e = { rooms, visitadas: new Set(c.visitadas),
16320:           posicionNPC: c.npc_version === 1 ? c.posicionNPC : crearPosicionNPC(),
16321:           conocimientoNPC: c.npc_version === 1 ? c.conocimientoNPC : crearConocimientoNPC() };
16322:         for (const k of ["player","pos","flags","quests","gates","atlas","saturacion","turnoGlobal","relojEcologico","respawnEn","interrupcionEn","errantes","cadaveres","objetosTirados"]) e[k] = c[k];
16323:         return e;
16324:       };
16325:       // Preparación aislada: reconstruir sólo vivos; jamás normalizar/importar el payload.
16326:       const temporal = Object.assign(Object.create(Object.getPrototypeOf(this)), this, preparar(JSON.parse(JSON.stringify(copia))));
16327:       for (const m of ["mostrarSala","recordarAtlas","actualizarMinimapa","actualizarPanel"]) temporal[m] = () => {};
16328:       temporal.entrarSala(); vivos = temporal.vivos; huboCooldown = temporal._huboMobsEnCooldown;
16329:       estado = preparar(JSON.parse(JSON.stringify(copia)));
16330:       preservado = preparar(copia);
16331:     } catch { this.salida("Partida CORRUPTA/INVÁLIDA. No se cargó ningún estado.", "error"); return false; }
16332:     const anteriores = Object.getOwnPropertyDescriptors(this);
16333:     try {
16334:       Object.assign(this, estado, { vivos, _huboMobsEnCooldown: huboCooldown,
16335:         combate: null, pregunta: null, terminado: false, elaboracion: null, alquimiaResultado: null,
16336:         ofiUltimoResultado: null, ofiUltimoResultadoHerboristeria: null, ofiUltimoResultadoExamen: null,
16337:         misionesNuevas: new Set(), misionAbierta: null, categoriasMisionesAbiertas: new Set(["activas","rumores"]),
16338:         atlasAreaVista: null, atlasCapaVista: null, atlasAcordeones: { lugares:new Set(), personas:new Set(), bestiario:new Set() } });
16339:       this.mostrarSala(); this.actualizarBarra(); this.actualizarPanel(); this.actualizarMinimapa();
16340:       // Consultar UI puede normalizar/podar sobre la copia de render. El save restaura exactamente su estado.
16341:       Object.assign(this, preservado);
16342:       return true;
16343:     } catch {
16344:       for (const k of Object.keys(this)) if (!Object.hasOwn(anteriores,k)) delete this[k];
16345:       Object.defineProperties(this, anteriores);
16346:       this.salida("No se pudo cargar la partida. El estado anterior se conserva.", "error");
16347:       return false;
16348:     }
16349:   }
16350: 
16351:   infoPartida(d) {
16352:     const estado = this.clasificarPartida(d);
16353:     if (estado === "INCOMPATIBLE") return estado + " · " + MENSAJE_SAVE_INCOMPATIBLE;
16354:     if (estado !== "VÁLIDO") return estado + " · No se puede cargar. Inicia una Nueva Partida.";
16355:     const p = d.player, fecha = new Date(d.fecha);
16356:     return `VÁLIDO · ${p.name} · ${p.reino} etapa ${p.etapa} · ${ROOMS[d.pos].name} · ${fecha.toLocaleDateString()} ${fecha.toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})}`;
16357:   }
16358: 
16359:   autoguardar(verbose = false) {
16360:     if (!this.player || this.combate || this.terminado) return false;
16361:     if (!this.escribirSlot(CLAVE_AUTO, this.serializar())) {
16362:       this.salida("No se pudo autoguardar. El almacenamiento no está disponible o la partida no es válida.", "error");
16363:       return false;
16364:     }
16365:     this.avisoAuto();
16366:     if (verbose) this.salida("   · partida autoguardada.");
16367:     return true;
16368:   }
16369: 
16370:   menuGuardar() {
16371:     if (this.terminado || !this.player) return;
16372:     if (this.combate) { this.salida("No se puede guardar en pleno combate."); return; }
16373:     if (this.pregunta) { this.salida("Responde antes a la pregunta pendiente."); return; }
16374:     const out = ["— GUARDAR PARTIDA —"];
16375:     for(let i=1;i<=NSLOTS;i++)out.push(`  ${i}) ${this.describirSlot(this.leerSlotDetallado(CLAVE_SLOT(i)))}`);
16376:     this.salida(out.join("\n"));
16377:     this.preguntar("¿En qué slot guardamos? (1/"+NSLOTS+" · 0 para cancelar)", r => {
16378:       const n=Number(r.trim());
16379:       if(!Number.isInteger(n)||n<1||n>NSLOTS){this.salida("Guardado cancelado.");return;}
16380:       if(this.escribirSlot(CLAVE_SLOT(n),this.serializar()))this.salida(`Partida guardada en el slot ${n}.`);
16381:       else this.salida("No se pudo guardar. El almacenamiento no está disponible o está lleno.","error");
16382:     },"1 / 2 / 3 / 0");
16383:   }
16384: 
16385:   menuCargar() {
```

## tests/guardas históricas QUESTS legacy

Fuente: `grulla-blanca_ver74.html` · líneas 25545-25590

```js
25545:   return {ok:fallos.length === 0, muestras:muestras.length, fallos};
25546: }
25547: 
25548: PRUEBAS.registrar("3C.1R: auditor de textos activos sin referencias funcionales retiradas", () => {
25549:   const r = auditarTextosActivos3C1R();
25550:   afirmar(r.ok, JSON.stringify(r.fallos));
25551: });
25552: PRUEBAS.registrar("3C.1R: auditor detecta regresiones sin bloquear términos genéricos", () => {
25553:   const prohibidos = [
25554:     "Anciana Kang", "Fan Ji", "mercader 8p",
25555:     "ESTUDIAR INJERTO en la biblioteca", "Estudia el injerto en la biblioteca",
25556:     "Medita en el estanque", "MEDITAR hacia el estanque",
25557:     '"biblioteca"', "'biblioteca'", '"estanque"', "'estanque'",
25558:     'this.quests["ratas"]', 'activarMision("jade")',
25559:   ];
25560:   for (const t of prohibidos)
25561:     afirmar(!auditarTextosActivos3C1R([t]).ok, "No detectó: " + t);
25562:   const permitidos = [
25563:     "estanque_riego", "una biblioteca que nadie recuerda llena", "ratas en la vegetación", "jade espiritual",
25564:     "Un canal trae agua al estanque y disipa parte de su fuerza antes de mezclarla con la reserva.",
25565:     "Un tramo de infraestructura de riego más antiguo que los canales visibles desciende junto al estanque hasta una obra de piedra.",
25566:     "La disposición favorece trabajo prolongado sin convertir el lugar en biblioteca ni archivo.",
25567:   ];
25568:   for (const t of permitidos)
25569:     afirmar(auditarTextosActivos3C1R([t]).ok, "Confundió término genérico con contenido retirado: " + t);
25570: });
25571: PRUEBAS.registrar("3C.1R: historial nuevo, normalización e ida y vuelta conservan hechos actuales", () => {
25572:   const j=PRUEBAS.banco();
25573:   afirmar(Object.keys(j.player.historialAcciones).sort().join() === "eventos,secuencia,version", "Esquema inesperado del historial");
25574:   j.registrarAccion("ROBAR", {clave:"prueba_3c1r",contexto:{recurso:"prueba"}});
25575:   const antes=JSON.stringify(j.player.historialAcciones);
25576:   j.player.historialAcciones.marcaRetirada = true;
25577:   j.normalizarHistorialAcciones(); afirmar(JSON.stringify(j.player.historialAcciones)===antes,"Alteró historial");
25578:   const copia=PRUEBAS.banco(); afirmar(copia.deserializar(JSON.parse(JSON.stringify(j.serializar()))),"No cargó save actual");
25579:   afirmar(JSON.stringify(copia.player.historialAcciones)===antes,"Perdió hechos actuales");
25580: });
25581: PRUEBAS.registrar("3C.1R: normalización no reinterpreta ramas ni acredita contribución externa", () => {
25582:   const j=PRUEBAS.banco(), p=j.player, tid=Object.keys(p.tecnicas)[0];
25583:   p.tecnicas[tid].ramas={1:1,2:2,3:0}; j.normalizarMeridianos();
25584:   afirmar(p.tecnicas[tid].ramas[1]===1 && p.tecnicas[tid].ramas[2]===2,"Reinterpretó ramas");
25585:   p.facciones.grulla_blanca.saldo=7;p.facciones.grulla_blanca.merito=12;p.contribucion=999;
25586:   j.normalizarFacciones();
25587:   afirmar(p.facciones.grulla_blanca.saldo===7 && p.facciones.grulla_blanca.merito===12 && p.contribucion===7,"Importó saldo externo");
25588: });
25589: 
25590: PRUEBAS.registrar("cultivo: CULTIVO_REINOS es coherente", () => {
```

