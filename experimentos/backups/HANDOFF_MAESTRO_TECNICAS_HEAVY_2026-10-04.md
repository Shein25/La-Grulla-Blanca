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


---

# ACTUALIZACIÓN MAESTRA — 2026-10-05

> **AUTORIDAD DE CONTINUIDAD:** este bloque supersede cualquier sección anterior incompatible de este mismo handoff.  
> No borrar el histórico previo: queda preservado como trazabilidad de decisiones.

## 1. Backup Git previo a esta actualización

Antes de modificar este handoff se creó una copia exacta del estado anterior:

- Ruta: `experimentos/backups/HANDOFF_MAESTRO_TECNICAS_HEAVY_2026-10-05_PRE_UPDATE_BACKUP.md`
- Commit de backup: `5dd7f27a3b79fe7d79eb618a7cd119d4407b502c`
- Rama: `experiment/techniques-kaggle-heavy-v0.4`
- `main` NO tocado.
- Sin merge.

## 2. Estado global de las 15 técnicas ordinarias — V0.2

Estado actual:

`PROVISIONAL_REBALANCE_PENDING_PASO_NUBE_HORIZONTAL_LAB`

Patrón provisional humano vigente:

- **Fuego:** F1 / F1 / F0
- **Metal:** F1 / F5 / F2
- **Viento:** F0 / F1 / F2
- **Tierra:** F0 / F2 / F2
- **Agua:** F0 / F1 / F1

Este patrón supersede el V0.1 anterior donde:
- Cuerpo-Horno estaba en F2;
- Destello estaba en F0;
- Armadura estaba en F7/F0 según checkpoint intermedio.

No reabrir las otras 14 técnicas salvo:
- bug verificado;
- nueva inconsistencia cross-root material;
- decisión humana explícita.

## 3. Cambios V0.2 que quedaron ratificados provisionalmente

### Fuego

#### Palma Ardiente — F1 KEEP
- `direct_pct/2: 15 -> 25`
- `eff/t1_t2_precision: 5 -> 6`
- `DOT_ROUTE_POTENCY_INCREMENT: 0.05 -> 0.04`
- Estado: `WATCH_FIRE_UNITARGET`
- No nerfear sólo porque Fuego conserve la media unitarget más alta.

#### Respiración del Cuerpo-Horno — F1
Cambio respecto al checkpoint viejo F2:
- conservar únicamente `barrier_t1_t2_synergy_pp: 0.05 -> 0.04`
- NO aplicar:
  - `absorption_pct 0.25 -> 0.30`
  - `barrier_pp_each 0.05 -> 0.04`
  - `CONVERSION_RATE_INCREMENT 0.10 -> 0.15`

Motivo:
el CROSS-ROOT V0.1 mostró que F2 elevaba demasiado el techo defensivo. F1 corrige esto sin desmontar la identidad de Fuego.

#### Círculo de las Cien Ascuas — F0 KEEP
Sin cambios.

### Metal

#### Destello de Plata — F1
Supersede la decisión vieja F0.

Cambios:
- `penetration/t1_percent_pp: 10 -> 11`
- `penetration/t2_flat: 3 -> 2`
- `execution/crit_pp/2: 5 -> 7`
- `BASE_DAMAGE_FLAT_MODIFIER: 4 -> 5`

Motivo:
el CROSS-ROOT V0.1 mostró déficit unitarget claro de Metal. F1 lo recupera sin convertirlo en daño bruto de Fuego.

#### Armadura de Plata — F5
Supersede F7 y el estado abierto del micro-lab.

Cambio:
- `base_defense_per_plate: 3 -> 4`

Mantener:
- `qi_cost = 7`
- `RESISTANCE_LATER_DEF_INCREMENT = 2`

F7 queda descartado.

Control V0.2 F5 vs F0:
- Δ utilidad media aproximada: `+0.03583`
- 333/476 celdas con ventaja material
- 0 pérdidas materiales
- 473/476 celdas con media positiva

No crear F8/DEF5 sin un nuevo microtest explícito.

