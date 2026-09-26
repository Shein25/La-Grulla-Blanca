# HANDOFF MAESTRO — Monster Adaptive Survival / Stage Progression / Balance
Fecha: 2026-09-26

## Estado congelado para continuar en otra conversación

Rama de trabajo:
`experiment/monster-adaptive-survival-lab-v0.1`

HEAD exacto de trabajo:
`427c4d59f6463323636e41ea74d9f7f797510dff`

Snapshot exacta, sin cambios:
`snapshot/handoff-2026-09-26-monster-adaptive-balance`

Rama de documentación de este backup:
`docs/experimentos-backup-2026-09-26`

## Guardas obligatorias

- NO tocar `main`.
- NO hacer merge.
- PR #17 y #18 permanecen draft/open.
- No repetir baselines históricos ya cerrados.
- No modificar el Monster Combat AI auditado salvo necesidad concreta.
- La IA decide; el motor resuelve.
- `CADENCE_COMPAT` sigue siendo autoritativo.
- Todo este bloque sigue siendo EXPERIMENTAL / NO CANÓNICO hasta decisión explícita.
- Las cifras Monte Carlo sirven para comparar modelos, no prometen win rates exactos.

## Verificación al cerrar

`main`:
`de3a7593dc59120f5940b3589bc42ed6e500ba9b`

PR #17:
- open
- draft
- merged = false
- HEAD `adc086ba5aca8d2a98c63f2df742ac019a498fea`

PR #18:
- open
- draft
- merged = false
- HEAD `289a090b83f2e0f3652c93c870f88ec2c4256bc4`

## Contexto ya establecido

El Arco 1 tiene cuatro bandas de progresión natural:

```text
LianQi I   → Secta Exterior / Bosques
LianQi II  → Cantera / Vetas
LianQi III → Aguas / Barrancos
LianQi IV  → Alturas
```

Distribución de monstruos:

### Etapa I
- Rata de Qi — NORMAL
- Avispa de Jade — NORMAL
- Serpiente de Qi — NORMAL
- Macaco ladrón — SKIRMISHER
- Lobo espiritual — APEX_BRIDGE

### Etapa II
- Sapo de Ceniza — NORMAL
- Escarabajo de Hierro — TANK
- Eco del Caído — ELITE
- Sapo Caldera — BOSS
- Rey Escarabajo — BOSS

### Etapa III
- Pez Lunar — NORMAL
- Anguila Estelar — SKIRMISHER
- Sombra Ahogada — ELITE
- Guardián Coral — BOSS

### Etapa IV
- Devorador de Niebla — NORMAL
- Halcón de Tormenta — SKIRMISHER
- Mantis de Nube — BOSS
- Centinela de Plumas — BOSS

## Progresión adaptativa ya acordada

La etapa nativa NO hace level scaling con la etapa actual del jugador.

```text
playerStage < nativeStage
→ Tier 0
→ BASE_NATURAL

playerStage == nativeStage
→ Tier 1
→ SUPERVIVENCIA

playerStage == nativeStage + 1
→ Tier 2
→ RECONOCIMIENTO DE PATRONES
→ memoria persistente
→ defensa anticipatoria elegible

playerStage == nativeStage + 2
→ Tier 3
→ CONTRAADAPTACIÓN
→ rama defensiva permitida por especie

playerStage == nativeStage + 3
→ Tier 4
→ ADAPTACIÓN MADURA
→ segunda adaptación compatible
```

El techo habilita capacidades; no las concede sin XP adaptativa real.

## Modelo defensivo E1 definitivo — candidato experimental

Archivo fuente:
`adaptive/survival-evolution-v0.1.mjs`

Estado:
`EXPERIMENTAL_NON_CANONICAL_SURVIVAL_V01_FINAL_CANDIDATE`

Valores:

