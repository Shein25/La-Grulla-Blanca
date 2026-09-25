# Monster Combat AI v0.1 — Deterministic Decision Kernel

**Este laboratorio no modifica ni reemplaza el combate oficial.**

Vive completamente aislado dentro de `experimentos/monster-ai/monster-combat-ai-v0.1/`
y no importa, referencia ni depende de ningún archivo de producción
(`grulla-blanca_ver*.html`, `experimentos/utility-ai/**`, `experimentos/goap/**`,
`experimentos/backups/**`, datos canónicos, ni ramas productivas).

---

## 1. Objetivo

Implementar `chooseMonsterIntent(input)`: dado un monstruo sintético, un kit
efectivo, un perfil cognitivo, preferencias tácticas, un snapshot observable
de combate, memoria semántica ya resuelta, contexto social y una fuente RNG
determinista, **seleccionar una intención elegible sin ejecutar ninguna
acción**.

> La IA decide. El motor resuelve.

v0.1 sólo construye "la IA decide".

## 2. No objetivos (explícitamente fuera de alcance)

- Adaptive Ecology, Species Pressure, grinding adaptation, tiers de población,
  desbloqueo persistente, decay ecológico, Area Activation, Catch-up.
- NPC Memory, NPC Relations, GOAP, Pathfinder, Scheduler NPC, Conversation AI,
  Behavior Tree, HTN.
- Planes tácticos de 2–3 pasos.
- Grulla real, bestiario productivo, integración con `Combate`.
- Reemplazo de `round % tecnica.cada`.
- Balance final, UI productiva.
- Ejecución de daño, mutación de HP/estados/cooldowns/memoria.

Ver también `CAMBIOS_v0.1.md` → sección de deudas (`D-MON-01` .. `D-MON-10`).

## 3. Arquitectura

```
experimentos/monster-ai/monster-combat-ai-v0.1/
├── README.md              (este archivo)
├── CAMBIOS_v0.1.md         registro de la implementación
├── PROMPT_AGENTE_TEST.md   prompt para auditor externo
├── engine.mjs              chooseMonsterIntent() — el kernel puro
├── profiles.mjs            perfiles cognitivos + perfiles sociales
├── fixtures.mjs            catálogo de habilidades sintéticas + monstruos fixture + RNG seeded
├── tests.mjs               goldens obligatorios + tests adversariales
├── stress.mjs              50.000+ decisiones, 5 seeds, digest determinista
└── package.json
```

`engine.mjs` es el único archivo que implementa lógica de decisión. No
consulta datos canónicos externos: todo lo que necesita llega por el objeto
`input` de `chooseMonsterIntent`.

## 4. API

```js
import { chooseMonsterIntent, STATUS, ContractError } from './engine.mjs';

chooseMonsterIntent({
  monster,   // instancia sintética (ver fixtures.mjs)
  profiles,  // catálogo de perfiles cognitivos (profiles.mjs → PROFILES)
  abilities, // catálogo declarativo de habilidades (fixtures.mjs → ABILITIES)
  combat,    // snapshot observable, inmutable para el kernel
  memory,    // array de eventos semánticos YA RESUELTOS (orden cronológico ascendente)
  social,    // contexto social observable (opcional; default neutral)
  rng        // { random(): number en [0,1) } — nunca Math.random()
});
```

Devuelve un objeto **deep-frozen**, JSON-friendly, con dos formas posibles:

```js
{ status: "INTENT_SELECTED", monsterId, abilityId, intent: { id, telegraph }, debug: {...} }
{ status: "NO_ELIGIBLE_INTENT", monsterId, reason: "NO_ELIGIBLE_ABILITY", debug: {...} }
```

Input contractualmente inválido (perfil inexistente, habilidad duplicada en
kit, pesos no finitos, RNG fuera de contrato, un `cooldowns[cooldownKey]`
que no sea estrictamente `true`/`false`, etc.) lanza `ContractError`
— nunca se confunde con `NO_ELIGIBLE_INTENT`, que es reservado para un
estado válido sin acciones disponibles.

