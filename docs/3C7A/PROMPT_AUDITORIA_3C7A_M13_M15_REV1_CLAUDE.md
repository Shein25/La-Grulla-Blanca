# Prompt de auditoría externa — 3C.7A M13–M15 REV1

Auditá de forma independiente la reconciliación documental M13–M15 de `La Grulla Blanca`.

Trabajá en modo **solo lectura**. No modifiques archivos, no crees ramas, no hagas commits, no hagas merge y no implementes 3C.7.

Repositorio: `Shein25/La-Grulla-Blanca`
Rama: `audit/3c7a-fase1-rev2`
HEAD exacto: será suministrado externamente al ejecutar la auditoría.

## Jerarquía

1. decisiones humanas posteriores explícitas;
2. Fuente Maestra ver55, T289 como autoridad principal de M13–M15;
3. T257 sólo para estructura/idempotencia donde no contradiga T289;
4. Auditoría 6;
5. Fase1 REV2 como recuperación derivada;
6. ver74/3C.5 para infraestructura real;
7. topología 329 congelada.

## Archivos

- `docs/3C7A/Reconciliacion_3C7A_M13_M15_REV1.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M13_M15_REV1.json`
- `docs/3C7A/fuentes/Fuente_Maestra_T289_M13_M15_EXTRACTO.md`
- `docs/3C7A/Reconciliacion_3C7A_M12_Gate_LIII_LIV_REV1.md` como frontera previa;
- `docs/3C7A/Matriz_Implementacion_3C7A_M12_Gate_LIII_LIV_REV1.json`;
- `docs/3C7A/Auditoria_3C7A_M08_M15_FASE1_REV2.md`;
- `docs/3C7A/Matriz_3C7A_M08_M15_FASE1_REV2.json`;
- `grulla-blanca_ver74.html`.

## A. M13 — Todo consume algo

Verificá que M13:
- sólo empiece tras LIV_REVELACION/M12;
- conceda `MANTENIMIENTO_INVESTIGACION` y abra `PASO_MANTENIMIENTO`, sin conceder Núcleo;
- no se cierre únicamente por leer el Registro de Consumo;
- exija cruzar evidencia material antigua/presente con Producción moderna;
- use scenery real sin fingir que T289 congeló room IDs donde no lo hizo;
- produzca R6=CONFIRMADO y +1 Comprensión `ARC1_M13_CONSUMO_ACTUAL`;
- permita descubrir `mantenimiento_dormitorio_turnos` sin convertirlo en objetivo obligatorio;
- no revele R7 ni una entidad viva;
- trate la Sombra de Marea Residual como opcional y no llave.

Auditá especialmente los grupos propuestos `CONSUMO_ANTIGUO_IDENTIFICADO`, `OPERACION_PRESENTE` y `CORRELACION_PRODUCCION`. Si endurecen demasiado T289, indicá la corrección mínima sin inventar otro esquema.

## B. M14 — La promesa aplazada

Verificá que:
- M14 requiera M13;
- `NUCLEO_SUPERIOR` sea autorización institucional limitada y abra únicamente `PASO_NUCLEO`;
- el recorrido `mantenimiento_compuerta_nucleo → nucleo_pozo_voto → nucleo_camara_voto → nucleo_galeria_primer_pacto → nucleo_primer_pacto` sea físicamente válido;
- las evidencias `ACTO_FORMAL`, `PARTICIPACION_MUTUA`, `CONSENTIMIENTO_DOCUMENTADO` puedan derivarse de scenery sin convertir nombre coincidente en canon;
- el cierre confirme R8 y el consentimiento original;
- no adelante R9, R7 ni R10;
- no confirme que la Grulla actual sea la misma;
- no modifique el vínculo;
- no conceda NUCLEO_PROFUNDO.

No inventes quién del Consejo concede el permiso si T289 no lo congela.

## C. M15 — Lo que debía terminar

Verificá que:
- requiera M14/NUCLEO_SUPERIOR;
- use `nucleo_archivo_promesa` como centro documental;
- mantenga `PASO_PULSO=false` y `NUCLEO_PROFUNDO=false`;
- confirme R9: el vínculo/relevo debía ser temporal;
- preserve la cadena institucional de aplazamientos sin convertirla en tres rooms obligatorias;
- los hitos propuestos `RELEVO_PREVISTO`, `APLAZAMIENTO_TECNICO`, `APLAZAMIENTO_RUPTURA`, `NORMALIZACION_MANTENIMIENTO` no endurezcan indebidamente la fuente;
- +1 Comprensión use `ARC1_M15_RELEVO_APLAZADO`;
- una posible acción HISTORY no determine LIBERAR/CUSTODIAR;
- R7/R10 permanezcan cerrados.

## D. Gates

Contrastá en ver74:
- `PASO_MANTENIMIENTO`: ala_umbral_mantenimiento ↔ mantenimiento_acceso;
- `PASO_NUCLEO`: mantenimiento_compuerta_nucleo ↔ nucleo_pozo_voto;
- `PASO_PULSO`: nucleo_archivo_promesa ↔ nucleo_descenso_pulso.

Confirmá que no se cambian `ROOMS.exits` y que cada permiso abre sólo el gate que corresponde.

## E. Persistencia e idempotencia

Auditá el uso de estructuras bajo `flags.arc1`: evidencia M13/M14/M15, R6/R8/R9, permisos y hitos one-shot.

Comprobá que repetir EXAMINAR/LEER/HABLAR, cargar partida o revisitar rooms no repague recompensas ni reactive autorizaciones.

## F. M15 → M16

Confirmá que cerrar M15 no active automáticamente `LIV_CRISIS` en el mismo evento.

T289 separa la formalización de M15 de avisos posteriores. El proyecto no usa tiempo diegético, así que REV1 deja el disparador de M16 para una reconciliación aparte y no introduce temporizador.

Clasificá si esto es fiel a la fuente y si existe algún riesgo de soft-lock por dejar el evento pendiente.

## G. Canon negativo/legacy

Confirmá que no vuelvan como llaves principales:
- Perla de la Marea;
- Pluma Celeste;
- Sombra derrotada;
- Centinela derrotado;
- dos reliquias como cerradura narrativa.

## Entrega

Entregá `Auditoria_Cierre_3C7A_M13_M15_REV1_CLAUDE.md` con:
1. hallazgos por gravedad;
2. tabla M13/M14/M15: requisito, activación, evidencia, cierre, revelación, recompensa, canon negativo;
3. tabla de los tres gates físicos;
4. persistencia/idempotencia/soft-locks;
5. decisiones técnicas correctamente etiquetadas vs canon inventado;
6. correcciones mínimas, si las hubiera.

Veredicto exacto, uno de:

`3C7A_M13_M15_REV1_APTA_PARA_CONTRATO`

`3C7A_M13_M15_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

`3C7A_M13_M15_REV1_REQUIERE_CORRECCIONES`

No implementes. No avances M16.
