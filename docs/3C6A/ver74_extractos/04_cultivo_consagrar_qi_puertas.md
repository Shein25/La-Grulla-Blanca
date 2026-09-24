# Extracto 04 — Cultivo/CONSAGRAR/qi/puertas

Fuente exacta: `grulla-blanca_ver74.html`

SHA-256 fuente: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Los prefijos numéricos son números de línea del archivo fuente original. Extracto de sólo lectura para auditoría 3C.6A.

## VASO_ETAPA / PUERTAS

Fuente: `grulla-blanca_ver74.html` · líneas 3105-3135

```js
03105: // probabilidad, por ronda, de que un hostil suelto en la sala (no trabado todavía)
03106: // se sume al combate en curso. Acordado en el rango 5–15% para no abrumar.
03107: const PROB_UNION_COMBATE = 0.10;
03108: 
03109: // ---------- PACING: vaso y puertas de etapa ----------
03110: const VASO_ETAPA = { 1: 25, 2: 45, 3: 75, 4: 110 };
03111: 
03112: const PUERTAS = {
03113:   2: null,
03114:   3: { pildoras: 1, logros: ["combate"] },
03115:   4: { pildoras: 2, logros: ["comprension:6"] },
03116: };
03117: // umbral de comprensión que reemplaza a la Píldora de Fundación en el cuello de
03118: // botella (etapa 4 de LianQi, qi al tope). Ver puedeIntentar() y progresoFundacion().
03119: const UMBRAL_COMPRENSION_FUNDACION = 10;
03120: 
03121: /* ======================================================================
03122:    CONTRATO DE MOTOR · HISTORIAL DE ACCIONES
03123: 
03124:    Las decisiones narrativas importantes se registran como ACCIONES
03125:    CANÓNICAS independientes del contenido que las originó. El objetivo es que
03126:    Iluminación, Tribulación y sistemas futuros puedan recordar lo que hizo el
03127:    personaje aunque cambien o desaparezcan NPC, misiones, diálogos o escenas.
03128: 
03129:    REGLAS DE ARQUITECTURA
03130:    1) El contenido puede llamar registrarAccion(); el motor espiritual consulta
03131:       obtenerAcciones()/tieneAccion(), nunca flags de un NPC o misión concreta.
03132:    2) Una acción registra HECHOS, no moralidad ni afinidad de Dao. Prohibido
03133:       guardar aquí puntos de libertad/protección/etc. Esa interpretación ocurre
03134:       después, durante una reflexión del jugador.
03135:    3) contexto/consecuencias usan conceptos generales (rival derrotado, memoria,
```

## compruebaPuerta / progresoFundacion

Fuente: `grulla-blanca_ver74.html` · líneas 17140-17188

