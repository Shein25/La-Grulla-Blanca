# Freeze final — variabilidad individual, Mutantes y sufijos LI

**Fecha:** 2026-10-06  
**Estado:** `MUTANT_SUFFIX_SYSTEM_FROZEN_FOR_T2_LAB`

## Autoridad

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- Variabilidad: `monster-individual-variance-v0.4`
- Sufijos: `MUTANT_SUFFIX_CONTRACT_V1.json`
- Gate final: `LI_MUTANT_SUFFIX_FINAL_FREEZE_GATE_V03`
- Review SHA-256: `bc4ef362e77d469aef9ea3af19a50bb686a1e01b3b2ab5a042e9c451b22adfe8`
- 2.500.000 spawns naturales + 404.480 combates.
- 0 timeouts / 0 NaN-Inf / `issues=[]`.

## Semántica congelada

No existe un monstruo repetible normal con estadísticas fijas.

Cada spawn:
```text
species T0 floor
→ q_axis independientes
→ individuo materializado
→ posible Mutante
→ taxonomía/sufijos derivados de los mismos q_axis
→ tier adaptativo
```

La tirada ocurre una vez por instancia y persiste.

## Sufijos especializados — CENTER congelado

- Acorazado A15: al primer cruce a <=50% HP, reserva de absorción = 15% HPmax.
- Fugaz F25: tras recibir crítico, +25 EVA para la siguiente acción ofensiva del jugador.
- Acechante C20: tras fallar ataque, +20 PREC al siguiente ataque.
- Indómito I25: +25 TEN sólo frente al primer intento de Control.
- Voraz V2: al primer cruce del jugador a <=40% HP, siguiente BASIC ×1.50.

## Excepcional / Ascendido

- Excepcional: exactamente 2 ejes variables con `q_axis >= 0.95`.
- Ascendido: 3 o más ejes variables con `q_axis >= 0.95`.

No existe RNG adicional de nombre.

Excepcional y Ascendido heredan las habilidades CENTER de los grupos representados por sus ejes extremos. Dos ejes del mismo grupo no duplican la misma habilidad.

## Dificultad

No existe piso mínimo de victoria contra Mutantes, Excepcionales ni Ascendidos. La rareza y dificultad extrema son válidas mientras no haya ruptura mecánica.

## Frontera

Este freeze autoriza el uso de la capa completa en laboratorios T2 en adelante.

No activa automáticamente runtime canónico. No toca `main`. No merge.
