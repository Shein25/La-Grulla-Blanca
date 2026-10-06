# HANDOFF — LI T0 cerrado / T1 V02 / Natural Overreach

**Fecha:** 2026-10-06  
**Proyecto:** La Grulla Blanca  
**Repo:** `Shein25/La-Grulla-Blanca`

## Guardias

- No tocar `main`.
- No merge.
- No modificar `ROOMS.exits`.
- No inventar NPCs/vendors/rooms/gates/misiones/estados.
- `freeAiText=false`.
- AI decide; motor resuelve.
- No nuevo reloj/timers.
- A07 cerrado salvo bug.
- Jefes únicos T0 solamente.
- No reabrir T0 ni técnicas ordinarias salvo anomalía material demostrada.
- El artefacto final sigue siendo un HTML monolítico/autocontenido.

## Ramas de autoridad

### Balance LI T0/T1
`experiment/li-monster-t0-final-t1-lab-v0.1`

Checkpoint previo al handoff final:
`6a3816e93653aefae099a671f6924fe22c5a8dbf`

### Adaptive Ecology
`experiment/monster-adaptive-survival-lab-v0.1`

HEAD:
`ff72a5f4827a8c63e7516ff92a673b2ffff83e04`

Status de learning/pressure:
`EXPERIMENTAL_V03_NATURAL_OVERREACH`

### Técnicas
`experiment/techniques-kaggle-heavy-v0.4` @ `b8a4d2740a172a1c8d81c2bd211db0b6fc9a4ef0`

Esa rama conserva documentación del cierre T0 pero **no es la autoridad actual del registry LI**.

---

## T0 LI — CERRADO

Evidencia:
- REVIEW exhaustivo SHA-256: `77337e8ee77dfcd53ca1e679998d158cf5d2f8de8b6f744fc5e4c426bb3bf542`
- 4.864 firmas mecánicas / 6.144 loadouts.
- 5 raíces × 2 policies.
- 3.571.200 combates representados.
- 0 timeouts.
- Veredicto: `T0_LI_EXHAUSTIVE_PASS_READY_TO_FREEZE`.

Freeze numérico:
`f53edd00dd894cb3534df0b8544543dc074f6acb`

Corrección de política del registry:
`0dd67d391191c00521f2a760736caa2245944c6c`

### Stats T0 congelados

| Especie | HP | PRE | EVA | DEF | Ataque / técnica |
|---|---:|---:|---:|---:|---|
| Rata Qi | 45 | 84 | 0 | 2 | básico `2d4+3` |
| Serpiente Qi | 57 | 94 | 11 | 0 | básico `1d2+2`; veneno CD2 `1d2+2 ×3` |
| Avispa Jade | 42 | 102 | 22 | 2 | básico `1d2+1`; veneno CD2 `1d3+2 ×2` |
| Mono Píldoras | 59 | 91 | 28 | 2 | básico `1d2+3`; Manotazo CD2 `1d2+3`; Qi drain 6 |
| Lobo Espiritual | 53 | 100 | 12 | 1 | básico `2d4+2`; Emboscada CD4 `2d6+1` |

EXPECTED final:
- Rata 83,67%
- Serpiente 76,48%
- Avispa 75,55%
- Mono 67,97%
- Lobo 60,86%

**No repetir T0.**

---

## Autoridad adaptativa final — libertad + consecuencias

La etapa del jugador **NO es un hard gate**.

Bandas esperadas:
- LI: T0/T1 esperado.
- LII: T1/T2 esperado.
- LIII: T2 esperado; sobreextensión posible.
- LIV: T3/T4 previstos como rejugabilidad/endgame.

Política:
`ALLOWED_NATURAL_LIMIT_BY_COMBAT_AND_DECAY`

Si un jugador puede seguir produciendo presión válida, puede empujar una población más allá de su banda esperada.

Ejemplo válido:
`T2 → fuerza T3 → ya no puede sostener bajas → pressure cae → T2`

