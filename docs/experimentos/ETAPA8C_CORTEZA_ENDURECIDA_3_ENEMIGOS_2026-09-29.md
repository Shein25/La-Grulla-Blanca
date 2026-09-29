# ETAPA 8C — Corteza Endurecida · 3 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA / PASS / PROMOCIÓN RECOMENDADA A PROVISIONAL**

## Pregunta única

¿La curva candidata de Corteza Endurecida `5 → 6 → 6` vuelve a escalar
demasiado cuando hay tres acciones enemigas potenciales por ronda?

No se testean todavía:

- Tramo II;
- Tramo III;
- enemigos LianQi III/IV;
- otras defensivas.

## Variantes

### Piel base PROVISIONAL

Con DEF base1 del benchmark:

```text
DEF total:
4 → 5 → 5
```

### Piel + Corteza candidata

```text
DEF total:
5 → 6 → 6
```

La tercera carga sigue sin añadir una unidad nueva de DEF.

## Escenario

- Tierra HP33;
- Qi31 LAB;
- DEF base1;
- EVA5;
- tres enemigos reales: 10 + 9 + 9 HP;
- HP enemigo total = 28;
- PREC90;
- EVA20;
- DEF2;
- daño enemigo `2d4+1`;
- una acción por enemigo vivo y ronda;
- Piel como apertura;
- Golpe de Montaña unitarget;
- Peso PROVISIONAL STACK_REFRESH.

## Resultado principal

200.000 combates:

| Métrica | Piel base | Piel + Corteza |
|---|---:|---:|
| Win rate | 57.90% | 70.03% |
| Rondas medias | 7.19 | 7.60 |
| HP restante medio | 19.50% | 28.83% |
| Usa ataque básico | 93.15% | 95.86% |
| Arraigo máximo medio | 2.99 | 2.92 |
| Extensión activada | 99.42% | 92.34% |
| Impactos enemigos medios | 11.42 | 11.74 |
| Daño recibido medio | 27.51 | 24.16 |

Diferencias:

```text
Win rate:
Corteza ≈ +12.13 pp

HP restante:
Corteza ≈ +9.33 pp

Extensión:
Corteza ≈ -7.08 pp
```

## Repetición por semillas

Cuatro semillas independientes de 100.000 combates:

Delta de win:

- +12.239 pp;
- +12.117 pp;
- +11.862 pp;
- +11.947 pp.

Delta de HP restante:

- +9.40 pp;
- +9.05 pp;
- +9.03 pp;
- +9.09 pp.

Delta de extensión:

- −7.05 pp;
- −7.09 pp;
- −7.16 pp;
- −7.22 pp.

La dirección y magnitud son estables.

## Lectura

Corteza gana mucho valor cuando aumenta la cantidad de impactos porque toda DEF
plana se aplica repetidamente.

Eso no es un bug: es precisamente la identidad de una ruta dedicada de
fortificación.

La pregunta relevante es si el resultado vuelve a la sobreprotección de la
Piel base antigua.

### Comparación con la Piel CURRENT descartada

En el mismo escenario de tres enemigos:

```text
Tierra sin Piel                ≈ 17.34% win
Piel base nueva 4→5→5         ≈ 57.90%
Piel antigua CURRENT 4→5→6    ≈ 68.04%
Piel nueva + Corteza 5→6→6    ≈ 70.03%
```

La rama de Tramo I supera ligeramente la antigua Piel base.

Eso se considera razonable porque:

- el poder ya no viene gratis en LianQi I;
- requiere invertir una elección de Tramo I;
- la tercera carga no vuelve a escalar DEF;
- la mayor DEF reduce ON_HP_DAMAGE;
- eso baja Arraigo máximo medio y frecuencia de extensión.

## Hallazgo para Tramos II y III

La etapa deja una advertencia clara:

> a partir de DEF total 6, añadir más DEF plana permanente por Tramo puede
> volver a escalar demasiado contra múltiples atacantes.

Por tanto:

- Estratos Compactos no debe recibir automáticamente otro +1 DEF permanente;
- Cuerpo de Roca tampoco debe asumir crecimiento lineal de DEF;
- las siguientes ramas de fortificación deberán explorar retornos decrecientes,
  condiciones, ventanas o transformación de defensa, no una escalera infinita.

## Resultado de Etapa 8C

**PASS.**

La curva:

```text
Piel + Corteza
DEF total 5 → 6 → 6
```

supera las pruebas 1v1, 2 enemigos y 3 enemigos.

## Decisión recomendada

Promover `CORTEZA_PLUS1_CAP` de LAB a **PROVISIONAL** para Tramo I:

```text
Corteza Endurecida

mientras Piel esté activa:
la contribución acumulada de DEF de Arraigo pasa de

1 / 2 / 2

a

2 / 3 / 3
```

Equivalente, con +2 DEF inmediata de Piel:

```text
Piel + Corteza aporta:
+4 / +5 / +5 DEF
```

Con DEF base1 del benchmark:

```text
DEF total:
5 → 6 → 6
```

## Próxima etapa

Tras promoción, el siguiente bloque debe ser **Estratos Compactos (Tramo II)**,
pero no puede diseñarse como un simple +1 DEF adicional.

Debe buscar una mejora de fortificación compatible con la advertencia
multiimpacto de esta etapa.
