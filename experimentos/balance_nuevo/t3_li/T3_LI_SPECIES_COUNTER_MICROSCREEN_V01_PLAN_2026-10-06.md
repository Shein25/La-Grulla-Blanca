# LI — T3 species-counter micro-screen V01

Fecha: 2026-10-06
Estado: DESIGN_READY / LAB ONLY

## Prerrequisitos congelados

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`.
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`.
- T2: `T2_LI_FINAL_FREEZE_2026-10-06`.
- Variabilidad: `monster-individual-variance-v0.4`.
- Mutantes/sufijos: `MUTANT_SUFFIX_CONTRACT_V1`.

T3 = **CONTRAADAPTACIÓN / SPECIES_COUNTER**.

No escalado universal de stats.

## Trigger causal común

Un counter T3 sólo puede armarse si:

1. T2 reconoció un patrón;
2. la acción real siguiente coincide con la categoría predicha;
3. la supervivencia T1 de esa especie estaba activa;
4. T1 fue causalmente responsable de mejorar el resultado defensivo.

### EVADE_NEXT / EVADE_CHAIN

Para Rata, Serpiente, Avispa y Mono:

- usar el mismo roll de hit;
- comprobar que habría impactado contra la evasión natural del individuo;
- comprobar que falla al añadir el bono T1;
- un fallo que ya ocurría sin T1 **no** puede activar T3.

En Mono cualquiera de las dos cargas de Salto puede satisfacer el trigger.

### DEFENSE_UP

Para Lobo:

- el ataque debe conectar;
- usar exactamente el mismo packet, penetración y roll;
- comparar daño con DEF natural vs DEF natural +10 de T1;
- T3 sólo es elegible si Paso de la Cola Vigilante previno >0 daño;
- no rerollear ataque, daño ni crítico.

## Ancla histórica — Rata

Revalidar, no transplantar números viejos:

`CONFIRMED_PATTERN_REFLEJO_MISS + INSTANCE_BASIC`

El packet usa el `basic_damage` del individuo actual.
En v0.4 la Rata tiene básico congelado `2d4+3`; no asumir la vieja ladder ofensiva.

## Hipótesis LAB por especie

### Rata Qi
- R1 `INSTANCE_BASIC`
  - counter físico inmediato;
  - pipeline normal de daño directo.

### Serpiente Qi
- S1 `INSTANCE_POISON_TICK`
  - un único tick inmediato usando el daño de veneno materializado de esa instancia;
  - no crea duración nueva.
- S2 `INSTANCE_POISON_APPLICATION`
  - aplica una copia normal del veneno actual de la instancia con sus ticks;
  - usa la semántica DOT existente; no inventa un nuevo tipo de stack.

### Avispa Jade
- A1 `INSTANCE_BASIC`
  - respuesta rápida física usando básico de instancia.
- A2 `INSTANCE_POISON_TICK`
  - un tick inmediato del veneno de instancia.

### Mono Píldoras
- M1 `QI_DRAIN_ONLY`
  - drena hasta 6 Qi;
  - sin daño adicional.
- M2 `INSTANCE_MANOTAZO_PACKET`
  - usa daño directo de Manotazo de la instancia + QI_DRAIN 6;
  - no altera la cadencia normal ni la consume.

### Lobo Espiritual
- L1 `INSTANCE_BASIC`
  - represalia física con básico de instancia.
- L2 `INSTANCE_EMBOSCADA_DAMAGE`
  - usa únicamente el daño directo materializado de Emboscada;
  - no modifica su cadencia normal.

Todos son **hipótesis LAB**, no nombres/skills canon.

## Comparación

Para cada especie:
- T2_FROZEN baseline;
- candidatos T3 propios;
- CRN pareado;
- EXPECTED_STAGE + HIGH_ROLL_STRESS;
- 5 raíces;
- 4 policies;
- NATURAL / SPECIALIZED / EXCEPCIONAL / ASCENDIDO;
- sin Definitivas.

## Métricas causales obligatorias

- T3 eligibility;
- T3 activations/pelea;
- false counter rate;
- causal T1 save rate;
- counter packet mean / p90;
- DOT/QI/direct decomposition;
- rounds / HP pressure / Qi pressure vs T2;
- normal vs specialized/exceptional/ascended;
- multi-counter rate;
- degenerate loop count;
- timeout/NaN/Inf.

## Guardias

- false counter debe ser 0;
- no counter por fallo natural;
- no counter si Lobo no previno daño con T1;
- no root/build inspection;
- no future RNG;
- no T0/T1/T2 recalibration;
- no T4;
- no nuevos clocks/timers;
- no win-rate target universal;
- no canonical runtime write.

## UI Colab

Usar estándar **single-panel**:
- `IPython.display(..., display_id=True)`;
- una sola barra;
- sin `tqdm.write()`;
- CPU/RAM/rate/ETA/checkpoint dentro del mismo panel;
- rutas `/content/...` o relativas;
- 0 rutas Kaggle.

## Objetivo

El micro-screen no elige automáticamente T3. Su función es eliminar familias que:
- no se expresan;
- rompen identidad;
- introducen loops;
- castigan patrones no confirmados;
- o crean presión desproporcionada sin aportar comportamiento legible.

Los finalistas pasan luego a focal/final gate.
