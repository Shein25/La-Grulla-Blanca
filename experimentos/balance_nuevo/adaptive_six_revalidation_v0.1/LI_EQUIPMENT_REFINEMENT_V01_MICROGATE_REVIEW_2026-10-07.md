# LianQi I — Equipment Refinement V01 — Microgate Review

Fecha: 2026-10-07  
Fuente: `LI_EQUIPMENT_REFINEMENT_V01_MICROGATE_REVIEW.zip`  
ZIP SHA-256: `822aadbca0824279eac2cf28d4bab4e4eb47579e9d50d3ffc656d26a205664bc`  
LAB: `LI_EQUIPMENT_REFINEMENT_V01_MICROGATE`

## 1. Integridad

- ZIP válido, 22 archivos.
- 21 artefactos listados en `PACKAGE_MANIFEST.json`, todos con SHA-256 y bytes correctos.
- `issues=[]`.
- 1.345.920 combates representados:
  - item duel: 720.000
  - canonical: 192.000
  - niche: 414.720
  - negative sentinel: 19.200
- 2 workers.
- 14 piezas LI.
- 6.144 loadouts crudos.
- 4.224 firmas mecánicas finales candidatas.
- 5 técnicas BASE LI; 0 defensivas; 0 AOE.

### Provenance del hotfix

`SOURCE_LOCK.json` conserva el checkout base `c158d33bd12c7458a1eed5b389acf2268830738d`, porque la reanudación se hizo sobre el runtime existente.

El `LAB_RUNNER.py` empaquetado tiene SHA-256:

`e59a61fc3216b91561500a2dd5b56ced1e9684ae8eaf40a8ea3d2e82c909ce0a`

y contiene la corrección efectiva:

`("lanza_nubes","destello_plata")`

No contiene `lanza_parte_nubes`.

Por tanto los resultados corresponden al source checkout original más el hotfix de runner aplicado in-place. Las fases 1/2 y chunks anteriores de fase 3 permanecen semánticamente válidos; el chunk defectuoso no llegó a producir un checkpoint válido.

## 2. Resultado de gates

`DECISION_GATES.status = PASS`

Todos los hard gates pasan:

- Bandana final positiva vs NONE: PASS
- Bandana no estrictamente dominada/clonada por Cinta: PASS
- Colgante final mejor que CURRENT: PASS
- Colgante final no peor materialmente que V04B CONTROL+4: PASS
- Bastón final mejora CURRENT TEN+2: PASS
- Pulsera final mejora CURRENT QI+1/TEN+1: PASS
- EXPECTED→HIGH_ROLL visible/moderado: PASS
- BASE NONE cero leaks: PASS

## 3. Bandana de lino — EVA+1 / TEN+1

Contra NONE:

- OFF: +1,2125 pp WR, +0,659 pp HP final
- ON: +0,9500 pp WR, +0,715 pp HP final

Contra Cinta PREC+1/TEN+1:

- OFF: -0,517 pp WR
- ON: -0,638 pp WR

La Cinta es mejor en promedio, pero la Bandana no está estrictamente dominada:
- ON: Bandana mejor en 42,9% de los contextos según utilidad comparada; Cinta en 46,5%; 10,6% empate.
- En el microgate de nicho R=96, Bandana supera claramente a Cinta contra Rata de qi (~+0,57 pp WR y +0,68 pp HP final), mientras Cinta domina más a menudo frente a Avispa, Lobo, Mono y Serpiente.
- Bandana final mejora NONE en todas las especies del nicho en WR medio; su mayor ganancia aparece contra Mono.

Conclusión:
- PASS.
- Identidad útil: tocado defensivo/movilidad.
- Cinta conserva identidad de precisión.
- No subir más la Bandana.

## 4. Colgante de fragmento de jade — QI+1 / CONTROL+3

Contra CURRENT CONTROL+2:

- OFF: +0,608 pp
- ON: +0,629 pp

Contra V04B CONTROL+4:

- OFF: +0,454 pp
- ON: +0,513 pp

La mejora se concentra correctamente en Agua:
- vs CONTROL+4, ON Agua: ~+2,90 pp en item duel.
- en niche R=96, Agua:
  - Avispa ~+5,01 pp
  - Lobo ~+4,30 pp
  - Mono ~+0,52 pp
  - Rata ~+0,91 pp
  - Serpiente ~+2,28 pp

En raíces no-Agua el cambio frente a CONTROL+4 es casi neutro, como se esperaba.

