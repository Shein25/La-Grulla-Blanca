# Rata T1 × variabilidad individual — revisión Heavy

Fecha: 2026-10-01

## Integridad

Archivo:

`RESULTADOS_RATA_T1_VARIANCE_INTERACTION_V01.zip`

SHA-256:

`8165e7f98bc0cbc696dfbc9c8f86d92ade2465bf2c1d8998206dfddf0d88c5dc`

Contrato:

- experimento `RATA_T1_VARIANCE_INTERACTION_V01`;
- 10 contextos;
- 2.000 peleas naturales/contexto;
- 500 peleas Mutante condicionadas/contexto;
- baseline T0 variable: 25.000 peleas;
- 9 brazos T1: 225.000 peleas;
- total: 250.000 peleas;
- misma distribución/instancia individual entre T0 y T1;
- RNG de combate común;
- RNG de IA separado;
- Mutante se clasifica antes de T1;
- no canonical write;
- T2-T4 no ejecutados.

## Baseline T0 variable

### Normal natural

- peleas: 19.857;
- victoria jugador: 99,9698%;
- rondas: 3,26434;
- HP final jugador: 77,2420%;
- daño total Rata: 7,20630;
- hit rate jugador: 93,5685%;
- evasiones Rata: 0,20315/pelea;
- Qi gastado jugador: 19,59324.

### Mutante condicionado

- peleas: 5.000;
- victoria jugador: 99,6800%;
- rondas: 3,87920;
- HP final jugador: 65,5050%;
- daño total Rata: 10,91748;
- hit rate jugador: 88,0193%;
- evasiones Rata: 0,42620/pelea;
- Qi gastado jugador: 23,15460.

## Frecuencia de Reflejo

La magnitud EVA no decide si la IA elige Reflejo; el selector decide por señales.

Elecciones medias por pelea natural:

- EARLY: ~0,848;
- BASE: ~0,719;
- LATE: ~0,504.

Mutantes condicionados:

- EARLY: ~0,889;
- BASE: ~0,758;
- LATE: ~0,551.

Los Mutantes activan Reflejo algo más porque sobreviven lo suficiente para
alcanzar señales relevantes con mayor frecuencia.

## Comparación de magnitud — brazo BASE

### +25 EVA / CD5

Normal:

- +0,193 evasiones;
- +0,141 rondas;
- hit jugador 88,18%;
- daño Rata -1,829;
- presión HP **-5,764 pp**;
- Qi jugador ≈20,348.

Mutante:

- +0,217 evasiones;
- +0,089 rondas;
- hit jugador 82,97%;
- daño Rata -2,333;
- presión HP **-7,362 pp**;
- Qi jugador ≈23,390.

### +40 EVA / CD5 — candidato central

Normal:

- +0,306 evasiones;
- +0,268 rondas;
- hit jugador 85,31%;
- daño Rata -1,427;
- presión HP **-4,497 pp**;
- Qi jugador ≈21,075;
- +1,482 Qi gastado vs T0 variable.

Mutante:

- +0,345 evasiones;
- +0,254 rondas;
- hit jugador 80,28%;
- daño Rata -1,742;
- presión HP **-5,502 pp**;
- Qi jugador ≈24,257;
- +1,102 Qi gastado vs T0 variable.

### +50 EVA / CD5

Normal:

- +0,381 evasiones;
- +0,349 rondas;
- hit jugador 83,51%;
- daño Rata -1,167;
- presión HP **-3,677 pp**;
- Qi jugador ≈21,548.

Mutante:

- +0,430 evasiones;
- +0,361 rondas;
- hit jugador 78,57%;
- daño Rata -1,373;
- presión HP **-4,338 pp**;
- Qi jugador ≈24,807.

## Lectura

El resultado es monotónico en la identidad defensiva:

```text
+25 → menos evasión / menor extensión
+40 → centro
+50 → más evasión / mayor extensión
```

No aparece inestabilidad con la variabilidad individual ni con Mutantes.

Sin embargo, `EVADE_NEXT` consume una acción de la Rata. Por eso todos los
brazos T1 reducen el daño total recibido por el jugador respecto de T0.

T1 no debe describirse como "más letal".

Su efecto real es:

- la Rata tarda más en morir;
- el jugador falla más;
- el jugador gasta más Qi;
- aumenta ligeramente el uso forzado de básicos;
- la Rata sacrifica parte de su presión HP por supervivencia.

Esto es coherente con una adaptación de **supervivencia / desgaste**.

## EARLY / BASE / LATE

EARLY activa Reflejo más frecuentemente y amplifica todos los efectos.

LATE lo activa menos.

BASE queda entre ambos y mantiene comportamiento estable tanto en normales
como Mutantes.

No hay indicios de que la variabilidad individual requiera cambiar el selector.

## Robustez

- timeout 0 en todos los brazos;
- victoria del jugador permanece ~99,97% frente a normales;
- spreads de victoria por raíz/loadout son mínimos;
- la variabilidad no produce interacción explosiva con T1;
- Mutante + T1 sigue siendo una Rata excepcional, pero no un mini-jefe absoluto;
- T1 no modifica clasificación Mutante ni recompensas.

## Recomendación de cierre humano

Conservar como candidato:

```text
Reflejo de Madriguera
EVADE_NEXT
+40 EVA
CD 5
selector REACTIVO_1
brazo de señal BASE
```

Motivo:

- +25 es perceptible pero moderado;
- +50 añade más extensión/evasión sin mejorar proporcionalmente la identidad;
- +40 permanece en el codo central;
- sigue funcionando sobre individuos variables y Mutantes;
- no requiere cambiar el cerebro adaptativo.

Estado recomendado:

`T1_NUMERIC_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION`

No escribir CANON todavía.
No habilitar T2.
