# Variabilidad intraespecie de monstruos — v0.3

**Estado:** DISEÑO LAB / NO RUNTIME CANON TODAVÍA

## Objetivo

Mantener un único `species_id` por criatura y permitir que dos individuos de
la misma especie tengan estadísticas distintas sin inflar el catálogo.

El T0 READY es el **piso natural**. No existe variación por debajo del T0 en
esta capa.

La variación individual incluye tanto ejes defensivos como **ofensivos**.

## Tiradas independientes

Cada eje variable recibe su propia tirada `q_axis ∈ [0,1]` una sola vez al
crear la instancia.

Ejes físicos/estadísticos:

```text
HP
DEF
EVA
PREC
TEN
```

Ejes ofensivos:

```text
daño básico
daño directo de técnica, cuando exista
daño DOT, cuando exista
duración/ticks del DOT, cuando exista evidencia experimental
```

Para stats enteros:

```text
stat_instance = round(base + q_axis * (ceiling - base))
```

Para expresiones de dados se usan **escaleras discretas formadas únicamente
por expresiones ya observadas en los experimentos**.

Por tanto un individuo puede ser más resistente sin pegar más, pegar más sin
ser más resistente, o reunir ambas condiciones.

## Qué NO varía por azar

La variación individual no cambia la identidad mecánica de la especie.

Se mantienen fijos:

- `resource_model`;
- Control base;
- crítico y multiplicador base;
- nombre/tipo de técnica;
- mecánicas de técnica;
- cadencia;
- QI_DRAIN;
- probabilidades de control;
- cognición/social AI;
- adaptación T1–T4.

Ejemplo: un Mono puede pegar más fuerte, pero no recibe aleatoriamente más
`QI_DRAIN` ni una cadencia distinta sólo por ser un individuo fuerte.

## Mutante

La coincidencia excepcional de tiradas altas es contenido emergente, no un
error a prevenir.

```text
individual_power_score
= media de q de todos los ejes que realmente varían
```

Esto incluye ejes ofensivos.

El umbral depende de la cantidad de ejes variables y se calibra para una cola
teórica de aproximadamente **0,75%**, siempre con guardia de **<1%**.

Cuando cruza el umbral:

```text
suffix = "Mutante"
loot_multiplier = 1.5
xp_multiplier = 1.5
```

No se crea un nuevo `species_id`.

## Fuentes ofensivas ya medidas

### Rata

No tiene técnica. Varía el daño básico dentro de expresiones ya observadas.

### Avispa

Puede variar:

- daño básico;
- daño de veneno;
- ticks del veneno.

La cadencia y la mecánica `POISON_DOT` permanecen fijas.

### Serpiente

Puede variar:

- daño básico si existen expresiones distintas medidas;
- daño de veneno;
- ticks del veneno.

La cadencia y `POISON_DOT` permanecen fijas.

### Lobo

Puede variar:

- daño básico;
- daño directo de `Emboscada de las Tres Colas`.

La cadencia permanece fija.

### Mono

T0 ratificado: `grid 43`.

Su variación incluye:

- DEF/EVA/PREC dentro de envolventes medidas;
- daño básico;
- daño directo de `Manotazo al Dantian`.

HP=34 y TEN=12 no se elevan en v0.3 porque no existe un techo medido superior
compatible con el piso ratificado. `QI_DRAIN=5` y cadencia 2 permanecen fijos
como identidad. El techo de supervivencia usa grid 48 y los techos ofensivos
usan candidatos del search amplio; sus combinaciones cruzadas son LAB-only
hasta ser validadas por Monte Carlo.

## Separación con adaptación

```text
species T0 READY
→ tiradas individuales defensivas + ofensivas
→ posible sufijo Mutante
→ stats/ataques de instancia
→ adaptation tier T0–T4
→ combate
```

Ser Mutante no concede T1/T2/T3/T4 ni altera `maxTierReached`.

## Guardia antes de runtime

1. ninguna stat o ataque cae por debajo del T0;
2. ningún valor supera una envolvente experimental declarada;
3. la incidencia Mutante permanece <1%;
4. `loot_multiplier=1.5` y `xp_multiplier=1.5` sólo se aplican a Mutantes;
5. las mecánicas identitarias no se sortean;
6. normales y Mutantes se validan por raíz/loadout;
7. los cinco LianQi I se prueban conjuntamente antes de activar runtime.

