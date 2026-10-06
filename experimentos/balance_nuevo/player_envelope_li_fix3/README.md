# Player Power Envelope LI — FIX3

FIX3 responde al `AUDIT_FAIL_BLOCKING` de Astra. No reutiliza checkpoints FIX2.

## Cambios principales
- fuente engine/guard sincronizada al soporte `resource_model=NONE` de `c7b87b84...`;
- patch de campaña G04: Tierra aplica +10% sólo al HP estructural y luego suma HP plano de equipo;
- recipe hash real ligado a sources/runner/reps/max_rounds/seeds;
- semillas SHA-256 de 128 bits por réplica, CRN cross-root declarado;
- SQLite `DELETE`, DB contractual y resume elegido por DB validada, no por `progress_score`;
- gear signatures se recomputan siempre;
- expected-set + batch ledger bidireccional;
- selección R128 determinista y hashada;
- REVIEW idempotente con panel R12 completo y provenance.

Runner SHA-256: `80abdd30445758a382d05e832c158649dfa5aed604cb5e3c0eb2d9d25e5b4e21`
Técnicas SHA-256: `912b7824eff9149909ca21b9ad6290c6c82b1e1ea31867da1185c32df383d187`
Package local FIX3 SHA-256: `0d3615fa8902b136fe15e03a5a0108e41b85c3d1f13aa38f648b2ed3efbaa94d`

Primera corrida: Internet activado. Después, una Save Version FIX3 compatible puede aportar las fuentes y la DB.
