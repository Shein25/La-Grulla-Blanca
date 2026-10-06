# LI — T2 focal Rata + Serpiente V02

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Motivo

V01 validó mecánica general, pero Rata y sobre todo Serpiente muestran sensibilidad a policy.

No se toca:
- T0;
- T1 congelado;
- magnitud/cooldown/cargas T1;
- stats;
- veneno;
- cadencia;
- variabilidad / Mutantes / sufijos.

Sólo se calibra **cuándo una predicción T2 puede gastar un turno en la supervivencia T1**.

## Arquitectura de reconocimiento fija

- memory_window=2;
- repeat=2;
- sólo acciones EFECTIVAS;
- categorías observables;
- sin root/build ocultos;
- misma T1 de especie.

## Brazos

1. `T1_FROZEN`
2. `T2_ALWAYS`
   - comportamiento V01: reconocimiento por sí solo habilita supervivencia.
3. `T2_PRESERVE_DUE`
   - reconocimiento solo NO puede pisar una técnica canónica que ya está due por cadencia;
   - trigger T1 natural (HP<=30% o golpe>=20%) conserva prioridad.
4. `T2_GATE_50_10_PRESERVE_DUE`
   - reconocimiento + (HP<=50% o golpe actual>=10% HPmax);
   - no pisa técnica due salvo trigger T1 natural.
5. `T2_GATE_40_15_PRESERVE_DUE`
   - reconocimiento + (HP<=40% o golpe actual>=15% HPmax);
   - no pisa técnica due salvo trigger T1 natural.

Para Rata, PRESERVE_DUE debe ser idéntico a ALWAYS porque no tiene técnica T0; sirve como guardia de implementación.

## Matriz focal

- Rata Qi + Serpiente Qi.
- EXPECTED_STAGE + HIGH_ROLL_STRESS.
- 5 raíces.
- 4 policies.
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO.
- pools: 64/16/8/4 individuos.
- 4 réplicas de combate por individuo y celda.
- CRN pareado entre brazos.
- ~147.200 combates.

## Métricas causales

Además de V01:
- recognition_while_technique_due;
- recognition_blocked_by_due;
- recognition_blocked_by_threat_gate;
- técnica ejecutada / DOT aplicado;
- preemptive survival;
- deltas vs T1 por policy y población.

## Objetivo

Elegir la regla T2 más simple que:
- exprese reconocimiento;
- preserve identidad de especie;
- no reabra T1;
- evite que la anticipación automática sacrifique innecesariamente la ofensiva/cadencia;
- permanezca estable en Mutantes/Excepcionales/Ascendidos.

No hay target de win-rate.
No ratificación automática.
Colab only: /content o rutas relativas; 0 rutas Kaggle.
