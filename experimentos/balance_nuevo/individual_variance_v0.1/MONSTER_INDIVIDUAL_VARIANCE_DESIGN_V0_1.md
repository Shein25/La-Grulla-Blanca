# Variabilidad intraespecie de monstruos — v0.1

**Estado:** DISEÑO LAB / NO RUNTIME CANON TODAVÍA

## Objetivo

Evitar inflar artificialmente el catálogo con variantes nominales como
`rata_debil`, `rata_fuerte`, `rata_robusta`.

Cada especie conserva un único `species_id`. El T0 READY representa el
**piso normal** de la especie para generación natural, no un clon exacto.

Cada instancia obtiene una calidad individual `q ∈ [0,1]` al generarse:

- `q=0`: T0 canónico seleccionado;
- `q=1`: techo fuerte representativo de la misma especie;
- nunca se generan individuos por debajo del T0 mediante esta capa.

El roll se realiza una vez por instancia y persiste hasta la muerte/despawn.

## No usar el outlier experimental absoluto

El techo natural no es necesariamente el candidato matemáticamente más brutal
del laboratorio. Se excluyen perfiles que ya cruzaron a otra identidad o a una
amenaza casi-boss.

Ejemplos:
- Lobo 629/1463 quedan fuera: eran casi letales;
- Avispa 1417 queda fuera de la banda natural: supervivencia/DOT demasiado altos;
- Serpiente 1453/1412 quedan fuera;
- estos perfiles siguen siendo evidencia de frontera, no spawns naturales.

## Distribución

No hay tiers visibles ni nuevas entradas de catálogo.

Propuesta inicial para `q`:

```text
70%  q ∈ [0.00, 0.50]
25%  q ∈ (0.50, 0.80]
 5%  q ∈ (0.80, 1.00]
```

Dentro de cada banda, q se sortea uniformemente.

Así todos los individuos son al menos T0, la mayoría vive en la mitad inferior
de la banda fuerte y una minoría alcanza valores cercanos al techo.

Los porcentajes son parámetros LAB y deberán validarse con Monte Carlo.

## Variación coordinada

No se sortean todos los stats independientemente.

Se usa el mismo `q` para mover la instancia entre base y techo:

```text
stat_instance = round(base + q * (ceiling - base))
```

Esto evita obtener simultáneamente el máximo independiente de HP, DEF, EVA,
PREC y TEN por pura casualidad.

Para dados se usa una **escalera discreta aprobada**, no interpolación de floats.

## Qué puede variar

Primera versión:

- HP;
- DEF;
- EVA;
- PREC;
- TEN;
- daño básico mediante escalera discreta.

Se mantienen fijos por especie:

- `resource_model`;
- Control si el T0 lo fija;
- crítico base/multiplicador;
- tipo de técnica;
- mecánicas de técnica;
- cadencia;
- DOT/QI_DRAIN/control de técnica;
- cognición/social AI;
- reglas adaptativas T1–T4.

Los parámetros de técnica podrán recibir variabilidad intraespecie sólo en una
fase posterior si los datos muestran que es segura.

## Separación con adaptación

```text
species T0
→ individual variance q
→ instance base stats
→ population adaptive tier T0–T4
→ combat state / effects
```

La variabilidad individual no concede aprendizaje adaptativo ni modifica
`maxTierReached`.

## Regla de identidad

El techo debe seguir siendo reconocible como la misma especie y el mismo rol.

Por eso se distinguen:

- `natural_ceiling`: permitido para spawn normal;
- `experimental_frontier`: datos de frontera que NO se sortean naturalmente.

## Estado actual

Rata, Avispa, Serpiente y Lobo pueden recibir banda preliminar porque su T0 está
READY. Mono queda bloqueado hasta terminar su refinación local T0.

Antes de activar esto en runtime se hará un `INDIVIDUAL_VARIANCE_LAB` contra
las cinco raíces y loadouts de etapa, usando el modelo empírico de LianQi I.
