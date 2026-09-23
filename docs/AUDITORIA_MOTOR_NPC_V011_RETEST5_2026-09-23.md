# Auditoría Motor NPC Vivo v0.1.1 — Retest 5

Fecha: 2026-09-23

## Estado

Resultado externo final: `V011_APTO_PARA_GOAP`.

Commit auditado de la rama experimental:

`8249378a0c572799a051d8d024f8567f8fec63eb`

PR #1 mergeado por squash a `main`:

`404411f09c0e110f02c92689ffeb1a3c69a213ab`

## Evidencia de cierre

- suite oficial: 44 PASS, 0 FAIL;
- cinco stress tests de 10.000 casos: PASS;
- snapshot interno validado contra TOCTOU/Proxy;
- `Proxy.get` adversarial no ejecutado durante cálculo;
- descriptor dinámico revalidado por cada llamada pública;
- `simulateTurn()` clona el snapshot validado, no el input externo;
- 26/26 campos obligatorios con `undefined` rechazados;
- 32/32 combinaciones de accessors rechazadas sin ejecutar getter/setter;
- estados heredados y topic IDs espurios rechazados;
- finitud preservada para acciones disponibles y disclosure;
- `nextNpc` profundamente independiente;
- desempate `score → raw → ACTION_ORDER` preservado;
- inercia `+6 → +4 → +2 → +0` preservada;
- `dutyMode` preservado;
- escenarios de aceptación preservados;
- tres personalidades siguen diferenciándose;
- `DESCONOCIDO` nunca revela;
- `SOSPECHA` nunca llega a `COMPARTE`.

## Deuda menor no bloqueante

La auditoría observó que un valor inválido como `Symbol('x')` puede hacer que el formateo del mensaje de error lance `TypeError` al interpolar el valor externo.

Esto no permite que la entrada inválida pase el validador ni produzca una decisión o disclosure inválido. Se registra como hardening de mensajes de error para v0.2; no se modificó la candidata después de la auditoría para preservar la correspondencia exacta con el commit aprobado.

## Alcance del merge

El merge incorpora únicamente el laboratorio experimental de Motor NPC Vivo v0.1.1.

No integra el motor en `grulla-blanca_ver73.html`, no modifica el baseline del juego, no convierte fixtures ficticios en NPC canónicos y no implementa GOAP.

## Próximo paso

Diseñar v0.2 experimental con separación estricta:

```text
Utility AI → selecciona OBJETIVO
GOAP       → construye PLAN
Executor   → aplica acciones y verifica efectos
```

La integración con los 32 NPC canónicos queda fuera de este hito.
