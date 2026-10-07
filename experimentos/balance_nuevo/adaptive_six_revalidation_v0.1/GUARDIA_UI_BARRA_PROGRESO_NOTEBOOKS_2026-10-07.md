# Guardia UI — barra de progreso de notebooks

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: HUMAN_DECISION / ESTÁNDAR VISUAL DEL FRENTE

## Regla

Los próximos notebooks de simulación deben usar una barra de progreso compacta y legible, no la barra larga por defecto de tqdm.

## Estilo esperado

- ancho aproximado: media línea / barra visual de ~24-30 bloques;
- porcentaje visible;
- completado / total;
- tiempo transcurrido;
- ETA;
- velocidad;
- fase actual;
- chunk/checkpoint actual cuando corresponda.

## Estados visuales

- ejecución normal: color principal estable;
- lectura/recuperación de checkpoint: **amarillo**;
- fase terminada: verde;
- error/bloqueo técnico: rojo cuando la UI lo permita.

La transición a amarillo debe ser temporal mientras se procesa un checkpoint y volver luego al color normal.

## Formato orientativo

`3/4 Root passive recalibration  29% |███████················| 81,288/278,400  01:09<03:15  1.0k fight/s`

Al recuperar checkpoint:

`3/4 Root passive recalibration  42% |██████████·············| checkpoint 8/23`

## QA

Antes de entregar:
- comprobar que la barra realmente se renderiza en Colab;
- comprobar el cambio visual de checkpoint;
- comprobar que no ocupe todo el ancho de pantalla;
- comprobar ETA y contador;
- mantener checkpoints funcionales;
- no sacrificar rendimiento por la UI.

No main. No merge. No cambio de balance.


## Ajuste posterior — evitar widget tqdm.notebook deformado

Tras observar V04A.1 en Colab, queda prohibido considerar aceptable una barra que:
- se divida en varias líneas;
- muestre la barra gráfica separada del texto;
- genere mini-barras residuales;
- haga wrap de fase, contador o ETA;
- cambie de altura durante la ejecución.

Para los próximos notebooks:

- preferir una barra propia de una sola línea y ancho fijo;
- no depender de `tqdm.notebook` si su renderizado altera el layout;
- usar actualización in-place estable;
- mantener aproximadamente 24–30 bloques;
- mostrar en una única línea:
  `fase | porcentaje | barra | completado/total | elapsed<ETA | velocidad`;
- amarillo sólo durante lectura/escritura de checkpoint;
- azul/estado normal durante cálculo;
- verde al finalizar;
- rojo ante error;
- comprobar visualmente en Colab que no haya wrapping antes de entregar.

Ejemplo deseado:

`1/2 Fine concordances  42% |██████████··············| 225,792/537,600  03:41<05:06  1.02k fight/s`

El QA de entrega debe considerar FAIL una barra funcional pero visualmente rota o multilinea.


## Ajuste posterior — checkpoint sin saltos visuales

Observado en V04B: al entrar/salir del estado CHECKPOINT la barra puede hacer saltos visuales o dejar frames antiguos en Colab.

Para los próximos notebooks:

- usar **un único contenedor persistente** para toda la fase;
- no crear un nuevo `display_id` ni un nuevo bloque al cambiar de estado;
- mantener ancho y alto completamente fijos;
- el checkpoint NO debe cambiar la geometría ni el texto principal;
- usar un badge fijo de ancho reservado, por ejemplo `[RUN]`, `[CP]`, `[DONE]`;
- durante checkpoint cambiar sólo color/badge, no el layout;
- mantener el contador de progreso congelado mientras se escribe el checkpoint;
- después de escritura exitosa volver a RUN sobre el mismo contenedor;
- si se recupera un checkpoint, el salto numérico permitido debe corresponder únicamente a trabajo realmente ya completado;
- evitar redraws forzados que generen líneas fantasma;
- QA visual FAIL si la barra salta de posición, cambia de altura, duplica frames o mueve columnas al cambiar a checkpoint.

Formato deseado estable:

`1/6 Attribution [RUN]  62.9% |███████████████·········| 483,168/768,000  07:16<04:17  1.11k fight/s`

Durante checkpoint:

`1/6 Attribution [CP ]  62.9% |███████████████·········| 483,168/768,000  07:16<04:17  1.11k fight/s`

Sólo cambia el color y el badge; nada debe desplazarse.


## Estándar visual definitivo — barra elegante y estable

La barra de progreso de los próximos notebooks debe tratarse como componente de UI, no como salida de consola.

### Composición

Una sola fila persistente:

`FASE | BADGE | BARRA | % | COMPLETADO/TOTAL | ETA | VELOCIDAD`

Ejemplo:

`1/6 Attribution  [RUN]  ████████████············  62.9%  483,168/768,000  ETA 04:17  1.11k/s`

### Estética

- ancho total compacto y estable;
- barra central de aproximadamente 260–300 px;
- bordes redondeados;
- fondo oscuro/discreto compatible con tema claro y oscuro;
- tipografía monoespaciada para números y métricas;
- separación uniforme entre columnas;
- badge pequeño con ancho fijo;
- sin texto que cambie el ancho del layout;
- porcentaje con una decimal;
- números con separadores de miles;
- ETA legible;
- velocidad abreviada cuando corresponda.

### Estados

- RUN: azul suave;
- CP: amarillo/dorado;
- DONE: verde;
- ERR: rojo.

El cambio de estado debe modificar sólo:
- color de barra;
- color/badge de estado.

NO debe modificar:
- posición;
- alto;
- ancho;
- número de líneas;
- geometría del contenedor.

### Implementación preferida

Preferir:
- `ipywidgets.IntProgress`;
- `HBox`;
- `HTML/Label` con anchos fijos;
- un único widget mostrado una sola vez por fase.

Evitar:
- `tqdm.notebook` si produce wrapping;
- múltiples `display()`;
- reemplazo completo de HTML en cada tick;
- `display_id` que deje frames fantasma;
- outputs ANSI que creen líneas nuevas.

### QA visual obligatorio

Antes de entrega ejecutar una demo corta que atraviese:

`RUN -> CP -> RUN -> DONE`

y confirmar:
- sin duplicados;
- sin salto vertical;
- sin cambio de ancho;
- sin wrap;
- amarillo visible en CP;
- verde visible en DONE;
- progreso numérico correcto;
- checkpoint real sigue funcionando.

Si no pasa esta demo, `PRE_DELIVERY_QA` no puede ser PASS.
