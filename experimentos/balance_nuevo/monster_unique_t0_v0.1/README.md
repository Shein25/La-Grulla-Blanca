# Eco del Caído — T0 único cerrado

Eco del Caído es un encuentro `unique:true`. Su T0 queda congelado y no
participa en la progresión adaptativa persistente T1→T4.

## T0

- HP 51
- PREC 102
- EVA 24
- DEF 1
- TEN 24
- CONTROL 0
- crítico 5%
- daño crítico 1.5
- básico `1d3+6`
- sin técnica propia

Fuente: `eco_caido-b06-a11ec42a75`.

## Auditoría causal 1v1

El OUTLIER original no exigía cambiar los stats del monstruo.

En 81.000 combates dirigidos, `AOE_FIRST` cayó por el scalar AOE de objetivo
único 0.65. Al retirar sólo esa penalización en laboratorio, el spread por
policy descendió aproximadamente 21 pp. Igualar el coste de Qi no resolvió el
problema.

Por eso, en duelos estrictamente 1v1 con scalar AOE < 1:

- VETERAN, UNITARGET_FIRST y DEFENSE_OPEN son policies de gate;
- ROTATION y AOE_FIRST permanecen como stress diagnóstico;
- roots, loadouts, timeout e identidad siguen siendo gates;
- no se persigue una tasa de victoria objetivo.

## Guardas

- Eco no recibe T1–T4.
- No existe T5.
- No se cambia CANON sin reapertura humana explícita.
