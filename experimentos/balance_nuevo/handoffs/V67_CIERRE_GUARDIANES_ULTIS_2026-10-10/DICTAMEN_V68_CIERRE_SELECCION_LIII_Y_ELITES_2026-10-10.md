# V68 — cierre de selección numérica LIII y auditoría de los élites (Sombra/Eco)

**Fecha:** 2026-10-10. **Rama:** `experiment/v67-cierre-guardianes-ultis-aoe-2026-10-10`.
**Autoridad:** avance de laboratorio y selección de referencias de diseño solicitada por el autor, NO aprobación automática de runtime ni reescritura de fichas congeladas.
**Catálogo vigente:** `experimentos/balance_nuevo/CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json` (31 identidades; 18 como conteo completo DEPRECADO).

## 1. NUEVAS SEIS ESPECIES LIII: selección T0 fijada como baseline de diseño

Se eligieron SIN retocar los perfiles candidatos originales `V45`, para conservar todo el estudio anterior. Ficha machine-readable:
`SELECCION_T0_SEIS_REPETIBLES_LIII_V67_2026-10-10.json`. Las seis especies y sus diseños están aprobados como canon; las cifras se seleccionan aquí como **baseline numérico de diseño**. Las seis siguen **NO_RUNTIME_READY**: faltan paridad, confirmación explícita de Control=0, estado de gate y validación de adquisición; **no modificar `stats_status` de origen ni `technique.params_status` a READY** solo por selección.

| Monstruo | HP | PREC | EVA | DEF | TEN | Básico | Especial |
|---|---:|---:|---:|---:|---:|---|---|
| Garza de Bruma de Roca | 75 | 109 | 31 | 0 | 14 | 1d2+6 | Pico Niebla 1d3+8 / CD3 |
| Cangrejo de Laja Húmeda | 90 | 98 | 9 | 3 | 28 | 1d2+6 | Tenaza 1d3+8 / CD4 |
| Sanguijuela de Remanso Turbio | 78 | 103 | 16 | 1 | 16 | 1d2+6 | Mordida 1d2+7 + veneno 1d2+2 ×2 / CD3 |
| Salamandra de Filtración Tibia | 79 | 103 | 16 | 2 | 22 | 1d2+6 | Salpicadura 1d2+7 + quemadura 1d2+1 ×2 / CD4 |
| Rana de Cascajo del Barranco | 84 | 100 | 17 | 2 | 23 | 1d2+6 | Salto 1d3+8 / CD3 |
| Carpa de Lámina Reflejada | 78 | 104 | 26 | 1 | 13 | 1d2+6 | Succión 1d3+7 + drenaje 3 Qi / CD3 |

**Estado adaptativo:** V46 T1/T2/T3/T4 y nuevos Mutantes continúan **NO RATIFICADOS**. Aunque V47 ejecutó 48.000 combates y V48 2.054.400 mezclados y V63 129.024 contra ocho LIII, la evidencia no es una ratificación secuencial; la Sanguijuela T4 Mutante del gate V63 castiga mucho a Metal y merece pantalla focal causal. No reclamar cierre completo de sistema.

## 2. Conflicto de autoridad histórico que no hay que ignorar

