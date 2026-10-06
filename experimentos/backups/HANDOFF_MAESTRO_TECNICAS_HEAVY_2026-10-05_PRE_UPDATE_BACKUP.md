# HANDOFF MAESTRO — TÉCNICAS HEAVY ARCO 1

Fecha: 2026-10-04  
Rama: `experiment/techniques-kaggle-heavy-v0.4`  
HEAD previo al checkpoint: `c693160cd5208585b5b3e0656d998ae1b46e7dfd`

## Guardias

- No tocar `main`.
- No mergear.
- No declarar CANON global automáticamente.
- Decisiones humanas prevalecen.
- No target win rate.
- No reabrir decisiones cerradas salvo bug verificado, inconsistencia cross-root o decisión humana explícita.
- No inventar valores faltantes: recuperar contrato, runner o artefacto real.
- Ultimates fuera de este balance ordinario.
- A07 no se reabre salvo bug.
- AI decide; motor resuelve.
- Runtime final: HTML único/autocontenido.

Objetivos HEAVY:
1. `WORST_SIBLING_REGRET`
2. `CONTEXT_POLARIZATION`
3. `NORMALIZED_PARAMETER_DISTANCE_FROM_CURRENT_DESIGN`

## Autoridades

Repositorio: `https://github.com/Shein25/La-Grulla-Blanca`

- Combat: `experiment/combat-stat-contract-v0.1` @ `64173e88a765228e48c54878c1362bca387bad51`
- Monster: `experiment/parallel-balance-npc-equipment-v0.1` @ `c7b87b84a80e0a42e20eec7574f860123685c782`
- LAB: `V04.1-KAGGLE-PORTABILITY-HOTFIX1`
- Asset commit HEAVY: `ac184bf496277eda78493262a1255f245d5c1d97`

Jugador de referencia:
- LI HP30 Qi37 basic1d4+4 scalar1.00
- LII HP36 Qi43 basic1d4+5 scalar1.08
- LIII HP42 Qi49 basic1d4+6 scalar1.16
- LIV HP48 Qi55 basic1d4+7 scalar1.24

Raíces:
- Fuego: +10% daño directo, +5 pp crítico
- Metal: +10 pp % penetration, +5 Precision
- Agua: -10% coste Qi, +5 Control
- Tierra: +10% HP máximo, +5 Tenacity
- Viento: +10 Evasion, +5 pp crit damage

# FUEGO — CERRADO PARA REVIEW DE RAÍZ

Estado:
- `CLOSED_FOR_ROOT_REVIEW`
- `READY_FOR_CROSS_ROOT_REVIEW`
- `GLOBAL_CANON: PENDING`

## Palma Ardiente
Selección humana: **F1 — TPE trial 188**
- `direct_pct/2: 15 -> 25`
- `eff/t1_t2_precision: 5 -> 6`
- `DOT_ROUTE_POTENCY_INCREMENT: 0.05 -> 0.04`
- Base: Qi6, `2d4+5`, 7–13 puro, sin equipo.

## Respiración del Cuerpo-Horno
Selección humana: **F2 — Sobol trial 54**
- `absorption_pct: 0.25 -> 0.30`
- `barrier_pp_each: 0.05 -> 0.04`
- `barrier_t1_t2_synergy_pp: 0.05 -> 0.04`
- `CONVERSION_RATE_INCREMENT: 0.10 -> 0.15`

## Círculo de las Cien Ascuas
Selección humana: **F0 BASELINE**
- Sin cambios.

# METAL — AUDITORÍA HEAVY

Original: `RESULTS_METAL_HEAVY.zip`  
Tamaño: 318426696 bytes  
SHA-256: `d7f5c14ec9106e4eb7caa4fb0f61323876c1c960a53fca05e9ac9fe9097ff987`

Reducido:
- `METAL_BALANCE_REVIEW_INPUT_V01.zip`
- `AUDITORIA_METAL.md`

Auditoría:
- 11837 miembros inspeccionados
- 5943 JSON
- 5884 Parquet
- 9 SQLite
- 11836 hashes de manifiesto verificados
- 808 trials cotejados
- cero corrupción/discrepancias detectadas
- tres objetivos MINIMIZE

Deep sólo cubre:
`base, 000, 111, 222, 012, 120, 201`

R64/R256/R1000 son incrementales/anidados, no experimentos independientes.

# METAL — DESTELLO DE PLATA

## DECISIÓN HUMANA APROBADA
**F0 BASELINE**

Estado: `APPROVED_FOR_ROOT_REVIEW`

Baseline:
- Qi6
- `2d4+4`
- +10 pp penetration propios
- raíz Metal además +10 pp % penetration y +5 Precision

