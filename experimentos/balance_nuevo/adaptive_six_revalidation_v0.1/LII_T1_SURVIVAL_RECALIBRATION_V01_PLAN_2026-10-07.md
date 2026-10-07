# LII T1 Survival Recalibration V01 — Sapo + Escarabajo

Fecha: 2026-10-07
Estado: READY_FOR_COLAB

## Fuente T0 congelada

Manifest:
`experimentos/balance_nuevo/t0_lii/T0_LII_FREEZE_MANIFEST_2026-10-07.json`

Registry freeze commit:
`80a3a77cc84178cd5cbde887df71f4c38f72664a`

Variance authority commit:
`0eb1cdb2e7bcaf6b70826f344370ad48421bbbb1`

## Semántica T1

Se reutiliza exactamente la semántica del runner LI T1 V02:

- trigger: HP <=30% OR golpe recibido >=20% HP máximo;
- survival action consume el turno del monstruo;
- sólo activa si cooldown <=0 y no hay survival activo;
- cooldown se resuelve por el lifecycle del motor;
- no T2/T3/T4.

### Sapo — MITIGATE_NEXT

Identidad histórica:
`MITIGATE_NEXT`.

Semántica del motor:
- reduce el siguiente paquete DIRECTO conectado;
- reducción ocurre antes de DEF plana;
- persiste si el ataque falla;
- se consume al conectar.

Grid:
- reducción: 5, 10, 15, 20, 25, 30, 35, 40%;
- cooldown: 3, 4, 5, 6.

Histórico:
- 10%, CD5.

### Escarabajo — DEFENSE_UP

Identidad histórica:
`DEFENSE_UP`.

Semántica del motor:
- añade DEF al siguiente player action;
- se consume después de esa acción, conecte o falle;
- usa pipeline normal de penetración/DEF.

Grid:
- DEF bonus: +1, +2, +3, +4, +5, +6, +8, +10;
- cooldown: 3, 4, 5, 6.

Histórico:
- +2 DEF, CD5.

## Objetivo de diseño

T0 HRS LII quedó aproximadamente:
- Sapo: 73,34% player-win.
- Escarabajo: 69,98%.

T1 debe tener espacio real de dificultad sin producir un cliff.

Banda diagnóstica HRS:
- 55–65% player-win;
- centro orientativo ~60%.

No es canon automático ni regla universal.

Hard guards:
- T1 no debe ser >2 pp más fácil que T0 pareado;
- 0 timeout;
- identidad debe proc;
- no root/policy cliff extremo;
- no tocar T0.

## Matriz

SCREEN:
- 64 candidatos totales;
- 3 gear contexts;
- 5 roots;
- 2 policies;
- R24.

46.080 fights.

CONFIRM:
- top 6 por especie;
- 3 gear contexts;
- 5 roots;
- 2 policies;
- R128.

46.080 fights.

T0 paired controls:
- 2 especies;
- 3 gear contexts;
- 5 roots;
- 2 policies;
- R128.

7.680 fights.

Total:
**99.840 combates**.

## Gear contexts

- CARRY_OVER_FLOOR = HIGH_ROLL_STRESS LI.
- EXPECTED_STAGE = EXPECTED_STAGE LII.
- HIGH_ROLL_STRESS = HIGH_ROLL_STRESS LII.

## Salida

`LII_T1_SURVIVAL_RECALIBRATION_V01_REVIEW.zip`

No freeze automático.
