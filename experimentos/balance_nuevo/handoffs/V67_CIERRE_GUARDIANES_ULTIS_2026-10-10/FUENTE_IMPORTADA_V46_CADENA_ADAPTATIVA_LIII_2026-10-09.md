# LA GRULLA BLANCA — V46: cadena T0–T4 y Mutantes desde LianQi III

**Corte:** 2026-10-09  
**Estado:** `DESIGN_PROPOSAL + T0_VARIANCE_PRELIMINARY_LAB_PASS`; **NO** cierre ni activación de T3/T4 de LII/LIII.  
**Autoridad humana de esta ronda:** aprobadas las **seis identidades y diseños V45** como nuevo bestiario LIII; se permite revisar toda la cadena de monstruos repetibles de LI, LII y LIII desde la perspectiva de un jugador LIII. El balance arranca con **el mejor equipo LII**, no equipo LIII gratuito. Esta aprobación de diseño no transforma automáticamente `stats_status=PENDING_INTEGRAL_REBALANCE` o un candidato P5/A5 en cierre numérico humano.

## 1. Alcance real y cierres inmutables

| Cohorte | Identidades | T0 | T1–T2 | T3 | T4 | Mutantes |
|---|---:|---|---|---|---|---|
| **LI** | 5 (rata, serpiente, avispa, mono, lobo) | Congelado | Congelados | **Congelado** | **Congelado** | Variación v0.4 + sufijos v1 congelados |
| **LII** | 2 (Sapo Ceniza, Escarabajo Hierro) | Congelado | Congelados | Diseño causal previo; freeze PENDIENTE | Sólo propuesta, bloqueado hasta cerrar T3 | Sobres históricos **no activos**, pendientes de ratificación |
| **LIII** | 8 (Pez, Anguila, seis nuevos V45) | P5/A5 y V45 candidatos | Propuestas nuevas | Propuestas condicionadas | Propuestas condicionadas | Sobres nuevos experimentales, NO aprobados |

**Excluidos:** Eco del Caído, Sombra Ahogada, Guardián Coral, Sapo Caldera, Rey Escarabajo, Mantis y Custodio de Tierra; son únicos/élite/jefes. No T1–T4, no Mutantes, no T5. Los 5 guardianes AOE se tratarán después y por su contrato propio.

**LI no se recalibra ni se vuelven a correr las campañas cerradas.** Autoridades: `LI_ADAPTIVE_CHAIN_T0_T4_FINAL_CLOSURE_2026-10-06.md`, `T3_LI_FINAL_FREEZE`, `T4_LI_FINAL_FREEZE`, `MUTANT_SUFFIX_FINAL_FREEZE`. El T3 LI exige que T2 haya predicho y que T1 haya cambiado causalmente la defensa; T4 sustituye sólo BASIC, después de T1 y la técnica canónica. Ningún cambio automático por ascenso del personaje.

**LII también está protegido:** T1 del Sapo, MITIGATE_NEXT 60 % / CD3 / reacción; T1 Escarabajo DEFENSE_UP +4 / CD3 / reacción; T2 memoria 2, repetición 2, resultado EFECTIVA, anticipación 40 % HP o golpe ≥15 % HPmax y prioridad T1 natural 30/20. T3 propuesto en el plan de Git **no está cerrado**; su counter es el BASIC de instancia `1d2+5` (Sapo) / `1d2+3` (Escarabajo), sólo después de un nexo causal auténtico. No reabrir T0–T2. Existe un gate de equipo LII V02 de 1.310.720 peleas históricas, con hotfix posterior de agregación; **recuperar el REVIEW y verificar su cierre, NO repetir la campaña por defecto**.

## 2. Pipeline autoritativo y tiers

```
species_id T0 floor
 -> q_axis individuales, independientes, una vez por instancia
 -> stats/técnica efectiva de instancia
 -> clasificación Mutante y sufijos de los mismos q_axis
 -> tier adaptativo de la población local, obtenido por presión real del jugador
 -> kit adaptativo acumulativo T0..tier
 -> IA del monstruo decide
 -> motor resuelve con daño/DEF/EVA/Abs/Qi y eventos reales
```

**No** hay escalado universal `+X% HP/daño por tier`. Los tiers son aprendizaje, defensa, reconocimiento y contrajuego, no un aumento automático de monstruos por estar en LIII. Un LI puede naturalmente llegar a T4 por presión sostenida, incluso antes de que el jugador suba de etapa. **Mutante no aumenta `maxTierReached`** ni sustituye T1/T2/T3/T4. Mutante + T4 puede coexistir si ambos fueron obtenidos independientemente.

## 3. Propuestas T1–T4 para los ocho normales LIII

Todas las cifras de esta tabla son **hipótesis V46, no parámetros READY**. Los daños canónicos y la cadencia se leen del individuo T0 y nunca se regeneran según tier.

