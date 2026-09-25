# Reconciliación 3C.7A — M13–M15 — REV1

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_AUDITORIA_DOCUMENTAL`  
**Autoridad principal:** Fuente Maestra ver55, T289 (2026-09-20T07:53:01Z).  
**Alcance:** M13, M14, M15; permisos y gates físicos asociados; R6, R8 y R9.  
**Fuera de alcance:** implementación, M16+, Núcleo Profundo, R7, R10, LIBERAR/CUSTODIAR.

## 1. Columna vertebral

`M12 + gate LIII→LIV → M13 → M14 → M15`.

M13 ocurre en `LIV_REVELACION`. M14 requiere M13 HECHA. M15 requiere M14 HECHA.

## 2. Gates y permisos físicos

### M13

`MANTENIMIENTO_INVESTIGACION` es permiso institucional limitado. Al activarse M13 abre `GATES_329.PASO_MANTENIMIENTO`, es decir `ala_umbral_mantenimiento ↔ mantenimiento_acceso`.

Este permiso **no concede Núcleo** y no abre `PASO_NUCLEO`.

### M14

El Consejo concede `NUCLEO_SUPERIOR`. Ese permiso habilita `GATES_329.PASO_NUCLEO`, es decir `mantenimiento_compuerta_nucleo ↔ nucleo_pozo_voto`.

### M15

`NUCLEO_SUPERIOR` permanece válido para el recorrido superior. `GATES_329.PASO_PULSO` (`nucleo_archivo_promesa ↔ nucleo_descenso_pulso`) permanece cerrado.

`NUCLEO_PROFUNDO` no se concede en M13, M14 ni M15.

## 3. M13 — Todo consume algo

### 3.1 Requiere y activa

Requiere `arc1.estado=LIV_REVELACION` y M12 HECHA.

T289 sitúa el inicio cuando Duan Shibo y He Zhen reciben el informe de Primera Ala y aparecen consumos de Producción sin destino moderno claro.

Disparador técnico candidato: conversación formal con Duan Shibo en `oficina_logistica`, incorporando el informe de He Zhen. Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`; la fuente no congela room/orden exactos de esa conversación.

Al activar: `M13=ACTIVA`, `MANTENIMIENTO_INVESTIGACION=true`, `gates.PASO_MANTENIMIENTO=true`.

### 3.2 Recorrido y evidencia

M13 no se cierra sólo por leer `mantenimiento_registro_consumo`. Debe cruzar evidencia antigua/material con información moderna de Producción.

Fuentes reales idóneas de ver74:

- `mantenimiento_registro_consumo`: categorías, manifiestos y comparaciones de consumos sin destino inmediato;
- `mantenimiento_almacen`: lotes y materiales todavía usados en Producción;
- `mantenimiento_taller`: piezas antiguas reparadas con materiales modernos;
- `mantenimiento_galeria_conductos`: empalmes y flujo hacia niveles profundos;
- `mantenimiento_camara_presion`: indicadores de una demanda de estabilidad continua situada más abajo;
- `oficina_logistica`: manifiestos actuales;
- `almacen_materiales`: inventario/reservas actuales;
- `taller_lu_cheng`: contraste técnico de piezas.

Se propone una evidencia semántica:

`CONSUMO_ANTIGUO_IDENTIFICADO`: datos de Mantenimiento muestran consumo continuado.

`OPERACION_PRESENTE`: evidencia material demuestra reparaciones/flujo/estabilidad actuales.

`CORRELACION_PRODUCCION`: el consumo antiguo se cruza con recursos o fabricación contemporáneos.

El cierre exige las tres ideas, no rooms concretas ni una cantidad fija de inspecciones.

### 3.3 Alojamiento

`mantenimiento_dormitorio_turnos` puede quedar conocido al visitarlo y funciona como alojamiento seguro de Mantenimiento. Descubrirlo no es requisito de M13.

### 3.4 Cierre

Al confirmar que recursos modernos siguen alimentando infraestructura antigua:

