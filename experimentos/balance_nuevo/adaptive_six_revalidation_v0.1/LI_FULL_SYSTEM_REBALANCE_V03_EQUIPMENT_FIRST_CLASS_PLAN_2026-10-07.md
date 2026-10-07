# LianQi I — Full System Rebalance V03 · Equipment First-Class

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: PLAN LAB / SUPERSEDE V02 COMO GATE GLOBAL LI / NO FREEZE / NO RUNTIME

## 0. Propósito

V03 convierte el gate de LI en una auditoría del **sistema completo de etapa**.

No se limita a adaptar monstruos ni a calibrar Concordancias.

Evalúa simultáneamente:

- monstruos;
- 5 técnicas unitarget BASE disponibles en LI;
- Concordancias BASE;
- raíces;
- equipo LI;
- economía de Qi;
- interacciones entre esas capas.

V02 queda como referencia válida para el subproblema Concordancias, pero V03 es el gate global que debe usarse para cerrar LI.

## 1. Progresión LI

Sólo:
- Palma Ardiente;
- Destello de Plata;
- Latigazo de Marea;
- Golpe de Montaña;
- Lanza que Parte Nubes.

Sin:
- técnicas defensivas;
- AOE;
- Tramo I/II/III.

## 2. Equipo LI

Censo exhaustivo:
- 14 piezas;
- 6.144 loadouts legales;
- 4.864 firmas mecánicas.

Se mantienen:
- NAKED;
- MANDATORY_ENTRY;
- EXPECTED_STAGE;
- HIGH_ROLL_STRESS;
- extremos por eje;
- farthest-point signature coverage.

## 3. Auditoría determinista de equipo

Por pieza:
- slot;
- stats;
- power_budget;
- accessibility;
- availability;
- source_type;
- source_mission;
- coste en piedras/contribución;
- build_tags.

Análisis:
- duplicación de firma;
- dominancia Pareto intra-slot;
- piezas sin identidad estadística;
- slots sin alternativas reales;
- breakpoints discretos;
- concentración de poder por slot.

La dominancia estadística NO basta para declarar una pieza obsoleta si tiene acceso, coste o timing distinto.

## 4. Gate marginal por pieza

Cada una de las 14 piezas se prueba con Common Random Numbers mediante dos brazos:

### ITEM_OFF
background legal sin la pieza y sin otra pieza incompatible en su slot.

### ITEM_ON
mismo background + pieza evaluada.

Se mantienen idénticos:
- raíz;
- par de técnicas;
- monstruo;
- tier;
- Concordance OFF/ON;
- seed.

Esto permite medir el valor causal de cada pieza.

### Matriz

- 14 piezas;
- 20 pares dirigidos de técnicas;
- 5 raíces principales;
- 5 monstruos LI;
- T0/T1;
- Concordance OFF/ON;
- réplica Monte Carlo.

El gate puede usar R moderado y expandir automáticamente colas anómalas.

## 5. Métricas por pieza

- delta win-rate;
- delta HP final;
- delta Qi final;
- delta rondas;
- delta daño;
- delta mitigación;
- delta control;
- delta frecuencia de Concordancia;
- delta T1 survival activations;
- sensibilidad por raíz;
- sensibilidad por monstruo;
- sensibilidad por relation_id;
- consistencia del signo del beneficio;
- worst-tail / best-tail.

## 6. Diagnósticos de equipo

Etiquetas LAB posibles:

- USEFUL_SPECIALIST;
- USEFUL_GENERALIST;
- SITUATIONAL;
- LOW_IMPACT;
- DEAD_ITEM_CANDIDATE;
- DOMINATED_CANDIDATE;
- MANDATORY_RISK;
- OUTLIER_POWER;
- BREAKPOINT_DEPENDENT;
- ACCESS_JUSTIFIED.

Estas etiquetas no modifican catálogo automáticamente.

## 7. Guardias

No se permite compensar automáticamente una anomalía de equipo mediante:
- +HP monstruo;
- +daño monstruo;
- +DEF monstruo;
- nerf global de Concordancias.

Primero debe identificarse la capa causal.

## 8. Resultado de cierre

El REVIEW debe producir veredictos independientes:

- monsters_status;
- techniques_status;
- concordances_status;
- equipment_status;
- roots_status;
- system_status.

Un sistema sólo puede considerarse listo para freeze si no existe una capa bloqueante.

## 9. Tiers avanzados

T3/T4 posteriores deben incorporar jugadores avanzados:
- mejor equipo;
- LIII/LIV;
- Tramos superiores;
- stress LIV con Tramo III disponible;
- EXPECTED_STAGE y HIGH_ROLL_STRESS de la etapa correspondiente.

No deben calibrarse usando restricciones artificiales de LI.

No main. No merge. No runtime. No auto-freeze.
