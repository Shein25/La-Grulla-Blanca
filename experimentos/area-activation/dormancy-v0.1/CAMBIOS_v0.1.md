# Cambios v0.1

- Activación determinista de sólo el área actual del jugador, con estados
  `INITIAL_ACTIVATION`, `AREA_SWITCHED` y `ALREADY_ACTIVE`.
- Dormancia derivada por resta entre turn actual y `lastSimulatedTurn`; un
  request de catch-up por reactivación, sin simular turns omitidos.
- Transición atómica como estado candidato; sólo áreas origen y destino se
  sincronizan y `activeAreaId` es la única fuente de verdad.
- Captura segura de configs y state mediante descriptores; validación de
  enteros seguros, clocks, IDs, estructura exacta e inputs hostiles.
- Fixtures sintéticos, Golden A–G, tests adversariales y stress con oracle
  independiente de 32 áreas y 20.000 updates para cinco seeds.
- Sin importación de Scheduler u otros motores ni Catch-up Resolver real.
