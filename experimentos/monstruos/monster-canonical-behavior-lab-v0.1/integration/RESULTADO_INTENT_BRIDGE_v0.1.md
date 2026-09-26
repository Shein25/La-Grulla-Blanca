# Resultado — Canonical Intent Bridge v0.1

## Verificación

```text
PASS: 11
FAIL: 0
```

Cobertura:

- 18/18 combatientes;
- rondas 1..12;
- `CADENCE_COMPAT` produce básico/técnica exactamente según `round % tecnica.cada`;
- telegraph reproduce `(round + 1) % tecnica.cada === 0`;
- payload de técnica conserva íntegro el objeto canónico;
- veneno, quemadura y drenaje de qi no se reinterpretan;
- intención de técnica fuera de cadencia lanza `CADENCE_VIOLATION`;
- mob sin técnica no puede bindear técnica;
- abilities desconocidas son rechazadas;
- órdenes resultantes quedan deep-frozen;
- snapshot MOBS permanece inmutable.

## Frontera

```text
Monster AI
→ intent
→ Canonical Intent Bridge
→ BASIC_ATTACK | TECHNIQUE
→ [executor productivo todavía externo]
```

El bridge no tira dados ni aplica efectos.

## Estado

`CANONICAL_INTENT_BRIDGE_V01: 11_PASS_0_FAIL_CONFIRMED`
