# LAB — PHASE C · Screen de las cinco defensivas base LianQi I

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO CANON**

## Objetivo

Comparar las cinco defensivas base bajo una economía mixta más limpia.

Candidato LAB usado:

- Qi máximo jugador = 31;
- HP base = 30;
- DEF base = 1;
- EVA base = 5;
- enemigo = HP28 / PREC90 / EVA20 / DEF2 / ataque 2d4+1;
- jugador actúa primero;
- defensiva usada como apertura;
- después se usa ofensiva mientras alcanza Qi y luego ataque básico;
- Agua usa Arrastre PROVISIONAL al 50% contra Tenacidad20;
- Tierra usa Peso PROVISIONAL STACK_REFRESH.

Runner:

`experimentos/balance_nuevo/phase_c_all_defensives_lab.py`

## Valores defensivos actuales

- Fuego · Cuerpo-Horno: coste7, 15% HP de Absorción, 2 turnos.
- Metal · Armadura de Plata: coste7, 3 Placas, +3 DEF por impacto, duración4.
- Agua · Espejo de Luna: coste7, 12% HP de Absorción, Reflujo25%, duración3.
- Tierra · Piel de Cobre: coste7, Arraigo/DEF progresiva, duración3.
- Viento · Paso de Nube Ligera: coste7, +15 EVA, duración2.

## Resultado

Confirmación de 120.000 duelos por raíz/estrategia:

| Raíz | Estrategia | Win rate | Turnos | HP restante | Usa básico |
|---|---|---:|---:|---:|---:|
| Fuego | sólo ofensiva | 95.76% | 4.25 | 52.25% | 13.58% |
| Fuego | Cuerpo-Horno | 94.12% | 5.32 | 50.74% | 35.15% |
| Metal | sólo ofensiva | 90.71% | 5.05 | 40.00% | 28.16% |
| Metal | Armadura de Plata | 92.79% | 6.32 | 49.70% | 64.93% |
| Agua | sólo ofensiva + Arrastre | 86.75% | 6.21 | 42.71% | 63.82% |
| Agua | Espejo 12% | 81.33% | 7.32 | 36.14% | 90.39% |
| Tierra | sólo ofensiva + Peso | 91.75% | 5.23 | 43.10% | 33.33% |
| Tierra | Piel de Cobre | 96.28% | 6.60 | 60.87% | 67.12% |
| Viento | sólo ofensiva | 87.98% | 5.68 | 38.94% | 47.71% |
| Viento | Paso +15 EVA / 2t | 77.81% | 6.74 | 29.73% | 80.38% |

## Clasificación LAB

### Armadura de Plata — PASS inicial

La defensiva de Metal aumenta win rate y HP restante y cumple una identidad
clara. No necesita buff inmediato.

### Piel de Cobre — PASS fuerte

Piel aumenta significativamente supervivencia y victoria.

Con Qi31 desaparece el problema artificial de Qi30:

- Piel7;
- quedan24;
- caben cuatro Golpes de Montaña.

Piel pasa a verse fuerte, por lo que no debe recibir buffs adicionales antes
de pruebas contra perfiles enemigos más duros.

### Cuerpo-Horno 15% — FAIL marginal

Cuerpo-Horno 15% reduce ligeramente win rate y también deja menos HP restante.

Barrido adicional:

- 20% todavía queda alrededor del umbral;
- aproximadamente 25% HP de Absorción empieza a justificar con claridad la apertura;
- 30%+ entra en una zona fuerte.

Zona LAB siguiente: **22–25% HP de Absorción**.

### Espejo de Luna 12% — FAIL claro

El 12% vuelve a fallar incluso con Qi31.

La reserva se rompe demasiado rápido y Reflujo rara vez consigue expresar su
identidad.

El test específico previo encontró **22–25% HP** como zona prometedora.

No subir daño de Agua para compensarlo; corregir la defensiva por su propia función.

### Paso de Nube Ligera +15 EVA / 2 turnos — FAIL claro

Es el resultado más débil del grupo.

Aunque reduce el hit rate enemigo durante dos turnos, perder una acción
ofensiva produce:

- win rate ~78% frente a ~88% sin Paso;
- menor HP restante;
- mayor dependencia del ataque básico.

Barridos de sensibilidad:

- +30 EVA durante2 turnos sigue siendo insuficiente;
- +30 EVA durante4 turnos se aproxima a la ofensiva pura (~87.5%);
- el problema no se resuelve con un pequeño +5 EVA.

Esto indica que hay que revisar **duración, magnitud o función base** de Paso,
no simplemente subirlo de +15 a +20.

## Hallazgo de arquitectura

Las cinco defensivas no necesitan compartir magnitud ni producir el mismo win rate.

Pero sí deberían cumplir un criterio mínimo:

> gastar un turno defensivo debe crear una mejora defensiva observable que
> justifique su coste en algún contexto normal de LianQi I.

Con el enemigo ordinario LAB actual:

- Metal: sí.
- Tierra: sí, con fuerza.
- Fuego: marginal/no.
- Agua: no.
- Viento: no.

## Siguiente trabajo

No cerrar todavía PHASE C.

Prioridad:

1. calibrar Cuerpo-Horno en banda 22–25% Absorción;
2. calibrar Espejo en banda 22–25% Absorción manteniendo Reflujo25%;
3. rediseñar/testear Paso de Nube Ligera con cambios estructurales moderados;
4. reejecutar las cinco defensivas juntas;
5. comprobar perfiles enemigo común / resistente / preciso antes de promover.



---

## Stress check — ¿las defensivas débiles sólo eran situacionales?

Se repitió la comparación actual contra cuatro presiones LAB:

- COMMON: PREC90 / 2d4+1;
- PRECISE: PREC100 / 2d4+1;
- HEAVY: PREC90 / 1d6+3;
- DANGEROUS: PREC100 / 1d6+3.

Se mide delta de win rate de apertura defensiva frente a sólo ofensiva.

| Perfil | Fuego | Metal | Agua | Tierra | Viento |
|---|---:|---:|---:|---:|---:|
| COMMON | −1.7 pp | +2.2 pp | −5.7 pp | +4.5 pp | −10.0 pp |
| PRECISE | −2.4 pp | +2.2 pp | −8.1 pp | +6.3 pp | −14.0 pp |
| HEAVY | −2.8 pp | +2.2 pp | −7.7 pp | +5.5 pp | −12.2 pp |
| DANGEROUS | −4.3 pp | +1.9 pp | −10.7 pp | +8.0 pp | −16.8 pp |

Lectura:

- Armadura de Plata conserva valor positivo bajo presión.
- Piel de Cobre escala muy bien con presión y requiere vigilancia por posible
  sobrepotencia en escenarios de muchos impactos.
- Cuerpo-Horno 15% no se rescata al aumentar daño/Precisión.
- Espejo 12% empeora aún más cuando aumenta la presión.
- Paso +15 EVA / 2 turnos tampoco se rescata contra enemigos más peligrosos.

Por tanto, Fuego/Agua/Viento necesitan recalibración real; no basta con
etiquetarlos como defensivas situacionales contra enemigos duros.

### Nota de grupos

Se hizo además un stress exploratorio con varias acciones enemigas por ronda.
No se toma como balance de grupo real porque los atacantes extra no eran
objetivos eliminables, pero sí mostró una advertencia:

- Piel escala muy rápido cuando recibe muchos impactos;
- Placas se consumen mucho más deprisa;
- Paso actual sigue sin compensar el turno en esa simulación artificial.

Antes de balancear grupos habrá que usar combates multiobjetivo reales, no
multiplicar ataques sobre un único HP enemigo.
