# Decisión humana — alcance real del balance por etapa

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: HUMAN_DECISION / AUTORIDAD DE BALANCE

## Objetivo

El balance de una etapa NO tiene como único objetivo adaptar o recalibrar monstruos.

Debe evaluar conjuntamente:

1. monstruos;
2. técnicas disponibles en la etapa;
3. Concordancias disponibles;
4. equipo disponible;
5. raíces;
6. economía de Qi;
7. progresión/Tramos legalmente desbloqueados.

## Equipo como dimensión primaria

Para cada etapa debe comprobarse:

- si cada pieza aporta una diferencia medible;
- si el aporte coincide con su identidad/build_tags;
- si una pieza es funcionalmente muerta;
- si una pieza es claramente dominada por otra disponible en la misma etapa;
- si una pieza se vuelve obligatoria;
- si un slot entero carece de valor;
- si una combinación genera un breakpoint desproporcionado;
- si EXPECTED_STAGE representa razonablemente el centro de potencia;
- si HIGH_ROLL_STRESS representa una cola fuerte pero plausible;
- si MANDATORY_ENTRY sigue siendo jugable;
- si el equipo mejora diferentes estilos sin borrar la importancia de raíz/técnica;
- si el coste/accesibilidad de una pieza guarda relación con su aporte.

## Orden de corrección

Ante un problema de balance:

1. verificar bug/metodología;
2. identificar si el problema nace de equipo, técnica, Concordancia o monstruo;
3. corregir la capa causal;
4. evitar inflar monstruos para compensar equipo roto;
5. evitar nerfear equipo útil para compensar una sola interacción de Concordancia;
6. sólo modificar monstruos si el perfil del monstruo es la causa demostrada.

## Métricas mínimas de equipo

- win-rate marginal vs desnudo / dotación mínima;
- HP final marginal;
- Qi final y Qi gastado;
- rondas;
- daño/mitigación/control según identidad;
- frecuencia de uso de técnicas;
- sensibilidad por raíz;
- sensibilidad por monstruo;
- sensibilidad por Concordancia;
- valor por slot;
- valor por pieza;
- frecuencia de aparición en mejores/peores colas;
- dominancia Pareto de vectores de stats;
- redundancia de firmas;
- breakpoints discretos provocados por stats;
- piezas con impacto estadísticamente indistinguible de 0 en el screen;
- piezas con impacto excesivo o universal.

## LianQi I

El gate LI debe estudiar explícitamente:

- 14 piezas disponibles;
- 6.144 loadouts legales;
- 4.864 firmas mecánicas;
- NAKED;
- MANDATORY_ENTRY;
- EXPECTED_STAGE;
- HIGH_ROLL_STRESS;
- extremos por eje;
- cohortes por slot/pieza;
- Concordance OFF/ON;
- T0/T1 principal;
- T2 sólo stress.

## Resultado

El cierre de una etapa debe responder por separado:

- MONSTERS: PASS / RETUNE;
- TECHNIQUES: PASS / RETUNE;
- CONCORDANCES: PASS / RETUNE;
- EQUIPMENT: PASS / RETUNE;
- ROOTS: PASS / RETUNE;
- SYSTEM: PASS / RETUNE.

Un PASS global no puede ocultar una capa fallida.

No main. No merge. No runtime. No auto-freeze.
