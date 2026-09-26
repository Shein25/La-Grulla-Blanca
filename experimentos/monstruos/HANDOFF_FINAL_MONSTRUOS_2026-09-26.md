# HANDOFF FINAL — Monstruos · IA, adaptación y comportamiento canónico

**Fecha:** 2026-09-26  
**Estado:** CERRADO PARA HANDOFF DE INTEGRACIÓN  
**Snapshot histórico de cierre:** `snapshot/handoff-2026-09-25-monsters-complete`  
**Commit de cierre feedback-loop:** `289a090b83f2e0f3652c93c870f88ec2c4256bc4`

## 1. Alcance cerrado

El laboratorio general de monstruos queda cerrado para esta etapa.

Se cerró:

- kernel de decisión Monster Combat AI congelado;
- conexión con los MOBS reales de ver74;
- cobertura candidata de los 18 combatientes;
- Tactical Overlay;
- Canonical Intent Bridge;
- Semantic Memory Recorder;
- Resolved Combat Signal Adapter;
- Combat Feedback Loop;
- hooks estructurados de absorción/recuperación en copia de ver74;
- supervivencia adaptativa E1;
- progresión/ceiling;
- modelo poblacional `C_STAGGERED`;
- decay con hitos irreversibles;
- techo de aprendizaje real.

El boss Grulla tiene un handoff propio y no se redefine aquí.

## 2. Canon y cobertura

Snapshot canónico:

`canonical/MOBS_ver74.snapshot.json`

```text
MOBS totales             19
combatientes con IA      18
muñeco de práctica        1 excluido
```

Las 18 criaturas tienen perfil cognitivo/social candidato experimental.

Distribución:

```text
INSTINTIVO   4
REACTIVO_1   5
CAZADOR_2    5
TACTICO_3    3
MASTER_4     1
TOTAL       18
```

Estas asignaciones son candidatas experimentales, NO canon narrativo de inteligencia.

## 3. Estado funcional cerrado

El snapshot de cierre dejó:

```text
canon transversal         13/13
baseline representativo   18/18
18 combatientes           15/15
tactical overlay          14/14
intent bridge             11/11
semantic memory           12/12
resolved signal adapter   13/13
feedback loop             11/11
TOTAL                    107/107 PASS
```

Estado declarado:

`MONSTER_LAB_STATUS: CLOSED_FEEDBACK_LOOP_CONFIRMED`

Posteriormente se cerraron hooks estructurados de ver74:

```text
absorción -> adapter -> memoria       PASS
recuperación qi exacta                PASS
recuperación hp con cap               PASS
recovery hook -> memoria              PASS
emisión después de round increment    PASS
TOTAL                                 5/5 PASS
```

## 4. Cadencia productiva

`CADENCE_COMPAT` continúa siendo autoridad.

```text
round % tecnica.cada === 0
```

La IA experimental no debe adelantar, retrasar ni saltar técnicas canónicas en producción salvo una decisión futura explícita.

`DECISION_EXPERIMENTAL` es laboratorio, no comportamiento productivo automático.

## 5. Modelo adaptativo seleccionado

Modelo seleccionado:

`C_STAGGERED`

No reabrir A vs B vs C salvo invalidación concreta.

```text
T0 NATURAL
T1 SUPERVIVENCIA
T2 RECONOCIMIENTO
T3 CONTRAADAPTACIÓN
T4 ADAPTACIÓN MADURA
```

Stats acumulativos:

```text
T1 HP×1.025 daño×1.025
T2 HP×1.05  daño×1.05  HIT+1
T3 HP×1.075 daño×1.075 HIT+1 EVA+5
T4 HP×1.10  daño×1.10  HIT+1 EVA+5 CRIT 5→10%
```

Thresholds de presión:

```text
T0  0–19
T1 20–44
T2 45–69
T3 70–89
T4 90–100
```

Referencia de muertes efectivas:

```text
T1 ~10
T2 ~25
T3 ~50
T4 ~90
```

