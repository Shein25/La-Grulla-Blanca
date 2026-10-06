# Resultado — LI T3 species-counter micro-screen V01

Fecha: 2026-10-06
Estado: **VALID / FINALISTS_SELECTED_FOR_DUAL_STAGE_FOCAL**

Review ZIP:
`LI_MONSTER_T3_SPECIES_COUNTER_MICROSCREEN_V01_REVIEW.zip`

## Integridad

- 103.040 combates.
- 2 workers.
- 2 réplicas por individuo/celda.
- manifest 7/7 correcto.
- T0/T1/T2 congelados.
- Mutantes/sufijos V1 activos.
- 0 timeouts.
- 0 NaN/Inf.
- false counter rate = 0.
- degenerate loops = 0.
- `issues=[]`.
- sin ratificación automática.

## Hallazgos

### Rata
`R1_INSTANCE_BASIC` se expresa con claridad:
- NATURAL ~0,397 counters/pelea;
- counter medio ~4,22 HP;
- delta win jugador ~-5,39 pp agregado NATURAL.
El nuevo T1/T2 permite multi-counter real (máximo observado 2), a diferencia del estudio histórico. Requiere focal con variante ONCE_PER_FIGHT.

### Serpiente
- S1 tick inmediato: claro, medible y coherente; NATURAL ~0,169 counters/pelea.
- S2 aplicación completa: funciona, pero su daño diferido no queda atribuido por la telemetría de packet del V01 y añade una duración completa adicional.
Finalista recomendado: **S1_INSTANCE_POISON_TICK**.

### Avispa
- A1 básico funciona.
- A2 tick de veneno conserva mejor identidad de especie y produce presión compacta sin nueva duración.
Finalista recomendado: **A2_INSTANCE_POISON_TICK**.

### Mono
- M1 QI_DRAIN_ONLY vuelve a mostrar saturación del recurso; efecto adicional pequeño.
- M2 Manotazo + drain añade una respuesta visible y usa únicamente el packet ya materializado de la instancia.
Finalista recomendado: **M2_INSTANCE_MANOTAZO_PACKET**.

### Lobo
L1 básico y L2 daño de Emboscada son ambos estables.
L2 es más fuerte; no hay evidencia suficiente para elegir sin focal.
Mantener ambos.

## Punto metodológico

V01 se ejecutó en LianQi I para validar causalidad mecánica.

T3 está orientado a presión avanzada / LianQi IV, aunque la política de sobreextensión permite alcanzarlo antes. El siguiente focal debe separar:

- `LI_OVERREACH_STRESS`: jugador LianQi I que forzó T3;
- `LIV_INTENDED`: jugador LianQi IV en la banda donde T3/T4 están previstos.

No usar el win-rate LI como objetivo de nerf.

## Finalistas V02

- Rata: R1 INSTANCE_BASIC unrestricted vs ONCE_PER_FIGHT.
- Serpiente: S1 INSTANCE_POISON_TICK.
- Avispa: A2 INSTANCE_POISON_TICK.
- Mono: M2 INSTANCE_MANOTAZO_PACKET.
- Lobo: L1 INSTANCE_BASIC vs L2 INSTANCE_EMBOSCADA_DAMAGE.

T2 baseline pareado para todas las especies.
