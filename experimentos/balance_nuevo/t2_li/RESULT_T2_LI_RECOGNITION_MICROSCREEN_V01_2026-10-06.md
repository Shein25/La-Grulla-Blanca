# Resultado — LI T2 Recognition Micro-screen V01

Fecha: 2026-10-06
Estado: **VALID / FOCAL_REQUIRED_FOR_RATA_SERPIENTE**

Review ZIP SHA-256:
`a0a1ee17d40218086f99075d20a5a669824d54cb221927532e17437d8e1b096f`

## Integridad

- 36.800 combates representados.
- 2 workers.
- 5 especies LI.
- T1 congelado vs T2 R2_SHORT preemptivo.
- individuos materializados desde variabilidad antes de Mutante/sufijo/tier.
- contrato Mutante+sufijos V1 activo en ambos brazos.
- 0 timeouts.
- issues=[].

## Lectura natural por especie

Promedio agregado NATURAL:

- Avispa Jade: delta win jugador +0,117 pp; +0,580 rondas; ~0,661 anticipaciones/pelea.
- Lobo Espiritual: delta win -1,250 pp; +1,580 rondas; ~1,884 anticipaciones/pelea.
- Mono Píldoras: delta win -1,484 pp; +1,100 rondas; ~1,271 anticipaciones/pelea.
- Rata Qi: delta win -1,016 pp; +0,406 rondas; ~0,730 anticipaciones/pelea.
- Serpiente Qi: delta win +1,289 pp; +1,068 rondas; ~1,038 anticipaciones/pelea.

No existe target universal de win-rate; estos deltas son diagnósticos.

## Rata — policy split

NATURAL:
- AOE_FIRST: +0,156 pp win jugador; +1,100 rondas.
- DEFENSE_OPEN: -5,469 pp; +0,130 rondas.
- ROTATION: -0,781 pp; +0,200 rondas.
- UNITARGET_FIRST: +2,031 pp; +0,194 rondas.

La mecánica es válida, pero la anticipación automática es demasiado dependiente de la policy para congelar directamente.

## Serpiente — policy split

NATURAL:
- AOE_FIRST: +1,094 pp; +2,116 rondas.
- DEFENSE_OPEN: -2,031 pp; +0,253 rondas.
- ROTATION: -0,156 pp; +0,106 rondas.
- UNITARGET_FIRST: +6,250 pp; +1,798 rondas.

En UNITARGET_FIRST el T2 incrementa daño directo pero reduce DOT en ~1,922 por pelea. Esto es compatible con un coste de oportunidad: la Muda anticipada consume turnos que de otro modo podían ejecutar Colmillos Venenosos.

## Decisión

- Lobo y Mono: señal suficientemente fuerte/estable para no abrir búsqueda grande.
- Avispa: señal moderada, sin evidencia de necesidad de focal grande.
- Rata y Serpiente: abrir focal de **eligibility T2**, no recalibración T1.

No reabrir magnitudes/cooldowns T1.
No modificar stats, veneno, técnicas ni variabilidad individual.
