# GRULLA 25/25 — Corrección de alcance: Ultis + equipo, técnicas después

Fecha: 2026-10-02

## Decisión humana nueva

Para el benchmark inmediato contra la Grulla:

- **sí usar equipo**;
- **no usar todavía técnicas normales**;
- las técnicas se integrarán cuando termine su ajuste;
- el benchmark final repetirá la misma matriz con todo junto.

Esta decisión posterior prevalece sobre el plan anterior `ULTIS_ONLY`.

## Etapa del encuentro

M18 · El Voto Inmóvil ocurre en `LIV_DESCENSO`.

Por tanto, el bench de equipo utiliza los perfiles `LianQi_IV` del catálogo.

## Perfiles principales

### MANDATORY_ENTRY

Controla el mínimo de equipo de progresión.

### EXPECTED_STAGE

Es el perfil principal por defecto para interpretar la Ulti en un jugador razonablemente equipado en LIV.

### HIGH_ROLL_STRESS

Estrés de equipamiento alto pero definido por el propio catálogo.

### NAKED

Sólo control diagnóstico. No es el resultado principal.

## Regla de pairing

Baseline y rama con Ulti deben usar exactamente:

- misma seed;
- mismo estado inicial del jugador;
- mismo perfil de equipo;
- mismas piezas;
- mismos stats derivados;
- mismos efectos de equipo.

La única diferencia causal es la disponibilidad/uso de la Ulti.

## Técnicas

Hasta nuevo cierre humano:

`NORMAL_TECHNIQUES_ENABLED = false`

No se aplican:

- ramas;
- daño de técnicas normales;
- buffs/debuffs de técnicas;
- técnicas defensivas;
- preparación generada por técnicas normales.

Las condiciones `PREPARED_OPPORTUNITY` de las Ultis deben ejercitarse por fixtures controlados propios de la Ulti, no simulando técnicas todavía no cerradas.

## Equipo

Se aplican los stats y efectos del equipo exactamente desde catálogo.

No se aplican consumibles en esta ronda.

## Tamaño del diseño actual

Con 3 perfiles de equipo principales:

### Smoke · 20 seeds

- 25 Ultis
- 4 ventanas
- 4 estados del jugador
- 3 perfiles de equipo
- 20 seeds

`25 × 4 × 4 × 3 × 20 = 24.000` encuentros con Ulti.

Baselines pareados únicos:

`4 × 3 × 20 = 240`.

### Pilot · 200 seeds

`240.000` encuentros con Ulti + `2.400` baselines.

El perfil NAKED puede correrse como control aparte sin contaminar los agregados principales.

## Futuro

Cuando las técnicas estén cerradas:

- no se cambia la Grulla;
- no se cambia el Pacto;
- no se cambian las Ultis;
- no se cambian seeds/ventanas/métricas;
- se agrega únicamente la capa de técnicas y policy del jugador.

Así podremos calcular:

`FULL_LOADOUT - ULTIS_EQUIPMENT`

y atribuir la diferencia específicamente a técnicas e interacción técnica+equipo+Ulti.