## 5. Perfiles cognitivos (`profiles.mjs`)

| Perfil | memoryDepth | usesMemory | usesSocial | repetitionPenalty | jitter |
|---|---|---|---|---|---|
| INSTINTIVO | 0 | false | false | 3 | 4 |
| REACTIVO_1 | 1 | true | false | 5 | 3 |
| CAZADOR_2 | 2 | true | true | 8 | 2 |
| TACTICO_3 | 3 | true | true | 12 | 1.5 |
| MASTER_4 | 4 | true | true | 16 | 1 |

Los valores numéricos son parámetros de laboratorio, no balance productivo
(ver `D-MON-09`).

Perfiles sociales (`SOCIAL_PROFILES`): `SOLITARIO`, `TERRITORIAL`, `MANADA`,
`COLONIA`, `OPORTUNISTA`, `RED`, `REBAÑO`. En v0.1 son sólo identificadores:
el kernel deriva flags booleanos declarativos a partir de `socialProfileId` +
contexto social + señales (ver sección 9). No hay coordinación real,
refuerzos, formación espacial ni telepatía.

## 6. Scoring

```
score = base
      + preferenceModifier(preferences, intentCategory)
      + Σ signalWeights[s]      para cada señal activa en combat.signals
      + Σ memoryWeights[cat] * signo(result)   sólo dentro de la ventana de memoria permitida
      + Σ socialWeights[flag]   sólo si el perfil usesSocial y el flag social está activo
      - repetitionPenalty * ocurrencias(abilityId, recentAbilityIds)
      + jitter                 (sólo si profile.jitter > 0; consume RNG)
```

- `preferenceModifier`: preferencia clamped a `[0, 2]` (default `1` = neutral
  si falta o no es finita), multiplicada por una escala fija
  (`PREFERENCE_SCALE = 20`) y centrada en 0. Esto evita `NaN`/`Infinity` sin
  ocultar el efecto de preferencias absurdas.
- `signo(result)`: `EFECTIVA → +1`, `FALLIDA → -1`, cualquier otro valor
  (`NEUTRA`, desconocido) → `0`. Es una interpretación explícita del prompt
  (que no fija esta regla); documentada aquí y en `CAMBIOS_v0.1.md`.
- Con `jitter = 0` no se consume RNG (requisito explícito del prompt).
- Todo término se valida finito; si un peso del catálogo no es finito, el
  kernel lanza `ContractError` en la validación de `abilities`, antes de
  calcular ningún score.
- **REV2 — orden de consumo de RNG (corrección de reorder invariance):** el
  jitter se calcula recorriendo las habilidades **elegibles en orden
  canónico** (`ability.id` ascendente), nunca en el orden en que aparecen en
  `effectiveKit` ni en el orden de claves del catálogo `abilities`. Antes de
  esta corrección, reordenar `effectiveKit` podía reasignar qué valor de
  `rng.random()` recibía cada habilidad y, con jitter suficientemente grande
  frente a diferencias de score pequeñas, cambiar la intención elegida. El
  desempate por empate exacto ya usaba este mismo orden canónico (sección 8);
  ahora todo el consumo de RNG dentro de una decisión es order-invariant.

  El campo `debug.considered` sigue reportándose en el orden de
  `effectiveKit` (es diagnóstico, no participa del cálculo), así que dos
  llamadas con `effectiveKit` reordenado pueden diferir en el **orden** de
  `debug.considered` sin que eso implique una decisión distinta.

## 7. Elegibilidad

Una habilidad es elegible si:

1. su id existe en `effectiveKit`;
2. existe en el catálogo `abilities` (si no, se registra
   `UNKNOWN_ABILITY_IN_KIT` en `debug.considered` y queda fuera del ranking);
