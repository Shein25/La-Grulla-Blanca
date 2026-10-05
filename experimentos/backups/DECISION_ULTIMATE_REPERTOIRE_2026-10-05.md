# DECISIÓN HUMANA — REPERTORIO, DESBLOQUEO Y PRESUPUESTO DE ULTIS

Fecha: 2026-10-05
Proyecto: La Grulla Blanca
Repositorio: `Shein25/La-Grulla-Blanca`
Rama: `experiment/grulla-ulti25-v031-handoff-2026-10-04`
HEAD previo al primer registro: `ed7e98c5c7310e73cf374f1219a9d51c57e08969`

## Decisión estructural de repertorio

El jugador no dispone de las 25 Ultis ni de las 5 Ultis de una raíz simultáneamente durante un combate.

Su repertorio activo admite como máximo **2 Ultis**:

1. una Ulti correspondiente al **elemento principal**;
2. una Ulti correspondiente al **elemento injertado**.

Ambas comparten un único presupuesto de uso: **máximo 1 activación válida de Ulti por combate en total**.

Una vez consumido ese presupuesto, la otra Ulti equipada queda bloqueada durante el resto del combate. Las dos Ultis deben tratarse como **alternativas tácticas**, no como una cadena/combo de dos Ultis.

## Decisión estructural de desbloqueo

Las Ultis **NO se desbloquean automáticamente por alcanzar una etapa de LianQi**. La etapa es sólo un requisito mínimo. El gate real es que la **rama elemental correspondiente haya sido aprendida al máximo**.

### Regla de maestría / aprendizaje máximo

`RAMA_APRENDIDA_AL_MAXIMO` es un estado de progresión/conocimiento de la rama y **NO depende de cómo el jugador distribuya sus puntos entre las especializaciones**.

Por tanto:

- no se exige tener puntos en todas las especializaciones;
- no se exige una distribución concreta;
- una build `2/2/2` conserva acceso a la Ulti;
- también son válidas otras distribuciones permitidas por el sistema aunque alguna especialización tenga 0 puntos;
- cambiar el reparto de puntos no debe bloquear una Ulti ya habilitada mientras la rama continúe aprendida al máximo.

La distribución de puntos define el **build**. El aprendizaje máximo de la rama define la **elegibilidad de la Ulti**. Son conceptos independientes.

### Ulti del elemento principal

Requisitos acumulativos:

- haber alcanzado como mínimo **LianQi III**;
- tener la rama del elemento principal en estado **aprendida al máximo**.

Cuando se cumplen ambos requisitos, se habilita la Ulti del elemento principal, independientemente del reparto de puntos entre especializaciones.

### Ulti del elemento injertado

Requisitos acumulativos:

- poseer efectivamente el **injerto elemental**;
- haber alcanzado como mínimo **LianQi IV**;
- tener la rama del elemento injertado en estado **aprendida al máximo**.

Cuando se cumplen los tres requisitos, se habilita la Ulti del elemento injertado, independientemente del reparto de puntos entre especializaciones.

### Consecuencia de progresión

- Antes de tener la rama principal aprendida al máximo en LianQi III: 0 Ultis disponibles.
- LianQi III + rama principal aprendida al máximo: hasta 1 Ulti disponible, la principal.
- Tener injerto en LianQi III NO concede automáticamente la Ulti injertada.
- LianQi IV + injerto + rama injertada aprendida al máximo: puede habilitarse la segunda Ulti.
- Incluso con 2 Ultis disponibles, el presupuesto global sigue siendo 1 activación válida por combate.

## Implicación de balance

Los benchmarks por etapa deben respetar disponibilidad real. No se debe probar un monstruo/jefe de LianQi III suponiendo automáticamente 2 Ultis ni una Ulti principal si el perfil no tiene su rama principal aprendida al máximo.

Los benchmarks **NO deben utilizar la distribución de puntos como gate de Ulti**. Distintas builds de una misma rama deben poder compararse conservando la misma Ulti cuando cumplen el mismo estado de aprendizaje máximo.

El balance futuro debe evaluar la decisión entre las dos Ultis disponibles en un mismo estado de combate sólo para perfiles que realmente hayan desbloqueado ambas.

Ejemplo conceptual:
- repertorio = Ulti del elemento principal + Ulti del elemento injertado;
- política = elegir una de las dos o no gastar la Ulti todavía;
- una activación válida consume el presupuesto global;
- la otra queda indisponible hasta el siguiente combate.

## Métricas obligatorias futuras

- `ULTIMATE_CHOICE_SHARE`
- `ULTIMATE_OPPORTUNITY_REGRET`
- `ULTIMATE_UNUSED_RATE`
- `PRIMARY_ULTIMATE_USE_RATE`
- `GRAFTED_ULTIMATE_USE_RATE`
- `ULTIMATE_UNLOCK_ELIGIBILITY`
- fase/ventana de activación
- interacción con Pacto F3
- supervivencia y estado final del jefe después de la elección

Debe detectarse especialmente si una Ulti domina a la otra en casi todos los contextos del repertorio, aunque ambas parezcan razonables en pruebas aisladas.

## No inventar todavía

Quedan pendientes de autoridad explícita:
- si un intento rechazado/no activado consume o no el presupuesto global;
- si elemento principal e injertado pueden ser el mismo elemento;
- reglas de adquisición/selección de la Ulti concreta dentro de cada elemento una vez cumplido el gate de aprendizaje máximo.

Hasta que esas reglas se definan, los runners futuros deben abortar las suites que dependan de ellas o marcarlas `AUTHORITY_REQUIRED`; no deben asumir una respuesta.

## Guardias

- V03.1 de 25 Ultis queda congelado como evidencia mecánica validada.
- No reescribir resultados QUICK/STANDARD por esta decisión.
- No auto-nerf/buff.
- Decisiones humanas prevalecen.
