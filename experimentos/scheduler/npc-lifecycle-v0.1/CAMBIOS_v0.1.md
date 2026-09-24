# Cambios v0.1

- Scheduler determinista basado exclusivamente en turns discretos.
- Eventos externos, vencimientos periódicos coalescidos, cooldown con bypass
  urgente exclusivo de `PLAN_INVALIDATED` y budget por tick.
- Razones pendientes con `firstTurn`, `lastTurn`, `count` y orden canónico;
  prioridad estable entre NPC y conservación de pendientes.
- Captura segura de configs, estado, eventos y opciones; rechazo de getters,
  Proxies hostiles, valores inválidos y overflow de enteros seguros.
- Fixtures sintéticos, Golden A–G, tests adversariales y stress reproducible
  de 64 NPC durante 5.000 ticks en cinco seeds.
- Sin importación ni ejecución de IA, navegación, planes o acciones reales.
