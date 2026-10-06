# T1 Survival General V02 — checkpoint

**Fecha:** 2026-10-06  
**Estado:** READY_FOR_KAGGLE_SEARCH

## Autoridad

La etapa del jugador es una banda esperada de capacidad, **no un gate duro**.

`adaptive_overreach_policy = ALLOWED_NATURAL_LIMIT_BY_COMBAT_AND_DECAY`

El jugador puede forzar una población más allá de la banda esperada si logra seguir produciendo presión válida. El muro natural es la dificultad real del combate y el decay.

Bandas orientativas:
- LI: T0/T1 esperado.
- LII: T1/T2 esperado.
- LIII: T2 esperado; sobreextensión posible.
- LIV: T3/T4 como rejugabilidad/endgame previsto.

## T0 fuente

Commit de registry/autoridad: `0dd67d391191c00521f2a760736caa2245944c6c`.

## T1

- Rata: Reflejo de Madriguera / EVADE_NEXT.
- Serpiente: Muda del Cauce / EVADE_NEXT.
- Avispa: Quiebro de Jade / EVADE_NEXT.
- Mono: Salto del Ladrón / EVADE_NEXT.
- Lobo: Paso de la Cola Vigilante / DEFENSE_UP.

Se calibran sólo magnitud y cooldown.
Triggers de laboratorio: HP <=30% o golpe >=20% HP máximo.

## Artefacto

`KAGGLE_LI_MONSTER_T1_SURVIVAL_GENERAL_V02.zip`

SHA-256: `08feef921d84b5c612dde8baf7110b831649971f352ba75a95d09197758ed93a`

Runner SHA-256: `46e81974468ba915b724962694a6760ab2ae617b1d8c0663e4a7a20f67aa0f48`

La V01 queda obsoleta porque contenía la interpretación anterior de ceiling duro.
