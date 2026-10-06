# Mutant Suffix T0/T1 Focal V02 — plan

Fecha: 2026-10-06
Estado: **READY_TO_RUN / LAB ONLY**

Corrige únicamente los huecos detectados en V01.

## Fase A — taxonomía sin combate

500.000 spawns por especie.

Además del classifier V01 exportar:
- cantidad de grupos de sufijo con score >= 0.80 / 0.85 / 0.90 / 0.95;
- cantidad de q_axis >= esos mismos umbrales;
- fracción entre Mutantes e incidencia absoluta.

Objetivo: decidir después, sin RNG extra, si Excepcional y Ascendido representan dos escalones multi-eje distintos. No asignar nombres automáticamente.

## Fase B — focal Acorazado/Voraz

Sólo EXPECTED_STAGE y HIGH_ROLL_STRESS, T0/T1, cinco roots, dos policies, R128.

Acorazado:
- A10/A15/A20;
- exportar `monster_absorbed` para distinguir intensidades aunque win-rate esté saturada.

Voraz:
- V1/V2/V3;
- detectar cruce de HP después de daño directo/técnica y también después del DOT enemigo en `player_turn_start`.

## Fase C — multi-sufijo pareado

- mismo upper-envelope de stress;
- NONE / todos los pares / ALL_SUPPORTED;
- misma seed CRN dentro de cada celda para todos los arms;
- EXPECTED/HIGH;
- T0/T1;
- R128.

## Guardias

- dificultad extrema no falla;
- 0 timeout/NaN/Inf;
- T0/T1 no se modifican;
- no ratificación automática;
- no main / no merge / no runtime canónico.
