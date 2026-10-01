# Variabilidad intraespecie de monstruos — v0.2

**Estado:** DISEÑO LAB / NO RUNTIME CANON TODAVÍA

## Objetivo

Mantener un único `species_id` por criatura y permitir que dos individuos de
la misma especie tengan estadísticas diferentes.

No se crean entradas como `rata_fuerte` o `lobo_elite`.

El T0 READY es el **piso natural**. La envolvente superior se toma del perfil
más difícil observado y medido para esa especie dentro de nuestros laboratorios.

No existe variación por debajo del T0 en esta capa.

## Tiradas independientes

Cada eje variable recibe su propia tirada `q_stat ∈ [0,1]` al crear la
instancia.

```text
stat_instance = round(base + q_stat * (ceiling - base))
```

Por tanto pueden coincidir varias tiradas altas. Esa coincidencia **no se
prohíbe**: es una característica del mundo.

El daño básico usa una escalera discreta entre el daño T0 y daños superiores
ya observados en experimentos.

La instancia conserva sus valores hasta morir/desaparecer.

## Mutante

La coincidencia excepcional de tiradas altas se convierte en contenido.

Se calcula:

```text
individual_power_score
= media de las q de todos los ejes que realmente varían
```

El daño básico cuenta como un eje si su escalera tiene más de un escalón.

El umbral depende del número de ejes variables y está calibrado para que,
con tiradas uniformes independientes, la cola teórica ronde **0,75%** y quede
por debajo de 1%.

Cuando el score supera el umbral:

```text
suffix = "Mutante"
loot_multiplier = 1.5
xp_multiplier = 1.5
```

No se crea un nuevo `species_id`. Por ejemplo:

```text
species_id = lobo_espiritual
display     = Lobo espiritual de tres colas Mutante
```

El Mutante puede comportarse como un mini-jefe emergente. El jugador decide
si combatir, huir, prepararse o buscar ayuda.

El Mutante entrega **botín x1.5 y XP x1.5** para compensar su dificultad adicional. La probabilidad de objetos únicos permanece sin cambios en v0.2.

## Techo: usar el perfil más difícil observado

A diferencia de v0.1, no descartamos el extremo sólo porque sea muy peligroso.
Ese extremo sirve precisamente para construir la cola rara.

Techos preliminares con datos ya medidos:

- Rata: trial 3325;
- Avispa: trial 1251;
- Serpiente: trial 1453;
- Lobo: trial 1463;
- Mono: pendiente del refinamiento local actual.

Esto no significa que esos perfiles aparezcan completos con frecuencia. Para
reconstruir casi todo el extremo a la vez deben coincidir muchas tiradas altas,
lo cual cae en la cola Mutante.

## Qué varía en v0.2

- HP;
- DEF;
- EVA;
- PREC;
- TEN;
- daño básico mediante escalera discreta.

Se mantienen fijos en esta primera validación:

- resource_model;
- Control;
- crítico y multiplicador;
- técnica y sus parámetros;
- cognición/social AI;
- adaptación T1–T4.

La técnica podrá recibir variación intraespecie en una fase posterior si la
simulación demuestra que la capa base es estable.

## Separación con adaptación

```text
species T0 READY
→ tiradas individuales
→ posible sufijo Mutante
→ stats de instancia
→ adaptation tier T0–T4
→ combate
```

Ser Mutante no concede T1/T2/T3/T4 ni altera `maxTierReached`.

## Guardia

Antes de runtime:

1. comprobar que ninguna stat cae por debajo de la envolvente T0↔techo;
2. comprobar que la frecuencia Mutante queda <1%;
3. medir presión de combate de normales y Mutantes por raíz/loadout;
4. verificar que `loot_multiplier=1.5` y `xp_multiplier=1.5` sólo se aplican a Mutantes;
5. añadir el Mono sólo después de cerrar su T0.