## 6. Unidad de adaptación

```text
populationId = territoryId + speciesId
```

No existe aprendizaje telepático global de especie.

Persistencia mínima prevista:

```text
populationId
speciesId
territoryId
pressure
maxTierReached
lastUpdate
recentEventIds
```

No crear `survivalXp` productivo paralelo.

## 7. Decay / consolidación

Campo histórico:

`maxTierReached`

Pisos:

```text
max T0 -> floor T0
max T1 -> floor T1
max T2 -> floor T1
max T3 -> floor T2
max T4 -> floor T3
```

`floorTier`, `pressureTier` y `effectiveTier` son derivados y no deben persistirse.

## 8. Ceiling de aprendizaje

`adaptiveCapabilityCeiling` limita lo que la población puede APRENDER, no sólo manifestar.

```text
playerStage < nativeStage      -> T0
playerStage == nativeStage     -> T1
+1 etapa                       -> T2
+2 etapas                      -> T3
+3 etapas                      -> T4
```

Caps de presión:

```text
T0 19
T1 44
T2 69
T3 89
T4 100
```

Subir de etapa no revela tiers precargados; hace falta nueva presión.

## 9. Supervivencia E1

Los 18 combatientes tienen una familia defensiva experimental:

```text
ESQUIVA       7
DEFENSA       3
MITIGACIÓN    3
ABSORCIÓN     5
```

Contratos:

```text
EVADE_NEXT
DEFENSE_UP
ABSORB_RESERVE
MITIGATE_NEXT
```

La identidad de especie debe conservarse: una población adaptada sigue siendo la misma especie.

## 10. Qué no debe reinterpretar el agente integrador

- `CADENCE_COMPAT`;
- `C_STAGGERED`;
- thresholds 0–19 / 20–44 / 45–69 / 70–89 / 90–100;
- ceiling como techo de aprendizaje real;
- `maxTierReached` y pisos de decay;
- unidad poblacional territorio+especie;
- no crear un XP paralelo;
- stats escalonados T1–T4;
- perfiles/overlays como experimentales, no canon narrativo;
- el boss Grulla, que usa su propio handoff.

## 11. Trabajo que pasa al agente integrador

Lo pendiente es productivo/integración, no rediseño del laboratorio:

- persistir Population State en el save/runtime apropiado;
- construir bridge `Population State -> effective adaptive tier -> effectiveKit`;
- ejecutar `EVADE_NEXT`, `DEFENSE_UP`, `ABSORB_RESERVE`, `MITIGATE_NEXT` usando el motor real;
- conectar señales reales de combate;
- conectar memoria persistente de patrones;
- integrar multi-enemigo/unión ecológica sin romper las reglas existentes;
- asignar/adaptar perfiles por monstruo en producto;
- ejecutar regresión contra ver74.

## 12. Hooks de integración disponibles

Ya existe evidencia dirigida para:

- absorción resuelta estructurada;
- recuperación HP/Qi estructurada;
- adapter de señales;
- semantic memory;
- intent bridge;
- feedback loop.

No parsear logs ni reconstruir deltas leyendo estado posterior.

## 13. Estado final

```text
MONSTER COMBAT AI              CERRADA
BESTIARIO 18/18                CUBIERTO
TACTICAL OVERLAY               CERRADO
INTENT BRIDGE                  CERRADO
SEMANTIC MEMORY                CERRADA
RESOLVED SIGNAL ADAPTER        CERRADO
COMBAT FEEDBACK LOOP           CERRADO
VER74 STRUCTURED HOOKS         5/5 PASS
C_STAGGERED                    SELECCIONADO / CONGELADO
DECAY + MAX TIER               CERRADO
LEARNING CEILING               CERRADO
SURVIVAL E1                    CERRADA COMO CONTRATO EXPERIMENTAL

INTEGRACIÓN PRODUCTIVA         PENDIENTE — OTRO AGENTE
TRABAJO DE DISEÑO AQUÍ         NINGUNO
```