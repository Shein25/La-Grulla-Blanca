# BACKUP MAESTRO DE CONTINUIDAD — CORTE MOTOR DE COMBATE

Fecha: 2026-09-25
Motivo: corte manual por límite de conversación.
Proyecto: La Grulla Blanca

## 1. Regla de continuidad

Este archivo es un handoff operativo. Al retomar:

- no reconstruir desde memoria aproximada;
- verificar GitHub en vivo antes de afirmar HEAD/PR/branch;
- no tocar main salvo orden explícita;
- no reabrir snapshots v0.1 ya cerrados;
- mantener producción y experimentos aislados;
- no mezclar Adaptive Ecology, Monster Combat AI y Autonomous NPC Loop salvo en un laboratorio de integración explícito.

## 2. Estado Git verificado en este corte

```text
repo = Shein25/La-Grulla-Blanca

main =
de3a7593dc59120f5940b3589bc42ed6e500ba9b

implement/3c6-prologo-m01-m07 =
748bd4480e37fd2523fa833081b20522b9724dab

experiment/monster-combat-ai-v0.1 =
aecbbcac1f2243dad16e2f881fdc6b683debe616

experiment/npc-autonomous-loop-v0.1 =
ddff6e7b386b401ae1e471cbfe05f0bd113bb866

experiment/monster-ecology-adaptation-v0.1 =
NO EXISTE
```

Producción 3C.6 continúa separada del main experimental.

## 3. Monster Combat AI v0.1 — CERRADO

PR #13 fue auditado y mergeado.

```text
HEAD auditado =
aecbbcac1f2243dad16e2f881fdc6b683debe616

merge commit =
df439ad789e668c526666fa3955deb5b2fe3e8d4

veredicto externo =
MONSTER_COMBAT_AI_V01_APTO_PARA_ITERAR
```

Evidencia:

- 38/38 tests;
- 50.000 decisiones stress;
- métricas críticas 0;
- auditoría independiente adicional 9.215 checks;
- auditoría Claude: 5.200 fuzz coherente, 0 bloqueantes.

Regla: v0.1 está congelada. No modificarla silenciosamente.

Principio:

> Monster Combat AI decide. El motor de combate resuelve.

## 4. Autonomous NPC Loop v0.1 — CERRADO

PR #12 fue auditado y mergeado.

```text
HEAD auditado =
ddff6e7b386b401ae1e471cbfe05f0bd113bb866

TREE =
a6f78d4a162650fc755e5fbe599084a5fef38237

merge commit =
de3a7593dc59120f5940b3589bc42ed6e500ba9b

veredicto externo =
NPC_AUTONOMOUS_LOOP_V01_APTO_PARA_ITERAR
```

Evidencia:

- 107/107 tests;
- stress oficial PASS;
- 14.400 ticks / ~44.000 dispatches fuzz independiente;
- 0 bloqueantes.

Deudas preservadas:

1. churn PERIODIC + DECISION_GOAL_ALREADY_SATISFIED;
2. riesgo de starvation semántica si dutyMode fijo sigue dominando con goal satisfecho;
3. test oficial faltante con Decision Pipeline stub para el guard de plan vacío;
4. higiene de Memory con claves extra / __proto__.

La deuda de starvation debe resolverse antes de producción real.

## 5. Adaptive Ecology v0.1 — ACTIVO / PENDIENTE REV2

Diseño FINAL congelado y apto para implementar.

Cadena:

```text
SPECIES_KILLED
→ pressure
→ decay
→ tier
→ activeAdaptations
→ effectiveKit
```

REV1 local:

- 62/62 tests PASS;
- 100.000 transiciones stress;
- digest determinista;
- 20.000 casos contra oráculo, 0 mismatches;
- pero NO aprobada por hardening.

Correcciones exigidas en REV2:

1. knownAbilityIds obligatorio y estricto;
2. recentEventIds.length <= dedupWindowSize;
3. snapshots internos para cerrar Proxy/TOCTOU;
4. campos requeridos deben ser own properties;
5. coherencia de política/test para recentEventIds duplicados;
6. nondeterministicMismatches debe medirse realmente.

Paquete listo:

`ADAPTIVE_ECOLOGY_v0.1_REV2_PARA_CLAUDE_OFFLINE.zip`

No existe todavía rama Git de implementación.

## 6. Decisión arquitectónica — repertorio de combate multifunción

effectiveKit NO debe significar sólo ataques.

Puede contener:

