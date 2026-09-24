# Cambios v0.3.1 — memoria → relaciones derivadas

- Añade `deriveRelations(baseRelations, memory, currentTurn)` como capa pura que usa `recallMemory()` de v0.3.0 sin modificar esa versión.
- Captura y valida las seis relaciones base mediante descriptores propios de datos, sin ejecutar getters ni releer valores externos durante el cálculo.
- Aplica únicamente `PLAYER_HELPED_ME=true` y `PLAYER_LIED=true`, con factor `importance × confidence / 10.000`, agregación determinista y clamp final.
- Devuelve relaciones, deltas previos al clamp y trazas explicativas de recuerdos aplicados e ignorados.
- Añade pruebas de reglas, expiración, orden, inmutabilidad, idempotencia, hardening y un stress sintético reproducible de 32 NPC por 1.000 rondas.
- No conecta la derivación a Utility AI, GOAP o Executor. No usa NPC ni topología canónicos.

**Límite deliberado:** `count` no da bonus, no hay decay y las relaciones derivadas no se convierten automáticamente en relaciones base.
