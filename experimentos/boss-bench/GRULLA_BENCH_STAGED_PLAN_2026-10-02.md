# GRULLA BENCH — Plan escalonado ULTI primero / build completo después

Fecha: 2026-10-02  
Estado: LAB / NO CANON / NO MAIN / NO MERGE / NO PUSH

## Decisión

El benchmark se divide en dos estadios compatibles.

### Etapa A — ULTIS_ONLY

Es la etapa inmediata.

Objetivo: medir las 25 Ultis contra la Grulla completa sin que técnicas y equipo todavía en ajuste alteren la lectura.

Mantiene:

- Grulla F1 -> F2 -> F3;
- IA/memoria/intenciones reales del jefe;
- Pacto del Último Vuelo;
- seeds pareadas;
- baseline sin Ulti;
- ventanas F1_EARLY / F2_ENTRY / F3_ENTRY / PREPARED_OPPORTUNITY;
- métricas por fase y presión de skip F3;
- misma implementación cerrada de cada Ulti.

No usa como variables de balance:

- ramas de técnicas Arco 1 aún provisionales;
- equipo Arco 1 aún provisional;
- optimización de build completo.

La política normal entre ventanas debe ser fija y declarada. No puede cambiar entre baseline y rama Ulti.

## Etapa B — FULL_LOADOUT

Se habilita únicamente después de que el usuario cierre:

1. técnicas;
2. ramas;
3. equipo;
4. build/fixture de personaje.

No se construirá otro benchmark. Se reutilizan exactamente:

- Grulla;
- Pacto;
- seeds;
- escenarios;
- ventanas;
- Ultis;
- métricas;
- formato de resultados.

Lo único que cambia será la capa del jugador:

`neutral/fixed policy -> real technique + equipment loadout`

Eso permitirá medir:

`Δ loadout = FULL_LOADOUT - ULTIS_ONLY`

y separar:

- potencia intrínseca de la Ulti;
- sinergia con técnicas;
- sinergia con equipo;
- economía real de Qi;
- supervivencia añadida por build;
- cambios en la ventana óptima de activación;
- presión de skip F3 antes/después del build.

## Gate humano

El archivo:

`FULL_LOADOUT_RELEASE_GATE_V0_1.json`

comienza bloqueado.

No se libera automáticamente aunque un catálogo cambie de nombre o status. Debe existir aprobación humana explícita de:

- técnicas;
- equipo;
- build.

Esto evita testear accidentalmente números viejos o provisionales.

## Fuentes observadas hoy

Técnicas:

`experimentos/balance_nuevo/techniques_arc1_catalog.json`

Estado observado:

`PROVISIONAL_LAB_INPUT_NOT_RUNTIME_CANON`

Equipo:

`experimentos/balance_nuevo/equipment_arc1_catalog.json`

Estado observado:

`PROVISIONAL_DESIGN_DESCRIPTIONS_AND_PROLOGUE_CLOSED_ACQUISITION_AUDIT_DEFERRED`

Por definición, ninguno entra todavía en FULL_LOADOUT.

## Contrato del futuro fixture

Cuando llegue el momento, el fixture de personaje debe declarar explícitamente:

- `fixture_id`;
- stats efectivos;
- técnicas y ramas;
- equipo por slot;
- consumibles incluidos;
- fuente/commit de cada autoridad.

El adapter no elegirá “el mejor equipo” ni rellenará huecos.

## Comparación final prevista

Una vez cerrados ambos estadios podremos tener tres lecturas:

1. `BASELINE_NO_ULTI`
2. `ULTIS_ONLY`
3. `FULL_LOADOUT`

Por seed pareada podremos responder:

- qué peleas cambia la Ulti por sí sola;
- qué peleas cambia el build sin depender de la Ulti;
- qué Ultis escalan demasiado con equipo/técnicas;
- cuáles necesitan preparación real;
- si guardar la Ulti para F3 sigue dominando con un personaje completo.

## Regla dura

Un resultado de FULL_LOADOUT nunca sustituye silenciosamente al resultado ULTIS_ONLY.

Ambos se conservan para poder atribuir la causa del cambio.
