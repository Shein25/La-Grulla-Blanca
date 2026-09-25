# CAMBIOS — Monster Combat AI v0.1

## ⚠️ Limitación de entorno — disciplina Git (sección 1 del prompt) NO ejecutada

Este laboratorio fue construido por un asistente de IA (Claude) sin acceso a
red saliente en el entorno de ejecución. Por eso **no fue posible**:

- clonar/consultar `https://github.com/Shein25/La-Grulla-Blanca`;
- verificar que la base `5812deb59cd1c133383b9af973486a702a26daf4` existe en
  `main`;
- verificar si la rama `experiment/monster-combat-ai-v0.1` ya existe;
- crear la rama nueva desde esa base exacta;
- calcular `HEAD SHA` / `PARENT SHA` / `TREE SHA` reales;
- abrir una PR DRAFT contra `main`.

En vez de inventar esos valores (lo cual violaría el principio de "elegir la
interpretación más conservadora y documentar como deuda en vez de inventar
funcionalidad"), se generó el contenido completo del laboratorio en un
entorno local aislado, exactamente con la estructura de carpetas exigida en
la sección 6 del prompt, listo para que una persona (o un agente con acceso
a git/GitHub) lo copie dentro de:

```
experimentos/monster-ai/monster-combat-ai-v0.1/
```

sobre una rama `experiment/monster-combat-ai-v0.1` creada desde el SHA base
exacto indicado, y abra la PR DRAFT correspondiente. Ningún archivo de
producción fue tocado porque, sencillamente, no se tocó el repositorio real
en absoluto.

**Esta candidata NO puede declararse `READY_FOR_EXTERNAL_AUDIT`** hasta que
alguien con acceso al repositorio complete la disciplina Git de la sección 1
y confirme los criterios de aceptación 1–4 de la sección 27 (rama correcta,
base verificable, diff aislado, producción intacta).

## Archivos entregados

```
experimentos/monster-ai/monster-combat-ai-v0.1/
├── README.md
├── CAMBIOS_v0.1.md
├── PROMPT_AGENTE_TEST.md
├── engine.mjs
├── profiles.mjs
├── fixtures.mjs
├── tests.mjs
├── stress.mjs
└── package.json
```

No se agregó ningún archivo auxiliar extra: no fue estrictamente necesario.

`experimentos/README.md` **no fue modificado** (no se tuvo acceso al
repositorio real; si se integra este laboratorio, decidir en ese momento si
amerita una entrada organizativa mínima, por sección 2 del prompt).

## Decisiones de diseño e interpretaciones conservadoras

1. **Cooldowns**: representados en `monster.cooldowns[cooldownKey]`
   (booleano). El prompt permitía snapshot o estado del monstruo; se eligió
   el monstruo por ser instancia-específica.
2. **Orden de memoria**: se asume `memory` en orden cronológico ascendente
   (el ejemplo del prompt así lo sugiere: round 2 antes que round 3). La
   ventana de profundidad es `memory.slice(-memoryDepth)`.
3. **Signo de memoria**: `EFECTIVA → +1`, `FALLIDA → -1`, otro valor → `0`.
   El prompt no fija esta regla explícitamente; se documenta aquí como
   decisión, no como deuda, porque es necesaria para que `memoryWeights`
   tenga semántica alguna.
4. **Preferencias**: clamped a `[0, 2]`, default `1` (neutral) si falta o no
   es finita, escaladas por una constante fija (`PREFERENCE_SCALE = 20`) y
   centradas en 0. Evita `NaN`/`Infinity` sin ocultar el efecto de
   preferencias extremas.
5. **`socialProfileId` desconocido**: no es un error contractual. El kernel
   no recibe el catálogo de perfiles sociales como input (no está en el
   shape de la sección 7), así que no puede validarlo contra un catálogo;
   simplemente ningún flag social se activa (comportamiento neutral). Se
   documenta como decisión conservadora, no como bug.
6. **Campos ajenos en `combat`** (p. ej. `futurePlayerAction`, GOLDEN H): se
   ignoran en vez de rechazarse. El prompt permitía ambas estrategias
   ("Preferentemente ignorarlo o rechazar shape no permitido"); se eligió
   ignorar para no acoplar el kernel a una lista blanca de campos futuros
   desconocidos hoy.
7. **`requirements`**: sólo se implementó `signalsAll` (todas las señales
   listadas deben estar activas). No se agregó `signalsAny` ni negación: no
   estaba pedido explícitamente y habría ampliado el alcance.
8. **Tie-break**: candidatos dentro de `TIE_TOLERANCE = 1e-9` se ordenan
   canónicamente por `ability.id` (orden estable, no dependiente de
   inserción) antes de aplicar `Math.floor(rng.random() * candidatos.length)`.

## Tests

Comando: `node tests.mjs` (ejecutado en el entorno local del laboratorio,
Node v22.22.2).

Resultado real de la última ejecución:

```
TOTAL: 35  PASS: 35  FAIL: 0
```

Incluye los 18 goldens obligatorios (A–R + tie-break dedicado) y 17 tests
adversariales de la sección 19.

## Stress

Comando: `node stress.mjs` (mismo entorno).

- Seeds: `1337, 1, 42, 999, 20260924`
- Decisiones por seed: 10.000 → total 50.000
- Repetición de seed `1337`: digest idéntico byte a byte (`REPEATED SEED
  MATCH: YES`)

Métricas críticas de la última ejecución real:

```
invalidSelections = 0
inputMutations = 0
executionSideEffects = 0
nondeterministicMismatches = 0
```

`STRESS RESULT: PASS`. Los digests concretos de cada seed quedan impresos
por el propio script en cada corrida (no se fijan aquí como constantes
porque dependen únicamente del código y las seeds, no de esta transcripción,
y deben poder ser recalculados de forma independiente por el auditor).

## Deudas no bloqueantes (backlog — sección 28, no resolver en v0.1)

```
D-MON-01  Bound Intent lifecycle
D-MON-02  Semantic Memory recorder desde resultados reales
D-MON-03  Short Tactical Plans 2–3 pasos
D-MON-04  Social coordination real en combates múltiples
D-MON-05  Adaptive Ecology / Species Pressure / effectiveKit resolver
D-MON-06  Adapter con motor Combate oficial
D-MON-07  Migración gradual de mobs
D-MON-08  UI de múltiples intenciones
D-MON-09  Balance de pesos canónicos (los valores actuales de perfiles y
          habilidades son de laboratorio, no balance final)
D-MON-10  Grulla y bosses
```

Deudas adicionales surgidas durante la implementación:

```
D-MON-11  Disciplina Git de la sección 1 no ejecutada (ver limitación de
          entorno arriba). Bloqueante para READY_FOR_EXTERNAL_AUDIT, no
          para la validez funcional del kernel.
D-MON-12  Conjunto de flags sociales deliberadamente pequeño (6 flags);
          ampliarlo es trabajo de una fase posterior.
D-MON-13  No se testeó con Proxies/getters exóticos como input (el prompt
          permite omitirlo si vuelve frágil el laboratorio).
D-MON-14  requirements sólo soporta signalsAll; signalsAny/negación no
          implementados por no haber sido pedidos explícitamente.
```

## Desviaciones justificadas del prompt

- No se creó rama ni PR (ver limitación de entorno).
- No se generó `REPORTE FINAL` de la sección 32 con SHAs reales; en su
  lugar, esta sección documenta honestamente qué se hizo y qué no.
- No se autoconcede ningún veredicto de auditor (`APTO_PARA_ITERAR`,
  `REQUIERE_CORRECCIONES`, `FALLO_CONCEPTUAL`); ese veredicto queda
  reservado, como exige el prompt, para el auditor externo — y aquí,
  además, para quien primero complete la disciplina Git.

No se afirma en ningún lugar de este documento que hubo auditoría externa.
No la hubo.

---

## REV2 — Correcciones puntuales (alcance limitado a 3 fixes)

Solicitadas explícitamente por el usuario, sin ampliar el alcance de v0.1 y
sin tocar producción. No se rehizo ni se rebalanceó nada fuera de lo pedido.

### Archivos modificados

```
engine.mjs   — corrección #1 (reorder invariance con jitter) y
               corrección #2 (cooldowns estrictamente booleanos)
tests.mjs    — 3 tests nuevos: 1 regresión de reorder invariance con
               jitter (seeds 1–10) + 2 regresiones de cooldowns
               estrictos (rechazo y aceptación)
stress.mjs   — corrección #3 (memoryInfluencedCases mide influencia real;
               executionSideEffects se mide con verificación por replay,
               ya no es un contador constante en 0). RNG por-escenario en
               vez de stream continuo (necesario para poder repetir una
               decisión individual sin desincronizar el resto).
README.md    — documentación de las 3 correcciones en las secciones 4, 6,
               7, 12 y 13.
CAMBIOS_v0.1.md — esta sección.
```

No se tocó `profiles.mjs`, `fixtures.mjs`, `PROMPT_AGENTE_TEST.md` ni
`package.json`.

### Corrección #1 — reorder invariance con jitter

**Causa raíz:** `chooseMonsterIntent` recorría `monster.effectiveKit` en su
orden de entrada y llamaba a `scoreAbility` (que consume `rng.random()` para
el jitter) dentro de ese mismo recorrido. Reordenar `effectiveKit`
reordenaba qué valor de la secuencia RNG recibía cada habilidad.

**Fix:** se separó el cálculo en dos fases. Fase 1 (elegibilidad, sin
consumo de RNG) recorre `effectiveKit` en el orden de entrada — es
inofensivo porque no consume aleatoriedad. Fase 2 (scoring, con consumo de
RNG para el jitter) recorre las habilidades elegibles en **orden canónico**
(`ability.id` ascendente), independiente del orden de `effectiveKit` o del
catálogo `abilities`. El desempate por empate exacto ya usaba este mismo
orden canónico; ahora todo el consumo de RNG de una decisión es
order-invariant.

**Regresión añadida:** `REV2 REGRESIÓN #1 — reorder invariance con jitter
activo (INSTINTIVO)` en `tests.mjs`. Dos habilidades sintéticas con score
determinista idéntico (mismo `base`, sin señales/memoria/social) bajo
`INSTINTIVO` (`jitter=4`); se prueban 10 seeds con `effectiveKit` en ambos
órdenes y se exige mismo `abilityId` y mismos scores.

**Verificación de que la regresión es real** (no un test que siempre pasa):
se reconstruyó temporalmente, en un directorio descartable fuera de esta
entrega, la versión de `engine.mjs` previa a esta corrección, y se corrió
sólo ese test contra ella. Resultado: **10 de 10 seeds fallan** (la
habilidad ganadora se invierte al invertir el orden de `effectiveKit`).
Contra el `engine.mjs` corregido de esta entrega, las 10 seeds pasan. El
directorio descartable no forma parte del ZIP.

### Corrección #2 — cooldowns estrictamente booleanos

**Fix:** `validateMonster` ahora exige que, si `monster.cooldowns` está
presente, cada valor sea estrictamente `=== true` o `=== false`. Cualquier
otro valor (`"false"`, `"true"`, `1`, `0`, `-1`, `[]`, `{}`, `NaN`, `null`,
`"yes"`, `"1"`, ...) lanza `ContractError` con código `INVALID_COOLDOWN`,
antes de evaluar ninguna elegibilidad. `isOnCooldown` se simplificó para
apoyarse en esa garantía (`cooldowns[key] === true`) en vez de coaccionar
con `Boolean(...)`.

**Regresiones añadidas:** `REV2 REGRESIÓN #2 — cooldowns rechaza valores no
estrictamente booleanos` (11 valores inválidos, cada uno debe lanzar
`ContractError`) y `REV2 REGRESIÓN #2 — cooldowns acepta estrictamente
true/false` (caso positivo: `true` bloquea la habilidad, `false` no).

### Corrección #3 — métricas de stress

- **`memoryInfluencedCases`**: redefinida para medir influencia real. Antes:
  `result.debug.activeMemory.length > 0` (la ventana de memoria no estaba
  vacía, sin importar si algún evento realmente pesaba en el score). Ahora:
  se cuenta sólo cuando la habilidad **efectivamente elegida** tuvo un
  término de memoria (`breakdown.memory`) distinto de cero. Efecto visible:
  la métrica bajó de ~7.000/10.000 a ~800–900/10.000 por seed — el número
  anterior sobrestimaba groseramente la influencia real de la memoria.
- **`executionSideEffects`**: antes era un contador que nunca se
  incrementaba en ningún camino de código (constante en `0` "por
  construcción", exactamente el problema señalado). Ahora, por cada
  decisión, se repite el mismo escenario con una fuente RNG fresca de
  idéntica semilla y se exige un resultado byte-idéntico (`JSON.stringify`);
  cualquier divergencia (o que la segunda corrida lance un `ContractError`
  que la primera no lanzó) incrementa la métrica. Esto exigió cambiar el
  esquema de RNG del arnés de stress: de un único stream continuo por seed a
  una semilla derivada por `(seed, índice de decisión)`, para poder repetir
  una decisión aislada sin desincronizar las siguientes.

**Verificación de que la métrica mide algo real:** se inyectó, en una copia
descartable fuera de esta entrega, una fuga de estado oculto artificial en
el kernel (un contador de llamadas a nivel de módulo que suma `+1000` al
score en llamadas pares). Al correr el stress contra esa copia envenenada,
`executionSideEffects` saltó de `0` a `49.372/50.000` y `STRESS RESULT`
cayó a `FAIL`. Contra el `engine.mjs` real de esta entrega (sin la fuga),
`executionSideEffects = 0` en las 50.000 decisiones. La copia envenenada no
forma parte del ZIP.

### Resultados tras REV2 (última corrida real, Node v22.22.2)

```
TESTS:  TOTAL 38  PASS 38  FAIL 0

STRESS: 5 seeds × 10.000 = 50.000 decisiones
  invalidSelections = 0
  inputMutations = 0
  executionSideEffects = 0
  nondeterministicMismatches = 0
  REPEATED SEED 1337 MATCH: YES
  STRESS RESULT: PASS
```

Los digests de REV2 cambian respecto a la candidata anterior porque cambió
el esquema de generación de semillas por-decisión del arnés de stress (no
la lógica del kernel); lo que se exige y se cumple es que la seed `1337`
siga dando el mismo digest consigo misma dentro de esta misma versión.

### Nuevas deudas encontradas en REV2

```
D-MON-15  El campo debug.considered se sigue reportando en el orden de
          effectiveKit (diagnóstico), mientras que el scoring interno usa
          orden canónico. Esto es intencional (ver README sección 6) pero
          significa que comparar dos `result.debug.considered` completos
          entre llamadas con effectiveKit reordenado puede diferir en
          orden de array aunque la decisión sea idéntica. No afecta
          ningún golden ni criterio de aceptación (se compara abilityId y
          scoreByAbility, no el array considered), pero se deja registrado
          por transparencia.
D-MON-16  executionSideEffects mide divergencia por replay determinista;
          no detecta necesariamente efectos colaterales que no se
          manifiesten en el valor de retorno (p. ej. una escritura a
          consola o un side effect en un objeto completamente externo al
          resultado y a los inputs snapshoteados). El kernel no tiene, por
          diseño, ninguna vía para eso (no importa I/O ni módulos con
          estado), pero se documenta como límite conceptual de la métrica.
```

### Recordatorio — disciplina Git sigue pendiente

Esta REV2 fue construida en el mismo entorno sin acceso a red que REV1 (ver
sección "Limitación de entorno" arriba). **Sigue sin materializarse ni
verificarse** la rama `experiment/monster-combat-ai-v0.1` sobre el SHA base
real, y **sigue sin abrirse** la PR draft. Esta candidata REV2 tampoco
puede declararse `READY_FOR_EXTERNAL_AUDIT` mientras eso no ocurra.
