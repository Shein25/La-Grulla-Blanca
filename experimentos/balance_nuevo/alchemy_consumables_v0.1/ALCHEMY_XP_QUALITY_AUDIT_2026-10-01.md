# Alquimia — auditoría de XP, práctica y calidad

Fecha: 2026-10-01

Estado: **RECOMENDACIÓN DE CONSERVAR EL NÚCLEO ACTUAL**

## Sistema actual

Umbrales globales:

```text
Iniciado   0 XP
Novicio   50 XP
Aprendiz 180 XP
```

Arco 1 conserva rango formal máximo **Novicio**. El XP y el ascenso formal son
sistemas separados.

XP base por dificultad de Alquimia:

```text
sencilla      2
normal        3
difícil       4
muy difícil   5
```

Decaimiento por elaboraciones válidas de esa receta:

```text
1ª       100%
2ª        75%
3ª–5ª     40%
6ª–10ª    15%
11ª+       0%
```

Hitos únicos por receta:

```text
primera válida      +2
primera Estable     +2
primera Superior    +3
primera Excepcional +4
```

## Techo de calidad por práctica

Asumiendo que el jugador ejecuta correctamente los tres pulsos:

| Dificultad | 1ª válida | 2ª | 3ª–5ª | 6ª+ |
|---|---|---|---|---|
| Sencilla | Superior | Excepcional | Excepcional | Excepcional |
| Normal | Estable | Superior | Excepcional | Excepcional |
| Difícil | Estable | Estable | Superior | Excepcional |
| Muy difícil | Impura | Estable | Superior | Excepcional |

Esto produce una buena curva para las formulaciones de Vitalidad:

```text
Básica LI       → Excepcional posible desde la 2ª válida
Templada LII    → desde la 3ª
Profunda LIII   → desde la 6ª
Condensada LIV  → desde la 6ª
```

Por eso las recetas de progresión no deben consumir materiales únicos.

## XP máximo útil por receta antes de agotarse la repetición

Incluyendo práctica de las diez primeras elaboraciones y los cuatro hitos:

```text
sencilla      18,40 XP
normal        22,10 XP
difícil       25,80 XP
muy difícil   29,50 XP
```

Las cuatro formulaciones de Vitalidad, dominadas por completo, pueden aportar
aproximadamente **95,8 XP** en total.

Esto es deseable: una sola familia profesional puede llevar al jugador a
Novicio, pero requiere progresar por el arco y dominar más de una receta. No
premia fabricar infinitamente la fórmula inicial.

## Catálogo legacy completo

Las ocho recetas actuales (1 sencilla, 4 normales, 2 difíciles, 1 muy difícil)
tienen un techo teórico conjunto de aproximadamente **187,9 XP**.

Por tanto es posible alcanzar numéricamente el umbral de Aprendiz dominando
gran parte del catálogo, aunque el rango formal de Arco 1 siga limitado a
Novicio.

### Recomendación

**No capar ni borrar ese XP excedente.**

Guardar el XP acumulado y mostrar que el rango formal está en el techo del Arco
1. Así el jugador no pierde progreso cuando el siguiente arco permita la
promoción.

## Decisión recomendada

Conservar sin cambios:

- `TRAMOS_APRENDIZAJE`;
- `XP_BASE_DIFICULTAD`;
- `HITOS_ALQUIMIA`;
- `TECHO_PRACTICA_ALQUIMIA`;
- fallos = 0 XP;
- XP por receta, no por objeto producido;
- calidad determinada por decisiones + techo de práctica, sin RNG.

Sólo debe revisarse el coste material de cada receta para que alcanzar su techo
de práctica sea económicamente razonable.