| Monstruo | T1: reacción posible (30/20, CD3) | T2 | T3: contraataque causal | T4 propuesto (CD7) |
|---|---|---|---|---|
| Pez Lunar | Mitigar 35% próximo directo conectado | Reconocimiento corto | BASIC de instancia `1d2+7`, si la mitigación evitó daño | Mordida de Corriente: reutilizar técnica |
| Anguila Estelar | EVA +8 siguiente acción ofensiva | Ídem | BASIC `1d2+6`, sólo si el +8 provocó esquiva | Mordida del Meridiano Azul, drenaje **5 Qi intacto** |
| Garza Brumosa | EVA +8 siguiente acción ofensiva | Ídem | BASIC `1d2+6` tras esquiva causal | Pico de Niebla Cortante |
| Cangrejo de Laja | DEF +2 siguiente acción ofensiva | Ídem | BASIC `1d2+6` si +2 DEF impidió daño | Tenaza de Pizarra |
| Sanguijuela Turbia | Mitigar 35% próximo directo conectado | Ídem | BASIC `1d2+6`, **sin nuevo DOT** | Mordida de Limo Frío; veneno base intacto |
| Salamandra Tibia | Mitigar 35% próximo directo conectado | Ídem | BASIC `1d2+6`, **sin nuevo DOT** | Salpicadura Irritante; quemadura base intacta |
| Rana de Cascajo | DEF +2 siguiente acción ofensiva | Ídem | BASIC `1d2+6` tras mitigación por DEF | Salto de Cascajo |
| Carpa Reflejada | EVA +8 siguiente acción ofensiva | Ídem | BASIC `1d2+6` tras esquiva causal | Succión de Corriente, drenaje **3 Qi intacto** |

- **T1 experimental:** reacción cuando HP ≤30 % o daño recibido ≥20 % de HPmax; CD3; no consume acción propia. `MITIGATE_NEXT` persiste ante miss y solo se consume por impacto directo conectado. `EVADE_NEXT`/`DEFENSE_UP` consumen la siguiente acción ofensiva pertinente. Una sola reserva activa. Sin defensa permanente.
- **T2 experimental:** ventana de dos acciones EFECTIVAS y dos repeticiones de la misma categoría; anticipación ≤40 % HP o golpe ≥15 % HPmax; no mira raíz/build, comandos futuros ni RNG futuro. El T1 natural tiene prioridad. No cancela acciones canónicas.
- **T3 experimental:** **solo** tras predicción confirmada **y** mitigación materialmente causal de T1. Para EVA se compara el mismo roll que conectaba contra la EVA natural y falló únicamente por T1; para DEF y mitigación se compara el mismo packet conectado con y sin T1. Un miss natural y una barrera de Mutante **nunca** son causalidad T1. Contraataque BASIC plano/dados de la **instancia**, pipeline normal, sin DOT/drenaje/control adicional, sin artificial `once_per_fight` y sin quitarle su acción ordinaria.
- **T4 experimental:** nunca altera la cadencia ni los parámetros del especial. CD7 como punto de partida **por probar**; reemplaza únicamente BASIC cuando la técnica canónica no está due y no está priorizada una reacción T1. Reutiliza el especial original sin crear un nuevo tipo de efecto. **Se deberá comprobar si adelantar un DOT/drenaje mediante T4 causa acumulaciones abusivas** y diseñar un límite de instanciación si el contrato común así lo exige. No atribuir ese límite al juego actual.

La propuesta de T4 LII es reutilizar Nube de Hollín/Carga de Caparazón como sustitución de BASIC bajo las mismas prioridades, **sin cambiar sus números**, y permanece bloqueada hasta ratificar T3 LII. Se probará contra LI/LII/LIII reales y contra Mutante; no heredará sin revisión el freeze LI.

## 4. Variación natural y Mutantes

**Contrato congelado:** q_axis uniforme [0,1] independiente por **eje realmente variable**, una vez por instancia; stat efectiva nunca debajo del piso T0, eje colapsado al piso no cuenta; score Mutante = media de q_axis; umbral depende de cantidad de ejes (5 ejes: 0,8041703275; 6: 0,779195057; 7: 0,7595352057). Cola ≈0,75 %, siempre <1 %. No hay RNG adicional para sufijo. Todo Mutante es un individuo excepcional del mismo `species_id`, no un nuevo monstruo.

**Sufijos congelados para LI y propuestos para reuso sin cambio semántico en LII/LIII:**

- **Acorazado A15:** al primer cruce del monstruo a ≤50 % HP, absorción del 15 % de HP máximo, una vez.
- **Fugaz F25:** tras recibir un crítico, +25 EVA en la siguiente acción ofensiva del jugador.
- **Acechante C20:** tras fallar un ataque, +20 Precisión en el próximo ataque del monstruo.
- **Indómito I25:** +25 Tenacidad frente al primer intento de Control.
- **Voraz V2:** primer cruce del jugador a ≤40 % HP, siguiente BASIC ×1,5.

