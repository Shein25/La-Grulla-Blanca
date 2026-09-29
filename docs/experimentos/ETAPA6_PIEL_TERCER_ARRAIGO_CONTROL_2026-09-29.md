# ETAPA 6 — Valor del tercer Arraigo frente a Control

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / DEF_CAP2 SIGUE COMO CANDIDATO PRINCIPAL LAB**

## Pregunta única

Si `DEF_CAP2` hace que el tercer Arraigo ya no añada otra unidad de DEF,
¿esa tercera carga conserva valor mecánico suficiente mediante:

- +3 Tenacidad;
- extensión de Piel al alcanzar 3 Arraigos?

No se testean:

- daño;
- grupos;
- otras defensivas;
- una técnica enemiga concreta;
- duración/severidad posterior de un Control aplicado.

## Fórmula CANON

```text
Control efectivo =
potencia base
+ Control del atacante
+ buffs
- debuffs

P(Control) =
clamp(Control efectivo - Tenacidad, 5, 100)
```

Tenacidad de Tierra:

```text
raíz Tierra = +5 Tenacidad
```

Piel:

```text
cada Arraigo = +3 Tenacidad
```

Por tanto:

| Estado | Tenacidad efectiva por estas fuentes |
|---|---:|
| Tierra sin Piel | 5 |
| Piel · 1 Arraigo | 8 |
| Piel · 2 Arraigos | 11 |
| Piel · 3 Arraigos | 14 |

## Aporte exacto del tercer Arraigo

Mientras la fórmula no esté pegada a un clamp:

```text
2 Arraigos
Tenacidad 11

3 Arraigos
Tenacidad 14
```

Por tanto:

```text
tercer Arraigo
→ +3 Tenacidad
→ -3 puntos porcentuales de probabilidad de Control
   por cada intento enemigo
```

Este resultado es determinístico; no necesita Monte Carlo.

La diferencia completa de 3 pp se conserva para una zona muy amplia de
Control efectivo. Sólo se comprime cuando las probabilidades chocan contra el
mínimo 5% o el máximo 100%.

## Valor de la extensión

Al alcanzar 3 Arraigos, Piel obtiene además:

```text
+1 turno a la duración restante
una vez por activación
```

Durante ese turno extra:

```text
Piel con 3 Arraigos
Tenacidad = 14

Piel ya expirada
Tierra conserva sólo Tenacidad = 5
```

Diferencia:

```text
+9 Tenacidad
→ hasta -9 pp de probabilidad de Control
   durante ese turno adicional
```

Por tanto la tercera carga bajo DEF_CAP2 sigue aportando dos capas distintas:

1. +3 Tenacidad frente al segundo Arraigo;
2. extensión de un turno manteniendo la protección completa de Piel.

## Ejemplo numérico ilustrativo

Para visualizar la magnitud se usa:

```text
Control efectivo = 65
```

Esto **NO** se declara como estadística canónica de un enemigo.
Es sólo un ancla matemática dentro de la escala ya utilizada para Control.

Probabilidades:

| Estado | P(Control) |
|---|---:|
| Tierra sin Piel · T5 | 60% |
| Piel · 2 Arraigos · T11 | 54% |
| Piel · 3 Arraigos · T14 | 51% |

Supongamos un horizonte ilustrativo de tres intentos de Control:

### Si Piel queda en 2 Arraigos

Dos intentos ocurren con T11 y el tercero después de expirar con T5:

```text
54% + 54% + 60%
→ 1.68 aplicaciones esperadas
```

Probabilidad de resistir los tres:

```text
46% × 46% × 40%
= 8.464%
```

### Si alcanza 3 Arraigos y activa extensión

Los tres intentos ocurren con T14:

```text
51% + 51% + 51%
→ 1.53 aplicaciones esperadas
```

Probabilidad de resistir los tres:

```text
49%^3
= 11.765%
```

Diferencia:

```text
-0.15 aplicaciones esperadas de Control
+3.30 pp de probabilidad de resistir los tres intentos
```

De nuevo: el ejemplo sólo ilustra la fórmula; no define una cadencia real de
Control enemigo.

## Relación CURRENT vs DEF_CAP2

En este eje no existe diferencia:

```text
CURRENT
3 Arraigos
→ +9 Tenacidad
→ extensión

DEF_CAP2
3 Arraigos
→ +9 Tenacidad
→ extensión
```

La diferencia entre ambas variantes sigue siendo exclusivamente:

```text
CURRENT
tercer Arraigo añade otra unidad de DEF

DEF_CAP2
tercer Arraigo no añade esa tercera unidad incremental de DEF
```

Por tanto eliminar +1 DEF en la tercera carga **no elimina la razón de alcanzar
Arraigo máximo**.

## Conclusión de Etapa 6

**PASS.**

El tercer Arraigo de `DEF_CAP2` sigue teniendo valor mecánico real:

- +3 Tenacidad adicional;
- -3 pp de Control por intento en el rango lineal;
- activa la extensión;
- el turno extendido conserva +9 Tenacidad de Piel frente a Piel expirada.

Esto resuelve la preocupación de que el tercer Arraigo pudiera convertirse en
una carga casi decorativa al no añadir DEF.

## Estado acumulado de DEF_CAP2

| Etapa | Resultado |
|---|---|
| 1 · común 1v1 | PASS |
| 2 · pesado 1v1 | PASS |
| 3 · preciso 1v1 | PASS |
| 4 · 2 enemigos | viable / recorte visible |
| 5 · 3 enemigos | candidato principal LAB |
| 6 · valor vs Control | PASS |

## Próxima etapa

No abrir todavía otras defensivas.

La siguiente etapa debe ser una **decisión de cierre de Piel base**:

- revisar conjuntamente únicamente la evidencia de Etapas 1–6;
- decidir si `DEF_CAP2` puede pasar de LAB a PROVISIONAL;
- si se promueve, actualizar después las ramas de fortificación que dependan de
  la antigua escalera de DEF.