#### Lluvia de Filos — F2 KEEP
Cambios:
- base % pen 10 -> 14
- `direct_pct/0: 15 -> 10`
- `direct_pct/1: 20 -> 15`
- crit 5 -> 4
- rupture T1/T2 pen 5 -> 4
- eff precision 5 -> 4
- full pen 5 -> 10
- `SHRED_DEF_INCREMENT: 1 -> 2`
- `BASE_DAMAGE_FLAT_MODIFIER: 1 -> 2`

No buffear sólo por media AOE menor: su valor relativo debe aparecer contra DEF real mediante penetración + shred.

### Viento

#### Lanza que Parte Nubes — F0 KEEP

#### Paso de Nube Ligera — F1 PROVISIONAL / ÚNICO PENDIENTE
F1 actual:
- Qi 7 -> 6
- EVA inicial 35 -> 36
- `response_precision_by_count/1: 5 -> 6`

El CROSS-ROOT V0.2 confirmó que sigue siendo el único rezagado transversal claro de DEFENSE_UTILITY.

Estado:
`DIRECTED_HORIZONTAL_LAB_REQUIRED`

No aplicar buff automático.
No usar Optuna/NSGA-II global.

#### Tijera del Vendaval — F2 KEEP
- crit pp +1
- `DEBUFF_PRECISION_INCREMENT_2: 3 -> 2`
- `BASE_DAMAGE_FLAT_MODIFIER: 1 -> 2`

### Tierra

- Golpe de Montaña — F0 KEEP
- Piel de Cobre — F2 KEEP
- Temblor de Montaña — F2 KEEP

No reabrir por distancia paramétrica aislada mientras el cross-root siga sano.

### Agua

- Latigazo de Marea — F0 KEEP
- Espejo de Luna — F1 KEEP; Qi 7 -> 6
- Marea de las Ocho Orillas — F1 KEEP:
  - direct T1/T2 crit pp 5 -> 6
  - eff T1/T2 precision 5 -> 6
  - `BASE_DAMAGE_FLAT_MODIFIER: 1 -> 2`

## 4. CROSS_ROOT 15 — V0.2 R64 completado

La validación se ejecutó dividida en cinco notebooks/raíces y luego se revisó de forma transversal.

Integridad:
- 5/5 PART completados;
- 5/5 `NUMERIC_CONTROL_GATE = PASS`;
- mismo `MASTER_SEED = 2026100301`;
- mismo snapshot T0;
- mismo catálogo V0.2;
- sin Optuna/Sobol/NSGA-II en este gate.

Compactación por rol, V0.1 -> V0.2:

- UNITARGET spread: ~0.1200 -> **~0.0615**
- DEFENSE spread: ~0.1412 -> **~0.0577**
- AOE spread: ~0.0472 -> **~0.0214**

### Unitarget V0.2 aproximado
- Fuego / Palma F1: ~0.6244
- Metal / Destello F1: ~0.5797
- Agua / Latigazo F0: ~0.5735
- Tierra / Golpe F0: ~0.5678
- Viento / Lanza F0: ~0.5629

Conclusión:
Metal queda recuperado.
Fuego sigue alto pero queda en WATCH, no en nerf automático.

### Defensa V0.2 aproximada
- Fuego / Cuerpo-Horno F1: ~0.5741
- Agua / Espejo F1: ~0.5646
- Tierra / Piel F2: ~0.5606
- Metal / Armadura F5: ~0.5474
- Viento / Paso F1: ~0.5165

Paso F1:
- `cross_gap ≈ -0.0354`
- 0 ventajas materiales
- ~303 desventajas materiales / 476 contextos
- rezago presente en LI, LII, LIII y LIV

Conclusión:
**las otras 14 técnicas quedan congeladas provisionalmente; Paso es el único frente abierto.**

### AOE V0.2 aproximado
- Viento / Tijera F2: ~0.2519
- Fuego / Círculo F0: ~0.2498
- Tierra / Temblor F2: ~0.2329
- Agua / Marea F1: ~0.2308
- Metal / Lluvia F2: ~0.2306

Conclusión:
no reabrir AOE general.

## 5. AOE single-target scalar