`M13=HECHA`, `R6=CONFIRMADO`, Comprensión `+1` one-shot `ARC1_M13_CONSUMO_ACTUAL`.

Recompensas: Mérito importante, Contribución moderada/sí según balance, prestigio en Recursos/Formaciones. Números pendientes.

Canon negativo: M13 demuestra entrada de energía/material, consumo, presión y residuos; **no revela una entidad viva**, no confirma R7 y no concede Núcleo.

La Sombra de Marea Residual puede existir como contenido lateral, pero nunca es requisito de R6 ni llave de progreso.

## 4. M14 — La promesa aplazada

### 4.1 Requiere y autorización

Requiere M13 HECHA.

El Consejo concede un acceso muy limitado al Núcleo Superior: `NUCLEO_SUPERIOR=true` y `gates.PASO_NUCLEO=true`.

La fuente no congela el NPC exacto que formaliza esa autorización ni una room de Consejo específica para M14. No inventarlos en REV1.

### 4.2 Recorrido

Ruta física real:

`mantenimiento_compuerta_nucleo → nucleo_pozo_voto → nucleo_camara_voto → nucleo_galeria_primer_pacto → nucleo_primer_pacto`.

### 4.3 Evidencia semántica

Objetivo: reconstruir evidencia inequívoca de que la Grulla histórica aceptó participar voluntariamente en el pacto original.

Fuentes idóneas de ver74:

- `nucleo_camara_voto.relieve/sellos/inscripciones`: acto compartido, no conquista;
- `nucleo_galeria_primer_pacto.cultivadores/grulla`: colaboración histórica;
- `nucleo_primer_pacto.sellos_dobles/suelo`: partes diferenciadas/equivalentes;
- `nucleo_primer_pacto.inscripciones`: fórmulas de aceptación, tarea y responsabilidad.

REV1 propone agruparlas como `ACTO_FORMAL`, `PARTICIPACION_MUTUA` y `CONSENTIMIENTO_DOCUMENTADO`. El evaluador puede requerir diversidad de evidencia, no un contador de cuatro rooms.

### 4.4 Cierre

Cuando la evidencia permite afirmar sin ambigüedad razonable la participación voluntaria:

`M14=HECHA`, `R8=CONFIRMADO`, Comprensión `+1` one-shot `ARC1_M14_CONSENTIMIENTO`, M15 disponible.

Recompensas: Mérito importante; Contribución pequeña/moderada o no necesariamente alta; balance pendiente.

Canon negativo:

- M14 **no** confirma todavía que el pacto debía ser temporal;
- no revela R9;
- no revela R7 ni R10;
- no confirma que la Grulla actual sea la misma;
- no modifica el vínculo;
- no concede `NUCLEO_PROFUNDO`.

## 5. M15 — Lo que debía terminar

### 5.1 Requiere y acceso

Requiere M14 HECHA y `NUCLEO_SUPERIOR`.

El centro documental es `nucleo_archivo_promesa`. `PASO_PULSO` sigue cerrado; `nucleo_descenso_pulso` puede ser conocido como continuación física, pero no atravesado.

### 5.2 Cadena documental

T289 congela la conclusión principal: el sistema original no debía depender indefinidamente de participación viva; existía obligación de sustitución/relevo.

También conserva una cadena de aplazamiento institucional:

1. un relevo/prototipo técnico todavía no era seguro;
2. la ruptura/pérdida de capacidad de Primera Ala volvió razonable extender el arreglo;
3. mantener el sistema existente terminó normalizándose como procedimiento/mantenimiento.

El scenery real `nucleo_archivo_promesa` ya contiene `relevo`, `aplazamientos`, `placas` y `descenso`. La interacción exacta para reconstruir esos tres hitos es técnica; no crear tres rooms nuevas.

Se proponen hitos semánticos `RELEVO_PREVISTO`, `APLAZAMIENTO_TECNICO`, `APLAZAMIENTO_RUPTURA` y `NORMALIZACION_MANTENIMIENTO`.

### 5.3 Cierre

