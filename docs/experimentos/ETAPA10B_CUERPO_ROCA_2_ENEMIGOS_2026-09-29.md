# ETAPA 10B — Cuerpo de Roca · 2 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA / PASS PARA CONTINUAR / TODAVÍA LAB**

## Pregunta única

¿`ROCA_GUARD_MAX_3` evita escalar con la cantidad de atacantes cuando hay
dos enemigos reales?

No se testean todavía:

- 3 enemigos;
- perfil autoritativo LianQi IV;
- otras defensivas.

## Candidato

```text
Piel activa
+
Arraigo == 3
↓
al comienzo del turno del usuario
se arma 1 Guardia de Roca

primer impacto directo conectado de ese turno
→ +3 DEF sólo para ese impacto
→ consume Guardia
```

Reglas:

- una evasión no consume Guardia;
- si Arraigo alcanza 3 durante las acciones enemigas, la Guardia NO se arma
  retroactivamente;
- se arma en el siguiente turno del usuario si Piel sigue activa y Arraigo
  sigue en 3;
- no aumenta DEF permanente;
- no altera Tenacidad, duración ni máximo de Arraigo.

## Escenario

- Tierra HP33;
- Qi31 LAB;
- DEF1;
- EVA5;
- 2 enemigos reales 14 + 14 HP;
- PREC90;
- EVA20;
- DEF2;
- daño `2d4+1`;
- Piel de apertura;
- Golpe de Montaña unitarget;
- Peso PROVISIONAL STACK_REFRESH.

## Resultado principal

200.000 combates:

| Variante | Win rate | HP restante | Extensión | Arraigo máx. | Usos Roca |
|---|---:|---:|---:|---:|---:|
| Piel base | 84.91% | 40.97% | 95.90% | 2.957 | — |
| Piel + Roca | 89.06% | 47.98% | 95.88% | 2.957 | 2.16 |
| Corteza + Estratos | 89.90% | 49.96% | 69.18% | 2.679 | — |
| Corteza + Estratos + Roca | 90.65% | 51.63% | 69.14% | 2.678 | 1.19 |

## Ganancia de Cuerpo de Roca

### Sobre Piel base

```text
win:
+4.15 pp

HP restante:
+7.00 pp
```

### Sobre ruta Corteza + Estratos

```text
win:
+0.75 pp

HP restante:
+1.66 pp
```

## Replicación por semillas

Cuatro semillas independientes de 50.000 combates.

### Sobre Piel base

Delta de win:

- +4.238 pp;
- +4.114 pp;
- +4.146 pp;
- +4.168 pp.

Delta de HP:

- +6.92 pp;
- +6.94 pp;
- +6.87 pp;
- +7.13 pp.

Usos de Guardia:

- ~2.15 por combate.

### Sobre ruta Corteza + Estratos

Delta de win:

- +0.640 pp;
- +0.786 pp;
- +0.674 pp;
- +0.708 pp.

Delta de HP:

- +1.62 pp;
- +1.65 pp;
- +1.53 pp;
- +1.66 pp.

Usos de Guardia:

- ~1.19 por combate.

La dirección del efecto es estable.

## Hallazgo principal

La condición `Arraigo == 3` evita que Cuerpo de Roca interfiera con la
construcción de Piel.

Prácticamente no cambia:

- Arraigo máximo medio;
- frecuencia de extensión.

Eso contrasta con variantes que protegían desde Arraigo2.

## Escalado con dos atacantes

Cuerpo de Roca NO se activa una vez por enemigo.

El límite es:

```text
máximo 1 Guardia por turno del usuario
```

Por tanto dos enemigos pueden aumentar la probabilidad de consumir esa Guardia,
pero no duplican automáticamente su número.

El resultado muestra:

- ~2.16 usos con Piel sola;
- ~1.19 usos con la ruta previa completa.

La segunda cifra baja porque Corteza + Estratos ya evitan parte del daño y
reducen la frecuencia con que Piel llega/mantiene su estado máximo.

## Retornos decrecientes

El patrón es muy fuerte:

```text
Cuerpo de Roca sin ramas previas
→ mejora grande

Cuerpo de Roca después de Corteza + Estratos
→ mejora pequeña adicional
```

Eso es deseable porque Tramo III debe funcionar como elección independiente,
pero no convertir una ruta completa de fortificación en una suma lineal de
capas equivalentes.

## Resultado de Etapa 10B

**PASS para continuar.**

`ROCA_GUARD_MAX_3` sigue como candidato principal LAB para Cuerpo de Roca.

Todavía:

- NO PROVISIONAL;
- NO CANON;
- NO runtime.

## Próxima etapa

**ETAPA 10C — ROCA_GUARD_MAX_3 contra 3 enemigos.**

Pregunta única:

¿el límite de una Guardia por turno sigue manteniendo acotado el beneficio
cuando existen tres atacantes?

Si pasa, habrá evidencia suficiente para decidir promoción a PROVISIONAL.