Decisión humana congelada:

`AOE_SINGLE_TARGET_SCALAR = 0.65`

No reabrir salvo:
- bug claro;
- desequilibrio global severo posterior.

Aplica a magnitud ofensiva AOE reutilizable al golpear un único objetivo.
No se aplica a debuffs/control/duración.
Las Ultis AOE no usan este castigo: conservan 100% de magnitud.

## 6. Paso de Nube — Horizontal Lab V01

Objetivo humano:
**no elegir una variante simplemente más potente**, sino encontrar varias configuraciones horizontalmente válidas donde cada una tenga un nicho y ninguna haga obsoletas a las otras.

Notebook corregido vigente:
`KAGGLE_PASO_NUBE_HORIZONTAL_LAB_V01_FIX1.ipynb`

SHA-256 notebook:
`2ee7f59fba93762e88e39be6fcf31019fc55ed6b4a80fb7e8e4988c0b90c3bbf`

Paquete:
`PASO_NUBE_HORIZONTAL_LAB_V01_FIX1_PACKAGE.zip`

SHA-256 paquete:
`2a685d67776de03aa4040ed41564fa8b549e63af845c1fe6095885d494eeaabb`

Configuración inicial:
- `RUN_LAB = True`
- `R64_REPLICATES = 64`
- `WORKERS = 2`
- `RUN_R256 = False`
- `R256_VARIANTS = []`

Variantes diseñadas:
- F1_CONTROL
- LIGEREZA
- NUBE_PURA
- CONTRAGOLPE
- FLUJO_CONTINUO
- NUBE_AFILADA
- RESPUESTA_PRECISA
- IMPULSO_NUBE
- TRIPLE_EQUILIBRIO

Principio:
- no existe `automatic_winner`;
- una variante que haga obsoletas a las otras debe rechazarse aunque tenga mejor utilidad media;
- R256 sólo para 2–4 supervivientes nombrados explícitamente después del R64.

El FIX1 corrige el error:
`ModuleNotFoundError: campaign_analysis`
causado por importar antes de montar `heavy_inputs`.

Pendiente actual:
**esperar resultado `PASO_NUBE_HORIZONTAL_LAB_V01_RESULTS.zip`.**

## 7. Progresión AOE

Decisión humana vigente:
- LI/LII: sin AOE;
- LIII permite percibir/encontrar Guardianes AOE;
- `LIII_PRE_AOE`: antes de derrotar al guardián, sin AOE;
- `LIII_POST_AOE`: después de obtener el manual, AOE disponible;
- LIV no auto-desbloquea AOE: debe haberse adquirido legalmente.

Guardianes AOE:
- únicos;
- T0-only;
- 0 fases;
- no respawn tras derrota;
- manual garantizado;
- huir/salir reinicia el encuentro;
- sin atracción inter-room.

## 8. Ultimates — decisión humana más reciente, AUTORIDAD

**Este bloque supersede cualquier nota anterior que colocara la Ulti principal en LianQi III.**

Regla vigente:

### Ulti de la rama principal
Se desbloquea en **LianQi IV** sólo si el jugador ha alcanzado la **maestría completa de toda su rama**.

La condición es conocimiento/maestría alcanzada, **NO mantener puntos actualmente asignados en todas las especializaciones**.

Ejemplo humano explícito:
un build `2 / 2 / 2` no debe perder acceso a su Ulti por no tener puntos permanentes en una tercera rama concreta si ya alcanzó la maestría requerida.

### Ulti del injerto
Requiere simultáneamente:
- poseer el injerto;
- llegar a LianQi IV;
- alcanzar la maestría completa de toda la rama de ese injerto.

Misma regla:
la maestría aprendida habilita la Ulti; la distribución actual de puntos no debe encerrar al jugador en un build obligatorio.

Consecuencia de balance:
- Guardianes AOE de LianQi III deben evaluarse como `LIII_PRE_AOE` **sin Ulti**, salvo nueva decisión humana explícita;
- el power envelope de Ultis entra desde LianQi IV;
- conservar métricas `MAX_LEGAL_1_ACTION_BURST`, `MAX_LEGAL_2_ACTION_BURST`, `MAX_LEGAL_3_ACTION_BURST` cuando corresponda a LIV.

