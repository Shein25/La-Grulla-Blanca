# ETAPA 9C — Estratos Compactos · 3 enemigos

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA / PASS / PROMOCIÓN A PROVISIONAL JUSTIFICADA**

## Pregunta única

¿`ESTRATO_REACTIVO_2` sigue acotado cuando hay tres acciones enemigas potenciales por ronda?

No se testean todavía:

- perfiles numéricos autoritativos de LianQi III;
- Cuerpo de Roca;
- otras defensivas.

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
Arraigo aumenta y alcanza 2 o 3
→ gana/refresca 1 Estrato Compacto

máximo almacenado = 1

siguiente impacto directo conectado
→ +2 DEF sólo para ese impacto
→ consume Estrato
```

Una evasión no consume Estrato.

Si el trigger fuerte hace saltar 1→3 Arraigos, genera un solo Estrato.

## Resultado principal

200.000 combates:

| Variante | Win rate | HP restante | Extensión | Usos Estrato |
|---|---:|---:|---:|---:|
| Piel base | 57.90% | 19.50% | 99.42% | — |
| Piel base + Estratos | 62.43% | 22.73% | 98.82% | 1.72 |
| Corteza | 70.03% | 28.83% | 92.34% | — |
| Corteza + Estratos | 71.71% | 30.53% | 88.59% | 1.74 |

## Ganancia de Estratos

### Sobre Piel base

```text
win:
+4.53 pp

HP restante:
+3.24 pp
```

### Sobre Corteza

```text
win:
+1.68 pp

HP restante:
+1.71 pp
```

## Replicación por semillas

Cuatro semillas independientes de 50.000 combates.

Sobre Piel base, delta de win:

- +4.546 pp;
- +4.624 pp;
- +4.534 pp;
- +4.056 pp.

Sobre Corteza:

- +1.546 pp;
- +1.728 pp;
- +1.904 pp;
- +1.730 pp.

La dirección se mantiene en todas las semillas.

## Escalado por cantidad de enemigos

Usos medios aproximados del Estrato:

```text
2 enemigos:
~1.63 sin Corteza
~1.50 con Corteza

3 enemigos:
~1.72 sin Corteza
~1.74 con Corteza
```

El número de usos no crece proporcionalmente con el número de ataques recibidos.

La razón es estructural:

> los Estratos nacen de transiciones de Arraigo, no de impactos enemigos.

Por tanto, tres enemigos pueden consumir más rápido las ventanas, pero no pueden fabricarlas de forma ilimitada.

## Retornos decrecientes

El patrón acumulado es consistente:

```text
Estratos sin Corteza
→ mejora apreciable

Estratos después de Corteza
→ mejora adicional claramente menor
```

En 3 enemigos:

- Piel base gana ~4.5 pp;
- sobre Corteza sólo ~1.7 pp.

Esto evita que la ruta completa sea una suma lineal de bonificaciones equivalentes.

## Relación con la extensión

La mitigación adicional vuelve a autolimitar Piel:

- Piel base: 99.42% → 98.82%;
- Corteza: 92.34% → 88.59%.

Más protección puntual reduce ON_HP_DAMAGE y, por tanto, parte del crecimiento reactivo posterior.

## Conclusión

**PASS.**

`ESTRATO_REACTIVO_2` supera:

- screen 1v1;
- sensibilidad contra golpe pesado;
- 2 enemigos;
- 3 enemigos;
- prueba con y sin Corteza.

No crea DEF7 permanente y conserva retornos decrecientes.

## Decisión

Promover `ESTRATO_REACTIVO_2` de LAB a **PROVISIONAL** para Estratos Compactos.

No pasa a CANON.

## Guardia futura

Esta promoción define la arquitectura y magnitud provisional del nodo, pero no sustituye el futuro benchmark específico de LianQi III cuando exista un perfil enemigo numérico autorizado para esa etapa.

## Próxima etapa

**Cuerpo de Roca — Tramo III / LianQi IV.**

Debe continuar la especialización defensiva sin añadir una nueva escalera permanente de DEF plana.
