# Auditoría externa: Area Catch-up Agenda v0.2

Auditá sólo `experiment/area-catchup-v0.2-agenda` respecto de `main@5812deb59cd1c133383b9af973486a702a26daf4`. No hagas merge ni modifiques PR #4–#8.

1. Informá HEAD exacto, padre, ancestry (`git merge-base`) y `git diff --stat base..HEAD`. Confirmá que sólo se agregan ocho archivos en `experimentos/area-catchup/agenda-v0.2/`, sin modificar archivos existentes.
2. Ejecutá `npm test`; informá pruebas y fallos. Verificá Golden A–H, boundaries exactos `[start,end)`, ciclos completos, remainder, offsets, múltiples NPC y elapsed cercano a `MAX_SAFE_INTEGER`.
3. Ejecutá stress con seeds `1337`, `1`, `42`, `999`, `20260924`; repetí `1337` y exigí digest idéntico. Reportá todas las métricas, especialmente `fullCyclesCollapsed`, `roomChanges` y `activityChanges`.
4. Confirmá oracle independiente BigInt para fase y ciclos, sin reutilizar helpers de producción. Verificá cobertura sin gaps/overlaps, exactamente un slot por fase y consistencia del snapshot inicial.
5. Revisá canonicalización, inmutabilidad de entradas, desacoplamiento de outputs, determinismo y rechazo de getters, setter-only, proxies estructurales, holes, índices accessor, Symbols, herencia y campos extra.
6. Inspeccioná explícitamente el código para confirmar ausencia de loops o arrays proporcionales a `elapsedTurns` o `fullCyclesElapsed`, y ausencia de replay por transición. Separá costo de recorrido y ordenamiento canónico.

Emití evidencia y un solo veredicto exacto:

```text
AREA_AGENDA_V02_APTO_PARA_ITERAR
AREA_AGENDA_V02_REQUIERE_CORRECCIONES
AREA_AGENDA_V02_FALLO_CONCEPTUAL
```
