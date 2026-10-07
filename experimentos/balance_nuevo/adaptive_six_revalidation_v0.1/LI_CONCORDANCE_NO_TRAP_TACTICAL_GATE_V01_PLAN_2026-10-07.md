# LianQi I — Concordance NO_TRAP Tactical Gate V01

Fecha: 2026-10-07  
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`

## Estado previo

Equipo LianQi I congelado:
`LI_EQUIPMENT_FREEZE_2026-10-07.md`

Catálogo integrado:
`60dbb1ebae69486b3d9215ea794362cccd3bff28`

Freeze doc:
`74922745aaf84db059dd35ecfcce5884483ce7f5`

## Pregunta

Una Concordancia bien usada, ¿puede convertirse sistemáticamente en una trampa para el jugador?

El gate NO exige que ON gane a OFF en cada semilla ni que una mala decisión táctica sea gratis.

Criterio conceptual:

> Una Concordancia bien usada no debe producir una desventaja material y sistemática atribuible al propio efecto de Concordancia.

## Separación causal

El gate separa dos preguntas:

1. **Monotonicidad del receptor:** partiendo del mismo estado después de generar el Eco, activar la Concordancia no debe degradar mecánicamente el receptor.
2. **Utilidad táctica de combate:** usando una política razonable de cuándo consumir/guardar el Eco, ON no debe mostrar una desventaja persistente frente a OFF con la misma secuencia de decisiones.

Así se evita confundir:
- efecto de Concordancia;
- coste de elegir una técnica de setup;
- mal timing del jugador;
- ruido Monte Carlo.

## Scope

- 16 relaciones activas LI.
- 4 BASE NONE como sentinel.
- 5 raíces.
- 5 monstruos.
- T0/T1.
- equipo final congelado:
  - MANDATORY_ENTRY
  - EXPECTED_STAGE
  - HIGH_ROLL_STRESS
- candidate roots V04B.
- relation-specific Concordance pack V04B.

No T2/T3/T4. No equipo nuevo. No cambios de monstruos.

## Políticas

### ASAP
Ciclo dirigido source→receiver repetido. Es referencia del comportamiento automático/temprano, no criterio de freeze.

### TACTICAL_HOLD
La política puede repetir la técnica fuente y conservar su Eco cuando consumirlo todavía no aporta valor claro.

Reglas por hook:

- DIRECT_DAMAGE: consumir salvo overkill evidente.
- PERCENT_PENETRATION: consumir cuando DEF dinámica > 0.
- PRECISION: consumir cuando el receptor no está ya en cap práctico de hit.
- CRIT_CHANCE: consumir salvo overkill evidente.
- CONTROL_POWER: consumir cuando el monstruo probablemente sobreviva al receptor y todavía pueda actuar.
- EVASION_DEBUFF: consumir cuando la evasión del monstruo sea relevante y el combate no esté ya resuelto.
- CONTAINED_TRIGGER / NÚCLEO DE MAGMA: consumir cuando exista ventana razonable para una detonación posterior dentro de duración y Qi disponible.

Las decisiones se calculan sin mirar el resultado aleatorio futuro.

## Fases

### 1 — Receiver monotonicity
R=32.

Se genera el Eco con la fuente. Antes del receptor se clona estado + RNG. Se ejecuta el mismo receptor OFF y ON.

Checks por hook:
- daño/hit no empeora para DIRECT_DAMAGE, PEN, PRECISION, CRIT;
- CONTROL_POWER no convierte un éxito de control OFF en fallo ON;
- EVASION_DEBUFF no reduce la magnitud útil del debuff;
- MAGMA no reduce el golpe receptor y crea reserva sólo cuando corresponde.

### 2 — Tactical paired fights
R=64.

Para cada contexto:
- misma semilla;
- misma política TACTICAL_HOLD;
- OFF vs ON;
- relación inversa deshabilitada;
- resultado pareado.

Métricas:
WR, HP final, Qi final, rondas, daño, control, survival activations, resoluciones.

### 3 — ASAP reference
R=32.

Misma matriz para observar cuándo el uso automático es peor que el táctico. No es hard gate.

### 4 — Escalation + BASE NONE
- candidatos sospechosos de Fase 2 se escalan automáticamente a R=512 con semillas nuevas;
- 4 BASE NONE: cero resolución/consumo/fallback.

## Suspicious screen

Escalar un contexto si en TACTICAL:
- delta WR ON-OFF <= -3,125 pp a R64; o
- delta HP final <= -2 pp sin mejora de WR.

Agrupar además por relation / monster / tier / gear / root.

## Hard NO_TRAP fail

Una relación falla sólo si, tras escalación:
- la desventaja ON es reproducible;
- el intervalo pareado 95% mantiene una desventaja material;
- no se explica por una decisión distinta entre brazos;
- y existe en un uso que la política clasifica como tácticamente válido.

Objetivo material de alerta:
- WR <= -1 pp con 95% CI superior < 0; o
- degradación consistente de supervivencia/recursos sin compensación.

No fallar por una semilla individual.

## Output

`LI_CONCORDANCE_NO_TRAP_TACTICAL_GATE_V01_REVIEW.zip`

No auto-freeze. Si PASS:
- freeze de Concordancias LI;
- luego freeze/cierre global de LianQi I.
