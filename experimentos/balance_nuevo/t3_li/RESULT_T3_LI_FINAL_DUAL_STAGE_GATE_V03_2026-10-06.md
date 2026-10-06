# Resultado — T3 final dual-stage gate V03

Fecha: 2026-10-06
Estado: **VALID / HUMAN FREEZE APPLIED**

Review ZIP SHA-256:
`ba9c8ef20c5155af0064f337b7eda7ff6cafcc79da8900e303a432849a0461d2`

## Integridad

- 294.400 combates representados.
- 2 workers.
- 4 réplicas por individuo/celda.
- stages:
  - LianQi_I / LI_OVERREACH;
  - LianQi_IV / LIV_STRUCTURAL.
- T0/T1/T2 congelados.
- variabilidad + Mutantes/sufijos V1 activos.
- manifest 7/7 verificado.
- 0 timeouts.
- 0 NaN/Inf.
- false counter rate = 0.
- degenerate counter loops = 0.
- `issues=[]`.

## Candidatos congelados

- Rata Qi — `R1_INSTANCE_BASIC`.
- Serpiente Qi — `S1_INSTANCE_POISON_TICK`.
- Avispa Jade — `A2_INSTANCE_POISON_TICK`.
- Mono Píldoras — `M2_INSTANCE_MANOTAZO_PACKET`.
- Lobo Espiritual — `L2_INSTANCE_EMBOSCADA_DAMAGE`.

## Lectura NATURAL — diagnóstico

### LianQi I / sobreextensión
- Rata: delta win jugador ~-5,27 pp; ~0,393 counters/pelea.
- Serpiente: ~-0,70 pp; ~0,177 counters/pelea.
- Avispa: ~-1,03 pp; ~0,165 counters/pelea.
- Mono: ~-0,50 pp; ~0,208 counters/pelea.
- Lobo: ~-2,85 pp; ~0,372 counters/pelea.

### LianQi IV / contexto estructural
- Rata: delta win ~0,00 pp; ~0,146 counters/pelea.
- Serpiente: ~-3,90 pp; ~0,570 counters/pelea.
- Avispa: ~-0,41 pp; ~0,214 counters/pelea.
- Mono: ~-0,10 pp; ~0,552 counters/pelea.
- Lobo: ~-0,09 pp; ~1,218 counters/pelea.

No existe target universal de win-rate. LI es sobreextensión autoinducida y LIV es la banda estructural prevista.

## Guardias causales

- No counter por fallo natural.
- Rata/Serpiente/Avispa/Mono: mismo roll debe demostrar que T1 EVA fue causal.
- Lobo: mismo packet debe demostrar que +10 DEF T1 previno >0 daño.
- acción real debe confirmar la predicción T2.
- no root/build inspection.
- no future RNG.
- no T4.
- no escalado universal de stats.

T3 queda apto para freeze.