Hay **DOS ramas/documentos discordantes**, ambos reales:
1. Commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35`, fecha de commit 2026-10-02, registro histórico que declara `eco_caido`, `sombra_ahogada` READY y `UNIQUE_T0_CLOSED_NO_T1_T4`; para `pez_lunar`, `anguila_estelar` declara READY y `ADAPTIVE_CHAIN_T0_T4_CLOSED`. Es una fuente cerrada antigua con valores diferentes.
2. Rama activa PRE-A08/ V66 `experiment/lii-tramo1-multirraiz-v08-2026-10-08` y `handoff/v66-guardianes-aoe-2026-10-10`: blob `c0d2131f2cc8dbbb96babf9711c197e54fe97591`, todos estos perfiles siguen `PENDING_INTEGRAL_REBALANCE`. Los informes posteriores V39 (2026-10-09), V44/V45/V47/V48/V63 prueban candidatos nuevos pero no declaran el source registry READY.

**REGLA DE CONFLICTO:** no elegir silenciosamente la rama conveniente, no sobrescribir T0/tiers ratificados del blob 45c3, no promover P5/A5 o `m11`/E8 solo porque una rama posterior esté desactualizada. Reconciliar linaje, decisiones humanas y runtime antes de integrar números. Este laboratorio no altera ninguno de los registros originales.

## 3. Sombra Ahogada — élite LIII (NO retocar ratificación antigua automáticamente)

El laboratorio micro V03 2026-10-01 ensayó 46.400 combates con 14 candidatos CLEAN, eligió como shortlist `m11` (HP51/PREC106/EVA20/DEF1/TEN19, básico 1d2+7, veneno `1d2+2×3` / cadence3); el commit 45c3 (2026-10-02) ya lleva exactamente esa ficha T0 READY/cerrada. La rama V66 sin sincronizar marca PENDING.

Se ejecutó un estudio nuevo en entorno físico E1 1v1 PRE_AOE para detectar impacto de progresión, **NO para reabrir Sombra**:
- 17.280 comparaciones iniciales con m11/m07/m05 en resolver base.
- 28.800 escenarios nuevos SCREEN de HP/DEF/cadencia (escala y peligro evaluados; diferencias importantes por raíz).
- 37.800 escenarios SCREEN usando resolver V61-C de habilidades nativas de cinco raíces, equipo max LII DEF/EVA y equipamiento III opcional, 3 builds, 3 políticas, R40.
- **38.880 combates HOLDOUT nuevos con semillas distintas**: tres brazos sobre 12.960 contextos cada uno (5 raíces ×3 builds ×3 equipos ×3 políticas ×96 semillas). Semillas iniciales compartidas entre brazos; consumo futuro de RNG puede divergir; 0 timeouts.

| Candidato | WR jugador HOLDOUT 1v1 | Kills <=3 rondas |
|---|---:|---:|
| m11 T0 ratificado en otra rama (51 HP) | **99,73%** | 315 |
| **HP90/DEF1/veneno original CD3 — RECOMENDACIÓN NUEVA NO RATIFICADA** | **75,54%** | 0 |
| HP90/DEF2/CD3 — alternativa más exigente NO RATIFICADA | 62,20% | 0 |

La opción HP90/DEF1 conserva PREC106, EVA20, TEN19, BASIC 1d2+7 y DOT veneno 1d2+2 ×3; no crear habilidad nueva. Aun así difiere de una ficha congelada; **no escribirla en canon sin reapertura aprobada expresamente**, y no convertir % de WIN en un objetivo rígido.

Por raíz, el HP90/DEF1 en HOLDOUT da Fuego 86,77%; Metal 70,72%; Agua 69,14%; Tierra 65,70%; Viento 85,38%. Por equipo: max LII DEF 76,97%; max LII EVA 64,38%; LIII opcional 85,28%. Estas diferencias sugieren comprobación eventual de acceso/Concordancias/aflicción post-combate antes de reemplazar el T0 histórico.

## 4. Eco del Caído — élite PENDIENTE en handoff PRE-A08 V39

**Frente humano abierto correcto:** `eco_caido`, no la Sombra ya congelada en 45c3. V39, autoridad de continuidad del 2026-10-09, documenta E8 **NO RATIFICADO**: HP84, PREC96, EVA18, DEF1, TEN18, básico 1d2+4, sin especial, Control=0 solo fixture.

V39 (18.240 combates nuevos + 2.160 COLD) mostró:
- Si se alcanza ocultamente desde LI en `cruce_vetas` (en ver74; acceso ver76 no certificado): player LI solo ofensiva prólogo vence **9,69%**.
- Jugador LII prólogo ofensiva **69,43%**; post-M03 ofensiva **70,52%**; post-M03 defensiva no acreditada **81,41%**.
- Con Sobretúnica M04 OPCIONAL DEF2/HP2: ofensiva **96,67%**, defensiva hipotética **98,80%**. No nerfear esa vestidura.
- Dilema: encuentro oculto disponible sin gate en ver74, **no** prueba en ver76. No inventar gate ni decidir automáticamente que sea jefe para LI.

Nuevo ensayo físico focal `ECO_ELITE_V39_E8_QI_SCREEN_RESULTS.csv`: **15.360 combates** (5 raíces ×3 builds T1 legal LII ×2 equipos fuertes LII ×2 políticas ×64 semillas ×4 brazos), 0 timeouts. Se comparó E8 sin especial y tres hipotéticas técnicas directas con QI_DRAIN 4/6/8 por golpe de cadencia3, usando solo un mecanismo que el motor ya soporta. No hay autorización para añadir ese especial canónico:

| E8 + hipótesis | WR jugador total LII fuerte | WR con equipo max LII DEF |
|---|---:|---:|
| Sin especial | 99,38% | 99,95% |
| Drenaje 4 Qi / CD3 | 99,01% | 99,95% |
| Drenaje 6 Qi / CD3 | 98,83% | 99,95% |
| Drenaje 8 Qi / CD3 | 98,57% | 99,95% |

**Conclusión causal LIMITADA:** el drenaje Qi sobre impacto no arregla la amenaza contra armadura DEF2, NO aprobarlo por inercia; nuestra pantalla usa E1 T0 más gear MAX LII, no reemplaza el estudio de adquisición legal de V39 con equipo prólogo real.

**Bloqueantes del cierre serio del Eco:**
- Decidir si el acceso secreto LI es un riesgo intencional o si se activa mediante estado de progresión EXISTENTE; no crear nuevas salas/gates ni alterar `ROOMS.exits`.
- Elegir mecánica auténtica propia del élite que cree contrajuego ante equipo LII superior, NO ataque básico inflado o nerf de equipo. Ni E8 sin especial ni pequeño drenaje satisfacen el objetivo observado.
- Conciliar el B06 antiguo de 45c3 (HP51) con E8 posterior sin autorizar T0 conflictivos y `control=0` no confirmado.
- Correr paridad de eventos con técnicas, antídotos/consumibles, SAVE/LOAD, si se integrará, y responder paso de LI a LII.

**Dictamen de Eco:** `E8_BASELINE_BEST_SUPPORTED_BUT_UNRATIFIED / NEW_QI_DRAIN_VARIANTS_REJECTED_AS_INEFFECTIVE / NUMERIC_T0_NOT_CLOSED`. **No es correcto decir «Eco balanceado definitivamente».**

## 5. Contrato de cierre antes de AOE
AOE POST_MANUAL no se ha probado de manera real multiblanco. Para cerrar el programa antes de AOE aún faltan:
1. T0 formal de seis nuevos LIII con Control, skills y contrato de runtime; paso de baseline seleccionado a READY solo tras paridad.
2. T1→T4/Mutantes secuenciales nuevos LIII con aprobación de magnitudes y event QA, sin tocar T0 de especies antiguas congeladas.
3. Decisión humana de acceso y mecánica élite Eco, diseño y ensayo legal, sin sustituir original ratificado.
4. Resolver AOE 1/2/3 hostiles legalmente presentes, una acción/un Qi, antes de cualquier WR de área.

Guardas: no main, no merge, no HTML, no ROOMS.exits, no T0 congelado, no spawns, no NPC, no ítems ni economía.
