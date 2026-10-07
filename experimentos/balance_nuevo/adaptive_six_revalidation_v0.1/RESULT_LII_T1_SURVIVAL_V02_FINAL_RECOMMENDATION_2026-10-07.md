# Review LII T1 V02 — four-policy paired gate

Fecha: 2026-10-07
Estado: MECHANICALLY_PASS / HUMAN_FREEZE_RECOMMENDATION

ZIP SHA-256:
`47430ab7afb03a153b615fd3422185e12f0a91da6b9582bd1cf6178b173ed6db`

## Integridad

- 247.680 combates.
- four-policy matrix:
  - UNITARGET_FIRST
  - AOE_FIRST
  - DEFENSE_OPEN
  - ROTATION
- 0 timeouts.
- issues=[].
- manifest íntegro.
- T0 paired matrix comparable to V04.

## Nota sobre el diagnostic target

La banda HRS 55–65% fue una guía de diseño, no un hard gate.
Ningún candidato saludable llega a esa banda manteniendo:
- misma identidad T1;
- survival action consume turno;
- single next-action defensive effect.

Esto es esperable: el monstruo sacrifica un ataque para preparar supervivencia.

No se recomienda rediseñar T1 sólo para forzar una win-rate.

## Sapo — recomendación

Candidate:
- MITIGATE_NEXT 90%
- cooldown 3
- candidate `f185d92fd600e410`

HRS:
- T0: 73,28125%
- T1: 72,96875%
- delta: -0,3125 pp

All profiles mean:
- delta win: -1,8359 pp
- HP pressure: +1,106 pp aprox.
- monster damage: +0,441
- rounds: +1,339
- adaptation procs: 1,514

Por gear:
- CARRY: 50,625% → 47,2266% (-3,3984 pp)
- EXPECTED: 72,8906% → 71,0938% (-1,7969 pp)
- HRS: 73,2813% → 72,9688% (-0,3125 pp)

Root spread HRS, promediando policies:
- T0: 10,94 pp
- T1: 12,11 pp
No hay cliff nuevo material por raíz.

Lectura:
90% parece alto en magnitud nominal, pero sólo afecta el siguiente paquete DIRECTO conectado, no DoT, y la activación consume turno. Es el primer candidato que compensa consistentemente el coste del turno sin rediseñar identidad.

## Escarabajo — recomendación

Plateau CD3:
+12, +14, +16, +18, +20 producen prácticamente el mismo outcome agregado.

Preferir el menor valor del plateau:
- DEFENSE_UP +12
- cooldown 3
- candidate `339ed6d4cbab4e50`

HRS:
- T0: 69,6484%
- T1: 70,3516%
- delta: +0,7031 pp

All profiles mean:
- delta win: +0,0521 pp
- rounds: +1,831 aprox.
- adaptation procs: 1,789

Por gear:
- CARRY: 34,5703% → 34,4922% (-0,0781 pp)
- EXPECTED: 85,1562% → 84,6875% (-0,4687 pp)
- HRS: 69,6484% → 70,3516% (+0,7031 pp)

Root spread HRS, promediando policies:
- T0: 17,38 pp
- T1: ~15–16 pp según plateau
No genera polarización nueva.

El histórico +2/CD5 es claramente demasiado débil:
- HRS delta +7,3828 pp
- all profiles delta +6,3021 pp

## Auditor diagnostic issue

El runner marca `catastrophic_policy_spread=true` porque usa el mínimo/máximo de contextos root×policy crudos.
Ese flag no debe usarse como bloqueo:
- T0 ya contiene gran sensibilidad por policy;
- la metodología LI exige revisar root spread después de promediar policies y comparar contra T0 pareado;
- bajo esa lectura los finalistas no introducen un cliff nuevo material.

## Recomendación de freeze humano

Sapo:
- T1 MITIGATE_NEXT 90%
- CD3
- trigger HP<=30% OR hit>=20% maxHP
- consumes monster turn

Escarabajo:
- T1 DEFENSE_UP +12
- CD3
- mismo trigger
- consumes monster turn

No freeze automático.
Si el humano aprueba, cerrar T1 LII y abrir T2 secuencialmente.
