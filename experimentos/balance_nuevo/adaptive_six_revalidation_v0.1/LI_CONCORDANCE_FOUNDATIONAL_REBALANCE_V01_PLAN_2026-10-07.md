# LianQi I — Concordance Foundational Rebalance V01

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: PLAN DE LAB / NO FREEZE / NO RUNTIME

## 0. Decisión de alcance

Se reabre el balance de **LianQi I como sistema completo de jugador** para incorporar Concordancias, sin descartar la autoridad congelada de monstruos.

Los freezes T0/T1/T2 existentes se conservan como **baseline de control**. Ningún stat o comportamiento de monstruo se modifica durante este gate.

### Banda adaptativa de LI

- T0–T1: rango normal y objetivo primario.
- T2: stress transitorio / overreach posible, no target de balance.
- T3–T4: fuera del gate fundacional de LI.

## 1. Progresión del jugador LI

Autoridad vigente:

- LianQi I usa técnicas **BASE**.
- LianQi I tiene **0 puntos de Tramo**.
- Tramo I sigue requiriendo LianQi II.
- No se permite ningún Tramo I/II/III en este laboratorio.

### Adquisición

La adquisición narrativa exacta de técnicas ajenas en LI todavía no se congela.

Para evitar perder combinaciones mecánicas, el laboratorio usa un **MECHANICAL ENVELOPE**:
- las 15 técnicas base pueden participar en el censo;
- esto NO significa que el jugador reciba automáticamente las 15;
- un filtro de adquisición futuro sólo puede reducir el subconjunto jugable;
- ningún resultado de este gate convierte adquisición en canon.

## 2. Concordancias

Autoridades:

- `docs/experimentos/CONTRATO_CONCORDANCIAS_GLOBALES_V0_1.md`
- `docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`
- `docs/experimentos/RESOLUCION_AUDITORIA_CONCORDANCIAS_HOOKS_2026-09-29.md`

Reglas duras:

1. relación dirigida ORIGEN → DESTINO;
2. un Eco produce una sola resolución primaria;
3. sólo `concordance_hooks[]` explícitos son receptores;
4. primer hook compatible gana;
5. sin hook compatible: no resolución, no fallback;
6. una técnica pura ejecutada válidamente puede generar su Eco y sustituir el anterior;
7. magnitudes escalables son relativas al hook receptor, nunca +N fijo;
8. transformaciones STRUCTURAL usan únicamente su `transformation_rule` registrada;
9. sin Tramos en LI, por lo que sólo existen hooks BASE;
10. no crear números canónicos automáticamente.

### Espacio base

15 técnicas = 3 por cada uno de 5 elementos.

Pares ordenados entre elementos distintos:

```
5 elementos × 4 destinos × 3 técnicas origen × 3 técnicas destino
= 180 pares ordenados
```

Según el mapeo canónico BASE:

- 49/60 celdas `técnica receptora × Eco entrante` tienen receptor BASE real;
- 11/60 son `BASE NONE / NONE`;
- 147/180 pares de técnicas pueden resolver Concordancia;
- 33/180 pares son controles negativos obligatorios.

Los 33 controles negativos deben permanecer:
- 0 resolución;
- 0 consumo por Concordancia;
- 0 fallback;
- Eco posterior sustituido sólo por la regla universal normal.

## 3. Equipo LI

Autoridad del screen LI:

- 14 piezas disponibles en LI;
- 6.144 loadouts crudos legales;
- 4.864 firmas mecánicas de equipo.

### Exhaustividad

Se enumeran **las 6.144 combinaciones** y se deduplican las 4.864 firmas.

No se pretende ejecutar R alto sobre el producto cartesiano completo, porque:

```
5 raíces principales
× 180 pares
× 4.864 firmas
× 5 monstruos
× 2 tiers primarios
= 43.776.000 contextos antes de cualquier réplica
```

La exhaustividad se divide en:

### Fase A — censo exhaustivo determinista
- 6.144 loadouts;
- 4.864 firmas;
- 180 pares ordenados;
- 147 positivos + 33 negativos;
- 5 raíces principales;
- compatibilidad de hooks;
- coste Qi;
- magnitudes base;
- breakpoints de redondeo;
- legalidad BASE sin Tramos.

### Fase B — screen Monte Carlo estratificado
Selección determinista de firmas que incluya:
- loadouts canónicos;
- mínimos/máximos por eje;
- extremos de Qi;
- extremos de precisión/evasión;
- extremos de DEF/HP;
- extremos ofensivos;
- farthest-distance coverage.

