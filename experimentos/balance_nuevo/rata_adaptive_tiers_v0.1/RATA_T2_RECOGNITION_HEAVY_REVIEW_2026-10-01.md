# Rata T2 — revisión Heavy Recognition

Fecha: 2026-10-01

## Integridad

Archivo:

`RESULTADOS_RATA_T2_RECOGNITION_V01.zip`

SHA-256:

`a5f2b72059653cc58b78ee59f651b9bf24a8be86b5687f3aff475b2ccf7e1700`

Contrato:

- experimento `RATA_T2_RECOGNITION_V01`;
- 10 contextos;
- 2.000 peleas naturales/contexto;
- 500 peleas Mutante condicionadas/contexto;
- T1 congelado: +40 EVA / CD5 / REACTIVO_1 / BASE;
- baseline T1: 25.000 peleas;
- 3 candidatos T2: 75.000 peleas;
- total: 100.000 peleas;
- misma distribución de instancias;
- mismo namespace RNG de combate;
- RNG de IA separado;
- sólo categorías observables;
- no canonical write;
- no T3-T4.

## Baseline T1 congelado

Normal natural:

- victoria jugador: 99,96475%;
- rondas: 3,53671;
- HP final jugador: 81,5565%;
- Qi gastado: 21,10605;
- daño Rata: 5,83828;
- evasiones Rata: 0,51506.

Mutante condicionado:

- victoria jugador: 99,76%;
- rondas: 4,1226;
- HP final jugador: 71,1683%;
- Qi gastado: 24,1916;
- daño Rata: 9,12436;
- evasiones Rata: 0,7606.

## R2_SHORT

Contrato:

```text
memory_window = 2
repeticiones = 2
bonus reconocimiento = +8
```

Normal:

- recognition trigger rate: 33,63%;
- predicciones evaluadas: 17.274;
- precisión predictiva: 99,19%;
- falsos positivos: 0,81%;
- Reflejos: 0,78125/pelea;
- desplazamiento de Reflejo vs T1: +0,068/pelea;
- rondas: +0,02573;
- Qi gastado: +0,14387;
- evasiones: +0,02790;
- daño Rata: -0,15527;
- presión HP: -0,491 pp;
- victoria: sin cambio material.

Mutante:

- recognition trigger rate: 29,31%;
- precisión: 97,42%;
- falsos positivos: 2,58%;
- Reflejos: 0,8326/pelea;
- desplazamiento vs T1: +0,0774/pelea;
- rondas: +0,0284;
- Qi: +0,1696;
- evasiones: +0,0424.

## R2_CENTRAL

Contrato:

```text
memory_window = 3
repeticiones = 2
bonus reconocimiento = +12
```

Normal:

- recognition trigger rate: 49,23%;
- predicciones evaluadas: 25.379;
- precisión predictiva: 97,16%;
- falsos positivos: 2,84%;
- Reflejos: 0,82575/pelea;
- desplazamiento vs T1: +0,1125/pelea;
- rondas: +0,03520;
- Qi: +0,20344;
- evasiones: +0,04129;
- daño Rata: -0,28748;
- presión HP: -0,911 pp;
- victoria: sin cambio material.

Mutante:

- recognition trigger rate: 45,93%;
- precisión: 92,62%;
- falsos positivos: 7,38%;
- Reflejos: 0,8864/pelea;
- desplazamiento vs T1: +0,1312/pelea;
- rondas: +0,0422;
- Qi: +0,2544;
- evasiones: +0,0656.

## R3_CONSERVATIVE

Contrato:

```text
memory_window = 3
repeticiones = 3
bonus reconocimiento = +16
```

Normal:

- recognition trigger rate: 4,31%;
- precisión: 99,45%;
- falsos positivos: 0,55%;
- Reflejos: 0,7140/pelea;
- desplazamiento vs T1: +0,00075/pelea;
- cambios de combate prácticamente nulos.

Mutante:

- recognition trigger rate: 5,34%;
- precisión: 98,32%;
- falsos positivos: 1,68%;
- Reflejos: 0,7568/pelea;
- desplazamiento vs T1: +0,0016/pelea;
- efecto de combate prácticamente nulo.

## Lectura

El reconocimiento funciona mecánicamente y no produce una interacción
explosiva con la variabilidad individual ni con Mutantes.

La frontera es clara:

```text
R3_CONSERVATIVE → demasiado raro para expresar T2
R2_SHORT        → reconocimiento frecuente y muy preciso
R2_CENTRAL      → reconocimiento muy frecuente, mayor desplazamiento
```

R2_CENTRAL no rompe combate, pero reconoce patrón en casi la mitad de todas las
decisiones del monstruo bajo VETERAN. Esto es suficiente para exigir una
prueba de generalización antes de cierre.

## Hallazgo metodológico

La policy VETERAN privilegia técnicas unitarget mientras son pagables y sólo
cambia a defensa/AOE/básico bajo condiciones observables concretas.

Por eso una secuencia de categorías repetidas puede ser altamente predecible.
La precisión 97–99% obtenida aquí podría representar:

1. aprendizaje real de un patrón observable; o
2. sobreespecialización a una policy de jugador muy repetitiva.

Este Heavy no distingue ambas posibilidades.

## Decisión

No promover T2 todavía.

Estado:

`T2_RECOGNITION_MECHANIC_VALIDATED_POLICY_GENERALIZATION_PENDING`

Siguiente prueba obligatoria:

comparar el T1 congelado y R2_SHORT/R2_CENTRAL/R3_CONSERVATIVE sobre policies
de jugador distintas:

- VETERAN;
- UNITARGET_FIRST;
- AOE_FIRST;
- DEFENSE_OPEN;
- ROTATION.

Métricas principales:

- trigger rate;
- prediction accuracy;
- false-positive rate;
- desplazamiento de Reflejo;
- rondas/Qi;
- normal vs Mutante.

T3–T4 permanecen bloqueados.
