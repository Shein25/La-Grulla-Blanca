# Calibración inicial — NPC Behavior Benchmark v0.1

## Propósito

Comprobar que el benchmark masivo produce señal útil antes de ampliar a más NPC o ejecutar millones de casos.

## Jiang Rui — Monte Carlo de calibración

Corrida independiente:

```text
N = 50.000 contextos
seed = 7
```

Variables muestreadas:

- peligro 0..100;
- urgencia 0..100;
- anomalía sí/no;
- superior alcanzable sí/no;
- fuera de puesto sí/no.

Umbrales categóricos experimentales para FSM/BT:

```text
highRisk = danger >= 60 OR missionUrgency >= 70
```

Resultado:

```text
FSM vs Behavior Tree      100.000 %
FSM vs Utility             61.698 %
BT  vs Utility             61.698 %
Acuerdo de los tres        61.698 %
Intents Utility inválidos       0
```

Distribución Utility:

```text
REPORT_SUPERIOR              28.606
PATROL_ROUTE                 12.863
RETURN_POST                   5.801
INVESTIGATE_ROUTE_ANOMALY     2.730
TOTAL                        50.000
```

## Interpretación

FSM y Behavior Tree coinciden al 100% en este barrido porque ambos usan la misma política categórica del laboratorio expresada con arquitecturas distintas.

Utility recibe las magnitudes completas y el perfil experimental de calibración. Su desacuerdo (~38,3%) no se considera error: representa la superficie donde una decisión ponderada difiere de la política categórica.

Este resultado justifica usar barridos más grandes para:

- localizar fronteras de decisión;
- medir sensibilidad a traits;
- comprobar si una política Utility resulta coherente con el personaje;
- evitar elegir arquitectura por intuición.

## Escalado

El benchmark admite:

```text
smoke      10.000 ejecuciones por NPC
standard  100.000
deep      500.000
million 1.000.000
custom   cualquier entero seguro >= 1
```

Las corridas de millones deben hacerse sólo cuando una pregunta concreta necesite más resolución.

## Estado

`BENCHMARK_CALIBRATION: SIGNAL_CONFIRMED`
