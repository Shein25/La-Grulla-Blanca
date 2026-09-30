# ETAPA 17B — Reserva jugable de Qi LianQi I–IV

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: CERRADA COMO AJUSTE PROVISIONAL DE JUGABILIDAD

## Motivo

ETAPA16 demostró que Qi31 era la frontera matemática mínima que evitaba una
asimetría entre defensivas de coste7 y Agua de coste efectivo6.

Pero una frontera mínima de balance no tiene por qué ser una reserva cómoda de
juego.

Objetivo de este ajuste:
- dar margen frente a enemigos fuertes;
- reducir la presión de meditar tras combates exigentes;
- conservar gestión de recurso;
- no trivializar ramas de Eficiencia;
- conservar la paridad discreta entre raíces.

La cadencia real de meditación todavía no está definida, por lo que esta etapa
no afirma un número concreto de combates consecutivos sin meditar.

## Comparación de candidatos LianQi I

| Qi | ofensivas coste6 | defensiva7 + ofensivas6 | Agua def6 + ofensivas6 | AOE9 puras |
|---:|---:|---:|---:|---:|
| 31 | 5 | 1+4 | 1+4 | 3 |
| 37 | 6 | 1+5 | 1+5 | 4 |
| 43 | 7 | 1+6 | 1+6 | 4 |

### Qi31

Ventaja:
- equilibrio matemático muy limpio.

Problema:
- es el mínimo exacto;
- ofrece poco colchón para error, Control, defensivas y encuentros duros;
- cualquier combate largo empuja rápidamente a recuperación de Qi.

### Qi37

Ventajas:
- +1 técnica base completa respecto de Qi31;
- +20% de capacidad en la secuencia pura coste6: 5 -> 6 usos;
- +1 ofensiva después de abrir con defensiva;
- 3 -> 4 AOE puras;
- conserva exactamente la misma paridad entre defensiva7 y Agua6;
- deja a Eficiencia espacio para seguir cruzando umbrales adicionales.

### Qi43

Ventaja:
- margen aún mayor.

Problema:
- 7 ofensivas base desde LianQi I;
- +40% de capacidad respecto de Qi31;
- adelanta demasiado la economía prevista para LianQi II;
- reduce el valor relativo de gestión de Qi y ramas de Eficiencia.

## Decisión

La reserva de jugador pasa a:

| Etapa | Qi anterior | Qi nuevo |
|---|---:|---:|
| LianQi I | 31 | 37 |
| LianQi II | 37 | 43 |
| LianQi III | 43 | 49 |
| LianQi IV | 49 | 55 |

Se conserva:

- +6 Qi por avance;
- +2 puntos de técnica por avance;
- HP 30 -> 36 -> 42 -> 48;
- stats iniciales fijos;
- ausencia de regeneración pasiva universal.

## Presupuesto base resultante

Ofensivas coste6:

- Qi37 -> 6;
- Qi43 -> 7;
- Qi49 -> 8;
- Qi55 -> 9.

Defensiva7 + ofensivas6:

- Qi37 -> defensiva +5 ofensivas = 6 acciones;
- Qi43 -> defensiva +6 = 7;
- Qi49 -> defensiva +7 = 8;
- Qi55 -> defensiva +8 = 9.

Agua con defensiva efectiva6 conserva la misma cantidad total.

Una AOE9 + ofensivas6:

- Qi37 -> AOE +4 ofensivas = 5 acciones;
- Qi43 -> AOE +5 = 6;
- Qi49 -> AOE +6 = 7;
- Qi55 -> AOE +7 = 8.

Defensiva7 + AOE9 + ofensivas6:

- Qi37 -> 5 acciones;
- Qi43 -> 6;
- Qi49 -> 7;
- Qi55 -> 8.

## Relación con ETAPA16

ETAPA16 no se invalida matemáticamente.

Su conclusión se reinterpreta:

- Qi31 = mínimo matemático limpio;
- Qi37 = baseline jugable elegido.

Por tanto Qi31 deja de ser el Qi máximo del jugador, pero permanece como
referencia de frontera de costes.

## Impacto sobre benchmarks anteriores

Los benchmarks de defensivas realizados con Qi31 siguen siendo evidencia de
mecánica y balance relativo bajo esa reserva, pero ya no representan exactamente
el baseline jugable final de LianQi I.

Deben revalidarse específicamente las ramas de Eficiencia y cualquier resultado
que dependa de fallback por agotamiento de Qi.

No se reabren automáticamente:
- identidad;
- magnitudes defensivas;
- DEF_CAP2;
- AGUANTE_DUR_CAP1;
- pools;
- Placas;
- Evasión.

## Puntos de técnica

Sin cambios.

El usuario recibe:
- +2 en LianQi II;
- +2 en LianQi III;
- +2 en LianQi IV;
- total6.

Esto mantiene la construcción de build como decisión principal.

## Pendiente separado: recuperación/meditación

Subir Qi máximo reduce presión de recuperación, pero no define todavía:
- cuánto Qi recupera meditar;
- cuánto tarda;
- si existe recuperación parcial post-combate;
- si hay consumibles de Qi;
- si zonas seguras modifican recuperación.

Ese sistema debe diseñarse aparte y no ocultarse dentro del Qi máximo.

## Estado

PROVISIONAL:
- LianQi I Qi37;
- LianQi II Qi43;
- LianQi III Qi49;
- LianQi IV Qi55.

Runtime/HTML: SIN CAMBIOS.
