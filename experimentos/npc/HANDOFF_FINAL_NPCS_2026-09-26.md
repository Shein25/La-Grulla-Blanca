# HANDOFF FINAL — NPCs · laboratorio de comportamiento y autonomía

**Fecha:** 2026-09-26  
**Estado:** CERRADO PARA HANDOFF DE INTEGRACIÓN  
**Snapshot autoritativo de cobertura:** `snapshot/handoff-2026-09-25-npc-complete`  
**Commit de cierre de cobertura:** `adc086ba5aca8d2a98c63f2df742ac019a498fea`

## 1. Alcance cerrado

El laboratorio de NPCs se considera terminado para esta etapa.

Se cerró:

- cobertura de los 32 NPC canónicos de ver74;
- baseline reproducible de comportamiento para 32/32;
- comparación de FSM / Behavior Tree / Utility según el caso;
- uso experimental de Memory, Relations, Utility, GOAP y Execution donde corresponde;
- identificación explícita de gaps de dominio;
- separación entre CANON y POLÍTICA EXPERIMENTAL.

Este cierre NO integra IA en `ver74`.

## 2. Cobertura

```text
Autoridades     7/7
Intermedios     7/7
Funcionales    12/12
Compañeros      6/6
TOTAL          32/32 NPC
```

Pruebas de baseline:

```text
Autoridades    88/88
Intermedios    74/74
Funcionales    89/89
Compañeros     85/85
TOTAL         336/336 PASS

Suite canónica transversal 15/15 PASS
```

## 3. Fuente de verdad

La cobertura completa y la matriz de arquitecturas probadas están en:

- `snapshot/handoff-2026-09-25-npc-complete`
- `experimentos/npc/canonical-behavior-lab-v0.1/README.md`
- `experimentos/npc/canonical-behavior-lab-v0.1/MATRIZ_NPC_ARQUITECTURAS_v0.1.md`

El snapshot conserva el laboratorio canónico completo aunque esa carpeta no esté copiada en la rama actual de Grulla.

## 4. Regla arquitectónica congelada

NO existe una regla que obligue a los 32 NPC a usar la misma IA.

Contrato:

```text
cada NPC
→ usar el motor más simple que cubra correctamente su comportamiento
```

Los baselines probados son evidencia, no asignación definitiva automática.

Ejemplos ya probados:

- FSM mínima/eventos para presencia, rutina o estados categóricos simples;
- Behavior Tree para preempción reactiva clara;
- Utility para decisiones ponderadas;
- Utility + GOAP + Execution cuando existe objetivo y plan simbólico;
- Memory/Relations sólo cuando la conducta realmente depende de historia social.

## 5. Componentes experimentales disponibles

```text
Utility AI v0.1.1
GOAP v0.2.2
Memory v0.3
Relations v0.3.1
Decision Pipeline v0.3.2
NPC Lifecycle / Scheduler v0.1
Execution + Replanning v0.1
Autonomous NPC Loop v0.1
```

Utility AI v0.1.1 tiene cierre auditado histórico:

```text
V011_APTO_PARA_GOAP
44 PASS / 0 FAIL
5 stress × 10.000 PASS
```

## 6. Advertencia sobre GOAP / Autonomous Loop

El repositorio conserva evidencia fuerte de tests y stress para las capas posteriores, pero NO existe en la rama actual un informe independiente final que autorice declarar `Autonomous NPC Loop v0.1` como motor productivo universal.

Por tanto:

```text
BASELINES NPC              CERRADOS
STACK EXPERIMENTAL         DISPONIBLE
ARQUITECTURA ÚNICA GLOBAL  NO SELECCIONADA
PRODUCCIÓN                 NO INTEGRADA
```

El agente integrador puede reutilizar estas capas, pero no debe presentar el Autonomous Loop como arquitectura obligatoria para todos los NPC.

## 7. Gaps de dominio preservados

Los siguientes gaps están documentados y pasan al agente de integración/dominio:

1. `KNOWLEDGE_SCHEMA_R1_TO_R10` completo;
2. navegación física real por rooms, rutas y gates;
3. executor de combate/seguridad para intents marciales;
4. `RESOURCE_ALLOCATION_AND_LOGISTICS`;
5. `ARCHIVE_PROTECTION_AND_CATALOG_STATE`;
6. `MEDICAL_TRIAGE_AND_TREATMENT_STATE`;
7. `FORMATION_NETWORK_STATE_AND_REPAIR`;
8. asignación de frentes M16 y responsables disponibles;
9. permisos institucionales (`ARCHIVO_RESTRINGIDO`, `NUCLEO_PROFUNDO`, etc.);
10. guardias para decisiones irreversibles;
11. mapeo de acciones sociales Utility a ejecución real;
12. estado de mundo de dominio y consecuencias físicas.

Estos gaps NO invalidan los baselines: fueron deliberadamente preservados para no inventar capacidad.

## 8. Qué no debe reinterpretar el agente integrador

- identidad, rol, rooms, rutas, anclajes y conocimiento canónico de NPC_DEF;
- los 32/32 baselines ya comprobados;
- la separación CANON / POLÍTICA EXPERIMENTAL;
- la regla de usar el motor más simple suficiente;
- las guardias documentadas para decisiones irreversibles;
- los gaps de dominio como si ya estuvieran resueltos.

## 9. Qué sí corresponde al agente integrador

- seleccionar por NPC la arquitectura mínima adecuada;
- conectar rooms/gates/pathfinding reales;
- implementar las capas de dominio que cada NPC necesita;
- conectar combate cuando proceda;
- mapear intents a acciones reales;
- conectar scheduler/dormancy/activación al runtime productivo;
- integrar memoria/relaciones sólo donde el diseño lo requiera;
- ejecutar regresión sobre ver74.

## 10. Estado final

```text
NPC CANÓNICOS / MOVILIDAD 3C.5    CERRADO
COBERTURA DE COMPORTAMIENTO       32/32 CERRADA
BASELINES                         336/336 PASS
SUITE CANÓNICA                    15/15 PASS
ARQUITECTURAS PROBADAS            DOCUMENTADAS
GAPS DE DOMINIO                   DOCUMENTADOS

INTEGRACIÓN IA PRODUCTIVA         PENDIENTE — OTRO AGENTE
TRABAJO DE DISEÑO AQUÍ            NINGUNO
```