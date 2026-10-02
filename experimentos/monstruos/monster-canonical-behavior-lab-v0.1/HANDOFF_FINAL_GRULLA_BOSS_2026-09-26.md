# HANDOFF FINAL — Grulla Boss · cierre experimental

**Fecha:** 2026-09-26  
**Estado:** CERRADO / LISTO PARA HANDOFF DE INTEGRACIÓN  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Alcance de este equipo/agente

El trabajo de este laboratorio termina aquí.

Este bloque cubrió:

- diseño del jefe trifásico;
- balance de Fase I;
- memoria/counterplay de Fase II;
- cerebro maestro de Fase III;
- anti-spam;
- validación de opcionales;
- stress de recursos;
- runtime/contratos de integración;
- tests dirigidos y blueprint de aplicación.

**NO corresponde a este agente integrar la IA en `ver74`.**

La integración de IA de NPCs, monstruos y jefes queda a cargo de otro agente.

## 2. Estado global congelado

```text
FASE I    EL VOTO INMÓVIL          CERRADA
FASE II   LAS ALAS RECUERDAN       CERRADA
FASE III  LA CAMPANA SIN DUEÑO     CERRADA

BALANCE                           CERRADO
MEMORIA                           CERRADA
COUNTERPLAY                       CERRADO
ANTI-SPAM                         CERRADO
OPCIONALES                        VALIDADAS
ZERO-QI                           VALIDADO
RUNTIME CONTRACT                  PREPARADO
BLUEPRINT DE INTEGRACIÓN          PREPARADO

VER74                             SIN CAMBIOS
INTEGRACIÓN PRODUCTIVA            NO REALIZADA
```

## 3. Contrato congelado del encuentro

### Fase I

```text
HP                150
ATQ               4
DEF               13
Golpe             1d6+2
Campanada         2d6+2
Pata Inmóvil      +3 DEF

Piel              G345_D1
Resonancia        x1,75
```

Resonancia:

```text
Pata Inmóvil
-> prepara el siguiente Golpe de Ala

si impacta con Piel activa:
    daño bruto x1,75
    luego Piel absorbe normalmente

si falla:
    Resonancia se consume igualmente
```

### Piel G345_D1

```text
Base              Guardia 3 / multiplicador 1 / reserva 3
Cobre endurecido  Guardia 4
Cobre flexible    +1 multiplicador
Cobre sobrio      coste -1
Aliento económico coste -1
Cobre grueso      Guardia 5
Placas continuas  +1 multiplicador

Flexible + Grueso Guardia 5 / reserva 10
```

### Fase II — CHAIN_A

```text
HP                100
ATQ               4
DEF               13

Golpe de Ala      1d4
Tormenta          1d6+1 / drain 1 qi
Cerrar Alas       ABS 3 / reserva 6
Recordar Filo     +10 EVA siguiente ofensiva
Eco Meridiano     drain 3 qi condicional
```

Memoria:

```text
3 usos consecutivos de una técnica
-> la Grulla la comprende

la siguiente repetición
-> queda suprimida

BASIC u otra técnica
-> rompe el lock

DEFENDER / RECOVER
-> NO rompen el lock
```

Counters cerrados:

```text
ofensiva      -> TRAZO VACÍO
esquiva       -> PULSO FIJADO
guardia       -> RESONANCIA INTERNA
control       -> ANCLA DEL VOTO
fortificación -> CAMPANA INVERSA
```

### Fase III — M_A

```text
HP                50
ATQ               4
DEF               13

Picotazo          +1 ATQ / 1d4+1
Campana           +1 ATQ / 1d6+2 / drain 2 qi
Ala Vacía         +10 EVA
Pata              +3 DEF
Romper Ritmo      +2 ATQ / 1d6+2
```

Política QA de referencia:

`MASTER_READER`

## 4. Contrato anti-spam global

```text
PURE SINGLE-SKILL       0% victoria completa
SPAM + DEFENDER         0% victoria completa
```

No debe relajarse al integrar.

## 5. Toolkit universal

El jugador debe poder superar el encuentro con:

```text
técnica raíz
ATACAR básico
DEFENDER
recursos normales
```

Paso, Piel y Filamento son opcionales y no deben convertirse en llaves obligatorias.

## 6. Archivos autoritativos

### Cierres

