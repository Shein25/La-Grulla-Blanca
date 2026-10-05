# DECISIÓN HUMANA — REPERTORIO DE ULTIS Y PRESUPUESTO POR COMBATE

Fecha: 2026-10-05
Proyecto: La Grulla Blanca
Repositorio: `Shein25/La-Grulla-Blanca`
Rama: `experiment/grulla-ulti25-v031-handoff-2026-10-04`
HEAD previo al registro: `ed7e98c5c7310e73cf374f1219a9d51c57e08969`

## Decisión estructural

El jugador no dispone de las 25 Ultis ni de las 5 Ultis de una raíz simultáneamente durante un combate.

Su repertorio activo admite como máximo **2 Ultis**:

1. una Ulti correspondiente al **elemento principal**;
2. una Ulti correspondiente al **elemento injertado**.

Ambas comparten un único presupuesto de uso: **máximo 1 activación válida de Ulti por combate en total**.

Una vez consumido ese presupuesto, la otra Ulti equipada queda bloqueada durante el resto del combate. Las dos Ultis deben tratarse como **alternativas tácticas**, no como una cadena/combo de dos Ultis.

## Implicación de balance

El balance futuro debe evaluar la decisión entre las dos Ultis disponibles en un mismo estado de combate. No es suficiente comparar cada Ulti aislada ni es válido sumar sus efectos como si ambas pudieran ejecutarse en el mismo combate.

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
- fase/ventana de activación
- interacción con Pacto F3
- supervivencia y estado final del jefe después de la elección

Debe detectarse especialmente si una Ulti domina a la otra en casi todos los contextos del repertorio, aunque ambas parezcan razonables en pruebas aisladas.

## No inventar todavía

Quedan pendientes de autoridad explícita:
- si un intento rechazado/no activado consume o no el presupuesto global;
- si elemento principal e injertado pueden ser el mismo elemento;
- reglas de desbloqueo/adquisición/selección de la Ulti concreta dentro de cada elemento.

Hasta que esas reglas se definan, los runners futuros deben abortar las suites que dependan de ellas o marcarlas `AUTHORITY_REQUIRED`; no deben asumir una respuesta.

## Guardias

- V03.1 de 25 Ultis queda congelado como evidencia mecánica validada.
- No reescribir resultados QUICK/STANDARD por esta decisión.
- No auto-nerf/buff.
- Decisiones humanas prevalecen.
