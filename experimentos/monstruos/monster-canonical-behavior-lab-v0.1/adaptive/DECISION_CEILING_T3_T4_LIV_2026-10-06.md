# SUPERSEDED — NO USAR COMO GATE\n\n> **Supersedido el 2026-10-06** por `DECISION_LIBERTAD_SOBREEXTENSION_ADAPTATIVA_2026-10-06.md`. T3/T4 siguen pensados principalmente para rejugabilidad avanzada/LIV, pero no están prohibidos antes si el jugador logra sostener presión válida.\n\n# Decisión — T3/T4 reservados a LianQi IV

**Fecha:** 2026-10-06  
**Estado:** SELECCIONADO / AUTORIDAD HUMANA

## Regla

Para el Arco 1:

- LianQi I: ceiling adaptativo máximo T1.
- LianQi II: ceiling máximo T2.
- LianQi III: ceiling máximo T2.
- LianQi IV: puede aprender T3 y T4 cuando la relación con la etapa nativa lo permita y exista nueva presión válida.

Para especies nativas de LianQi I:

```text
LI  -> T1
LII -> T2
LIII-> T2
LIV -> T4
```

T3 y T4 son contenido de rejugabilidad/endgame de Arco 1.

## Razón ecológica

T3 es el puente de contraadaptación. Debe ser difícil pero sostenible para un jugador LIV competente, porque la población necesita poder acumular presión de 70 a 90 para alcanzar T4.

Si una población alcanza T3 pero no consigue mantener presión:
- maxTierReached=T3;
- floor histórico=T2;
- puede decaer a T2.

Si alcanza T4:
- maxTierReached=T4;
- floor histórico=T3;
- T4 puede decaer, pero la población ya no baja de T3.

## Invariantes

- Subir de etapa no concede tiers automáticamente.
- Hace falta nueva presión válida.
- No se autoriza escalado universal de stats por tier.
- T1–T4 se calibran secuencialmente por especie sobre T0 READY.
