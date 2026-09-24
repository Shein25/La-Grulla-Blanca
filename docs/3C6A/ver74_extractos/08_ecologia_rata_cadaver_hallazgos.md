# Extracto 08 — 3C.4/rata/cadáver/HALLAZGOS

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## ERRANTES_INICIALES / ciclo base

Fuente: `grulla-blanca_ver74.html` · líneas 3662-3787

```js
03662: // pulsos ecológicos que tarda un mob no-único en volver a aparecer en su sala
03663: // tras ser derrotado. Se puede afinar por mob agregando `respawnCooldown` a su entrada
03664: // en MOBS (ej. rata_qi: { ..., respawnCooldown: 6 }); si no lo tiene, usa este default.
03665: const RESPAWN_COOLDOWN_DEFAULT = 10;
03666: const DURACION_OBJETO_TIRADO = 500;
03667: // Los restos son información ambiental, no una segunda fuente de botín.
03668: // Duran menos que el respawn común para que nunca se solapen con la nueva criatura.
03669: const DURACION_CADAVER = 6;
03670: 
03671: // ---------- MOBS ERRANTES: territorio fijo, se mueven entre comandos de movimiento ----------
03672: // array de instancias: para agregar un mob errante nuevo, solo hace falta sumar otra
03673: // entrada acá (con su propio `id`, mob, territorio y sala de origen). El motor
03674: // (actualizarErrantes/moverErrantes/entrarSala/recompensas) ya es genérico y no
03675: // necesita tocarse. La atracción QI/SANGRE consulta vecinos reales por separado.
03676: const PROB_MOVIMIENTO_ERRANTE = 0.28;
03677: const ERRANTES_INICIALES = [
03678:   {
03679:     "id": "lobo_madriguera",
03680:     "mobId": "lobo_espiritual",
03681:     "territorio": [
03682:       "bosque_paso_hundido",
03683:       "bosque_hondonada",
03684:       "bosque_corredor_viento"
03685:     ],
03686:     "origen": "bosque_hondonada",
03687:     "sala": "bosque_hondonada",
03688:     "muertoHasta": 0
03689:   },
03690:   {
03691:     "id": "rata_despensa",
03692:     "mobId": "rata_qi",
03693:     "territorio": [
03694:       "deposito_comun",
03695:       "tablon_encargos"
03696:     ],
03697:     "origen": "deposito_comun",
03698:     "sala": "deposito_comun",
03699:     "muertoHasta": 0
03700:   },
03701:   {
03702:     "id": "serpiente_bambu",
03703:     "mobId": "serpiente_qi",
03704:     "territorio": [
03705:       "bosque_claro_raices",
03706:       "bosque_sendero_bajo",
03707:       "bosque_puesto_marcas"
03708:     ],
03709:     "origen": "bosque_claro_raices",
03710:     "sala": "bosque_claro_raices",
03711:     "muertoHasta": 0
03712:   },
03713:   {
03714:     "id": "avispa_exploradora",
03715:     "mobId": "avispa_jade",
03716:     "territorio": [
03717:       "bosque_claro_humedo",
03718:       "bosque_pinos_torcidos",
03719:       "bosque_quebrada_niebla",
03720:       "bosque_loma_niebla"
03721:     ],
03722:     "origen": "bosque_claro_humedo",
03723:     "sala": "bosque_claro_humedo",
03724:     "muertoHasta": 0
03725:   },
03726:   {
03727:     "id": "macaco_rebuscador",
03728:     "mobId": "mono_pildoras",
03729:     "territorio": [
03730:       "bosque_claro_humedo",
03731:       "bosque_pinos_torcidos",
03732:       "bosque_quebrada_niebla",
03733:       "bosque_loma_niebla"
03734:     ],
03735:     "origen": "bosque_claro_humedo",
03736:     "sala": "bosque_claro_humedo",
03737:     "muertoHasta": 0
03738:   },
03739:   {
03740:     "id": "sapo_de_la_grieta",
03741:     "mobId": "sapo_ceniza",
03742:     "territorio": [
03743:       "camara_caldera",
03744:       "desvio_termal"
03745:     ],
03746:     "origen": "camara_caldera",
03747:     "sala": "camara_caldera",
03748:     "muertoHasta": 0
03749:   },
03750:   {
03751:     "id": "escarabajo_de_la_cuota",
03752:     "mobId": "escarabajo_hierro",
03753:     "territorio": [
03754:       "nido_escarabajos",
03755:       "camara_hierro",
03756:       "veta_negra"
03757:     ],
03758:     "origen": "veta_negra",
03759:     "sala": "veta_negra",
03760:     "muertoHasta": 0
03761:   },
03762:   {
03763:     "id": "pez_de_la_corriente",
03764:     "mobId": "pez_lunar",
03765:     "territorio": [
03766:       "aguas_inicio_barranco",
03767:       "aguas_poza_clara",
03768:       "aguas_terraza_humeda"
03769:     ],
03770:     "origen": "aguas_inicio_barranco",
03771:     "sala": "aguas_inicio_barranco",
03772:     "muertoHasta": 0
03773:   },
03774:   {
03775:     "id": "anguila_extraviada",
03776:     "mobId": "anguila_estelar",
03777:     "territorio": [
03778:       "aguas_manantial_partido",
03779:       "aguas_rama_oscura",
03780:       "aguas_cuenca_reunion"
03781:     ],
03782:     "origen": "aguas_manantial_partido",
03783:     "sala": "aguas_manantial_partido",
03784:     "muertoHasta": 0
03785:   },
03786:   {
03787:     "id": "devorador_de_paso",
```

