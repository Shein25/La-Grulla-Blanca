# Lin Yue — baseline de compañero / LAB v0.1

## Objetivo

Primer compañero canónico probado con memoria social real del stack:

```text
Memory
→ Relation Deriver
→ Utility
→ GOAP
→ Execution Session
```

## Canon relevante

- aspirante — enlace territorial / rutas;
- movilidad RUTA;
- LI: Patio Exterior + Marcial;
- LII/LIII: expansión progresiva hacia rutas y sectores más amplios;
- M16: anclada en RUTAS junto a Jiang Rui/Ren Bo;
- M16: va a RUTAS por iniciativa propia salvo circunstancia narrativa distinta;
- epílogo: COORDINADORA_TERRITORIAL.

## Perfil experimental

Traits y relación base son:

`EXPERIMENTAL_NON_CANONICAL`

Se calibraron para colocar `hablar_jugador` y `ayudar_jugador` cerca de una frontera de decisión. No describen la personalidad canónica de Lin Yue.

## Escenario A — sin memoria

Mismo contexto social:

- jugador presente;
- jugador pide ayuda;
- deber bajo;
- peligro bajo/moderado.

Resultado esperado:

```text
hablar_jugador
```

Como esa acción no tiene goal GOAP, el Autonomous Loop devuelve `UTILITY_ACTION_UNMAPPED` y no crea una session.

## Escenario B — memoria PLAYER_HELPED_ME

Se registra exclusivamente mediante Memory:

```text
PLAYER_HELPED_ME
importance = 100
confidence = 100
```

Relation Deriver debe producir:

```text
afinidad   40 → 52
confianza  40 → 50
deuda       0 → 8
```

sin modificar las relaciones base del NPC.

Con el mismo contexto, la nueva relación derivada debe cambiar la decisión a:

```text
ayudar_jugador
→ HELP_PLAYER
→ [ir_jugador, ayudar_jugador]
```

y el plan se ejecuta en dispatches posteriores hasta `playerHelped=true`.

## Gap físico M16

El canon exige que Lin Yue vaya a RUTAS por iniciativa propia en M16.

El GOAP actual opera con ubicaciones simbólicas `puesto/jugador/superior` y no contiene las rooms canónicas ni pathfinding.

Por tanto:

`SELF_INITIATED_ROUTE_TRAVEL_TO_RUTAS = CANONICAL_REQUIREMENT_CAPABILITY_GAP_PHYSICAL_NAVIGATION`

Esto no es un fallo de Lin Yue ni se rellena inventando movimiento en el test.

## Estado

`LIN_YUE_COMPANION_BASELINE: PENDING_RUNTIME_CONFIRMATION`
