# Rata T3 — revisión de triggers y generalización

Fecha: 2026-10-01

## Alcance

Fase inicial de T3: aislar **cuándo** existe un contraataque válido antes de
calibrar **cuánto** daño debe hacer.

T1 y T2 permanecieron congelados:

```text
T1 Reflejo de Madriguera
+40 EVA / CD5 / REACTIVO_1 / BASE

T2 R2_SHORT
memory 2 / repeat 2 / EFECTIVA / +8
```

El daño T3 de referencia fue el básico canónico `2d4`.

Un miss sólo se considera causado por Reflejo cuando, usando exactamente el
mismo roll de hit:

```text
EVA natural del individuo → el ataque habría conectado
EVA natural + Reflejo +40 → el ataque falla
```

Por tanto un fallo natural no puede armar T3.

## Estudio VETERAN — 24.000 combates

Los tres triggers resultaron indistinguibles:

- ~0,288 contraataques/pelea normal;
- ~0,77 daño T3/pelea normal;
- 0 loops;
- máximo 1 counter/pelea;
- predicción confirmada en prácticamente todos los misses causales.

Conclusión: VETERAN no puede separar las reglas.

## Generalización — 50.000 combates

Policies:

- VETERAN;
- UNITARGET_FIRST;
- AOE_FIRST;
- DEFENSE_OPEN;
- ROTATION.

### RECOGNIZED_REFLEJO_MISS

Es demasiado permisivo.

En AOE_FIRST:

```text
normal:
counter       0,299/pelea
false counter 46,46%

Mutante:
counter       0,252/pelea
false counter 59,52%
```

La Rata contraataca aunque la categoría realmente ejecutada ya no coincida con
la predicción aprendida.

Esto rompe el contrajuego establecido en T2.

**Descartado.**

### CONFIRMED_PATTERN_REFLEJO_MISS

Exige:

1. patrón T2 reconocido;
2. Reflejo activo;
3. la acción real coincide con la categoría predicha;
4. el roll habría acertado contra EVA natural;
5. el +40 EVA de Reflejo convierte ese mismo roll en miss.

Resultados normales aproximados:

| Policy | counters/pelea | false counter |
|---|---:|---:|
| VETERAN | 0,279 | 0% |
| UNITARGET_FIRST | 0,280 | 0% |
| AOE_FIRST | 0,160 | 0% |
| DEFENSE_OPEN | 0,290 | 0% |
| ROTATION | 0,001 | 0% |

Esto conserva exactamente el contrajuego deseado: ROTATION casi apaga T3 y el
cambio de patrón en AOE_FIRST reduce el counter en vez de castigarlo de todos
modos.

### CONFIRMED_PATTERN_ONCE_PER_FIGHT

Produjo los mismos resultados que el trigger confirmado sin límite.

En toda la generalización:

- multi-counter fight rate = 0;
- máximo observado = 1 counter/pelea;
- loops degenerados = 0.

La restricción `ONCE_PER_FIGHT` es redundante con la duración actual del
combate y el CD5 de Reflejo. Añadirla ahora sería una regla extra sin efecto
observable.

## Candidato provisional de trigger T3

`CONFIRMED_PATTERN_REFLEJO_MISS`

No está ratificado como T3 completo todavía.

La siguiente fase separa el segundo eje:

**daño del counter**.

Se probarán únicamente referencias ofensivas ya medidas para Rata, manteniendo
este trigger fijo y sin abrir T4.
