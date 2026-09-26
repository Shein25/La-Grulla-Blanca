# Resultado — Monster Adaptive Survival v0.1 · cuatro familias defensivas

## Estado

`EXPERIMENTAL_NON_CANONICAL_SURVIVAL_V01_FOUR_DEFENSE_FAMILIES`

Rama:

`experiment/monster-adaptive-survival-lab-v0.1`

No toca `main`, PR #17 ni PR #18.

## Cambio respecto al primer balance

La Evolución I ya no reduce “defensa” a dos efectos.

Ahora existen cuatro contratos experimentales:

```text
EVADE_NEXT
DEFENSE_UP
ABSORB_RESERVE
MITIGATE_NEXT
```

La asignación depende de anatomía, elemento, descripción y comportamiento de cada monstruo.

## Cobertura

Los 18 combatientes tienen una y sólo una política de supervivencia:

```text
ESQUIVA       7
DEFENSA       3
MITIGACIÓN    3
ABSORCIÓN     5
```

El muñeco de práctica queda fuera.

## Resultado conductual

Validación dirigida sobre el HEAD del laboratorio:

```text
17/17 PASS
```

Se preservó el balance de decisión:

```text
sano                              0.0 % defensa
HP bajo                          49.5 % defensa
golpe fuerte, HP sano             0.0 % defensa
HP bajo + golpe fuerte          100.0 % defensa
defensa en cooldown               0.0 % defensa
violaciones CADENCE_COMPAT            0
```

El 100% crítico no produce spam porque la defensa consume acción y entra en cooldown.

## Resultado mecánico — referencia actualizada

La tabla sintética del primer prototipo queda **retirada como evidencia de balance**.

Se conserva únicamente como smoke test de que las cuatro mecánicas producen efectos distintos.

El balance vigente se calcula contra el arsenal real de ver74 en:

`adaptive/ANALISIS_ARSENAL_JUGADOR_DEFENSAS_E1_v0.1.md`

Benchmark reproducible:

`npm run benchmark:player-arsenal`

Hallazgos principales:

```text
Arco I objetivo: LianQi IV
ramas disponibles: 1–2
artes raíz ofensivas: Palma / Filo / Látigo
qi máximo: 110
equipo de ataque máximo actual: +2
```

La precisión de ramas puede sumar +7 ataque ya en Arco I, por lo que ESQUIVA y DEFENSA tienen counters reales.

Mitigación 30–35% de un golpe queda por debajo de la acción DEFENDER del jugador.

Absorción debe medirse por reserva total respecto del HP:

```text
Devorador        6 / 38 = 15,8%
Sapo Caldera     8 / 34 = 23,5%
Escarabajo       8 / 21 = 38,1%
Rey Escarabajo  10 / 38 = 26,3%
Guardián Coral  10 / 52 = 19,2%
```

Por ahora **no se modifica ningún número** sólo por porcentaje de golpe evitado.

El próximo cierre de balance debe incluir el coste real de que el monstruo pierda su ataque al defender y el consumo completo de la reserva.

## Ataque-only

Los dos monstruos sin técnica canónica continúan evolucionando hacia supervivencia:

```text
rata_qi
BASIC_ATTACK
+ Reflejo de Madriguera / EVADE_NEXT

eco_caido
BASIC_ATTACK
+ Guardia del Último Ensayo / MITIGATE_NEXT
```

No reciben ofensiva inventada.

## Gradiente de inteligencia preservado

Cuando ambos lados están bajos de HP y no hubo un golpe fuerte reciente:

```text
REACTIVO_1  — rata_qi          ~22%
CAZADOR_2   — serpiente_qi     ~13%
TACTICO_3   — lobo_espiritual   ~5%
MASTER_4    — guardian_coral     0%
```

Los perfiles más avanzados asumen más riesgo de rematar al jugador. Si además acaban de sufrir un golpe fuerte, vuelven a priorizar supervivencia.

## Gaps reales

### Persistencia adaptativa
Aún no existe almacenamiento productivo de `survivalXp/evolutionStage`.

### Executor defensivo
ver74 todavía no ejecuta los cuatro intents nuevos.

El siguiente paso mínimo debe definir un bridge/executor capaz de aplicar:

```text
EVADE_NEXT
DEFENSE_UP
ABSORB_RESERVE
MITIGATE_NEXT
```

sin cambiar el canon, sin romper `CADENCE_COMPAT` y reutilizando las mecánicas existentes siempre que ya haya una equivalente.
