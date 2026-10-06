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


## Paquete Colab preparado

Artefacto:
`COLAB_LI_MONSTER_T2_RATA_SERPIENTE_FOCAL_V02.zip`

- ZIP SHA-256: `8dddd320f8689da212c638fe8d95c4119f5aa4f61ff21e9fd34321c751dca5c3`
- Notebook SHA-256: `f7df1ee51ecc54bc09bf073dde75e6cc4651619fbe70d67221ab71a4b55dcdf1`
- Runner SHA-256: `74e7aa1c45258beff6c2a7afa98d1d3c3f3b53b5ff7feb36736316b39ce0ee5b`
- notebook: nbformat 4 válido;
- runner: py_compile PASS;
- rutas `/kaggle/`: 0;
- backend: Google Colab;
- workers: auto-detect CPU lógicas;
- checkpoint parcial y completo por especie;
- combates representados previstos: 147.200;
- CRN pareado entre brazos.
