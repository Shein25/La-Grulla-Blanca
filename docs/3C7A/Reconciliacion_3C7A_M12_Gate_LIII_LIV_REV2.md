# Reconciliación 3C.7A — M12 + gate LIII→LIV — REV2

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_REAUDITORIA_DE_CIERRE`  
**Base:** REV1 + auditoría externa Claude.  
**No implementar todavía.**

## 1. Correcciones de auditoría

### H-A1 — promoción a CONCLUYENTE

REV2 elimina como regla cerrada la vía `SUFICIENTE + Custodio terminal + confirmación central => CONCLUYENTE`.

T288 no congela literalmente que resolver al Custodio eleve por sí solo la evidencia.

Regla REV2:

- `SUFICIENTE` habilita progreso y PROTOCOLO.
- `CONCLUYENTE` exige `SUFICIENTE + CORROBORACION_FUERTE_INDEPENDIENTE`.
- el Custodio terminal es un requisito separado de cierre.
- resolver al Custodio con evidencia `SUFICIENTE` no cierra M12 ni cambia automáticamente el nivel.

`CORROBORACION_FUERTE_INDEPENDIENTE` es una categoría técnica a fijar y auditar. Debe existir al menos una fuente concreta alcanzable antes y después de resolver al Custodio, sin exigir 6/6 atajos ni todas las ramas.

### H-A2 — ruta física corregida

La Cámara de las Dos Alas no conecta directamente con el umbral de Mantenimiento.

Ruta de investigación:
`formaciones_sello_antiguo → formaciones_descenso_tecnico → ala_vestibulo → ala_nudo_seis_corrientes ↔ ala_camara_dos_alas`.

Ruta física desde la Cámara hacia el umbral:
`ala_camara_dos_alas → ala_nudo_seis_corrientes → ala_vestibulo → ala_galeria_distribucion → ala_umbral_mantenimiento`.

### H-A3 — M11/R3 verificados

`Reconciliacion_3C7A_M08_M11_REV2.md` y su matriz confirman que M11 produce:

- `M11=HECHA`;
- `flags.arc1.revelaciones.R3=CONFIRMADO`;
- `flags.arc1.sintesis.DOS_ALAS=PRINCIPIO`.

Por tanto `M11 HECHA => R3 CONFIRMADO` queda respaldado documentalmente. REV2 no crea `DOS_ALAS=COMPRENDIDAS`.

## 2. Gates

`GATES_329.M12`: `formaciones_sello_antiguo ↔ formaciones_descenso_tecnico`. Entrada oficial a Primera Ala.

Gate LIII→LIV: gate de cultivo, no topológico.

`GATES_329.PASO_MANTENIMIENTO`: `ala_umbral_mantenimiento ↔ mantenimiento_acceso`. Permanece cerrado durante M12 y abre en M13.

## 3. Activación M12

Requiere `M11=HECHA` y `arc1.estado=LIII_INVESTIGACION`.

Al activarse: `M12=ACTIVA`, `PRIMERA_ALA_INVESTIGACION=true`, `gates.M12=true`.

Disparador propuesto: `HABLAR he_zhen @ formaciones_sello_antiguo`. Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`.

## 4. Evidencia Primera Ala

Persistencia propuesta: `flags.arc1.evidenciaPrimeraAla` con `nivel`, `hitos` y `fuentes`.

Niveles: `INSUFICIENTE → SUFICIENTE → CONCLUYENTE`.

Hitos centrales:
- `NUDO_INTERPRETADO` — `ala_nudo_seis_corrientes`;
- `DOS_ALAS_ARQUITECTURA` — `ala_camara_dos_alas`;
- `PATRON_RAMA` — evidencia funcional + patrón de diseño compartido. `ELECCION_TECNICA_3C7_AUDITAR`.

Evaluador REV2:
- `INSUFICIENTE`: faltan hitos centrales;
- `SUFICIENTE`: NUDO + DOS_ALAS + PATRON_RAMA;
- `CONCLUYENTE`: SUFICIENTE + `CORROBORACION_FUERTE_INDEPENDIENTE`.

