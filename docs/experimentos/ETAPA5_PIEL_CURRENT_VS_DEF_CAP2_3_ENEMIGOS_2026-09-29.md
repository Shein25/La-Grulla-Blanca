# ETAPA 5 — Piel CURRENT vs DEF_CAP2 · 3 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / DEF_CAP2 PASA A CANDIDATO PRINCIPAL LAB**

## Pregunta única

¿Limitar la DEF máxima de Piel de Cobre de 6 a 5 corrige el exceso
multiimpacto frente a tres enemigos o destruye demasiado su identidad?

No se testean todavía:

- Control enemigo;
- otras defensivas;
- AOE;
- jefes;
- progresión de Tramos.

## Baseline

Jugador Tierra:

- HP efectivo 33;
- Qi31 LAB;
- DEF1;
- EVA5;
- Piel como apertura;
- Golpe de Montaña narrow;
- Peso PROVISIONAL STACK_REFRESH.

Tres enemigos reales:

- HP total = 28;
- 10 + 9 + 9 HP;
- PREC90;
- EVA20;
- DEF2;
- ataque `2d4+1`;
- cada enemigo vivo ejecuta una acción por ronda.

## Resultado principal

Simulación de 200.000 combates:

| Métrica | CURRENT | DEF_CAP2 |
|---|---:|---:|
| Win rate | 68.04% | 57.90% |
| Rondas medias | 7.53 | 7.19 |
| HP restante medio | 26.72% | 19.50% |
| Usa ataque básico | 95.74% | 93.15% |
| Arraigo máximo medio | 2.99 | 2.99 |
| Impactos enemigos medios | 11.68 | 11.42 |
| Daño recibido medio | 24.90 | 27.51 |
| Activa extensión de Piel | 99.41% | 99.42% |

Diferencias:

```text
Win rate:
DEF_CAP2 ≈ -10.14 pp

HP restante:
DEF_CAP2 ≈ -7.22 pp
```

## Repetición por semillas

Cuatro semillas independientes de 100.000 combates:

Delta de win:

- −10.212 pp;
- −10.050 pp;
- −10.181 pp;
- −9.903 pp.

Delta de HP restante:

- −7.25 pp;
- −6.91 pp;
- −7.09 pp;
- −6.94 pp.

La diferencia es muy estable.

## Contexto: Tierra sin Piel

En el mismo escenario de tres enemigos, Tierra sin usar Piel queda alrededor de:

- 17.34% de victoria;
- 3.71% de HP restante medio.

Por tanto, incluso DEF_CAP2 mantiene un salto enorme:

```text
sin Piel     ≈ 17%
DEF_CAP2     ≈ 58%
CURRENT      ≈ 68%
```

La técnica sigue siendo, con claridad, una respuesta muy fuerte a presión múltiple.

## Lectura

Esta etapa confirma dos cosas a la vez.

### 1. CURRENT sí está amplificando demasiado la tercera unidad de DEF

Con tres atacantes:

- Arraigo máximo se alcanza prácticamente siempre;
- la extensión se activa ~99.4%;
- DEF6 se aplica repetidamente sobre muchas acciones;
- una sola unidad adicional de DEF produce ~10 pp de diferencia de victoria.

Eso demuestra que el problema detectado en el stress anterior era real.

### 2. DEF_CAP2 no destruye la identidad de Tierra

Aunque pierde bastante frente a CURRENT:

- conserva ~58% de victoria;
- sigue superando de forma enorme a Tierra sin Piel;
- sigue alcanzando 3 Arraigos;
- sigue activando extensión;
- mantiene el mismo sistema reactivo;
- la tercera carga sigue importando por Tenacidad y extensión.

Por tanto, el ajuste no convierte Piel en una defensiva mediocre.

## Resultado de Etapa 5

**DEF_CAP2 pasa a ser el candidato principal LAB frente a CURRENT.**

No se promueve todavía a PROVISIONAL.

La evidencia acumulada queda:

| Etapa | Escenario | Efecto de DEF_CAP2 |
|---|---|---:|
| 1 | común 1v1 | −0.61 pp win |
| 2 | pesado 1v1 | −0.95 pp |
| 3 | preciso 1v1 | −0.83 pp |
| 4 | 2 enemigos | −3.92 pp |
| 5 | 3 enemigos | −10.14 pp |

Patrón:

> casi no altera el duelo normal, pero reduce progresivamente el exceso cuando
> aumenta la cantidad de impactos.

Ese comportamiento coincide con el objetivo del ajuste.

## Siguiente etapa

**ETAPA 6 — comprobar DEF_CAP2 contra Control enemigo.**

Pregunta única:

¿La tercera carga sigue teniendo suficiente valor cuando deja de aportar DEF
pero conserva +3 Tenacidad y la extensión?

No probar todavía otras defensivas.