3. no está `disabled: true`;
4. no está en cooldown — representado en `monster.cooldowns[cooldownKey]`
   (booleano observable; el kernel nunca decrementa cooldowns). **REV2:**
   el contrato es estrictamente booleano: sólo `true`/`false` son válidos.
   Cualquier otro valor (`"false"`, `1`, `-1`, `[]`, `{}`, `NaN`, `null`,
   etc.) lanza `ContractError` en la validación de `monster`, antes de
   evaluar ninguna elegibilidad — nunca se interpreta silenciosamente como
   "truthy"/"falsy";
5. cumple `requirements.signalsAll` contra `combat.signals` (todas deben
   estar activas).

## 8. Determinismo

Mismo input + misma fuente RNG (misma secuencia de valores) ⇒ mismo
resultado, incluyendo `debug`. El orden de `effectiveKit` y del catálogo
`abilities` no debe cambiar la selección: los candidatos empatados (dentro
de `TIE_TOLERANCE = 1e-9`) se ordenan canónicamente por `ability.id` antes de
aplicar el desempate por RNG, de modo que el orden de inserción nunca actúa
como desempate oculto.

## 9. Memoria

`memory` es un array de eventos ya resueltos, en **orden cronológico
ascendente** (el más reciente al final) — así los entrega el ejemplo del
prompt maestro. El kernel toma la ventana `memory.slice(-memoryDepth)` según
el perfil cognitivo del monstruo. Fuera de esa ventana, ningún evento influye
en el score. Si `usesMemory = false` (INSTINTIVO), la ventana es siempre
vacía sin importar `memory`.

## 10. Social

`social` es opcional; si falta, se usa un contexto neutral
(`{ alliesAlive: 0, sameSpeciesAllies: 0, outnumbersPlayer: false }`). El
kernel deriva flags declarativos combinando `socialProfileId` + `social` +
`combat.signals`:

| Flag | Condición |
|---|---|
| `MANADA_WITH_ALLY` | `socialProfileId === 'MANADA'` y hay aliado presente |
| `COLONIA_WITH_ALLY` | `socialProfileId === 'COLONIA'` y hay aliados de la misma especie |
| `OPORTUNISTA_LOW_HP` | `socialProfileId === 'OPORTUNISTA'` y `PLAYER_LOW_HP` |
| `REBAÑO_SELF_LOW_HP` | `socialProfileId === 'REBAÑO'` y `SELF_LOW_HP` |
| `TERRITORIAL_SOLO` | `socialProfileId === 'TERRITORIAL'` y sin aliados vivos |
| `OUTNUMBER_PLAYER` | `social.outnumbersPlayer` o `signals.OUTNUMBER_PLAYER` |

Estos flags sólo influyen si `profile.usesSocial = true` y la habilidad
declara peso para ese flag en `utility.socialWeights`. `socialProfileId`
desconocido resuelve todos los flags en `false` (neutral), nunca un error
— el kernel no recibe el catálogo de perfiles sociales como input, así que
no puede ni debe rechazar un id social que no reconoce.

## 11. Fixtures

`fixtures.mjs` define un catálogo pequeño de habilidades sintéticas
(`mordida`, `acechar`, `tres_flancos`, `golpe_certero`, `retirada`,
`veneno_lento`, `estudio_tactico`, `ataque_devastador`) y cinco monstruos
fixture conceptualmente inspirados en el prompt maestro, pero sin ningún
dato canónico:

- `rata_fixture` — INSTINTIVO / COLONIA
- `serpiente_fixture` — REACTIVO_1 / SOLITARIO
- `wolf_fixture` — CAZADOR_2 / MANADA
- `devorador_fixture` — TACTICO_3 / SOLITARIO
- `mantis_fixture` — MASTER_4 / SOLITARIO

También expone `createSeededRng(seed)` (mulberry32), usado exclusivamente
por tests/stress — nunca importado por `engine.mjs`.

## 12. Ejecución de tests

```bash
npm test
# equivalente a: node tests.mjs
```