## 9. Orden de continuidad actualizado

1. Ejecutar `PASO_NUBE_HORIZONTAL_LAB_V01_FIX1` R64.
2. Auditar horizontalidad, no “ganador”.
3. Si quedan 2–4 opciones sanas, activar R256 sólo para esas IDs.
4. Elegir humanamente la identidad final de Paso.
5. Revalidar sólo lo necesario contra peers defensivos V0.2.
6. Congelar las 15 técnicas como autoridad provisional de simulación.
7. Construir player power envelope LI -> LIV respetando:
   - LI/LII sin AOE;
   - LIII PRE/POST AOE;
   - Ultis desde LIV según maestría.
8. T0 -> T4 monstruos.
9. Guardianes AOE.
10. Ultis / burst LIV.
11. Bosses / Grulla.

## 10. Guardias reforzadas

- No tocar `main`.
- No merge.
- No push/commit fuera de la rama autorizada.
- Decisiones humanas prevalecen.
- No inventar CANON.
- No volver a optimización global de técnicas por una anomalía local.
- Las otras 14 técnicas quedan congeladas mientras se resuelve Paso.
- No confundir “mejor score” con “mejor diseño”: horizontalidad y nicho importan.
- No hacer que una especialización sea estrictamente superior a otra.
- No introducir nuevas mecánicas de Paso fuera de las ya expresables/autorizadas sin decisión humana.
- AI decide; motor resuelve.
- `freeAiText=false`.
- Sin nuevo reloj/timers.
- A07 no se reabre salvo bug.
- Runtime final sigue siendo HTML único/autocontenido.

## 11. Punto exacto para retomar si se corta la conversación

Leer primero este bloque 2026-10-05.

Estado resumido:
- 14/15 técnicas V0.2 congeladas provisionalmente;
- Paso de Nube es el único ajuste abierto;
- CROSS_ROOT V0.2 R64 ya completado y mejoró fuertemente los tres roles;
- horizontal lab FIX1 preparado y pendiente de resultado;
- AOE scalar 0.65 congelado;
- Ultis se desbloquean en LIV por maestría, no por distribución actual de puntos;
- no tocar main / no merge.

Próximo artefacto esperado:
`PASO_NUBE_HORIZONTAL_LAB_V01_RESULTS.zip`.


---

# ACTUALIZACIÓN PASO DE NUBE — RESULTADO HORIZONTAL LAB V01 R64 — 2026-10-05

## Backup previo
- Ruta: `experimentos/backups/HANDOFF_MAESTRO_TECNICAS_HEAVY_2026-10-05_PRE_PASO_R64_RESULT_UPDATE.md`
- Commit: `ebe6f7597a5444bed99ed1fc4fa4d7f9e5d8b524`

## Artefacto recibido
- `PASO_NUBE_HORIZONTAL_LAB_V01_RESULTS.zip`
- SHA-256: `be79f711505c3ee1f333a8b53972708af8c4b733c0b1ff286216782f3321e3b0`
- Tamaño aproximado: 2.57 MB
- 17 archivos.
- `PACKAGE_MANIFEST.json`: 16/16 entradas verificadas por hash y tamaño.
- `NUMERIC_CONTROL_GATE = PASS`
- Error máximo del control histórico: `2.22e-16`.

## Resultado principal
`HORIZONTAL_VIABLE_SET_R64.status = NO_MULTI_OPTION_HORIZONTAL_SET_YET`

No hubo ninguna variante horizontalmente válida en V01.

### F1_CONTROL
- utility_mean: `0.516458`
- cross_gap: `-0.035385`
- material disadvantages: `303/476`
- regret: `0.052311`
- polarization: `0.042843`
- distance: `0.107143`
- falla por gap transversal y por máximo gap de etapa.

### NUBE_AFILADA — mejor punto de partida
Parámetros:
- Qi 6
- EVA inicial 37
- EVA por mejora 6
- response precision 5
- response crit 4
- eff flat -1
- eff mult 0.95

