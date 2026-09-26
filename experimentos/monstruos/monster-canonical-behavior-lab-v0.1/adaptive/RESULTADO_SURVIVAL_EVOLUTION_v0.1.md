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

## Resultado mecánico

Se compararon las cuatro familias usando la fórmula de impacto actual de ver74, sin inventar otra resolución.

Representantes:

- Rata: `EVADE_NEXT +25`;
- Centinela: `DEFENSE_UP +4`;
- Eco: `MITIGATE_NEXT 35%`;
- Guardián: `ABSORB_RESERVE 5 / reserva 10`.

Daño esperado evitado en el siguiente ataque:

```text
                         EVADE   DEFENSE   MITIGATE   ABSORB
grande/impreciso          5.00      4.00       4.55      3.25
medio/equilibrado         2.50      2.00       2.25      3.75
pequeño/preciso           1.00      0.80       0.95      3.80
grande/preciso            5.00      4.00       6.65      4.75
```

Por tanto las cuatro familias tienen nichos diferentes:

- esquiva castiga ataques grandes con posibilidad real de fallar;
- defensa plana crea postura/armadura sin consumir daño después del impacto;
- absorción protege especialmente de golpes pequeños/medios y repetidos;
- mitigación porcentual escala con golpes grandes que probablemente conectarán.

## Ajuste de absorción

El primer borrador usaba reservas demasiado altas.

Se redujo Evolución I a:

```text
Devorador       3 / reserva 6
Sapo Caldera    4 / reserva 8
Escarabajo      4 / reserva 8
Rey Escarabajo  5 / reserva 10
Guardián Coral  5 / reserva 10
```

Así la absorción conserva su identidad sin dominar también los golpes grandes.

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
