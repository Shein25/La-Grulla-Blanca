# LianQi I — System Recalibration V04A · Microgates

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: PLAN LAB / REOPENED FOR SYSTEM RECALIBRATION / NO FREEZE / NO RUNTIME

## 0. Estado de LI

LianQi I se reabre únicamente para recalibración sistémica.

Se preservan como control:
- monstruos LI T0/T1 congelados;
- cinco técnicas unitarget BASE;
- reglas de progresión LI;
- contrato conceptual de Concordancias.

Se reabren para ajuste:
- magnitudes de Concordancias;
- pasivos numéricos de raíces;
- equipo LI selectivo.

## 1. Evidencia V03

V03 Full System Rebalance:
- 1.068.160 combates representados;
- 0 issues técnicos;
- 0 leakage en BASE NONE;
- 10% universal de Concordancia fue estable como screen global pero no como freeze;
- efecto medio ON-OFF ~+3 pp;
- respuesta muy desigual entre hooks;
- ranking de equipo prácticamente estable ON/OFF;
- Bandana de lino y Bastón de fresno: impacto PvE LI exactamente 0 en el gate marginal;
- Uniforme gris: fuerte pero STARTING_ISSUE/GUARANTEED; no se nerfea automáticamente;
- spread de raíces ya existía con Concordance OFF, con Fuego por encima de Agua/Metal.

## 2. V04A-A — Concordancias dirigidas aisladas

Las 16 relaciones BASE válidas se calibran una por una.

Durante el test de una relación:
- sólo esa relation_id puede resolver;
- la dirección inversa queda desactivada aunque el Eco exista;
- BASE NONE sigue sin fallback;
- Common Random Numbers OFF vs ON.

### Grids LAB por hook

DIRECT_DAMAGE:
`[0.025, 0.05, 0.075, 0.10, 0.125, 0.15]`

CONTROL_POWER:
`[0.05, 0.10, 0.15, 0.20, 0.25, 0.30]`

PERCENT_PENETRATION:
`[0.25, 0.50, 0.75, 1.00, 1.25, 1.50]`

PRECISION:
`[0.25, 0.50, 0.75, 1.00, 1.50, 2.00]`

CRIT_CHANCE:
`[0.25, 0.50, 0.75, 1.00, 1.50, 2.00]`

EVASION_DEBUFF:
`[0.10, 0.20, 0.30, 0.40, 0.50, 0.75]`

CONTAINED_TRIGGER:
- stored scale `[0.10, 0.15, 0.20, 0.25, 0.30, 0.40]`;
- duration `[1,2,3]` source turns;
- structural descriptor unchanged.

No se exige igual win delta a todas las relaciones. Se busca:
- efecto visible;
- ausencia de dominancia universal;
- identidad del hook preservada;
- estabilidad por raíz/equipo/monstruo;
- colas sin cliffs artificiales.

## 3. V04A-B — Raíces

La V03 permite aislar pasivos porque cruzó las mismas técnicas/equipo/monstruos con las cinco raíces.

Se prueba Concordance OFF primero.

No se crean estadísticas nuevas: sólo se barren magnitudes de los pasivos existentes.

Fuego — direct_damage_pct / crit_chance_pp:
- current 10 / 5
- candidatos: 4/2, 5/2, 6/3, 7/3, 8/4, 10/5.

Metal — percent_penetration_pp / precision:
- current 10 / 5
- candidatos: 10/5, 15/5, 20/5, 15/7, 20/7, 25/8.

Agua — qi_cost_mult / control:
- current 0.90 / 5
- candidatos: 0.90/5, 0.85/5, 0.85/7, 0.80/7, 0.80/10, 0.75/10.

Tierra — hp_max_mult / tenacity:
- current 1.10 / 5
- candidatos: 1.10/5, 1.15/5, 1.20/5, 1.15/10, 1.20/10.

Viento — evasion / crit_damage_add:
- current 10 / 0.05
- candidatos: 10/0.05, 12/0.05, 15/0.05, 12/0.10, 15/0.10, 18/0.10.

No auto-selección ni freeze.

## 4. V04A-C — Equipo selectivo

No se rediseña el catálogo entero.

### Bastón de fresno
CURRENT:
- TEN +2

candidatos LAB:
- TEN +2 (control);
- TEN +1 / PREC +1;
- TEN +1 / HP +1;
- PREC +2.

### Bandana de lino
CURRENT:
- TEN +2

candidatos LAB:
- TEN +2 (control);
- TEN +1 / HP +1;
- TEN +1 / EVA +1.

Además se reporta opción no numérica:
- MOVE_TO_LII_CANDIDATE.

### Pulsera de fibra
CURRENT:
- QI +1 / TEN +1

candidatos:
- current;
- QI +2;
- QI +1 / CONTROL +1.

### Colgante de jade
CURRENT:
- CONTROL +2

candidatos:
- CONTROL +2;
- CONTROL +3;
- CONTROL +4.

El Anillo oxidado no se retunea por este gate porque tiene utilidad extracomabte pendiente de contrato.

El Uniforme gris no se retunea automáticamente porque es dotación inicial garantizada.

## 5. Contextos

Concordancias:
- 16 relations;
- 5 roots;
- 8 gear contexts;
- 5 monsters;
- T0/T1;
- R moderado;
- expansión de colas.

Raíces:
- Concordance OFF;
- 20 ordered technique pairs;
- canonical gear contexts;
- 5 monsters;
- T0/T1.

Equipo:
- ITEM_OFF vs ITEM_ON;
- current vs candidate variant;
- Concordance OFF y un pequeño ON regression;
- mismos seeds/contextos.

T2:
- sólo tail stress posterior de candidatos; no calibra magnitudes.

T3/T4:
- excluidos de V04A.

## 6. Objetivo

V04A devuelve fronteras y recomendaciones, NO valores canónicos.

Salida:
`LI_SYSTEM_RECALIBRATION_V04A_MICROGATES_REVIEW.zip`

Luego decisión humana y V04B full regression.

No main. No merge. No runtime. No auto-freeze.
