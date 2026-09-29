# ETAPA 8A — Corteza Endurecida · selección de curva 1v1 común

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / CANDIDATO LAB SELECCIONADO**

## Pregunta única

¿Qué curva de DEF debe usar **Corteza Endurecida** sobre la nueva base
`DEF_CAP2` para mejorar la fortificación sin reabrir el problema de la
tercera carga?

No se testean todavía:

- 2 enemigos;
- 3 enemigos;
- Tramo II;
- Tramo III;
- Control enemigo;
- otras técnicas.

## Baseline

Piel base PROVISIONAL:

```text
contribución de DEF de Arraigo:
1 → +1
2 → +2
3 → +2
```

Con +2 DEF inmediata de Piel:

```text
Piel aporta:
1 Arraigo → +3 DEF
2 Arraigos → +4 DEF
3 Arraigos → +4 DEF
```

Escenario:

- Tierra HP33 / Qi31 / DEF1 / EVA5;
- enemigo HP28 / PREC90 / EVA20 / DEF2;
- daño enemigo `2d4+1`;
- Piel de apertura.

## Curvas probadas

### BASE_DEF_CAP2

```text
Arraigo DEF acumulada:
1 / 2 / 2
```

### CORTEZA_PLUS1_CAP

Añade una unidad adicional de DEF en todos los estados, pero conserva el
mismo tope entre 2 y 3 Arraigos:

```text
2 / 3 / 3
```

### CORTEZA_DOUBLE_CAP

Intenta preservar más literalmente la antigua idea de “doblar” la
fortificación:

```text
2 / 4 / 4
```

### CORTEZA_PROGRESSIVE

Vuelve a permitir crecimiento en la tercera carga:

```text
2 / 3 / 4
```

## Resultado 1v1 común

100.000 duelos, semilla principal:

| Variante | Win rate | HP restante | Arraigo máx. medio | Extensión |
|---|---:|---:|---:|---:|
| BASE_DEF_CAP2 | 95.56% | 58.39% | 2.72 | 74.85% |
| CORTEZA_PLUS1_CAP | 96.32% | 61.53% | 2.37 | 46.30% |
| CORTEZA_DOUBLE_CAP | 96.37% | 61.86% | 2.23 | 32.50% |
| CORTEZA_PROGRESSIVE | 96.55% | 62.43% | 2.37 | 46.25% |

## Hallazgo emergente

Aumentar DEF no sólo reduce daño.

También reduce la frecuencia con la que daño directo llega realmente a Vida.

Como Arraigo exige daño directo que quite Vida:

```text
más DEF
→ menos ON_HP_DAMAGE
→ menos Arraigo generado
→ menos frecuencia de extensión
```

Por eso las curvas más agresivas empiezan a **auto-frenar la propia mecánica
reactiva de Piel**.

Esto es importante: una rama de fortificación demasiado fuerte puede terminar
haciendo que Piel “se asiente” menos, aunque numéricamente mitigue más.

## Comparación del candidato moderado

`CORTEZA_PLUS1_CAP` contra Piel base, cuatro semillas de 100.000 duelos:

Delta de win:

- +0.764 pp;
- +0.563 pp;
- +0.659 pp;
- +0.535 pp.

Delta de HP restante:

- +3.13 pp;
- +2.99 pp;
- +3.04 pp;
- +3.05 pp.

El efecto es estable.

## Por qué no elegir las otras dos todavía

### DOUBLE_CAP

Da una mejora defensiva apenas mayor en 1v1, pero reduce mucho más:

- Arraigo máximo medio;
- activación de extensión.

Eso empieza a erosionar la identidad reactiva a cambio de una ganancia mínima
adicional.

### PROGRESSIVE

Es la variante con mayor win/HP del test, pero vuelve a introducir exactamente
la propiedad que acabamos de corregir en Piel base:

```text
la tercera carga vuelve a sumar DEF
```

Eso debe considerarse de alto riesgo frente a múltiples impactos.

No hay motivo para reabrir ese problema sólo por ~0.2 pp adicionales de win
en 1v1.

## Candidato seleccionado para la próxima etapa

**CORTEZA_PLUS1_CAP**.

Curva LAB:

```text
contribución acumulada de DEF de Arraigo con Corteza:

1 Arraigo → +2 DEF
2 Arraigos → +3 DEF
3 Arraigos → +3 DEF
```

Con +2 DEF inmediata de Piel:

```text
Piel + Corteza aporta:

1 Arraigo → +4 DEF
2 Arraigos → +5 DEF
3 Arraigos → +5 DEF
```

Con DEF base1 del benchmark:

```text
DEF total:
5 → 6 → 6
```

## Estado de Etapa 8A

**PASS para continuar con CORTEZA_PLUS1_CAP.**

Todavía **NO PROVISIONAL**.

## Próxima etapa

**ETAPA 8B — CORTEZA_PLUS1_CAP contra 2 enemigos.**

Pregunta única:

¿la curva 5→6→6 conserva una mejora de especialización razonable sin volver a
crear el crecimiento multiimpacto que motivó DEF_CAP2?

No avanzar todavía a Tramo II ni III.
