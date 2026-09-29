# LAB — PHASE B · Economía mixta de Qi LianQi I

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO CANON**

## Motivo

Los primeros tests defensivos mostraron que Qi30 funciona bien para cinco
ofensivas de coste6, pero castiga artificialmente una secuencia con defensiva7.

Todas las defensivas base actuales de Fuego, Metal, Agua, Tierra y Viento
parten de coste7. Agua reduce ese coste a 6 por su rasgo CANON de −10%.

Runner:

`experimentos/balance_nuevo/phase_b_mixed_qi_lab.py`

## Barrido 28–36 Qi

| Qi | sólo ofensivas6 | defensiva6 + ofensivas6 | defensiva7 + ofensivas6 |
|---:|---|---|---|
| 28 | 4 acciones · sobra4 | 1+3 · sobra4 | 1+3 · sobra3 |
| 29 | 4 · sobra5 | 1+3 · sobra5 | 1+3 · sobra4 |
| 30 | 5 · sobra0 | 1+4 · sobra0 | **1+3 · sobra5** |
| 31 | 5 · sobra1 | 1+4 · sobra1 | **1+4 · sobra0** |
| 32 | 5 · sobra2 | 1+4 · sobra2 | 1+4 · sobra1 |
| 33 | 5 · sobra3 | 1+4 · sobra3 | 1+4 · sobra2 |
| 34 | 5 · sobra4 | 1+4 · sobra4 | 1+4 · sobra3 |
| 35 | 5 · sobra5 | 1+4 · sobra5 | 1+4 · sobra4 |
| 36 | 6 · sobra0 | 1+5 · sobra0 | **1+4 · sobra5** |

## Hallazgo

Qi30 y Qi36 son **acantilados** para las defensivas de coste7.

En Qi30:

- ofensiva pura: 5 técnicas;
- defensiva7 + ofensiva6: sólo 4 técnicas totales;
- además quedan 5 Qi inutilizables.

Qi31 es el primer punto que elimina ese castigo:

- ofensiva pura: 5 ofensivas;
- defensiva Agua efectiva6: 1 defensiva +4 ofensivas;
- defensiva normal7: 1 defensiva +4 ofensivas.

Así una defensiva reemplaza exactamente **una** acción ofensiva en el
presupuesto de técnicas, en vez de reemplazar una acción y además perder otra
por aritmética.

## Candidato estructural

`Qi máximo LianQi I = 31` emerge como candidato LAB muy limpio para economía
mixta.

No se promueve todavía a PROVISIONAL.

La razón no es estética; es esta relación:

`7 + 4×6 = 31`

Mientras:

`5×6 = 30`

Por tanto Qi31 permite comparar de manera justa:

- cinco ofensivas;
- una defensiva7 + cuatro ofensivas;
- una defensiva6 de Agua + cuatro ofensivas.

## Guardia

No reducir automáticamente todas las defensivas de 7 a 6 para encajar Qi30.

El coste7 es compartido por las cinco defensivas base y puede ser una decisión
intencional de presupuesto.

Primero debe probarse Qi31 contra las cinco defensivas.

