# LianQi I — Equipment Refinement V01 — Final Microgate Plan

Fecha: 2026-10-07  
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`  
Estado: HUMAN APPROVED CANDIDATE PACK / MICROGATE ONLY / NO PRODUCTIVE FREEZE

## 1. Objetivo

Validar el pack final de equipo LI aprobado por el usuario sin repetir la regresión masiva V04B.

El microgate debe responder:

1. ¿Bandana EVA+1/TEN+1 tiene valor real en LI y una identidad distinta de Cinta PREC+1/TEN+1?
2. ¿Colgante QI+1/CONTROL+3 mejora al candidato CONTROL+4 y al original CONTROL+2 sin volverse obligatorio?
3. ¿Bastón TEN+1/PREC+1 y Pulsera QI+1/CONTROL+1 conservan el valor observado en V04B dentro del pack final combinado?
4. ¿La curva MANDATORY_ENTRY → EXPECTED_STAGE → HIGH_ROLL_STRESS mejora de manera visible pero moderada?
5. ¿El pack final mantiene sanas las raíces y especies T0/T1 con Concordance OFF/ON?

## 2. Pack humano aprobado

- `baston_fresno_practica`: TEN +1 / PREC +1
- `bandana_lino_simple`: EVA +1 / TEN +1
- `pulsera_fibra_trenzada`: QI +1 / CONTROL +1
- `colgante_fragmento_jade`: QI +1 / CONTROL +3
- resto del equipo LI: sin cambios

La Bandana permanece en LianQi I.

## 3. Controles congelados

- monstruos T0/T1: sin cambios;
- 5 técnicas BASE LI: sin cambios;
- raíces: candidate pack V04B;
- Concordancias: relation-specific candidate pack V04B;
- T0/T1 = objetivo;
- T2/T3/T4 excluidos de este microgate.

## 4. Fases

### Fase 1 — Modified item duel

Comparaciones directas con Common Random Numbers.

Bandana:
- NONE
- CURRENT TEN+2
- FINAL EVA+1/TEN+1
- CINTA PREC+1/TEN+1

Colgante:
- NONE
- CURRENT CONTROL+2
- V04B CONTROL+4
- FINAL QI+1/CONTROL+3

Bastón:
- CURRENT TEN+2
- FINAL TEN+1/PREC+1
- ESPADA DE MADERA como referencia

Pulsera:
- NONE
- CURRENT QI+1/TEN+1
- FINAL QI+1/CONTROL+1

Cruce:
- 20 pares;
- 5 raíces;
- 5 monstruos;
- T0/T1;
- Concordance OFF/ON;
- R=24 por variante/contexto.

### Fase 2 — Canonical progression

Pack final completo.

Loadouts:
- NAKED
- MANDATORY_ENTRY
- EXPECTED_STAGE
- HIGH_ROLL_STRESS

Cruce:
- 20 pares;
- 5 raíces;
- 5 monstruos;
- T0/T1;
- OFF/ON;
- R=24.

### Fase 3 — Focused niche validation

Mayor R sólo en los nichos donde cambian las piezas:

- Bandana vs Cinta: evasión/precisión frente a las 5 especies.
- Colgante: Agua/Latigazo y raíces no-Agua para comprobar utilidad general limitada.
- Pulsera: Agua/Latigazo.
- Bastón: comparación contra espada/cuchillo en builds sin otras ayudas de precisión.

R=128 con semillas pareadas.

### Fase 4 — Regression sentinels

- 4 BASE NONE aislados: deben continuar en 0 resolución.
- checks de roots/species contra V04B:
  - no deriva global material;
  - no nuevo cliff por especie;
  - no pieza opcional con marginal general desproporcionado.

## 5. Gates

### Bandana
PASS si:
- marginal FINAL vs NONE > 0;
- FINAL no es estrictamente dominada por Cinta;
- Cinta tampoco queda estrictamente dominada por Bandana;
- ambas muestran contextos favorables distintos.

### Colgante
PASS si:
- FINAL > CURRENT de forma consistente;
- FINAL mejora o iguala razonablemente CONTROL+4 en utilidad total;
- mantiene nicho de Agua/control;
- marginal global moderado, no obligatorio.

### Bastón / Pulsera
PASS si:
- conservan marginal positivo;
- mantienen identidad de especialista/equilibrado;
- no dominan universalmente alternativas de slot.

### Curva de equipo
Objetivo blando:
- MANDATORY_ENTRY → EXPECTED_STAGE: mejora visible;
- EXPECTED_STAGE → HIGH_ROLL_STRESS: objetivo aproximado +1 a +3 pp ON;
- evitar saltos opcionales > ~7 pp global salvo pieza garantizada.

### Sistema
- root spread no debe reabrirse por el equipo;
- ninguna especie nueva debe convertirse en cliff;
- BASE NONE = 0 leaks.

## 6. Ejecución

- WORKERS=2.
- checkpoints reanudables.
- barra `ipywidgets.IntProgress + HBox` persistente, mostrada una sola vez por fase.
- estados:
  - RUN azul
  - CP amarillo
  - DONE verde
  - ERR rojo
- geometría fija; sin `display_id`, sin `tqdm.notebook`, sin redraw completo.
- QA demo obligatoria RUN→CP→RUN→DONE.
- no main, no merge, no cambios productivos.

## 7. Salida

`LI_EQUIPMENT_REFINEMENT_V01_MICROGATE_REVIEW.zip`

El microgate no auto-freezea. Tras revisión humana:
- si PASS: freeze de equipo LI;
- luego Concordance `NO_TRAP`;
- luego cierre final de LianQi I.