Resultados:
- utility_mean: `0.523593`
- cross_gap: `-0.029418`
- material disadvantages: `263/476`
- regret: `0.069659`
- polarization: `0.069060`
- distance: `0.238095`
- 0 pares hermanos universalmente dominados.
- no queda dominada por otra variante.
- **sólo falla el gate global `abs_cross_gap_mean <= 0.020`.**
- máximo gap por etapa queda dentro del gate (`~0.03944`).

Conclusión:
`NUBE_AFILADA` es el ancla para el siguiente diseño, pero NO está aprobada todavía.

### NUBE_PURA
- utility_mean: `0.523480`
- cross_gap: `-0.029459`
- regret: `0.077636`
- falla además en LII y regret.
- no preferir frente a NUBE_AFILADA.

### Resto
CONTRAGOLPE, FLUJO_CONTINUO, IMPULSO_NUBE, LIGEREZA y RESPUESTA_PRECISA quedan materialmente por debajo o dominadas por otra variante.
TRIPLE_EQUILIBRIO sigue débil y además excede regret/distance.

## Decisión de continuidad
**NO ejecutar R256 todavía.**

Motivo:
R64 ya muestra que ninguna variante V01 entra al rango horizontal. Aumentar réplicas sólo confirmaría con más precisión una insuficiencia de diseño conocida.

Próximo paso:
`PASO_NUBE_HORIZONTAL_LAB_V02`

Objetivo:
- partir de NUBE_AFILADA;
- mantener las otras 14 técnicas V0.2 congeladas;
- no reabrir Optuna/NSGA-II;
- introducir un refuerzo mínimo de base/identidad para Paso;
- volver a generar varias configuraciones horizontalmente válidas;
- ninguna opción puede hacer obsoletas a las otras;
- R256 sólo después de obtener 2–4 supervivientes R64 reales.

Estado nuevo:
`PASO_NUBE_V01_NO_SURVIVORS_V02_DESIGN_REQUIRED`

## Regla importante
No bajar el gate sólo para hacer pasar una candidata.
El objetivo sigue siendo corregir la técnica, no adaptar el criterio al resultado.


---

# ACTUALIZACIÓN PASO DE NUBE — FINAL CONFIRMATION V01 — 2026-10-05

## Backup previo
- Commit: `edbc22bc4046f952a141b2a39d755642998898c5`
- Ruta: `experimentos/backups/HANDOFF_MAESTRO_TECNICAS_HEAVY_2026-10-05_PRE_FINAL_CONFIRM_RESULT.md`

## Artefacto
- `PASO_NUBE_FINAL_CONFIRMATION_V01_RESULTS.zip`
- SHA-256: `29247e5fe30f71b091de1903b7fd3cbb25ce7c5cf5eca1670435f6bdfa28284a`
- Tamaño: 569725 bytes
- Manifest verificado completamente.
- `NUMERIC_CONTROL_GATE = PASS`.

## Resultado
`FINAL_GATE.status = FAIL_REVIEW_REQUIRED`

### F1_CONTROL
- utility_mean: `0.516458`
- cross_gap: `-0.035385`
- regret: `0.052311`
- polarization: `0.042843`
- material disadvantages: `303/476`

### INFERRED_FINAL probado
Parámetros:
- Qi 5
- EVA inicial 37
- EVA_each 7
- response PREC 5
- response CRIT 4
- eff_flat -1
- eff_mult 0.90

Resultados:
- utility_mean: `0.536088`
- cross_gap: `-0.019990` → PASS transversal
- material advantages: 7
- material disadvantages: 207
- regret: `0.091672` → FAIL
- polarization: `0.109432` → FAIL
- distance: `0.238095` → PASS
- universal dominated sibling pairs: 0
- hard dominance risk vs F1: TRUE

Gaps por etapa:
- LI: `-0.025733`
- LII: `-0.027511`
- LIII: `-0.020193`
- LIV: `-0.018813`

Interpretación:
el candidato alcanzó la potencia transversal necesaria, pero el refuerzo de `eva_each` deformó la horizontalidad interna y elevó regret/polarización. No congelar.

