# Resultado — readiness de integración Grulla → ver74 v0.1

**Fecha:** 2026-09-26  
**Estado:** INTEGRATION-READY EN LABORATORIO / NO APLICADO A PRODUCTO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Estado del balance

```text
FASE I       CERRADA
FASE II      CERRADA
FASE III     CERRADA
ENCUENTRO    CERRADO
```

No quedan tareas de recalibración para esta integración.

## 2. Estado de la rama productiva disponible

La rama conocida:

`implement/3c5-npc-ver74`

declara en su guardia alcance exclusivo de 3C.5 NPC/movilidad.

Por tanto el boss NO fue escrito allí.

También permanecen intactos:

```text
main
ROOMS.exits
GATES_329
SAVE_SCHEMA_VERSION
CADENCE_COMPAT de monstruos genéricos
```

## 3. Runtime de encuentro preparado

Archivo:

`integration/grulla-encounter-runtime-contract-v0.1.mjs`

Congela en código:

- pools 150 / 100 / 50;
- ATQ/DEF por fase;
- todos los dados/bonos cerrados;
- CHAIN_A;
- M_A;
- Piel G345_D1;
- Resonancia x1,75;
- requisito committed de Romper Ritmo.

## 4. Adaptador de acciones del jugador

Archivo:

`integration/grulla-player-action-adapter-v0.1.mjs`

Normaliza únicamente acciones ya resueltas:

```text
BASIC
DEFEND
RECOVER
TECHNIQUE
CONTROL
```

No parsea logs y no inventa elemento de técnicas híbridas.

## 5. Gate previo de técnicas

Archivo:

`integration/grulla-technique-gate-v0.1.mjs`

Separa correctamente:

```text
PRE-RESOLUTION
consulta si la técnica ya está comprendida

POST-RESOLUTION
registra lo que realmente ocurrió
```

Esto conserva la regla cerrada:

```text
1ª entra
2ª entra
3ª entra y aprende
4ª consume qi pero se suprime
```

## 6. Session controller

Archivo:

`integration/grulla-encounter-session-v0.1.mjs`

Gestiona:

- fase actual;
- HP del pool actual;
- brain state;
- memoria resumida entre fases;
- Resonancia preparada;
- transición I→II→III;
- bloqueo de overkill entre pools.

## 7. Adaptador de combate especial ver74

Archivo:

`integration/grulla-ver74-special-combat-adapter-v0.1.mjs`

Discriminador local:

`grulla_boss_v01`

Este string NO es todavía `mobId` productivo.

El adaptador cubre:

- detección del combate especial;
- creación del estado trifásico;
- gate de técnicas;
- observación post-resolución;
- selección de intención enemiga;
- armado/consumo de Resonancia;
- aplicación de daño al pool;
- transición sin muerte prematura;
- derrota final sólo en Fase III;
- snapshot público sin memoria oculta.

## 8. Blueprint ver74

Documento:

`integration/GRULLA_VER74_INTEGRATION_BLUEPRINT_v0.1.md`

Se inspeccionó el `class Combate` real de `ver74` y se localizaron cuatro rutas de daño que deberán centralizarse para el boss:

```text
ATACAR básico
técnica ofensiva
daño de corte de Filamento
DOT enemigo
```

También se fijó el orden exacto del gate, observación, respuesta enemiga y cleanup.

## 9. Suites dirigidas preparadas

```text
tests/grulla-encounter-runtime-contract.test.mjs
tests/grulla-player-action-adapter.test.mjs
tests/grulla-technique-gate.test.mjs
tests/grulla-encounter-session.test.mjs
tests/grulla-ver74-special-combat-adapter.test.mjs
```

Comando:

`npm run test:grulla-integration-ready`

## 10. Estado de ejecución de tests

Los tests están escritos y registrados en `package.json`.

En esta sesión no existe CI GitHub asociado a los commits de la rama y el entorno local no puede materializar directamente los archivos del repositorio autenticado.

Por tanto:

```text
SUITE PREPARADA       SÍ
SUITE EJECUTADA AQUÍ  NO
PASS DECLARADO        NO
```

Antes de aplicar el parche al HTML debe ejecutarse la suite dirigida en la rama de integración.

## 11. Datos deliberadamente no inventados

Siguen pendientes de una decisión narrativa/productiva, no de balance:

```text
mobId real del boss
ubicación exacta
trigger de aparición/inicio
recompensa/loot
cadáver o no cadáver
flags posteriores
política de huida
unión o aislamiento respecto de otros combatientes
```

No deben inferirse desde los benchmarks.

## 12. Próximo gate

Para pasar de laboratorio a producto se necesita una rama cuyo alcance permita explícitamente la integración del boss.

En esa rama:

1. ejecutar `npm run test:grulla-integration-ready`;
2. aplicar el blueprint al HTML;
3. ejecutar pruebas históricas de combate;
4. ejecutar tests dirigidos otra vez contra el HTML modificado;
5. hacer QA manual de telegraphs y transiciones;
6. mantener valores congelados sin recalibrar.

## 13. Conclusión

```text
BALANCE                    CERRADO
CEREBRO                    CERRADO
RUNTIME CONTRACT           PREPARADO
PLAYER ACTION ADAPTER      PREPARADO
TECHNIQUE GATE             PREPARADO
SESSION CONTROLLER         PREPARADO
SPECIAL COMBAT ADAPTER     PREPARADO
VER74 PATCH BLUEPRINT      PREPARADO

PRODUCT HTML               SIN CAMBIOS
RAMA 3C.5                  SIN CAMBIOS
INTEGRACIÓN REAL           PENDIENTE DE RAMA AUTORIZADA
```