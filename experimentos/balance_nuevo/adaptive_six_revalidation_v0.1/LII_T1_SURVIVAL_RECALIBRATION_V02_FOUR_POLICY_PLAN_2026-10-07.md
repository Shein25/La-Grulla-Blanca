# LII T1 Survival Recalibration V02 — four-policy paired gate

Fecha: 2026-10-07
Estado: READY_FOR_COLAB

## Corrección sobre V01

V01 fue mecánicamente válido pero metodológicamente incompleto para el target agregado porque usó sólo:
- UNITARGET_FIRST
- DEFENSE_OPEN

V02 restaura la matriz comparable al T0 V04:
- UNITARGET_FIRST
- AOE_FIRST
- DEFENSE_OPEN
- ROTATION

## T0 congelado

Sapo:
- HP55 / PRE98 / EVA11 / DEF0 / TEN6
- BASIC 1d2+5
- Nube de Hollín 1d2+4 + burn 1d2+2 x3
- cadence3

Escarabajo:
- HP75 / PRE90 / EVA14 / DEF2 / TEN24
- BASIC 1d2+3
- Carga de Caparazón 1d2+8
- cadence3

## T1

Trigger:
- HP <=30% OR heavy hit >=20% maxHP.

Activation:
- consumes monster turn.

### Sapo
MITIGATE_NEXT
magnitudes:
10,20,30,40,50,60,70,80,90%
cooldowns:
3,4,5,6

36 candidates.

Historical 10/CD5 retained as control.

### Escarabajo
DEFENSE_UP
bonuses:
+2,+4,+6,+8,+10,+12,+14,+16,+18,+20
cooldowns:
3,4,5,6

40 candidates.

Historical +2/CD5 retained as control.

## Matrix

SCREEN:
76 candidates × 3 gears × 5 roots × 4 policies × R24
= 109.440 fights.

CONFIRM:
TOP8 per species × 2 species × 3 gears × 5 roots × 4 policies × R128
= 122.880 fights.

Paired T0:
2 species × 3 gears × 5 roots × 4 policies × R128
= 15.360 fights.

TOTAL:
**247.680 fights**.

## Selection

Primary:
- paired T1 must not be >2 pp easier than T0;
- 0 timeout;
- T1 must proc;
- no root/policy catastrophic cliff.

Diagnostic:
- HRS aggregate around 55–65% is desirable to leave space for T2;
- not a universal hard target.

If no candidate reaches the diagnostic band, choose the strongest mechanically healthy non-easier candidate and review whether T1 identity itself needs reopening. Do not silently redesign identity.

No automatic freeze.