```js
17140:     if (tiene < puerta.pildoras) {
17141:       faltan.push(`${puerta.pildoras - tiene} píldoras de consolidación`);
17142:     }
17143:     const L = this.logros();
17144:     for (const req of puerta.logros) {
17145:       if (req === "combate" && L.combate < 1) faltan.push("haber ganado un combate");
17146:       if (req.startsWith("comprension:")) {
17147:         const min = parseInt(req.split(":")[1], 10);
17148:         if (L.comprension < min) faltan.push(`comprensión ${min} (tienes ${L.comprension})`);
17149:       }
17150:     }
17151:     return { ok: faltan.length === 0, faltan };
17152:   }
17153: 
17154:   // Resumen legible de qué falta para avanzar de etapa dentro de LianQi, o para
17155:   // establecer la Fundación (ZhuJi) una vez en el cuello de botella. Se usa en
17156:   // HOJA y en el aviso de MEDITAR, para que el umbral (10 de comprensión, o la
17157:   // Píldora de Fundación) sea siempre el mismo número visible en ambos lados.
17158:   progresoFundacion() {
17159:     const p = this.player;
17160:     if (!reinoExacto(p, "LianQi")) return null;
17161:     if (p.etapa < 4) {
17162:       const siguiente = p.etapa + 1;
17163:       const { ok, faltan } = this.compruebaPuerta(siguiente);
17164:       return {
17165:         titulo: `Próxima puerta: Etapa ${siguiente}/${totalEtapas(p.reino)}`,
17166:         detalle: ok ? "Requisitos cumplidos. MEDITA con el qi al tope para cruzar." : "Falta: " + faltan.join(" · ") + ".",
17167:       };
17168:     }
17169:     const tienePildora = p.inventario.includes("pildora_fundacion");
17170:     const faltaComprension = Math.max(0, UMBRAL_COMPRENSION_FUNDACION - p.comprension);
17171:     const listo = tienePildora || faltaComprension === 0;
17172:     return {
17173:       titulo: "Cuello de botella: Establecimiento de Fundación",
17174:       detalle: listo
17175:         ? "Requisitos cumplidos. MEDITA con el qi al tope para intentar la tribulación."
17176:         : `Falta: la Píldora de Fundación o comprensión ${UMBRAL_COMPRENSION_FUNDACION} (tienes ${p.comprension}).`,
17177:     };
17178:   }
17179: 
17180:   registroLogro(tipo) {
17181:     this.flags["logro_" + tipo] = (this.flags["logro_" + tipo] || 0) + 1;
17182:   }
17183: 
17184:   logros() {
17185:     return {
17186:       combate: this.flags["logro_combate"] || 0,
17187:       comprension: this.player ? this.player.comprension : 0,
17188:     };
```

## aprenderManual / cmd_meditar / CONSAGRAR

Fuente: `grulla-blanca_ver74.html` · líneas 20068-20230

