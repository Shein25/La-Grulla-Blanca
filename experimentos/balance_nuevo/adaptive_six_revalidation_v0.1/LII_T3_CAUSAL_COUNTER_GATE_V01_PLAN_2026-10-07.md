# LII T3 Causal Counter Gate V01

Fecha: 2026-10-07
Estado: DESIGN_READY / LAB ONLY
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`

## Autoridad congelada

T0:
`experimentos/balance_nuevo/t0_lii/T0_LII_FREEZE_MANIFEST_2026-10-07.json`

T1:
`experimentos/balance_nuevo/t1_lii/T1_LII_REACTIVE_FREEZE_2026-10-07.json`

T2:
`experimentos/balance_nuevo/t2_lii/T2_LII_RECOGNITION_FREEZE_2026-10-07.json`

T2 está human-ratified y no se recalibra en este frente.

## Identidad T3

T3 = **CONTRAADAPTACIÓN / SPECIES_COUNTER CAUSAL**.

No agrega stats.
No modifica T1/T2.
No crea una técnica canónica nueva.
No consume ni sustituye la técnica canónica due.
No introduce T4.

## Trigger común obligatorio

Un counter T3 sólo puede ocurrir si, en este orden:

1. T2 había reconocido un patrón válido;
2. la siguiente acción real del jugador confirma la categoría predicha;
3. T1 estaba activo antes de resolver esa interacción;
4. T1 fue causalmente responsable de mejorar el resultado defensivo;
5. el counter se resuelve después de la interacción causal usando el pipeline normal.

Que T1 esté activo NO basta.
Que T2 haya reconocido algo NO basta.
Un miss natural o una interacción donde T1 previno 0 NO puede activar T3.

## Sapo Ceniza

T1 congelado:
`MITIGATE_NEXT 60% / CD3 / REACTIVE`.

### Trigger causal

Lab ID:
`SAPO_T3_CAUSAL_INSTANCE_BASIC_V01`

Elegible sólo si:
- la predicción T2 fue confirmada;
- el paquete DIRECTO del jugador conecta;
- MITIGATE_NEXT estaba activo;
- usando exactamente el mismo packet/roll/crit, la mitigación T1 previno >0 daño directo.

No counter:
- por miss;
- por DoT;
- si el paquete directo prevenido por T1 es 0;
- por mera presencia de T1 sin interacción causal.

### Counter

`INSTANCE_T0_BASIC`

- un packet inmediato de daño directo;
- usa el basic_damage congelado actual del Sapo: `1d2+5`;
- pipeline normal de daño directo;
- no añade burn;
- no QI drain;
- no control;
- no consume el turno ordinario del monstruo;
- no consume ni retrasa Nube de Hollín;
- no existe límite artificial ONCE_PER_FIGHT.

## Escarabajo de Hierro

T1 congelado:
`DEFENSE_UP +4 / CD3 / REACTIVE`.

### Trigger causal

Lab ID:
`ESCARABAJO_T3_CAUSAL_INSTANCE_BASIC_V01`

Elegible sólo si:
- la predicción T2 fue confirmada;
- la acción ofensiva conecta;
- DEFENSE_UP estaba activo;
- se compara el mismo packet, penetración, roll y crit con DEF natural vs DEF natural +4;
- el +4 de T1 previno >0 daño directo.

No counter:
- por miss;
- si penetración/packet hace que +4 DEF prevenga 0;
- por mera presencia de T1.

### Counter

`INSTANCE_T0_BASIC`

- un packet inmediato de daño directo;
- usa el basic_damage congelado actual del Escarabajo: `1d2+3`;
- pipeline normal;
- no QI drain;
- no DoT;
- no control;
- no consume turno ordinario;
- no consume ni retrasa Carga de Caparazón;
- sin ONCE_PER_FIGHT artificial.

## Variación LII

Para V01:
`ORDINARY_VARIANCE_COLLAPSED_TO_FLOOR`.

No reactivar historical_upper_evidence.
No introducir excepcionales/mutantes.
El objetivo es aislar el efecto marginal T2 -> T3.

## Matriz V01

- 2 especies:
  - sapo_ceniza
  - escarabajo_hierro
- 3 gear contexts:
  - CARRY_OVER_FLOOR
  - EXPECTED_STAGE
  - HIGH_ROLL_STRESS
- 5 roots
- 4 policies
- 2 arms:
  - T2_FROZEN
  - T3_CAUSAL_COUNTER
- R512
- CRN pareado entre brazos

Total:
**122.880 combates**.

Se duplica R respecto del gate T2 porque el evento causal T3 es más raro que recognition/anticipation y necesitamos estimar false-counter y multi-counter con mejor resolución.

## Métricas obligatorias

### Integridad
- represented fights;
- timeout;
- NaN/Inf;
- issues;
- task uniqueness;
- paired context completeness.

### Upstream freeze
- T0 exacto;
- T1 magnitude/CD/semantics exactos;
- T2 memory2/repeat2, EFECTIVA-only y 40/15 exactos;
- T2 recognition/prediction rates vs baseline;
- natural T1 priority;
- canonical due preservation.

### Causalidad T3
- T3 eligibility;
- T3 activations;
- T3 activations/fight;
- T2 predictions confirmed;
- T1 causal interactions;
- false counter count/rate;
- counter after natural miss;
- counter when T1 prevented 0;
- multi-counter fight rate;
- max counters/fight;
- counter packet damage mean/p50/p90/max.

### Combate
- player win-rate;
- rounds;
- player HP pressure;
- monster direct/DOT/total damage;
- T1 natural activations;
- T2 anticipatory activations;
- T3 counter damage;
- canonical technique uses/due preservation.

### Balance
- T3 vs T2 by species × gear × root × policy;
- species × gear aggregates;
- root spread AFTER averaging policies;
- HRS deltas;
- worst paired contexts.

## Hard guards

- expected 122.880 fights;
- 0 timeout;
- 0 NaN/Inf;
- `issues=[]` or every issue explained;
- T2 arm has zero T3 leakage;
- false counter rate = 0;
- no counter after natural miss;
- Sapo: no counter unless MITIGATE_NEXT prevented >0 direct damage;
- Escarabajo: no counter unless +4 DEF prevented >0 direct damage;
- T3 activations <= causal eligibility;
- T3 cannot modify T0/T1/T2;
- no root/build inspection;
- no future RNG inspection;
- no new clock/timer;
- no universal stat scaling;
- no T4;
- no T5;
- no main;
- no merge;
- canonical due/turn preserved;
- no degenerate counter loops.

## Diagnostic guards

- T3 must not be >2 pp easier than paired T2 in any aggregate intended for decision.
- HRS drop >8 pp vs T2 = flag for cliff review, not automatic failure.
- Counter must be nonzero at least in every species × gear aggregate.
- No universal target of player win-rate.
- A very small global delta is not automatically failure if causal activation is real and legible.
- A large delta is not automatically failure if confined to voluntary overreach, but must be explained.

## Interpretation rule

T3 should feel qualitatively different from T2:

T2:
`te reconoce y anticipa su defensa`.

T3:
`te reconoce, su defensa cambia causalmente tu ataque y entonces contraataca`.

La dificultad adicional debe proceder de esa cadena causal, no de stats ocultos.

## Resultado esperado

Artefacto:
`LII_T3_CAUSAL_COUNTER_GATE_V01_REVIEW.zip`

No freeze automático.

Si V01 pasa:
1. auditar resultado;
2. presentar interpretación + propuesta de freeze o focal si aparece un cliff;
3. esperar ratificación humana;
4. sólo después congelar T3;
5. recién entonces desbloquear T4.
