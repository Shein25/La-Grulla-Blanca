# La Grulla Blanca — PRE-A08 V26: Concordancias condicionales, batería de balance puro

**Fecha:** 2026-10-09. **Estado:** `LAB PASS PARA HIPÓTESIS FÍSICAS; REGLAS NUMÉRICAS CONDICIONALES SIN RATIFICAR.` **SIN FREEZE / SIN A08 / SIN RUNTIME**.

## 1. Alcance y continuidad

Este frente sigue V25 y verifica los seis handlers del preflight bloqueado. No reejecuta V17–V25. Monstruos normales V19 **originales** (Araña, Búho, Zorro, Murciélago, Cangrejo, Jabalí), T1/T2 adaptativos, 16 builds por raíz (incluye 4 que eligieron la familia Tramo I pertinente), EARLY y DELAYED_TRIGGER, equipo **M03** y **Sobretúnica DEF+1/HP+2** como controles; la Sobretúnica DEF+1 **no se aplica al catálogo canónico**. Sin precios, comercio ni NPC. No `main`, merge, HTML, `ROOMS.exits`, A07, IA ni runtime.

Fuente: V17 `CONCORDANCIAS_DEF_LII_V17_CANDIDATE.json` (status `DESIGN_CANDIDATE_FOR_MONSTER_LAB__NOT_HUMAN_RATIFIED_NOT_RUNTIME`; `conditional_effects_physical_validation=false`), y motor LAB V24 derivado de `LI_V04B_REFERENCE_RUNNER` / `etapa19b_combat_engine.py`.

**Precaución decisiva:** V17 NO fijó todas las fórmulas de magnitud para `REACTIVE_RESPONSE` e `INTERNAL_RESOURCE`. V26 usó, como **hipótesis diagnóstica exclusivamente**, un multiplicador relativo `(1+scale V17)` sobre la precisión de respuesta local o sobre la tasa de conversión de calor. Para QI, `qi_cost_raw × (1-scale)` con HALF_UP una sola vez después de la eficiencia local. **Ni fórmulas ni deltas de victoria son propuestas canónicas.**

## 2. Duelos ejecutados

- DISCOVERY, semillas `100100–100103`: **36.864**.
- HOLDOUT, semillas `100500–100503`: **36.864**.
- **73.728 duelos nuevos**; 36.864 contextos de `BASE` frente a `CONDITIONAL` pareados por RNG y atributos. **0 timeout; 0 due_missed**.
- **9.216 pares** con familia condicional realmente elegida; **27.648 pares** sin familia elegida: **exactamente idénticos** en los indicadores de combate entre ambos brazos.
- La batería COLD (semilla 100100, 1 repetición) reconstruyó **9.216 filas y 35 columnas de métricas exactamente** comparadas con DISCOVERY, salvo la etiqueta `cohort`; no son duelos nuevos.
- `7.720` activaciones condicionales reales entre todos los brazos `CONDITIONAL` válidos (incluidos T1 y T2). 446 contextos elegibles modificaron el vencedor.

## 3. Diferencias de victoria T2: solo seleccionadores Tramo I

Se enfrentan `BASE` versus la opción `CONDITIONAL` exclusiva, nunca suma automática de ambos. Ambos equipos de referencia combinados, 768 pares por relación.

| Relación / elección | N pareado | Victoria BASE | Victoria CONDICIONAL | Δ |
|---|---:|---:|---:|---:|
| Agua → Fuego / Calor | 768 | 75.91% | 75.91% | +0.00 pp |
| Agua → Viento / Respuesta | 768 | 61.85% | 55.47% | -6.38 pp |
| Metal → Agua / Qi | 768 | 64.45% | 69.79% | +5.34 pp |
| Viento → Agua / Qi | 768 | 64.06% | 70.83% | +6.77 pp |
| Metal → Fuego / Calor | 768 | 74.09% | 73.44% | -0.65 pp |
| Tierra → Fuego / Calor | 768 | 73.83% | 73.44% | -0.39 pp |

### Estabilidad entre cohortes (T2)

| Relación | Δ Discovery | Δ Holdout |
|---|---:|---:|
| Agua → Fuego / Calor | +0.00 pp | +0.00 pp |
| Agua → Viento / Respuesta | -7.03 pp | -5.73 pp |
| Metal → Agua / Qi | +4.95 pp | +5.73 pp |
| Viento → Agua / Qi | +7.29 pp | +6.25 pp |
| Metal → Fuego / Calor | -0.52 pp | -0.78 pp |
| Tierra → Fuego / Calor | -0.26 pp | -0.52 pp |

## 4. Hallazgos de funcionamiento y balance

**Agua → Fuego / CONVERSION:** BASE era `NONE`. La activación condicional existe para quien ha elegido la familia CONVERSION de Cuerpo-Horno; el consumidor nativo transforma más absorción en Calor (fixture 0,4 → 0,44), con cap de calor y barrera inalterados. En el bloque T2 la conversión no cambia victorias, pese a algunos HP finales diferentes. **Investigar cap, cantidad de impactos y consumo de Calor antes de aumentar números.**

