# LI — T3 final dual-stage gate V03

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / FINAL T3 GATE

## Candidatos únicos

- Rata Qi: `R1_INSTANCE_BASIC`
- Serpiente Qi: `S1_INSTANCE_POISON_TICK`
- Avispa Jade: `A2_INSTANCE_POISON_TICK`
- Mono Píldoras: `M2_INSTANCE_MANOTAZO_PACKET`
- Lobo Espiritual: `L2_INSTANCE_EMBOSCADA_DAMAGE`

Cada uno se compara únicamente contra `T2_FROZEN`.

## Trigger T3 común

Counter sólo si:
1. T2 había reconocido patrón;
2. siguiente acción real confirma la predicción;
3. T1 estaba activo;
4. T1 cambió causalmente el resultado defensivo.

EVADE:
- mismo roll habría impactado contra EVA natural;
- el bono T1 lo convierte en fallo.

DEFENSE_UP:
- mismo packet conecta;
- DEF T1 previene >0 daño respecto de DEF natural.

## Matriz final

- 2 stages:
  - LianQi_I / LI_OVERREACH;
  - LianQi_IV / LIV_STRUCTURAL.
- 5 especies.
- EXPECTED_STAGE + HIGH_ROLL_STRESS.
- 5 raíces.
- 4 policies.
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO.
- pools 64/16/8/4.
- 4 réplicas.
- CRN pareado T2/T3.

Total previsto: **294.400 combates**.

## Hard guards

- T0/T1/T2 exactos;
- false counter = 0;
- no counter por fallo natural;
- Lobo sólo counter si T1 previno >0;
- no root/build inspection;
- no future RNG;
- no universal stat scaling;
- no new clocks/timers;
- no T4;
- no canonical write;
- no win-rate target;
- 0 timeout/NaN/Inf;
- 0 degenerate loops.

## UI Colab

Estándar definitivo:
- panel único con `display_id`;
- barra HTML/CSS coloreada;
- verde normal;
- ámbar checkpoint;
- rojo sólo error;
- track gris;
- porcentaje, n/total, CPU, RAM, fights/s, ETA y checkpoint en el mismo panel;
- 0 tqdm;
- 0 rutas Kaggle.

No ratificación automática.


## Paquete Colab preparado

Artefacto:
`COLAB_LI_MONSTER_T3_FINAL_DUAL_STAGE_GATE_V03.zip`

- ZIP SHA-256: `391701791a3dd8b66878062afceafef576fbb44e623bb9bf24e783dcf00ac9a9`
- Notebook SHA-256: `6a8fc396d9b06d7c325d3e4790d96ec19592dccb89356baaeffff35c150365dd`
- Runner SHA-256: `edb52e3f635dc54aca2a845072d7378224ce1bf60fb144aed099223a7568c1e1`
- notebook válido `nbformat 4`;
- 294.400 combates previstos;
- 0 imports tqdm;
- 0 rutas Kaggle;
- panel único HTML coloreado:
  - verde ejecución;
  - ámbar checkpoint;
  - rojo issues/error;
- workers automáticos;
- checkpoints por etapa/especie.

No ratifica T3 automáticamente.
