# Resultado — T4 Cooldown Focal V02

Fecha: 2026-10-06
Estado: **VALID / FINAL COOLDOWN CANDIDATES SELECTED**

Review ZIP SHA-256:
`a5c7ab92ea2318c50e9000dcfe4057e7e6e75eb916875ac94dcecdf03d72a721`

## Integridad

- 294.400 combates representados.
- 2 workers.
- 2 réplicas.
- stages:
  - LianQi I / LI_OVERREACH;
  - LianQi IV / LIV_STRUCTURAL.
- T0/T1/T2/T3 congelados.
- variabilidad + Mutantes/sufijos activos.
- manifest 8/8 correcto.
- `issues=[]`.
- 0 timeouts.
- 0 NaN/Inf.
- T3 false counter rate = 0.
- Acechante precision drift = 0.
- no T5.

## Cooldowns evaluados

Por especie:
- CD3
- CD5
- CD7
- baseline T3_FROZEN

Geometrías fijas:
- Rata: `R4A_HISTORIC_CANONICAL_HALF`
- Serpiente: `S4A_BASIC_POISON_ON_OPEN_HIT`
- Avispa: `A4A_BASIC_POISON_ON_OPEN_HIT`
- Mono: `M4B_MANOTAZO_REPLACE`
- Lobo: `L4A_EMBOSCADA_REPLACE`

## Selección para gate final

Se selecciona **CD7 para las cinco especies**.

Esto no es una regla universal impuesta de antemano; es la convergencia observada del focal V02.

### Motivo común

Con la cadena T0→T3 final, CD3 y CD5 permiten que la segunda respuesta madura reemplace BASIC con demasiada frecuencia, especialmente en encuentros LIV largos.

CD7:
- mantiene expresión T4 clara;
- conserva más BASIC;
- conserva la técnica canónica due;
- permite segunda aparición cuando el encuentro se extiende;
- no crea loops;
- no degrada T3;
- no depende de win-rate objetivo.

### Rata Qi
Finalista:
`R4A_HISTORIC_CANONICAL_HALF_CD7`

LIV NATURAL:
- ~1,365 usos/pelea;
- multi-use ~36,5%;
- T3 permanece estable.

La autoridad histórica usaba CD5, pero fue calibrada sobre T1/T2/T3 antiguos.
Bajo la cadena final, CD7 ya no es casi once-per-fight: mantiene recurrencia real y preserva mejor la identidad básica de Rata.

### Serpiente Qi
Finalista:
`S4A_BASIC_POISON_ON_OPEN_HIT_CD7`

LIV NATURAL:
- ~1,282 usos/pelea;
- multi-use ~28,4%;
- presión venenosa madura clara sin convertir casi todos los BASIC elegibles en extensión de veneno.

### Avispa Jade
Finalista:
`A4A_BASIC_POISON_ON_OPEN_HIT_CD7`

LIV NATURAL:
- ~1,423 usos/pelea;
- multi-use ~42,2%;
- conserva picadura/veneno y movilidad sin saturar la segunda respuesta.

### Mono Píldoras
Finalista:
`M4B_MANOTAZO_REPLACE_CD7`

LIV NATURAL:
- ~1,892 usos/pelea;
- multi-use ~84,2%;
- sigue siendo la especie con mayor recurrencia efectiva aun en CD7 debido a la duración de sus combates y a la convivencia con la cadencia canónica.
- CD3/CD5 aumentan demasiado la repetición de Manotazo sobre turnos BASIC.

### Lobo Espiritual
Finalista:
`L4A_EMBOSCADA_REPLACE_CD7`

LIV NATURAL:
- ~1,583 usos/pelea;
- multi-use ~58,0%;
- suficiente repetición para identidad apex;
- CD3/CD5 acercan demasiado el encuentro a una cadena recurrente de Emboscadas.

## Filosofía

La selección no busca igualar tasas de victoria.
T4 es reto autoinducido y puede ser muy severo.

El criterio es:
- identidad;
- legibilidad;
- preservación de BASIC;
- convivencia con técnica canónica;
- recurrencia madura sin spam estructural;
- ausencia de degeneraciones.

## Próximo paso

Gate final T4:
- geometría final por especie;
- CD7;
- T3_FROZEN vs T4 final;
- 4 réplicas;
- LI_OVERREACH + LIV_STRUCTURAL;
- todas las poblaciones, roots y policies;
- Acechante corregido;
- no T5;
- no ratificación automática.
