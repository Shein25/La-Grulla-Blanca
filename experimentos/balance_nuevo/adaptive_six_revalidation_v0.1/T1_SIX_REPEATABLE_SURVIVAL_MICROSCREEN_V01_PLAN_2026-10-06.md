# Six Repeatables — T1 Survival Revalidation Micro-screen V01

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Rama

`experiment/monster-adaptive-six-revalidation-v0.1`

Base:
`experiment/li-monster-t0-final-t1-lab-v0.1`

No main. No merge. No runtime canónico.

## Alcance

Revalidar T1 para seis especies repetibles con T0 y variación individual ya ratificados:

- Sapo Ceniza — LianQi II
- Escarabajo de Hierro — LianQi II
- Pez Lunar — LianQi III
- Anguila Estelar — LianQi III
- Devorador de Niebla — LianQi IV
- Halcón Tormenta — LianQi IV

Los siete `unique:true` quedan fuera de T1–T4.

## Autoridad preservada

No se reabre:
- T0 de estas seis especies;
- envelopes de variación individual;
- incidencia Mutante;
- T0→variación→Mutante como orden de materialización.

Fuente consolidada:
`SIX_REPEATABLE_T0_VARIANCE_AUTHORITY_V01.json`

La cadena T1–T4 histórica del 2026-10-01 es sólo ancla conceptual/numérica.
No es autoridad final porque precede a las semánticas adaptativas congeladas el 2026-10-06.

## Semántica T1 actual

Se adopta la semántica común final:

- trigger natural: HP <=30% OR golpe recibido >=20% HPmax;
- activar T1 consume el turno del monstruo;
- no root/build inspection;
- no future RNG;
- no universal stat scaling;
- no target universal de win-rate;
- no T2/T3/T4 durante este micro-screen.

## Hipótesis V01

Cooldown común de laboratorio: **CD5**.
Se aísla primero la magnitud. El cooldown se focaliza después.

### Sapo Ceniza
Identidad histórica: `MITIGATE_NEXT`.

Candidatos:
- 10%
- 20%
- 30%

La magnitud histórica cerrada fue 10%, pero se revalida bajo trigger 30/20.

### Escarabajo de Hierro
Identidad histórica: `DEFENSE_UP`.

Candidatos:
- +2 DEF
- +4 DEF
- +6 DEF

La magnitud histórica cerrada fue +2 DEF.

### Pez Lunar
Identidad histórica: `EVADE_NEXT`.

Candidatos:
- +20 EVA
- +30 EVA
- +40 EVA

Ancla histórica: +20 EVA.

### Anguila Estelar
Identidad histórica: `EVADE_NEXT`.

Candidatos:
- +25 EVA
- +35 EVA
- +45 EVA

Ancla histórica: +35 EVA.

### Devorador de Niebla
Identidad histórica: `EVADE_NEXT`.

Candidatos:
- +20 EVA
- +30 EVA
- +40 EVA

Ancla histórica: +20 EVA.

### Halcón Tormenta
Identidad histórica: `EVADE_NEXT`.

Candidatos:
- +25 EVA
- +35 EVA
- +45 EVA

Ancla histórica: +35 EVA.

## Stage contexts

Para medir amenaza nativa + replay/overreach sin convertir la etapa en hard gate:

- Sapo/Escarabajo:
  - LianQi II / NATIVE
  - LianQi IV / REPLAY
- Pez/Anguila:
  - LianQi III / NATIVE
  - LianQi IV / REPLAY
- Devorador/Halcón:
  - LianQi III / OVERREACH
  - LianQi IV / NATIVE

## Matriz V01

Por especie:
- 2 stage contexts;
- EXPECTED_STAGE + HIGH_ROLL_STRESS;
- 5 raíces;
- 4 policies;
- T0_FROZEN + 3 candidatos T1;
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO;
- pools 64/16/8/4;
- 2 réplicas;
- CRN pareado.

Total previsto: **353.280 combates**.

## Guardias

- T0 exacto.
- variación exacta.
- sufijos Mutantes derivados de q_axis, sin RNG extra.
- Acechante C20: +20 PREC sólo siguiente ataque.
- 0 precision drift.
- T1 consume turno.
- T1 no toca técnica T0.
- no T2/T3/T4.
- no unique.
- no Definitivas.
- no T5.
- no root/build inspection.
- no future RNG.
- 0 timeout/NaN/Inf.
- no canonical write.

## Métricas

- player win-rate, diagnóstica;
- rounds;
- HP final;
- Qi spent/drained;
- T1 procs/fight;
- causal mitigation/evasion/DEF;
- técnica T0 turns/fight;
- BASIC turns/fight;
- delta pareado T1 vs T0;
- split por stage/policy/population/root;
- precision drift;
- timeouts/issues.

## UI Colab

Estándar actual:
- panel único;
- barra HTML/CSS verde;
- ámbar checkpoint;
- rojo error/issues;
- porcentaje;
- CPU/RAM;
- peleas/s;
- ETA;
- checkpoint;
- 0 tqdm;
- 0 rutas Kaggle.

## Salida

El micro-screen NO congela T1.

Objetivo:
- seleccionar una magnitud finalista por especie;
- detectar si alguna identidad T1 histórica ya no funciona bajo las semánticas actuales;
- abrir después un focal de cooldown sólo donde sea necesario.
