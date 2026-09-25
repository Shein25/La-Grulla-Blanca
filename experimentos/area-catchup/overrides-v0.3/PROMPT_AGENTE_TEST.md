# Auditoría externa: Area Catch-up Overrides v0.3

Auditá únicamente `experiment/area-catchup-v0.3-overrides` contra `main@5812deb59cd1c133383b9af973486a702a26daf4`. No hagas merge ni modifiques PR #4–#9.

1. Registrá HEAD exacto, padre, base y ancestry (`git merge-base`). Revisá `git diff --stat base..HEAD`: sólo ocho archivos nuevos en `experimentos/area-catchup/overrides-v0.3/`, cero archivos existentes modificados y status limpio.
2. Ejecutá `npm test`; informá cantidad y fallos. Comprobá Golden A–L, boundaries exactos de inicio y fin, prioridad, desempates, override indefinido, expiración, futuro, shadowing y cambio de source sin cambio visible.
3. Ejecutá stress con seeds `1337`, `1`, `42`, `999`, `20260924`; repetí `1337` y exigí digest idéntico. Informá todas las métricas, en especial `shadowedOverrides`, `expiredOverrides`, `sourceChanges` y `fullCyclesCollapsed`.
4. Confirmá que tests y stress usan oracle independiente con BigInt para fase, slot base y ciclos, más selección separada de overrides activos por prioridad, inicio e ID. Comprobá huge elapsed cercano a `MAX_SAFE_INTEGER`.
5. Comprobá snapshot coherente, rechazo de finitos stale, cobertura de slots, orden canónico, inmutabilidad, desacoplamiento, determinismo y hostiles en todos los niveles: getters, setter-only, proxies (`get`, `getPrototypeOf`, `ownKeys`, `getOwnPropertyDescriptor`), herencia, Symbols, holes, índices accessor y extras.
6. Inspeccioná explícitamente ausencia de loops o arrays proporcionales a `elapsedTurns` o `fullCyclesElapsed`, y ausencia de replay por turn, ciclo o boundary. Verificá que `kind` y `activity` no ejecuten efectos.

Emití evidencia concreta y **un solo veredicto exacto**:

```text
AREA_OVERRIDES_V03_APTO_PARA_ITERAR
AREA_OVERRIDES_V03_REQUIERE_CORRECCIONES
AREA_OVERRIDES_V03_FALLO_CONCEPTUAL
```
