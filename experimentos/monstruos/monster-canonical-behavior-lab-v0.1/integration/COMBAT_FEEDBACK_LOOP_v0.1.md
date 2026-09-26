# Combat Feedback Loop v0.1

## Objetivo

Componer los componentes ya confirmados:

```text
Monster Combat AI
→ Canonical Intent Bridge
→ resolved combat signal
→ Semantic Memory Recorder
→ Monster Combat AI
```

sin ejecutar daño ni modificar producción.

## Caso determinista

Sujeto experimental:

`guardian_coral / TACTICO_3 / TERRITORIAL`

Ronda:

`round = tecnica.cada`

Contexto fijo:

- selfHp = 0.20;
- playerHp = 0.05;
- seed = 1.

### Sin memoria

```text
DECISION_EXPERIMENTAL
→ guardian_coral__technique
→ TECHNIQUE
```

### Feedback resuelto

Tres resultados reales normalizados:

```text
absorbido = 4
→ PLAYER_ABSORPTION_RESOLVED
→ DEFENSA_ABSORCION / EFECTIVA
```

en rondas 1, 2 y 3.

La técnica de control recibe:

```text
memory = -24
```

### Decisión posterior experimental

```text
guardian_coral__basic
→ BASIC_ATTACK
```

La memoria cambia una decisión real del kernel.

## Guardia de producción

La misma memoria bajo:

`CADENCE_COMPAT`

sigue produciendo:

```text
guardian_coral__technique
→ TECHNIQUE
```

porque la cadencia canónica restringe el effectiveKit antes de la decisión.

Por tanto:

- la adaptividad está demostrada;
- no puede saltarse la cadencia productiva;
- el bridge conserva el payload canónico;
- no se ejecuta daño en el laboratorio.

## Estado

`COMBAT_FEEDBACK_LOOP_V01: CANDIDATE_PENDING_TEST`
