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

Las Ultis **NO se desbloquean automáticamente por alcanzar una etapa de LianQi**. La etapa es sólo un requisito mínimo. El gate real es la **maestría completa de la rama elemental correspondiente**.

### Ulti del elemento principal

Requisitos acumulativos:

- haber alcanzado como mínimo **LianQi III**;
- haber alcanzado la **maestría completa de la rama del elemento principal**;
- "maestría completa de la rama" significa que el jugador ha progresado lo suficiente como para **ser capaz de asignar al menos 1 punto en cada especialización de esa rama**.

No se exige haber gastado efectivamente un punto en cada especialización: se exige haber alcanzado el nivel de maestría que permite hacerlo.

Cuando se cumplen ambos requisitos, se habilita la Ulti del elemento principal.

### Ulti del elemento injertado

Requisitos acumulativos:

- poseer efectivamente el **injerto elemental**;
- haber alcanzado como mínimo **LianQi IV**;
- haber alcanzado la **maestría completa de la rama del elemento injertado**;
- la misma definición de maestría aplica: capacidad de asignar al menos 1 punto en cada especialización de esa rama.

Cuando se cumplen los tres requisitos, se habilita la Ulti del elemento injertado.

### Consecuencia de progresión

- Antes de cumplir la maestría de la rama principal en LianQi III: 0 Ultis disponibles.
- LianQi III + maestría completa de la rama principal: hasta 1 Ulti disponible, la principal.
- Tener injerto en LianQi III NO concede automáticamente la Ulti injertada.
- LianQi IV + injerto + maestría completa de la rama injertada: puede habilitarse la segunda Ulti.
- Incluso con 2 Ultis disponibles, el presupuesto global sigue siendo 1 activación válida por combate.

## Implicación de balance

Los benchmarks por etapa deben respetar disponibilidad real. No se debe probar un monstruo/jefe de LianQi III suponiendo automáticamente 2 Ultis ni una Ulti principal si el perfil no demuestra maestría completa de su rama.

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
- reglas de adquisición/selección de la Ulti concreta dentro de cada elemento una vez cumplido el gate de maestría.

Hasta que esas reglas se definan, los runners futuros deben abortar las suites que dependan de ellas o marcarlas `AUTHORITY_REQUIRED`; no deben asumir una respuesta.

## Guardias

- V03.1 de 25 Ultis queda congelado como evidencia mecánica validada.
- No reescribir resultados QUICK/STANDARD por esta decisión.
- No auto-nerf/buff.
- Decisiones humanas prevalecen.