| Monstruo | Defensa E1 |
|---|---|
| Rata de Qi | Esquiva +25 |
| Avispa de Jade | Esquiva +25 |
| Serpiente de Qi | Esquiva +20 |
| Macaco ladrón | Esquiva +20 |
| Lobo espiritual | Defensa +3 |
| Sapo de Ceniza | Mitigación 35% |
| Escarabajo de Hierro | Absorción 4 / reserva 8 |
| Eco del Caído | Mitigación 40% |
| Sapo Caldera | Absorción 4 / reserva 8 |
| Rey Escarabajo | Absorción 5 / reserva 10 |
| Pez Lunar | Esquiva +25 |
| Anguila Estelar | Esquiva +25 |
| Sombra Ahogada | Mitigación 40% |
| Guardián Coral | Absorción 5 / reserva 10 |
| Devorador de Niebla | Absorción 4 / reserva 8 |
| Halcón de Tormenta | Esquiva +30 |
| Mantis de Nube | Defensa +5 |
| Centinela de Plumas | Defensa +5 |

Todas:
- consumen la acción del monstruo;
- cooldown = 2 rondas;
- subordinadas a `CADENCE_COMPAT`;
- no atacan y defienden simultáneamente;
- se adaptan a anatomía/comportamiento de la especie.

## Dos modelos de balance ya fijados para comparación

Fuente principal:
`adaptive/RESULTADO_COMPARACION_DEFENSAS_ESCALADO_ESTADISTICO_v0.1.md`

### MODELO A — FINAL_E1_FIXED_STATS

```text
estadísticas canónicas ver74
+
defensas E1 finales
+
inteligencia/adaptación
```

Promedio de victoria de jugador preparado por banda:

```text
Etapa I    94,9%
Etapa II   71,3%
Etapa III  78,6%
Etapa IV   87,2%
```

Casos representativos:

```text
Escarabajo       94,6%
Sapo Caldera     44,2%
Rey Escarabajo   31,5%
Guardián Coral   35,8%
Devorador        97,9%
Halcón           96,3%
Mantis           72,9%
Centinela        81,8%
```

Lectura:
- maximiza el peso de la IA y del aprendizaje;
- preserva mejor la sensación de superar zonas antiguas;
- menor riesgo de power creep.

### MODELO B — FINAL_E1_STAGE_SCALING

La etapa nativa añade crecimiento físico fijo por banda:

```text
            HP        DAÑO      ATQ     DEF

Etapa I    ×1,00      ×1,00      +0      +0
Etapa II   ×1,05      ×1,05      +0      +0
Etapa III  ×1,10      ×1,10      +0      +0
Etapa IV   ×1,15      ×1,15      +0      +0
```

Implementado experimentalmente en:
`adaptive/stage-progression-v0.1.mjs`

Estado:
`EXPERIMENTAL_NON_CANONICAL_HP_DAMAGE_5PCT_PER_STAGE_V01`

Promedio preparado por banda:

```text
Etapa I    94,7%
Etapa II   66,4%
Etapa III  71,4%
Etapa IV   74,3%
```

Casos representativos:

```text
Escarabajo       91,8%
Sapo Caldera     35,7%
Rey Escarabajo   24,5%
Guardián Coral   22,1%
Devorador        93,4%
Halcón           89,5%
Mantis           51,3%
Centinela        63,0%
```

Lectura:
- hace que Cantera/Aguas/Alturas se sientan físicamente distintas;
- NO escala según la etapa actual del jugador;
- una Rata siempre pertenece a banda I y queda ×1,00;
- una Mantis siempre pertenece a banda IV y usa ×1,15 en este modelo.

## Escalados rechazados

### ATQ/DEF porcentual

Descartado.

Razón: ATQ/DEF son enteros dentro de d20 y pequeños porcentajes cruzan breakpoints por redondeo.

Ejemplo:

```text
DEF 15 × 1,06 = 15,9
→ 16
```

Ese +1 puede equivaler aproximadamente a otro escalón de 5 puntos porcentuales de impacto.

Resultados representativos al escalar todos los stats:

