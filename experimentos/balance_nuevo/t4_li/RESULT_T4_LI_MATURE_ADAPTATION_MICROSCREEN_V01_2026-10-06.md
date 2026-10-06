# Resultado — T4 Mature Adaptation Micro-screen V01

Fecha: 2026-10-06
Estado: **VALID / FINALIST GEOMETRIES SELECTED**

Review ZIP SHA-256:
`b07a8c1ff33b48623b689dc1e7b580cad88fcfe3905d2edd9ee41b3132993d2c`

## Integridad

- 220.800 combates representados.
- 2 workers.
- 2 réplicas.
- LianQi I / LI_OVERREACH.
- LianQi IV / LIV_STRUCTURAL.
- T0/T1/T2/T3 congelados.
- Variabilidad y sufijos activos.
- manifest íntegro.
- `issues=[]`.
- 0 timeouts.
- 0 NaN/Inf.
- T3 false counter rate = 0.
- precisión residual Acechante = 0.
- no T5.

## Selección de geometrías para V02

### Rata Qi
Seleccionado:
`R4A_HISTORIC_CANONICAL_HALF`

Mordisco Frenético:
- opening `INSTANCE_BASIC ×1.0`;
- follow-up `2d4 canónico ×0.50`;
- rolls independientes.

Motivo:
- preserva la autoridad histórica ratificada;
- evita que el follow-up vuelva a escalar con el basic individual y doble-capture variabilidad;
- R4B fue sistemáticamente más agresiva en LI sin aportar identidad nueva;
- ambas fueron mecánicamente estables.

### Serpiente Qi
Seleccionado:
`S4A_BASIC_POISON_ON_OPEN_HIT`

- BASIC de instancia;
- si impacta, un tick inmediato del veneno de la instancia;
- no añade duración.

Motivo:
- el veneno queda causalmente ligado al contacto;
- S4A/S4B fueron casi indistinguibles en presión;
- se prefiere la versión más simple y legible.

### Avispa Jade
Seleccionado:
`A4A_BASIC_POISON_ON_OPEN_HIT`

- BASIC de instancia;
- si impacta, un tick inmediato del veneno de la instancia.

Motivo:
- evita introducir un segundo “contacto” sin daño directo que no existe como autoridad canónica;
- presión y estabilidad fueron equivalentes a A4B;
- conserva movilidad + picadura/veneno sin inventar packet extra.

### Mono Píldoras
Seleccionado:
`M4B_MANOTAZO_REPLACE`

- reemplaza BASIC disponible por packet de Manotazo;
- si impacta, drena 6 Qi;
- no desplaza la técnica debida por cadencia.

Motivo:
- expresa de forma visible la adaptación madura sobre el Dantian;
- M4A añade drenaje al basic pero resulta menos reconocible;
- M4B mostró mayor presión estructural LIV sin inestabilidad.

### Lobo Espiritual
Seleccionado:
`L4A_EMBOSCADA_REPLACE`

- reemplaza BASIC disponible por daño de Emboscada de instancia;
- no desplaza la Emboscada canónica debida por cadencia.

Motivo:
- usa el packet canónico completo, sin scalar arbitrario;
- encaja con identidad apex;
- L4B añade una geometría híbrida BASIC + media Emboscada que no aporta suficiente ventaja conceptual.

## Lectura NATURAL destacada

LIV:
- Rata R4A: win jugador 100%; T4 ~1,67 usos/pelea; +0,16 daño directo/pelea vs T3.
- Serpiente S4A: win jugador ~61,64% vs ~69,28% T3; ~1,60 usos/pelea; +3,09 DOT/pelea.
- Avispa A4A: ~84,71% vs ~88,55% T3; ~1,63 usos/pelea; +3,59 DOT/pelea.
- Mono M4B: ~98,93% vs ~99,79% T3; ~2,40 usos/pelea; +5,14 Qi drenado/pelea y +1,55 daño directo.
- Lobo L4A: ~99,82% vs ~99,92% T3; ~2,19 usos/pelea; +1,49 daño directo/pelea.

No existe target universal de win-rate.

## Acechante C20

V01 ejecutó la semántica contractual correcta:
- +20 PREC únicamente al siguiente ataque;
- luego se retira;
- `max_abs_precision_drift = 0`.

El baseline T3 corregido permanece mecánicamente limpio.
No se reabre el contrato T3; el bug correspondía al harness anterior, no a su diseño.

## Próximo paso

V02 debe mantener una única geometría por especie y comparar:
`CD3 / CD5 / CD7`

contra `T3_FROZEN`, en LI_OVERREACH + LIV_STRUCTURAL.

No freeze automático.
