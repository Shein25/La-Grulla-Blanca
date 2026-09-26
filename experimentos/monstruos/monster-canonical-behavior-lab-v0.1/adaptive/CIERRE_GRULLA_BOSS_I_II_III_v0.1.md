# Cierre experimental — Grulla Blanca · encuentro completo I→II→III v0.1

**Fecha:** 2026-09-26  
**Estado:** ENCUENTRO COMPLETO CERRADO EXPERIMENTALMENTE  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Fases

```text
FASE I    EL VOTO INMÓVIL          CERRADA
FASE II   LAS ALAS RECUERDAN       CERRADA
FASE III  LA CAMPANA SIN DUEÑO     CERRADA
```

## 2. HP total

```text
Fase I     150
Fase II    100
Fase III    50
----------------
TOTAL      300 HP
```

## 3. Fase I congelada

```text
ATQ 4
DEF 13
Golpe 1d6+2
Campanada 2d6+2
Pata +3 DEF
Piel G345_D1
Resonancia x1,75 después de Pata contra Piel activa
```

## 4. Fase II congelada

```text
ATQ 4
DEF 13
HP 100

CHAIN_A
Golpe de Ala 1d4
Tormenta 1d6+1 / drain 1
Cerrar Alas 3 / reserva 6
Recordar Filo +10 EVA
Eco drain 3 condicional
```

Memoria:

```text
3 usos consecutivos de una técnica
-> comprendida
-> siguiente repetición suprimida

BASIC u otra técnica
-> rompe lock

DEFENDER / RECOVER
-> no borran conocimiento
```

## 5. Fase III congelada

```text
PERFIL M_A
HP 50
ATQ 4
DEF 13

Picotazo +1 ATQ / 1d4+1
Campana +1 ATQ / 1d6+2 / drain 2
Ala Vacía +10 EVA
Pata +3 DEF
Romper Ritmo +2 ATQ / 1d6+2
```

Política QA: `MASTER_READER`.

## 6. Contrato global

El encuentro completo debe premiar:

- lectura de telegraphs;
- administración de qi;
- BASIC como herramienta real;
- variación consciente;
- ruptura de patrones;
- selección situacional de defensas;
- adaptación mutua jugador↔Grulla.

Debe castigar:

- una única técnica ofensiva para todo;
- defender mecánicamente cada amenaza;
- abusar de Piel sin leer Resonancia;
- gastar qi de forma automática;
- repetir una técnica aprendida por la Grulla.

## 7. Anti-spam

```text
PURE SINGLE-SKILL       0% victoria completa
SPAM + DEFENDER         0% victoria completa
```

Este contrato es global y no debe relajarse al integrar.

## 8. Viabilidad sin opcionales

El toolkit universal continúa siendo suficiente:

```text
raíz ofensiva
ATACAR básico
DEFENDER
recursos normales
```

Paso, Piel y Filamento son opcionales.

## 9. Cadena de referencia

M_A + MASTER_READER:

```text
llega FIII           ~20,22%
FIII condicional     ~35,17%
victoria I+II+III     ~8,33%
```

Este ~8% no representa al jugador promedio ni un objetivo comercial de dificultad; es una referencia Monte Carlo del policy model bajo la cadena calibrada.

## 10. Estado

```text
BALANCE FASE I                   CERRADO
BALANCE FASE II                  CERRADO
BALANCE FASE III                 CERRADO
MEMORIA                          CERRADA
COUNTERPLAY                      CERRADO
ANTI-SPAM                        CERRADO
OPCIONALES                       VALIDADAS
STRESS ZERO-QI                   VALIDADO

VER74                            SIN CAMBIOS
INTEGRACIÓN AL JUEGO             PENDIENTE
```

El próximo trabajo no es recalibrar nuevamente la Grulla.

El próximo trabajo, si se autoriza, es traducir este contrato experimental a integración productiva y QA de implementación sin alterar los valores congelados.

## 11. Documentos autoritativos

- `adaptive/CIERRE_GRULLA_FASE1_v0.1.md`
- `adaptive/CIERRE_GRULLA_FASE2_v0.1.md`
- `adaptive/CIERRE_GRULLA_FASE3_v0.1.md`
- `adaptive/RESULTADO_GRULLA_FASE3_FINAL_VALIDATION_v0.1.md`