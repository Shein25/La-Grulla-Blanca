# Tercera revisión independiente — Adaptive Ecology v0.1 REV3

Revisá:

`ESPECIFICACION_ADAPTIVE_ECOLOGY_v0.1_REV3.md`

**No implementes código todavía.**

REV3 incorpora los bloqueantes de la segunda revisión:

1. locality se valida antes de dedup;
2. `occurredAt` fue eliminado de v0.1;
3. la garantía limitada de `recentEventIds` está documentada explícitamente;
4. poda de dedup = FIFO por orden de aplicación;
5. la justificación de no hysteresis fue reescrita: se posterga porque hoy no existe consumidor real de tier/effectiveKit;
6. se anota para v0.2 el riesgo de cambiar effectiveKit a mitad de encuentro;
7. `effectiveKit` usa orden canónico por ID ASCII normalizado;
8. el resolver no filtra silenciosamente abilities “desconocidas”, porque no recibe un catálogo autoritativo; sólo valida el shape del ID;
9. `INVALID_POPULATION` queda separado de `DUPLICATE_EVENT`;
10. se agregaron Goldens para locality-vs-dedup, replay tras poda, FIFO, duplicate+decay y canonical kit.

## Objetivo de esta pasada

Decidir si el contrato ya es suficientemente cerrado para construir el laboratorio experimental.

No busques balance fino. Buscá defectos de contrato que harían que dos implementadores razonables construyan motores distintos o que permitirían estado invisible/inconsistente.

## Revisá especialmente

- locality antes de dedup;
- semántica de duplicate cuando elapsedTime > 0;
- ventana acotada de dedup y replay después de poda;
- FIFO;
- source of truth;
- `now` / `lastUpdate`;
- aritmética entera y overflow;
- thresholds;
- orden canónico del effectiveKit;
- validación de IDs;
- idempotencia;
- configuración recalibrada;
- ausencia de hysteresis en esta etapa;
- frontera futura con Monster Combat AI.

## Formato obligatorio

### 1. Veredicto

Usá exactamente uno:

`ADAPTIVE_ECOLOGY_V01_REV3_APTA_PARA_IMPLEMENTAR`

`ADAPTIVE_ECOLOGY_V01_REV3_REQUIERE_CAMBIOS`

`ADAPTIVE_ECOLOGY_V01_REV3_FALLO_CONCEPTUAL

### 2. Bloqueantes
### 3. No bloqueantes
### 4. Escenarios adversariales
### 5. Contradicciones internas
### 6. Evaluación final de dedup
### 7. Evaluación final de tiempo/decay
### 8. Evaluación final de source of truth
### 9. Goldens faltantes
### 10. Contrato final recomendado
### 11. Conclusión
Si no encontrás bloqueantes reales, no inventes cambios por preferencia estética.

No implementes nada.
No crees ramas.
No modifiques GitHub.
