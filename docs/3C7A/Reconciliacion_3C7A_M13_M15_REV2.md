# Reconciliación 3C.7A — M13–M15 — REV2

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_REAUDITORIA_DE_CIERRE`  
**Base:** REV1 + auditoría externa Claude.  
**No implementar todavía.**

## 1. Correcciones de auditoría

### H-B1 — M15: premisa vs aplazamientos

`RELEVO_PREVISTO` deja de contarse como cuarto aplazamiento.

REV2 separa:

- **premisa de R9:** `RELEVO_PREVISTO` — existía obligación de sustitución/relevo;
- **tres hitos de aplazamiento:**
  1. `APLAZAMIENTO_TECNICO` — el relevo/prototipo aún no era seguro;
  2. `APLAZAMIENTO_RUPTURA` — la pérdida de capacidad tras la ruptura de Primera Ala volvió razonable extender el arreglo;
  3. `NORMALIZACION_MANTENIMIENTO` — la excepción terminó normalizándose como procedimiento/mantenimiento.

El cierre de M15 exige la premisa + la cadena de tres aplazamientos suficientemente reconstruida. `RELEVO_PREVISTO` no se presenta como cuarto aplazamiento independiente.

### H-B2 — evaluador M13

Las categorías `CONSUMO_ANTIGUO_IDENTIFICADO`, `OPERACION_PRESENTE` y `CORRELACION_PRODUCCION` son una traducción técnica de T289, no nombres canónicos literales.

Clasificación REV2: `ELECCION_TECNICA_3C7_AUDITAR`.

El contrato conserva el significado, pero permite ajustar nombres/agrupación durante la reauditoría sin alterar R6.

### H-B3 — dependencia formal M16

M15 no activa M16 en el mismo evento y no usa temporizador.

REV2 registra formalmente:

`DEPENDENCIA_DE_CIERRE_ARCO_M12_M16: definir un evento narrativo separado, alcanzable e idempotente que transforme LIV_REVELACION -> LIV_CRISIS y active M16`.

Esta dependencia no pertenece a M15 ni se implementa aquí, pero debe resolverse antes de considerar documentalmente cerrado el tramo M12–M16.

## 2. Columna vertebral

`M12 + gate LIII→LIV → M13 → M14 → M15`.

M13 ocurre en `LIV_REVELACION`; M14 exige M13; M15 exige M14.

## 3. Gates y permisos

M13: `MANTENIMIENTO_INVESTIGACION=true` abre `PASO_MANTENIMIENTO` (`ala_umbral_mantenimiento ↔ mantenimiento_acceso`). No concede Núcleo.

M14: `NUCLEO_SUPERIOR=true` abre `PASO_NUCLEO` (`mantenimiento_compuerta_nucleo ↔ nucleo_pozo_voto`).

M15: `PASO_PULSO` (`nucleo_archivo_promesa ↔ nucleo_descenso_pulso`) permanece cerrado. `NUCLEO_PROFUNDO=false`.

## 4. M13 — Todo consume algo

Requiere `arc1.estado=LIV_REVELACION` y `M12=HECHA`.

T289 sitúa el inicio cuando Duan Shibo y He Zhen reciben el informe de Primera Ala y aparecen consumos de Producción sin destino moderno claro.

Disparador técnico candidato: `HABLAR duan_shibo @ oficina_logistica`. Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`.

Al activar: `M13=ACTIVA`, `MANTENIMIENTO_INVESTIGACION=true`, `PASO_MANTENIMIENTO=true`.

### 4.1 Evidencia M13

REV2 conserva tres funciones semánticas, todas bajo `ELECCION_TECNICA_3C7_AUDITAR`:

- `CONSUMO_ANTIGUO_IDENTIFICADO`: registros de Mantenimiento demuestran consumo continuado;
- `OPERACION_PRESENTE`: evidencia material demuestra intervención/flujo/estabilidad actuales;
- `CORRELACION_PRODUCCION`: la evidencia se cruza con recursos/fabricación contemporáneos.

Fuentes candidatas reales incluyen `mantenimiento_registro_consumo`, `mantenimiento_almacen`, `mantenimiento_taller`, `mantenimiento_galeria_conductos`, `mantenimiento_camara_presion`, `oficina_logistica`, `almacen_materiales` y `taller_lu_cheng`.

El cierre exige las tres **ideas**, no una lista fija de rooms.

`mantenimiento_dormitorio_turnos` puede descubrirse como alojamiento seguro pero no es requisito.

Cierre: `M13=HECHA`, `R6=CONFIRMADO`, Comprensión +1 `ARC1_M13_CONSUMO_ACTUAL`, M14 disponible derivada.

Canon negativo: no revela R7, no demuestra entidad viva, no concede Núcleo. Sombra de Marea Residual es opcional y no llave.