Conclusión:
- PASS fuerte.
- QI+1/CONTROL+3 cumple mejor que CONTROL+4 porque mantiene nicho de control y añade utilidad real por economía de Qi.
- No requiere más ajuste.

## 5. Bastón de fresno — TEN+1 / PREC+1

Contra CURRENT TEN+2:

- OFF: +1,642 pp
- ON: +1,638 pp

El beneficio aparece en las cinco raíces.

Frente a Espada PREC+1, el resultado de combate es idéntico en LI porque Tenacidad no encuentra amenaza relevante en este PvE. Esto es aceptable:
- Espada = dotación inicial garantizada.
- Bastón = opción institucional posterior con la misma precisión y una reserva de Tenacidad útil fuera del microentorno actual.
- Cuchillo sigue siendo la opción agresiva: ~+3,53 pp ON vs Espada en el duel, pagando PREC -1 y con condición origin-only.

Conclusión:
- PASS.
- Bastón deja de ser pieza muerta sin desplazar al Cuchillo.
- No necesita más potencia en LI.

## 6. Pulsera — QI+1 / CONTROL+1

Contra CURRENT QI+1/TEN+1:

- OFF: +0,104 pp
- ON: +0,079 pp

La diferencia directa es pequeña porque el valor principal ya era QI+1; CONTROL+1 es especialización, no buff general.

En niche Agua R=96:
- mejora marginalmente a la versión vieja en casi todas las especies;
- no muestra dominancia;
- conserva el fuerte valor de QI de la pieza;
- CONTROL+1 aporta identidad de Agua/control sin inflarla.

Conclusión:
- PASS como especialista sutil.
- No subir más.

## 7. Curva de progresión final

Con Concordancias ON:

- NAKED: 41,433%
- MANDATORY_ENTRY: 65,608%
- EXPECTED_STAGE: 70,379%
- HIGH_ROLL_STRESS: 71,446%

Saltos:
- NAKED→ENTRY: +24,175 pp
- ENTRY→EXPECTED: +4,771 pp
- EXPECTED→HIGH_ROLL: +1,067 pp

El último salto era ~+0,74 pp en V04B; ahora entra en el objetivo blando de +1 a +3 pp sin convertir HIGH_ROLL en requisito.

## 8. Raíces con equipo final

EXPECTED_STAGE ON:
- Agua 65,69%
- Fuego 69,79%
- Metal 72,69%
- Tierra 72,00%
- Viento 71,73%
- spread ~7,00 pp

HIGH_ROLL_STRESS ON:
- Agua 69,65%
- Fuego 69,67%
- Metal 73,23%
- Tierra 72,67%
- Viento 72,02%
- spread ~3,58 pp

El HIGH_ROLL final beneficia especialmente a Agua y reduce el spread de raíces, que es coherente con Colgante/Pulsera orientados a Qi/control.

No hay señal para reabrir raíces.

## 9. Especies con equipo final

La jerarquía T0/T1 se conserva.

No aparece ningún nuevo cliff atribuible al pack final.

Con EXPECTED ON:
- Lobo T0/T1 ~57,71% / 48,63%
- Mono T0/T1 ~64,38% / 52,38%

Con HIGH_ROLL ON:
- Lobo ~55,04% / 51,33%
- Mono ~66,75% / 54,75%

Las diferencias pequeñas entre cohorts canónicos no deben leerse como marginal pareado, porque la fase canonical usa seeds por contexto de gear; los duels pareados son la autoridad para causalidad por pieza.

## 10. BASE NONE

600 filas de sentinel:
- AGUA_TO_METAL: 0 resoluciones
- AGUA_TO_VIENTO: 0
- METAL_TO_FUEGO: 0
- TIERRA_TO_VIENTO: 0

`negative_control_leak = 0.0`

PASS.

## 11. Decisión recomendada

El pack humano aprobado supera el microgate.

Recomendación:
- BASTÓN TEN+1/PREC+1: FREEZE CANDIDATE PASS
- BANDANA EVA+1/TEN+1: FREEZE CANDIDATE PASS
- PULSERA QI+1/CONTROL+1: FREEZE CANDIDATE PASS
- COLGANTE QI+1/CONTROL+3: FREEZE CANDIDATE PASS

No ejecutar más balance masivo de equipo LI.

Próximo orden:
1. freeze humano/productivo del equipo LI;
2. Concordance `NO_TRAP` con equipo final;
3. freeze/cierre total de LianQi I.