## Inferencia dirigida posterior
Con los 10 diseños R64 ya medidos, el patrón apunta a que el refuerzo debe ir principalmente a la base común y no al escalado de una especialización.

Candidato siguiente inferido, NO canon y pendiente de confirmación:
- Qi 5
- EVA inicial 38
- EVA_each 5
- response PREC 7
- response CRIT 5
- eff_flat -1
- eff_mult 0.90

Razonamiento:
- conserva el escalado evasivo interno de F1;
- usa un +1 adicional de EVA base respecto al techo histórico 37;
- refuerza la respuesta precisa sin inflar crítico;
- mantiene eficiencia sin cambios;
- distancia normalizada estimada: 0.25.

Predicción del modelo sobre los puntos medidos:
- cross_gap ~`-0.0196`
- regret ~`0.0471`
- polarization ~`0.0465`
- LI ~`-0.0326`
- LII ~`-0.0377`
- LIII ~`-0.0177`
- LIV ~`-0.0176`

IMPORTANTE:
esto es una inferencia/extrapolación un paso fuera del techo histórico de EVA inicial (37→38), no evidencia simulada todavía.

Estado:
`PASO_NUBE_FINAL_CONFIRM_V01_FAIL_INTERNAL_HORIZONTALITY_NEXT_DIRECTED_CANDIDATE_PENDING`

No ejecutar R256 del candidato fallido.


---

# DECISIÓN HUMANA — PASO CERRADO PROVISIONALMENTE / INICIO PLAYER POWER ENVELOPE — 2026-10-06

## Backup previo
- `experimentos/backups/HANDOFF_MAESTRO_TECNICAS_HEAVY_2026-10-06_PRE_PLAYER_ENVELOPE.md`
- commit: `08eea5fb2d2cf3a7f3493f8095007a173ee2f0d2`

## Paso de Nube Ligera — autoridad provisional de simulación

Por decisión humana se acepta la inferencia sin una nueva campaña dedicada.

Parámetros:
- Qi: **6**
- EVA base / `evasion_granted`: **40**
- `evasion_each`: **5**
- `response_precision_by_count/1`: **6**
- `response_full_crit_pp`: **5**
- `eff/t1_flat_cost`: **-1**
- `eff/later_mult`: **0.90**

Regla:
- NO potenciar especializaciones internas.
- El refuerzo pertenece a la base común de Paso.
- Estado: `PROVISIONAL_ACCEPTED_FOR_PLAYER_ENVELOPE`.
- No declarar CANON global todavía; podrá reabrirse sólo si el Player Power Envelope detecta una anomalía material atribuible a Paso.

## Las 15 técnicas ordinarias quedan congeladas como autoridad provisional de simulación

- Fuego: F1 / F1 / F0
- Metal: F1 / F5 / F2
- Viento: F0 / Paso base EVA40 con internals F1 / F2
- Tierra: F0 / F2 / F2
- Agua: F0 / F1 / F1

## Siguiente frente
`PLAYER_POWER_ENVELOPE_LI`

Arquitectura ratificada:
- 5 instancias Kaggle paralelas: FUEGO, METAL, AGUA, TIERRA, VIENTO.
- checkpoint/resume por instancia;
- persistencia pesada queda en Kaggle;
- Save Version puede reutilizarse como input sin descargar checkpoints;
- outputs REVIEW compactos para auditoría;
- consolidación LI sólo después de cerrar las cinco ramas;
- después: LII, LIII_PRE_AOE, LIII_POST_AOE, LIV.

Estado:
`PLAYER_POWER_ENVELOPE_LI_PREPARATION`


---

# PLAYER POWER ENVELOPE — LI PARALLEL V01 PREPARADO — 2026-10-06

Estado: `READY_TO_RUN_5_PARALLEL_ROOTS`

## Técnicas
Autoridad provisional:
- catálogo exacto CROSS-ROOT V0.2 fixed-set;
- parche humano adicional: `paso_nube.model_params.evasion_granted = 40`;
- SHA-256 catálogo resultante: `912b7824eff9149909ca21b9ad6290c6c82b1e1ea31867da1185c32df383d187`.