Al reconstruir el relevo previsto y la cadena de aplazamientos:

`M15=HECHA`, `R9=CONFIRMADO`, Comprensión `+1` one-shot `ARC1_M15_RELEVO_APLAZADO`.

Recompensas: Mérito importante; Contribución mínima o ninguna; números pendientes.

M15 puede registrar una acción HISTORY sobre cómo el jugador interpreta la responsabilidad heredada, pero esa postura **no decide** LIBERAR/CUSTODIAR ni cambia R9.

### 5.4 Límites

Al terminar M15:

- `PASO_PULSO=false`;
- `NUCLEO_PROFUNDO=false`;
- R7 sigue cerrado;
- R10 sigue cerrado;
- no se sabe si la red depende actualmente de una entidad viva;
- no se sabe si la Grulla histórica y la actual son la misma;
- no se decide LIBERAR/CUSTODIAR.

## 6. Relación M15 → M16

M15 no causa mágicamente la crisis. T289 dice que la investigación se formaliza y **después** comienzan avisos simultáneos.

Como el proyecto no usa tiempo diegético, REV1 no introduce temporizador ni `setTimeout` narrativo.

El cierre de M15 sólo deja satisfechas las condiciones previas para un **evento narrativo separado** que activará M16 en su reconciliación específica.

No definir todavía cuál acción concreta dispara ese evento.

## 7. Persistencia propuesta

Extender `flags.arc1` sin claves top-level:

- `evidenciaMantenimiento` para M13;
- `evidenciaPacto` para M14;
- `evidenciaPromesa` para M15;
- `revelaciones.R6/R8/R9`;
- `permisos.MANTENIMIENTO_INVESTIGACION`;
- `permisos.NUCLEO_SUPERIOR`.

Los hitos one-shot pueden reutilizar `flags.arc1.hitos` si el contrato global de 3C.7 mantiene esa decisión. No duplicar el mismo hecho entre dos fuentes persistentes.

## 8. Idempotencia

Cada evidencia nueva debe registrarse una sola vez y reconciliar progreso en la misma acción. Repetir `EXAMINAR`, `LEER/ESTUDIAR`, conversaciones o cargar partida no repite Comprensión, Mérito, Contribución, permisos ni revelaciones.

`NUCLEO_SUPERIOR` y los gates físicos deben persistir coherentemente en save/load.

## 9. Anclajes NPC

T289 nombra para M13 a Duan Shibo, He Zhen, Ma Qiren, Lu Cheng y Song Rui. No todos necesitan anclaje.

ver74 documenta a Duan Shibo con anclaje M13 y sala inicial `oficina_logistica`. REV1 propone usarlo como punto de activación técnica y liberar el anclaje una vez entregado el encargo.

Para He Zhen, Ma Qiren, Lu Cheng y Song Rui se prefieren sus territorios válidos y conversaciones contextuales; no inventar reuniones conjuntas ni moverlos a Mantenimiento sin fuente.

M14/M15 son principalmente investigación material/documental; no inventar una expedición grupal.

## 10. Legacy que se elimina del progreso principal

Perla de la Marea + Pluma Celeste dejan de ser reliquias-llave. Sombra y Centinela pueden sobrevivir como entidades antiguas opcionales, pero derrotarlas no abre la historia ni sustituye evidencia/autorización.

## 11. Pendientes antes de contrato

1. Auditar el mapeo de evidencias M13 a scenery concreto.
2. Auditar los tres grupos semánticos de M14.
3. Auditar si los cuatro hitos propuestos de M15 deben reducirse/renombrarse para no endurecer T289.
4. Cerrar modelo uniforme de permisos heredado del frente M12.
5. Balance numérico M13–M15.
6. Reconciliar por separado el evento de inicio M16; no incorporarlo aquí.
7. Congelar runtime predecesor sólo después del PASS de 3C.6.

## Estado

`3C7A_M13_M15_REV1_LISTA_PARA_AUDITORIA_DOCUMENTAL`

**NO IMPLEMENTAR TODAVÍA.**
