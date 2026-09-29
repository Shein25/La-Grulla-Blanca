# ETAPA 9B — Estratos Compactos · 2 enemigos

Fecha: 2026-09-29
Rama: `experiment/combat-stat-contract-v0.1`
Estado: **CERRADA / PASS PARA CONTINUAR / TODAVÍA LAB**

## Pregunta única

¿`ESTRATO_REACTIVO_2` mantiene controlado el escalado cuando aumenta la
cantidad de impactos, tanto con Piel base como con Corteza?

No se testean todavía:

- 3 enemigos;
- perfiles autoritativos LianQi III;
- Cuerpo de Roca;
- otras defensivas.

## Mecánica candidata

```text
Piel activa
+
Arraigo aumenta y alcanza 2 o 3
→ gana/refresca 1 Estrato

máximo almacenado = 1

siguiente impacto directo conectado
→ +2 DEF sólo para ese impacto
→ consume Estrato
```

Una evasión no consume Estrato.

Si el trigger fuerte hace saltar Arraigo 1→3, genera un solo Estrato.

## Escenario

- Tierra HP33;
- Qi31 LAB;
- DEF1;
- EVA5;
- dos enemigos reales 14 + 14 HP;
- PREC90;
- EVA20;
- DEF2;
- daño `2d4+1`;
- Piel como apertura;
- Golpe de Montaña unitarget;
- Peso PROVISIONAL STACK_REFRESH.

## Resultado principal

200.000 combates por variante:

| Variante | Win rate | HP restante | Extensión | Usos Estrato |
|---|---:|---:|---:|---:|
| Piel base | 84.91% | 40.97% | 95.90% | — |
| Piel base + Estratos | 87.30% | 45.01% | 91.80% | 1.63 |
| Corteza | 89.41% | 48.55% | 78.44% | — |
| Corteza + Estratos | 89.90% | 49.96% | 69.18% | 1.50 |

## Ganancia de Estratos

### Sobre Piel base

```text
win:
+2.39 pp

HP restante:
+4.03 pp
```

### Sobre Piel + Corteza

```text
win:
+0.49 pp

HP restante:
+1.42 pp
```

## Replicación por semillas

Cuatro semillas independientes de 50.000 combates.

### Estratos sobre Piel base

Delta de win:

- +2.410 pp;
- +2.386 pp;
- +2.478 pp;
- +2.510 pp.

Delta de HP restante:

- +4.05 pp;
- +4.08 pp;
- +4.02 pp;
- +4.24 pp.

### Estratos sobre Corteza

Delta de win:

- +0.654 pp;
- +0.518 pp;
- +0.722 pp;
- +0.374 pp.

Delta de HP restante:

- +1.46 pp;
- +1.49 pp;
- +1.74 pp;
- +1.33 pp.

La dirección del efecto se mantiene en todas las semillas.

## Hallazgo principal

El diseño logra retorno decreciente de forma natural.

```text
Estratos sin Corteza
→ mejora defensiva clara

Estratos con Corteza
→ mejora pequeña adicional
```

Eso evita que la ruta de fortificación se convierta en una suma lineal de
capas equivalentes.

## Autolimitación adicional

Estratos también reduce ON_HP_DAMAGE.

Consecuencia:

- Piel base: extensión baja 95.90% → 91.80%;
- Corteza: extensión baja 78.44% → 69.18%.

Por tanto:

```text
más protección puntual
→ menos daño llega a Vida
→ menos transiciones de Arraigo
→ menos extensión
```

La técnica se autolimita también por su propia interacción con Piel.

## Evaluación

El candidato supera la pregunta de esta etapa:

- no añade DEF permanente;
- no crea un beneficio por cada enemigo;
- sus usos están limitados por transiciones de Arraigo;
- funciona aunque no exista Corteza;
- combinado con Corteza muestra retorno decreciente;
- conserva una mejora clara contra múltiples impactos.

## Resultado de Etapa 9B

**PASS para continuar.**

`ESTRATO_REACTIVO_2` sigue como candidato principal LAB para
Estratos Compactos.

Todavía:

- NO PROVISIONAL;
- NO CANON;
- NO runtime.

## Próxima etapa

**ETAPA 9C — ESTRATO_REACTIVO_2 contra 3 enemigos.**

Pregunta única:

¿el diseño sigue acotado cuando hay tres acciones enemigas potenciales por
ronda, o el mayor número de impactos permite extraer demasiado valor de las
ventanas reactivas?

No abrir todavía Cuerpo de Roca.
