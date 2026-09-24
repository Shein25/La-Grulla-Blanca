# Cambios v0.1

- Pathfinder físico entre rooms sintéticas con BFS determinista y coste uniforme.
- Validación fuerte de grafo dirigido y captura segura mediante descriptores.
- Soporte de `norte`, `este`, `sur`, `oeste`, `arriba`, `abajo`, desempate fijo,
  ciclos, rutas unidireccionales y bloqueos temporales por búsqueda.
- Estados `ROUTE_FOUND`, `ALREADY_THERE`, `NO_ROUTE`, `SEARCH_LIMIT` con límite
  explícito `maxVisited`.
- Fixtures de laboratorio, tests adversariales, oracle independiente de rutas
  mínimas y stress determinista con cinco seeds.
- Sin integración con GOAP, Utility AI, Executor ni mapa real.
