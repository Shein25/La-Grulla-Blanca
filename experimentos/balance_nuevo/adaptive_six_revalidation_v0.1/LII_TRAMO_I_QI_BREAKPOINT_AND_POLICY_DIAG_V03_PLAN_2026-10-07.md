# LII Tramo I — Qi, timing y potencia ofensiva — Microgate V03

Fecha: 2026-10-07.
Estado: **PLAN DE LABORATORIO, NO FREEZE, NO REBALANCE CANONICO**.
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`.

## Autoridad y corrección explícita de V02

Revisión: `LII_DEFENSIVE_T1_T2_FOCAL_R256_V02_REVIEW_2026-10-07.md`.

**ERRATA OBLIGATORIA:** V02 describió equivocadamente el efecto +38,28–53,13 pp como `Palma Ardiente DIRECT T1` cuando pertenecía a `OFF_T1_0`. El catálogo establece:
- `OFF_T1_0` = **DOT**;
- `OFF_T1_1` = **DIRECT**;
- `OFF_T1_2` = **EFFICIENCY**.

Comprobación sobre el ZIP de V02: `OFF_T1_0` (DOT) 16 contextos, mean +45,36 pp, min +32,03 pp, max +53,13 pp; `OFF_T1_1` (DIRECT) 16 contextos, mean +23,49 pp, min +17,97 pp, max +32,42 pp. Son contextos focalizados por alertas previas, **no** estimadores representativos del juego.

No ajustar DIRECT hasta corregir la atribución. V03 mide todas las raíces de forma no seleccionada por las alertas anteriores.

## Matriz V03

Pin fuente: `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`.
Base runner SHA-256: `fc14ff185419d694160121ad9684539bfd324ea171fda8fe8ef8261566510fa9`.
V03 runner SHA-256: `bfcac6ba62b29798ad333bcf9f44534f0d45b5f2948ace6a4f6e356b7b885105`.

### A. Timing defensivo Fuego y Tierra: 46.080 combates

2 raíces × 3 equipos × 2 especies LII × T1/T2 × 3 builds × 5 políticas × R128.

Políticas: OFFENSE_ONLY, DEFENSE_OPEN, DEFENSE_DUE, DEFENSE_GUARD y THREAT_AWARE.
THREAT_AWARE sólo inspecciona HP, Qi y cadencia publicada; prueba defender antes de la siguiente acción debida y reservar Qi ofensivo. No predice RNG ni intención oculta.
Comparaciones por mismos seeds (CRN); acciones y stream RNG posteriores pueden divergir.

### B. Tramo I ofensivo amplio: 15.360 combates

5 raíces × 3 equipos × 2 especies × T1/T2 × BASE y 3 especializaciones ofensivas × R64.
Política ofensiva fija. Familia real obtenida del catálogo por `node_id`/`family`.
Objetivo: screening transversal para diagnosticar DOT/DIRECT/EFFICIENCY en Fuego y evitar sesgo de la muestra V02. R64 no autoriza freeze por sí mismo.

### C. Agua EFICIENCIA de Espejo de Luna: 13.824 combates

3 equipos × 2 especies × T1/T2 × (BASE, EFICIENCIA canon, EFICIENCIA candidata) × 3 políticas × R128.
Problema confirmado: coste final de Agua `5→5` por redondeo bajo el descuento `-1`.
Experimento acotado: cambiar sólo `espejo_luna.model_params.eff.t1_flat_cost` de `-1` a `-2` **en memoria para EFICIENCIA Tramo I**, de forma que Qi final se vuelva `5→4`. No tocar redondeo global ni coste base.
Auditar efectos hipotéticos del mismo cambio al compilar Tramo II/III **sin usarlos en combates LII ni canonizarlos**.

## Gates / resultados

- Source lock SHA de ocho fuentes, T0/T1/T2 LII congelados, eventos 10/10, legalidad de LII 0 AOE, sin supresión de due.
- Checkpoints completos por fase con firma de runner, git, semillas y jobs.
- Raw seed CSV + comparaciones pareadas por política/especialización y resumen de coste.
- Manifest SHA-256, runner dual y QA.
- Salida `LII_TRAMO_I_QI_BREAKPOINT_AND_POLICY_DIAG_V03_REVIEW.zip`.
- Dictamen únicamente **REVIEW_REQUIRED_NO_AUTOFREEZE** antes de la decisión humana.

## Guardias

No tocar monstruos congelados, equipo LI, `main`, merges, pushes, HTML, integración Astra. No inventar mutantes, sufijos, builds multielementales ni Concordancias LII; se ensayarán posteriormente a partir de contratos reales. No inferir que mejores políticas implican más poder intrínseco de una técnica.
