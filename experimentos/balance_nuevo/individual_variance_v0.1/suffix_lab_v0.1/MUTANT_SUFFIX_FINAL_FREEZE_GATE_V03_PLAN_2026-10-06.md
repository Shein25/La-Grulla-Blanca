# Mutant Suffix Final Freeze Gate V03 — plan

Fecha: 2026-10-06
Estado: READY_TO_RUN / FINAL GATE BEFORE T2

## Semántica autoritativa del laboratorio

No existe un monstruo repetible normal con estadísticas fijas.

Cada spawn:
1. parte del piso T0 y la envolvente propia de su especie;
2. tira una sola vez sus q_axis independientes;
3. materializa sus estadísticas individuales;
4. evalúa si la conjunción cae en la cola Mutante;
5. deriva su taxonomía/sufijo de esas mismas características;
6. conserva esos valores durante la vida de la instancia;
7. después se aplica el tier adaptativo T0/T1.

No existe RNG adicional para elegir sufijo y no se agrega un paquete artificial de stats al declarar Mutante.

## Taxonomía candidata a congelar

- Mutante especializado: Mutante con menos de 2 q_axis >= 0.95; su familia es el grupo semántico dominante.
- Excepcional: exactamente 2 q_axis >= 0.95.
- Ascendido: 3 o más q_axis >= 0.95.

Los grupos siguen siendo:
- Acorazado = HP/DEF.
- Fugaz = EVA.
- Acechante = PREC.
- Indómito = TEN.
- Voraz = daño/ofensiva.

## Finalistas de habilidad

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

## Fase A — población

500.000 spawns naturales por especie = 2.500.000.

Exportar:
- incidencia de NORMAL / cinco especializados / EXCEPCIONAL / ASCENDIDO;
- distribución exacta de número de ejes >=0.95 entre Mutantes;
- percentiles P10/P25/P50/P75/P90/P95/P99 de cada stat/eje materializado.

Objetivo adicional: dejar evidencia cuantitativa de que la especie es una población de individuos distintos, no un perfil fijo.

## Fase B — Mutantes especializados

128 individuos naturales condicionados por combinación especie/sufijo disponible.

Comparar con CRN:
- NONE;
- CENTER;
- STRONG.

Matriz:
- EXPECTED_STAGE / HIGH_ROLL_STRESS;
- cinco raíces;
- UNITARGET_FIRST / DEFENSE_OPEN;
- T0 / T1 congelado.

## Fase C — Excepcional / Ascendido

- 96 Excepcionales naturales por especie.
- 64 Ascendidos naturales por especie.

La habilidad se deriva de los grupos realmente tocados por los q_axis extremos.

Comparar con CRN:
- NONE;
- DOMINANT_CENTER: sólo habilidad del grupo extremo dominante;
- INHERIT_CENTER: todas las habilidades de los grupos extremos, intensidad CENTER;
- INHERIT_STRONG: todas las habilidades de los grupos extremos, intensidad STRONG.

Esto decide si Excepcional/Ascendido deben heredar una o varias habilidades y si la acumulación sigue siendo estable.

## Guardias

- T0/T1 no se recalibran.
- Baja win-rate contra Mutantes NO es fallo.
- 0 timeout/soft-lock.
- 0 NaN/Inf.
- floors/envelopes intactos.
- clasificación determinista desde q_axis.
- incidencia Mutante <1%.
- no main.
- no merge.
- no runtime canónico.
- ninguna decisión se ratifica automáticamente desde el runner.

## Artefacto

Kaggle:
KAGGLE_LI_MUTANT_SUFFIX_FINAL_FREEZE_GATE_V03.zip

Al cerrar este gate:
- congelar variabilidad individual + Mutantes + sufijos;
- abrir T2 usando individuos aleatorios desde el primer micro-screen.