38 casos: 17 goldens obligatorios (A–R), 1 test dedicado de tie-break, 3
regresiones específicas de REV2 (reorder invariance con jitter activo +
cooldowns estrictamente booleanos, positivo y negativo) y 17 tests
adversariales (sección 19 del prompt maestro).

## 13. Ejecución de stress

```bash
npm run stress
# equivalente a: node stress.mjs
```

5 seeds (`1337, 1, 42, 999, 20260924`) × 10.000 decisiones = 50.000
decisiones, más una repetición de la seed `1337` que debe producir un
digest SHA-256 idéntico byte a byte sobre una representación canónica de
resultados (sin timestamps, sin rutas locales, claves ordenadas).

**REV2 — RNG por escenario:** cada decisión del stress usa una semilla
derivada determinísticamente de `(seed, índice de decisión)` en vez de un
único stream de RNG consumido de forma continua a lo largo de las 10.000
decisiones. Esto permite repetir una decisión individual de forma aislada
(necesario para medir `executionSideEffects` de verdad — ver más abajo) sin
afectar a las demás, y la corrida completa sigue siendo 100% reproducible a
partir de `(seed, DECISIONS_PER_SEED)`. Los digests de REV2 **no coinciden**
con los de la candidata anterior (es un cambio esperado del esquema de RNG
del arnés de stress, no del kernel); lo que importa es que la seed `1337`
siga dando el mismo digest consigo misma.

**REV2 — métricas corregidas (no se amplía ninguna otra parte del alcance):**

- `memoryInfluencedCases` ya no cuenta "la ventana de memoria no estaba
  vacía" (eso podía ser cierto sin que ningún evento pesara realmente en el
  score de la habilidad elegida). Ahora cuenta casos donde la memoria aportó
  un término **distinto de cero** al score de la habilidad efectivamente
  seleccionada — influencia real, no presencia.
- `executionSideEffects` deja de ser un contador que permanece en `0` sólo
  porque nunca se le escribía nada. Ahora, por cada decisión, se repite
  exactamente el mismo escenario con una fuente RNG fresca de idéntica
  semilla y se exige un resultado byte-idéntico; cualquier divergencia
  incrementa la métrica. Se verificó manualmente que, si se inyecta una fuga
  de estado oculto en el kernel, la métrica lo detecta de inmediato (pasa de
  `0` a decenas de miles de casos y `STRESS RESULT` cae a `FAIL`) — no es un
  contador decorativo.

## 14. Limitaciones conocidas de v0.1

- El shape de habilidades/perfiles puede refinarse en versiones futuras
  manteniendo la semántica.
- El conjunto de flags sociales es deliberadamente pequeño (ver sección 10);
  ampliarlo es trabajo de una fase posterior, no de v0.1.
- No hay generador de "requirements" más allá de `signalsAll` (lista de
  señales que deben estar activas). No se implementó `signalsAny` ni
  negación explícita: se consideró alcance extra no solicitado. Ver
  `CAMBIOS_v0.1.md`.
- No se testeó con Proxies/getters exóticos como input (el prompt permite
  omitirlo si vuelve frágil el laboratorio); ver deuda no bloqueante en
  `CAMBIOS_v0.1.md`.

## 15. Frontera futura con Adaptive Ecology

```text
Population Pressure → Adaptation Tier → unlocked abilities → effectiveKit → chooseMonsterIntent()
```

El kernel sólo recibe `effectiveKit`. No conoce kills, pressure, territorio,
decay ni tier. Esto es un requisito arquitectónico ya respetado por el
diseño de `monster.effectiveKit` como lista ya resuelta.

## 16. Qué NO se integró

- Ninguna integración con el motor de combate oficial.
- Ninguna Adaptive Ecology.
- Ningún registrador de memoria semántica desde resultados reales (la
  memoria de entrada es siempre sintética, provista por quien llama).
- Ningún ciclo `Bound Intent → player action → Combat Engine resolves →
  Semantic Memory recorder → next chooseMonsterIntent()` (documentado, no
  implementado; ver `CAMBIOS_v0.1.md`).
