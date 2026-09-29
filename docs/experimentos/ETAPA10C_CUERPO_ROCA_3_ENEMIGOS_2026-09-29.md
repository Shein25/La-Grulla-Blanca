# ETAPA 10C — Cuerpo de Roca · 3 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA / PASS / PROMOCIÓN A PROVISIONAL JUSTIFICADA**

## Pregunta única

¿`ROCA_GUARD_MAX_3` sigue acotado cuando existen tres atacantes?

## Escenario

- Tierra HP33;
- Qi31 LAB;
- DEF1;
- EVA5;
- tres enemigos reales 10 + 9 + 9 HP;
- PREC90;
- EVA20;
- DEF2;
- daño `2d4+1`;
- Piel de apertura;
- Golpe de Montaña unitarget;
- Peso PROVISIONAL STACK_REFRESH.

## Mecánica candidata

```text
Piel activa
+
Arraigo == 3
↓
al comienzo de cada turno del usuario
se arma 1 Guardia de Roca

primer impacto directo conectado de ese turno
→ +3 DEF sólo para ese impacto
→ consume Guardia
```

Una evasión no consume Guardia.

Alcanzar Arraigo3 durante las acciones enemigas no arma la Guardia
retroactivamente; se arma en el siguiente turno del usuario.

## Resultado principal

200.000 combates:

| Variante | Win rate | HP restante | Extensión | Arraigo máx. | Usos Roca |
|---|---:|---:|---:|---:|---:|
| Piel base | 57.90% | 19.50% | 99.42% | 2.994 | — |
| Piel + Roca | 66.35% | 25.67% | 99.43% | 2.994 | 2.65 |
| Corteza + Estratos | 71.71% | 30.53% | 88.59% | 2.884 | — |
| Corteza + Estratos + Roca | 73.87% | 32.89% | 88.52% | 2.883 | 1.87 |

## Ganancia de Cuerpo de Roca

### Sobre Piel base

```text
win:
+8.45 pp

HP restante:
+6.18 pp
```

### Sobre ruta Corteza + Estratos

```text
win:
+2.16 pp

HP restante:
+2.36 pp
```

## Replicación por semillas

Cuatro semillas independientes de 50.000 combates.

### Sobre Piel base

Delta de win:

- +8.388 pp;
- +8.506 pp;
- +8.098 pp;
- +8.256 pp.

Delta de HP:

- +6.15 pp;
- +6.13 pp;
- +6.00 pp;
- +6.07 pp.

Usos de Guardia:

- ~2.64–2.65 por combate.

### Sobre ruta Corteza + Estratos

Delta de win:

- +2.562 pp;
- +2.100 pp;
- +2.088 pp;
- +2.256 pp.

Delta de HP:

- +2.46 pp;
- +2.38 pp;
- +2.35 pp;
- +2.46 pp.

Usos de Guardia:

- ~1.87–1.88 por combate.

La dirección del efecto es estable.

## ¿Escala con el número de atacantes?

No de forma lineal.

La Guardia está limitada por:

```text
máximo 1 activación útil por turno del usuario
```

Tres enemigos aumentan la probabilidad de consumirla, pero no crean tres
Guardias.

Comparación de usos:

```text
2 enemigos:
~2.15 sobre Piel
~1.19 sobre ruta completa

3 enemigos:
~2.65 sobre Piel
~1.87 sobre ruta completa
```

El crecimiento existe porque Piel permanece más tiempo bajo presión y hay más
ocasiones de conectar un impacto, pero está muy lejos de multiplicarse por el
número de atacantes.

## Interacción con Arraigo y extensión

La condición Arraigo3 sigue funcionando como guardia estructural.

En la simulación principal:

- extensión Piel base: 99.420% → 99.435% con Roca;
- ruta completa: 88.591% → 88.520%;
- Arraigo máximo prácticamente no cambia.

Por tanto Cuerpo de Roca no está acelerando ni frenando materialmente la
construcción de Piel.

## Retornos decrecientes

El nodo funciona como elección independiente:

```text
Piel + Cuerpo de Roca
→ mejora grande bajo presión múltiple
```

Pero cuando ya existen Corteza + Estratos:

```text
Cuerpo de Roca
→ mejora adicional mucho menor
```

Esto preserva libertad de rutas sin hacer que apilar toda la línea de
fortificación produzca una suma lineal de potencia.

## Conclusión

**PASS.**

`ROCA_GUARD_MAX_3` supera:

- screen 1v1;
- sensibilidad contra golpes pesados;
- 2 enemigos;
- 3 enemigos;
- prueba independiente;
- prueba apilada con Corteza + Estratos.

No crea DEF permanente adicional.

## Decisión

Promover `ROCA_GUARD_MAX_3` de LAB a **PROVISIONAL** para Cuerpo de Roca.

No pasa a CANON.

## Guardia futura

La magnitud deberá revalidarse cuando exista un perfil enemigo numérico
autoritativo de LianQi IV.

## Estado de la ruta de fortificación

```text
LianQi I
Piel base
PROVISIONAL

LianQi II
Corteza Endurecida
PROVISIONAL

LianQi III
Estratos Compactos
PROVISIONAL

LianQi IV
Cuerpo de Roca
PROVISIONAL
```

La ruta completa queda estructuralmente cerrada para el benchmark actual,
pendiente de validación por etapa cuando existan perfiles LianQi II–IV
autoritativos.
