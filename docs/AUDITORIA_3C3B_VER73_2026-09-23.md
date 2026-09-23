# Auditoría independiente 3C.3B — ver73

**Fecha:** 2026-09-23  
**Entrega:** `grulla-blanca_ver73.html`  
**SHA-256:** `a66310f06fbf8c76e054df89f9d8cdf6959ac64c79400694474351c0936bc6dc`

## Veredicto

**3C.3B APROBADO.**

Con la cartografía 3C.3A ya aprobada, **3C.3 queda CERRADO** y `ver73` pasa a ser el baseline canónico para las siguientes integraciones.

## Comprobaciones independientes

- hash de ver72a canónico confirmado;
- hash de REV3 canónico confirmado;
- hash de ver73 coincide con la entrega;
- `ROOMS` y `GATES_329` idénticos a ver72a;
- `serializar()`, `deserializar()`, `validarSave329()` y `salidasAtlas()` idénticos a ver72a;
- `MAPA_POS`, `MAPA_ETIQ`, `MAPA_CAPA_SALA`, `MAPA_RUTAS` y `MAPA_CROSSOVERS` coinciden exactamente con REV3;
- firmas internas REV3 recomputadas y correctas;
- `auditarTopologiaMapa()`: 0 fallos;
- `auditarCartografia329()`: ok=true, 0 fallos;
- 22 mutaciones negativas del auditor rechazadas;
- 329 salas / 17 áreas;
- 787 salidas = 786 internas + 1 externa;
- 0 reciprocidades rotas;
- 0 salas aisladas;
- 1 componente;
- 63 articulation rooms;
- 70 bridges;
- 185 alcanzables inicialmente / 144 bloqueadas;
- capas: 217 principal / 19 sumergido / 73 profundo / 0 superior / 20 cumbre;
- 355 cardinales intra-hoja;
- 20 cardinales entre hojas;
- 18 verticales;
- 29 pares entre áreas;
- 2 cardinales cambian capa;
- 349 rectas + 6 routes = 355 representadas;
- 0 pendientes;
- exactamente 2 cruces no incidentes y ambos coinciden con `CO_AGUAS_01` y `CO_VALLE_01`;
- 0 líneas sobre rooms ajenas;
- 0 autointersecciones;
- bloque de 11 pruebas 3C.4 idéntico a ver72a;
- JavaScript extraído: `node --check` PASS;
- sin referencias runtime externas nuevas;
- sin nueva prosa prohibida de tiempo diegético;
- `SAVE_SCHEMA_VERSION = 2`.

## Revisión de lógica Atlas

La navegación de hoja exige conocimiento de la combinación exacta `(area,capa)`, no sólo del área.

La consulta cambia `atlasAreaVista/atlasCapaVista` pero no `this.pos`.

Los crossovers cortan sólo la línea inferior cuando las dos aristas implicadas están realmente visibles, evitando un hueco fantasma que revele una ruta desconocida.

Los atajos cerrados siguen la política de visibilidad prevista y abrir un gate no descubre por sí solo la hoja destino.

## Límite de esta auditoría

El informe de Codex declara 394/394 PASS y revisión visual de seis hojas. El entorno independiente no permitió relanzar Chromium; por ello se verificaron directamente el código, los datos, los auditores puros, la geometría, los negativos, el diff y la sintaxis, pero no se reclama una segunda ejecución del harness DOM completo.

## Decisión

`grulla-blanca_ver73.html` es el nuevo baseline canónico.

Siguiente foco: 3C.5 NPC y 3C.6A Prólogo + M01–M07.
