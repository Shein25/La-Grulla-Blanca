# Cambios v0.1

- Agregada session de ejecución para un objetivo ya elegido, con captura defensiva de datos externos y contadores seguros.
- Agregado coordinador que reutiliza `executeNext`, `planGOAP` y `factsMatch` del GOAP estable; una llamada aplica un paso o intenta replanning.
- Separados goal obsoleto, goal alcanzado externamente, `NO_PLAN` y planificación inconclusa; el replan conserva el mismo goal.
- Agregados fixtures sintéticos, Golden A–L, pruebas hostiles y stress reproducible con perturbaciones entre llamadas y oracle BFS independiente.
- No se incorporan Utility, Scheduler, Pathfinder ni acciones con duración.
