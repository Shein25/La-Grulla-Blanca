# LianQi I — V04B Full Regression Exhaustive

Fecha: 2026-10-07  
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`  
Estado: HUMAN-AUTHORIZED FOR REGRESSION / NO FREEZE / NO RUNTIME PRODUCTIVO

## 0. Propósito

V04B es la regresión exhaustiva de cierre de LianQi I después de V03, V04A y V04A.1.

No busca seguir explorando candidatos. Usa el conjunto de candidatos humanos/review seleccionado y pregunta:

> ¿El sistema completo de LianQi I sigue sano cuando raíces, equipo y Concordancias recalibradas se ejecutan simultáneamente contra los monstruos T0/T1 congelados?

No se modifica automáticamente ningún monstruo.

## 1. Fuentes de evidencia

- V03 Full System Review SHA-256:
  `4ff5335d6757cc61954502b18906cc9ae4bb2e53c7dccf9a4490e98a6d789209`
- V04A Microgates Review SHA-256:
  `1b068ee26509b7c7e55a55dcd35fd41223a8dbe2c4fb7fe13cc468488bc73dbf`
- V04A.1 Fine Tuning Review SHA-256:
  `062b7aac3663c3aba89a55628e443f6fd2f820a6fa36810deb8e97f0e229a810`

## 2. Progresión LI fijada para el gate

Disponibles:
- Palma Ardiente;
- Destello de Plata;
- Latigazo de Marea;
- Golpe de Montaña;
- Lanza que Parte Nubes.

No disponibles:
- defensivas;
- AOE;
- Tramo I/II/III.

T0/T1 = objetivo principal.  
T2 = stress transitorio.  
T3/T4 = excluidos.

## 3. Candidatos de raíz para regresión

Estos valores son CANDIDATOS V04B, no canon:

- Fuego: `direct_damage_pct=6`, `crit_chance_pp=3`.
- Metal: `percent_penetration_pp=15`, `precision=7`.
- Agua: `qi_cost_mult=0.75`, `control=10`.
- Tierra: conservar `hp_max_mult=1.10`, `tenacity=5`.
- Viento: conservar `evasion=10`, `crit_damage_add=0.05`.

## 4. Candidatos de equipo para regresión

Se aplica únicamente en memoria dentro del lab:

- `baston_fresno_practica`: `TEN +1 / PREC +1`.
- `pulsera_fibra_trenzada`: `QI +1 / CONTROL +1`.
- `colgante_fragmento_jade`: `CONTROL +4`.
- `bandana_lino_simple`: excluida del espacio LI como `DEFER_TO_LII_CANDIDATE`.

La exclusión de Bandana es sólo candidata. Si se adopta después, debe reconciliarse su adquisición M02 antes de cambiar el catálogo productivo.

Resto de piezas: sin cambios.

Espacio candidato esperado:
- 13 piezas LI;
- 4.096 loadouts crudos;
- 2.688 firmas mecánicas.

## 5. Candidatos de Concordancia por relación

Valores relativos por relación, no un porcentaje universal:

- AGUA→FUEGO — DIRECT_DAMAGE: 0.045
- AGUA→TIERRA — EVASION_DEBUFF: 2.00
- FUEGO→AGUA — CONTROL_POWER: 0.10
- FUEGO→METAL — PERCENT_PENETRATION: 1.50
- FUEGO→TIERRA — DIRECT_DAMAGE: 0.05
- FUEGO→VIENTO — CRIT_CHANCE: 1.50
- METAL→AGUA — CONTROL_POWER: 0.10
- METAL→TIERRA — DIRECT_DAMAGE: 0.05
- METAL→VIENTO — PRECISION: 0.75
- TIERRA→AGUA — CONTROL_POWER: 0.15
- TIERRA→FUEGO — CONTAINED_TRIGGER / NÚCLEO_DE_MAGMA: scale 0.10, duración 2 turnos de fuente
- TIERRA→METAL — PERCENT_PENETRATION: 1.25
- VIENTO→AGUA — CONTROL_POWER: 0.15
- VIENTO→FUEGO — DIRECT_DAMAGE: 0.045
- VIENTO→METAL — PERCENT_PENETRATION: 1.25
- VIENTO→TIERRA — DIRECT_DAMAGE: 0.045

Los 4 BASE NONE permanecen:
- resolución 0;
- consumo por Concordancia 0;
- fallback 0.

## 6. Baseline histórico V03

Referencia externa conservada, no recalculada como autoridad:

Global:
- T0 OFF: 59.1141%
- T0 ON: 62.2672%
- T1 OFF: 54.5234%
- T1 ON: 57.3375%
- global OFF: 56.8187%
- global ON: 59.8023%

El objetivo de V04B no es reproducir esos porcentajes exactamente, sino mostrar qué cambia con el sistema recalibrado.

## 7. Diseño exhaustivo V04B

### Fase A — Attribution Matrix

Cohorte común de equipo legal en ambos sistemas:
- NAKED;
- MANDATORY_ENTRY;
- EXPECTED_STAGE;
- HIGH_ROLL_STRESS;
- extremos y cobertura mecánica sin Bandana.

Brazos:
1. CURRENT_ROOTS + CURRENT_EQUIPMENT + CONCORDANCE_OFF
2. CURRENT_ROOTS + CURRENT_EQUIPMENT + V03_CONCORDANCE_10PCT
3. CANDIDATE_ROOTS + CURRENT_EQUIPMENT + CONCORDANCE_OFF
4. CURRENT_ROOTS + CANDIDATE_EQUIPMENT + CONCORDANCE_OFF
5. CANDIDATE_ROOTS + CANDIDATE_EQUIPMENT + CONCORDANCE_OFF
6. CANDIDATE_ROOTS + CANDIDATE_EQUIPMENT + CANDIDATE_CONCORDANCE_ON

Cruce:
- 20 pares ordenados;
- 5 raíces;
- 5 monstruos;
- T0/T1;
- R alto/moderado con Common Random Numbers por contexto.

Objetivo: atribuir cuánto cambio proviene de raíces, equipo y Concordancias.

### Fase B — Exhaustive Candidate Signature Screen

Se recorren las 2.688 firmas mecánicas candidatas.

Cruce completo:
- 2.688 firmas;
- 20 pares ordenados;
- 5 raíces;
- 5 monstruos;
- T0/T1;
- CANDIDATE_CONCORDANCE_OFF vs ON;
- Common Random Numbers;
- R=1 de screen exhaustivo.

Esto cubre el producto cartesiano completo de firma × par × raíz × monstruo × tier.

La salida cruda no se empaqueta completa: se agregan estadísticas por firma/raíz/especie/relación/tier y se retienen sólo anomalías y hashes de chunks para mantener el REVIEW auditable y liviano.

### Fase C — High-R canonical/extreme regression

Sobre 16 contextos de equipo:
- NAKED;
- MANDATORY_ENTRY;
- EXPECTED_STAGE;
- HIGH_ROLL_STRESS;
- extremos por eje;
- farthest-signature coverage.

Cruce:
- 20 pares;
- 5 raíces;
- 5 monstruos;
- T0/T1;
- OFF/ON;
- R alto.

Objetivo: confirmar con menor ruido los resultados de Fase B.

### Fase D — Equipment marginal final

Para cada una de las 13 piezas LI candidatas:
- ITEM_OFF vs ITEM_ON;
- 20 pares;
- 5 raíces;
- 5 monstruos;
- T0/T1;
- Concordance OFF/ON;
- Common Random Numbers.

Objetivo:
- pieza muerta;
- pieza obligatoria;
- especialista;
- dominancia;
- breakpoints;
- sensibilidad por raíz/monstruo/Concordancia.

### Fase E — T2 stress transitorio

No calibra valores.

Se usa una muestra determinista de 128 firmas candidatas:
- canonical;
- extremos;
- farthest coverage.

Cruce:
- 20 pares;
- 5 raíces;
- 5 monstruos;
- OFF/ON;
- T2;
- R moderado.

### Fase F — BASE NONE isolated sentinel

Las 4 relaciones negativas se aíslan direccionalmente.

Debe permanecer:
- concordance_resolutions = 0;
- no consumption;
- no fallback.

## 8. Métricas y diagnósticos

### Sistema
- win rate;
- HP final;
- Qi final/gastado;
- rondas;
- timeout;
- concordance resolutions;
- delta OFF→ON;
- comparación con V03.

### Raíces
- spread global y por tier;
- spread por monstruo;
- sensibilidad al equipo;
- sensibilidad a Concordancia;
- Qi exhaustion.

### Monstruos
- dificultad global;
- dificultad por raíz;
- T0→T1 delta;
- survival activations;
- cliffs por equipo/relación.

### Concordancias
- delta por relation_id;
- delta por hook;
- frecuencia real de resolución;
- root/species/gear spread;
- structural events;
- controles NONE.

### Equipo
- curva NAKED→ENTRY→EXPECTED→HRS;
- marginal por pieza;
- slot value;
- firma extrema;
- candidatos muertos/obligatorios;
- ranking OFF vs ON.

## 9. Decisión posterior

V04B no auto-freezea.

El REVIEW debe producir:
- MONSTERS: PRESERVE / REOPEN_CANDIDATE
- TECHNIQUES: PASS / REOPEN_CANDIDATE
- CONCORDANCES: PASS / RETUNE
- EQUIPMENT: PASS / RETUNE
- ROOTS: PASS / RETUNE
- SYSTEM: READY_FOR_HUMAN_FREEZE / RETUNE

Sólo después de revisión humana se podrá cerrar nuevamente LianQi I.

## 10. Guardias de ejecución

- 2 workers en el runtime conocido de 2 CPU lógicas.
- checkpoints reanudables.
- barra propia compacta de una sola línea.
- no `tqdm.notebook` si rompe layout.
- checkpoint amarillo.
- cálculo azul.
- final verde.
- error rojo.
- pre-delivery QA obligatorio.
- no main.
- no merge.
- no cambio productivo.
