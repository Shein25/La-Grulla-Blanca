# DECISIÓN HUMANA — REPERTORIO, DESBLOQUEO Y PRESUPUESTO DE ULTIS

Fecha: 2026-10-07
Proyecto: La Grulla Blanca
Repositorio: `Shein25/La-Grulla-Blanca`
Rama: `experiment/grulla-ulti25-v031-handoff-2026-10-04`

## Decisión estructural de ramas, afinidad y builds

La **profundidad de una rama elemental NO depende del injerto**.

Un jugador puede aprender y profundizar cualquiera de las cinco ramas elementales hasta su estado de **APRENDIDA_AL_MAXIMO**, aunque esa rama no sea ni su elemento principal ni su elemento injertado.

Por tanto:

- principal, injertada y no afines pueden profundizarse hasta el final;
- el injerto no desbloquea la profundidad de la rama;
- la distribución de puntos/build define cómo explota el jugador las ramas aprendidas;
- las ramas no afines se balancean mediante las penalizaciones propias del sistema;
- no se fijan aquí magnitudes nuevas de penalización: deben venir de la autoridad de técnicas/balance;
- una rama no afín aprendida al máximo sigue siendo una rama completamente aprendida, aunque conserve las penalizaciones correspondientes a no tener afinidad.

La distinción correcta es:

- **aprendizaje/maestría de rama** = cuánto conoce y ha desarrollado el jugador esa rama;
- **afinidad** = relación elemental privilegiada del personaje;
- **build** = distribución actual de puntos y elecciones;
- **injerto** = segunda afinidad elemental, no permiso para profundizar.

## Afinidades

El jugador tiene:

1. un **elemento principal**;
2. opcionalmente, un **elemento injertado** cuando el sistema de injerto lo habilita.

Las demás ramas pueden ser aprendidas y dominadas, pero siguen siendo **no afines** mientras no exista una autoridad que diga lo contrario.

## Decisión estructural de repertorio de Ultis

El jugador no dispone de las 25 Ultis ni de las 5 Ultis de una raíz simultáneamente durante un combate.

Su repertorio activo admite como máximo **2 Ultis**:

1. una Ulti correspondiente al **elemento principal**;
2. una Ulti correspondiente al **elemento injertado**.

Una rama no afín, aunque esté aprendida al máximo, **NO concede una tercera Ulti**.

Ambas Ultis disponibles comparten un único presupuesto de uso: **máximo 1 activación válida de Ulti por combate en total**.

Una vez consumido ese presupuesto, la otra Ulti equipada queda bloqueada durante el resto del combate. Las dos Ultis deben tratarse como **alternativas tácticas**, no como una cadena/combo de dos Ultis.

## Regla de maestría / aprendizaje máximo

`RAMA_APRENDIDA_AL_MAXIMO` es un estado de progresión/conocimiento de la rama y **NO depende de cómo el jugador distribuya sus puntos entre las especializaciones ni de poseer afinidad con esa rama**.

Por tanto:

- no se exige tener puntos en todas las especializaciones;
- no se exige una distribución concreta;
- una build `2/2/2` conserva acceso a las capacidades que correspondan a una rama ya dominada;
- también son válidas otras distribuciones permitidas por el sistema aunque alguna especialización tenga 0 puntos;
- cambiar el reparto de puntos no elimina el estado histórico de rama aprendida al máximo;
- una rama no principal/no injertada también puede alcanzar `RAMA_APRENDIDA_AL_MAXIMO`.

La distribución de puntos define el **build**. El aprendizaje máximo define la **maestría**. La afinidad define qué bonificaciones/penalizaciones y qué acceso a Ultis corresponden. Son conceptos independientes.

## Desbloqueo de Ultis

### Ulti del elemento principal

Requisitos acumulativos:

- haber alcanzado como mínimo **LianQi III**;
- tener la rama del elemento principal en estado **APRENDIDA_AL_MAXIMO**.

Cuando se cumplen ambos requisitos, se habilita la Ulti del elemento principal, independientemente del reparto de puntos entre especializaciones.

### Ulti del elemento injertado

Requisitos acumulativos:

- poseer efectivamente el **injerto elemental**;
- haber alcanzado como mínimo **LianQi IV**;
- tener la rama del elemento injertado en estado **APRENDIDA_AL_MAXIMO**.

Cuando se cumplen los tres requisitos, se habilita la Ulti del elemento injertado, independientemente del reparto de puntos entre especializaciones.

Una rama no afín aprendida al máximo no satisface este segundo gate si no es la rama efectivamente injertada.

## Consecuencia de progresión

- Cualquier rama aprendida puede profundizarse hasta el final, tenga o no afinidad.
- Las builds pueden invertir en ramas no afines y serán balanceadas por las penalizaciones correspondientes.
- LianQi III + rama principal aprendida al máximo: hasta 1 Ulti disponible, la principal.
- Tener otras ramas aprendidas al máximo no concede Ultis adicionales.
- Tener injerto en LianQi III NO concede automáticamente la Ulti injertada.
- LianQi IV + injerto + rama injertada aprendida al máximo: puede habilitarse la segunda Ulti.
- Incluso con 2 Ultis disponibles, el presupuesto global sigue siendo 1 activación válida por combate.

## Implicación de balance

Los benchmarks deben probar:

- ramas afines y no afines a igual profundidad de aprendizaje;
- múltiples distribuciones de build;
- las penalizaciones reales de uso de ramas no afines;
- especialización extrema y builds híbridas;
- casos donde una rama no afín está aprendida al máximo pero no es elegible para Ulti;
- principal e injerto como únicas fuentes posibles de las dos Ultis del repertorio.

No se debe confundir una penalización de afinidad con una prohibición de progresión.

## No inventar todavía

Quedan pendientes de autoridad explícita:

- valores y naturaleza exacta de las penalizaciones de ramas no afines;
- si un intento de Ulti rechazado/no activado consume o no el presupuesto global;
- reglas de adquisición/selección de la Ulti concreta dentro de cada elemento una vez cumplido su gate;
- cualquier regla de cambio/reemplazo de injerto.

Hasta que esas reglas se definan, los runners futuros deben usar la autoridad disponible o marcar `AUTHORITY_REQUIRED`; no deben inventar valores.

## Guardias

- V03.1 de 25 Ultis queda congelado como evidencia mecánica validada.
- No reescribir resultados QUICK/STANDARD por esta decisión.
- No auto-nerf/buff.
- Decisiones humanas prevalecen.