```js
20068:   
20069: 
20070:   aprenderManual(mid) {
20071:     const it = ITEMS[mid];
20072:     const tid = it.tecnica;
20073:     const t = TECNICAS[tid];
20074:     if (!t) return [[`Lees ${it.name}... escritura ilegible para ti.`], false];
20075:     if (!cumpleRequisitoReino(this.player, t.req)) {
20076:       return [[`Abres el ${it.name}... y el pergamino ARAÑA: exige un qi de reino ${t.req.reino} para siquiera dejarse leer.`], false];
20077:     }
20078:     if (tid in this.player.tecnicas) return [["Ya conoces esa técnica."], false];
20079:     this.player.inventario.splice(this.player.inventario.indexOf(mid), 1);
20080:     this.player.tecnicas[tid] = { maestria: 0, usos: 0, practica: 0, ramas: { 1: 0, 2: 0, 3: 0 } };
20081:     this.mostrarAprendizajeManual(mid, tid);
20082:     return [[], true];
20083:   }
20084: 
20085:   // ---------- MEDITAR (con puertas de etapa) ----------
20086: 
20087:   cmd_meditar(args) {
20088:     const p = this.player, r = RAICES[p.raiz];
20089:     const profundo = !!(args && args.some(a => a.includes("profund") || a === "hondo"));
20090:     const sala = this.rooms[this.pos];
20091:     const vena = this.venaActual(sala);
20092: 
20093:     if (this.vivos.some(m => m.hp > 0)) {
20094:       return "Con algo moviéndose en la sala, la quietud no llega. (Resuélvelo primero.)";
20095:     }
20096: 
20097:     const out = ["Te sientas con la espalda recta. El aliento se vuelve lento; el mundo, leve."];
20098:     out.push(...this.avanzarAflicciones(1));
20099: 
20100:     if (p.qi >= p.qi_max) {
20101:       if (!CULTIVO_REINOS[p.reino]?.jugable) {
20102:         // Reino ya alcanzado pero sin mecánica jugable todavía (ZhuJi en
20103:         // adelante: Arco 2+ no implementado). No hay puerta que cruzar ni
20104:         // stats que ganar acá — evita que tocar el tope se explote para
20105:         // subir stats infinitamente en un reino sin contenido real.
20106:         out.push(`Tu qi toca el techo de tu cultivo en ${p.reino}. Su desarrollo pertenece a un arco todavía no implementado.`);
20107:         this.salida(out.join("\n"));
20108:         return;
20109:       }
20110:       if (!reinoExacto(p, "LianQi") || p.etapa < totalEtapas("LianQi")) {
20111:         const siguiente = p.etapa + 1;
20112:         const puerta = this.compruebaPuerta(reinoExacto(p, "LianQi") ? siguiente : 99);
20113:         if (reinoExacto(p, "LianQi") && !puerta.ok) {
20114:           out.push("El vaso está lleno. Intentas que el qi se asiente... y algo se niega a ceder.");
20115:           out.push("Algo falta. El qi está, la voluntad también. La montaña no te deja pasar todavía.");
20116:           out.push("Te falta: " + puerta.faltan.join(" · ") + ".");
20117:           this.salida(out.join("\n"));
20118:           return;
20119:         }
20120:         const pt = reinoExacto(p, "LianQi") ? PUERTAS[siguiente] : null;
20121:         if (pt && pt.pildoras) {
20122:           for (let i = 0; i < pt.pildoras; i++) {
20123:             const idx = p.inventario.indexOf("pildora_consolidacion");
20124:             if (idx >= 0) p.inventario.splice(idx, 1);
20125:           }
20126:         }
20127:         const maxHpAnterior = p.max_hp;
20128:         const ataqueAnterior = p.ataque;
20129:         const vasoAnterior = p.qi_max;
20130:         p.qi = Math.max(0, p.qi - vasoAnterior);
20131:         p.etapa = Math.min(4, p.etapa + 1);
20132:         p.qi_max = reinoExacto(p, "LianQi") ? VASO_ETAPA[p.etapa] : vasoAnterior + 20;
20133:         p.max_hp += 4;
20134:         p.ataque += 1;
20135:         p.hp = Math.max(1, Math.round(p.max_hp * 0.6));
20136:         const puntosGanados = this.sincronizarPuntosTecnica();
20137:         this.registrarActividadReposo();
20138:         this.intentarPulsoMeditacion();
20139:         this.salida(out.join("\n"));
20140:         this.mostrarConsagracion({ maxHpAnterior, ataqueAnterior, puntosGanados });
20141:         this.actualizarPanel();
20142:         return;
20143:       } else {
20144:         out.push("Tu qi ha tocado el TOPE DEL TOPE de LianQi: el cuello de botella.");
20145:         // Cadena del final del Arco 1. El orden lo deciden los helpers, nunca
20146:         // comparaciones sueltas: Gran Perfección → Iluminación → Tribulación →
20147:         // Fundación. Cada paso se dispara al MEDITAR con el vaso al tope.
20148:         if (puedeAlcanzarGranPerfeccion(p)) {
20149:           this.registrarActividadReposo();
20150:           this.intentarPulsoMeditacion();
20151:           this.salida(out.join("\n"));
20152:           this.alcanzarGranPerfeccion();
20153:           return;
20154:         }
20155:         if (puedeBuscarIluminacion(p)) {
20156:           this.registrarActividadReposo();
20157:           this.intentarPulsoMeditacion();
20158:           this.salida(out.join("\n"));
20159:           this.iniciarIluminacion();
20160:           return;
20161:         }
20162:         if (puedeIniciarTribulacion(p)) {
20163:           this.registrarActividadReposo();
20164:           this.intentarPulsoMeditacion();
20165:           this.salida(out.join("\n"));
20166:           this.iniciarTribulacionCorazon();
20167:           return;
20168:         }
20169:         if (this.puedeIntentar()) {
20170:           this.registrarActividadReposo();
20171:           this.intentarPulsoMeditacion();
20172:           this.salida(out.join("\n"));
20173:           this.triunfoZhuji();
20174:           return;
20175:         }
20176:         out.push(`Necesitas: la Píldora de Fundación o comprensión ${UMBRAL_COMPRENSION_FUNDACION} (tienes ${p.comprension}). Consulta HOJA para ver el detalle.`);
20177:       }
20178:       this.salida(out.join("\n"));
20179:       return;
20180:     }
20181: 
20182:     if (vena.diente) {
20183:       out.push("El qi pisoteado rehúye tu respiración. A veces muerde.");
20184:       if (Azar.random() < PROB_MORDIDA) {
20185:         const d = 1 + Math.floor(Azar.random() * 2);
20186:         p.hp = Math.max(1, p.hp - d);
20187:         out.push(`Un hilo de qi resentido te muerde los meridianos: ${d} de daño. La sala no te quiere.`);
20188:       }
20189:       this.salida(out.join("\n"));
20190:       return;
20191:     }
20192:     const base = Math.round(r.qi_med * vena.mult);
20193:     if (base === 0) {
20194:       this.salida(out.join("\n"));
20195:       this.mostrarQiAgotado("vacia");
20196:       return;
20197:     }
20198: 
20199:     const satIdx = Math.min(this.saturacionDe(this.pos), SATURACION_MULT.length - 1);
20200:     const sat = SATURACION_MULT[satIdx];
20201:     if (sat === 0) {
20202:       this.salida(out.join("\n"));
20203:       this.mostrarQiAgotado("agotada");
20204:       return;
20205:     }
20206: 
20207:     this.registrarActividadReposo();
20208: 
20209:     if (sala.salvaje) {
20210:       const mob = this.atraerHostilVecino("QI");
20211:       if (mob) {
20212:         out.push("Cierras los ojos... y la maleza cruje a tu espalda.");
20213:         out.push("¡" + mob.name + " interrumpe tu meditación!");
20214:         return out.join("\n");
20215:       }
20216:     }
20217: 
20218:     const anillo = p.equipado.dedo === "anillo" ? 1 : 0;
20219:     const metodo = p.metodo ? 1 : 0;
20220:     let ganancia = Math.max(1, Math.round(base * sat)) + anillo + metodo;
20221:     const heridas = p.heridas_meridianos || 0;
20222:     if (heridas > 0) {
20223:       ganancia = Math.max(1, ganancia - heridas);
20224:       out.push(`Los meridianos heridos estrechan la circulación: −${heridas} qi por meditación.`);
20225:     }
20226: 
20227:     if (sala.vena === "rica") {
20228:       out.push(sala.purificaMeditacion
20229:         ? "El qi se posa en la superficie como polen. Aquí solo hay que abrir la boca."
20230:         : "El qi dorado del bambú entra contigo, denso como agua clara.");
```

