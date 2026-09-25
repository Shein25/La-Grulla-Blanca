# Auditoría documental independiente — 3C.7A M16 REV1 · "Cuando falla el centro"

**Auditor:** Claude (solo lectura)
**Snapshot documental auditado:** `f575a45f322575680f972e2313c1bfadbf73616d`
**Verificación de integridad:** `MANIFEST_SHA256.txt` — 18/18 archivos OK.
**Documento auditado:** `docs/3C7A/Reconciliacion_3C7A_M16_REV1.md` + `docs/3C7A/Matriz_Implementacion_3C7A_M16_REV1.json`
**Jerarquía aplicada:** T281 > T260 > T257 > Auditoría 6 > ver74/3C.5 > cierre M13–M15 REV2.

## Resultado ejecutivo

No se detectaron bloqueantes.

- No hay contradicción con T281/T260/Auditoría 6/ver74.
- No hay soft-lock nuevo.
- No hay canon inventado.
- Las 21 rooms candidatas citadas existen en ver74.
- No se adelanta M17, R7, R10, NUCLEO_PROFUNDO ni LIBERAR/CUSTODIAR.
- El reemplazo de seis booleanos paralelos por un estado enumerado único por frente es una mejora estructural legítima y compatible con idempotencia.

## Hallazgos moderados no bloqueantes

### DT-M16-01 — límite de apoyos externos

La regla REV1 “máximo uno o dos apoyos externos importantes por frente” no es literal de T281.

Debe tratarse como:

`DECISION_TECNICA_3C7_AUDITAR`

y no como canon fuente.

### DT-M16-02 — atribución de resolución

Auditoría 6 conserva semántica de atribución del tipo:

`crisis_<frente>_resuelta_por_<companero>`

El modelo enum único de REV1 no define aún si “quién resolvió” se conserva o descarta.

Debe decidirse explícitamente antes de implementar, evitando reintroducir una segunda fuente de verdad para el estado terminal del frente.

Opciones compatibles:
- conservar atribución como metadato/subcampo independiente del estado;
- descartarla explícitamente si no se necesita para HISTORY/diálogos posteriores.

## Hallazgos menores

- T281 es la única versión de M16 localizada en la Fuente Maestra; conviene registrar DHP-1 por trazabilidad.
- Riesgo futuro de acoplamiento RUTAS ↔ postas/carruajes debe arrastrarse como nota cuando exista fast travel jugable.

## Verificación por frente

MEDICINA, RUTAS, FORMACIONES, RECURSOS, SAUCES y JARDINES resultaron consistentes con T281/T260/Auditoría 6 y con rooms reales de ver74.

En todos los casos:
- no hay puerta oculta obligatoria;
- DAÑADO no bloquea progresión;
- las rooms son anclajes candidatos, no checklist.

## Activación y cierre

Confirmado:
- M16 no se activa en el cierre de M15;
- el disparador exacto puede quedar como decisión técnica precontrato;
- seis frentes nacen PENDIENTE;
- EMERGENCIA_SECTA se activa;
- todos los frentes deben ser terminales para cerrar;
- al cerrar expira EMERGENCIA_SECTA;
- M17 queda disponible derivada;
- arc1.estado sigue LIV_CRISIS;
- PASO_PULSO y NUCLEO_PROFUNDO siguen cerrados;
- R7/R10 no se confirman;
- LIBERAR/CUSTODIAR no se decide.

## Persistencia e idempotencia

Compatible y aprobada la propuesta:

`flags.arc1.crisisM16.frentes[ID] = PENDIENTE | ESTABLE | COSTOSO | DAÑADO`

Los antiguos booleanos de “resuelta” deben ser derivados, no una segunda persistencia.

`resolverFrente(id)` es one-shot e idempotente.

Save/load no debe disparar, resolver, reasignar, recalcular, reactivar ni repagar nada.

## Soft-lock

No se identificó ningún vector de soft-lock sin cubrir.

Debe añadirse como test futuro explícito:

`0 requisiciones opcionales + 0 únicos + pocos atajos => M16 sigue completable`

## Veredicto

`3C7A_M16_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

## Límite

NO IMPLEMENTAR. NO AVANZAR M17 hasta registrar este cierre y sus decisiones técnicas pendientes.
