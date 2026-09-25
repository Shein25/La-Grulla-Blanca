# Cambios v0.3

- Agregado resolver independiente de agenda base con overrides temporales genéricos, prioridad y desempates deterministas.
- Agregada validación del snapshot inicial, intervalos `[startTurn,endTurn)`, sources explícitos y eliminación de overrides expirados.
- Agregados resúmenes por entidad y updates que distinguen cambio visible de cambio de source.
- Agregados fixtures sintéticos, Golden A–L, pruebas de hostiles y stress reproducible con oracle BigInt independiente.
- No se ejecutan `kind`, actividades, efectos ni historial intermedio; no hay integración con otros laboratorios.