**Excepcional:** exactamente 2 q_axis ≥0,95. **Ascendido:** 3 o más. Heredan los grupos de habilidades representados por esos ejes sin duplicar el mismo grupo. Mutante especializado: menos de dos ejes extremos, familia dominante. Mutantes dan ×1,5 botín y XP de combate, **no** XP de oficio ni probabilidad de drop único ni tiers; no imponer WR mínimo del jugador.

### Sobres provisionales LII/LIII

`VARIANCE_PROPOSALS_V46.json` define 10 sobres candidatos: dos LII derivados de **upper evidence histórico, actualmente colapsado**, y ocho LIII nuevos que **no tienen evidencia histórica de techo**. Esta distinción está registrada por especie. Los ocho LIII usan exactamente cinco ejes variables de diseño: HP/DEF/EVA/PREC/TEN y/o daño básico/especial/DoT según su identidad. No se aumenta el Qi de monstruos ni Control/crit/cadencia/drenaje de Qi. Una tirada natural jamás puede empeorar el piso T0.

**Pendiente humano y técnico:** dar autoridad a la nueva envolvente de estadística LII/LIII tras T0 y paridad con eventos, sin alterar la v0.4 LI. Nunca cambiar el runtime de Mutantes solo por pasar estas pruebas hipotéticas.

## 5. Resultado de la batería realmente ejecutada

### A. Apariciones — diseño de rareza, SIN combate

- **1.600.000 apariciones nuevas:** 160.000 por cada una de 10 especies LII/LIII bajo sus **sobres candidatos**.
- **40.000 reproducciones prefijo COLD** exactamente comprobadas; no son muestras nuevas.
- Incidencia por especie de **0,6963 % a 0,7881 %**, siempre <1 %; medias y taxonomía en `MUTANT_INCIDENCE_V46.csv`.
- La reproducción demuestra estabilidad algorítmica **del nuevo prototipo**; no sustituye el cierre LI (2,5 M spawns + 404.480 combates históricos ya ratificados).

### B. Casos estructurales de adaptación y sufijos — NO son combates

- **1.903 escenarios de causalidad T3, precedencia T4, relación etapa↔tier y conservación de esquemas** ejecutados como casos estáticos/microresolver.
- **258 microcomprobaciones de sufijos** A15/F25/C20/I25/V2 y la frontera donde absorción de sufijo por sí sola no cuenta como T1 causal.
- Estos tests verifican un **contrato de diseño** local, NO que el motor productivo ya despache esas acciones.

### C. Peleas T0 — ETAPA19B real, sin efectos de sufijo ni tiers

- **15.360 combates nuevos** LIII 1v1, 5 raíces, 2 builds/raíz, 2 políticas, 2 sets máximos LII, 8 normales LIII, individuos FLOOR frente a **Mutantes estadísticamente extremos condicionados** (24 semillas/celda).
- **5.120 repeticiones COLD**: coincidencia exacta fila por fila, no sumadas a nuevas.
- **Cero timeouts**. AOE y Ulti excluidas; no se presupone torso M08.

| Normal LIII | Jugador vence: T0 piso, equipo LII DEF | Jugador vence: Mutante condicional, equipo LII DEF |
|---|---:|---:|
| Pez Lunar P5 | 90,00 % | 69,58 % |
| Anguila Estelar A5 | 90,00 % | 65,83 % |
| Garza de Bruma | 93,33 % | 72,71 % |
| Cangrejo de Laja | 93,12 % | **43,96 %** |
| Sanguijuela Turbia | 92,92 % | 61,67 % |
| Salamandra Tibia | 96,25 % | 66,67 % |
| Rana de Cascajo | 94,79 % | 70,21 % |
| Carpa Reflejada | 93,12 % | 60,42 % |

Cada celda `n=480`: 5 raíces ×2 builds×2 políticas×24 repeticiones. La selección condicional de Mutantes se sobre-representa de forma deliberada para el diagnóstico; esas victorias **NO reflejan la frecuencia real de 0,75 %**. Las tasas de T0 son distintas de V44/V45 porque **este subconjunto de builds está sesgado a OFF_II/BOTH_II** y no incluye los siete estilos de esas campañas. No comparar los porcentajes como si fueran cohortes idénticas.

**Cangrejo es riesgo focal**: baja ~49,16 puntos porcentuales de victoria antes de aplicar habilidades de sufijo o T3/T4. No es motivo automático de nerf: la mutación excepcional está diseñada para ser difícil. Hay que probar si produce softlocks, DEF impenetrable, Qi agotado o combate prolongado cuando coexiste con T4, especialmente en Agua/Metal/Viento.

