# Auditoría — Mutant Suffix T0/T1 Battery V01

Fecha: 2026-10-06
Estado: **VALID RESULTS / PARTIAL EVIDENCE — NO RATIFICATION**

Review SHA-256:
`10f4de9cc09c7244d2c2e268239f6170f026edf1e88c9816fa37e3cf18465c0d`

## Integridad

- ZIP íntegro.
- Manifest 8/8 hashes y bytes correctos.
- 2.500.000 spawns de clasificación.
- 368.640 combates de habilidad.
- 92.160 combates de stack stress.
- 0 timeouts / 0 NaN/Inf / `issues=[]`.
- T0 y T1 congelado ejecutados.
- Sin piso mínimo de win-rate para Mutantes.

## Clasificación

El control dominante es `multi_margin`, no `min_group_score`.

Con min_group_score 0.80:
- margin 0.00: 0% MULTI, siempre sufijo dominante.
- margin 0.05: MULTI ≈31–63% de Mutantes según especie.
- margin 0.10: MULTI ≈55–92%.

Conclusión: no usar MULTI por cercanía de scores como equivalente automático de Excepcional/Ascendido. Es demasiado frecuente. Excepcional y Ascendido siguen pendientes y deben estudiarse por cantidad/intensidad de grupos/ejes altos.

## Sufijos individuales

### Fugaz
Señal clara y monotónica. +15/+25/+35 EVA aumenta evasiones y reduce win-rate del jugador sin conflicto con T1. F25/F35 quedan como candidatos útiles; no se ratifica aún.

### Acechante
La hipótesis LAB de +PREC después de fallar funciona y es auto-limitante: al subir PREC disminuyen sus propios retriggers. Señal fuerte en Rata, más tenue donde el Mutante base ya satura. Sigue siendo hipótesis nueva, no decisión histórica.

### Indómito
Mecánicamente limpio. En Agua, la primera resistencia extra reduce la tasa de Control aproximadamente 4–9 pp según I15/I25/I35. T1 no rompe la interacción.

### Acorazado
Semántica de cruce de HP, incluido DOT del jugador, está correctamente cubierta. Pero las especies compatibles ya tienen win-rate casi saturada y A10/A15/A20 no se distinguen bien sólo por victorias. Hace falta telemetría de absorción usada antes de escoger intensidad.

### Voraz
La V01 submide especies DOT. El cruce de HP se comprueba tras el turno directo/técnica del monstruo, pero no tras el tick de veneno que ocurre en `player_turn_start`. Por eso Serpiente/Avispa pueden cruzar el umbral mediante DOT sin armar el siguiente BASIC. No ratificar V1/V2/V3 desde V01.

## Multi-sufijo

El stress confirma robustez: pares y ALL_SUPPORTED no producen timeout/soft-lock.

Sin embargo V01 usa `arm_name` dentro de la seed de Fase C, por lo que NONE, pares y ALL_SUPPORTED no comparten CRN. Sirve como stress de estabilidad, pero no para diferencias finas de potencia ni para separar Excepcional vs Ascendido.

## Resultado

Evidencia confiable:
- arquitectura de sufijos estable en T0/T1;
- Fugaz, Acechante e Indómito muestran comportamiento válido;
- no hay explosión de runtime al combinar habilidades.

Pendiente antes de ratificación global:
1. Voraz con cruce por DOT corregido.
2. Acorazado con telemetría de absorción.
3. stack stress con CRN compartido.
4. distribución natural por número de grupos/ejes altos para decidir Excepcional vs Ascendido.

No tocar `main`. No merge. No activar sufijos en runtime canónico.
