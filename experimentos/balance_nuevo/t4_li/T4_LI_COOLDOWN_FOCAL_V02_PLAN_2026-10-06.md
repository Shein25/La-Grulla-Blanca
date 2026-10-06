# LI — T4 Cooldown Focal V02

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Geometrías seleccionadas

- Rata Qi: `R4A_HISTORIC_CANONICAL_HALF`
- Serpiente Qi: `S4A_BASIC_POISON_ON_OPEN_HIT`
- Avispa Jade: `A4A_BASIC_POISON_ON_OPEN_HIT`
- Mono Píldoras: `M4B_MANOTAZO_REPLACE`
- Lobo Espiritual: `L4A_EMBOSCADA_REPLACE`

## Eje único V02

Cada geometría se prueba con:

- CD3
- CD5
- CD7

más baseline:
- `T3_FROZEN`

No cambia ningún otro eje.

## Prioridad congelada

1. T1 survival.
2. Técnica canónica due.
3. T4 si lista.
4. BASIC.

T4 jamás desplaza survival ni una técnica due.

## Matriz

- 2 stages:
  - LianQi_I / LI_OVERREACH
  - LianQi_IV / LIV_STRUCTURAL
- 5 especies.
- 4 brazos por especie: T3 + CD3/CD5/CD7.
- EXPECTED_STAGE + HIGH_ROLL_STRESS.
- 5 raíces.
- 4 policies.
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO.
- pools 64/16/8/4.
- 2 réplicas.
- CRN pareado.

Total previsto: **294.400 combates**.

## Guardias

- T0–T3 exactos.
- Acechante C20 temporal, sin precision drift.
- false T3 counter = 0.
- no root/build inspection.
- no future RNG.
- no universal stat scaling.
- no Definitivas.
- no T5.
- no canonical write.
- no win-rate target.
- 0 timeout/NaN/Inf.
- no desplazamiento de survival/due technique.

## Decisión esperada

Elegir un cooldown final por especie.

No asumir que todas deben compartir CD.

Si dos cooldowns son funcionalmente equivalentes por interacción con cadencia,
preferir el más simple/coherente y documentar la equivalencia efectiva.

## UI Colab

- panel único;
- barra verde en ejecución;
- ámbar checkpoint;
- rojo error/issues;
- porcentaje, CPU, RAM, fights/s, ETA, checkpoint;
- 0 tqdm;
- 0 rutas Kaggle.

No ratificación automática.


## Paquete Colab preparado

Artefacto:
`COLAB_LI_MONSTER_T4_COOLDOWN_FOCAL_V02.zip`

- ZIP SHA-256: `f571c7283baa909b9a9e4c69dbef9cde78b9403dc1339da8af09ec5c76573878`
- Notebook SHA-256: `3e050516d91fe45efa0b531e84bdd2394187ff422112908558c7bb47c4dfffd4`
- Runner SHA-256: `7ce941bdf743b81bc9b8f188c7f7cc871b0b92d796cc449acfb2e85607fbb998`
- notebook válido `nbformat 4`;
- 294.400 combates previstos;
- 0 imports tqdm;
- 0 rutas Kaggle;
- panel único coloreado;
- Acechante C20 con semántica temporal corregida;
- no ratificación automática.
