# Monster Canonical Behavior Lab v0.1

Laboratorio aislado para conectar el bestiario real de ver74 con el kernel auditado `Monster Combat AI v0.1`.

## Frontera

```text
MOBS canónico
→ adaptador experimental
→ effectiveKit
→ chooseMonsterIntent()
→ intent solamente
```

La IA **no** ejecuta daño, veneno, quemadura, drenaje de qi, movimiento, aggro, loot ni muerte.

## Cadencia oficial preservada

El combate productivo despliega una técnica cuando:

```js
round % tecnica.cada === 0
```

y avisa la ronda anterior cuando:

```js
(round + 1) % tecnica.cada === 0
```

El modo `CADENCE_COMPAT` reproduce esto sin dar libertad a la IA para adelantar, retrasar o saltar la técnica:

- ronda sin técnica → effectiveKit contiene sólo ataque básico;
- ronda técnica → effectiveKit contiene sólo técnica canónica.

`DECISION_EXPERIMENTAL` existe sólo para laboratorio: en ronda técnica ofrece básico + técnica y permite comparar qué decidiría el kernel. No es comportamiento productivo.

## Perfiles experimentales iniciales

- rata_qi → INSTINTIVO / COLONIA
- serpiente_qi → REACTIVO_1 / SOLITARIO
- lobo_espiritual → CAZADOR_2 / MANADA
- devorador_niebla → TACTICO_3 / SOLITARIO
- mantis_nube → MASTER_4 / SOLITARIO

Estas asignaciones **no son canon**.

## Motores congelados

- engine blob: `f5b2cd5f6a1a4bff42f1fc74c04f09539adeb192`
- profiles blob: `7c5687ab1bdbd3870f768cf49e8c66f873713cbc`

## Canon

`canonical/MOBS_ver74.snapshot.json` contiene los 19 MOBS extraídos del blob exacto de ver74.

## Estado

`MONSTER_LAB_STATUS: REPRESENTATIVE_BASELINE_CONFIRMED`


## Baseline representativo confirmado

```text
all-mobs canon          13/13 PASS
representative baseline 18/18 PASS
TOTAL                    31/31 PASS
```

La cadencia productiva queda preservada para los 19 MOBS.

Los cinco representantes prueban el cableado de perfiles cognitivos, pero el adaptador canónico mantiene deliberadamente vacíos `signalWeights`, `memoryWeights` y `socialWeights`. Por tanto, la siguiente fase es definir asignaciones candidatas para las criaturas combatientes y una capa táctica experimental separada del canon.
