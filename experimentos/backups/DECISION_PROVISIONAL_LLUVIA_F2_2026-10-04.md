# DECISIÓN PROVISIONAL — LLUVIA DE FILOS F2

Fecha: 2026-10-04
Rama: `experiment/techniques-kaggle-heavy-v0.4`
HEAD antes de registrar decisión: `e47695c919969bb9d70c68cb9a654c96fa1cc14d`

## Guardias

- No tocar `main`.
- No merge.
- No declarar CANON global.
- Decisiones humanas prevalecen.
- Este registro congela un candidato provisional para revisión cross-root; no cierra el balance global.

## Estado

**Lluvia de Filos — F2 / SOBOL trial 194**

Estado: `SELECTED_FOR_CROSS_ROOT_REVIEW — PROVISIONAL`

No es CANON global.

## Motivo de selección provisional

Comparación HIGH observada:

- F0 baseline: regret 0.11142105913311266; polarización 0; distancia 0.
- F1 TPE/269: regret 0.09256957645262492; polarización 0.02580249802916831; distancia 0.09691358024691359.
- F2 SOBOL/194: regret 0.08610299115417241; polarización 0.11827684607693771; distancia 0.16574074074074074.
- F3/F4 no reducen regret frente a baseline.
- F5/F6 aumentan regret.
- Todos los finalistas observados de Lluvia mantienen 0 pares universales.

F1 tiene menor polarización y distancia que F2, pero su Deep R256:
- media Δ ~ -0.0011085009;
- 0 ganancias materiales;
- 10 pérdidas materiales;
- peor celda ~ -0.0367866848.

F2 tiene Deep incremental R64/R256/R1000:
- R1000 media Δ ~ +0.0272048386;
- 609 ganancias materiales;
- 0 pérdidas materiales;
- peor celda observada = 0;
- mejor celda observada ~ +0.111320887;
- polarización deep R1000 ~ 0.1113208874.

Por tanto F2 es el candidato provisional más probable para llevar al balance conjunto. No se interpreta como aprobación de potencia final: el patrón 609 ganancias / 0 pérdidas y su polarización/distancia elevadas indican riesgo de buff amplio y posible overtuning cross-root.

## Cambios exactos F2

- `base_percent_pen_pp: 10 -> 14`
- `direct_pct/0: 15 -> 10`
- `direct_pct/1: 20 -> 15`
- `full_direct_crit_pp: 5 -> 4`
- `rupture/t1_t2_pen_pp: 5 -> 4`
- `eff/t1_t2_precision: 5 -> 4`
- `eff/full_pen_pp: 5 -> 10`
- `SHRED_DEF_INCREMENT: 1 -> 2`
- `BASE_DAMAGE_FLAT_MODIFIER: 1 -> 2`

## Lectura de diseño

F2 desplaza potencia desde bonos directos/crit/precision hacia:
- mayor penetración base y full;
- mayor shred;
- mayor daño plano base.

Esto preserva identidad Metal, pero puede estar demasiado por encima del envelope del resto de raíces.

## Próximo criterio

No seguir retocando Lluvia en aislamiento.

Mantener:
- F0 como ancla conservadora;
- F1 como alternativa de menor polarización/distancia;
- F2 como candidato principal provisional.

Reabrir sólo durante cross-root review de las 15 técnicas, o antes si aparece bug verificado/inconsistencia cross-root.

## Metal provisional

- Destello de Plata: F0 — aprobado por decisión humana.
- Armadura de Plata: F7 — candidato provisional para cross-root.
- Lluvia de Filos: F2 — candidato provisional para cross-root.
- Metal global: NO CANON.
