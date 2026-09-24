# Experimentos — Memoria de NPC

Familia experimental dedicada a memoria semántica y estado persistente de NPC ficticios.

## Línea actual

`motor-npc-vivo-v0.3-memory/`

La primera iteración es **v0.3.0**.

## Objetivo

Probar una memoria:

- semántica y selectiva, no un log infinito de turnos;
- determinista;
- acotada por capacidad;
- con expiración explícita opcional;
- sin mutar inputs;
- endurecida contra accessors e inputs heredados básicos;
- totalmente aislada de NPC, rooms, misiones y conocimiento canónicos.

## Secuencia prevista

```text
v0.3.0  núcleo de memoria
   ↓
v0.3.1  memoria → relaciones/estado derivado
   ↓
v0.3.2  memoria → Utility AI → GOAP
```

La numeración posterior es una guía de laboratorio, no una obligación de implementación.

## Regla

La memoria no define verdad canónica. Sólo conserva experiencias o hechos que otra capa válida le haya entregado.