## Escrituras directas a `p.qi` encontradas

```js
15048:             p.qi -= conf.coste;
15064:                 p.qi = Math.min(p.qi_max, p.qi + devuelto);
15078:               p.qi -= drenado;
15211:       p.qi += absorcion;
15436:         p.qi -= drenado;
16919:       p.qi = Math.min(p.qi + e.qi_recompensa, p.qi_max);
17194:     if (qi) { const antes = p.qi; p.qi = Math.min(p.qi + qi, p.qi_max); out.push(`   +${p.qi - antes} qi.`); }
19825:     p.qi = Math.min(p.qi_max, p.qi + Math.ceil(p.qi_max * 0.5));
20025:       p.qi = Math.min(p.qi_max, p.qi + it.recupera_qi);
20130:         p.qi = Math.max(0, p.qi - vasoAnterior);
20242:         p.qi = Math.max(0, p.qi - perdida);
20255:     p.qi = Math.min(p.qi_max, p.qi + ganancia);
20533:     p.qi_max = 140; p.qi = 70;
25692:   p.etapa = 3; p.qi = 61; p.qi_max = VASO_ETAPA[3]; p.comprension = 7;
25759:   p.etapa = 2; p.qi = 0;
25880:   p.etapa = 4; p.qi_max = VASO_ETAPA[4]; p.qi = VASO_ETAPA[4];
25909:   p.etapa = 4; p.qi_max = VASO_ETAPA[4]; p.qi = VASO_ETAPA[4];
```