La corroboración concreta queda `ELECCION_TECNICA_3C7_AUDITAR`; puede apoyarse en continuidad hacia superficie u otra evidencia independiente equivalente respaldada por infraestructura real.

Cada primera evidencia nueva debe ejecutar en la misma acción: `registrarEvidenciaPrimeraAla → evaluarEvidenciaPrimeraAla → reconciliarProgresionArc1`.

## 5. Atajos

Los seis `ATAJO_ALA_*` son opcionales, se abren individualmente, no son requisito de M12 ni LIII→LIV y no se abren automáticamente al cerrar M12.

## 6. Custodio de las Dos Alas

Persistencia única: `flags.arc1.custodioDosAlas = NO_RESUELTO | DERROTADO | RESUELTO_POR_PROTOCOLO`.

COMBATE: derrotar → `DERROTADO`; huir/morir/abandonar no resuelve; reintentable; sin llave/reliquia ni premio superior exclusivo.

PROTOCOLO: requiere `M11=HECHA + evidenciaPrimeraAla>=SUFICIENTE`; no exige 6 atajos, 14 secretos, único ecológico ni Afinidad alta.

No crear `ala_control_este/oeste`. La interfaz exacta sigue pendiente.

Localización candidata: `ala_camara_dos_alas`, clasificada `ELECCION_TECNICA_RESPALDADA_POR_FUENTE_A_AUDITAR`.

## 7. Cierre M12

Requiere simultáneamente:
- `evidenciaPrimeraAla=CONCLUYENTE`;
- Custodio en `DERROTADO` o `RESUELTO_POR_PROTOCOLO`.

Produce one-shot:
- `M12=HECHA`;
- `R5=CONFIRMADO`;
- Comprensión +1 `ARC1_M12_RED_PRIMERA_ALA`;
- Primera Ala confirmada;
- `ala_umbral_mantenimiento` conocido;
- `AUTORIZACION_INVESTIGACION_PROFUNDA=true`.

Mantiene `PRIMERA_ALA_INVESTIGACION=true` y `PASO_MANTENIMIENTO=false`.

## 8. Autorización y permisos

`PRIMERA_ALA_INVESTIGACION` y `AUTORIZACION_INVESTIGACION_PROFUNDA` son permisos semánticamente distintos.

`AUTORIZACION_INVESTIGACION_PROFUNDA`: fuente institucional; origen cierre formal M12; vigencia al menos hasta superar LIII→LIV; NPC emisor `NO_CONGELADO_EN_FUENTE`.

Antes del contrato debe elegirse un modelo uniforme global para permisos: boolean + metadatos separados, o objeto `{activo, fuente, origen, vigencia}`. Estado: `DECISION_TECNICA_GLOBAL_PENDIENTE`. No mezclar ambos en un mismo save.

## 9. Gate LIII→LIV

Autoridad T288:
`qi>=75 + M11 HECHA + M12 HECHA + R3 CONFIRMADO + R5 CONFIRMADO + autorización institucional correspondiente`.

Al superar: `player.etapa=4`, `arc1.estado=LIV_REVELACION`, M13 disponible derivada. No cambia rango institucional.

## 10. Sustitución del legacy PUERTAS[4]

El legacy `2 píldoras + comprension:6` se clasifica `CAMBIO_NECESARIO_3C7`.

El futuro contrato debe garantizar:
- etapa 3→4 usa exclusivamente el gate Arc1/T288;
- no exige ni consume dos píldoras;
- no exige `comprension:6`;
- no queda una segunda validación legacy;
- toda mutación irreversible ocurre después de validar el nuevo gate.

La estrategia concreta de código queda fuera de esta reconciliación.

## 11. Pendientes antes de contrato

1. fijar una fuente concreta para `CORROBORACION_FUERTE_INDEPENDIENTE`;
2. auditar mecanismo del PROTOCOLO sin rooms nuevas;
3. auditar localización del Custodio;
4. elegir modelo uniforme de permisos;
5. fijar balance M12;
6. congelar runtime predecesor tras PASS de 3C.6.

## Estado final

`3C7A_M12_GATE_LIII_LIV_REV2_LISTA_PARA_REAUDITORIA_DE_CIERRE`