- `adaptive/CIERRE_GRULLA_FASE1_v0.1.md`
- `adaptive/CIERRE_GRULLA_FASE2_v0.1.md`
- `adaptive/CIERRE_GRULLA_FASE3_v0.1.md`
- `adaptive/CIERRE_GRULLA_BOSS_I_II_III_v0.1.md`

### Validaciones

- `adaptive/RESULTADO_GRULLA_FASE3_FINAL_VALIDATION_v0.1.md`
- `adaptive/CHECKPOINT_GRULLA_FASE1_G345D1_RESONANCIA_v0.1.md`

### Integración preparada

- `integration/grulla-encounter-runtime-contract-v0.1.mjs`
- `integration/grulla-player-action-adapter-v0.1.mjs`
- `integration/grulla-technique-gate-v0.1.mjs`
- `integration/grulla-encounter-session-v0.1.mjs`
- `integration/grulla-ver74-special-combat-adapter-v0.1.mjs`
- `integration/GRULLA_VER74_INTEGRATION_BLUEPRINT_v0.1.md`
- `integration/RESULTADO_GRULLA_INTEGRATION_READINESS_v0.1.md`

## 7. Tests preparados para el agente integrador

```text
tests/grulla-encounter-runtime-contract.test.mjs
tests/grulla-player-action-adapter.test.mjs
tests/grulla-technique-gate.test.mjs
tests/grulla-encounter-session.test.mjs
tests/grulla-ver74-special-combat-adapter.test.mjs
```

Comando:

`npm run test:grulla-integration-ready`

Estado:

```text
SUITE ESCRITA          SÍ
SUITE EJECUTADA AQUÍ   NO
PASS DECLARADO         NO
```

El agente integrador debe ejecutarla antes y después de aplicar el parche productivo.

## 8. Qué NO debe hacer el agente integrador

- no reabrir balance sin invalidación concreta;
- no volver a comparar A/B/C de adaptación;
- no cambiar G345_D1;
- no cambiar Resonancia x1,75;
- no cambiar DEF13 ni Pata +3 de Fase I;
- no cambiar CHAIN_A;
- no cambiar M_A;
- no cambiar HP 150/100/50;
- no transferir overkill entre fases;
- no hacer que la cuarta técnica sea gratis: consume qi aunque quede suprimida;
- no hacer que DEFENDER/RECOVER rompan el lock;
- no convertir Paso/Piel/Filamento en requisitos;
- no tocar `CADENCE_COMPAT` de otros monstruos;
- no mezclar este trabajo con 3C.5 NPC/movilidad.

## 9. Qué sí debe resolver el agente integrador

Estas decisiones quedaron fuera del laboratorio y siguen abiertas:

```text
mobId productivo del boss
ubicación narrativa exacta
trigger de aparición/inicio
loot/recompensa
cadáver o no cadáver
flags/misión posteriores
política de huida
aislamiento o unión con otros combatientes
```

Esas decisiones no deben alterar el contrato de combate congelado.

## 10. Rama de implementación

`implement/3c5-npc-ver74` tiene guardia de alcance exclusivo para 3C.5 NPC/movilidad.

Por eso este agente NO aplicó el boss allí.

El agente integrador debe trabajar únicamente en una rama cuyo alcance autorice explícitamente la integración del boss.

## 11. Criterio de cierre de este laboratorio

Este laboratorio se considera terminado porque:

1. las tres fases están balanceadas y cerradas;
2. memoria y counters están definidos;
3. anti-spam está validado;
4. opcionales están validadas;
5. stress cero-qi está validado;
6. el contrato ejecutable está preparado;
7. el adaptador de acciones está preparado;
8. el gate pre-resolución está preparado;
9. el session controller está preparado;
10. el adaptador de combate especial está preparado;
11. el blueprint productivo está documentado;
12. no queda trabajo de diseño/balance pendiente.

## 12. Estado final del handoff

```text
LABORATORIO DE GRULLA BOSS      CERRADO
DISEÑO                          CERRADO
BALANCE                         CERRADO
QA DE SIMULACIÓN                CERRADO
CONTRATOS DE INTEGRACIÓN        PREPARADOS

RESPONSABLE SIGUIENTE           AGENTE DE INTEGRACIÓN
TRABAJO SIGUIENTE AQUÍ          NINGUNO
```

No continuar recalibrando este jefe salvo que el agente integrador encuentre una discrepancia reproducible entre el contrato cerrado y el comportamiento real del motor.