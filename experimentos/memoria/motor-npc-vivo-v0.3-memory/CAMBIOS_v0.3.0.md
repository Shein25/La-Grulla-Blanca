# Cambios — Motor NPC Vivo v0.3.0

## Nueva familia experimental

Se crea `experimentos/memoria/` para aislar la prueba de memoria de Utility AI y GOAP.

## Núcleo

Se incorpora `memory.mjs` con:

- `createMemoryState()`;
- `recordMemory()`;
- `recallMemory()`;
- `pruneMemory()`;
- `forgetMemory()`;
- `memoryStats()`.

## Decisiones deliberadas

- memoria semántica por `key`, no log cronológico infinito;
- upsert en lugar de duplicación;
- reloj monotónico global por estado de memoria;
- capacidad por defecto 32;
- expiración explícita, sin decay automático;
- orden de expulsión determinista;
- valores recordados limitados a primitivos finitos;
- inputs no mutados;
- eventos con accessors o herencia no plana rechazados;
- índices accessor en `memory.entries` rechazados;
- overflow de `count` rechazado antes de incrementar.

## No integración todavía

v0.3.0 no modifica:

- pesos de Utility AI;
- relaciones del NPC;
- GOAP;
- Executor;
- fixtures GOAP/Utility existentes.

La integración memoria → decisión se pospone hasta validar este núcleo.
