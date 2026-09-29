# ETAPA 7 — Cierre de Piel de Cobre base

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA / DEF_CAP2 PROMOVIDO A PROVISIONAL**

## Pregunta única

¿La evidencia acumulada de Etapas 1–6 es suficiente para promover
`DEF_CAP2` desde LAB a PROVISIONAL como curva base de Piel de Cobre?

## Evidencia acumulada

| Etapa | Escenario | CURRENT | DEF_CAP2 | Lectura |
|---|---|---:|---:|---|
| 1 | común 1v1 | 96.21% | 95.60% | diferencia mínima |
| 2 | pesado 1v1 | 93.91% | 92.96% | pérdida moderada |
| 3 | preciso 1v1 | 94.70% | 93.87% | diferencia estable |
| 4 | 2 enemigos | 88.83% | 84.91% | recorte multiimpacto visible |
| 5 | 3 enemigos | 68.04% | 57.90% | corrige escalado fuerte |
| 6 | Control/Tenacidad | — | PASS | tercera carga conserva función |

## Patrón observado

La diferencia de win de DEF_CAP2 frente a CURRENT fue:

```text
1v1 común     -0.61 pp
1v1 pesado    -0.95 pp
1v1 preciso   -0.83 pp
2 enemigos    -3.92 pp
3 enemigos   -10.14 pp
```

Esto demuestra un patrón deseable:

```text
pocos impactos
→ el ajuste casi no se siente

muchos impactos
→ el ajuste reduce progresivamente el valor repetido de DEF plana
```

## Identidad preservada

DEF_CAP2 conserva:

- activación con +2 DEF inmediata;
- 1 Arraigo inicial;
- máximo 3 Arraigos;
- +3 Tenacidad por Arraigo;
- trigger reactivo por daño directo a Vida;
- trigger fuerte de +2 Arraigos;
- extensión de +1 turno al alcanzar máximo;
- Eco de Tierra.

No cambia:

- frecuencia de Arraigo;
- identidad reactiva;
- utilidad contra Control;
- extensión;
- coste;
- duración base.

## Curva promovida

La contribución de DEF de Piel queda PROVISIONALMENTE:

```text
1 Arraigo
+2 DEF inmediata
+1 DEF de Arraigo
= +3 DEF de Piel

2 Arraigos
+2 DEF inmediata
+2 DEF acumulada de Arraigo
= +4 DEF de Piel

3 Arraigos
+2 DEF inmediata
+2 DEF acumulada de Arraigo
= +4 DEF de Piel
```

Con DEF base1 del benchmark:

```text
DEF total
4 → 5 → 5
```

Tenacidad permanece:

```text
+3 → +6 → +9
```

## Por qué se descarta CURRENT como candidato principal

CURRENT alcanzaba:

```text
DEF total 4 → 5 → 6
```

En 1v1 la diferencia era pequeña.

Con múltiples atacantes, la tercera unidad de DEF se aplicaba repetidamente a
cada impacto y generaba una amplificación excesiva:

- ~4 pp de win con 2 enemigos;
- ~10 pp con 3 enemigos.

Ese comportamiento no provenía de una identidad nueva, sino de repetir una
reducción plana muy alta sobre muchas acciones.

## Tercera carga no decorativa

Al pasar de 2 a 3 Arraigos bajo DEF_CAP2:

- +3 Tenacidad adicionales;
- reduce P(Control) en 3 pp por intento en rango lineal;
- activa la extensión de Piel;
- durante el turno extendido mantiene +9 Tenacidad de Piel.

Por tanto la tercera carga sigue siendo una meta mecánica relevante.

## Decisión

**DEF_CAP2 pasa de LAB a PROVISIONAL para la base de Piel de Cobre.**

No pasa a CANON.

## Cambios documentales aplicados

Se actualizó:

`docs/experimentos/TECNICAS_ARCO1_DISENO_APROBADO_2026-09-28.md`

La base ahora declara la curva DEF_CAP2 como PROVISIONAL.

## Guardia sobre Tramos

Las ramas de fortificación que dependían de la vieja escalera deben
recalibrarse:

- Corteza Endurecida;
- Estratos Compactos;
- Cuerpo de Roca.

Sus magnitudes anteriores dejan de ser autoridad numérica.

Las ramas de Tenacidad y aguante no se modifican en esta etapa.

## Próxima etapa

La siguiente etapa ya no debe seguir tocando Piel base.

Corresponde volver al bloque de defensivas y elegir **una sola** de estas
líneas para continuar:

1. recalibrar ramas de fortificación de Piel sobre DEF_CAP2;
2. cerrar Cuerpo-Horno base 25%;
3. cerrar Espejo de Luna base 24%;
4. cerrar Paso de Nube Ligera base +35 EVA / 4 turnos.

No mezclar más de una en la misma etapa.
