# Resultado — ver74 Structured Hooks v0.1

## Rama

`experiment/monster-ver74-structured-hooks-v0.1`

Base exacta:

`289a090b83f2e0f3652c93c870f88ec2c4256bc4`

Snapshot de origen:

`snapshot/handoff-2026-09-25-monsters-complete`

## Alcance cerrado

Se instrumentó una **copia experimental de ver74**, sin tocar `main`, sin modificar PR #18 y sin cambiar los motores congelados.

### Absorción

Punto real:

```js
const r = this.absorberGolpe(gu, dmg);
```

Hook opcional:

`juego.onPlayerAbsorptionResolved`

Payload exacto y congelado:

```js
{ round, absorbido }
```

El payload entra directamente en `absorptionOutcomeFromResolvedHit()`.

### Recuperación

`beber()` conserva sus dos posiciones históricas:

```text
[msgs, bebido]
```

y añade un tercer valor opcional sólo cuando resuelve recuperación de HP o Qi:

```js
{ vidaRecuperada, qiRecuperado }
```

Los deltas se calculan **en el punto de mutación**, incluyendo topes reales; no se parsean mensajes y ningún consumidor reconstruye el resultado leyendo HP/Qi después.

En combate, el hook opcional es:

`juego.onPlayerRecoveryResolved`

Payload exacto y congelado:

```js
{ round, vidaRecuperada, qiRecuperado }
```

La ronda se incrementa antes de emitir la recuperación, de modo que la señal y la respuesta enemiga pertenecen a la misma ronda consumida.

## Verificación dirigida

Se añadió:

`tests/ver74-structured-hooks.integration.test.mjs`

Script separado:

```text
npm run test:ver74-hooks
```

No se añadió al `npm test` histórico para no reabrir ni redefinir el cierre 107/107.

Verificación dirigida sobre HEAD:

```text
1. ver74 absorption -> adapter -> semantic memory       PASS
2. beber exact qi delta                                 PASS
3. beber exact hp capped delta                          PASS
4. recovery hook -> adapter -> semantic memory          PASS
5. recovery emission after round increment              PASS

TOTAL                                                    5/5 PASS
```

Cadena comprobada:

```text
ver74 resuelve
→ hook estructurado
→ Resolved Combat Signal Adapter v0.1
→ Semantic Memory Recorder v0.1
```

## Hallazgo preexistente — no modificado

`destilado_lunar` declara simultáneamente `purifica` y `recupera_qi`.

En ver74, `beber()` evalúa actualmente:

```text
purifica
antes que
recupera_qi
```

por lo que ese ítem entra en la rama de purificación y no fue usado para forzar artificialmente una prueba de recuperación.

La prueba usa `elixir_qi`, que sí recorre la rama real de recuperación de Qi.

**No se cambió la prioridad de efectos de `destilado_lunar`**, porque hacerlo sería un cambio de comportamiento/canon fuera del alcance de esta integración.

## Invariantes preservados

- `main` intacto.
- PR #17 y PR #18 no modificados.
- sin merge.
- CANON sin cambios.
- perfiles/traits experimentales sin cambios.
- Monster Combat AI congelada.
- `CADENCE_COMPAT` sin cambios.
- `round % tecnica.cada === 0` sin cambios.
- no se parsean logs.
- no se infiere recuperación desde HP/Qi posterior.
- no se implementó NPC↔monstruos en producción.

## Siguiente frontera

Con los hooks estructurados y su integración dirigida cerrados en copia de ver74, la siguiente frontera ya no es reconstruir Monster Combat AI.

El próximo laboratorio debe seguir aislado y resolver la frontera **NPC ↔ combate ↔ monstruo**, empezando por el contrato mínimo para que un NPC pueda participar como actor de combate sin fusionar su cerebro general con Monster Combat AI ni inventar capacidades que el executor NPC todavía no tenga.
