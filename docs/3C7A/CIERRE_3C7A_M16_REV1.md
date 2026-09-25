# Cierre documental — 3C.7A M16 REV1

**Fecha:** 2026-09-25  
**Estado:** `CERRADA_DOCUMENTALMENTE_APTA_CON_DECISION_TECNICA_PENDIENTE`  
**Snapshot auditado:** `f575a45f322575680f972e2313c1bfadbf73616d`

## Fuentes de cierre

1. `Reconciliacion_3C7A_M16_REV1.md`
2. `Matriz_Implementacion_3C7A_M16_REV1.json`
3. `Auditoria_3C7A_M16_REV1_CLAUDE.md`
4. Fuente Maestra ver55 T281 como autoridad principal de M16.
5. T260 como fuente histórica complementaria.
6. T257 para patrón de idempotencia.
7. Auditoría 6.
8. `grulla-blanca_ver74.html` para infraestructura real.
9. `CIERRE_3C7A_M13_M15_REV2.md` como frontera previa.

## Huella congelada

Matriz REV1 — Git blob SHA:

`44f7b042c0aec0008e57d6881a61fda558389247`

Reconciliación REV1 — Git blob SHA:

`52f712b84919ac6ad21aea9dcae2bb8ceb327bac`

## Veredicto externo

`3C7A_M16_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

No hay bloqueantes.

## Contrato documental congelado

- M16 no se activa en el mismo evento que cierra M15.
- El inicio es un evento narrativo posterior, explícito, alcanzable, one-shot, sin RNG macro, sin tiempo diegético y sin `entrarSala()` genérico.
- Al activarse:
  - `M16=ACTIVA`;
  - `arc1.estado=LIV_CRISIS`;
  - seis frentes = `PENDIENTE`;
  - `EMERGENCIA_SECTA=ACTIVA`.
- Frentes:
  - MEDICINA;
  - RUTAS;
  - FORMACIONES;
  - RECURSOS;
  - SAUCES;
  - JARDINES.
- Estados terminales:
  - `ESTABLE`;
  - `COSTOSO`;
  - `DAÑADO`.
- No existe estado `FALLIDO`.
- `DAÑADO` nunca bloquea M17, Fundación/ZhuJi, recetas obligatorias ni llaves de progreso.
- Resolución macro determinista.
- `resolverFrente(id)` es one-shot e idempotente.
- El jugador interviene aproximadamente en dos frentes, sin contador visible rígido.
- Los compañeros son autónomos y no asignables por UI.
- `EMERGENCIA_SECTA` es permiso temporal, no llave universal.
- Los seis atajos son opcionales y 6/6 no genera crisis perfecta.
- M16 no concede Comprensión.
- M16 cierra sólo cuando ningún frente está `PENDIENTE`.
- Al cerrar:
  - `M16=HECHA`;
  - `EMERGENCIA_SECTA=EXPIRADA`;
  - M17 queda disponible derivada;
  - `arc1.estado=LIV_CRISIS` permanece hasta transición propia de M17.
- M16 NO abre `PASO_PULSO`.
- M16 NO concede `NUCLEO_PROFUNDO`.
- M16 NO confirma R7 ni R10.
- M16 NO decide LIBERAR/CUSTODIAR.
- No modificar `ROOMS.exits`.

## DHP-1 — trazabilidad de T281

Auditoría 6 registra que T281 es la única versión de M16 localizada en la Fuente Maestra ver55.

Para este cierre se adopta explícitamente:

`T281 = VERSION_UNICA_LOCALIZADA_Y_AUTORIDAD_M16`

T260 se conserva como contexto histórico y sólo complementa donde no contradice a T281.

## Decisiones técnicas pendientes

### DT-M16-01 — apoyos externos por frente

La formulación REV1:

`máximo uno o dos apoyos externos importantes por frente`

NO es canon literal de T281.

Se clasifica desde este cierre como:

`DECISION_TECNICA_3C7_AUDITAR`

El contrato puede mantenerla, modificarla o sustituirla por otra regla de resiliencia, siempre que:

- no cree dependencias absolutas entre frentes;
- no genere dominó de resultados;
- no introduzca soft-lock;
- preserve la semántica de apoyo moderado de T281.

### DT-M16-02 — atribución "resuelto por quién"

El estado terminal del frente permanece como única fuente de verdad:

`frentes[ID] = PENDIENTE | ESTABLE | COSTOSO | DAÑADO`

Queda pendiente decidir si la atribución histórica:

`resuelta_por_<companero>`

se conserva como **metadato separado del estado** o se descarta explícitamente.

Prohibido reintroducir un booleano paralelo que duplique la condición de resolución.

Si se conserva, el modelo preferido para auditoría técnica será semánticamente equivalente a:

`frentesMeta[ID].resueltoPor = JUGADOR | COMPANERO:<id> | EQUIPO:<id> | SISTEMA`

El nombre/shape exacto NO queda congelado en este cierre.

## Riesgo futuro no bloqueante

CRISIS_RUTAS deberá revisarse contra el sistema de postas/carruajes si ese sistema llega a producción jugable.

No ampliar M16 ahora por esta razón.

## Test adicional obligatorio para futuro contrato

Añadir explícitamente:

`0 requisiciones opcionales + 0 únicos + pocos atajos => M16 sigue completable`

## Pendientes antes de implementación

1. disparador concreto M16;
2. regla final de cardinalidad/fases de intervención;
3. evaluadores concretos por frente;
4. conexiones que aceptan `EMERGENCIA_SECTA`;
5. modelo global de permisos;
6. movilidad/anclajes de emergencia;
7. balance numérico;
8. DT-M16-01;
9. DT-M16-02;
10. runtime predecesor aprobado de 3C.6 y contratos anteriores.

## Prohibiciones

- No implementar todavía.
- No hacer merge.
- No avanzar M17 dentro de este cierre.
- No reabrir M16 por las dos decisiones técnicas pendientes salvo que una decisión futura contradiga T281 o cree un soft-lock.

## Marca final

`3C7A_M16_REV1_CERRADA_DOCUMENTALMENTE_APTA_CON_DECISION_TECNICA_PENDIENTE`