### D. Qué NO se probó (prohibido declarar PASS)

- Ni un solo combate T1/T2/T3/T4 nuevo en V46; sólo microcontratos/fixtures.
- Los cinco efectos de sufijos se testearon en **microfixtures**, no en el runner 1v1.
- No se probó Mutante + T3/T4 real, IA/eventos integrados, encuentros 1v2/1v3, hordas/respawn, Control auténtico ni T0 de monstruos en el runtime.
- No se verificó gate de cultivo NEW productivo ni el acceso efectivo a equipo LII/LIII por economía/misiones.

## 6. Plan de pruebas posterior — gates estrictos

1. **LI regresión LIII:** usar freeze exacto, poblaciones LI T0 vs T3 vs T4 con armaduras máximas LII, 5 raíces, builds Tramo II y Mutantes raros. No recalibrar ni repetir 294.400 + 294.400 pruebas ya cerradas; solo un screen focal de nuevas interacciones LIII.
2. **LII T3:** recuperar `LII_T3_EQUIPMENT_SPACE_GATE_V02_REVIEW.zip` y su hotfix de postproceso de 1.310.720 combates antes de hacer nuevas corridas. Auditar causalidad real, no `causal=true` inventado. Si la suite histórica no cubre LIII, crear una extensión focal LIII; después solicitar freeze humano T3. **No activar T4 antes.**
3. **LII T4:** primer micro/holdout pareado T3 congelado vs T4 candidato, sólo BASIC reemplazable, técnica canónica preservada, CADENCE_COMPAT y cuatro raíces/modos de juego; mutantes históricos como estrés, siempre condicionados a aprobar el envelope.
4. **LIII T0:** ratificar numéricamente P5/A5 y seis V45 luego de revisar outliers por raíz. No elevar `PENDING` a `READY` como efecto de esta batería.
5. **LIII T1:** probar por especie defensa reactiva, cooldown, cadencia y costes; contraste T0/T1 pareado, sin conceder stat buffs permanentes. Freeze humano.
6. **LIII T2:** confirmar memoria/observabilidad, anticipación y ventaja defensiva sin cancelar especial canónico. Freeze humano.
7. **LIII T3:** comparación causal y contrajuego real, incl. miss natural vs EVA T1, DEF/pen, DOT que ignora DEF, evento de stun/Control cuando exista. Freeze humano.
8. **LIII T4:** reuso especial CD7 básico-only, evitar proc de DOT/Qi duplicado y ciclos de acción; frente a jugador recién ascendido, luego equipado M08/M11, y en estrés LIV cuando corresponda. Freeze humano.
9. **Mutantes combinados:** normal piso, normal alto, Mutante (y subgrupos especializado/excepcional/ascendido) × T0/T1/T2/T3/T4 × seis escenarios defensivos/ofensivos por raíz; muestra natural 0,75 % y oversample condicional separadas; verificar multiplicadores, taxonomía, población/respawn, no reaparición indebida y mismo registro especie.

Para cada gate: RNG/semillas pareadas por evento; mediana/P90 de duración, WR por raíz/build/gear/política, daño/absorción/DOT/Qi, #activaciones y procs causales, false triggers=0, timeout/NaN=0, si técnica canónica debida=conservada; clones individuales con semilla fija y manifest; alto estrés aparte. **Ningún freeze automático**.

## 7. Material exportado

`SPECIES_T0_T4_MATRIX_V46.json`: 15 especies y sus estados/técnicas; referencias LI inmutables.  
`VARIANCE_PROPOSALS_V46.json`: 10 envolventes de laboratorio, origen histórico vs creado.  
`MUTANT_INCIDENCE_V46.csv`: apariciones y tasas observadas.  
`MUTANT_SPECIMENS_FOR_SCREEN_V46.json`: individuos condicionales reproducibles, no metadata productiva.  
`SUMMARY_V46_MUTANT_T0_COMBAT.csv` y `RAW_V46_{HOLDOUT,COLD}.csv.gz`: combate y COLD reproducible.  
`run_v46_mutants.py`, `run_v46_combat.py`, `qa_v46_adaptive.py`, `qa_v46_suffix.py`: scripts autónomos.  
`SOURCE_PINS_V46.json`, `MANIFEST_SHA256_V46.json`, `verify_v46_package.py`: integridad.  
`HANDOFF_ASTRA_V46.md`: fronteras de integración y tarea futura.

**Ningún commit / merge / push.** No modificar `main`, HTML, ROOMS.exits, NPC, misiones, A07, precios, recompensas, habilidades ya cerradas ni las estadísticas de equipo. El ZIP contiene **propuestas y pruebas locales**. `T4_LIII_READY=false` y `MUTANTS_LIII_PRODUCTION=false`.