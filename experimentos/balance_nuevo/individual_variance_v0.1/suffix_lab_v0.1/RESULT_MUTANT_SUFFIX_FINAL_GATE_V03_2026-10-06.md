# Resultado — Mutant Suffix Final Freeze Gate V03

Fecha: 2026-10-06
Estado: MUTANT_SUFFIX_FINAL_GATE_VALID_AWAITING_HUMAN_FREEZE

Review ZIP SHA-256:
`bc4ef362e77d469aef9ea3af19a50bb686a1e01b3b2ab5a042e9c451b22adfe8`

## Integridad

- 500.000 spawns naturales por especie × 5 = 2.500.000.
- 404.480 combates representados.
- T0 + T1 congelado.
- EXPECTED_STAGE + HIGH_ROLL_STRESS.
- cinco raíces.
- dos policies.
- CRN pareado.
- 0 timeouts.
- 0 NaN/Inf.
- issues=[].
- ninguna ratificación automática.

## Incidencia Mutante

- Rata Qi: 0,7432%.
- Serpiente Qi: 0,7540%.
- Avispa Jade: 0,7120%.
- Mono Píldoras: 0,7714%.
- Lobo Espiritual: 0,7514%.

Todas <1%.

## Taxonomía candidata

- Especializado: Mutante con menos de 2 q_axis >=0.95; familia semántica dominante.
- Excepcional: exactamente 2 q_axis >=0.95.
- Ascendido: 3 o más q_axis >=0.95.

No existe RNG adicional de sufijo.

## Finalistas

CENTER:
- Acorazado A15.
- Fugaz F25.
- Acechante C20.
- Indómito I25.
- Voraz V2.

STRONG:
- Acorazado A20.
- Fugaz F35.
- Acechante C30.
- Indómito I35.
- Voraz V3.

Lectura de cierre recomendada:
- CENTER ofrece identidad suficiente en las cinco familias y evita magnitudes extra cuando STRONG aporta ganancias pequeñas o saturadas.
- Excepcional/Ascendido: INHERIT_CENTER es la interpretación más coherente con el modelo emergente, porque hereda las habilidades de los grupos realmente representados por los ejes extremos.
- INHERIT_STRONG fue estable, pero no es necesario para expresar la conjunción extrema.
- DOMINANT_CENTER es estable pero pierde parte de la información emergente de múltiples rasgos extremos.

No congelar hasta decisión humana explícita.

## Regla de backend

Colab y Kaggle deben mantener launchers/rutas separados.
- Colab: rutas relativas o /content/...
- Kaggle: /kaggle/input/... y /kaggle/working/...
- Prohibido mezclar rutas entre backends.
