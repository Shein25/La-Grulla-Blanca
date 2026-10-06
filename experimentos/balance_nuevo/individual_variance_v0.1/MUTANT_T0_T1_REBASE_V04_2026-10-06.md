# Rebase Mutantes LI v0.4 — 2026-10-06

## Estado

`HUMAN_RATIFIED_REBASED_T0_T1_COMPAT_PENDING`

## Autoridad

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`

## Regla de rebase

- El T0 congelado es el piso natural.
- Un techo histórico se conserva sólo si sigue >= al T0 actual.
- Si el techo histórico quedó por debajo, el eje colapsa al T0 hasta nueva evidencia.
- Escaleras ofensivas por debajo del T0 se eliminan.
- No se inventan techos.
- Mono sincroniza QI_DRAIN=6.
- Lobo sincroniza cadencia de Emboscada=4.

## Ejes efectivos v0.4

- Rata: 3 ejes — EVA, PREC, TEN.
- Serpiente: 6 ejes — DEF, EVA, PREC, TEN, daño veneno, ticks veneno.
- Avispa: 6 ejes — EVA, PREC, TEN, daño básico, daño veneno, ticks veneno.
- Mono: 5 ejes — DEF, EVA, PREC, daño básico, daño directo Manotazo.
- Lobo: 4 ejes — HP, DEF, daño básico, daño directo Emboscada.

## Selfcheck de incidencia

Muestreo determinista de 1.000.000 spawns por especie, sin combate:

| Especie | Mutantes | Incidencia |
|---|---:|---:|
| rata_qi | 7.587 | 0,7587% |
| serpiente_qi | 7.597 | 0,7597% |
| avispa_jade | 7.561 | 0,7561% |
| mono_pildoras | 7.522 | 0,7522% |
| lobo_espiritual | 7.513 | 0,7513% |

Todas pasan la guardia <1% y permanecen alrededor del objetivo 0,75%.

## Criterio humano de dificultad

No hay piso mínimo de win-rate del jugador contra Mutantes.

Una caída fuerte de victoria es esperable por rareza y no es fallo de balance. El próximo compatibility gate debe bloquear sólo por problemas de contrato/runtime: floors inválidos, identidad alterada, NaN/Inf, timeout/soft-lock, T1 roto, tier concedido por mutación o inversión anómala donde el Mutante resulte sistemáticamente más fácil.

## Próximo paso

Gate focal Normal/Mutante sobre los cinco T1 congelados, más stress del upper-envelope. No activar runtime antes del cierre humano.
