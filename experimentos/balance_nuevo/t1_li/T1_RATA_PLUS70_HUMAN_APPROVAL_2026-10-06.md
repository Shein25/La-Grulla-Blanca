# T1 LI — aprobación humana Rata Qi +70 EVA / CD6

**Fecha:** 2026-10-06  
**Rama:** `experiment/li-monster-t0-final-t1-lab-v0.1`

## Decisión humana

Se aprueba reemplazar el candidato T1 anterior de Rata Qi:

- Reflejo de Madriguera
- EVADE_NEXT
- +60 EVA
- CD6

por:

- Reflejo de Madriguera
- EVADE_NEXT
- **+70 EVA**
- **CD6**
- una sola carga
- triggers sin cambios: HP <=30% o golpe >=20% HP máximo
- la activación sigue consumiendo el turno del monstruo
- sin daño adicional
- sin QI drain
- sin timer nuevo

Candidate ID nuevo: `48a4e5535db32cc5`.

## Motivo

El gate exhaustivo final T1 V02 cerró Serpiente, Avispa, Mono y Lobo. El único bloqueo fue Rata Qi: el candidato +60/CD6 quedó +2.265625 pp más fácil que su T0 pareado en EXPECTED_STAGE, apenas por encima del guardrail de +2 pp, con tendencia positiva en los cuatro perfiles.

La corrección +70/CD6 es deliberadamente mínima: no cambia la identidad ni la geometría de la habilidad; sólo aumenta la magnitud defensiva.

## Estado

- T0 permanece congelado.
- Serpiente, Avispa, Mono y Lobo no se reabren.
- Rata +70/CD6 queda como **candidato humano aprobado pendiente de confirmación focal autoritativa**.
- No se congela todavía el registry.
- T2–T4 permanecen bloqueados hasta completar el cierre humano de T1.
- No tocar main. No merge.

## Confirmación focal preparada

Artefacto local preparado:

`KAGGLE_RATA_T1_PLUS70_FOCAL_CONFIRM_V02.zip`

Cobertura:
- perfiles canónicos R1024, T1 + T0 pareado;
- 50 tails de Rata provenientes del gate final V02, R512 T1 + T0 pareado;
- 133,120 combates representados.

La confirmación usa las mismas fuentes fijadas que el gate final V02 y el parche G04 de Tierra.