## 5. M14 — La promesa aplazada

Requiere M13 HECHA.

El Consejo concede acceso limitado: `NUCLEO_SUPERIOR=true`, `PASO_NUCLEO=true`. NPC/room exactos de autorización siguen `NO_CERRADO_EN_FUENTE`.

Ruta física:
`mantenimiento_compuerta_nucleo → nucleo_pozo_voto → nucleo_camara_voto → nucleo_galeria_primer_pacto → nucleo_primer_pacto`.

Grupos semánticos propuestos:
- `ACTO_FORMAL`;
- `PARTICIPACION_MUTUA`;
- `CONSENTIMIENTO_DOCUMENTADO`.

Clasificación conjunta: `ELECCION_TECNICA_3C7_AUDITAR`, apoyada en scenery real del Voto/Primer Pacto.

Cierre: `M14=HECHA`, `R8=CONFIRMADO`, Comprensión +1 `ARC1_M14_CONSENTIMIENTO`, M15 disponible derivada.

Canon negativo: no R9, no R7/R10, no temporalidad todavía, no identidad actual de la Grulla, no cambio de vínculo, no Núcleo Profundo.

## 6. M15 — Lo que debía terminar

Requiere M14 HECHA + `NUCLEO_SUPERIOR=true`.

Centro documental: `nucleo_archivo_promesa`. `PASO_PULSO=false`. `NUCLEO_PROFUNDO=false`.

### 6.1 Premisa

`RELEVO_PREVISTO`: existía obligación de sustitución/relevo; no es un aplazamiento.

### 6.2 Tres aplazamientos

1. `APLAZAMIENTO_TECNICO`;
2. `APLAZAMIENTO_RUPTURA`;
3. `NORMALIZACION_MANTENIMIENTO`.

Estos tres hitos representan la cadena recuperada de T289. La interacción exacta con `relevo`, `aplazamientos` y `placas` es técnica; no se crean rooms adicionales.

### 6.3 Cierre

Requiere:
- premisa `RELEVO_PREVISTO` confirmada;
- los tres aplazamientos suficientemente reconstruidos.

Produce:
- `M15=HECHA`;
- `R9=CONFIRMADO`;
- Comprensión +1 `ARC1_M15_RELEVO_APLAZADO`;
- condiciones previas para el futuro evento M16 satisfechas.

Una acción HISTORY puede registrar postura sobre responsabilidad heredada, pero no decide LIBERAR/CUSTODIAR ni modifica R9.

Al cerrar: R7 cerrado, R10 cerrado, `PASO_PULSO=false`, `NUCLEO_PROFUNDO=false`, identidad actual de la Grulla no resuelta, dependencia viva actual no resuelta.

## 7. M15 → M16

M15 no causa la crisis inmediatamente.

No se usa `setTimeout`, reloj narrativo ni tiempo diegético.

Se registra la dependencia formal:

`M16_EVENTO_INICIO_PENDIENTE_RECONCILIACION`.

Requisitos del futuro diseño M16:
- debe ser un evento narrativo separado de M15;
- debe ser alcanzable tras M15 sin depender de azar no acotado;
- debe ser idempotente;
- debe pasar `arc1.estado` de `LIV_REVELACION` a `LIV_CRISIS` una sola vez;
- no puede depender de `entrarSala()` genérico como parche invisible;
- su ausencia bloquea el cierre documental del tramo M12–M16, pero no invalida M13–M15.

## 8. Persistencia e idempotencia

Todo bajo `flags.arc1` / `this.quests`, sin nuevas claves top-level.

Estructuras propuestas: `evidenciaMantenimiento`, `evidenciaPacto`, `evidenciaPromesa`, `revelaciones.R6/R8/R9`, permisos Mantenimiento/Núcleo y hitos one-shot.

Cada evidencia nueva se registra una vez y reconcilia progreso en la misma acción. Repetir comandos o cargar partida no repaga recompensas ni reabre permisos.

## 9. Legacy que no vuelve como llave

Perla de la Marea, Pluma Celeste, Sombra y Centinela pueden sobrevivir como contenido opcional/histórico, pero no sustituyen evidencia, permisos ni gates.

## 10. Pendientes antes de contrato

1. reauditar la traducción técnica de las tres funciones M13;
2. reauditar los tres grupos semánticos M14;
3. validar que M15 trate `RELEVO_PREVISTO` como premisa y exactamente tres aplazamientos;
4. cerrar modelo uniforme de permisos junto con M12 REV2;
5. balance numérico M13–M15;
6. reconciliar M16 en documento separado antes del cierre del tramo M12–M16;
7. congelar runtime predecesor tras PASS de 3C.6.

## Estado final

`3C7A_M13_M15_REV2_LISTA_PARA_REAUDITORIA_DE_CIERRE`
