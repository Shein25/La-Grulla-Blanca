# Handoff — Motor NPC Vivo v0.1.1 apto para GOAP

Fecha: 2026-09-23

## Hito cerrado

Motor NPC Vivo v0.1.1 queda congelado como base experimental para diseñar GOAP.

PR #1:
`experiment/motor-npc-v0.1.1` → `main`

Commit auditado:
`8249378a0c572799a051d8d024f8567f8fec63eb`

Merge squash:
`404411f09c0e110f02c92689ffeb1a3c69a213ab`

Veredicto:
`V011_APTO_PARA_GOAP`

## Invariantes del laboratorio

- determinista para inputs válidos;
- Utility AI explicable con score/raw/contribuciones;
- snapshots internos planos y validados;
- sin lecturas tardías del input externo durante cálculo;
- finitud protegida;
- `nextNpc` independiente;
- inercia decreciente;
- `dutyMode` como precondición experimental;
- reglas de conocimiento preservadas.

## No es producción

No está conectado a `grulla-blanca_ver73.html`.
No usa los 32 NPC canónicos.
No implementa misiones.
No implementa GOAP todavía.

## Deuda menor

Sanitizar el formateo de mensajes de error para valores externos como `Symbol` u objetos con coerción hostil.

No es bloqueante para iniciar v0.2 experimental.

## Próxima arquitectura

```text
Utility AI
  └─ selecciona objetivo

GOAP
  └─ construye plan con hechos, precondiciones, efectos y coste

Executor
  └─ ejecuta paso, verifica resultado y provoca replanning si corresponde
```

Mantener esta separación. No convertir `dutyMode` en sustituto del planner.