Todos los 180 pares aparecen en el screen.

### Fase C — expansión de colas
Se expanden automáticamente:
- mejores/peores deltas;
- cliffs por raíz;
- cliffs por monstruo;
- relaciones con activación anómala;
- breakpoints discretos de duración/rounding;
- configuraciones donde una Concordancia parezca obligatoria o inútil.

### Fase D — stress T2
Sólo sobre:
- contextos extremos;
- relaciones más fuertes/débiles;
- loadouts canónicos;
- casos con alta repetición de patrón.

T2 no se usa para calibrar el valor base de la Concordancia.

## 4. Comparación causal

Cada contexto debe ejecutar con Common Random Numbers:

### ARM A — CONCORDANCE_OFF
- mismas técnicas;
- misma secuencia;
- mismo equipo;
- misma raíz;
- mismo monstruo;
- mismo T0/T1;
- Eco/resolver de Concordancia desactivado.

### ARM B — CONCORDANCE_ON
Todo idéntico, pero con el resolver activo.

Esto separa el valor marginal de la Concordancia del valor de simplemente conocer una segunda técnica.

## 5. Monstruos LI congelados

No modificar durante el gate:

- Rata Qi
- Serpiente Qi
- Avispa Jade
- Mono Píldoras
- Lobo Espiritual

T0: `T0_LI_FREEZE_MANIFEST_2026-10-06.json`
T1: `T1_LI_FINAL_FREEZE_2026-10-06.md`
T2: `T2_LI_FINAL_FREEZE_2026-10-06.md`

T0/T1 son el benchmark principal.

## 6. Calibración numérica

El contrato de Concordancias está cerrado conceptualmente pero **SIN NÚMEROS DE BALANCE**.

Por tanto el laboratorio no parte de un porcentaje inventado como canon.

Para cada `relation_id + receiver_hook + context`:

1. generar candidatos relativos;
2. incluir breakpoints donde el redondeo produce el primer cambio visible;
3. evaluar magnitud por activación;
4. evaluar frecuencia real de activación;
5. evaluar win-rate marginal vs CONCORDANCE_OFF;
6. evaluar Qi/turn efficiency;
7. evaluar root spread;
8. evaluar monster spread;
9. evaluar worst-tail;
10. devolver frontera de candidatos, no auto-freeze.

Transformaciones STRUCTURAL se prueban sólo con su regla registrada.

## 7. Métricas obligatorias

- fights / contexts / seeds;
- win/loss/timeout;
- rounds;
- HP final;
- Qi final;
- Qi spent;
- Concordance opportunities;
- Concordance resolutions;
- no-compatible-hook events;
- Eco replacements;
- Eco consumptions;
- resolution by relation;
- resolution by receiver hook;
- marginal damage;
- marginal mitigation;
- marginal control;
- marginal duration;
- marginal resource efficiency;
- OFF→ON win delta;
- principal-root spread;
- monster spread;
- equipment-tail spread;
- negative-control leakage;
- fallback violations;
- structural-rule violations.

## 8. Guardias

Bloqueantes técnicos:

- cualquier Tramo activo en LI;
- cualquier resolución en los 33 pares negativos;
- fallback genérico;
- más de una resolución primaria por Eco;
- consumo de Eco sin resolución válida;
- hook no expuesto;
- modificación de T0/T1/T2 congelados;
- T3/T4;
- NaN/timeout anómalo;
- discrepancias de cardinalidad;
- seeds no reproducibles.

Guardias de balance se reportan para decisión humana; no producen freeze automático.

## 9. Política de rebalance

Orden de corrección:

1. corregir bug/semántica del resolver;
2. ajustar magnitud de Concordancia;
3. revisar interacción técnica receptora si el problema es hook-específico;
4. sólo si no existe solución razonable, discutir reapertura de números de monstruos LI.

No nerfear T0/T1 primero por la aparición de una mecánica nueva.

## 10. Resultado esperado

Artefacto final:

`LI_CONCORDANCE_FOUNDATIONAL_REBALANCE_V01_REVIEW.zip`

Debe permitir decidir:

- magnitudes numéricas de Concordancia para LI;
- qué relaciones quedan equilibradas en BASE;
- qué relaciones necesitan retune;
- si T0/T1 congelados siguen válidos con juego multielemental;
- si T2 transitorio sigue siendo tolerable;
- qué riesgos deben revalidarse al abrir Tramo I en LII.

No main. No merge. No runtime. No freeze automático.
