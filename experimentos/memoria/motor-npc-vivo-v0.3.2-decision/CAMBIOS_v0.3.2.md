# Cambios v0.3.2

- Nueva capa `decideFromMemory`: Memory → Relations → Utility AI → mapping → GOAP.
- Mapping explícito de las nueve acciones Utility; `hablar_jugador` queda sin goal.
- Resultado trazable con cuatro estados; no hay búsqueda de otro goal tras `NO_PLAN`.
- Captura segura de NPC, contexto, world y opciones del planner; comparación de
  siete hechos equivalentes antes de decidir.
- Golden A/B/C prueban cambios de decisión y plan por recuerdos positivos y
  negativos, incluido `PLAYER_LIED` con `subject: 'superior'`.
- Tests de límites, inputs hostiles, inmutabilidad, determinismo y stress con
  seeds reproducibles.
- Todas las dependencias congeladas permanecen sin cambios.
