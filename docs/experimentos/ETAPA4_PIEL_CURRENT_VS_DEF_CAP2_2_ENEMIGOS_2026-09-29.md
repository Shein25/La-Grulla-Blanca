# ETAPA 4 — Piel CURRENT vs DEF_CAP2 · 2 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / NO PROMOCIÓN**

## Pregunta única

¿Cuánto recorta `DEF_CAP2` el escalado de Piel de Cobre cuando el jugador
recibe dos acciones enemigas por ronda?

No se testean todavía:

- 3 enemigos;
- Control enemigo;
- otras defensivas;
- AOE.

## Baseline

Jugador Tierra:

- HP efectivo 33;
- Qi31 LAB;
- DEF1;
- EVA5;
- Piel como apertura;
- Golpe de Montaña narrow;
- Peso PROVISIONAL STACK_REFRESH.

Dos enemigos reales:

- HP total ~28;
- 14 HP cada uno;
- PREC90;
- EVA20;
- DEF2;
- ataque `2d4+1`;
- cada enemigo vivo ejecuta una acción por ronda.

## Resultado principal

Simulación de 200.000 combates:

| Métrica | CURRENT | DEF_CAP2 |
|---|---:|---:|
| Win rate | 88.83% | 84.91% |
| Rondas medias | 7.25 | 7.15 |
| HP restante medio | 46.52% | 40.97% |
| Usa ataque básico | 82.06% | 81.94% |
| Arraigo máximo medio | 2.96 | 2.96 |
| Impactos enemigos medios | 7.87 | 7.82 |
| Daño recibido medio | 17.89 | 19.81 |
| Activa extensión de Piel | 95.89% | 95.90% |

Diferencias:

```text
Win rate:
DEF_CAP2 ≈ -3.92 pp

HP restante:
DEF_CAP2 ≈ -5.54 pp
```

## Repetición por semillas

Cuatro semillas independientes de 100.000 combates:

Delta de win:

- −4.040 pp;
- −3.947 pp;
- −3.766 pp;
- −3.882 pp.

Delta de HP restante:

- −5.54 pp;
- −5.49 pp;
- −5.44 pp;
- −5.58 pp.

La dirección y magnitud son estables.

## Lectura

Ésta es la primera etapa donde `DEF_CAP2` deja de ser casi equivalente a
CURRENT.

Eso es exactamente donde esperábamos que actuara el ajuste:

- con un solo enemigo, la tercera unidad de DEF máxima importa poco;
- con dos atacantes, esa unidad adicional se aplica repetidamente;
- CURRENT convierte DEF6 en una reducción fuerte sobre muchas acciones;
- DEF_CAP2 detiene Piel en DEF5 y reduce ese crecimiento acumulativo.

Importante:

- ambas variantes siguen alcanzando 3 Arraigos casi siempre;
- ambas activan la extensión ~96% de los combates;
- el ajuste no está frenando la identidad reactiva;
- está reduciendo específicamente el valor repetido de la DEF máxima.

## ¿Es demasiado recorte?

Todavía no se puede responder.

DEF_CAP2 mantiene:

- ~85% de victoria contra dos enemigos;
- ~41% HP restante medio;
- una mejora defensiva todavía muy importante respecto de Tierra sin Piel.

Pero la diferencia de ~4 pp frente a CURRENT ya es suficientemente grande para
que **no podamos aprobar DEF_CAP2 sólo con los tests 1v1**.

## Conclusión de Etapa 4

**RESULTADO: DEF_CAP2 sigue siendo viable, pero entra en zona de decisión.**

No se marca PASS definitivo ni FAIL.

Interpretación:

> el ajuste logra su objetivo de contener el escalado multiimpacto, pero ahora
> debemos comprobar si frente a 3 enemigos corrige un exceso o recorta demasiado
> la identidad de Tierra bajo presión.

## Próxima etapa

**ETAPA 5 — CURRENT vs DEF_CAP2 contra 3 enemigos.**

No avanzar todavía a Control enemigo ni a otras defensivas.
