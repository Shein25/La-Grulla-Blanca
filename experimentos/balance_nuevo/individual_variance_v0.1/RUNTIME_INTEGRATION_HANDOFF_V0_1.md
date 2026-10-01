# Handoff de integración runtime — variabilidad individual / Mutante

Fecha: 2026-10-01

Estado: **HUMAN_RATIFIED_FOR_EXPERIMENTAL_RUNTIME_INTEGRATION**

## Decisiones congeladas

- distribución natural: `UNIFORM_0_1`;
- T0 READY = piso natural;
- ejes defensivos y ofensivos tiran independientemente;
- no se crean nuevos `species_id`;
- convergencia extrema <1% recibe sufijo `Mutante`;
- Mutante: botín x1.5 y XP de combate x1.5;
- probabilidad de objetos únicos no se multiplica;
- XP profesional no recibe el multiplicador;
- T1–T4 no se conceden ni modifican desde esta capa.

Heavy validado:

- 250.000 spawns naturales;
- 50.000 Mutantes condicionados;
- incidencia observada 0,7556%;
- resultados SHA-256
  `5e077b9513aedc36502a214b37c7f8e8a3f5ce2ed7577e5bc8811c35039f8aae`.

## Adapter

`runtime_variance_adapter.mjs` recibe:

- perfil T0 canónico READY;
- configuración ratificada;
- RNG proporcionado por el runtime;
- id opcional de instancia.

Devuelve una copia independiente:

- stats y ataques individuales;
- `combat_profile`;
- `display_name`;
- clasificación Mutante;
- multiplicadores de recompensa;
- metadatos de adaptación.

Nunca modifica el registro canónico.

## Persistencia

La tirada se hace **al crear/spawnear el individuo**, no al iniciar combate.

La instancia debe conservar:

- stats/ataques ya resueltos;
- `individual_power_score`;
- `mutant`;
- `suffix`;
- multiplicadores de recompensa.

Salir/reentrar a la sala o iniciar otro turno de combate no debe rerollear al
mismo individuo.

Respawn = nueva instancia = nueva tirada.

## Puntos de integración observados en ver74 (REFERENCIA, NO PARCHEAR)

La rama experimental todavía contiene `grulla-blanca_ver74.html`, no la fuente
ver76 actual. Por eso estos puntos sirven sólo de mapa semántico:

1. `crearMob(mid, plantilla, meta)`
   - es el lugar natural para consumir una instancia ya resuelta;
   - no debe tirar nuevamente durante combate.

2. `etiquetaMob(mob)`
   - debe mostrar `Mutante` desde el nombre de instancia;
   - `mob_id` sigue siendo el species id original.

3. `recompensas(mobId, e)`
   - en ver74 entrega Qi y recorre probabilidades `loot[].prob`;
   - el adapter **no debe multiplicar esas probabilidades**.

4. bloque de muerte en `Combate.turno()`
   - ya pasa la instancia muerta a `recompensas`;
   - es el lugar donde el runtime nuevo puede leer los metadatos de recompensa
     de esa instancia.

## XP

El cliente ver74 no expone una vía general de XP de combate de monstruos.
Las funciones `sumarExperienciaProfesion` pertenecen a oficios.

Por tanto está **prohibido** conectar `combat_xp_multiplier=1.5` con:

- Examen;
- Herboristería;
- Alquimia.

El multiplicador espera el contrato de XP de combate/progresión del runtime
actual. Si ese contrato todavía no existe, debe conservarse como metadato hasta
que exista; no inventar una fuente de XP.

## Botín x1.5

El adapter devuelve `loot_multiplier=1.5`, pero no decide si el contrato
económico final lo interpreta como cantidad, valor o pool adicional.

No convertirlo automáticamente en `drop.prob *= 1.5`: eso modificaría tasas
de descubrimiento/objetos únicos y contradice la decisión congelada.

## Guardia ver76

No integrar directamente en ver74. El agente de integración debe tomar la
fuente ver76/autoritativa, localizar los equivalentes actuales de spawn,
etiqueta y recompensa, y adaptar allí este contrato.