Motivo:
- buscamos paridad cross-root con Fuego, no igualdad numérica;
- Palma debe conservar mayor daño bruto;
- Destello recupera terreno frente a DEF mediante penetración;
- F1 elevaba damage flat 4->5 y mostraba 350 ganancias profundas / 0 pérdidas, señal de buff general;
- F0 mantiene mejores objetivos HIGH aunque conserva un par universal dominado.

Nota cross-root:
si Destello queda materialmente atrás frente a las otras ofensivas unitarget, crear un ajuste mínimo específico. No adoptar F1 completo automáticamente.

# METAL — ARMADURA DE PLATA

Estado: `OPEN — HUMAN_MICROLAB_REQUIRED`

Baseline/F0/F2 numéricamente equivalente:
- Qi7
- DEF/placa3
- FIRST=1
- LATER=2

Congelado:
- `adapt_tenacity_by_count/1 = 5`
- no tocar en este micro-lab.

## F1 HEAVY
- Qi7
- DEF3
- FIRST1
- LATER1
- regret HIGH ~0.0711368
- elimina los 5 pares universalmente dominados
- 13 pérdidas materiales profundas
- peor celda ~-0.101824

## F5 HEAVY
- Qi7
- DEF4
- FIRST1
- LATER2
- 125 ganancias profundas
- 0 pérdidas
- regret casi baseline
- quedan 4 pares universales

## F7 — CANDIDATO HUMANO NUEVO
- Qi6
- DEF3
- FIRST1
- LATER1

Hipótesis:
conservar la corrección estructural de F1 y compensar parte de la pérdida mediante coste Qi, sin introducir el buff acumulativo DEF/placa de F5.

F7 NO está aprobado.

# MICROLAB ARMADURA F7 — PRÓXIMO PASO

Comparar F0/F1/F5/F7.
No Sobol, TPE ni NSGA-II.
No búsqueda paramétrica.

## Paso A — HIGH R64
- mismas 40 rutas
- mismos contextos
- mismas seeds/CRN
- mismas policies
- mismos loadouts
- mismos monstruos
- mismo runner/contrato HEAVY

Abort guard:
si F0/F1/F5 no reproducen los agregados conocidos dentro de tolerancia, marcar `CONTROL_REPRODUCTION_FAIL`, conservar evidencia y NO interpretar F7.

## Paso B — DEEP R256
Sólo si controles reproducen y F7 no es claramente inválido.

Rutas:
`base,000,111,222,012,120,201`

## Paso C — R1000
Sólo si F7 sigue prometedor.
Usar F7 y controles mínimos necesarios.

Gates humanos:
- ideal 0 pares universalmente dominados;
- regret cercano a F1 (~0.071) y claramente mejor que baseline (~0.126);
- reducir de forma importante las 13 pérdidas materiales de F1;
- peor celda bastante menos severa que ~-0.10;
- evitar buff global excesivo;
- no superar sistemáticamente a Cuerpo-Horno.

Entregable esperado:
`ARMADURA_PLATA_F7_MICROLAB_REVIEW_V01.zip`

# METAL — LLUVIA DE FILOS

Todavía NO ratificada humanamente.

Candidato principal actual:
**F2 — Sobol trial 194**

HIGH:
- baseline regret 0.1114210591
- F2 regret 0.0861029912
- polarización 0.1182768461
- distancia 0.1657407407
- 0 pares universales

Cambios F2:
- base % pen 10->14
- direct_pct/0 15->10
- direct_pct/1 20->15
- full crit pp 5->4
- rupture t1_t2 pen 5->4
- eff precision 5->4
- eff full pen 5->10
- SHRED_DEF_INCREMENT 1->2
- BASE_DAMAGE_FLAT_MODIFIER 1->2

Deep R1000:
- Δ utilidad media ~+0.027205
- 609 ganancias materiales
- 0 pérdidas materiales
- peor celda observada 0

Esperar decisión humana tras Armadura.

# Orden de continuidad

1. Ejecutar/auditar micro-lab Armadura F7.
2. Decidir Armadura.
3. Revisar y ratificar/rechazar Lluvia F2.
4. Cerrar Metal.
5. Continuar raíces restantes.
6. Cross-root review de las 15 técnicas.
7. Sólo después decidir CANON global.
8. Luego: player power envelope -> monstruos -> Ultis -> veteran/full envelope -> bosses.

# Inicio del nuevo chat

El chat nuevo debe:
- leer este handoff completo;
- verificar HEAD real de `experiment/techniques-kaggle-heavy-v0.4`;
- no reabrir Fuego;
- respetar Destello F0 como decisión humana aprobada;
- no aceptar F7 antes del micro-lab;
- no declarar Lluvia F2 CANON antes de ratificación;
- registrar decisiones nuevas en este flujo de backups Git.
