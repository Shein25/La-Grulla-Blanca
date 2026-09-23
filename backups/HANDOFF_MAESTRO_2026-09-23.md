# HANDOFF MAESTRO — LA GRULLA BLANCA

**Fecha de snapshot:** 2026-09-23  
**Propósito:** permitir retomar el proyecto con seguridad aunque se pierda la conversación de ChatGPT.

## 1. Regla principal de continuidad

Jerarquía general:

1. decisiones humanas explícitas posteriores;
2. fuentes canónicas vigentes del proyecto;
3. matrices/auditorías reconciliadas y aprobadas;
4. propuestas históricas sólo como contexto.

Nunca inventar conexiones, room IDs, gates, estados, NPC, resultados de misión o comportamiento ausente de las fuentes.

La versión corregida `Auditoria_4B_Movilidad_Postas_Carruajes_CORREGIDA.md` es la 4B válida. La anterior queda obsoleta.

## 2. Baseline técnico vigente

`grulla-blanca_ver72a.html`

SHA-256:

`5fa5306940dba5c9c829b67b4e59bd03d1a9e0153aa8bd7ec1dd707c56f70820`

`SAVE_SCHEMA_VERSION = 2`

`ver71` es histórico y `ver72` fue superado por `ver72a`.

## 3. Invariantes congelados del mundo

- 329 salas.
- 17 áreas.
- 787 salidas dirigidas.
- 786 internas + 1 externa.
- 0 reciprocidades rotas.
- 0 salas aisladas.
- 1 componente físico.
- 329 alcanzables ignorando gates.
- 185 inicialmente alcanzables.
- 144 inicialmente bloqueadas.
- 63 articulation rooms.
- 70 bridges.
- 13 alojamientos.
- 6 atajos de Primera Ala.

Bloqueo inicial:
- primera_ala 41
- alturas 20
- archivos 16
- formaciones 17
- secta_interior 22
- mantenimiento 15
- nucleo 13

Invariante:

`SECTA_INTERIOR=false => M12=false => todos ATAJO_ALA_* false`

Los gates nunca modifican `ROOMS.exits`.

Deep links:
- `ala_umbral_mantenimiento.abajo ↔ mantenimiento_acceso.arriba`
- `mantenimiento_compuerta_nucleo.abajo ↔ nucleo_pozo_voto.arriba`
- `nucleo_archivo_promesa.abajo ↔ nucleo_descenso_pulso.arriba`

No introducir tiempo diegético basado en fechas, horas, día/noche, amanecer o estaciones en prosa de juego/Atlas.

## 4. Roadmap

Cerrado:
- PRE-3C
- 3C.1
- 3C.1R
- 3C.1B
- 3C.2
- 3C.3A
- 3C.4

Pendiente/en curso:
- 3C.3B — integración Atlas
- 3C.5 — NPC
- 3C.6 — Prólogo + M01–M07
- 3C.7 — M08–M15
- 3C.8 — M16
- 3C.9 — M17 + M18 + epílogo
- 3C.10 — cleanup + regresión completa

La modularización comienza sólo después de 3C.10 y de congelar el Arco 1.

## 5. 3C.3A Cartografía

APROBADA / congelable.

REV3:
`Cartografia_329_Estructurada_v3_CANDIDATA.json`

SHA-256:
`ac46c34ef967c3b9f15103784b68d04c36991dc63567f3e110a4232abf3d4077`

Resultado:
- 329/329 salas
- 17/17 áreas
- 22 hojas area/capa
- 355/355 cardinales intra-hoja
- 349 rectas + 6 rutas
- 2 crossovers certificados
- 0 pendientes
- 0 geometrías REV2 alteradas

Crossovers:
- `CO_AGUAS_01` en `(24,0)`
- `CO_VALLE_01` en `(72,42)`

`CRUCE_CARTOGRAFICO_NO_CONECTIVO` es sólo gráfico y jamás crea una conexión diegética.

## 6. 3C.3B Atlas

Integrar REV3 sin reescribir la experiencia Atlas actual.

Reglas:
- conservar `atlasAreaVista/atlasCapaVista` separado de `this.pos`;
- conservar selector de áreas conocidas y `MI ZONA`;
- consultar hojas sin mover jugador;
- soportar 6 rutas y 2 crossovers;
- una hoja sólo puede consultarse si esa `(area,capa)` es conocida;
- el gap del crossover sólo se dibuja cuando ambas aristas están visibles;
- escala: 12 unidades REV3 → 56 px;
- no tocar NPC/misiones.

Target previsto:
- `grulla-blanca_ver73.html`
- `Informe_Implementacion_3C3B_ver73.md`

Toda salida Codex debe auditarse independientemente antes de convertirse en baseline.

## 7. 3C.4

CERRADO Y CONGELADO.

