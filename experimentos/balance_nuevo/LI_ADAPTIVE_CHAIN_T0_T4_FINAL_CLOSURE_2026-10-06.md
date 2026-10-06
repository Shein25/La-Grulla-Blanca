# Cierre final — cadena adaptativa LI T0→T4

**Fecha:** 2026-10-06  
**Estado:** `ADAPTIVE_CHAIN_LI_T0_T4_HUMAN_RATIFIED_CLOSED`

## Cadena cerrada

```text
T0 NATURAL
↓
T1 SUPERVIVENCIA
↓
T2 RECONOCIMIENTO
↓
T3 CONTRAADAPTACIÓN
↓
T4 ADAPTACIÓN MADURA
```

No existe T5.

## Autoridades finales

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `experimentos/balance_nuevo/t1_li/T1_LI_FINAL_FREEZE_2026-10-06.md`
- T2: `experimentos/balance_nuevo/t2_li/T2_LI_FINAL_FREEZE_2026-10-06.md`
- T3: `experimentos/balance_nuevo/t3_li/T3_LI_FINAL_FREEZE_2026-10-06.md`
- T4: `experimentos/balance_nuevo/t4_li/T4_LI_FINAL_FREEZE_2026-10-06.md`

## Semántica global

- Adaptación pertenece a población local.
- El jugador provoca voluntariamente presión adaptativa.
- Subir de etapa no concede tiers.
- Variación individual se resuelve antes de adaptación.
- Mutante no concede tier.
- No existe escalado universal de estadísticas por tier.
- Cada especie conserva identidad.
- T1–T4 son comportamiento/arsenal adaptativo, no sacos de stats.
- LI puede sobreextenderse naturalmente hasta T4 si sostiene presión válida.
- T3/T4 están principalmente pensados para presión avanzada/rejugabilidad LIV.
- El bajo win-rate del jugador no constituye por sí solo fallo de balance.
- Definitivas quedan fuera de toda calibración de monstruos T0–T4.

## Orden operativo final

```text
species
→ T0 floor
→ independent individual variance
→ mutant taxonomy/suffix
→ population adaptive tier
→ effective adaptive kit
→ Monster AI
→ combat resolver
```

## Integración

Este cierre no activa automáticamente las capas en runtime productivo.

La integración debe:
- respetar contratos congelados;
- preservar CADENCE_COMPAT donde siga siendo autoridad;
- no reinterpretar números;
- no tocar main sin autorización;
- no crear T5;
- mantener AI decide / engine resolves.

Cualquier cambio a T0–T4 requiere reapertura humana explícita y nuevo laboratorio.
