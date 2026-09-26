# Qiao Ren — baseline avanzado / LAB v0.1

## Objetivo

Primer NPC canónico probado con el stack avanzado:

```text
Scheduler
→ Memory/Relations
→ Utility
→ GOAP
→ Execution Session
```

No se integra a producción.

## Canon relevante

- autoridad;
- Disciplina y Administración;
- ruta Disciplina → Interior → Consejo;
- gate canónico `SECTA_INTERIOR`;
- M16: coordinación institucional;
- M17: debe autorizar una excepción que habilita `NUCLEO_PROFUNDO`.

## Perfil numérico

Los traits y relación con jugador usados por Utility son de calibración:

`EXPERIMENTAL_NON_CANONICAL`

No deben convertirse en personalidad canónica por efecto del test.

## Escenarios

### 1. Deber institucional ordinario

Expectativa del stack:

```text
Utility: trabajar
→ goal FULFILL_DUTY
→ GOAP plan
→ cumplir_deber
→ dutySatisfied=true
```

### 2. Coordinación M16 con evidencia disponible

Contexto experimental compatible con el rol canónico de coordinación.

Expectativa:

```text
Utility: informar_superior
→ goal REPORT_SUPERIOR
→ GOAP plan ejecutable
```

No se afirma que "informar superior" sea literalmente la acción canónica de M16; es una abstracción experimental del laboratorio.

### 3. Retorno al puesto

Expectativa:

```text
Utility: regresar_puesto
→ goal RETURN_POST
```

## Gap canónico detectado — M17

El canon exige:

```text
Qiao Ren autoriza una excepción
→ habilita NUCLEO_PROFUNDO
```

El vocabulario GOAP actual no contiene una acción ni effect para representar esa autorización.

Por tanto:

`M17 authorization = CANONICAL_REQUIREMENT_CAPABILITY_GAP`

Este hueco NO debe cerrarse inventando comportamiento dentro del test. Si más adelante queremos que Qiao ejecute M17 mediante el stack autónomo, habrá que diseñar explícitamente la capacidad institucional correspondiente y auditarla.

## Límite adicional

El stack autónomo actual tampoco implementa pathfinding/gates físicos, por lo que `SECTA_INTERIOR` se conserva como canon pero no se ejecuta en este baseline.

## Estado

`QIAO_REN_ADVANCED_BASELINE: CANDIDATE_PENDING_RUNTIME_RUN`