Puntos clave:
- mover errantes sólo en área activa;
- cooldown/respawn global;
- 11 territorios canónicos;
- atracción QI/SANGRE siempre usa criatura real;
- fixed atraído muerto → cooldown origen;
- fixed que sobrevive/huye → vuelve conceptualmente, sin cooldown;
- errante que sobrevive permanece;
- EXTRAER suma exactamente 1 `turnoGlobal`;
- fallo pierde exactamente 1 turno útil;
- SANGRE sólo en fallo;
- eliminados `mobInterrupcion` y `PROB_INTERUPCION`;
- deadlines con `turnoGlobal`;
- dormir no avanza deadlines;
- P06 `sangre_huerto` sigue pendiente;
- schema 2; atracción no persistente.

Fix ver72a:
`if (this.combate) { this.cerrarInteraccionOficio(); return; }`

Auditoría:
- 11/11 PASS 3C.4
- 350/350 PASS suite completa
- mundo 329/17/787
- 0 broken
- 0 isolated
- 1 component

## 8. 3C.5 NPC

NO CERRADO.

REV1 cubrió 32/32 NPC pero la auditoría independiente detectó correcciones obligatorias para REV2.

Revisar:
- conteo editorial correcto: 16 explícitos + Shen Baojun + Pei Luo = 18 elecciones técnicas;
- leakage de `territorio_por_etapa`;
- Gao Shun epílogo: permanece en la puerta;
- knowledge R1-R10 completo;
- Gao Shun R1 → SOSPECHA;
- Feng Zhi R5 → SABE;
- Luo Yan R5 → SABE;
- Ning Cai R1 conserva ambigüedad;
- Han Qiao R6 requiere justificación;
- separar territorio narrativo de `TRANSITO_TECNICO_3C5`;
- rutas técnicas de Qiao Ren, Wei Jian, Wen Tao, Yu Shun y Gao Shun deben quedar como `ELECCION_TECNICA_3C5_RUTA`;
- save/load con marcador de subsistema como `npc_version=1`;
- `atlas.personas` nunca es posición real;
- alias sólo si globalmente inequívocos.

No implementar hasta aprobar REV2.

## 9. 3C.6A

Auditoría documental P + M01–M07 iniciada en paralelo.

3C.4 no bloquea.
3C.5 bloquea implementación, pero no auditoría documental.

Paquete preparado:

`LA_GRULLA_BLANCA_3C6A_AUDITORIA_PARA_CLAUDE.zip`

SHA-256:
`fdb181cfa57d084de2e6c14bf69b71a52315f9c5d4dd3794042e3ffc53b16ccd`

Incluye:
- Auditoría 6 canónica M01–M18
- Auditoría 6 estructurada
- Auditoría 5 NPC
- handoff 2026-09-22
- matriz NPC canónica
- topología 329 v2
- baseline ver72a
- prompt y límites 3C.6A

Claude debe devolver:
1. `Reconciliacion_3C6A_Prologo_M01_M07_REV1.md`
2. `Matriz_Implementacion_3C6A_Prologo_M01_M07_REV1.json`

No inventar room IDs. Localizaciones sin mapping explícito quedan `NO_CERRADO_EN_FUENTE`.

## 10. Roles

- ChatGPT/Sol: diseño, reconciliación y auditoría independiente.
- Claude: auditoría documental/cartográfica.
- Codex: implementación técnica; no debe ser único auditor conceptual de su propio trabajo.

No cerrar una etapa sólo porque el implementador informe PASS.

## 11. Modularización

Punto de corte acordado:

`3C.10 PASS → congelar Arco 1 → modularización → mejoras UI/assets → Arco 2`

Durante migración:
- conservar HTML final como referencia dorada;
- extraer módulos progresivamente;
- correr regresión tras cada extracción;
- código modular = fuente;
- HTML generado = artefacto de distribución, no edición manual.

Estructura futura aproximada:
- src/core
- src/world
- src/atlas
- src/npcs
- src/combat
- src/professions
- src/quests
- src/persistence
- src/ui
- src/data
- tests
- assets

## 12. GitHub/web

Repositorio maestro:
`Shein25/La-Grulla-Blanca`

Commits iniciales:
- `c488b9e9de9c04f171245a1478b17f393b085cbc`
- `639e4d1566299345c0d7147efc137653065c6263`
- `215d98ddf0dcebf453502bf70818764349b64cd8`

Se prevé GitHub Pages para versión jugable por link una vez que exista un baseline de distribución adecuado.

## 13. Política de backups

Este snapshot no se sobrescribe.

Crear uno nuevo después de:
- etapa 3C aprobada;
- nuevo baseline HTML aprobado;
- cambio de schema;
- cartografía/NPC/misiones congeladas;
- 3C.10;
- modularización;
- primera versión web;
- inicio/cierre de arco.

Cada backup debe incluir:
- baseline + SHA;
- fuentes vigentes;
- decisiones nuevas;
- etapas cerradas/pendientes;
- invariantes;
- entregables;
- problemas abiertos;
- siguiente acción.

## 14. Próxima acción

Tres frentes compatibles:
1. 3C.3B: recibir implementación Atlas y auditar.
2. 3C.5: recibir/reconciliar REV2 NPC y auditar.
3. 3C.6A: recibir REV1 Claude y auditar.

No implementar 3C.6 si 3C.5 todavía no está cerrado.
