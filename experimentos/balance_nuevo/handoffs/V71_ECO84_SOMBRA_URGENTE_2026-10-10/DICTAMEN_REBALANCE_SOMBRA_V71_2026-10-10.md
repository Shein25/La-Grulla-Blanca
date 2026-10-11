# Dictamen V71 — Eco 84 HP confirmado; Sombra Ahogada LIII reequilibrada en laboratorio

**Fecha:** 2026-10-10. **Rama experimental:** `experiment/v67-cierre-guardianes-ultis-aoe-2026-10-10`. **Estado:** REBALANCE T0 DE DISEÑO SELECCIONADO / QA LAB PASS / NO HTML / NO MAIN / NO MERGE.

## Autoridad humana: Eco del Caído LII
El usuario ratificó expresamente **84 HP** para `eco_caido`, sustituyendo los 51 HP del snapshot anterior como criterio de diseño. Queda anotado en la [decisión humana](DECISION_HUMANA_ECO_HP84_Y_REAPERTURA_SOMBRA.md) y en `CATALOGO_CANONICO_MONSTRUOS_ARCO1_V3.json` (`current_design_t0_override.hp=84`). Las tres habilidades del frente V69 permanecen como diseño autorizado que exige paridad de runtime; ninguna cifra se ha sobrescrito en el HTML ni el registro de T0 histórico.

## Problema confirmado en élite LIII
`sombra_ahogada` tenía HP **51**, DEF 1, PREC 106, EVA 20, TEN 19, básico `1d2+7`; `Velo de Ahogo` aplica veneno `1d2+2` durante 3 pulsos, cada 3 rondas. Contra builds LIII legales, resultó **99,68%** victoria del jugador. Es una dificultad inadecuada para un élite único.

El usuario autorizó reabrir el balance de Sombra. Se revisaron cambios de HP y DEF, y una defensa reactiva contra golpes grandes sin ventajas por raíz. Ni convertirla en DEF2 de forma permanente ni inflarla a >100 HP ofrecía la mejor distribución entre raíces.

## Ficha candidata seleccionada: 90 HP + Espejo del Remanso
- **HP 90** (reemplaza HP 51 histórico); DEF **1** sin aumento.
- PREC **106**, EVA **20**, TEN **19**, crítico 5% ×1,5 y ataque básico `1d2+7`, sin cambios.
- **Velo de Ahogo** sin cambios: veneno `1d2+2` ×3, cadencia **3**; DOT ignora DEF, no absorción.
- **Espejo del Remanso** (`SOMBRA_ESPEJO_REMANSO`): después del **primer** ataque/acción ofensiva efectiva que quite **al menos 16 HP reales** a Sombra mientras siga viva, obtiene **16 puntos de absorción**, una sola vez por encuentro. **No absorbe el golpe que lo activa**, no cura, no otorga DEF plana y no crea turnos gratuitos. La activación debe mostrarse en las intenciones/registro reales del juego. No usar temporizadores globales.
- Sigue siendo **único, T0**; sin cadena T1–T4 ni Mutantes.

## Evidencia de balance

**Screens físicos:** 45.360 ejecuciones de HP/DEF/cadencia y 60.480 ejecuciones de variantes de Espejo; algunos escenarios comparten semillas y controles, por lo que **no se deben sumar como muestras independientes**.

**Holdout con semillas nuevas:** 51.840 combates **1v1 PRE_AOE**, divididos en cuatro brazos de **12.960 cada uno**; 5 raíces × 3 builds de 4 PT legales × 3 conjuntos (2 máximos de LII y 1 LIII opcional hipotético) × 3 políticas × 96 réplicas. Cero timeouts.

| Variante | WR jugador | Eliminación de Sombra en <=3 rondas |
|---|---:|---:|
| HP51/DEF1, T0 histórico | 99,68% | 289 |
| HP90/DEF1 sin Espejo (V68) | 75,11% | 0 |
| **HP90/DEF1 + Espejo 16 tras golpe real >=16** | **58,11%** | **0** |
| HP90/DEF1 + Espejo 12 tras golpe real >=16 | 63,06% | 0 |

**Por raíz, candidata:** Fuego **69,52%**; Metal **49,58%**; Agua **57,79%**; Tierra **50,23%**; Viento **63,43%**.
**Por equipo:** Máximo LII defensivo **58,80%**; máximo LII evasivo **44,91%**; LIII esperado **70,62%** (OPCIONAL, no concedido al cultivar).
**Por política:** STRIKE **56,32%**; DEFENSE_OPEN **55,67%**; TELEGRAPH_RESPONSE **62,34%**.

Espejo se activó en **8.309 de 12.960** peleas con la candidata y no puede activarse dos veces en una misma pelea. No se introduce protección global por elemento. Varias celdas particulares de raíz+equipo (p. ej. Fuego con equipamiento LIII esperado) pueden superar 70%: **el 58,11% es una media, no un límite artificial para cada build**.

QA: **405 comparaciones 1v1 emparejadas** del wrapper desactivado contra la fuente física E1, **0 diferencias**; 15 builds nativas validadas por guarda de 4 PT; 51.840 filas completas, sin timeouts. `V66` representa motor E1, no paridad con HTML productivo.

## Artefactos / reproducibilidad
Archivo portable **`GRULLA_V71_ECO_HP84_Y_REBALANCE_SOMBRA_LIII_2026-10-10.zip`**, SHA-256 `6a628a12659f4c3bc124f02f70b1fd34a5cdccb577385c59e488b31f5605b1ba`, 1.984.100 bytes, 17 entradas, CRC y manifiesto SHA-256 verificados. Incluye scripts, motor V66 de referencia y todos los CSV de combate. El ZIP está adjunto a la conversación, **no subido a GitHub**. Resumen máquina: [`SOMBRA_AHOGADA_T0_V71_CANDIDATA.json`](SOMBRA_AHOGADA_T0_V71_CANDIDATA.json).

## Guardas para integración posterior
1. Este cambio es **T0 candidato de diseño aprobado para evaluación**, no una sustitución automática de la fuente histórica ratificada ni un parche runtime. Confirmar humanamente la ficha final antes del cambio del registro activo.
2. Integrar el disparador sobre evento de **daño real al HP** con efectos absorbidos excluidos; Espejo no puede dispararse si murió el élite, no aplica dos veces y debe ser anunciado de forma visible.
3. Comprobar equipamiento real y momento de adquisición, narración, aflicción/antídoto, SAVE/LOAD y un solo encuentro persistido. Los sets de LIII utilizados son opcionales experimentales.
4. No se ejecutaron Ultis, AOE multiblanco, Concordancias ON ni intervención del HTML. **No adelantar esos frentes**.
5. No tocar `main`, merge, `ROOMS.exits`, spawns, misiones, tiendas, economía, drops ni balances congelados de los demás monstruos.

**Conclusión:** Sombra deja de ser trivial en la batería LIII legal: **99,68% → 58,11%** de victorias del jugador, sin convertirla en esponja de HP/DEF y preservando su veneno. El nuevo T0 necesita aprobación numérica final y después paridad productiva.