## HALLAZGOS_CADAVER

Fuente: `grulla-blanca_ver74.html` · líneas 7250-7335

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
07316:         { id: "branquia", item: "branquia_lunar", cantidad: 1, dificultad: "dificil", metodo: "separar filamento branquial", pista: "Un filamento branquial separa agua y sedimento espiritual sin mezclarlos." },
07317:       ],
07318:     },
07319:     anguila_estelar: {
07320:       descripcion: "Una línea azul recorre su piel oscura como una grieta de luz apagada.",
07321:       pistas: "La línea azul que recorre su carne es un conducto verdadero; junto a él hay un saco donde se acumula la descarga que no pudo liberar.",
07322:       hallazgos: [
07323:         { id: "conducto", item: "conducto_estelar", cantidad: 1, dificultad: "normal", metodo: "extraer conducto estelar", pista: "La línea azul que recorre su carne es un conducto verdadero." },
07324:         { id: "saco_residual", item: "saco_residual_estelar", cantidad: 1, dificultad: "dificil", metodo: "sellar saco residual", pista: "Junto al conducto hay un saco donde se acumula la descarga que no pudo liberar." },
07325:       ],
07326:     },
07327:     halcon_tormenta: {
07328:       descripcion: "Plumas oscuras que todavía chisporrotean con una estática residual.",
07329:       pistas: "Las plumas superficiales sólo descargan el exceso. La energía útil corre por fibras profundas del ala y por una cámara pulmonar comprimida.",
07330:       hallazgos: [
07331:         { id: "fibra_ala", item: "fibra_tempestad", cantidad: 1, dificultad: "normal", metodo: "extraer fibra de tempestad", pista: "Las plumas superficiales sólo descargan el exceso; la energía útil corre por fibras profundas del ala." },
07332:         { id: "saco_pulmonar", item: "saco_pulmonar_tormenta", cantidad: 1, dificultad: "dificil", metodo: "aislar saco pulmonar", pista: "La energía útil también se comprime en una cámara pulmonar profunda." },
07333:       ],
07334:     },
07335:     devorador_niebla: {
```

## Examen/cadáver/profesión alrededor de HALLAZGOS

Fuente: `grulla-blanca_ver74.html` · líneas 19095-19360

```js
19095:     const siguiente = siguienteNivel === null ? null : UMBRALES_OFICIO[siguienteNivel];
19096:     const maxArco = PROFESIONES[id]?.rangoMaximoArco1 ?? (RANGOS_OFICIO.length - 1);
19097:     return {
19098:       nivel, nombre: RANGOS_OFICIO[nivel], xp, nivelPorXP,
19099:       siguiente, apto: siguiente !== null && xp >= siguiente && nivel < maxArco,
19100:       bloqueadoPorArco: siguiente !== null && xp >= siguiente && nivel >= maxArco,
19101:     };
19102:   }
19103: 
19104:   sumarExperienciaProfesion(id, cantidad) {
19105:     this.normalizarProfesiones();
19106:     const antes = this.rangoProfesion(id);
19107:     const oficio = this.player?.profesiones?.[id];
19108:     if (!oficio) return "";
19109:     oficio.xp += Math.max(0, Number(cantidad) || 0);
19110:     const despues = this.rangoProfesion(id);
19111:     if (!antes.apto && despues.apto)
19112:       return `${PROFESIONES[id].nombre}: experiencia suficiente para solicitar reconocimiento como ${RANGOS_OFICIO[despues.nivel + 1].toUpperCase()}.`;
19113:     return "";
19114:   }
19115: 
19116:   promoverProfesion(id) {
19117:     this.normalizarProfesiones();
19118:     if (!this.player?.profesiones?.[id] || !PROFESIONES[id]) return "Ese oficio no está registrado.";
19119:     const estado = this.rangoProfesion(id);
19120:     // rangoProfesion() normaliza y puede reconstruir el registro; toma SIEMPRE
19121:     // la referencia vigente después de consultarlo. Esta regla evita escribir
19122:     // sobre referencias sustituidas por una normalización.
19123:     const oficio = this.player.profesiones[id];
19124:     const maxArco = PROFESIONES[id].rangoMaximoArco1 ?? (RANGOS_OFICIO.length - 1);
19125:     if (estado.nivel >= maxArco) return `${PROFESIONES[id].nombre}: el rango superior requiere contenido de un arco posterior.`;
19126:     if (!estado.apto) {
19127:       const faltan = estado.siguiente === null ? 0 : Math.max(0, estado.siguiente - estado.xp);
19128:       return `${PROFESIONES[id].nombre}: aún faltan ${formatearXP(faltan)} XP para el próximo reconocimiento.`;
19129:     }
19130:     oficio.rango += 1;
19131:     this.autoguardar();
19132:     return `✦ ${PROFESIONES[id].nombre}: reconocido como ${RANGOS_OFICIO[oficio.rango].toUpperCase()}.`;
19133:   }
19134: 
19135:   probabilidadExamen(hallazgo, nivelRango = null) {
19136:     const dificultad = hallazgo?.dificultad || "normal";
19137:     const base = EXITO_BASE_EXAMEN[dificultad] ?? 0;
19138:     const nivel = nivelRango === null ? this.rangoProfesion("examen").nivel : Math.max(0, Number(nivelRango) || 0);
19139:     return Math.min(.90, base + (BONO_RANGO_EXAMEN[nivel] ?? BONO_RANGO_EXAMEN[BONO_RANGO_EXAMEN.length - 1] ?? 0));
19140:   }
19141: 
19142:   registroEspecieExamen(mobId, crear = true) {
19143:     this.normalizarProfesiones();
19144:     const oficio = this.player?.profesiones?.examen;
19145:     if (!oficio) return null;
19146:     let reg = oficio.descubrimientos[mobId];
19147:     if (!reg && crear) reg = oficio.descubrimientos[mobId] = { observaciones: 0, exitos: 0, procedimientos: {} };
19148:     if (reg === true) reg = oficio.descubrimientos[mobId] = { observaciones: 1, exitos: 0, procedimientos: {} };
19149:     if (!reg || typeof reg !== "object") return null;
19150:     reg.observaciones = Math.max(0, Math.floor(Number(reg.observaciones) || 0));
19151:     reg.exitos = Math.max(0, Math.floor(Number(reg.exitos) || 0));
19152:     reg.procedimientos ||= {};
19153:     return reg;
19154:   }
19155: 
19156:   familiaridadExamen(mobId) {
19157:     const reg = this.registroEspecieExamen(mobId, false);
19158:     if (!reg) return { nivel: 0, nombre: "Desconocida", observaciones: 0, exitos: 0, completos: 0, total: HALLAZGOS_CADAVER[mobId]?.hallazgos?.length || 0 };
19159:     const tabla = HALLAZGOS_CADAVER[mobId];
19160:     const ids = tabla?.hallazgos?.map(h => h.id) || [];
19161:     const completos = ids.filter(id => (reg.procedimientos[id] || 0) > 0).length;
19162:     let nivel = 1, nombre = "Observada";
19163:     if (reg.observaciones >= 2 || reg.exitos >= 2) { nivel = 2; nombre = "Estudiada"; }
19164:     if (reg.observaciones >= 6 && ids.length && completos === ids.length) { nivel = 3; nombre = "Comprendida"; }
19165:     return { nivel, nombre, observaciones: reg.observaciones, exitos: reg.exitos, completos, total: ids.length };
19166:   }
19167: 
19168:   registrarMaterialExamen(itemId, cantidad = 1) {
19169:     if (!this.player || ITEMS[itemId]?.tipo !== "material") return;
19170:     this.normalizarProfesiones();
19171:     const oficio = this.player.profesiones.examen;
19172:     const n = Math.max(1, Math.floor(Number(cantidad) || 1));
19173:     oficio.materiales[itemId] = (oficio.materiales[itemId] || 0) + n;
19174:     oficio.hallazgos[itemId] = (oficio.hallazgos[itemId] || 0) + n;
19175:     oficio.total = (oficio.total || 0) + n;
19176:   }
19177: 
19178:   procedimientoUsadoEnCadaver(cuerpo, hallazgo) {
19179:     cuerpo.examenProcedimientos ||= {};
19180:     if (cuerpo.examenProcedimientos[hallazgo.id]) return cuerpo.examenProcedimientos[hallazgo.id];
19181:     return null;
19182:   }
19183: 
19184:   cuerpoExamenAgotado(cuerpo) {
19185:     const tabla = HALLAZGOS_CADAVER[cuerpo.mob_id];
19186:     if (!tabla) return false;
19187:     return tabla.hallazgos.every(h => !!this.procedimientoUsadoEnCadaver(cuerpo, h));
19188:   }
19189: 
19190:   observarCadaver(indice = 0) {
19191:     const cuerpos = this.cadaveresEnSala();
19192:     const cuerpo = cuerpos[Number(indice) || 0];
19193:     if (!cuerpo) return { ok:false, texto:"No hay un cadáver fresco con ese número en esta sala." };
19194:     if (!this.profesionDesbloqueada("examen")) return { ok:false, texto:"Enseñanza de Examen pendiente de implementación canónica 3C." };
19195:     const tabla = HALLAZGOS_CADAVER[cuerpo.mob_id];
19196:     if (!tabla) return { ok:false, texto:"Este cuerpo no presenta una estructura que tu Extracción Espiritual pueda aprovechar." };
19197:     cuerpo.investigado ||= [];
19198:     cuerpo.examenProcedimientos ||= {};
19199:     const yaObservado = cuerpo.investigado.includes("observado");
19200:     if (!yaObservado) {
19201:       cuerpo.investigado.push("observado");
19202:       const especie = this.registroEspecieExamen(cuerpo.mob_id, true);
19203:       especie.observaciones += 1;
19204:       this.autoguardar();
19205:     }
19206:     return { ok:true, cuerpo, tabla, nuevo:!yaObservado };
19207:   }
19208: 
19209:   recolectarCadaver(indice = 0, metodo = "") {
19210:     const cuerpos = this.cadaveresEnSala();
19211:     const cuerpo = cuerpos[Number(indice) || 0];
19212:     if (!cuerpo) return "No hay un cadáver fresco con ese número en esta sala.";
19213:     if (!this.profesionDesbloqueada("examen")) return "Enseñanza de Examen pendiente de implementación canónica 3C.";
19214:     const tabla = HALLAZGOS_CADAVER[cuerpo.mob_id];
19215:     if (!tabla) return "Este cuerpo no presenta una estructura que tu Extracción Espiritual pueda aprovechar.";
19216:     cuerpo.investigado ||= [];
19217:     cuerpo.examenProcedimientos ||= {};
19218:     const accion = String(metodo || "").toLowerCase().replace(/_/g, " ").trim();
19219:     const oficio = this.player.profesiones.examen;
19220: 
19221:     // EXTRAER sólo acepta procedimientos anatómicos reales del cadáver.
19222:     // Observar el cuerpo es automático y gratuito al abrir la interfaz.
19223:     const hallazgo = tabla.hallazgos.find(h => accion === h.id || accion === h.id.replace(/_/g, " ") || accion.includes(h.metodo) || h.metodo.includes(accion));
19224:     if (!hallazgo) return "No reconoces un procedimiento compatible con esa estructura. Abre EXTRAER y elige una de las estructuras disponibles.";
19225:     this.observarCadaver(indice);
19226:     if (this.procedimientoUsadoEnCadaver(cuerpo, hallazgo)) return "Ese procedimiento ya fue intentado en este cadáver; la estructura no admite una segunda intervención.";
19227: 
19228:     this.turnoGlobal += 1;
19229:     this.registrarActividadReposo(1);
19230:     this.avanzarEcologia(1);
19231:     const afliccionesAccion = this.avanzarAflicciones(1);
19232:     oficio.cadaveres = (oficio.cadaveres || 0) + 1;
19233: 
19234:     const prob = this.probabilidadExamen(hallazgo);
19235:     const exito = Azar.random() <= prob;
19236:     if (exito) cuerpo.desapareceEn += 1; // compensa el turno de EXTRAER sólo al acertar.
19237:     cuerpo.examenProcedimientos[hallazgo.id] = exito ? "exito" : "fallo";
19238:     cuerpo.investigado.push(hallazgo.metodo);
19239:     if (!exito) {
19240:       const atraido = this.atraerHostilVecino("SANGRE");
19241:       this.autoguardar();
19242:       this.actualizarBarra(); this.actualizarPanel();
19243:       return `La intervención falla y arruina ${hallazgo.metodo}. No obtienes material: 0 XP. Esa estructura ya no puede intentarse en este cadáver.${atraido ? " La sangre atrae a " + atraido.name + "." : ""}${afliccionesAccion.length ? "\n" + afliccionesAccion.join("\n") : ""}`;
19244:     }
19245: 
19246:     const especie = this.registroEspecieExamen(cuerpo.mob_id, true);
19247:     const clave = `${cuerpo.mob_id}:${hallazgo.id}`;
19248:     const exitosPrevios = Math.max(0, Number(oficio.procedimientos[clave]) || 0);
19249:     const numeroExito = exitosPrevios + 1;
19250:     const xpPractica = xpPracticaPorDificultad("examen", hallazgo.dificultad, numeroExito);
19251:     const bonoEspecie = especie.exitos === 0 ? BONO_PRIMERA_ESPECIE_EXAMEN : 0;
19252:     const bonoProcedimiento = exitosPrevios === 0 ? BONO_PRIMER_PROCEDIMIENTO_EXAMEN : 0;
19253:     const xpTotal = xpPractica + bonoEspecie + bonoProcedimiento;
19254: 
19255:     oficio.procedimientos[clave] = numeroExito;
19256:     especie.exitos += 1;
19257:     especie.procedimientos[hallazgo.id] = (especie.procedimientos[hallazgo.id] || 0) + 1;
19258:     for (let i = 0; i < hallazgo.cantidad; i++) this.player.inventario.push(hallazgo.item);
19259:     this.registrarMaterialExamen(hallazgo.item, hallazgo.cantidad);
19260:     const avisoRango = this.sumarExperienciaProfesion("examen", xpTotal);
19261:     const fam = this.familiaridadExamen(cuerpo.mob_id);
19262: 
19263:     this.autoguardar();
19264:     this.actualizarBarra(); this.actualizarPanel();
19265:     const bonos = [bonoEspecie ? `+${bonoEspecie} especie nueva` : "", bonoProcedimiento ? `+${bonoProcedimiento} procedimiento nuevo` : ""].filter(Boolean);
19266:     const detalleXP = `+${formatearXP(xpTotal)} XP${bonos.length ? ` (${formatearXP(xpPractica)} práctica · ${bonos.join(" · ")})` : ` (${formatearXP(xpPractica)} práctica)`}`;
19267:     return `Extracción espiritual: obtienes ${hallazgo.cantidad} ${ITEMS[hallazgo.item].name} mediante ${hallazgo.metodo}. ${detalleXP}. Familiaridad: ${fam.nombre}.${avisoRango ? " " + avisoRango : ""}${afliccionesAccion.length ? "\n" + afliccionesAccion.join("\n") : ""}`;
19268:   }
19269: 
19270:   probabilidadHerboristeria(procedimiento, nivelRango = null) {
19271:     const dificultad = procedimiento?.dificultad || "normal";
19272:     const base = EXITO_BASE_HERBORISTERIA[dificultad] ?? 0;
19273:     const nivel = nivelRango === null ? this.rangoProfesion("herboristeria").nivel : Math.max(0, Number(nivelRango) || 0);
19274:     return Math.min(.90, base + (BONO_RANGO_HERBORISTERIA[nivel] ?? BONO_RANGO_HERBORISTERIA[BONO_RANGO_HERBORISTERIA.length - 1] ?? 0));
19275:   }
19276: 
19277:   estadoNodoHerboristeria(nodoId, crear = true) {
19278:     this.normalizarProfesiones();
19279:     const oficio = this.player?.profesiones?.herboristeria;
19280:     if (!oficio || !NODOS_HERBORISTERIA[nodoId]) return null;
19281:     let st = oficio.nodos[nodoId];
19282:     if (!st && crear) st = oficio.nodos[nodoId] = { partes:{}, observaciones:0, exitos:0, cambios:0, cambioObservado:-1, muertaHasta:0 };
19283:     if (!st) return null;
19284:     st.partes ||= {};
19285:     st.observaciones = Math.max(0, Math.floor(Number(st.observaciones) || 0));
19286:     st.exitos = Math.max(0, Math.floor(Number(st.exitos) || 0));
19287:     st.cambios = Math.max(0, Math.floor(Number(st.cambios) || 0));
19288:     st.cambioObservado = Number.isFinite(Number(st.cambioObservado)) ? Math.max(-1, Math.floor(Number(st.cambioObservado))) : -1;
19289:     st.muertaHasta = Math.max(0, Number(st.muertaHasta) || 0);
19290:     return st;
19291:   }
19292: 
19293:   plantasEnSala(rid = this.pos) {
19294:     return Object.entries(NODOS_HERBORISTERIA)
19295:       .filter(([, nodo]) => !!ROOMS[nodo.sala] && !nodo.pendiente && nodo.sala === rid)
19296:       .map(([id, nodo]) => ({ id, ...nodo, planta: PLANTAS_ESPIRITUALES[nodo.especie] }))
19297:       .filter(reg => !!reg.planta);
19298:   }
19299: 
19300:   registroEspecieHerboristeria(especieId, crear = true) {
19301:     this.normalizarProfesiones();
19302:     const oficio = this.player?.profesiones?.herboristeria;
19303:     if (!oficio || !PLANTAS_ESPIRITUALES[especieId]) return null;
19304:     let reg = oficio.especies[especieId];
19305:     if (!reg && crear) reg = oficio.especies[especieId] = { observaciones:0, exitos:0, procedimientos:{} };
19306:     if (!reg || typeof reg !== "object") return null;
19307:     reg.observaciones = Math.max(0, Math.floor(Number(reg.observaciones) || 0));
19308:     reg.exitos = Math.max(0, Math.floor(Number(reg.exitos) || 0));
19309:     reg.procedimientos ||= {};
19310:     return reg;
19311:   }
19312: 
19313:   familiaridadHerboristeria(especieId) {
19314:     const reg = this.registroEspecieHerboristeria(especieId, false);
19315:     const planta = PLANTAS_ESPIRITUALES[especieId];
19316:     const principales = planta?.procedimientos?.filter(p => p.principal).map(p => p.id) || [];
19317:     if (!reg) return { nivel:0, nombre:"Desconocida", observaciones:0, exitos:0, completos:0, total:principales.length };
19318:     const completos = principales.filter(id => (reg.procedimientos[id] || 0) > 0).length;
19319:     let nivel = 1, nombre = "Observada";
19320:     if (reg.observaciones >= 2 || reg.exitos >= 2) { nivel = 2; nombre = "Estudiada"; }
19321:     if (reg.observaciones >= 6 && principales.length && completos === principales.length) { nivel = 3; nombre = "Comprendida"; }
19322:     return { nivel, nombre, observaciones:reg.observaciones, exitos:reg.exitos, completos, total:principales.length };
19323:   }
19324: 
19325:   registrarMaterialHerboristeria(itemId, cantidad = 1) {
19326:     if (!this.player || ITEMS[itemId]?.tipo !== "material") return;
19327:     this.normalizarProfesiones();
19328:     const oficio = this.player.profesiones.herboristeria;
19329:     const n = Math.max(1, Math.floor(Number(cantidad) || 1));
19330:     oficio.materiales[itemId] = (oficio.materiales[itemId] || 0) + n;
19331:     oficio.total = (oficio.total || 0) + n;
19332:   }
19333: 
19334:   nodoHerboristeriaAgotado(nodo) {
19335:     const fam = this.familiaridadHerboristeria(nodo.especie);
19336:     if (fam.observaciones <= 0) return false; // nunca ocultar antes del primer EXAMINAR
19337:     return nodo.planta.procedimientos.every(p => !this.estadoPartePlanta(nodo.id, p).disponible);
19338:   }
19339: 
19340:   estadoPartePlanta(nodoId, procedimiento) {
19341:     const st = this.estadoNodoHerboristeria(nodoId, true);
19342:     if (!st) return { disponible:false, espera:0, planta:false };
19343:     const ahora = this.turnoGlobal;
19344:     if (st.muertaHasta > ahora) return { disponible:false, espera:Math.ceil(st.muertaHasta - ahora), planta:false };
19345:     const hasta = Math.max(0, Number(st.partes[procedimiento.id]) || 0);
19346:     return { disponible:hasta <= ahora, espera:Math.max(0, Math.ceil(hasta - ahora)), planta:true };
19347:   }
19348: 
19349:   recolectarPlanta(indice = 0, metodo = "examinar") {
19350:     const plantas = this.plantasEnSala();
19351:     const nodo = plantas[Number(indice) || 0];
19352:     if (!nodo) return "No hay una planta espiritual con ese número en esta sala.";
19353:     if (!this.profesionDesbloqueada("herboristeria")) return "Herboristería no está habilitada para este personaje.";
19354:     const planta = nodo.planta;
19355:     const estado = this.estadoNodoHerboristeria(nodo.id, true);
19356:     const accion = String(metodo || "examinar").toLowerCase().replace(/_/g, " ").trim();
19357:     const oficio = this.player.profesiones.herboristeria;
19358: 
19359:     if (accion === "examinar" || accion === "observar" || accion === "mirar") {
19360:       const especie = this.registroEspecieHerboristeria(nodo.especie, true);
```

## respawn/errantes/cadáveres runtime (contexto)

Fuente: `grulla-blanca_ver74.html` · líneas 16600-16735

```js
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
16621:       e.sala = e.origen;
16622:       e.muertoHasta = 0;
16623:       e.desde = null;
16624:       e.movidoEn = this.turnoGlobal;
16625:     }
16626:   }
16627: 
16628:   actualizarErrantes() {
16629:     for (const e of this.errantes || []) this.actualizarErrante(e);
16630:   }
16631: 
16632:   moverErrante(e) {
16633:     this.actualizarErrante(e);
16634:     if (e.muertoHasta > 0) return; // en cooldown: no vaga
16635:     if (Azar.random() >= PROB_MOVIMIENTO_ERRANTE) return; // no le tocó moverse este turno
16636:     const salaActual = ROOMS[e.sala];
16637:     if (!salaActual) return;
16638:     const vecinos = Object.values(salaActual.exits || {}).filter(d => e.territorio.includes(d));
16639:     if (!vecinos.length) return;
16640:     const anterior = e.sala;
16641:     e.sala = vecinos[Math.floor(Azar.random() * vecinos.length)];
16642:     e.desde = anterior;
16643:     e.movidoEn = this.turnoGlobal;
16644:   }
16645: 
16646:   moverErrantes() {
16647:     const area = ROOMS[this.pos]?.area;
16648:     if (!area) return;
16649:     for (const e of this.errantes || []) {
16650:       if (ROOMS[e.sala]?.area === area && e.territorio?.every(id => ROOMS[id]?.area === area)) this.moverErrante(e);
16651:     }
16652:   }
16653: 
16654:   venaActual(sala) {
16655:     if (sala.vena === "resentida" && this.flags.muerto_eco_caido) return VENAS.normal;
16656:     return VENAS[sala.vena] || VENAS.normal;
16657:   }
16658: 
16659:   // ---------- vitales ----------
16660: 
16661:   entrarSala() {
16662:     const sala = this.rooms[this.pos];
16663:     this.vivos = [];
16664:     this._huboMobsEnCooldown = false;
16665:     const ordinalFijo = {};
16666:     for (const mid of sala.mobs || []) {
16667:       const plant = MOBS[mid];
16668:       ordinalFijo[mid] = (ordinalFijo[mid] || 0) + 1;
16669:       const fijoId = `${this.pos}:${mid}:${ordinalFijo[mid]}`;
16670:       if (plant.unico && this.flags["muerto_" + mid]) continue;
16671:       if (!plant.unico) {
16672:         const claveVieja = this.pos + ":" + mid;
16673:         const espera = [this.respawnEn[fijoId], this.respawnEn[claveVieja]].filter(v => v !== undefined);
16674:         if (espera.some(listo => this.relojEcologico < listo)) { this._huboMobsEnCooldown = true; continue; }
16675:       }
16676:       this.vivos.push(crearMob(mid, plant, { fijoId }));
16677:     }
16678:     // mobs errantes: viven fuera de las listas fijas, se materializan según su ubicación actual
16679:     for (const errante of this.errantes || []) {
16680:       if (!errante.territorio.includes(this.pos)) continue;
16681:       this.actualizarErrante(errante);
16682:       if (errante.muertoHasta === 0 && errante.sala === this.pos) {
16683:         this.vivos.push(crearMob(errante.mobId, MOBS[errante.mobId], {
16684:           erranteId: errante.id,
16685:           erranteDesde: errante.desde,
16686:           erranteMovidoEn: errante.movidoEn,
16687:         }));
16688:       } else if (errante.muertoHasta > 0) {
16689:         this._huboMobsEnCooldown = true;
16690:       }
16691:     }
16692:     const totales = {};
16693:     for (const mob of this.vivos) totales[mob.mob_id] = (totales[mob.mob_id] || 0) + 1;
16694:     const vistos = {};
16695:     for (const mob of this.vivos) {
16696:       mob.indice_especie = (vistos[mob.mob_id] || 0) + 1;
16697:       vistos[mob.mob_id] = mob.indice_especie;
16698:       mob.total_especie = totales[mob.mob_id];
16699:     }
16700:     this.mostrarSala();
16701:     this.visitadas.add(this.pos);
16702: 
16703:     this.recordarAtlas();
16704:     this.actualizarMinimapa();
16705:     this.actualizarPanel();
16706:   }
16707: 
16708:   mostrarSala() {
16709:     const sala = this.rooms[this.pos];
16710:     // El marco del título lleva el color del área. Se estampa en cada línea porque el
16711:     // registro conserva los títulos anteriores: no deben cambiar al viajar.
16712:     aplicarAreaUI(this.addLine(sala.name, "titulo"), areaDeSala(this.pos));
16713:     const plantasSala = this.plantasEnSala();
16714:     const todasAgotadas = plantasSala.length > 0 && plantasSala.every(n => this.nodoHerboristeriaAgotado(n));
16715:     this.addLine((todasAgotadas && sala.descAgotada) ? sala.descAgotada : sala.desc, "descripcion-sala");
16716:     for (const det of sala.detalles || []) {
16717:       if (this.cumple(det.req || {})) this.addLine(det.text, "detalle-sala");
16718:     }
16719:     if (this.tieneSentido() && sala.sentido) this.addLine(`(sentido divino) ${sala.sentido}`, "sentido");
16720:     const items = this.itemsNaturalesVisibles();
16721:     if (items.length) {
16722:       this.addLine("Ves: " + agruparObjetos(items).map(({ mid, cantidad }) => capitalizarUI(nombreCantidad(mid, cantidad))).join(", "), "sala-meta sala-objetos");
16723:     }
16724:     const plantas = plantasSala.filter(n => !this.nodoHerboristeriaAgotado(n));
16725:     if (plantas.length) {
16726:       const nombres = plantas.map(n => {
16727:         const st = this.estadoNodoHerboristeria(n.id, true);
16728:         const espera = Math.max(0, Math.ceil((st?.muertaHasta || 0) - this.turnoGlobal));
16729:         return `${capitalizarUI(n.planta.nombre)}${espera ? ` (regenerando: ${espera})` : ""}`;
16730:       });
16731:       this.addLine("Plantas: " + nombres.join(", "), "sala-meta sala-plantas");
16732:     }
16733:     const tirados = this.resumenObjetosTirados();
16734:     if (tirados.length) {
16735:       this.addLine("En el suelo: " + tirados.join(", "), "sala-meta sala-objetos");
```

## DURACION_CADAVER

```js
03669: const DURACION_CADAVER = 6;
16873:       desapareceEn: this.turnoGlobal + DURACION_CADAVER,
26650:   for (let i = 0; i < DURACION_CADAVER + 5; i++) j.ejecutar("nada_de_esto_existe", []);
26652:   if (despues !== antes) return [`${antes} cadáver(es) antes, ${despues} después de ${DURACION_CADAVER + 5} órdenes inválidas`];
```

## RESPAWN_COOLDOWN

```js
03665: const RESPAWN_COOLDOWN_DEFAULT = 10;
16946:       const cd = (MOBS[mobId] && MOBS[mobId].respawnCooldown) || RESPAWN_COOLDOWN_DEFAULT;
```

## muertoHasta references

```js
02412:       if(has(e,"desde")&&e.desde!==null&&!base.territorio.includes(e.desde))fail('errante.desde');num(e.muertoHasta,'errante.muertoHasta');if(has(e,"movidoEn"))integer(e.movidoEn,'errante.movidoEn',-1);}
03688:     "muertoHasta": 0
03699:     "muertoHasta": 0
03711:     "muertoHasta": 0
03724:     "muertoHasta": 0
03737:     "muertoHasta": 0
03748:     "muertoHasta": 0
03760:     "muertoHasta": 0
03772:     "muertoHasta": 0
03784:     "muertoHasta": 0
03796:     "muertoHasta": 0
03810:     "muertoHasta": 0
16597:     const presentes = (this.errantes || []).filter(e => e.muertoHasta === 0 && e.sala === this.pos);
16619:     if (e.muertoHasta > 0 && this.relojEcologico >= e.muertoHasta) {
16622:       e.muertoHasta = 0;
16634:     if (e.muertoHasta > 0) return; // en cooldown: no vaga
16682:       if (errante.muertoHasta === 0 && errante.sala === this.pos) {
16688:       } else if (errante.muertoHasta > 0) {
16951:         errante.muertoHasta = this.relojEcologico + cd;
25020:         if (errante.sala !== destino || errante.muertoHasta !== 0) continue;
25046:       if (!errante || errante.mobId !== candidato.mobId || errante.sala !== candidato.roomOrigen || errante.muertoHasta !== 0) return null;
25222:   je.errantes.find(x=>x.id===ce.erranteId).muertoHasta=je.relojEcologico+10;
25269:   const e=remote[0][0]; e.muertoHasta=j.relojEcologico+1; j.relojEcologico+=1; j.actualizarErrantes();
25270:   afirmar(e.muertoHasta===0,"cooldown remoto no avanzó");
25391:     j.errantes[0].muertoHasta=12;j.errantes[0].desde=null;j.errantes[0].movidoEn=19;
```

