# Progressive Monster Stage Anchoring V01

Fecha: 2026-10-06  
Estado: HUMAN-DIRECTED METHODOLOGY / ACTIVE

## Regla de progresión

Los monstruos repetibles de una nueva etapa no se calibran de forma aislada.

La referencia inferior de una etapa nueva es el monstruo T0 repetible más fuerte ya congelado de la etapa anterior.

```text
strongest frozen T0 of stage N
→ benchmark at player stage N+1
→ candidate T0 monsters of stage N+1
→ role-preserving recalibration
→ freeze T0 stage N+1
→ only then validate T1→T4
```

No se exige dominancia stat-by-stat.
Se exige progresión de **amenaza de encuentro** preservando identidad.

## Ancla LianQi I → LianQi II

Ancla: **Lobo Espiritual T0 final**.

Fuente:
`experimentos/balance_nuevo/t0_li/T0_LI_FREEZE_MANIFEST_2026-10-06.json`

Lobo final:
- HP 53
- PREC 100
- EVA 12
- DEF 1
- basic `2d4+2`
- Emboscada `2d6+1`
- cadence 4

El Lobo fue el cierre más exigente de LI y tiene rol de puente/apex.

### Candidatos LII actuales

Sapo Ceniza:
- HP 49
- PREC 97
- EVA 11
- DEF 0
- basic `1d2+5`
- Nube de Hollín cadence 3:
  - direct `1d2+4`
  - burn `1d2+2 ×3`

Escarabajo de Hierro:
- HP 75
- PREC 90
- EVA 14
- DEF 2
- basic `1d2+3`
- Carga de Caparazón cadence 3:
  - direct `1d2+8`

## Lectura previa

Sapo no supera al Lobo en durabilidad ni basic. Su posible superioridad proviene de presión sostenida por quemadura.

Escarabajo supera ampliamente al Lobo en durabilidad, pero sacrifica precisión y daño basic; su superioridad debe surgir de tanqueo + Carga.

No se aceptará la progresión sólo porque un stat aislado sea mayor.

## Benchmark correcto

Todos deben ser enfrentados contra **el mismo jugador LianQi II** y los mismos contextos:

- Lobo T0 final, como referencia;
- Sapo T0 candidato;
- Escarabajo T0 candidato.

Comparar:
- win-rate diagnóstico;
- rounds;
- HP final del jugador;
- daño directo;
- DOT;
- Qi pressure;
- técnica/pelea;
- basic/pelea;
- root/policy/loadout spread;
- NATURAL;
- high-roll no-mutant;
- Mutante por separado, sin usarlo como floor de etapa.

### Regla de interpretación

El nuevo monstruo no necesita superar al Lobo en cada eje.

Debe existir una razón de identidad clara por la que el encuentro LII sea al menos una progresión real respecto del techo LI.

Ejemplos:
- Sapo: presión sostenida / burn.
- Escarabajo: durabilidad / castigo por combate largo.

Si un candidato LII resulta globalmente más débil que Lobo contra el mismo jugador LII, se recalibra T0 antes de abrir adaptación.

## Secuencia futura

1. Cerrar T0 LII usando Lobo como ancla.
2. Cerrar T1→T4 de Sapo/Escarabajo.
3. Elegir el monstruo T0 más fuerte de LII como ancla de LIII.
4. Recalibrar Pez/Anguila T0.
5. Cerrar T1→T4 LIII.
6. Elegir el monstruo T0 más fuerte de LIII como ancla de LIV.
7. Recalibrar Devorador/Halcón T0.
8. Cerrar T1→T4 LIV.

No saltar etapas.

## Guardias

- No usar T4 del stage anterior como stat floor del siguiente stage.
- El ancla de progresión es T0 congelado; adaptación se valida después.
- No universal stat scaling.
- No obligación de +X% fijo.
- No target universal de win-rate.
- Preservar identidad.
- No unique.
- No main.
- No merge.


## Regla de continuidad de equipo entre etapas

Decisión humana:

> El equipo mínimo efectivo de una etapa nueva es el equipo máximo alcanzable de la etapa anterior.

Por lo tanto, para benchmarks de progresión no se usa `MANDATORY_ENTRY` del catálogo como piso si éste es inferior al techo real previo.

Cadena metodológica:

```text
MAX_GEAR(LI)   → FLOOR_GEAR(LII)
MAX_GEAR(LII)  → FLOOR_GEAR(LIII)
MAX_GEAR(LIII) → FLOOR_GEAR(LIV)
```

### Catálogo actual

El catálogo de simulación contiene perfiles:
- `MANDATORY_ENTRY`
- `EXPECTED_STAGE`
- `HIGH_ROLL_STRESS`

Estos perfiles siguen siendo útiles para simulación, pero **no definen por sí mismos la continuidad progresiva entre etapas**.

Para este frente:

- `HIGH_ROLL_STRESS(LI)` se usa como **carry-over floor de LII**;
- `HIGH_ROLL_STRESS(LII)` se usa como **carry-over floor de LIII**;
- `HIGH_ROLL_STRESS(LIII)` se usa como **carry-over floor de LIV**.

No se modifica todavía el catálogo productivo; la regla se aplica en los runners de laboratorio.

### Benchmark de etapa

Cada nueva etapa se evalúa al menos en tres contextos de equipo:

1. **CARRY_OVER_FLOOR** — máximo de la etapa anterior;
2. **EXPECTED_STAGE** — equipo esperado de la etapa actual;
3. **HIGH_ROLL_STRESS** — techo/stress de la etapa actual.

Esto permite separar:

- si el monstruo nuevo realmente supera el techo de amenaza anterior;
- cómo se comporta con equipamiento normal de su propia etapa;
- si se mantiene mecánicamente sano frente al techo de equipo de su etapa.

La comparación del monstruo ancla anterior y los monstruos nuevos debe usar exactamente el mismo loadout dentro de cada contexto.