No existe mensaje de bloqueo por nivel. El muro es combate + decay.

### Thresholds
- T0: 0–19
- T1: 20–44
- T2: 45–69
- T3: 70–89
- T4: 90–100

### Pisos históricos
- max T0 → floor T0
- max T1 → floor T1
- max T2 → floor T1
- max T3 → floor T2
- max T4 → floor T3

Por tanto:
- T3 sin alcanzar T4 puede decaer a T2.
- Alcanzar T4 consolida T3 como piso.
- T4 es extremo y reversible hacia T3.

### Código alineado

En `adaptive-learning-ceiling-v0.2.mjs`:
- `pressureCapForAdaptiveCeiling()` devuelve 100 para cualquier banda esperada.
- `clampPressureToAdaptiveCeiling()` no recorta pressure.
- `effectiveAdaptiveTier` usa el tier ganado realmente.
- `overreachedExpectedBand` informa sobreextensión.
- `capabilityCeilingTier` queda sólo como campo histórico/orientativo.

Tests dirigidos: **7/7 PASS**.

Los documentos históricos que exigían ceiling duro quedaron marcados `SUPERSEDED`.

---

## T1 V02 — siguiente paso

Artefacto vigente:
`KAGGLE_LI_MONSTER_T1_SURVIVAL_GENERAL_V02.zip`

SHA-256:
`08feef921d84b5c612dde8baf7110b831649971f352ba75a95d09197758ed93a`

Notebook SHA-256:
`2fedfe163fae1830e657b23701b3e4a7ff6f5961db54762f6239a58fd3a46bb4`

Runner SHA-256:
`46e81974468ba915b724962694a6760ab2ae617b1d8c0663e4a7a20f67aa0f48`

Technique catalog SHA-256:
`912b7824eff9149909ca21b9ad6290c6c82b1e1ea31867da1185c32df383d187`

**NO usar T1 V01.**

Identidades:
- Rata — Reflejo de Madriguera / `EVADE_NEXT`
- Serpiente — Muda del Cauce / `EVADE_NEXT`
- Avispa — Quiebro de Jade / `EVADE_NEXT`
- Mono — Salto del Ladrón / `EVADE_NEXT`
- Lobo — Paso de la Cola Vigilante / `DEFENSE_UP`

Se calibran sólo:
1. magnitud;
2. cooldown.

Triggers de lab:
- HP monstruo ≤30%;
- o golpe recibido ≥20% HP máximo.

La `SURVIVAL_ACTION` consume el turno del monstruo.

Objetivo inicial: caída moderada aproximada de 8–10 pp frente a T0, sólo como target de búsqueda.

### Importante sobre V02

El ZIP V02 fue generado antes del último cambio físico del módulo de pressure, pero **no importa ni ejecuta ese módulo**. Ya declara la política correcta de natural overreach y sólo calibra la acción T1 sobre T0 congelado.

Por eso sus resultados siguen siendo válidos y **no hace falta regenerarlo**.

---

## Próximo chat — procedimiento exacto

El usuario subirá:
`LI_MONSTER_T1_SURVIVAL_GENERAL_V02_REVIEW.zip`

Hacer:
1. integridad/hashes/CRN;
2. duplicados/NaN/Inf/conteos;
3. comparar T1 contra T0 congelado;
4. auditar finalistas por especie;
5. revisar las cinco raíces y dos policies como guardrail;
6. revisar NAKED/MANDATORY/EXPECTED/HIGH_ROLL;
7. elegir un único T1 por especie;
8. preparar un único gate exhaustivo T1;
9. congelar T1 sólo si pasa;
10. abrir T2 después.

No reabrir T0. No inventar T2–T4 numéricos.

## Estado final

`T0_LI = FROZEN`  
`ADAPTIVE_OVERREACH = NATURAL_NO_HARD_STAGE_GATE`  
`T1_V02 = READY_FOR_REVIEW_RESULTS`  
`NEXT = AUDIT_T1_V02_REVIEW`