## Autoridades runtime
- Combat commit: `64173e88a765228e48c54878c1362bca387bad51`
- `etapa19b_combat_engine.py` blob: `e4650b615af2c63d91ea15347ac471432e7237da`
- `monster_new_engine_guard.py` blob: `02dee3e83a6ef160632f3b5acbb4da41d84c5418`
- Monster/equipment commit: `c7b87b84a80e0a42e20eec7574f860123685c782`
- monster registry blob: `26979e85a3679f33c32404e601c3dfbc72d0ce44`
- equipment catalog blob: `f3ba217b834eb0c2bb4156b12d4f7e8b9990263f`

## Legalidad LI
- 0 puntos de especialización.
- AOE bloqueado.
- Ultis bloqueadas.
- T0-only en este frente.
- 5 monstruos LI nativos.
- 6.144 loadouts estructurales de equipo.
- 4.864 firmas mecánicas deduplicadas.
- políticas de motor usadas: `UNITARGET_FIRST`, `DEFENSE_OPEN`.
- NO usar `AOE_FIRST` ni `ROTATION` en LI.

## Carga por instancia
- 48.640 celdas screen por raíz.
- R12 screen = 583.680 combates por raíz.
- refinamiento R128 dirigido a extremos, frontera, presión de Qi, supervivencia y loadouts de referencia.
- cinco instancias en paralelo.

## Checkpoint / resume
- SQLite acumulativo por rama.
- transacciones atómicas por batch.
- hashes SHA-256 por batch.
- seeds deterministas.
- `PLAYER_ENVELOPE_CHECKPOINT.json`.
- al reanudar, adjuntar la última Kaggle Save Version de ESA MISMA RAMA como Input.
- jobs confirmados no se repiten.
- fuentes descargadas sólo en primera ejecución; una Save Version posterior las reutiliza.

## Notebooks
- FUEGO: `KAGGLE_PLAYER_ENVELOPE_LI_FUEGO_V01.ipynb`
  - SHA-256 `d0aefa08f647c559b4c248cf348cd7e0daf016eee2a20904b2c4fea774fd75f8`
- METAL: `KAGGLE_PLAYER_ENVELOPE_LI_METAL_V01.ipynb`
  - SHA-256 `607dae6d338c7b07d8f4a50ca71c4a2e8e40e015f28a45e37ce7db7df7b12dc4`
- AGUA: `KAGGLE_PLAYER_ENVELOPE_LI_AGUA_V01.ipynb`
  - SHA-256 `0bef2c52f78edba884f398c9b840ec01b7fc04f773a8c6d246f06db1b915f7ce`
- TIERRA: `KAGGLE_PLAYER_ENVELOPE_LI_TIERRA_V01.ipynb`
  - SHA-256 `8f0bff240f5482a5f8a8b1649798c5eff5fce8430308ff65badce8868896a4ce`
- VIENTO: `KAGGLE_PLAYER_ENVELOPE_LI_VIENTO_V01.ipynb`
  - SHA-256 `f786ebd38e6d42400b73720bc80922522b2a545589daab7a5a53937ba7fcacbb`

Paquete conjunto:
- `KAGGLE_PLAYER_ENVELOPE_LI_5_ROOTS_V01.zip`
- SHA-256 `ccb36d4880337e462958d03b36c9aa37c0bff6d01a0ddac507fc47241a0824ce`

## Entregables al terminar
Pasar únicamente:
- `PLAYER_ENVELOPE_LI_FUEGO_REVIEW.zip`
- `PLAYER_ENVELOPE_LI_METAL_REVIEW.zip`
- `PLAYER_ENVELOPE_LI_AGUA_REVIEW.zip`
- `PLAYER_ENVELOPE_LI_TIERRA_REVIEW.zip`
- `PLAYER_ENVELOPE_LI_VIENTO_REVIEW.zip`

Los SQLite/checkpoints pesados se quedan en Kaggle.

Próximo gate:
`LI_5_ROOTS_COMPLETE -> CROSS_ROOT_LI_CONSOLIDATION`
