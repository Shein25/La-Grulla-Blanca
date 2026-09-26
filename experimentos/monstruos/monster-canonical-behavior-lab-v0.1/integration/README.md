# Canonical Intent Bridge v0.1

## Objetivo

Cerrar la frontera entre:

```text
chooseMonsterIntent()
→ intent seleccionado
→ orden canónica
```

sin ejecutar todavía el combate.

## Órdenes

`BASIC_ATTACK`

Copia únicamente:

- ataque canónico;
- dado de daño canónico;
- elemento si existe.

`TECHNIQUE`

Copia byte-semánticamente el objeto `MOBS[id].tecnica`, incluyendo:

- ataque/daño;
- veneno;
- quemadura;
- drenaje de qi;
- nombre;
- cadencia.

## Guardia crítica

Una intención de técnica sólo puede bindearse cuando:

```text
round % tecnica.cada === 0
```

Si no:

`CADENCE_VIOLATION`

El kernel puede experimentar en `DECISION_EXPERIMENTAL`, pero esta capa impide que una decisión experimental se cuele accidentalmente en producción fuera de cadencia.

## Telegraph

`canonicalTelegraph()` reproduce:

```text
(round + 1) % tecnica.cada === 0
```

y sólo devuelve información; no muta combate.

## Fuera de alcance

- tirar dados;
- resolver impacto;
- aplicar daño;
- aplicar aflicciones;
- drenar qi;
- cooldowns;
- aggro;
- movimiento;
- loot;
- muerte.

## Estado

`CANONICAL_INTENT_BRIDGE_V01: 11_PASS_0_FAIL_CONFIRMED`


## Memoria semántica

El bridge de intención queda separado del feedback del combate.

El componente `Semantic Memory Recorder v0.1` fue confirmado con:

```text
12 PASS / 0 FAIL
```

Cadena validada:

```text
resolved outcome normalizado
→ semantic event
→ memoria semántica
→ Monster Combat AI
```

El siguiente hueco es adaptar resultados reales del combate productivo a esos outcomes normalizados sin inferirlos.
