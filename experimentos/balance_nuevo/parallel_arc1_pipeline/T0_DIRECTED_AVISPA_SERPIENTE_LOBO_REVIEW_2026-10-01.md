# Avispa / Serpiente / Lobo — revisión T0 dirigida

Fecha: 2026-10-01

## Integridad

Archivo analizado:

`RESULTADOS_T0_DIRIGIDOS_AVISPA_SERPIENTE_LOBO(1).zip`

SHA-256:

`858bc4ef969c76863813e2c6bb227c19c8fdfe2bc21dc95a285980ce7a2b06d5`

Contrato de corrida:

- 3 especies;
- 5 candidatos por especie;
- 10000 peleas/contexto;
- 10 contextos;
- 100000 peleas/candidato;
- common random numbers;
- 0 timeouts;
- no selección automática;
- no escritura CANON;
- no T1–T4;
- sin Definitivas;
- sin filas de combate persistidas.

## Avispa de Jade

Identidad buscada:

`NORMAL / movilidad-evasión + picadura + veneno; no tanque`

### Candidato recomendado — trial 872

```text
HP              17
DEF              0
EVA             22
PREC            90
TEN              7
CTRL             0
crit             5%
crit damage      x1.50
basic            1d2+1

Picadura de Esmeralda
poison           1d3+2
ticks             2
cadence           2
```

100000 peleas:

- victoria jugador: 99.985%;
- presión HP media: 9.594%;
- HP final p10: 73.607%;
- rondas medias: 2.833;
- daño monstruo medio: 3.034;
- DOT medio: 2.527;
- fracción DOT: **83.304%**;
- usos de técnica: 0.570/pelea;
- evasiones monstruo: 0.526/pelea;
- spread HP entre raíces: 4.019 pp;
- spread HP entre loadouts: 0.229 pp.

La Avispa 872 expresa de forma limpia sus dos rasgos: **movilidad y veneno**.

Contrastes:

- 1119: demasiado pequeña; presión 1.63%, técnica 0.015/pelea.
- 1468: presión similar a 872 (10.44%) pero sólo 1.85% del daño proviene de DOT;
  funciona como atacante básico rápido, no como Avispa venenosa.
- 1251/1417: cruzan a una criatura excesivamente dominante y demasiado resistente
  para el rol NORMAL; 1417 gana por DOT extremo + EVA55/DEF2 y 1251 combina daño,
  supervivencia y veneno de forma demasiado amplia.

Estado recomendado:

`T0_NUMERIC_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION = trial 872`

## Serpiente de Qi

Identidad buscada:

`NORMAL / presión sostenida por veneno; prolongar el combate debe ser peligroso`

### Candidato recomendado — trial 1484

```text
HP              27
DEF              0
EVA              5
PREC            86
TEN              5
CTRL             0
crit             5%
crit damage      x1.50
basic            1d2+2

Colmillos Venenosos
poison           1d2+2
ticks             3
cadence           2
```

100000 peleas:

- victoria jugador: 100%;
- presión HP media: 17.196%;
- HP final p10: 67.742%;
- rondas medias: 3.497;
- daño monstruo medio: 5.437;
- DOT medio: 3.868;
- fracción DOT: **71.139%**;
- usos de técnica: 0.955/pelea;
- spread HP entre raíces: 6.352 pp;
- spread HP entre loadouts: 0.324 pp.

La técnica aparece aproximadamente una vez por pelea y el veneno explica la
mayoría del daño sin convertir a la Serpiente en un tanque.

Contraste principal — trial 1013:

- presión HP: 47.975%;
- victoria jugador: 95.14%;
- DOT: 86.34% del daño;
- spread HP entre raíces: **31.305 pp**.

1013 expresa veneno, pero la respuesta depende demasiado de la raíz y pasa de
NORMAL sostenido a una amenaza mucho más polarizada.

1453/1412 son directamente extremos de alta mortalidad/resistencia.

Estado recomendado:

`T0_NUMERIC_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION = trial 1484`

## Lobo Espiritual

Identidad buscada:

`APEX_BRIDGE / depredador directo; enfrentarlo puede ser una mala decisión aunque aparezca`

### Candidato recomendado — trial 1425

```text
HP              41
DEF              1
EVA             12
PREC            97
TEN             20
CTRL             0
crit             5%
crit damage      x1.50
basic            2d4+2

Emboscada de las Tres Colas
direct damage    2d6+1
cadence           5
```

100000 peleas:

- victoria jugador: 90.226%;
- presión HP media: 65.498%;
- HP final p10: 0.968%;
- rondas medias: 7.006;
- daño monstruo medio: 20.705;
- daño p90: 31;
- usos de técnica: 0.857/pelea;
- spread HP entre raíces: 15.042 pp;
- spread HP entre loadouts: 1.592 pp.

Por raíz:

- Agua: 88.70% victoria;
- Fuego: 94.73%;
- Metal: 89.23%;
- Tierra: 96.315%;
- Viento: 82.155%.

El spread de raíz es material, pero no proviene de dependencia de equipo
(el spread entre loadouts es pequeño). Para un APEX_BRIDGE esto documenta
diferencias reales entre herramientas ofensivas/defensivas de las raíces,
no una fragilidad del candidato ante gear.

Contrastes:

- 1429: 99.472% victoria y 36.96% presión; funciona como depredador fuerte,
  pero no delimita bien la transición APEX_BRIDGE.
- 1194: 37.63% victoria; cruza demasiado hacia una amenaza casi ELITE/BOSS.
- 629/1463: prácticamente letales (≈0.4% o menos de victoria jugador);
  quedan como extremos de frontera, no candidatos T0.
- 1425 ocupa la zona intermedia claramente distinguible.

Estado recomendado:

`T0_NUMERIC_CANDIDATE_SELECTED_AWAITING_HUMAN_RATIFICATION = trial 1425`

## Decisión del bloque

No se justifica otra búsqueda local para estas tres especies.

Candidatos de ratificación:

```text
avispa_jade       trial 872
serpiente_qi      trial 1484
lobo_espiritual   trial 1425
```

Todavía no se modifica `stats_status` ni se habilita T1.

El Mono sigue su refinación local separada.

## Valor para extrapolación

Estas tres selecciones, junto con Rata T0 READY, permiten congelar cuatro
anclas metodológicas LianQi I:

- Rata: BASIC / NORMAL inferior;
- Avispa: EVA + DOT corto;
- Serpiente: DOT sostenido;
- Lobo: DIRECT_DAMAGE / APEX_BRIDGE.

Mono cerrará la quinta ancla: QI_DRAIN / SKIRMISHER.

Estas anclas sirven para reducir espacios de búsqueda posteriores, nunca para
copiar números finales ni multiplicar stats por etapa.
