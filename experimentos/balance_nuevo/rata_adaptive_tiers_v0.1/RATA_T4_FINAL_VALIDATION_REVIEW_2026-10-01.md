# Rata T4 — Mordisco Frenético — validación final

Fecha: 2026-10-01

## Candidato completo validado

```text
Mordisco Frenético

activation:
REPLACE_BASIC_WHEN_READY

opening:
INSTANCE_BASIC ×1.0

follow-up:
1 × (2d4 canónico ×0.50)

precision:
INDEPENDENT_PER_HIT

critical:
INDEPENDENT_PER_HIT

cooldown:
5

each packet:
normal direct-damage pipeline

effective tier required:
T4

decay below T4:
disables Mordisco Frenético
```

T1–T3 permanecen congelados.

No QI_DRAIN.
No DOT.
No Control.
No root/build inspection.
No precision bonus.
No crit bonus.
No T5.

## Evolución del diseño

### Phase A — canonical replacement

Reemplazar completamente el BASIC individual por packets canónicos fue
descartado: reducía la amenaza de individuos cuyo ataque ya era superior a
`2d4` y violaba la variabilidad ofensiva ratificada.

### Phase A2 — follow-up geometry

Se preservó:

```text
INSTANCE_BASIC
+
follow-up canónico
```

La geometría seleccionada provisionalmente fue:

```text
1 × (2d4 ×0.50)
```

porque era perceptible sin dominar el resto del kit.

### Phase B — precision / critical

Seleccionado:

```text
precision = independent per hit
critical  = independent per hit
```

No aparecieron razones empíricas para introducir una regla especial que
condicione el follow-up al hit de apertura o suprima sus críticos.

### Phase C — cooldown

Seleccionado:

`CD5`

CD3 resultó demasiado recurrente en peleas largas.
CD7 volvió T4 casi once-per-fight.
CD5 mantuvo una segunda aparición sólo cuando la pelea realmente se extendía.

## Validación final

- 5 player policies;
- 10 contextos/policy;
- 1.000 naturales/contexto;
- 250 Mutantes condicionados/contexto;
- T3 baseline + T4 candidato;
- 125.000 combates totales;
- no canonical write;
- no tier por encima de T4.

## VETERAN

Normal:

- 0,9764 usos/pelea;
- multi-use 2,16%;
- 4,36 daño/uso;
- p90 Mordisco = 7;
- packet hit rate 83,51%;
- crit/hit 4,71%;
- +0,69 daño monstruo/pelea;
- +2,20 pp presión HP;
- delta win jugador ≈ -0,07 pp.

Mutante:

- 1,048 usos/pelea;
- multi-use 7,28%;
- 5,21 daño/uso;
- p90 = 8;
- packet hit rate 90,55%;
- +0,83 daño/pelea;
- +2,65 pp presión HP;
- delta win ≈ -0,52 pp.

## UNITARGET_FIRST

Normal:

- 0,959 usos/pelea;
- multi-use 0,46%;
- 4,41 daño/uso;
- +0,67 daño/pelea;
- +2,13 pp presión HP;
- delta win ≈ -0,03 pp.

Mutante:

- 0,992 usos/pelea;
- multi-use 1,64%;
- 5,42 daño/uso;
- +0,76 daño/pelea;
- +2,39 pp presión HP;
- win rate sin cambio material.

## AOE_FIRST

Es la policy de stress más dura y ya era débil en 1v1 antes de T4.

Normal:

- 1,331 usos/pelea;
- multi-use 33,12%;
- 4,33 daño/uso;
- +0,71 daño/pelea;
- +2,24 pp presión HP;
- delta win ≈ -1,09 pp.

Mutante:

- 1,595 usos/pelea;
- multi-use 59,48%;
- 5,33 daño/uso;
- +1,12 daño/pelea;
- +3,52 pp presión HP;
- delta win ≈ -5,12 pp.

Este resultado es consistente con Phase C: encuentros largos permiten una
segunda activación real de CD5. No hay loop ni bypass.

## DEFENSE_OPEN

Normal:

- 1,028 usos/pelea;
- multi-use 2,81%;
- 1,13 daño/uso;
- p90 = 4;
- +0,50 daño/pelea;
- +1,62 pp presión HP.

Mutante:

- 1,080 usos/pelea;
- multi-use 7,96%;
- 1,77 daño/uso;
- p90 = 5;
- +0,75 daño/pelea;
- +2,45 pp presión HP.

La DEF plana amortigua fuertemente cada packet como exige el motor.

## ROTATION

Romper patrón sigue anulando casi todo T2/T3, pero T4 continúa porque es una
habilidad física instintiva adquirida por una población que ya alcanzó T4.

Normal:

- 1,175 usos/pelea;
- multi-use 17,52%;
- 1,54 daño/uso;
- +0,74 daño/pelea;
- +2,39 pp presión HP;
- delta win ≈ -0,20 pp.

Mutante:

- 1,362 usos/pelea;
- multi-use 36,12%;
- 2,50 daño/uso;
- +1,15 daño/pelea;
- +3,69 pp presión HP;
- delta win ≈ -0,92 pp.

Esto confirma que T4 no depende de seguir cayendo en el patrón T2/T3.

## Interacción con tiers previos

Durante la validación final:

- Reflejo permanece estable;
- T3 counter permanece prácticamente estable;
- Mordisco no desplaza elecciones de supervivencia de forma material;
- no aparece escalada recursiva entre T3 y T4;
- tier decay por debajo de T4 deshabilita Mordisco.

## Lectura final

El candidato cumple la identidad T4:

- físico;
- instintivo;
- claramente más expresivo que un BASIC;
- conserva la ofensiva individual;
- añade una ráfaga canónica reconocible;
- responde a EVA, DEF y absorción por packet;
- no necesita bonos ocultos;
- no convierte al monstruo en una técnica completamente distinta;
- mantiene diferencias naturales entre normales y Mutantes.

## Estado recomendado

`T4_READY_HUMAN_RATIFIED`

Candidato:

```text
Mordisco Frenético
REPLACE_BASIC_WHEN_READY

INSTANCE_BASIC ×1.0
+
2d4 canónico ×0.50

precision independent/hit
critical independent/hit
CD5
```

No existe T5 en este contrato.

Ratificación humana: 2026-10-01.

La cadena adaptativa de la Rata queda cerrada en T4. Reabrir T1–T4 o añadir un tier superior requiere una nueva decisión humana explícita.
