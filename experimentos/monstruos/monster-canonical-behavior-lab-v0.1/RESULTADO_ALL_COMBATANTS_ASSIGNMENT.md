# Cobertura candidata 18/18 — Monster Canonical Behavior Lab v0.1

## Matriz

Las 18 criaturas combatientes canónicas tienen ahora una asignación cognitiva/social **experimental**.

El muñeco de práctica queda excluido explícitamente.

## Qué demuestra esta fase

- ningún combatiente queda sin perfil candidato;
- todos los profile IDs existen;
- todos los social profile IDs existen;
- los 18 entran en `DECISION_EXPERIMENTAL`;
- las 16 criaturas con técnica reciben básico + técnica en ronda canónica;
- rata_qi y eco_caido, sin técnica, sólo reciben básico;
- las ventanas de memoria se ajustan al perfil;
- mismo input + seed sigue siendo determinista.

## Qué NO demuestra

La memoria y lo social todavía no afectan los scores canónicos.

Dos comprobaciones explícitas:

```text
guardian_coral:
memory=[] vs memory activa
→ mismos scoreByAbility

lobo_espiritual:
solo vs manada
→ mismos scoreByAbility
```

La razón es deliberada:

```text
signalWeights = {}
memoryWeights = {}
socialWeights = {}
```

Por tanto, esta fase completa la **asignación de capacidad cognitiva candidata**, pero no la táctica adaptativa.

## Próxima capa

Hace falta un overlay táctico experimental que:

1. no toque MOBS;
2. no cambie cadencia canónica;
3. use señales observables;
4. use memoria semántica real o claramente sintética;
5. use flags sociales sólo donde corresponda;
6. permita medir cuándo una criatura realmente cambia de decisión.

## Estado

`ALL_COMBATANTS_ASSIGNMENT_BASELINE: PENDING_CONFIRMATION`
