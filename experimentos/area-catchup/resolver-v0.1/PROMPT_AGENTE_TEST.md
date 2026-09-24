# Auditoría externa: Area Catch-up Resolver v0.1

Auditá únicamente la rama `experiment/area-catchup-v0.1` contra `main@5812deb59cd1c133383b9af973486a702a26daf4`. No hagas merge ni modifiques PR #4–#7.

1. Registrá `git rev-parse HEAD`, la ancestry (`git merge-base`, padres del commit y relación con la base) y `git diff --stat 5812deb59cd1c133383b9af973486a702a26daf4..HEAD`. Confirmá que el diff sólo agrega los ocho archivos de `experimentos/area-catchup/resolver-v0.1/` y que no cambia archivos existentes.
2. Ejecutá `npm test`; informá cantidad, fallos y cobertura real de Golden A–G, timers, meters positivos/negativos/cero, límites, eventos vencidos/futuros y orden canónico.
3. Ejecutá `npm run stress -- <seed>` para `1337`, `1`, `42`, `999` y `20260924`; repetí `1337` y exigí digest idéntico. Informá `scenarios`, `catchUpCalls`, `totalElapsedTurns`, `maxElapsedTurns` y las demás métricas.
4. Inspeccioná que tests y stress usen un oracle independiente con `BigInt` para timers y meters; contrastá casos aleatorios y adversariales con overflow, rango completo safe integer, saturación y elapsed enorme.
5. Verificá hostiles: getters sin ejecución, setter-only, proxies estructurales, herencia, Symbols, extras, arrays con holes e índices accessor, IDs duplicados, targets inválidos y números no seguros.
6. Verificá inmutabilidad de inputs, desacoplamiento de outputs, determinismo y que no se ejecute `kind` de eventos.
7. Inspeccioná explícitamente código y generación de datos para confirmar ausencia de loops y estructuras proporcionales a `elapsedTurns`. Separá el costo por registros del costo de ordenamiento canónico al evaluar complejidad.

Emití evidencia concreta y **un solo veredicto exacto**:

```text
AREA_CATCHUP_V01_APTO_PARA_ITERAR
AREA_CATCHUP_V01_REQUIERE_CORRECCIONES
AREA_CATCHUP_V01_FALLO_CONCEPTUAL
```
