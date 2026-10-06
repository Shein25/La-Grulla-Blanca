# LI — T4 Mature Adaptation Micro-screen V01

Fecha: 2026-10-06
Estado: READY_FOR_COLAB / LAB ONLY

## Prerrequisitos congelados

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- T2: `T2_LI_FINAL_FREEZE_2026-10-06`
- T3: `T3_LI_FINAL_FREEZE_2026-10-06`
- Variabilidad: `monster-individual-variance-v0.4`
- Mutantes/sufijos: `MUTANT_SUFFIX_CONTRACT_V1`

T4 = **ADAPTACIÓN MADURA / segunda respuesta compatible**.

No existe T5.

## Activación común V01

Para aislar geometría:

`REPLACE_BASIC_WHEN_READY / CD5`

Reglas:
1. T1 survival conserva prioridad.
2. Técnica canónica due por cadencia conserva prioridad.
3. Sólo si el turno iba a ser BASIC y T4 está listo, T4 reemplaza ese BASIC.
4. T4 usa cooldown de 5 rondas en V01.
5. T4 no altera T0–T3.
6. Decay por debajo de T4 deshabilita la segunda respuesta.

CD5 es control común de laboratorio. No se congela para las especies nuevas hasta focal.

## Rata — autoridad histórica + control

Identidad histórica: `Mordisco Frenético`.

### R4A_HISTORIC_CANONICAL_HALF
- opening: `INSTANCE_BASIC ×1.0`;
- follow-up: `2d4 canónico ×0.50`;
- precisión independiente por packet;
- crítico independiente por packet;
- DEF y absorción por packet.

### R4B_INSTANCE_HALF
- opening: `INSTANCE_BASIC ×1.0`;
- follow-up: `INSTANCE_BASIC ×0.50`;
- resto idéntico.

Objetivo: comprobar si el follow-up canónico histórico sigue siendo preferible con el T0/T1/T2/T3 actual.

## Serpiente Qi — hipótesis LAB

Identidad: presión sostenida por veneno.

### S4A_BASIC_POISON_ON_OPEN_HIT
- opening: `INSTANCE_BASIC`;
- si opening impacta: un `INSTANCE_POISON_TICK` inmediato;
- no añade duración.

### S4B_BASIC_POISON_INDEPENDENT
- opening: `INSTANCE_BASIC`;
- segundo contacto con precisión independiente;
- si conecta: un `INSTANCE_POISON_TICK` inmediato;
- no añade duración.

## Avispa Jade — hipótesis LAB

Identidad: movilidad/evasión + picadura + veneno.

### A4A_BASIC_POISON_ON_OPEN_HIT
- opening: `INSTANCE_BASIC`;
- si impacta: un `INSTANCE_POISON_TICK`.

### A4B_BASIC_POISON_INDEPENDENT
- opening: `INSTANCE_BASIC`;
- segundo contacto independiente;
- si conecta: un `INSTANCE_POISON_TICK`.

La comparación busca si su perfil móvil justifica un follow-up independiente sin crear una técnica nueva.

## Mono Píldoras — hipótesis LAB

Identidad: oportunismo y presión sobre Qi/Dantian.

### M4A_BASIC_DRAIN
- opening: `INSTANCE_BASIC`;
- si impacta: QI_DRAIN 6.

### M4B_MANOTAZO_REPLACE
- un packet `INSTANCE_MANOTAZO`;
- si impacta: QI_DRAIN 6;
- no consume ni desplaza la cadencia normal de Manotazo.

## Lobo Espiritual — hipótesis LAB

Identidad: apex / Emboscada.

### L4A_EMBOSCADA_REPLACE
- reemplaza BASIC por `INSTANCE_EMBOSCADA_DAMAGE`.

### L4B_BASIC_PLUS_HALF_EMBOSCADA
- opening: `INSTANCE_BASIC`;
- follow-up independiente: `INSTANCE_EMBOSCADA_DAMAGE ×0.50`;
- DEF/absorción por packet.

## Baseline

Cada especie se compara contra:
`T3_FROZEN`

T3 permanece activo y congelado en todos los brazos T4.

## Matriz

- stages:
  - LianQi_I / LI_OVERREACH;
  - LianQi_IV / LIV_STRUCTURAL;
- 5 especies;
- EXPECTED_STAGE + HIGH_ROLL_STRESS;
- 5 raíces;
- 4 policies;
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO;
- pools 64/16/8/4;
- 2 réplicas;
- 3 brazos por especie (baseline + 2 candidatos);
- CRN pareado.

Total previsto: **220.800 combates**.

## Métricas T4

- T4 uses/fight;
- multi-use rate;
- T4 direct/DOT/Qi per fight;
- T4 packet hit rate;
- T4 damage/use y p90;
- survival displacement = 0;
- due-technique displacement = 0;
- T3 activations / false counters / loops;
- rounds / HP / Qi pressure;
- split por stage/policy/población;
- timeout/NaN/Inf.

## Hard guards

- T0/T1/T2/T3 exactos;
- T4 nunca desplaza survival;
- T4 nunca desplaza técnica due;
- no root/build inspection;
- no future RNG;
- no universal stat scaling;
- no Definitivas;
- no T5;
- no canonical runtime write;
- no win-rate target universal;
- false counter T3 = 0;
- 0 degenerate loops.

## UI Colab

- panel único;
- barra HTML coloreada;
- verde ejecución;
- ámbar checkpoint;
- rojo error/issues;
- CPU/RAM/fights/s/ETA/checkpoint en el mismo panel;
- 0 tqdm;
- 0 rutas Kaggle.

## Alcance metodológico

`LIV_STRUCTURAL` usa etapa/equipo LIV pero técnicas base sin especializaciones para no contaminar el frente con el balance de técnicas normales aún separado.

Antes de integración final del Arco 1 deberá existir un cross-check específico contra el Player Power Envelope/técnicas cerradas.

No ratificación automática.
