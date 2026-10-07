# Human Decision — LII T1 Reactive Survival Semantics

Fecha: 2026-10-07
Estado: HUMAN_APPROVED_DESIGN_CHANGE / EXPERIMENTAL_BRANCH_ONLY

## Alcance

Esta decisión aplica únicamente a:
- `sapo_ceniza`
- `escarabajo_hierro`

en su T1 de LianQi II.

No modifica:
- los T1 cerrados de LianQi I;
- T2–T4;
- main;
- runtime productivo.

## Problema detectado

La semántica usada en V01/V02 hacía que activar T1 consumiera el turno del monstruo.

Resultado:
- Sapo T0 HRS ~73.28% player-win;
- Sapo T1 90%/CD3 ~72.97%;
- Escarabajo T0 HRS ~69.65%;
- Escarabajo T1 +12/CD3 ~70.35%.

La defensa ganada quedaba neutralizada por la pérdida de una acción ofensiva.

## Nueva semántica T1 LII

### Regla general

Cuando se cumple:
- HP <=30% del máximo, o
- el golpe recién recibido >=20% del HP máximo,

y:
- cooldown <=0;
- no hay una supervivencia T1 activa;

el monstruo activa su defensa T1 **como reacción**.

La activación:
- NO reemplaza el turno del monstruo;
- NO cancela su técnica ordinaria;
- NO agrega daño;
- NO crea una familia mecánica nueva.

Después de reaccionar, el monstruo ejecuta normalmente su turno.

### Sapo — MITIGATE_NEXT

La reacción prepara:
`MITIGATE_NEXT`

- reduce el siguiente paquete DIRECTO del jugador que conecte;
- reducción antes de DEF plana;
- si el jugador falla, la mitigación permanece;
- no mitiga DoT;
- se consume al conectar.

### Escarabajo — DEFENSE_UP

La reacción prepara:
`DEFENSE_UP`

- añade DEF contra la siguiente acción ofensiva del jugador;
- usa el pipeline normal de penetración y DEF;
- se consume después de esa acción, conecte o falle.

## Cooldown

Se mantiene el lifecycle existente del laboratorio:
- la activación fija `monster_survival_cd`;
- `end_round()` lo decrementa;
- no se introduce un reloj nuevo.

## Consecuencia

Los resultados numéricos V02 quedan como evidencia de que la semántica de acción-coste no diferenciaba T0/T1.

No se congela:
- Sapo 90%/CD3;
- Escarabajo +12/CD3.

Ambos deben recalibrarse bajo la nueva semántica reactiva.

## Hard guards

- T0 LII sigue congelado;
- no tocar LI;
- no T2–T4 hasta cerrar este T1;
- no T5;
- no nuevas técnicas;
- no nuevo timer/reloj;
- no main;
- no merge.
