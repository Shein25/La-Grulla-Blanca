# Resultado — T2 focal Rata + Serpiente V02

Fecha: 2026-10-06
Estado: VALID / CANDIDATO UNIVERSAL DERIVADO

## Integridad
- 147.200 combates.
- 2 workers.
- 4 réplicas por individuo/celda.
- CRN pareado.
- T1 congelado.
- Variabilidad + Mutantes + sufijos V1 activos.
- issues=[].
- sin ratificación automática.

## Rata

`T2_PRESERVE_DUE` es exactamente equivalente a `T2_ALWAYS`, como debía ocurrir porque la Rata no tiene técnica T0 canónica.

El brazo `T2_GATE_40_15_PRESERVE_DUE` modera la anticipación:
- NATURAL: ~0,356 anticipaciones/pelea;
- delta global de victoria jugador: aprox. -1,34 pp frente a T1;
- reduce la oscilación por policy respecto de ALWAYS;
- mantiene reconocimiento expresado.

## Serpiente

`T2_ALWAYS` confirma el problema causal: puede reemplazar turnos de técnica y reducir presión DOT.

`T2_PRESERVE_DUE` corrige esa interferencia:
- preserva los turnos de técnica due;
- NATURAL: 2,409 aplicaciones de veneno/pelea vs 2,325 en T1;
- NATURAL: delta win jugador ~-1,69 pp;
- mantiene ~0,662 anticipaciones/pelea.

`T2_GATE_40_15_PRESERVE_DUE` es aún más conservador:
- NATURAL: ~0,181 anticipaciones/pelea;
- NATURAL: 2,366 aplicaciones de veneno/pelea;
- delta win jugador ~-1,20 pp;
- elimina el outlier UNITARGET_FIRST del V01 sin reabrir T1.

## Derivación recomendada

Probar como candidato universal final:

`T2_R2_SHORT_THREAT_40_15_PRESERVE_DUE`

Semántica:
1. memoria 2;
2. 2 acciones EFECTIVAS consecutivas de la misma categoría;
3. reconocimiento sólo habilita anticipación si HP<=40% o golpe actual>=15% HPmax;
4. la anticipación no reemplaza una técnica canónica que está due por cadencia;
5. los triggers naturales T1 HP<=30% / golpe>=20% conservan prioridad;
6. magnitud, cargas y cooldown de T1 permanecen congelados.

Es una expansión mínima y legible de T1:
T1 reacciona a amenaza severa; T2 reconoce el patrón y puede reaccionar un poco antes.

No congelar hasta gate conjunto de las cinco especies.
