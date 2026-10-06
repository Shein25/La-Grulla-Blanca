# Handoff de integración runtime — variabilidad individual / Mutante v0.4

Fecha: 2026-10-06

Estado: **HUMAN_RATIFIED_FOR_EXPERIMENTAL_RUNTIME_INTEGRATION — T1 COMPAT PASSED**

## Autoridades

- T0: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`
- T1: `T1_LI_FINAL_FREEZE_2026-10-06`
- config: `monster-individual-variance-v0.4`

La validación heavy del 2026-10-01 (250.000 naturales + 50.000 Mutantes condicionados, incidencia 0,7556%) sigue siendo evidencia de que el **método estadístico y el thresholding** funcionan, pero sus combates no certifican la v0.4 porque se ejecutaron contra T0 antiguos.

## Decisiones conservadas

- `UNIFORM_0_1`;
- tiradas independientes por eje;
- T0 congelado = piso natural;
- un único `species_id`;
- Mutante <1%;
- Mutante: botín x1.5 y XP de combate x1.5;
- objetos únicos no aumentan su probabilidad;
- XP profesional no recibe multiplicador;
- Mutante no concede tiers adaptativos.

## Rebase

Los pisos fueron sincronizados al T0 final. Cuando el techo histórico quedó por debajo del nuevo T0, el eje fue colapsado al piso en vez de inventar un techo.

Identidades corregidas:
- Mono: `QI_DRAIN=6`;
- Lobo: cadencia de Emboscada = 4.

## Dificultad Mutante

No existe guardrail de win-rate mínimo para el jugador.

Una caída fuerte —incluso extrema— de la probabilidad de victoria es válida para una aparición Mutante rara. El compatibility gate sólo debe bloquear por incoherencia mecánica, identidad rota, valores inválidos, timeouts/soft-locks o por una inversión clara donde el Mutante resulte más fácil debido a un bug.

## Runtime adapter

El adapter continúa:
- clonando el perfil canónico;
- aplicando stats/ataques de instancia;
- sin mutar el registro;
- sin conceder T1–T4;
- persistiendo la tirada por instancia.

La config v0.4 volvió a status `HUMAN_RATIFIED_FOR_EXPERIMENTAL_RUNTIME_INTEGRATION` después de pasar el gate Normal/Mutante con T1. Esto habilita integración experimental, no activación automática del runtime canónico.

## Próximo gate

Debe comprobar:
1. incidencia natural <1%;
2. floors y envelopes;
3. normales y Mutantes condicionados para las cinco especies;
4. aplicación posterior de T1 congelado;
5. 0 timeout/NaN/loops;
6. identidad fija;
7. no hard-floor de win rate Mutante.

No activar automáticamente en runtime canónico tras el test: requiere cierre humano.

## Gate de compatibilidad T1 — PASS 2026-10-06

- 1.000.000 spawns.
- 102.400 combates T1.
- 0 timeouts / 0 NaN-Inf / 0 issues.
- review SHA-256: `c4e3c73f8ff907fa3b8e698bbc6ae991b9dfde1015a5eb2b439b154630b4bf34`.
- dificultad extrema de Mutantes permanece válida y no bloqueante.
