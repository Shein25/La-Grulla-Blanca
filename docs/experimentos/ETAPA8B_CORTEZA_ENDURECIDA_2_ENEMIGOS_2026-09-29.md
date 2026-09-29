# ETAPA 8B — Corteza Endurecida · 2 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / PASS PARA CONTINUAR / TODAVÍA LAB**

## Pregunta única

¿La curva candidata de Corteza Endurecida `5 → 6 → 6` conserva una mejora
razonable contra dos enemigos sin reabrir el problema multiimpacto que motivó
`DEF_CAP2`?

No se testean todavía:

- 3 enemigos;
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

La tercera carga sigue sin añadir otra unidad de DEF.

## Escenario

- Tierra HP33;
- Qi31 LAB;
- DEF base1;
- EVA5;
- dos enemigos reales de 14 HP;
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
| Win rate | 84.91% | 89.41% |
| Rondas medias | 7.15 | 7.26 |
| HP restante medio | 40.97% | 48.55% |
| Usa ataque básico | 81.94% | 82.04% |
| Arraigo máximo medio | 2.96 | 2.77 |
| Extensión activada | 95.90% | 78.44% |
| Impactos enemigos medios | 7.82 | 7.88 |
| Daño recibido medio | 19.81 | 17.20 |

Diferencias:

```text
Win rate:
Corteza ≈ +4.50 pp

HP restante:
Corteza ≈ +7.58 pp

Extensión:
Corteza ≈ -17.46 pp
```

## Repetición por semillas

Cuatro semillas independientes de 100.000 combates:

Delta de win:

- +4.611 pp;
- +4.592 pp;
- +4.531 pp;
- +4.562 pp.

Delta de HP restante:

- +7.54 pp;
- +7.61 pp;
- +7.49 pp;
- +7.58 pp.

Delta de extensión:

- −17.54 pp;
- −17.22 pp;
- −17.32 pp;
- −17.46 pp.

La dirección y magnitud son muy estables.

## Lectura

Corteza hace exactamente lo esperable de una rama de fortificación de Tramo I:

- mejora de forma clara la supervivencia;
- aumenta la tasa de victoria;
- no añade daño;
- no reabre crecimiento de DEF en el tercer Arraigo.

Pero aparece una contrapartida sistémica importante:

```text
más DEF
→ menos daño llega a Vida
→ menos ON_HP_DAMAGE
→ menos Arraigo generado
→ menos extensiones
```

Por eso Corteza no es simplemente una suma lineal de defensa.

La propia técnica reduce la frecuencia con la que alcanza y explota su estado
máximo.

## Comparación con la Piel CURRENT descartada

La antigua Piel base con DEF total `4 → 5 → 6` había dado aproximadamente
88.8% de victoria contra dos enemigos.

Piel PROVISIONAL + Corteza candidata queda alrededor de 89.4%.

Esto es coherente con una especialización de Tramo I:

- el personaje invertido en fortificación puede superar la vieja Piel base;
- pero lo hace mediante una elección de progresión;
- no porque la técnica base entregue DEF6 gratuitamente;
- la tercera carga continúa sin añadir DEF nueva.

## ¿Reabre el problema multiimpacto?

En este escenario de dos enemigos, **no hay evidencia suficiente para afirmar
que lo reabre**.

La ganancia de +4.5 pp es significativa, pero:

- pertenece a una rama dedicada exclusivamente a fortificación;
- la extensión cae mucho;
- Arraigo máximo medio también cae;
- el incremento no proviene de devolver +1 DEF a la tercera carga.

Sin embargo, dado que el problema original apareció con fuerza al pasar a tres
enemigos, no corresponde promover Corteza todavía.

## Resultado de Etapa 8B

**PASS para continuar.**

`CORTEZA_PLUS1_CAP` sigue siendo el candidato LAB principal:

```text
Piel + Corteza:
DEF total 5 → 6 → 6
```

Todavía **NO PROVISIONAL**.

## Próxima etapa

**ETAPA 8C — Corteza candidata contra 3 enemigos.**

Pregunta única:

¿la mejora de fortificación sigue siendo una especialización razonable cuando
hay tres acciones enemigas potenciales por ronda, o vuelve a escalar demasiado?

No abrir todavía Estratos Compactos ni Cuerpo de Roca.