- ofensiva directa;
- AOE/multiimpacto;
- defensa;
- evasión;
- absorción;
- control;
- recuperación;
- preparación/buffs;
- buffs de ataque;
- buffs de crítico;
- buffs de daño crítico;
- habilidades híbridas ofensiva+defensa.

Regla:

- Ecology habilita repertorio;
- Monster AI elige;
- Combat Engine ejecuta/resuelve.

Ecology NO hace stat scaling oculto.

## 7. Auditoría inicial del motor de combate — PUNTO EXACTO ACTUAL

Fuente productiva verificada:

```text
branch =
implement/3c6-prologo-m01-m07

HEAD =
748bd4480e37fd2523fa833081b20522b9724dab

file =
grulla-blanca_ver75.html

blob =
1c897be6ddf3d18436a043fab0c848ef7f3fb18c
```

Se comparó `class Combate` de ver74/main con ver75/3C.6.

Resultado:

- 641 líneas en ambos bloques;
- lógica semánticamente igual;
- sólo diferencias de whitespace;
- por tanto el análisis hecho sobre ver74 aplica también a ver75.

### 7.1 Lo que el motor YA soporta de verdad para el jugador

- ataque normal;
- técnicas ofensivas single-target;
- AOE;
- ataque/precisión;
- critMin;
- critMult;
- daño;
- quemadura;
- debuff de ataque;
- control/atadura;
- evasión temporal;
- defensa plana temporal;
- absorción con reserva;
- DEFENDER porcentual por 2 impactos reales;
- afinidad/concordancia elemental;
- estados independientes y reemplazo por categoría.

Roles actuales de técnica:

```text
ofensiva
fortificacion
guardia
esquiva
control
```

Estados declarados:

```text
esquiva
defensa
guardia
dano
ataque
tenacidad
quemadura
veneno
debil
atadura
```

### 7.2 Distinción crítica encontrada

No confundir “estado declarado/UI” con “efecto conectado al pipeline”.

`dano` y `ataque` existen como categorías preparadas, pero hoy NO están conectados como buffs temporales genéricos en la resolución de combate.

### 7.3 Enemigos actuales

Contrato de `mob.tecnica` observado:

```js
{
  name,
  cada,
  ataque?,
  daño?,
  veneno?,
  quemadura?,
  drenaQi?
}
```

`respuestaEnemigos()`:

- cada mob responde;
- puede desplegar una técnica periódica;
- técnica puede modificar ataque/daño del golpe de ese turno;
- puede aplicar veneno/quemadura;
- puede drenar qi;
- usa el mismo `atacar()` base contra el jugador;
- jugador sí aporta evasión/defensa/guardia al pipeline defensivo.

### 7.4 Asimetría crítica a resolver

`aplicarAMob()` puede almacenar estados genéricos en enemigos, PERO actualmente el pipeline de ataque contra un mob no consulta estados propios de mob para:

- defensa;
- evasión;
- guardia/absorción;
- ataque;
- dano.

Por tanto:

> guardar un estado defensivo en el mob NO significa todavía que tenga efecto real.

Esto debe guiar el futuro Combat Ability Contract.

## 8. Próxima tarea al retomar

Continuar la auditoría del motor de combate y crear:

`Combat Ability Contract v0.1`

Sin tocar producción todavía.

Debe separar:

1. capacidades que ya existen y son reutilizables;
2. capacidades declaradas pero aún no conectadas;
3. capacidades que requieren adapter experimental;
4. responsabilidades de Monster AI vs Combat Engine.

Objetivo del contrato:

```text
Monster Combat AI
→ abilityId / intent
→ adapter de habilidad
→ Combat Engine existente
→ impacto / daño / crítico / evasión / defensa / absorción / estado
→ resultado
```

Familias mínimas a cubrir:

- OFFENSE;
- DEFENSE;
- EVASION;
- ABSORPTION;
- CONTROL;
- BUFF_ATTACK;
- BUFF_CRIT_CHANCE;
- BUFF_CRIT_DAMAGE;
- HYBRID.

No diseñar números finales todavía.

## 9. Orden recomendado de trabajo

En paralelo:

A. Esperar/recibir Adaptive Ecology REV2 de Claude.
B. Continuar Combat Ability Contract v0.1.

Después:

C. cerrar Ecology;
D. laboratorio Adaptive Ecology × Monster Combat AI;
E. Bound Intent Lifecycle;
F. adapter controlado al combate real.

## 10. Regla de seguridad

No merge automático.
No tocar main sin orden explícita.
No tocar `implement/3c6-prologo-m01-m07` durante la auditoría de combate.
No reescribir snapshots v0.1 ya cerrados.