```text
Mantis
0% → 73,5%
1% → 72,1%
2% → 58,6%

Centinela
0% → 82,6%
1% → 81,2%
2% → 70,4%

Guardián Coral
0% → 34,9%
1% → 32,9%
2% → 27,2%
```

### HP/daño + ATQ discreto

También se probó:

```text
HP/daño +5% por etapa
+
ATQ +1 desde Etapa III
```

Promedio:

```text
Etapa I   95,2%
Etapa II  66,9%
Etapa III 67,9%
Etapa IV  70,0%
```

Casos:

```text
Guardián Coral 17,2%
Mantis         45,3%
Centinela      57,5%
```

Descartado como base por hacer que el peso estadístico empiece a dominar sobre técnicas/equipo/IA.

## Simulación acumulada de este cierre

Sólo para comparar los modelos A/B y sensibilidades finales:

```text
828.000 duelos — sensibilidad 0–5% escalando todos los stats
496.800 duelos — set anterior vs defensa final vs all-stat 1%
372.600 duelos — sin escalado vs HP/daño vs HP/daño+ATQ
---------------------------------------------------------------
≈1.697.400 duelos
```

Más el barrido anterior por etapas:

```text
1.104.000 duelos
```

No hizo falta Colab todavía.

## Tests cerrados

Validación dirigida final:
`12/12 PASS`

No repetirla salvo que cambien:
- valores E1;
- política de cooldown;
- distribución de etapas;
- escalado de stats;
- contrato de `CADENCE_COMPAT`.

Tampoco repetir:
- 107/107 Monster Canonical Behavior baseline;
- 336/336 NPC baseline;
- 15/15 transversal NPC;
salvo que se cambie directamente algo que invalide esos baselines.

## Archivos clave para retomar

1. `adaptive/survival-evolution-v0.1.mjs`
2. `adaptive/stage-progression-v0.1.mjs`
3. `adaptive/RESULTADO_COMPARACION_DEFENSAS_ESCALADO_ESTADISTICO_v0.1.md`
4. `adaptive/RESULTADO_PROGRESION_MONSTRUOS_ETAPAS_v0.1.md`
5. `adaptive/MATRIZ_PROGRESION_MONSTRUOS_ETAPAS_v0.1.md`
6. `adaptive/ANALISIS_ARSENAL_JUGADOR_DEFENSAS_E1_v0.1.md`
7. `benchmark/stage-progression-benchmark-v0.1.mjs`
8. `benchmark/player-arsenal-vs-survival-v0.1.mjs`
9. `tests/survival-evolution.test.mjs`
10. `tests/stage-progression.test.mjs`

## Nota de precedencia documental

`RESULTADO_PROGRESION_MONSTRUOS_ETAPAS_v0.1.md` fue escrito antes del experimento de escalado estadístico y todavía dice que no se otorga stat scaling.

Para el estado actual, la precedencia es:

```text
RESULTADO_COMPARACION_DEFENSAS_ESCALADO_ESTADISTICO_v0.1.md
>
RESULTADO_PROGRESION_MONSTRUOS_ETAPAS_v0.1.md
```

Es decir:
- Modelo A conserva la política original sin stat scaling.
- Modelo B añade el escalado HP/daño 100/105/110/115.
- ambos siguen siendo candidatos experimentales válidos.

## Próximo punto lógico de trabajo

No volver a debatir desde cero los valores de E1 ni las cuatro bandas.

La siguiente conversación debe empezar desde la elección/continuación entre:

```text
A — FINAL_E1_FIXED_STATS
B — FINAL_E1_STAGE_SCALING
```

y después avanzar sobre uno de estos huecos reales:

1. decidir cuál modelo será preferido para Arco 1;
2. persistencia real de `survivalXp / evolutionStage`;
3. política de aprendizaje Tier 2–4;
4. memoria persistente de patrones del jugador;
5. defensa anticipatoria;
6. executor defensivo real para EVADE / DEFENSE / ABSORB / MITIGATE;
7. después, NPC↔monster combat integration.

No inventar nuevas arquitecturas si las capas existentes bastan.