**Agua → Viento / RESPONSE:** con familia RESPONSE elegida, la respuesta tras **evasión exitosa** aumenta la precisión local de `5→6` en el fixture. El efecto reemplaza, no suma, el aumento de duración BASE de Paso de Nube (`4 vs 5 turnos` en fixture). Esta pérdida de duración pesa más que la mejora condicional: alrededor de **−6,38 pp en T2**. Esto es una **alerta de elección dominada potencial**, no un error demostrado en el juego. Examinar si el efecto condicional debería ofrecer una contraprestación comparable, con decisión humana posterior y una regla cuantitativa explícita.

**Metal/Viento → Agua / EFFICIENCY:** orden `DECLARE > PREVIEW > QI local multiplicativo > validación/pago > COMMIT`; HALF_UP una vez. Con la especialización EFFICIENCY T1 del Espejo, `raw 4,5→4,05 (Metal)` o `3,825 (Viento)`, redondeo `5→4 Qi`. Sustituye, no suma, el refuerzo BASE de reflujo de absorción. Mejora victoria +5,34/+6,77 pp T2. **El Qi medio TOTAL gastado por pelea puede SUBIR porque se sobrevive más y se realizan más técnicas; no confundir con mayor coste por activación.**

**Metal/Tierra → Fuego / CONVERSION:** cuando Tramo I elige CONVERSION, la conversión a calor reemplaza refuerzo de absorción BASE. Fixturas: tasa `0,40→0,48` o `0,44`, con cap sin cambios. La pérdida de absorción BASE es más influyente que este incremento: cambios pequeños de victorias y HP. Las magnitudes de conversión son diagnósticas no ratificadas; no modificar todavía.

### La Araña revela un problema de evento, no de balance

El ataque especial sin daño directo que aplica veneno incrementaba la evasión del jugador, pero el motor LAB antiguo no creaba la respuesta de Paso de Nube desde esa ruta, solo desde `resolve_monster_direct`. V26 añadió **un adaptador simétrico para BASE y CONDITIONAL**, reconociendo la evasión tanto en ataques directos como especiales. Las pruebas mecanicistas verifican `una sola respuesta` en cada caso y que el segundo golpe no la multiplica otra vez. **Esto no modifica el motor canónico y no valida persistencia poscombate de veneno.**

## 5. Cobertura y limitaciones

PASS: seis rutas reconocidas según `receiver + source + familia Tramo I`, un único hook prioritario, consumo del Eco por defensa efectiva, exclusión de doble efecto, negativo por eco del mismo elemento, `QI PRE_COST HALF_UP`, response solo tras evasión, Calor nativo ligado a absorción, control ON/OFF idéntico cuando familia no seleccionada, semillas pareadas, 0 cadencias omitidas, monstruos originales restaurados y 9.216 casos reproducibles.

NO APROBADO: magnitudes condicionales V17, estadística base productiva `NEW_COMBAT_STATS`, equipamiento/consumibles runtime, activación de estas hooks dentro del HTML ver76, adquisición real de técnicas ajenas, persistencia de aflicciones al terminar duelo y tratamientos. No representa T3/T4, mini-jefes ni AOE. No inferir balance final del Arco 1 entero.

## 6. Dictamen y próximo bloque

1. **No tocar precios** ni comercio. Mantener Sobretúnica DEF+1/HP+2 como candidato apoyado por V23–V25, aún no ratificado.
2. **No aprobar** la respuesta Viento ni eficiencias de Qi por estos porcentajes: son sensibilidad físico-comparativa de reglas provisionales. Solicitar/decidir fórmula definitiva después de revisar el trade-off.
3. La conversión a Calor (tres rutas) necesita traza de impacto→absorción→reserva de Calor→disparo; igual que Embalse, no aumentar escala sin mecanismo probado de utilidad.
4. **Próxima batería V27:** persistencia postcombate de veneno y quemaduras, antídotos y bálsamos, coste de curación en oportunidades de acción. Depende de localizar y verificar contrato real de aflicciones: sin inventar reglas.
5. A08/Astra continúa esperando **cierre numérico**. No implementar B01 hasta entregar cifras definitivas y aprobación humana.

### Reproducción

Código `run_v26_conditional.py` y `analyze_v26.py`; `RAW_V26_DISCOVERY.csv.gz`, `RAW_V26_HOLDOUT.csv.gz`, `RAW_V26_COLD.csv.gz`; `PAIRED_V26_FULL.csv.gz`; `SUMMARY_V26_PAIRED.csv`, `SUMMARY_V26_BY_COHORT.csv`, `SUMMARY_V26_BY_MONSTER.csv`; controles `QA_V26_*.json`.