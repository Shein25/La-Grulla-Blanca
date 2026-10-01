# Rata T4 — Mordisco Frenético — Phase C cooldown review

Fecha: 2026-10-01

## Mecánicas congeladas

```text
activation:
REPLACE_BASIC_WHEN_READY

opening:
INSTANCE_BASIC ×1.0

follow-up:
1 × (2d4 canónico ×0.50)

precision:
INDEPENDENT_PER_HIT

critical:
INDEPENDENT_PER_HIT
```

Sólo varió cooldown:

- CD3;
- CD5;
- CD7.

Cinco policies: VETERAN, UNITARGET_FIRST, AOE_FIRST, DEFENSE_OPEN y ROTATION.

## Lectura general

En peleas cortas VETERAN/UNITARGET, CD5 y CD7 son parecidos porque normalmente
Mordisco sólo llega a estar disponible una vez.

La diferencia aparece cuando la pelea se prolonga.

### VETERAN

Normal:

```text
CD3: 1,149 usos/pelea | multi-use 19,06%
CD5: 0,974 usos/pelea | multi-use  2,17%
CD7: 0,954 usos/pelea | multi-use  0,25%
```

Mutante:

```text
CD3: 1,392 usos/pelea | multi-use 39,2%
CD5: 1,066 usos/pelea | multi-use  8,8%
CD7: 0,994 usos/pelea | multi-use  1,6%
```

CD3 empieza a convertir T4 en una acción recurrente. CD7 hace que casi siempre
sea una aparición única.

### UNITARGET_FIRST

Normal:

```text
CD3: 1,047 usos
CD5: 0,958
CD7: 0,952
```

Mutante:

```text
CD3: 1,236
CD5: 1,006
CD7: 0,982
```

La separación es moderada.

### AOE_FIRST

Es el mejor stress test de frecuencia porque las peleas duran más.

Normal:

```text
CD3: 1,976 usos | multi-use 90,60% | max 4
CD5: 1,339 usos | multi-use 33,92% | max 2
CD7: 1,023 usos | multi-use  2,33% | max 2
```

Mutante:

```text
CD3: 2,138 usos | multi-use 95,2% | max 4
CD5: 1,578 usos | multi-use 57,6% | max 3
CD7: 1,070 usos | multi-use  7,0% | max 2
```

CD3 domina demasiado la secuencia ofensiva.
CD7 prácticamente elimina la posibilidad de una segunda ráfaga incluso en
peleas largas.
CD5 permite una segunda aparición sólo cuando el encuentro realmente se
extiende.

### DEFENSE_OPEN

Normal:

```text
CD3: 1,419 usos | multi-use 41,15%
CD5: 1,024 usos | multi-use  2,38%
CD7: 1,003 usos | multi-use  0,30%
```

La DEF plana sigue amortiguando fuertemente los packets. No existe bypass.

### ROTATION

Normal:

```text
CD3: 1,825 usos | multi-use 77,76%
CD5: 1,172 usos | multi-use 17,14%
CD7: 1,018 usos | multi-use  1,77%
```

Mutante:

```text
CD3: 2,012 usos | multi-use 87,8%
CD5: 1,342 usos | multi-use 34,2%
CD7: 1,066 usos | multi-use  6,6%
```

Romper patrones sigue apagando T2/T3, pero T4 es instintivo y puede reaparecer
por cooldown. CD5 mantiene esa identidad sin llegar al spam de CD3.

## Selección provisional Phase C

`CD5`.

Motivo:

- CD3 es demasiado recurrente en encuentros largos;
- CD7 vuelve T4 casi estrictamente once-per-fight sin que exista esa regla;
- CD5 responde naturalmente a duración del combate;
- no necesita límites artificiales;
- mantiene visible T4 sin convertirlo en BASIC mejorado permanente.

## Candidato T4 completo para validación final

```text
Mordisco Frenético

activation:
REPLACE_BASIC_WHEN_READY

opening:
INSTANCE_BASIC ×1.0

follow-up:
1 × (2d4 canónico ×0.50)

precision:
INDEPENDENT_PER_HIT

critical:
INDEPENDENT_PER_HIT

cooldown:
5

each packet:
normal direct-damage pipeline

skip_next_action:
respected
```

No QI_DRAIN.
No DOT.
No Control.
No root/build inspection.
No T5.

Estado:

`T4_FULL_CANDIDATE_SELECTED_FINAL_VALIDATION_PENDING`
